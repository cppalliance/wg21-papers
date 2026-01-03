# Executor Storage: `executor_ref` vs. Abstract Base Class

**Research Question:** Can we reduce memory overhead by replacing `executor_ref` (16 bytes) with a pointer to an abstract base class (8 bytes) in task promises?

## Current Architecture

```
async_run(Executor ex, task t)
    └── root_task<Executor>::promise_type
            └── Executor ex_;              // BY VALUE (concrete, templated)
                    ▲
                    │ executor_ref points here
                    │
            task::promise_type
                └── executor_ref ex_;        // 16 bytes (ops* + void*)
                └── executor_ref caller_ex_; // 16 bytes (ops* + void*)
```

The `executor_ref` is a type-erased wrapper storing two pointers:

```cpp
struct executor_ref {
    ops const* ops_;   // pointer to static vtable
    void const* ex_;   // pointer to executor object
};
```

## Proposed Architecture

```
async_run(Executor ex, task t)
    └── root_task<Executor>::promise_type
            └── Executor ex_;              // BY VALUE, Executor : executor_base
                    ▲
                    │ executor_base* points here
                    │
            task::promise_type
                └── executor_base* ex_;        // 8 bytes
                └── executor_base* caller_ex_; // 8 bytes
```

Executors derive from an abstract base:

```cpp
struct executor_base {
    virtual ~executor_base() = default;
    virtual coro dispatch(coro h) const = 0;
    virtual void post(work* w) const = 0;
};

struct io_context::executor : executor_base {
    io_context* ctx_;
    coro dispatch(coro h) const override { return h; }
    void post(work* w) const override { ctx_->q_.push(w); }
};
```

**Key insight:** External APIs remain unchanged. `io_context::get_executor()` still returns `executor` by value. The abstract base is only visible in internal promise storage.

## Memory Analysis

### Per-Component Overhead

| Location | `executor_ref` | `executor_base*` |
|----------|---------------|------------------|
| `root_task::promise_type` | 8 bytes | 16 bytes (+8 vptr) |
| `task::promise_type` | 32 bytes | 16 bytes |

### Total Memory for N Nested Tasks

| Design | Formula | N=1 | N=4 | N=10 | N=100 |
|--------|---------|-----|-----|------|-------|
| `executor_ref` | 8 + 32N | 40 | 136 | 328 | 3208 |
| `executor_base*` | 16 + 16N | 32 | 80 | 176 | 1616 |
| **Savings** | 16N - 8 | 8 | **56** | **152** | **1592** |

Break-even at N = 0.5. **For any nesting depth ≥ 1, abstract base uses less memory.**

## Indirection Analysis

### `executor_ref::dispatch(h)`

```cpp
coro dispatch(coro h) const { return ops_->dispatch_coro(ex_, h); }
```

Assembly pattern:
```asm
mov rax, [this]          ; 1. load ops_ from executor_ref
mov rdi, [this + 8]      ; 2. load ex_ from executor_ref
mov rax, [rax]           ; 3. load function pointer from static ops
call rax                 ; 4. indirect call(ex_, h)
```

**Memory accesses:**
1. Promise (hot) — 2 loads (`ops_`, `ex_`)
2. Static ops table (cold) — 1 load

### `executor_base*->dispatch(h)`

```cpp
ex_->dispatch(h);  // virtual call
```

Assembly pattern:
```asm
mov rax, [this]          ; 1. load ex_ from promise
mov rcx, [rax]           ; 2. load vptr from executor object
mov rax, [rcx + offset]  ; 3. load function pointer from vtable
call rax                 ; 4. indirect call(this, h)
```

**Memory accesses:**
1. Promise (hot) — 1 load (`ex_`)
2. Executor object (warm) — 1 load (vptr)
3. Static vtable (cold) — 1 load

### Comparison

| Metric | `executor_ref` | `executor_base*` |
|--------|---------------|------------------|
| Total loads | 3 | 3 |
| Loads from promise | 2 | 1 |
| Loads from executor object | 0 | 1 |
| Loads from static table | 1 | 1 |

**Total indirection cost is equivalent.**

## Cache Behavior

### `dispatch()` Path

- **`executor_ref`**: Both `ops_` and `ex_` are in the promise (same cache line). Static ops table may be cold.
- **`executor_base*`**: `ex_` is in promise; must chase pointer to executor object for vptr. Static vtable may be cold.

Slight advantage to `executor_ref` when only calling `dispatch()`.

### `post()` Path

```cpp
void post(work* w) const { ctx_->q_.push(w); }
```

Both designs must access `ctx_` in the executor object. With `executor_base*`, the vptr is in the same cache line as `ctx_`, making the vptr access effectively free.

**Advantage to `executor_base*` when calling `post()`.**

### Benchmark Hot Paths

| Operation | Location | Calls |
|-----------|----------|-------|
| `final_suspend` | `caller_ex_.dispatch()` | Every task completion |
| `read_state::operator()` | `ex_.dispatch()` | Every I/O completion |
| `do_read_some` | `ex.post()` | Every I/O initiation |

The benchmark has roughly equal dispatch and post calls, making the cache behavior a wash.

## Lifetime Guarantee

The concrete `Executor` is stored by value in `root_task<Executor>::promise_type`:

```cpp
template<class Executor>
struct root_task {
    struct promise_type {
        Executor ex_;  // concrete executor lives here
        // ...
    };
};
```

All nested `task` promises store pointers back to this executor. The `root_task` self-destructs only at `final_suspend`, after all nested tasks have completed. **Lifetime is guaranteed by construction.**

## Implementation Changes Required

### New Abstract Base

```cpp
struct executor_base {
    virtual ~executor_base() = default;
    virtual coro dispatch(coro h) const = 0;
    virtual void post(work* w) const = 0;
};
```

### Modified `io_context::executor`

```cpp
struct io_context::executor : executor_base {
    io_context* ctx_;
    coro dispatch(coro h) const override { return h; }
    void post(work* w) const override { ctx_->q_.push(w); }
    // ... rest unchanged
};
```

### Modified `task::promise_type`

```cpp
struct promise_type {
    executor_base* ex_;         // was: executor_ref ex_;
    executor_base* caller_ex_;  // was: executor_ref caller_ex_;
    coro continuation_;
    // ...
};
```

### Modified `socket::read_state`

```cpp
struct read_state : work {
    coro h_;
    executor_base* ex_;  // was: executor_ref ex_;
    // ...
};
```

## Summary

| Criterion | `executor_ref` | `executor_base*` | Winner |
|-----------|---------------|------------------|--------|
| Memory per task | 32 bytes | 16 bytes | **Abstract** |
| Memory (root only) | 8 bytes | 16 bytes | executor_ref |
| Net memory (N ≥ 1) | 8 + 32N | 16 + 16N | **Abstract** |
| dispatch() cache | 2 hot + 1 cold | 1 hot + 1 warm + 1 cold | Tie |
| post() cache | 2 hot + 1 cold + ctx | 1 hot + vptr free + 1 cold | **Abstract** |
| External API | unchanged | unchanged | Tie |
| Implementation | manual vtable | standard inheritance | Tie |

## Conclusion

**The abstract base design is superior for coroutine-based I/O:**

1. **Memory savings scale with composition depth.** Each nested task saves 16 bytes. For the 4-level benchmark (session → request → read → I/O), this is 56 bytes per call chain.

2. **Indirection cost is equivalent.** Both designs perform 3 memory loads per virtual call. The access patterns differ but total cost is the same.

3. **Cache behavior favors abstract base for `post()`.** The vptr shares a cache line with executor data that must be accessed anyway.

4. **External API is unchanged.** Users continue to work with concrete executor types. The abstract base is an implementation detail.

5. **Lifetime is trivially safe.** The root task owns the concrete executor; nested tasks hold pointers to it.

**Recommendation:** Replace `executor_ref` with `executor_base*` in promise types. The 8-byte vptr overhead in `root_task` is amortized across all nested tasks, yielding net memory savings for any composition depth ≥ 1.
