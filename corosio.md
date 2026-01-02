# Coroutine-First Asynchronous I/O: A Type-Erased Affine Framework

## Abstract

This paper presents a coroutine-first asynchronous I/O framework that achieves executor flexibility without sacrificing encapsulation. We introduce the *affine awaitable protocol*, a technique for propagating execution context through coroutine chains without embedding executor types in public interfaces. Platform I/O types and their operation states remain hidden in translation units, while composed algorithms expose only `task` return types. We compare allocation behavior and performance against traditional callback-based designs, revealing that coroutines trade a fixed overhead for superior scaling at depth.

---

## 1. The Problem: Callback Hell Meets Template Hell

Traditional asynchronous I/O frameworks face an uncomfortable choice. The callback model—templated on executor and completion handler—achieves zero-overhead abstraction but leaks implementation details into every public interface:

```cpp
template<class Executor, class Handler>
void async_read(Executor ex, Handler&& handler);
```

Every composed operation must propagate these template parameters, creating a cascade of instantiations. The executor type, the handler type, and often an allocator type all become part of the function signature. Users cannot hold heterogeneous operations in containers. Libraries cannot define stable ABIs. The "zero-cost abstraction" exacts its price in compile time, code size, and API complexity.

Type erasure offers an escape, but the traditional approach—`std::function` for handlers, `any_executor` for executors—introduces heap allocations at every composition boundary. Our benchmarks show this penalty compounds: a four-level operation using fully type-erased callbacks allocates 601 times per invocation and runs 5.6× slower than native templates.

We sought a third path.

---

## 2. Motivation: Why Not the Networking TS?

The Networking TS (and its progenitor Boost.Asio) is the de facto standard for asynchronous I/O in C++. It is mature, well-tested, and supports coroutines through completion tokens. Why build something new?

### 2.1 The Template Tax

The Networking TS design philosophy—zero-overhead abstraction through templates—incurs costs that compound in large codebases:

**Every async operation signature includes executor and handler types:**
```cpp
template<class Executor, class ReadHandler>
void async_read(basic_socket<Protocol, Executor>& s,
                MutableBufferSequence const& buffers,
                ReadHandler&& handler);
```

**Composed operations propagate these types:**
```cpp
template<class Executor, class Handler>
void async_http_request(basic_socket<tcp, Executor>& sock,
                        http::request const& req,
                        Handler&& handler);
```

This creates:
- **N×M template instantiations** for N operations × M executor/handler combinations
- **Header-only dependencies** that must be recompiled on change
- **Binary size growth** that can reach megabytes in complex applications
- **Compile times measured in minutes** for moderate codebases

### 2.2 The Encapsulation Problem

The Networking TS templates expose implementation details through public interfaces:

```cpp
// User sees:
class http_client
{
public:
    template<class Executor, class Handler>
    void async_get(Executor ex, std::string url, Handler&& h);
};
```

The user is forced to know:
- What executor types are valid
- What handler signatures are expected
- That the implementation uses sockets at all

Platform types (`OVERLAPPED`, `io_uring_sqe`) are hidden, but the *structure* of the async machinery leaks through every API boundary.

**Our approach:**
```cpp
class http_client
{
public:
    task async_get(std::string url);  // That's it.
};
```

The implementation—sockets, buffers, executors—lives in the translation unit. The interface is stable. The ABI is stable. Compilation is fast.

### 2.3 Translation Unit Benefits

Hiding implementation in `.cpp` files provides:

1. **ABI Stability**: Library interfaces don't change when implementation details change. Users don't recompile when you switch from `epoll` to `io_uring`.

2. **Compile Time**: Incremental builds recompile only changed translation units. Header changes don't cascade through the dependency graph.

3. **Encapsulation**: Platform-specific types (`OVERLAPPED`, `HANDLE`, `io_uring_sqe`) never appear in headers. Mocking and testing become trivial.

4. **Binary Size**: One instantiation per function, not one per template argument combination.

### 2.4 Coroutine-Compatible vs Coroutine-First

The Networking TS added coroutine support through completion tokens like `use_awaitable`:

```cpp
co_await async_read(socket, buffer, use_awaitable);
```

This adapts callback-based operations for coroutines. It works, but:
- **Double indirection**: Callback machinery wraps coroutine machinery
- **Executor handling is manual**: `co_spawn` and `bind_executor` required
- **Error handling diverges**: Exceptions vs `error_code` vs `expected`
- **Mental model mismatch**: Writing coroutines that think in callbacks

Our design is **coroutine-first**: the suspension/resumption model is the foundation, not an adapter. Executor propagation is automatic. Type erasure is structural. The callback path (`dispatch().resume()`) is the compatibility layer, not the other way around.

### 2.5 When to Use the Networking TS Instead

The Networking TS remains the right choice when:
- You need callback-based APIs for C compatibility
- Template instantiation cost is acceptable
- You're already invested in the Asio ecosystem
- Maximum performance with zero abstraction is required
- Standardization timeline matters for your project

Our framework is better suited when:
- Coroutines are the primary programming model
- Public APIs must hide implementation details
- Compile time and binary size matter
- ABI stability is required across library boundaries
- Clean, simple interfaces are prioritized

---

## 3. The Insight: Coroutines as Natural Type Erasure

C++20 coroutines provide type erasure *by construction*—but not through the handle type. `std::coroutine_handle<void>` and `std::coroutine_handle<promise_type>` are both just pointers with identical overhead. The erasure that matters is *structural*:

1. **The frame is opaque**: Callers see only a handle, not the promise's layout
2. **The return type is uniform**: All coroutines returning `task` have the same type, regardless of body
3. **Suspension points are hidden**: The caller doesn't know where the coroutine may suspend

This structural erasure is often lamented as overhead, but we recognized it as opportunity: *the allocation we cannot avoid can pay for the type erasure we need*.

The key insight is that a coroutine's promise can store execution context *by reference*, receiving it from the caller at suspension time rather than at construction time. This deferred binding enables a uniform `task` type that works with any executor, without encoding the executor type in its signature.

---

## 4. The Executor Model

We define an executor as any type satisfying the `is_executor` concept:

```cpp
template<class T>
concept is_executor = requires(T const& t, coro h, work* w) {
    t.dispatch(h);      // Resume coroutine inline
    t.post(w);          // Queue work for later execution
    { t == t } -> std::convertible_to<bool>;
};
```

The distinction between `dispatch` and `post` is fundamental:
- **dispatch**: Immediately invoke the coroutine. Used when resuming on the correct executor.
- **post**: Enqueue work for the event loop. Used for I/O completion and cross-executor transitions.

Executors must be equality-comparable to enable optimizations when source and target executors are identical.

### 4.1 Type-Erased Executor Reference

To store executors without encoding their type, we introduce `executor_ref`—a non-owning, type-erased reference:

```cpp
struct executor_ref
{
    struct ops
    {
        void (*dispatch_coro)(void const*, coro) = nullptr;
        void (*post_work)(void const*, work*) = nullptr;
        bool (*equals)(void const*, void const*) = nullptr;
    };

    template<class Executor>
    static constexpr ops ops_for{ /* lambdas */ };

    ops const* ops_ = nullptr;
    void const* ex_ = nullptr;
};
```

The `ops` table has static storage duration, instantiated once per executor type. The executor itself is stored by pointer, assuming the referent outlives the reference. This is safe because executors are typically owned by I/O contexts with longer lifetimes than any operation.

Equality comparison short-circuits on the `ops_` pointer—if two references have different operation tables, they wrap different types and cannot be equal:

```cpp
bool operator==(executor_ref const& other) const noexcept
{
    return ops_ == other.ops_ && ops_->equals(ex_, other.ex_);
}
```

### 4.2 Executor Composition and Placement

A subtle but important property: executor types are fully preserved at call sites even though they're type-erased internally. This enables zero-overhead composition at the API boundary while maintaining uniform internal representation.

**Composable executor wrappers work naturally:**

```cpp
template<class Ex>
struct strand {
    Ex inner_;
    
    coro dispatch(coro h) const {
        // Serialization logic, then delegate to inner
        return inner_.dispatch(h);
    }
    // ...
};

// Full type information at the call site
strand<pool_executor> s{pool.get_executor()};
async_run(s, my_task());  // strand<pool_executor> passed by value
```

When `async_run` stores the executor in the root task's frame, it preserves the complete type. The `strand` wrapper's serialization logic remains inlinable. Only when the executor propagates to child tasks—as `executor_ref`—does type erasure occur. The erasure boundary is pushed to where it matters least: internal propagation rather than the hot dispatch path.

**Why the executor belongs at the call site, not on the I/O object:**

- **The caller knows the concurrency requirements.** A multithreaded `io_context` may need strand-wrapped executors; a single-threaded context may not. The socket cannot know this—it only knows how to perform I/O.

- **I/O objects become context-agnostic.** A socket works identically whether wrapped in a strand, run on a thread pool, or executed on a single-threaded context. The same socket type serves all deployment scenarios.

- **Composition happens at the edge.** Users compose executors (`strand<pool_executor>`, `priority_executor<strand<...>>`) at the point of use. The I/O object doesn't need N template parameters for N possible wrapper combinations.

**The coroutine advantage:**

Traditional callback-based designs often embed the executor in the I/O object's type, creating signatures like `basic_socket<Protocol, Executor>`. This leaks concurrency policy into type identity—two sockets with different executors have different types, complicating containers and APIs.

Coroutines invert this relationship. The executor enters at `async_run` or `run_on`, propagates invisibly through `executor_ref`, and reaches I/O operations via the affine awaitable protocol's `await_transform`. The I/O object participates in executor selection without encoding it in its type:

```cpp
// Traditional: executor embedded in socket type
basic_socket<tcp, strand<pool_executor>> sock;

// Coroutine model: executor supplied at launch
socket sock;  // No executor type parameter
async_run(strand{pool.get_executor()}, use_socket(sock));
```

The socket receives its executor indirectly—through the coroutine machinery—yet still benefits from the caller's choice of strand wrapping, thread pool, or any other executor composition.

---

## 5. Platform I/O: Hiding the Machinery

A central goal is encapsulation: platform-specific types (`OVERLAPPED`, `io_uring_sqe`, file descriptors) should not appear in public headers. We achieve this through *preallocated, type-erased operation state*.

### 5.1 The Socket Abstraction

```cpp
struct socket
{
    socket() : op_(new state) {}

    async_awaitable async_io();

private:
    struct state : work
    {
        coro h_;
        executor_ref ex_;
        // OVERLAPPED, HANDLE, etc. — hidden here
        
        void operator()() override
        {
            ex_.dispatch(h_);
        }
    };

    std::unique_ptr<state> op_;
};
```

The `state` structure:
1. Inherits from `work`, enabling intrusive queuing
2. Stores the coroutine handle and executor reference needed for completion
3. Contains platform-specific members (OVERLAPPED, handles) invisible to callers
4. Is allocated *once* at socket construction, not per-operation

### 5.2 Intrusive Work Queue

Submitted work uses an intrusive singly-linked list:

```cpp
struct work
{
    virtual ~work() = default;
    virtual void operator()() = 0;
    work* next = nullptr;
};
```

This design eliminates container allocations—each work item carries its own link. The `queue` class manages head and tail pointers with O(1) push and pop. Combined with the preallocated socket state, I/O operations require *zero allocations* in steady state.

---

## 6. The Affine Awaitable Protocol

The core innovation is how execution context flows through coroutine chains. We extend the standard awaitable protocol with an *affine* overload of `await_suspend` that returns a coroutine handle for symmetric transfer:

```cpp
template<class Executor>
std::coroutine_handle<> await_suspend(coro h, Executor const& ex) const;
```

This two-argument form receives both the suspended coroutine handle and the caller's executor, and returns the next coroutine to resume. The caller's promise uses `await_transform` to inject the executor:

```cpp
template<class Awaitable>
auto await_transform(Awaitable&& a)
{
    struct transform_awaiter
    {
        std::decay_t<Awaitable> a_;
        promise_type* p_;
        
        auto await_suspend(std::coroutine_handle<Promise> h)
        {
            return a_.await_suspend(h, p_->ex_);  // Inject executor, return handle
        }
    };
    return transform_awaiter{std::forward<Awaitable>(a), this};
}
```

This mechanism achieves implicit executor propagation: child coroutines inherit their parent's executor without explicit parameter passing.

### 6.1 Symmetric Transfer

A critical design decision is that `await_suspend` returns `std::coroutine_handle<>` rather than `void`. When `await_suspend` returns a handle, the runtime resumes that coroutine *without growing the stack*—effectively a tail call. This prevents stack overflow in deep coroutine chains.

Without symmetric transfer:
```
A finishes → dispatch(B) → B finishes → dispatch(C) → ...
                ↓                          ↓
           stack grows              stack grows more
```

With symmetric transfer:
```
A finishes → return B → runtime resumes B → return C → runtime resumes C
             (constant stack depth)
```

The executor's `dispatch` method also returns a handle:

```cpp
coro dispatch(coro h) const
{
    return h;  // Return handle for symmetric transfer
}
```

If the executor must post rather than dispatch (cross-thread), it returns `std::noop_coroutine()`.

### 6.2 Sender/Receiver Compatibility

The design is compatible with P3352R3 and `std::execution`. The `dispatch()` method returns a `std::coroutine_handle<>` that can be used in two ways:

- **Symmetric transfer** (coroutine context): Return the handle from `await_suspend`
- **Explicit resume** (sender context): Call `handle.resume()` directly

```cpp
// In a sender's completion:
ex.dispatch(continuation).resume();
```

If `dispatch()` posts work rather than dispatching inline, it returns `std::noop_coroutine()`. Calling `.resume()` on this is defined as a no-op, making the API safe in all contexts:

```cpp
coro dispatch(coro h) const
{
    return h;  // Return for symmetric transfer OR explicit resume
}

// Coroutine caller:
return ex.dispatch(h);        // Symmetric transfer

// Sender/callback caller:
ex.dispatch(h).resume();      // Explicit resume, noop if posted
```

This means one executor interface serves both coroutines and senders with no conditional code paths.

### 6.3 The Task Type

The `task` type represents a lazy, composable coroutine:

```cpp
struct task
{
    struct promise_type
    {
        executor_ref ex_;           // Where this task runs
        executor_ref caller_ex_;    // Where to resume caller
        coro continuation_;          // Caller's coroutine handle
        // ...
    };

    std::coroutine_handle<promise_type> h_;
    bool has_own_ex_ = false;
};
```

When awaited, a task:
1. Stores the caller's continuation and executor
2. Either inherits the caller's executor (default) or uses its own (if `set_executor` was called)
3. Returns the child's handle for symmetric transfer (or `noop_coroutine()` if posted)

At completion (`final_suspend`), the task returns the continuation for symmetric transfer:

```cpp
std::coroutine_handle<> await_suspend(coro h) const noexcept
{
    std::coroutine_handle<> next = std::noop_coroutine();
    if(p_->continuation_)
        next = p_->caller_ex_.dispatch(p_->continuation_);
    h.destroy();
    return next;
}
```

---

## 7. Executor Switching: The `run_on` Primitive

Any coroutine can switch executors mid-operation using `run_on`:

```cpp
template<class Executor>
task run_on(Executor const& ex, task t)
{
    t.set_executor(ex);
    return t;
}

// Usage:
co_await run_on(other_executor, some_operation());
```

When awaited, a task with its own executor posts a starter work item to that executor rather than resuming inline. Upon completion, it dispatches back to the *caller's* executor—not its own—ensuring seamless return to the original context.

This separation of `ex_` (where I run) and `caller_ex_` (where my caller resumes) enables crossing executor boundaries without explicit continuation management.

---

## 8. Launching the Root: Executor Lifetime

Top-level coroutines present a lifetime challenge: the executor must outlive all operations, but the coroutine owns only references. We solve this with a wrapper coroutine that *owns* the executor:

```cpp
template<class Executor>
struct root_task
{
    struct promise_type
    {
        Executor ex_;  // Owned by value
        // ...
    };
    std::coroutine_handle<promise_type> h_;
};

template<class Executor>
void async_run(Executor ex, task t)
{
    auto root = wrapper<Executor>(std::move(t));
    root.h_.promise().ex_ = std::move(ex);
    
    // Post starter to begin execution
    root.h_.promise().ex_.post(new starter{root.h_});
    root.release();
}
```

The `root_task` frame lives on the heap and contains the executor by value. All child tasks receive `executor_ref` pointing into this frame. The frame self-destructs at `final_suspend`, after all children have completed.

This design imposes overhead only at the root—intermediate tasks pay nothing for executor storage.

---

## 9. Frame Allocator Customization

The default coroutine allocation strategy—one heap allocation per frame—is suboptimal for repeated operations. We introduce a *frame allocator protocol* that allows I/O objects to provide custom allocation strategies.

### 9.1 The Frame Allocator Concepts

```cpp
template<class A>
concept frame_allocator = requires(A& a, void* p, std::size_t n) {
    { a.allocate(n) } -> std::convertible_to<void*>;
    { a.deallocate(p, n) } -> std::same_as<void>;
};

template<class T>
concept has_frame_allocator = requires(T& t) {
    { t.get_frame_allocator() } -> frame_allocator;
};
```

The `has_frame_allocator` concept allows I/O objects to opt-in explicitly by providing a `get_frame_allocator()` member function.

### 9.2 Why I/O Objects?

The frame allocator lives on I/O objects rather than the executor or root task—a Goldilocks choice that balances accessibility, lifetime, and efficiency:

- **The executor is type-erased.** Our design propagates `executor_ref` through coroutine chains. Type erasure means the executor cannot carry concrete allocator state without either templating on allocator type (defeating type erasure) or adding another indirection layer (adding overhead).

- **The root task is too distant.** While the root task owns the executor by value, intermediate coroutines only see `executor_ref`. Tunneling allocator access through every `co_await` would add indirection costs, and the allocation pattern wouldn't match the I/O pattern.

- **I/O objects have the right lifetime.** A socket outlives its operations. Frames for `socket.async_read()` are allocated when the call begins and freed when it completes—while the socket remains alive. The allocator naturally follows the object initiating the operation.

- **Locality of allocation sizes.** Operations on the same I/O object tend to produce similar frame sizes. A socket's read operations all generate roughly equal frames. Per-object pools achieve better cache locality and recycling efficiency than global pools shared by unrelated operations.

- **C++20 machinery supports it naturally.** The `promise_type::operator new` overloads receive coroutine parameters directly. Detecting `has_frame_allocator` on the first or second parameter is zero-overhead—no runtime dispatch, no extra storage. The I/O object is already there as the natural first argument.

- **A global fallback handles everything else.** Coroutines without I/O object parameters—lambdas, wrappers, pure computation—fall back to a global frame pool. Universal recycling without universal plumbing.

### 9.3 Task Integration

The `task::promise_type` overloads `operator new` to detect frame allocator providers:

```cpp
struct promise_type
{
    // First parameter has get_frame_allocator()
    template<has_frame_allocator First, class... Rest>
    static void* operator new(std::size_t size, First& first, Rest&...);

    // Second parameter (for member functions where this comes first)
    template<class First, has_frame_allocator Second, class... Rest>
    static void* operator new(std::size_t size, First&, Second& second, Rest&...)
        requires (!has_frame_allocator<First>);

    // Default: no frame allocator
    static void* operator new(std::size_t size);

    static void operator delete(void* ptr, std::size_t size);
};
```

When a coroutine's first or second parameter satisfies `has_frame_allocator`, the frame is allocated from that object's allocator. Otherwise, the global heap is used.

### 9.4 Allocation Tagging

To enable unified deallocation, we prepend a header to each frame:

```cpp
struct alloc_header
{
    void (*dealloc)(void* ctx, void* ptr, std::size_t size);
    void* ctx;
};
```

The header stores a deallocation function pointer and context. When `operator delete` is called, it reads the header to determine whether to use the custom allocator or the global heap.

### 9.5 Thread-Local Frame Pool

I/O objects implement `get_frame_allocator()` returning a pool with thread-local caching:

```cpp
class frame_pool
{
    void* allocate(std::size_t n)
    {
        // 1. Try thread-local free list
        // 2. Try global pool (mutex-protected)
        // 3. Fall back to heap
    }

    void deallocate(void* p, std::size_t)
    {
        // Return to thread-local free list
    }
};
```

After the first iteration, frames are recycled without syscalls. The global pool handles cross-thread returns safely.

---

## 10. Allocation Analysis

With recycling enabled for both models, we achieve zero steady-state allocations:

| Operation | Callback (recycling) | Coroutine (pooled) |
|-----------|---------------------|-------------------|
| async_io (1 level) | 0 | 0 |
| async_read_some (2 levels) | 0 | 0 |
| async_read (3 levels) | 0 | 0 |
| async_request (100 iterations) | 0 | 0 |

### 10.1 The Critical Insight: Recycling Matters for Both

A naive implementation of either model performs poorly. Without recycling:
- **Callbacks**: Each I/O operation allocates and deallocates operation state
- **Coroutines**: Each coroutine frame is heap-allocated and freed

The key optimization for *both* models is **thread-local recycling**: caching recently freed memory for immediate reuse by the next operation.

### 10.2 Callback Recycling

For callbacks, we implement a single-block thread-local cache:

```cpp
struct op_cache
{
    static void* allocate(std::size_t n)
    {
        auto& c = get();
        if(c.ptr_ && c.size_ >= n)
        {
            void* p = c.ptr_;
            c.ptr_ = nullptr;
            return p;
        }
        return ::operator new(n);
    }

    static void deallocate(void* p, std::size_t n)
    {
        auto& c = get();
        if(!c.ptr_ || n >= c.size_)
        {
            ::operator delete(c.ptr_);
            c.ptr_ = p;
            c.size_ = n;
        }
        else
            ::operator delete(p);
    }
};
```

The critical pattern is: **delete before dispatch**. When an I/O operation completes, it deallocates its state *before* invoking the completion handler. If that handler immediately starts another operation, the allocation finds the just-freed memory in the cache.

### 10.3 Coroutine Frame Pooling

For coroutines, we use a global frame pool that all coroutines share, regardless of whether they have explicit frame allocator parameters:

```cpp
// Default operator new uses global pool
static void* operator new(std::size_t size)
{
    static frame_pool alloc(frame_pool::make_global());
    // ... allocate from pool
}
```

This ensures that *all* coroutines—including lambdas, wrappers, and tasks without I/O object parameters—benefit from frame recycling. The pool uses thread-local caching with a global overflow pool for cross-thread scenarios.

### 10.4 Amortized Cost

Both models achieve **zero steady-state allocations** after warmup. The first iteration populates the caches; all subsequent operations recycle memory without syscalls.

---

## 11. Performance Comparison

### 11.1 Clang with Frame Elision

Benchmarks compiled with Clang 20.1, `-O3`, Windows x64, with `[[clang::coro_await_elidable]]`:

| Operation | Callback | Coroutine | Ratio |
|-----------|----------|-----------|-------|
| async_io | 3 ns | 21 ns | 7.0× |
| async_read_some | 4 ns | 25 ns | 6.3× |
| async_read (10×) | 44 ns | 99 ns | 2.3× |
| async_request (100×) | 498 ns | 750 ns | **1.5×** |

### 11.2 MSVC Comparison

The same benchmarks compiled with MSVC 19.x, RelWithDebInfo, Windows x64:

| Operation | Callback | Coroutine | Ratio |
|-----------|----------|-----------|-------|
| async_io | 5 ns | 58 ns | 11.6× |
| async_read_some | 5 ns | 69 ns | 13.8× |
| async_read (10×) | 60 ns | 226 ns | 3.8× |
| async_request (100×) | 673 ns | 1749 ns | 2.6× |

MSVC's coroutine implementation is approximately 2× slower than Clang's for this workload. The difference stems from:
- Less aggressive inlining of coroutine machinery
- No support for `[[clang::coro_await_elidable]]`
- Different code generation for symmetric transfer

### 11.3 Analysis

**Overhead Ratio Improves with Depth**: The key observation is that the callback/coroutine ratio *improves* as operation complexity increases:

| Depth | Clang Ratio | MSVC Ratio |
|-------|-------------|------------|
| 1 operation | 7.0× | 11.6× |
| 10 operations | 2.3× | 3.8× |
| 100 operations | **1.5×** | 2.6× |

This is because coroutine overhead is *fixed per suspension*, while the useful work (queue operations) scales with depth. For `async_request`:
- Clang: 750 ns / 100 ops = 7.5 ns per I/O
- MSVC: 1749 ns / 100 ops = 17.5 ns per I/O
- Callback: ~5 ns per I/O

### 11.4 Real-World Context

For I/O-bound workloads:
- Network RTT: 100,000+ ns
- Disk access: 10,000+ ns  
- Coroutine overhead: 7-18 ns per suspension (compiler-dependent)

Even with MSVC, the coroutine overhead is **0.02%** of a typical network operation. The 1.5-2.6× overhead for `async_request` is the cost of compositional async/await syntax versus hand-optimized state machines—a reasonable trade-off for most applications.

---

## 12. The Unavoidable Cost: `resume()` Opacity

Coroutine performance is fundamentally limited by the opacity of `std::coroutine_handle<>::resume()`. The compiler cannot inline across resume boundaries because:

1. The coroutine may be suspended at any of multiple `co_await` points
2. The frame address is only known at runtime
3. Resume effectively performs an indirect jump through the frame's resumption pointer

Note: This overhead is unrelated to handle typing. Whether you hold `coroutine_handle<void>` or `coroutine_handle<promise_type>`, the resume operation is identical—an indirect jump through the frame's resumption pointer. The opacity is intrinsic to the coroutine model, not an artifact of type erasure.

This prevents optimizations that callbacks enable: register allocation across async boundaries, constant propagation through handlers, and dead code elimination of unused paths.

### 12.1 HALO and Coroutine Elision

HALO (Heap Allocation eLision Optimization) can inline coroutine frames when the compiler can prove:
1. The coroutine is immediately awaited
2. The frame doesn't escape the caller's lifetime
3. The coroutine's lifetime is bounded by the caller

Standard HALO is limited because our design—where tasks store handles and pass through executors—causes the frame to "escape" into the task object.

However, **Clang provides `[[clang::coro_await_elidable]]`**, an attribute that enables more aggressive frame elision:

```cpp
#ifdef __clang__
#define CORO_AWAIT_ELIDABLE [[clang::coro_await_elidable]]
#else
#define CORO_AWAIT_ELIDABLE
#endif

struct CORO_AWAIT_ELIDABLE task { /* ... */ };
```

With this attribute, Clang can elide nested coroutine frames into the parent's frame when directly awaited. Our benchmarks show a **26% performance improvement** with this attribute enabled:

| Metric | Without Attribute | With Attribute |
|--------|-------------------|----------------|
| async_request | 1001 ns | 750 ns |
| Overhead ratio | 2.0× | 1.5× |

This optimization is Clang-specific. MSVC does not currently support coroutine await elision, contributing to its 2× slower coroutine performance.

### 12.2 Compiler Differences

| Feature | Clang 20.x | MSVC 19.x |
|---------|-----------|-----------|
| `[[coro_await_elidable]]` | ✓ | ✗ |
| Frame elision (HALO) | Aggressive | Conservative |
| Symmetric transfer | Optimized | Less optimized |
| Overall coroutine speed | Faster | ~2× slower |

For performance-critical coroutine code, Clang currently provides superior optimization. MSVC's coroutine implementation continues to improve, but production code should account for this difference.

### 12.3 Implemented Mitigations

1. **Frame pooling** (Section 9): Custom `operator new/delete` with thread-local caching eliminates allocation overhead after warmup
2. **`[[clang::coro_await_elidable]]`**: Enables frame elision for nested coroutines on Clang
3. **Symmetric transfer** (Section 6.1): Returning handles from `await_suspend` prevents stack growth
4. **Preallocated I/O state** (Section 5.1): Socket operation state is allocated once, not per-operation
5. **Global frame pool fallback**: Coroutines without explicit frame allocator parameters still benefit from pooling

---

## 13. Design Trade-offs

| Aspect | Callback Model | Coroutine Model |
|--------|---------------|-----------------|
| API Complexity | High (templates everywhere) | Low (uniform `task` type) |
| Compile Time | Poor (deep template instantiation) | Good (type erasure at boundaries) |
| Runtime (shallow, Clang) | Excellent (~3-4 ns) | Moderate (~21-25 ns) |
| Runtime (deep, Clang) | ~500 ns for 100 ops | ~750 ns for 100 ops (1.5×) |
| Runtime (deep, MSVC) | ~670 ns for 100 ops | ~1750 ns for 100 ops (2.6×) |
| Allocations (optimized) | 0 (recycling allocator) | 0 (frame pooling) |
| Handle overhead | N/A | Zero (`handle<void>` = `handle<T>`) |
| Sender compatibility | N/A | Native (`dispatch().resume()` pattern) |
| Code Readability | Callback chains / state machines | Linear `co_await` sequences |
| Debugging | Stack traces fragmented | Stack traces fragmented |
| Encapsulation | Poor (leaky templates) | Excellent (hidden state) |
| Customization | Explicit allocator parameters | Trait-based detection |
| Compiler optimization | Uniform | Clang >> MSVC |

---

## 14. Conclusion

We have demonstrated a coroutine-first asynchronous I/O framework that achieves:

1. **Flexible executors**: Any type satisfying `is_executor` works without modification
2. **Clean public interfaces**: No templates, no allocators, just `task`
3. **Hidden platform types**: I/O state lives in translation units
4. **Efficient composition**: Preallocated operation state, intrusive queuing
5. **Seamless executor switching**: The `run_on` primitive enables cross-context operations
6. **Safe executor lifetime**: Root tasks own executors by value
7. **Zero steady-state allocations**: Global frame pooling benefits all coroutines
8. **Compiler-aware optimization**: `[[clang::coro_await_elidable]]` for frame elision

The affine awaitable protocol—injecting execution context through `await_transform`—provides the mechanism. The frame allocator protocol—with a global pool fallback for coroutines without explicit allocator parameters—eliminates allocation overhead for *all* coroutines, not just those with I/O object parameters.

A critical lesson: **recycling matters equally for callbacks and coroutines**. Without recycling, both models suffer from allocation overhead. The delete-before-dispatch pattern for callbacks and thread-local frame pooling for coroutines both achieve zero steady-state allocations. Neither model is inherently allocation-free; both require deliberate optimization.

Coroutines are not free, but they are cheaper than expected. With Clang and `[[coro_await_elidable]]`, the overhead for 100 I/O operations is just **1.5×** compared to hand-optimized callbacks. MSVC lags at 2.6×, but compiler optimizations continue to improve. For I/O-bound workloads where operations take microseconds or milliseconds, even the worst-case overhead vanishes into the noise.

What remains is code that reads like synchronous logic, composes like functions, and hides complexity behind stable interfaces. The future of asynchronous C++ is not callbacks with ever-more-elaborate template machinery. It is coroutines with ever-more-refined execution models and ever-smarter compilers. This framework demonstrates what is achievable today.

---

## References

1. N4680 - C++ Extensions for Coroutines
2. P0443R14 - A Unified Executors Proposal for C++
3. P2300R7 - std::execution
4. P3352R3 - std::execution integration with coroutines
5. Boost.Asio documentation on composed operations
6. Lewis Baker, "Asymmetric Transfer" blog series
