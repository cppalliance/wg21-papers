---
title: "Executor Utilities: Design Rationale"
document: D0006R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Shared mutable state is the oldest concurrency problem. Mutexes solve it by blocking. Strands solve it by ordering.

This paper documents the design rationale for `strand<Ex>` and `any_executor`, the two executor utilities proposed in the companion ask paper *Executor Utilities*<sup>[14]</sup>. `strand` serializes coroutine resumption over any executor without locks. `any_executor` type-erases any `Executor` behind an owning handle with small buffer optimization. Both are general-purpose utilities with no I/O dependency and no platform dependency. Both ship in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> today.

This paper is Paper 3 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>. It depends on Paper 1 ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup>), the IoAwaitable Protocol. Read the companion *Executor Utilities*<sup>[14]</sup> for the proposal; read this paper when you need the design audit trail.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper is part of the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) ([P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>), a project to bring coroutine-native I/O to C++.

The author develops and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[4]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper asks for nothing.

---

## 2. Why Strand

### 2.1 The Problem

Concurrent access to shared mutable state requires synchronization. The standard library provides `std::mutex`, `std::shared_mutex`, `std::atomic`, and related primitives. These are correct and sufficient. They are also hazardous.

A mutex composes badly with async I/O. A coroutine that holds a mutex across a suspension point prevents other coroutines from making progress. A coroutine that releases a mutex before suspending and re-acquires it after resuming has a window in which the invariant is visible to other threads - the mutex does not protect across the suspension. Both patterns are common sources of production bugs.

```cpp
task<> bad_pattern(std::mutex& mtx, state& st,
                   socket& sock)
{
    {
        std::lock_guard lk(mtx);
        st.counter++;
    }
    auto [ec, n] = co_await sock.read_some(buf);
    {
        std::lock_guard lk(mtx);
        st.counter--;                // another coroutine may
    }                                // have modified st between
}                                    // the two lock regions
```

The two lock regions protect individual accesses but not the logical transaction. The invariant the programmer intended - that `counter` reflects exactly the number of in-flight reads - is not enforced across the suspension.

### 2.2 Strands Solve This

A strand serializes coroutine execution. Coroutines dispatched through the same strand never execute concurrently. The serialization holds across suspension points because the strand controls resumption, not just access.

```cpp
strand<decltype(ex)> s(ex);

task<> correct_pattern(strand<decltype(ex)>& s,
                       state& st, socket& sock)
{
    co_await run(s)([&]() -> task<> {
        st.counter++;
        auto [ec, n] = co_await sock.read_some(buf);
        st.counter--;
        co_return;
    }());
}
```

No mutex. No lock guard. No window. The strand guarantees that while one coroutine runs within it, no other coroutine dispatched through the same strand executes. The serialization covers the entire coroutine body, including suspension points. When the coroutine suspends at `co_await`, the strand does not release - it holds the ordering. When the coroutine resumes, it resumes under the strand's guarantee.

### 2.3 Strands in a Coroutine-Native Model

In callback-based models like [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[5]</sup>, strands serialize completion handler dispatch. The completion handler is a function object that the reactor invokes when an I/O operation completes. The strand ensures that two handlers associated with the same strand are never invoked concurrently.

In a coroutine-native model, there are no completion handlers. Coroutines suspend and resume. The strand serializes resumption instead of handler dispatch. The semantic guarantee is the same: No two pieces of work associated with the same strand execute concurrently. The mechanism is different: The strand's `dispatch` and `post` control coroutine resumption via `continuation` and symmetric transfer.

The shift from handler dispatch to coroutine resumption is not a design choice - it is forced by the execution model. In the IoAwaitable protocol, I/O operations return awaitables, not completion tokens. The awaitable's `await_suspend` receives a `continuation` and dispatches through an executor. The strand wraps that executor and adds the serialization invariant. The mechanism maps directly to the protocol.

### 2.4 Why Not Just Mutexes

Mutexes block the calling thread. In a coroutine-native model with a limited thread pool, blocking one thread reduces the pool's capacity. A strand does not block any thread. It enqueues the continuation and returns. The thread that posted the continuation is free to run other work.

Mutexes are not composable with `co_await`. A lock held across a suspension point is held by a thread that may be running a different coroutine when the original coroutine resumes - a thread that did not acquire the lock. The C++ standard does not permit unlocking a mutex from a different thread than the one that locked it. A strand has no such constraint because it does not bind to a thread.

Mutexes cause deadlocks. A strand cannot deadlock because it never blocks. It can cause starvation (one strand monopolizes the underlying executor), but that is a scheduling concern, not a correctness concern.

**Strands serialize without blocking. Mutexes serialize by blocking. The coroutine model needs the former.**

---

## 3. Why Type-Erased Executor

### 3.1 The Problem

The `Executor` concept in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup> is satisfied by any type that provides `dispatch`, `post`, `context`, `on_work_started`, `on_work_finished`, and equality comparison. Different execution contexts produce different executor types: `io_context::executor_type`, `thread_pool::executor_type`, `strand<io_context::executor_type>`.

Code that stores an executor polymorphically - a connection object, a service registry, a work queue - needs a single type that holds any executor. Templates are not the answer: A `connection<Executor>` template leaks the executor type into every consumer.

### 3.2 `executor_ref` vs `any_executor`

[P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup> defines `executor_ref` as a non-owning, two-pointer type-erased view of an executor. It lives inside `io_env` and is used at suspension points. It is the right tool for borrowing: The launch function owns the executor, and every coroutine in the chain borrows it through `executor_ref`.

`executor_ref` is not the right tool for storage. It does not own the executor. If the executor goes out of scope, the `executor_ref` dangles. A connection object that outlives the scope that created its executor cannot use `executor_ref`.

`any_executor` fills this gap. It owns the erased executor, manages its lifetime, and provides value semantics. It is the owning counterpart to `executor_ref`.

```cpp
struct session
{
    any_executor ex;

    task<> run()
    {
        co_await run(ex)(process());
    }
};
```

The session stores its executor without knowing the concrete type. The executor outlives the scope that created it because `any_executor` owns it.

### 3.3 Why Not `std::any`

`std::any` type-erases any type but does not model `Executor`. Casting back to the concrete type defeats the purpose - the consumer would need to know the type to use it. `any_executor` provides the `Executor` interface directly: `dispatch`, `post`, `context`, work counting, and comparison. The type erasure is not about hiding the type from the implementation; it is about hiding the type from the consumer while preserving the interface.

### 3.4 Why Not `std::function`

`std::function` type-erases a callable. An executor is not a single callable - it is an object with multiple operations and associated state. Wrapping each operation in a separate `std::function` would fragment the executor's identity and break comparison semantics.

**`any_executor` is the owning, polymorphic executor handle. `executor_ref` is the borrowing, lightweight view. Both are necessary.**

---

## 4. Convergence

Five ecosystems provide serialization and executor type erasure. None designed them to interoperate. All arrived at the same shapes.

### 4.1 Serialization

| Ecosystem                | Serialization primitive          | Model                              |
|--------------------------|----------------------------------|------------------------------------|
| Boost.Asio<sup>[5]</sup> | `strand<Executor>`              | Handler dispatch ordering          |
| Go                       | Channels + goroutines            | CSP: communicate, do not share     |
| Rust (Tokio)             | `tokio::sync::Mutex`            | Async-aware mutex (yields, does not block) |
| .NET                     | `SynchronizationContext`        | Post callbacks to a single-threaded context |
| Capy<sup>[1]</sup>       | `strand<Ex>`                    | Coroutine resumption ordering      |

Go eliminates the problem by forbidding shared mutable state at the language level - goroutines communicate through channels. Rust's `tokio::sync::Mutex` is an async-aware mutex that yields the task instead of blocking the thread, achieving the same non-blocking property as a strand but through a different mechanism. .NET's `SynchronizationContext` posts continuations to a single-threaded context, providing serialization through thread affinity.

The Asio strand is the direct ancestor. The coroutine-native strand in Capy inherits the guarantee and adapts the mechanism: Where Asio strands serialize handler dispatch, Capy strands serialize coroutine resumption via `continuation` and symmetric transfer.

### 4.2 Type Erasure

| Ecosystem                | Type-erased executor              | Ownership    |
|--------------------------|-----------------------------------|--------------|
| Boost.Asio<sup>[5]</sup> | `any_io_executor`                | Owning, SBO  |
| Java                     | `ExecutorService` (interface)     | Reference    |
| .NET                     | `TaskScheduler` (abstract class)  | Reference    |
| Capy<sup>[1]</sup>       | `any_executor`                   | Owning, SBO  |

Asio's `any_io_executor` (formerly `any_executor` in Asio 1.x) is the direct precedent. It type-erases any I/O executor with small buffer optimization and provides the full executor interface. Java and .NET use interface-based polymorphism, which is the reference-semantics analogue.

**Five ecosystems. Same two abstractions. Serialization and type erasure over executors are universal needs.**

---

## 5. Design Decisions

### 5.1 `strand` Is a Class Template

The strand is parameterized on the executor type: `strand<Ex>`. The alternative - a type-erased strand that works with any executor through `any_executor` - was considered and rejected. The template parameter avoids the vtable overhead of type erasure on every `dispatch` and `post` call. A strand is typically constructed once per connection or per shared-state group and used on every I/O operation. The construction cost of a template instantiation is amortized over thousands of dispatch calls.

A type-erased strand can be obtained by wrapping a `strand<Ex>` in `any_executor`: `any_executor(strand<Ex>(ex))`. The reverse - extracting the concrete type from a type-erased strand - requires a `target<T>()` accessor or a type-unsafe cast. The template parameter preserves type information where it is useful and allows erasure where it is needed.

### 5.2 `strand` Is Move-Only

Copying a strand would create two handles to the same serialization state. Both handles would need to serialize against each other, but the user would have no way to know they share state. The result would be a "strand" that does not serialize - a defect by design.

Move-only semantics make ownership unambiguous. One strand, one owner. If shared ownership is needed, `std::shared_ptr<strand<Ex>>` provides it with explicit lifetime semantics.

### 5.3 `any_executor` Uses Small Buffer Optimization

The common executor types - `io_context::executor_type`, `strand<...>::executor_type`, `thread_pool::executor_type` - are small. An `io_context` executor is typically one or two pointers. A strand executor adds one more pointer for the strand state. SBO avoids a heap allocation for these common cases.

The SBO threshold is implementation-defined. Quality implementations should accommodate at least the executors shipped in the standard library. The observable behavior is identical regardless of whether the SBO applies - the optimization is invisible to the user.

### 5.4 `any_executor` Supports Comparison

Executor equality is load-bearing. Two executors compare equal if they dispatch to the same execution context with the same properties. This is the foundation for strand identity: A strand's executor compares equal to itself regardless of how many copies exist. Without comparison, `strand` cannot detect whether a dispatch call is already within the strand.

`any_executor` preserves comparison across the type erasure boundary. Two `any_executor` instances compare equal if they hold the same type and the underlying executors compare equal. This is the same contract as `std::any` would provide if `std::any` supported equality comparison - which it does not.

### 5.5 `any_executor` Is Nullable

A default-constructed `any_executor` holds no executor. This is useful for deferred initialization:

```cpp
struct server
{
    any_executor ex;

    void start(io_context& ctx)
    {
        ex = ctx.get_executor();
    }
};
```

The null state is testable with `explicit operator bool()` and comparable with `nullptr`. Calling `dispatch` or `post` on a null `any_executor` is undefined behavior - the same contract as dereferencing a null pointer.

---

## 6. Anticipated Objections

### 6.1 "But Mutexes Already Serialize"

They do. They also block. A mutex held across a `co_await` is either released (creating a window) or held (blocking the thread for the duration of the I/O operation). Neither is acceptable in a coroutine-native model where threads are shared across thousands of coroutines.

Strands serialize without blocking. The thread that posts a continuation to a strand is free to run other coroutines immediately. The strand enqueues the continuation and returns. Section 2 documents the full comparison.

### 6.2 "But `std::execution` Schedulers Handle This"

`std::execution` schedulers ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[6]</sup>) determine where work runs. They do not provide serialization guarantees. A scheduler that dispatches to a thread pool does not prevent concurrent execution of two senders scheduled on the same scheduler. Serialization in the sender model requires explicit synchronization primitives (`when_all` with sequenced dependencies, or async mutexes external to the sender algebra).

A strand is not a scheduler. It is a serialization wrapper around an executor. The distinction is structural: A scheduler says "run this here," a strand says "run this here, and not at the same time as that."

The two models are complementary. A strand can be used inside a sender-based system by wrapping a scheduler's executor. Nothing in this proposal conflicts with `std::execution`.

### 6.3 "But `any_executor` Adds Overhead"

It does. One vtable indirection per `dispatch` and `post` call. The overhead is bounded and constant: one pointer load, no allocation (with SBO), no template instantiation.

The alternative is a template parameter on every type that stores an executor: `connection<Executor>`, `session<Executor>`, `server<Executor>`. This produces template explosion, prevents separate compilation, and destroys ABI stability. [P4089R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4089r0.pdf)<sup>[7]</sup> documents why a second template parameter on the task type creates cross-library interoperability problems. The same argument applies to any type that stores an executor.

The vtable overhead is one pointer load per dispatch. The I/O operation behind the dispatch - a socket read, a timer wait, a DNS resolution - takes microseconds to milliseconds. The vtable load takes nanoseconds. The overhead is not measurable relative to the operation cost.

### 6.4 "But Strand Is Asio-Specific"

The name originates in Asio. The concept does not. Every concurrent system needs serialization without blocking. Go uses channels. Rust uses async-aware mutexes. .NET uses `SynchronizationContext`. The implementation differs; the requirement is universal.

The Asio strand has been deployed in production for over twenty years. It has been used in trading systems, game servers, web servers, and embedded systems. The field evidence for the abstraction is deeper than for any other C++ serialization primitive except `std::mutex` itself.

The coroutine-native strand in Capy inherits the guarantee and adapts the mechanism. The API shape is familiar to Asio users. The implementation is built on the IoAwaitable protocol's `continuation` and symmetric transfer. The name is established practice, not an implementation dependency.

**Strands are not Asio-specific. They are serialization-specific. Asio named them.**

---

## 7. What This Paper Does Not Standardise

### 7.1 Distributed Executors

A distributed executor dispatches work across process boundaries or across machines. Strands over distributed executors would require consensus protocols, network round-trips, and failure modes that are far outside the scope of this paper. This paper addresses single-process, multi-threaded serialization.

### 7.2 Priority Scheduling

A strand imposes ordering but not priority. All continuations dispatched through a strand run in FIFO order. Priority scheduling - running some continuations before others based on urgency - requires a priority queue inside the strand. This is a possible future extension. It is not part of this proposal.

### 7.3 Strand Groups

A strand group would allow multiple strands to share a common serialization boundary - "none of the coroutines in any of these strands execute concurrently with each other." The use case is real (multiple connection groups that share state). The design space is large. This paper does not address it.

### 7.4 Custom Allocators for `any_executor`

The SBO in `any_executor` handles the common case. For executors too large for SBO, the implementation allocates from the default allocator. A custom allocator parameter for `any_executor` is a possible future extension. It is not part of this proposal because the common executors fit in SBO and the use case for custom allocation has not been demonstrated.

---

## 8. Why Now

The executor utilities proposed here have been available in [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[5]</sup> for over twenty years (callback model) and in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> for the coroutine-native model. The need is not speculative.

| Year | Event                                                                                           |
|------|-------------------------------------------------------------------------------------------------|
| 2003 | Asio ships `strand` and `any_executor` (callback model)                                        |
| 2017 | [N4711](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4711.pdf)<sup>[8]</sup> Networking TS draft includes strand |
| 2020 | [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html)<sup>[9]</sup> executor unification (never deployed as unified) |
| 2024 | [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[6]</sup> `std::execution` adopted - does not include strand or type-erased executor |
| 2026 | Capy ships coroutine-native `strand` and `any_executor`                                        |

The standard library has `std::execution` schedulers but no serialization primitive and no owning type-erased executor. The gap is real. Every concurrent C++ application that uses async I/O needs both.

**The standard has the executor concept. It does not have the executor utilities. This paper fills the gap.**

---

## 9. Closing

We built this. It works. We are reporting what we found. Proposed wording for the vocabulary documented here lives in *Executor Utilities*<sup>[14]</sup>.

---

## Appendix A. `<std::io>` Synopsis (Informative)

Executor-utilities-only synopsis. The `Executor` concept and `executor_ref` live in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[2]</sup>.

```cpp
namespace std::io {

  // strand
  template<Executor Ex>
  class strand
  {
  public:
    using inner_executor_type = Ex;

    strand() = delete;
    explicit strand(Ex ex);

    strand(strand const&) = delete;
    strand& operator=(strand const&) = delete;

    strand(strand&& other) noexcept;
    strand& operator=(strand&& other) noexcept;

    ~strand();

    Ex const& get_inner_executor() const noexcept;

    execution_context& context() const noexcept;
    void on_work_started() const noexcept;
    void on_work_finished() const noexcept;

    std::coroutine_handle<>
    dispatch(continuation& c) const;

    void post(continuation& c) const;

    bool operator==(strand const& other)
        const noexcept;
    bool operator!=(strand const& other)
        const noexcept;
  };

  // any_executor
  class any_executor
  {
  public:
    any_executor() noexcept;
    any_executor(std::nullptr_t) noexcept;

    template<Executor Ex>
        requires (!std::same_as<
            std::decay_t<Ex>, any_executor>)
    any_executor(Ex ex);

    any_executor(any_executor const& other);
    any_executor(any_executor&& other) noexcept;

    any_executor& operator=(
        any_executor const& other);
    any_executor& operator=(
        any_executor&& other) noexcept;
    any_executor& operator=(
        std::nullptr_t) noexcept;

    ~any_executor();

    explicit operator bool() const noexcept;

    execution_context& context() const;
    void on_work_started() const noexcept;
    void on_work_finished() const noexcept;

    std::coroutine_handle<>
    dispatch(continuation& c) const;

    void post(continuation& c) const;

    bool operator==(any_executor const& other)
        const noexcept;
    bool operator!=(any_executor const& other)
        const noexcept;
    bool operator==(std::nullptr_t) const noexcept;
  };

}
```

---

## Appendix B. Capy Header Inventory

The vocabulary in this paper ships in the following headers in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup>. The list is a pointer to the implementation for the reader who wants to inspect it.

| Header                              | Provides                                      |
|-------------------------------------|-----------------------------------------------|
| `boost/capy/strand.hpp`             | `strand<Ex>`                                  |
| `boost/capy/any_executor.hpp`       | `any_executor`                                |

---

## Acknowledgments

Christopher Kohlhoff designed Asio's strand and `any_io_executor`. Two decades of production deployment across trading systems, game servers, web servers, and embedded systems established both abstractions as essential executor infrastructure. The coroutine-native forms in Capy inherit the guarantee and adapt the mechanism.

The Networking TS authors codified the strand and executor type erasure semantics in [N4711](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4711.pdf)<sup>[8]</sup> and [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[10]</sup>. The shapes in this paper are the shapes they specified, adapted for coroutine-native execution.

Lewis Baker's work on coroutine synchronization primitives in cppcoro informed the coroutine-specific design considerations in Section 2.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[3] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[5] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Strand and executor type erasure (Christopher Kohlhoff, 2003-2026).

[6] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[7] [P4089R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4089r0.pdf) - "On the Diversity of Coroutine Task Types" (Vinnie Falco, 2026).

[8] [N4711](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4711.pdf) - "Networking TS Working Draft" (2017).

[9] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Michael Wong, 2020).

[10] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[11] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[12] [P4094R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r0.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[13] [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf) - "Coroutine-Native I/O at a Derivatives Exchange" (Mungo Gill, 2026).

[14] *Executor Utilities* (Vinnie Falco, 2026). Companion ask paper. D0005R0.
