**Document number:** PXXXXR0  
**Date:** 2025-12-30  
**Reply-to:** Vinnie Falco \<vinnie.falco@gmail.com\>  
**Audience:** SG1, LEWG  

---

# Affine Awaitables : Zero-Overhead Scheduler Affinity for the Rest of Us

## Abstract

This document describes a library-level extension to C++ coroutines that enables zero-overhead scheduler affinity for awaitables without requiring the full sender/receiver protocol. By introducing an `affine_awaitable` concept and a unified `resume_context` type, we achieve:

1. Zero-allocation affinity for opt-in awaitables
2. Transparent integration with P2300 senders
3. Graceful fallback for legacy awaitables
4. No language changes required

---

## 1. The Lost Context Problem

Consider a common scenario: a coroutine running on the UI thread needs to fetch data from the network.

```cpp
task ui_handler() {               // Runs on UI thread
    auto data = co_await fetch(); // fetch() completes on network thread
    update_ui(data);              // BUG: Where are we now?
}
```

When `fetch()` completes, the network subsystem resumes our coroutine—but on the *network* thread, not the UI thread. The call to `update_ui()` races, crashes, or corrupts state.

**This is the scheduler affinity problem:** after any `co_await`, how does a coroutine resume on its *home* scheduler?

The challenge deepens when coroutines call other coroutines:

```cpp
task<Data> fetch_and_process() {  // Started on UI thread
    auto raw = co_await network_read();   // Completes on network thread
    auto parsed = co_await parse(raw);    // Where does parse() run?
    co_return transform(parsed);          // Where does this run?
}
```

Every suspension point is an opportunity to get lost.

---

## 2. Today's Solutions (and Their Costs)

P3552 proposes coroutine tasks with scheduler affinity—ensuring a coroutine resumes on its designated scheduler after any `co_await`. Several approaches exist:

### 2.1 Manual Discipline

```cpp
task ui_handler() {
    auto data = co_await fetch();
    co_await resume_on(ui_scheduler);  // Programmer must remember
    update_ui(data);
}
```

**Problem:** Error-prone. Every `co_await` is a potential bug.

### 2.2 Sender Composition

```cpp
task ui_handler() {
    auto data = co_await continues_on(fetch(), ui_scheduler);
    update_ui(data);  // Guaranteed: UI thread
}
```

**Problem:** Only works with P2300 senders. The vast ecosystem of awaitables (Asio, cppcoro, custom libraries) is excluded.

### 2.3 Universal Trampoline

```cpp
// Works with ANY awaitable
auto data = co_await make_affine(fetch(), dispatcher);
```

**Problem:** Allocates on every `co_await`. The trampoline coroutine handle escapes to the dispatcher, defeating HALO optimization.

> **Note on HALO reliability:** Testing shows HALO is far more limited than often assumed. MSVC (19.50) does not implement HALO at all. Clang elides only the *outermost* coroutine frame; nested coroutines still allocate. The affine protocol provides the only *reliable* zero-allocation path. See the reference implementation's [HALO notes](https://github.com/vinniefalco/make_affine/blob/main/research/halo-notes.md) for detailed findings.

### 2.4 The Gap

| Approach | Works With | Allocation | HALO Reliable? |
|----------|------------|------------|----------------|
| `continues_on(sender, scheduler)` | Senders only | 0 | N/A |
| `make_affine(awaitable, dispatcher)` | Any awaitable | 1 per `co_await` | No |
| Nested coroutines (baseline) | Tasks | 1 per inner task | Clang only, outer frame only |

You either exclude most of the async ecosystem, or pay an allocation cost on every suspension point. And even without `make_affine`, nested coroutines allocate on every mainstream compiler.

**What if we could have universal compatibility AND zero overhead?**

### 2.5 Why This Matters Now

Twenty years of Boost.Asio. A decade of cppcoro. Countless custom awaitables in production codebases worldwide. This infrastructure *works*.

P2300's sender/receiver framework represents a significant investment in async standardization. Like any new framework, it will prove itself through production use over time. Affine awaitables provide a hedge that costs nothing if senders succeed and provides value if adoption is gradual:

**Ecosystem compatibility.** Boost.Asio has over 20 years of production deployment. Libraries like cppcoro, libcoro, folly::coro, and Bloomberg's Quantum power real systems today. Countless custom awaitables exist in proprietary codebases. These libraries represent proven, stable infrastructure that developers rely on. Affine awaitables let this ecosystem benefit from scheduler affinity without requiring conversion to senders—bridging the gap while the sender ecosystem matures.

**Incremental adoption.** Not every codebase needs the full compositional power of senders. Many applications simply need coroutines that resume on the correct thread. The affine protocol (~10 lines) provides a lower barrier to entry than the full sender/receiver protocol (~100+ lines), allowing teams to adopt scheduler affinity immediately and evolve toward senders as their needs grow.

**No-regret design.** Affine awaitables integrate seamlessly with P2300—senders flow through the same `await_transform` and receive optimal handling. If senders become ubiquitous, affine awaitables remain useful for custom awaitables and legacy integration. If sender adoption is slower than expected, affine awaitables ensure scheduler affinity is available today. Either way, the ecosystem benefits.

**Layered abstraction.** The dispatcher concept is more general than the scheduler concept—every scheduler can produce a dispatcher, but not every dispatcher requires the full sender protocol. This positions affine awaitables as a foundation that sender-based designs can build upon (see §11).

---

## 3. The Fix: One Parameter

The allocation in `make_affine` happens because the awaitable doesn't know where to resume. It hands back control blindly, and a trampoline must intercept and redirect.

The fix is simple: tell the awaitable where to resume.

```cpp
// Standard: awaitable is blind
void await_suspend(std::coroutine_handle<> h);

// Extended: awaitable knows the dispatcher
void await_suspend(std::coroutine_handle<> h, Dispatcher& d);
```

One additional parameter eliminates the allocation.

The awaitable receives the dispatcher and uses it directly:

```cpp
template<typename Dispatcher>
void await_suspend(std::coroutine_handle<> h, Dispatcher& d) {
    start_async([h, &d] {
        d(h);  // Resume through dispatcher
    });
}
```

No trampoline. No allocation. The awaitable handles affinity internally.

---

## 4. The Affine Protocol

The protocol outlined in this paper gives authors tools to solve two aspects of the lost context problem:

- **As an Awaitable**: You implement the protocol to respect the Caller's affinity (resume them where they want).

- **As a Task Type**: You implement the promise logic to enforce Your affinity (resume yourself where you want).

> The formal specification of the Affine Awaitable Protocol is here:  
> https://github.com/vinniefalco/make_affine/blob/master/affine-protocol.md

This protocol is fully implementable as a library today; standardization would bless the concepts and reduce boilerplate, without requiring `std::execution::task`. Dispatchers can also carry extra policy (e.g., priority save/restore) without affecting the core protocol.

### 4.1 Concepts

A **dispatcher** accepts a coroutine handle for resumption:

```cpp
template<typename D, typename P = void>
concept dispatcher = requires(D d, std::coroutine_handle<P> h) { d(h); };
```

An awaitable is *affine* if it accepts a dispatcher in `await_suspend`:

```cpp
template<typename A, typename D, typename P = void>
concept affine_awaitable =
    dispatcher<D, P> &&
    requires(A a, std::coroutine_handle<P> h, D& d) {
        a.await_suspend(h, d);
    };
```

### 4.2 Awaiter Adapter

This adapter is applied by the caller’s `await_transform` to affine awaitables (those with `await_suspend(h, d)`), injecting the caller’s dispatcher while keeping the standard awaiter shape.
To bridge the standard coroutine machinery to the extended protocol, we wrap affine awaitables:

```cpp
template<typename Awaitable, typename Dispatcher>
struct affine_awaiter {
    Awaitable awaitable_;
    Dispatcher* dispatcher_;

    bool await_ready() { 
        return awaitable_.await_ready(); 
    }

    auto await_suspend(std::coroutine_handle<> h) {
        return awaitable_.await_suspend(h, *dispatcher_);
    }

    decltype(auto) await_resume() { 
        return awaitable_.await_resume(); 
    }
};

template<typename A, typename D>
affine_awaiter(A&&, D*) -> affine_awaiter<A, D>;
```

### 4.3 Opting In

Library authors add a single overload—roughly 10 lines:

```cpp
struct my_async_op {
    bool await_ready() { return false; }

    // Standard overload (for non-affine contexts)
    void await_suspend(std::coroutine_handle<> h) {
        start_async([h] { h.resume(); });
    }

    // Extended overload (for affine contexts)
    template<typename Dispatcher>
    void await_suspend(std::coroutine_handle<> h, Dispatcher& d) {
        start_async([h, &d] {
            d(h);
        });
    }

    int await_resume() { return result_; }
};
```

---

## 5. Bridging Two Worlds

P2300 senders need *schedulers*. Awaitables need *callables*. How do we serve both?

### 5.1 The Unified Resume Context

A single type that is both callable (for awaitables) and provides scheduler access (for senders):

```cpp
template<typename Scheduler>
class resume_context {
    Scheduler* sched_;

public:
    explicit resume_context(Scheduler& s) noexcept : sched_(&s) {}

    // Dispatcher interface: callable with continuation
    template<typename F>
    void operator()(F&& f) const {
        sched_->dispatch(std::forward<F>(f));
    }

    // Scheduler interface: access underlying scheduler
    Scheduler& scheduler() const noexcept {
        return *sched_;
    }
};
```

### 5.2 Usage Patterns

This enables uniform handling:

- `continues_on(sender, ctx.scheduler())` — uses scheduler interface
- `affine_awaiter{awaitable, &ctx}` — uses callable interface
- `make_affine(awaitable, ctx)` — uses callable interface

One context type. Three dispatch paths. Zero friction.

---

## 6. Three Tiers, One `await_transform`

### 6.1 Architecture

```
                    ┌─────────────────────────┐
                    │     resume_context      │
                    │ (Scheduler + Callable)  │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
   ┌─────────┐          ┌──────────────┐         ┌───────────┐
   │ Sender  │          │   Affine     │         │  Legacy   │
   │         │          │  Awaitable   │         │ Awaitable │
   └────┬────┘          └──────┬───────┘         └─────┬─────┘
        │                      │                       │
        ▼                      ▼                       ▼
  continues_on            affine_awaiter          make_affine
                                                  (trampoline)
        │                      │                       │
        └──────────┬───────────┘                       │
                   ▼                                   ▼
            Zero Allocation                      One Allocation
```

### 6.2 Path Selection

The promise's `await_transform` selects the optimal path based on awaitable type:

```cpp
template<typename Awaitable>
auto await_transform(Awaitable&& a) {
    using A = std::remove_cvref_t<Awaitable>;

    if constexpr (std::execution::sender<A>) {
        // Tier 1: Sender — use continues_on with scheduler
        return std::execution::as_awaitable(
            std::execution::continues_on(
                std::forward<Awaitable>(a),
                dispatcher_->scheduler()),
            *this);
    }
    else if constexpr (affine_awaitable<A, context_type>) {
        // Tier 2: Affine awaitable — zero overhead
        return affine_awaiter{
            std::forward<Awaitable>(a), dispatcher_};
    }
    else {
        // Tier 3: Legacy awaitable — trampoline fallback
        return make_affine(
            std::forward<Awaitable>(a), *dispatcher_);
    }
}
```

This design follows the C++ tradition of making the widest range of programs work correctly, including existing code. Senders get optimal handling, modern awaitables opt into zero overhead, and legacy awaitables continue to function without modification.

---

## 7. Migration Strategy and Strict Mode

The tiered approach in §6 prioritizes maximum compatibility. However, some use cases demand compile-time guarantees. This section shows how the same affine primitives support both strategies—and how to migrate between them.

### 7.1 Non-Breaking Overload Addition

*(Tiered = accepts legacy via trampoline; Strict = rejects non-affine, zero-alloc guarantee.)*

**Key insight:** Adding `await_suspend(h, d)` alongside an existing `await_suspend(h)` is completely non-breaking.

```cpp
struct network_read {
    // Existing overload — unchanged, continues to work everywhere
    void await_suspend(std::coroutine_handle<> h) {
        start_async([h] { h.resume(); });
    }

    // New overload — enables zero-alloc affinity in affine contexts
    template<typename Dispatcher>
    void await_suspend(std::coroutine_handle<> h, Dispatcher& d) {
        start_async([h, &d] {
            d(h);
        });
    }
    
    bool await_ready() { return false; }
    int await_resume() { return result_; }
};
```

**What this means in practice:**

| Context | Overload Selected | Behavior |
|---------|------------------|----------|
| Non-affine coroutine | `await_suspend(h)` | Works as before |
| Tiered affine task | `await_suspend(h, d)` | Zero allocation |
| Strict affine task | `await_suspend(h, d)` | Zero allocation |

Existing code calling `co_await network_read{}` in a plain coroutine continues to compile and run identically. The new overload only activates when an affine-aware task invokes it through `affine_awaiter`.

### 7.2 Strict Mode: Compile-Time Enforcement

For use cases requiring guaranteed zero allocation, constrain `await_transform` to reject non-affine awaitables:

```cpp
template<typename Awaitable>
auto await_transform(Awaitable&& a) {
    using A = std::remove_cvref_t<Awaitable>;

    if constexpr (std::execution::sender<A>) {
        // Senders: optimal path via continues_on
        return std::execution::as_awaitable(
            std::execution::continues_on(
                std::forward<Awaitable>(a),
                dispatcher_->scheduler()),
            *this);
    }
    else {
        // Strict: ONLY affine awaitables accepted
        static_assert(affine_awaitable<A, context_type>,
            "Strict mode: awaitable must satisfy affine_awaitable<A, Dispatcher>. "
            "Add await_suspend(handle, dispatcher) overload or use a sender.");
        
        return affine_awaiter{
            std::forward<Awaitable>(a), dispatcher_};
    }
}
```

**Compile-time guarantee:** If it compiles, every `co_await` is zero-allocation.

### 7.3 Tiered vs. Strict: Same Primitives, Different Policies

| Policy | `await_transform` Behavior | Use Case |
|--------|---------------------------|----------|
| **Tiered** (§6) | Accept all; optimize what we can | Library adoption, gradual migration |
| **Strict** (§7.2) | Reject non-affine at compile time | Performance-critical systems, embedded |

Both modes use identical primitives:
- Same `affine_awaitable` concept
- Same `affine_awaiter` adapter
- Same `await_suspend(h, d)` protocol

The only difference is the `await_transform` constraint. This means:

1. **Libraries target one protocol.** Implementing `await_suspend(h, d)` works for both modes.
2. **Applications choose their policy.** Tiered for flexibility, strict for guarantees.
3. **Migration is mechanical.** Remove the `make_affine` fallback tier → strict mode.

### 7.4 Gradual Library Evolution

**Coroutine task maintainers:** add dispatcher storage + affine `await_transform` (tiered or strict); expose both await paths.

**Awaitable library maintainers:** add `await_suspend(h, d)`; legacy callers keep working; affine callers get zero-alloc.

The affine protocol enables a clear migration path:

```
Phase 1: Library works everywhere (status quo)
         └─ Only await_suspend(h) exists
         └─ Affine tasks use make_affine fallback (1 alloc)

Phase 2: Library adds affine overload (non-breaking)
         └─ Both await_suspend(h) and await_suspend(h, d) exist
         └─ Non-affine callers: unchanged behavior
         └─ Affine callers: zero allocation

Phase 3: Library deprecates legacy overload (optional)
         └─ Only await_suspend(h, d) remains
         └─ Strict-mode tasks: compile-time guarantee
         └─ Legacy callers: compile error with clear message
```

**Phase 2 is the key transition.** It's additive, non-breaking, and immediately provides zero-allocation benefits to affine callers while maintaining backward compatibility.

### 7.5 Migration Tool, Not Just Detection

The `affine_awaitable` concept serves dual purposes:

**Detection (Tiered Mode):**
```cpp
if constexpr (affine_awaitable<A, D>) {
    // Optimize: zero allocation
} else {
    // Fallback: make_affine trampoline
}
```

**Enforcement (Strict Mode):**
```cpp
static_assert(affine_awaitable<A, D>,
    "Zero-allocation guarantee requires affine awaitable");
```

This duality makes the concept a **migration tool**:

1. Start with tiered mode to identify which awaitables need upgrading
2. Upgrade awaitables incrementally (each upgrade is non-breaking)
3. When all awaitables are affine, switch to strict mode
4. Enjoy compile-time zero-allocation guarantees

The concept doesn't change—only the policy around it.

---

## 8. Building Affine Tasks

To simplify task implementation, we provide CRTP mixins that handle the dispatcher plumbing.

### 8.1 Promise Mixin

The `affine_promise` CRTP base provides:
- `set_continuation(h)` — stores the caller's handle
- `set_dispatcher(d)` — stores the dispatcher for affinity
- `final_suspend()` — resumes continuation through dispatcher if set

> `await_transform` policy (tiered vs. strict) is intentionally left to the task author; you can implement it inline or with a small helper/mixin to select between tiered (fallback trampoline) and strict (compile-time rejection).

```cpp
template<typename Derived, typename Dispatcher>
class affine_promise {
protected:
    std::coroutine_handle<> continuation_;
    Dispatcher* dispatcher_ = nullptr;
    
public:
    void set_continuation(std::coroutine_handle<> h) noexcept;
    void set_dispatcher(Dispatcher& d) noexcept;
    auto final_suspend() noexcept;  // Dispatches continuation if dispatcher set
};
```

### 8.2 Task Mixin

The `affine_task` CRTP base provides both `await_suspend` overloads:

```cpp
template<typename T, typename Derived, typename Dispatcher>
class affine_task {
public:
    bool await_ready() const noexcept;
    
    // Legacy: non-affine callers
    std::coroutine_handle<> await_suspend(std::coroutine_handle<> caller) noexcept;
    
    // Affine: receives dispatcher from caller
    template<typename D>
    std::coroutine_handle<> await_suspend(std::coroutine_handle<> caller, D& d) noexcept;
    
    decltype(auto) await_resume();
};
```

See the [reference implementation](https://github.com/vinniefalco/make_affine) for complete code.

### 8.3 Example: Complete Task Type

```cpp
using pool_context = resume_context<pool_scheduler>;

template<typename T = void>
class task : public affine_task<T, task<T>, pool_context>
{
public:
    struct promise_type : affine_promise<promise_type, pool_context>
    {
        // User provides: initial_suspend, return_value, result, get_return_object
        // Mixin provides: final_suspend, set_dispatcher, set_continuation
        
        template<typename Awaitable>
        auto await_transform(Awaitable&& a) {
            // Three-tier dispatch as shown above (tiered policy)
            // A strict policy would replace the fallback with static_assert
        }
    };
    
    using handle_type = std::coroutine_handle<promise_type>;
    
    handle_type handle() const { return handle_; }
    
    void set_scheduler(pool_scheduler& sched) {
        handle_.promise().set_dispatcher(pool_context{sched});
    }

private:
    handle_type handle_;
};
```

---

## 9. The Full Picture

### 9.1 Allocation Overhead

| Awaitable Type | Mechanism | Allocations per `co_await` |
|----------------|-----------|---------------------------|
| P2300 Sender | `continues_on` | 0 |
| Affine awaitable | `affine_awaiter` | 0 |
| Legacy | `make_affine` | 1 |

**Crucially, the zero-allocation paths do not depend on HALO.**

### 9.2 Implementation Complexity

| Approach | Lines to Implement | Expertise Required |
|----------|-------------------|-------------------|
| Full Sender | ~100+* | High (S/R protocol) |
| Affine awaitable | ~10 | Low (one overload) |
| Legacy (no change) | 0 | None |

*Based on P3552R3 §9.4.5 `promise_type` specification.

### 9.3 Feature Matrix

| Feature | Sender | Affine Awaitable | Legacy |
|---------|--------|------------------|--------|
| Zero allocation | Yes | Yes | No |
| Composable (pipe) | Yes | No | No |
| Works with any task | Yes | Yes | Yes |
| Opt-in required | Yes | Yes | No |
| Standard today | P2300 | This proposal | Library |

---

## 10. Adoption Path

### 10.1 Migration Story

```
Legacy Awaitable ───────▶ Affine Awaitable ───────▶ Full Sender
   (works today)            (add 1 overload)         (full protocol)
   (1 alloc/await)          (zero overhead)          (composable)
```

### 10.2 Incremental Adoption

1. **Immediate compatibility:** Legacy awaitables work via `make_affine` with no code changes.
2. **Optimization:** Add `await_suspend(h, dispatcher)` overload for zero allocation overhead.
3. **Full composition:** Evolve to senders when pipe-style composition is needed.

Libraries can adopt at their own pace. Users benefit from scheduler affinity immediately.

---

## 11. Foundational Analysis

This section demonstrates that affine awaitables represent a more fundamental abstraction than P3552's sender-only approach, and that P3552's `task` can be built upon this foundation.

### 11.1 The Abstraction Hierarchy

A **dispatcher** is simply a callable that accepts a coroutine handle:

```cpp
template<typename D, typename P = void>
concept dispatcher = requires(D d, std::coroutine_handle<P> h) {
    d(h);  // Schedule coroutine for resumption
};
```

Since `std::coroutine_handle<>` has `operator()` which calls `resume()`, the handle itself is callable and can be dispatched directly.

A **scheduler** (P2300) requires the full sender protocol:

```cpp
concept scheduler = requires(Sch sch) {
    { schedule(sch) } -> sender;  // Returns a sender with completion signatures
};
```

The relationship is asymmetric:

```
                    ┌─────────────────────┐
                    │     Dispatcher      │
                    │ (callable concept)  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌──────────┐     ┌──────────┐     ┌──────────┐
       │ Scheduler│     │ Executor │     │ Simple   │
       │ (P2300)  │     │ (legacy) │     │ Callable │
       └──────────┘     └──────────┘     └──────────┘
```

**Every scheduler can produce a dispatcher.** The `resume_context` type demonstrates this:

```cpp
template<typename Scheduler>
class resume_context {
    void operator()(F&& f) const { sched_->dispatch(f); }  // Dispatcher interface
    Scheduler& scheduler() const { return *sched_; }       // Scheduler access
};
```

**But not every dispatcher is a scheduler.** A simple thread pool with `post(f)` is a dispatcher but may not implement the full sender protocol.

### 11.2 Zero-Cost Subsumption

The affine approach handles every case P3552 handles, plus more, at equal or lower cost:

| Awaitable Type | P3552 Path | Affine Path | Cost Delta |
|----------------|------------|-------------|------------|
| P2300 Sender | `affine_on` + `as_awaitable` | `continues_on` + `as_awaitable` | **0** |
| Affine awaitable | ✗ Not supported | `affine_awaiter` | **N/A → 0** |
| Legacy awaitable | ✗ Not supported | `make_affine` | **N/A → 1 alloc** |
| Task awaiting Task | Full sender machinery | `affine_awaiter` | **Overhead → 0** |

The sender path is *identical*—both use `continues_on`/`affine_on` to maintain affinity. The affine approach simply adds two additional paths that P3552 cannot support.

### 11.3 Integration with P3552

P3552's `promise_type` specifies ~100 lines of scheduler-affinity machinery inline. With affine awaitables as a foundation:

```cpp
class promise_type 
    : public affine_promise<promise_type, task_context>  // Provides final_suspend
    , public with_awaitable_senders<promise_type>        // Existing CRTP
{
    // Task-specific: error/result storage, allocator, environment queries
};
```

Building P3552's `task` on affine awaitables would provide:

1. **Ecosystem support.** Non-sender awaitables (Asio, cppcoro, custom) gain scheduler affinity.
2. **Task-to-task optimization.** When one `task` awaits another, the `affine_awaiter` path avoids the full sender machinery.
3. **Cleaner factoring.** The mixins become building blocks for any scheduler-affine coroutine.
4. **Incremental adoption.** Libraries can start with ~10 lines and evolve to full senders later.

### 11.4 Relationship to P3552

The affine awaitable abstraction complements and extends P3552:

1. Senders are handled via the same `continues_on` path P3552 uses
2. Affine awaitables add a zero-overhead path for non-sender awaitables
3. Legacy awaitables gain affinity through the `make_affine` fallback
4. The dispatcher concept generalizes the scheduler concept

This positions affine awaitables as a foundation that P3552's `task` could build upon, rather than a competing approach.

---

## 12. Proposed Wording

*Relative to N4981.*

### 12.1 Header `<coroutine>` synopsis

Add to the `<coroutine>` header synopsis:

```cpp
namespace std {
  // [coroutine.affine.dispatcher], dispatcher concept
  template<class D, class P = void>
    concept dispatcher = see below;

  // [coroutine.affine.concept], affine awaitable concept
  template<class A, class D, class P = void>
    concept affine_awaitable = see below;

  // [coroutine.affine.awaiter], affine awaiter
  template<class Awaitable, class Dispatcher>
    struct affine_awaiter;

  // [coroutine.affine.context], resume context
  template<class Scheduler>
    class resume_context;

  // [coroutine.affine.promise], affine promise mixin
  template<class Derived, class Dispatcher>
    class affine_promise;

  // [coroutine.affine.task], affine task mixin
  template<class T, class Derived, class Dispatcher>
    class affine_task;

  // [coroutine.affine.trampoline], affine trampoline fallback
  template<class Awaitable, class Dispatcher>
    auto make_affine(Awaitable&& awaitable, Dispatcher& dispatcher);
}
```

### 12.2 Dispatcher concept [coroutine.affine.dispatcher]

```cpp
template<class D, class P = void>
concept dispatcher = requires(D d, coroutine_handle<P> h) { d(h); };
```

*Remarks:* Since `coroutine_handle<P>` has `operator()` which invokes `resume()`, the handle itself is callable and can be dispatched directly.

### 12.3 Affine awaitable concept [coroutine.affine.concept]

```cpp
template<class A, class D, class P = void>
concept affine_awaitable =
  dispatcher<D, P> &&
  requires(A a, coroutine_handle<P> h, D& d) {
    a.await_suspend(h, d);
  };
```

### 12.4 Affine awaiter [coroutine.affine.awaiter]

```cpp
template<class Awaitable, class Dispatcher>
struct affine_awaiter {
  Awaitable awaitable_;
  Dispatcher* dispatcher_;

  constexpr bool await_ready()
    noexcept(noexcept(awaitable_.await_ready()))
    { return awaitable_.await_ready(); }

  constexpr auto await_suspend(coroutine_handle<> h)
    noexcept(noexcept(awaitable_.await_suspend(h, *dispatcher_)))
    { return awaitable_.await_suspend(h, *dispatcher_); }

  constexpr decltype(auto) await_resume()
    noexcept(noexcept(awaitable_.await_resume()))
    { return awaitable_.await_resume(); }
};

template<class A, class D>
affine_awaiter(A&&, D*) -> affine_awaiter<A, D>;
```

### 12.5 Resume context [coroutine.affine.context]

```cpp
template<class Scheduler>
class resume_context {
  Scheduler* sched_;  // exposition only

public:
  explicit resume_context(Scheduler& s) noexcept;

  template<class F>
    void operator()(F&& f) const;

  Scheduler& scheduler() const noexcept;
};
```

*Effects:* `operator()` invokes `sched_->dispatch(std::forward<F>(f))`.

*Returns:* `scheduler()` returns `*sched_`.

### 12.6 Affine promise mixin [coroutine.affine.promise]

```cpp
template<class Derived, class Dispatcher>
class affine_promise {
protected:
  coroutine_handle<> continuation_;        // exposition only
  Dispatcher* dispatcher_ = nullptr;       // exposition only
  bool* done_flag_ = nullptr;              // exposition only

public:
  void set_continuation(coroutine_handle<> h) noexcept;
  void set_dispatcher(Dispatcher& d) noexcept;
  void set_done_flag(bool& flag) noexcept;
  auto final_suspend() noexcept;
};
```

*Effects:* `final_suspend()` returns an awaiter that:
- Sets `*done_flag_` to `true` if `done_flag_` is not null.
- If `dispatcher_` is not null, invokes `(*dispatcher_)(f)` where `f` resumes `continuation_` if non-null, then returns `noop_coroutine()`.
- Otherwise returns `continuation_` if non-null, or `noop_coroutine()`.

*Remarks:* `done_flag_` is an optional pointer set via `set_done_flag` for sync-wait style patterns.

### 12.7 Affine task mixin [coroutine.affine.task]

```cpp
template<class T, class Derived, class Dispatcher>
class affine_task {
public:
  bool await_ready() const noexcept;

  coroutine_handle<>
  await_suspend(coroutine_handle<> caller) noexcept;

  template<class D>
    requires convertible_to<D, Dispatcher>
  coroutine_handle<>
  await_suspend(coroutine_handle<> caller, D& d) noexcept;

  decltype(auto) await_resume();
};
```

*Requires:* `Derived` shall provide a `handle()` member function returning a coroutine handle whose promise type provides `set_continuation`, `set_dispatcher`, and `result` member functions.

### 12.8 Affine trampoline [coroutine.affine.trampoline]

```cpp
template<class Awaitable, class Dispatcher>
auto make_affine(Awaitable&& awaitable, Dispatcher& dispatcher)
  -> /* affinity_trampoline<await-result-type<Awaitable>> */;
```

*Effects:* Returns an awaitable that wraps `awaitable` in a trampoline coroutine. When `awaitable` completes, the trampoline dispatches the continuation through `dispatcher` before resuming the caller.

*Returns:* An awaitable yielding the same result type as `awaitable`.

*Remarks:* This function is the fallback for legacy awaitables that do not implement the `affine_awaitable` protocol. The trampoline coroutine incurs one heap allocation per invocation. See the reference implementation at https://github.com/vinniefalco/make_affine/blob/master/affine.hpp for the complete trampoline design.

---

## 13. Summary

| Component | Purpose |
|-----------|---------|
| `dispatcher<D,P>` | Concept for types callable with `coroutine_handle<P>` |
| `affine_awaitable<A,D,P>` | Concept detecting extended `await_suspend` protocol |
| `affine_awaiter<A,D>` | Bridges standard coroutine machinery to extended protocol |
| `resume_context<Scheduler>` | Single type: callable for awaitables, scheduler access for senders |
| `affine_promise<Derived,D>` | CRTP mixin providing `final_suspend` with dispatcher support |
| `affine_task<T,Derived,D>` | CRTP mixin providing both `await_suspend` overloads |
| `make_affine(a, d)` | Trampoline fallback for legacy awaitables |

**The core insight:** Awaitables that accept a dispatcher can resume through it, achieving zero-overhead scheduler affinity without the full sender/receiver protocol. A unified `resume_context` type enables transparent integration with P2300 senders while serving the broader awaitable ecosystem.

**The vision:** Every coroutine resumes where it belongs. No exceptions, no overhead, no rewrites.

---

## Acknowledgements

Thanks to Matheus Izvekov for feedback on reusable components and third-party coroutine extensibility. Thanks to Klemens Morgenstern for insights on real-world `await_transform` patterns, the strict-mode migration strategy (§7), and refining the dispatcher concept to accept coroutine handles directly. Thanks to the authors of P3552 (Dietmar Kühl, Maikel Nadolski) for establishing the foundation this proposal builds upon.

---

## References

### WG21 Papers

- **[P2300R10]** Michał Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach. *`std::execution`*. [https://wg21.link/P2300R10](https://wg21.link/P2300R10)

- **[P3109R0]** Eric Niebler. *A plan for `std::execution` for C++26*. [https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3109r0.html](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3109r0.html)

- **[P3552R3]** Dietmar Kühl, Maikel Nadolski. *Add a Coroutine Task Type*. [https://wg21.link/P3552](https://wg21.link/P3552)

- **[P0981R0]** Gor Nishanov, Richard Smith. *Halo: Coroutine Heap Allocation eLision Optimization*. [https://wg21.link/P0981](https://wg21.link/P0981)

- **[P2855R1]** Ville Voutilainen. *Member customization points for Senders and Receivers*. [https://isocpp.org/files/papers/P2855R1.html](https://isocpp.org/files/papers/P2855R1.html)

- **[N4981]** Thomas Köppe. *Working Draft, Standard for Programming Language C++*. [https://wg21.link/N4981](https://wg21.link/N4981)

### Implementations

- **stdexec** — NVIDIA's reference implementation of P2300.  
  [https://github.com/NVIDIA/stdexec](https://github.com/NVIDIA/stdexec)

- **libunifex** — Meta's implementation of the Unified Executors proposal.  
  [https://github.com/facebookexperimental/libunifex](https://github.com/facebookexperimental/libunifex)

- **Intel Bare Metal Senders and Receivers** — Embedded adaptation demonstrating implementation challenges.  
  [https://github.com/intel/cpp-baremetal-senders-and-receivers](https://github.com/intel/cpp-baremetal-senders-and-receivers)

### Existing Awaitable Ecosystem

- **Boost.Asio** — Cross-platform C++ library for network and low-level I/O programming, with coroutine support since Boost 1.66 (2017).  
  [https://www.boost.org/doc/libs/release/doc/html/boost_asio.html](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)

- **cppcoro** — Lewis Baker's coroutine library providing task types, generators, and async primitives.  
  [https://github.com/lewissbaker/cppcoro](https://github.com/lewissbaker/cppcoro)

- **libcoro** — Modern C++20 coroutine library.  
  [https://github.com/jbaldwin/libcoro](https://github.com/jbaldwin/libcoro)

- **Bloomberg Quantum** — Production multi-threaded coroutine dispatcher.  
  [https://github.com/bloomberg/quantum](https://github.com/bloomberg/quantum)

- **folly::coro** — Meta's coroutine library used in production at scale.  
  [https://github.com/facebook/folly/tree/main/folly/coro](https://github.com/facebook/folly/tree/main/folly/coro)

### Background Reading

- Corentin Jabot. *A Universal Async Abstraction for C++*. Discussion of executor models and design trade-offs.  
  [https://cor3ntin.github.io/posts/executors/](https://cor3ntin.github.io/posts/executors/)

- Lewis Baker. *C++ Coroutines: Understanding operator co_await*.  
  [https://lewissbaker.github.io/2017/11/17/understanding-operator-co-await](https://lewissbaker.github.io/2017/11/17/understanding-operator-co-await)

- Lewis Baker. *C++ Coroutines: Understanding the promise type*.  
  [https://lewissbaker.github.io/2018/09/05/understanding-the-promise-type](https://lewissbaker.github.io/2018/09/05/understanding-the-promise-type)

---

## Revision History

### R0 (2025-12-30)

Initial revision. This paper supersedes the earlier "Simplifying P3552R3 with `make_affine`" draft, which focused narrowly on the trampoline fallback. This revision presents a complete framework:

- Introduces the `affine_awaitable` concept for zero-overhead scheduler affinity
- Provides `affine_awaiter` to bridge standard coroutine machinery
- Defines `resume_context` to unify scheduler and dispatcher interfaces  
- Specifies CRTP mixins (`affine_promise`, `affine_task`) as building blocks
- Retains `make_affine` as the fallback for legacy awaitables
- Positions affine awaitables as a foundation that P3552's `task` can build upon

The key insight: passing the dispatcher to the awaitable eliminates the trampoline allocation entirely for opt-in awaitables, while maintaining full compatibility with existing code.

### R1 (2025-12-31)

Incorporated feedback and clarifications contributed by Logan McDougall:
- Added formal protocol link and clarified adapter direction in §4.2
- Clarified tiered vs. strict policies and migration roles in §7
- Simplified allocation table and references; documented `done_flag_` and reference link
- Noted library implementability and dispatcher extensibility
