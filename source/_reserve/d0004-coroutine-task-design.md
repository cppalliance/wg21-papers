---
title: "Coroutine Task: Design Rationale"
document: D0004R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

C++ has coroutines. C++ does not have a coroutine task.

Every coroutine-based C++ library ships its own `task<T>`. [Folly](https://github.com/facebook/folly)<sup>[11]</sup> has one. [cppcoro](https://github.com/lewissbaker/cppcoro)<sup>[12]</sup> has one. [Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)<sup>[3]</sup> has `awaitable<T>`. [libunifex](https://github.com/facebookexperimental/libunifex)<sup>[13]</sup> has one. None of them compose with each other. The language gave us coroutines; the standard library did not give us the return type. This paper documents why the shape that ships in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> - one template parameter, lazy start, context propagation through the IoAwaitable protocol - is the right shape for the standard.

This paper is the design-rationale companion to *Coroutine Task*<sup>[8]</sup>, which contains the proposal-only specification and the straw poll. It is part of the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup>, in which the coroutine task is Paper 2. The IoAwaitable protocol that the task implements is defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[5]</sup> and [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[6]</sup>.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[9]</sup> and develops [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, plus three further Boost libraries built on them: Boost.Http, Boost.Beast2, and Boost.Burl. Every asynchronous entry point in these libraries returns `task<T>`. The body of work creates a bias toward a single coroutine task type with minimal template parameters.

This paper documents the design rationale for `task<T>`, the launch functions, and the execution contexts. The proposal-only ask paper is *Coroutine Task*<sup>[8]</sup>. The IoAwaitable protocol that `task<T>` implements is defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[5]</sup> and [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[6]</sup>.

A limitation of the proposed shape is honestly noted: `task<T>` is single-consumer. It cannot be awaited from two coroutines concurrently. Task groups and nurseries that manage multiple concurrent tasks are deferred to Paper 7 (Combinators). Section 8 records all deferrals.

This paper is Paper 2 in the [Network Endeavor](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) ([P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup>). It depends on Paper 1 (the IoAwaitable Protocol) - and that dependency is the protocol the promise type implements.

The companion papers are *Coroutine Task*<sup>[8]</sup> (proposal-only ask paper for the types in this paper), [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[5]</sup> and [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[6]</sup> (the IoAwaitable Protocol pair), and [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup> (the umbrella paper that places this work in series).

Every type proposed in the companion ask paper ships in Capy. Every Corosio example and test uses `task<T>` with `run()`. Appendix B is the inventory.

This paper asks for nothing.

---

## 2. Why One Template Parameter

`task<T>` has one template parameter. The result type. Nothing else.

The question the committee will ask: Where did the allocator, the executor, and the scheduler go?

### 2.1 The Allocator Is in the Frame

Coroutine frames are allocated by `promise_type::operator new`. The IoAwaitable protocol propagates the frame allocator from the parent coroutine to the child through TLS before `operator new` executes. The allocator does not appear in the task's type because the task does not choose its allocator - the execution context does. The propagation is forward, not parametric.

```cpp
std::io::task<int> compute()
{
    co_return 42;
}

std::io::task<int> caller()
{
    auto result = co_await compute();
    co_return result;
}
```

The frame allocator that `caller()` uses flows into `compute()` at the co_await. Neither function names an allocator. The frame allocator is infrastructure, not interface. Recycling allocators on MSVC yield a 3.1x throughput improvement ([P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[7]</sup> Section 5).

### 2.2 The Executor Is in the Protocol

The executor that runs the coroutine is part of the `io_env` - the environment bundle that the IoAwaitable protocol propagates through `await_suspend`. When a parent coroutine awaits a child task, the child inherits the parent's executor. The executor does not appear in the task's type because the task does not choose its executor - the caller's context provides it.

```cpp
std::io::task<> handle_client(std::io::any_stream& stream)
{
    // runs on whatever executor the parent was running on
    co_await stream.read_some(buf);
}
```

### 2.3 The Scheduler Is Not Needed

`task<T>` is not a work item that a scheduler picks off a queue. It is a coroutine that suspends and resumes. The scheduler concept in `std::execution` serves a different purpose: It represents a source of execution resources for sender algorithms. A coroutine task does not need to name a scheduler because it does not schedule itself - it is resumed by the entity that completes the I/O operation it was waiting on.

### 2.4 The Cost of Extra Parameters

Every template parameter that appears in the task's type propagates through every function signature, every container, and every generic algorithm that stores or passes tasks. `task<T, Alloc>` means every function that returns a task must name the allocator. `task<T, Alloc, Exec>` means every function must name both. The type system tax compounds through the codebase.

`asio::awaitable<T>` has one template parameter. It proved the shape works at scale. `task<T>` keeps that property and adds frame allocator propagation through the protocol rather than the type.

**One parameter. The protocol carries the rest.**

---

## 3. Why Lazy, Not Eager

An eager task starts executing the moment it is constructed. A lazy task starts executing the moment it is awaited.

### 3.1 The Eager Problem

An eager task that starts immediately has three structural problems:

1. **No context at construction.** The coroutine needs an executor and a frame allocator. If the task starts before anyone awaits it, where do they come from? The answer is either a global default (implicit, surprising) or a constructor parameter (which puts the executor back in the type).

2. **Wasted work on discard.** An eager task that is constructed but never awaited has already begun executing. If the caller decides not to proceed - a timeout, a cancellation, a different branch - the work is wasted. The resources (file descriptors, connections, memory) are allocated and must be cleaned up.

3. **Composition breaks.** `when_all(task_a(), task_b())` with eager tasks means both tasks are already running before the combinator sees them. The combinator cannot control start order, cannot inject a shared stop token, cannot batch-allocate frames.

### 3.2 What Lazy Provides

Lazy start means the caller controls when execution begins. The sequence is:

1. The coroutine function is called. A `task<T>` is returned. The coroutine is suspended at `initial_suspend`.
2. The caller awaits the task (or passes it to `run()` or `run_async()`).
3. `await_suspend` propagates the execution context. The coroutine begins.

Between steps 1 and 2, the task is an inert value. It can be stored, moved, passed to a combinator, or discarded without cost. The caller has full control.

### 3.3 Lazy Is the Ecosystem Default

Every major C++ coroutine library ships a lazy task:

| Library        | Task type           | Start |
| -------------- | ------------------- | ----- |
| cppcoro        | `task<T>`           | Lazy  |
| Folly          | `Task<T>`           | Lazy  |
| libunifex      | `task<T>`           | Lazy  |
| Asio           | `awaitable<T>`      | Lazy  |
| Capy           | `task<T>`           | Lazy  |

The ecosystem converged on lazy. This paper follows the convergence.

**Lazy start. The caller controls when. The frame is not wasted.**

---

## 4. Why `run()` and `run_async()` Are Free Functions

### 4.1 `run()` Is the Entry Point

Synchronous code must bridge to asynchronous code somewhere. `run()` is that bridge. It is a free function because it operates on any `task<T>`, not on a specific execution context.

```cpp
int main()
{
    return std::io::run(compute_result());
}
```

`run()` blocks the calling thread. It creates or uses an execution context, starts the task, and drives the event loop until the task completes. The result type is `T` - the same type the task produces.

Making `run()` a free function rather than a member of `thread_pool` or `system_context` keeps the call site minimal. The common case - a program that wants to run one top-level coroutine - should be one line.

### 4.2 `run_async()` Is Fire-and-Forget

`run_async()` submits a task for concurrent execution on the current execution context. It is the coroutine-native equivalent of spawning a background thread - except the task runs on the existing pool and inherits the caller's context.

```cpp
std::io::task<> server(std::io::tcp_acceptor& acceptor)
{
    for (;;)
    {
        auto [ec, stream] = co_await acceptor.accept();
        if (ec) break;
        std::io::run_async(
            handle_client(std::move(stream)));
    }
}
```

`run_async()` is a free function for the same reason `run()` is: It operates on any task, and the execution context is inherited through the protocol.

**Free functions. Minimal signatures. The protocol carries the context.**

---

## 5. Why `thread_pool` and `system_context`

### 5.1 Thread Pool

A coroutine-native I/O system needs an execution context that multiplexes coroutines across threads. `thread_pool` is that context. It satisfies `execution_context` (defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[5]</sup>). Its executor satisfies `Executor`.

The pool manages a fixed number of worker threads. Each worker runs an event loop that dequeues and resumes coroutines. The pool provides `dispatch` (run immediately if already on a pool thread, otherwise enqueue) and `post` (always enqueue).

### 5.2 System Context

`system_context` is a process-wide singleton backed by a `thread_pool`. It exists because most programs need exactly one execution context and do not want to manage its lifetime.

```cpp
int main()
{
    auto result = std::io::run(do_work());
}
```

`run()` without an explicit context uses `system_context::instance()`. The thread count is implementation-defined. The user who needs control over thread count creates a `thread_pool` explicitly.

### 5.3 Why Not `std::jthread`

`std::jthread` is a single thread with cooperative cancellation. A `thread_pool` is a collection of threads with a shared work queue. The two serve different purposes. `std::jthread` does not provide `dispatch`/`post` semantics, does not provide a shared work queue, and does not satisfy `execution_context`. A thread pool built from `std::jthread` instances would wrap each thread in infrastructure that `std::jthread` does not provide. The pool is the right abstraction.

**One pool for work distribution. One singleton for the common case.**

---

## 6. Convergence

Five language ecosystems provide a standard coroutine task or equivalent. The shapes differ in surface; they agree in substance.

| Ecosystem   | Task type                  | Start | Parameters          | Launch                      |
| ----------- | -------------------------- | ----- | ------------------- | --------------------------- |
| Go          | goroutine                  | Eager | (none - implicit)   | `go f()`                    |
| Rust        | `tokio::spawn`/`JoinHandle`| Lazy  | Result type only    | `tokio::spawn(f())`         |
| .NET        | `Task<T>`                  | Eager | Result type only    | `Task.Run()`                |
| Python      | `asyncio.Task`             | Eager | Result type only    | `asyncio.create_task()`     |
| Swift       | `Task<Success, Failure>`   | Eager | Result, Error       | `Task { ... }`              |
| C++ (Capy)  | `task<T>`                  | Lazy  | Result type only    | `run()`, `run_async()`      |

Observations:

1. **Result-only parameterisation.** No ecosystem parameterises the task type on the allocator, the executor, or the scheduler. The execution context is a runtime concern, not a type-system concern. Go does not even have a visible task type - the goroutine is implicit.

2. **Eager vs lazy.** Go, .NET, Python, and Swift use eager start. Rust and C++ use lazy start. The eager ecosystems have garbage collection or runtime-managed memory that makes eager-start safe. C++ does not. Lazy start is the safe default for a language without garbage collection.

3. **Launch function.** Every ecosystem has one. Go has `go`. Rust has `tokio::spawn`. .NET has `Task.Run`. Python has `create_task`. Swift has the `Task` initialiser. C++ has `run()` and `run_async()`.

**Six ecosystems. One template parameter. The rest is runtime.**

---

## 7. Anticipated Objections

### 7.1 "But `std::execution` Already Provides Task-Like Functionality"

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[10]</sup> provides sender algorithms that compose at compile time. The sender model does not provide a coroutine return type. A user who writes `task<T> f() { co_await ...; co_return ...; }` needs a concrete `task<T>`. `std::execution` does not define one.

The two models serve different domains. Senders compose work graphs for schedulers. `task<T>` is the return type of a coroutine that suspends on I/O. A sender-based I/O library would still benefit from a standard `task<T>` for coroutines that call into it.

`task<T>` does not compete with `std::execution`. It is the vocabulary type the language mechanism already needs.

### 7.2 "But One Template Parameter Loses Allocator and Executor Control"

It does not lose control. It moves control from the type system to the protocol. The IoAwaitable protocol propagates the frame allocator and the executor through `await_suspend`. The user who wants a recycling allocator configures the execution context. The user who wants a specific executor posts to it. Both get what they want without naming the allocator or executor in every function signature.

The cost of parametric control is type proliferation. `task<T, Alloc, Exec>` means every function must agree on the allocator and executor types. The cost of protocol-based control is indirection through TLS for the allocator. The 3.1x throughput improvement on MSVC ([P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[7]</sup>) demonstrates that the protocol approach does not sacrifice performance.

### 7.3 "But Lazy Coroutines Are Less Intuitive Than Eager Ones"

Intuition depends on the mental model. If the mental model is "function call," eager feels natural - calling the function runs it. If the mental model is "value that represents work," lazy feels natural - the value is inert until consumed.

C++ coroutines are values. A `task<T>` returned from a coroutine function is a handle to a suspended coroutine. The user must do something with it - await it, pass it to `run()`, or pass it to a combinator. This is the same model as `std::future<T>`: The future is inert; `.get()` blocks.

The ecosystem has already made the choice. Every major C++ coroutine library ships a lazy task (Section 3.3). The committee would be fighting established practice by mandating eager start.

### 7.4 "But `thread_pool` Belongs in the OS Abstraction Layer"

`thread_pool` is not a platform primitive. It is a C++ class that creates `std::thread` objects and runs an event loop on each. It has no platform-specific code beyond what `std::thread` already provides. It belongs in the same layer as `std::thread` itself.

`system_context` is a convenience wrapper around `thread_pool`. It provides a default execution context for programs that do not want to manage pool lifetime. The singleton pattern is the same as `std::cout` - a process-wide default that most programs use and some programs replace.

### 7.5 "But a Standard Task Type Will Ossify the Design"

The design has been stable for five years. Lewis Baker's cppcoro<sup>[12]</sup> shipped `task<T>` in 2017. Folly<sup>[11]</sup> shipped `Task<T>`. Asio shipped `awaitable<T>`. Capy ships `task<T>`. The interface has not changed: lazy start, one template parameter, symmetric transfer on completion. There is nothing left to discover about the basic shape.

What evolves is the execution context and the protocol - and those are not part of the task's type. A future revision of the IoAwaitable protocol can propagate additional context without changing `task<T>`.

---

## 8. What This Paper Does Not Standardise

Five deferrals. Each is named so the scope is unambiguous.

### 8.1 Task Groups and Nurseries

`when_all` and `when_any` - the structured concurrency primitives that manage multiple concurrent tasks - are the subject of Paper 7 (Combinators) in the series. `task<T>` is the building block; the combinators are the composition layer.

### 8.2 Cancellation Policies

The stop token propagated by the IoAwaitable protocol provides cooperative cancellation. Cancellation policies - what happens when a parent is cancelled, whether children are cancelled automatically, whether cancellation is propagated depth-first or breadth-first - are policy decisions that belong in the combinator layer, not in the task type.

### 8.3 Custom Schedulers

`task<T>` runs on whatever executor the IoAwaitable protocol provides. Custom scheduler integration - mapping a `std::execution::scheduler` to an `Executor`, or vice versa - is a bridge that belongs in a separate paper. This paper proposes `thread_pool` and `system_context` as the execution contexts for coroutine-native I/O.

### 8.4 Multi-Consumer Tasks

`task<T>` is single-consumer. It can be awaited exactly once. A multi-consumer variant - a `shared_task<T>` that multiple coroutines can await concurrently, with the result broadcast to all waiters - is a useful extension. It is not part of this paper because the single-consumer shape is sufficient for I/O and the multi-consumer shape introduces reference-counting and lifetime questions that deserve separate treatment.

### 8.5 Result Storage Customisation

`task<T>` stores its result in the promise. A future extension could allow the result to be stored externally (in a caller-provided buffer, in shared memory, in a memory-mapped region). This paper does not address result storage because the promise-owned model is sufficient for the I/O domain and the alternatives introduce ABI constraints.

---

## 9. Why Now

The language shipped coroutines in C++20. Six years later, the standard library has no coroutine return type.

| Year | Event                                      |
| ---- | ------------------------------------------ |
| 2017 | cppcoro ships `task<T>`<sup>[12]</sup>     |
| 2017 | Folly ships `Task<T>`<sup>[11]</sup>       |
| 2020 | C++20 ships coroutines                     |
| 2020 | Asio ships `awaitable<T>`                  |
| 2023 | Capy ships `task<T>`<sup>[1]</sup>         |
| 2026 | The standard library has no task type       |

Every library invents its own. None compose with each other. A function that returns Folly's `Task<T>` cannot be awaited from cppcoro's `task<T>`. A function that returns Asio's `awaitable<T>` cannot be awaited from Capy's `task<T>`. The ecosystem is fragmented on the most basic coroutine vocabulary type.

The standard task type is the vocabulary that lets the ecosystem compose. It is the `std::string` of coroutines - not the only possible string type, but the one everyone agrees to use at interfaces.

**Six years. Five incompatible tasks. The standard library has none.**

---

## 10. Closing

```cpp
namespace std::io {

  template<class T = void>
  class task;

  template<class T> T run(task<T>);
  template<class T> void run_async(task<T>);

  class thread_pool;
  class system_context;

}
```

We built this. It works. We are reporting what we found. Proposed wording for the types documented here lives in *Coroutine Task*<sup>[8]</sup>.

---

## Appendix A. `<std::io>` Synopsis (Informative)

Task-only synopsis. The IoAwaitable protocol that the promise type implements is defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[5]</sup>.

```cpp
namespace std::io {

  // The coroutine task
  template<class T = void>
  class task
  {
  public:
      using value_type = T;

      struct promise_type;

      task(task&& other) noexcept;
      task& operator=(task&& other) noexcept;
      ~task();

      task(task const&) = delete;
      task& operator=(task const&) = delete;
  };

  // Launch functions
  template<class T>
  T run(task<T> t);

  template<class T>
  void run_async(task<T> t);

  // Execution contexts
  class thread_pool
  {
  public:
      explicit thread_pool(std::size_t thread_count);
      ~thread_pool();

      thread_pool(thread_pool const&) = delete;
      thread_pool& operator=(thread_pool const&) = delete;

      using executor_type = /* unspecified */;
      executor_type get_executor() noexcept;

      void join();
      void stop();
  };

  class system_context
  {
  public:
      system_context(system_context const&) = delete;
      system_context& operator=(system_context const&) = delete;

      static system_context& instance() noexcept;

      using executor_type = /* unspecified */;
      executor_type get_executor() noexcept;

      void join();
      void stop();
  };

}
```

---

## Appendix B. Capy Header Inventory

The task type, launch functions, and execution contexts ship in the following [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> headers. The IoAwaitable protocol headers are listed in [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[6]</sup>.

| Header                                  | Provides                                              |
| --------------------------------------- | ----------------------------------------------------- |
| `boost/capy/task.hpp`                   | `task<T>`, `task<T>::promise_type`                    |
| `boost/capy/run.hpp`                    | `run(task<T>)`                                        |
| `boost/capy/run_async.hpp`              | `run_async(task<T>)`                                  |
| `boost/capy/thread_pool.hpp`            | `thread_pool`                                         |
| `boost/capy/system_context.hpp`         | `system_context`                                      |

---

## Acknowledgments

Gor Nishanov and Lewis Baker designed C++20 coroutines. `coroutine_handle<>`, `promise_type`, symmetric transfer, and stackless frames are the language mechanisms that make `task<T>` possible. Lewis Baker's cppcoro<sup>[12]</sup> demonstrated the lazy single-parameter task shape years before standardization was on the table.

Christopher Kohlhoff designed Asio's executor model, codified in the [Networking TS](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf)<sup>[14]</sup>. The `dispatch`/`post` semantics of `thread_pool` in this paper follow the model Asio established. Asio's `awaitable<T>` proved that one template parameter is sufficient for production I/O.

The `std::execution` authors - Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators - explored execution contexts and schedulers at depth. Their `system_context` concept informs the `system_context` in this paper.

Peter Dimov's review of the Capy task implementation surfaced the frame-allocator propagation timing questions that led to the TLS-based forward propagation model documented in [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf)<sup>[6]</sup>.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[3] [Boost.Asio](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) - Executor model, completion tokens, and `awaitable<T>` (Christopher Kohlhoff, 2003-2026).

[4] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[5] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[6] [P4172R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r0.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[7] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Senders and Coroutines" (Vinnie Falco, Mungo Gill, 2026).

[8] *Coroutine Task* (Vinnie Falco, 2026). Companion ask paper. D0003R0.

[9] [Boost.Beast](https://github.com/boostorg/beast) - HTTP and WebSocket built on Boost.Asio (Vinnie Falco, 2017-2026).

[10] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[11] [Folly](https://github.com/facebook/folly) - Facebook's C++ library, including `folly::coro::Task<T>` (Meta Platforms, 2012-2026).

[12] [cppcoro](https://github.com/lewissbaker/cppcoro) - Coroutine library for C++20, including `cppcoro::task<T>` (Lewis Baker, 2017-2020).

[13] [libunifex](https://github.com/facebookexperimental/libunifex) - Unified executors library with sender/receiver model and `task<T>` (Eric Niebler, Kirk Shoop, Lewis Baker, 2020-2023).

[14] [N4771](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).
