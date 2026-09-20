---
title: "Combinators: Design Rationale"
document: D0014R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Two combinators complete Stage One of the Network Endeavor.

After Papers 1-6, a user has `task<T>` coroutines, type-erased streams, standard buffers, executors, and strands. What is missing is the ability to do two things at once. `when_all` and `when_any` fill that gap. This paper documents why those two combinators are the right primitives, why the design choices were forced by the constraints of structured concurrency, how five other ecosystems converged on the same shapes, and what was deliberately deferred. The companion ask paper *Combinators*<sup>[1]</sup> proposes the vocabulary. This paper is the audit trail.

This paper is Paper 7 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[2]</sup>. It depends on Paper 2 (Coroutine Task, D0003R0<sup>[3]</sup> / D0004R0<sup>[4]</sup>).

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops [Capy](https://github.com/cppalliance/capy)<sup>[5]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

This paper asks for nothing.

---

## 2. Structured Concurrency

### 2.1 Why Combinators Matter

A coroutine that does one thing at a time is sequential code with suspension points. The value of an async model appears when multiple operations proceed concurrently. Without combinators, the programmer must coordinate concurrent coroutines by hand - spawning fire-and-forget tasks, synchronizing with mutexes or condition variables, managing lifetimes manually. Every hand-rolled coordination is a new opportunity for lifetime errors, data races, and leaked tasks.

Structured concurrency eliminates this class of errors by enforcing a scope discipline: Child operations do not outlive the parent that launched them. The parent suspends until all children complete. RAII works. Stack unwinding works. Error propagation works. The combinator is the structured concurrency primitive - the `{}` block of concurrent code.

### 2.2 The Fork-Join Model

Both combinators implement fork-join:

1. **Fork.** Launch N children concurrently. Each child inherits the parent's execution environment through the IoAwaitable protocol.
2. **Join.** The parent suspends until the join condition is met. For `when_all`, the condition is "all children completed." For `when_any`, the condition is "one child completed and all others exited."
3. **Cleanup.** No child outlives the join. The parent's scope is intact when it resumes.

This model is the concurrent analogue of a function call: The caller does not proceed until the callee returns. The difference is that the caller launched multiple callees.

### 2.3 Why Two Combinators

`when_all` is parallel composition - do everything, collect all results. `when_any` is racing composition - do everything, keep the first result. These two modes cover the overwhelming majority of concurrent patterns in I/O code:

- **`when_all`**: parallel fetch, scatter/gather, multi-resource acquisition.
- **`when_any`**: timeout (race against a timer), graceful shutdown (race against a signal), first-responder (race against multiple backends).

Additional combinators exist (Section 7). Two cover the common case. The standard should ship what is proven and defer what is speculative.

---

## 3. `when_all` Design

### 3.1 Why Variadic

The children of a `when_all` are typically heterogeneous: One fetches from a database, another reads a file, a third calls a remote API. Their return types differ. A variadic parameter pack expresses this directly. The alternative - a homogeneous container of awaitables - requires type erasure and loses the per-child result type.

```cpp
// Heterogeneous: each child has a distinct return type.
auto [users, orders, config] = co_await io::when_all(
    fetch_users(db),
    fetch_orders(db),
    load_config(file));
```

A homogeneous overload taking a range of identical awaitables is useful for fan-out patterns and is a natural future extension. The variadic form is the more general primitive and ships first.

### 3.2 Why `std::tuple` Return

The variadic pack produces heterogeneous results. `std::tuple` is the standard vocabulary for heterogeneous positional aggregates. Structured bindings make `std::tuple` ergonomic at the call site. The mapping from argument position to result position is fixed at compile time - no runtime indexing, no variant dispatch.

### 3.3 Error Propagation

When one child fails in a `when_all`, the remaining children must be cancelled. The alternative - letting other children run to completion and then reporting the error - wastes work and delays error delivery. The design cancels early:

1. The first child to fail triggers the stop token of every sibling.
2. `when_all` waits for all siblings to exit cooperatively.
3. `when_all` propagates the first observed error.

**Why discard subsequent errors.** If child A fails, siblings B and C are cancelled. B and C may themselves report errors - but those errors are consequences of the cancellation, not independent failures. Propagating only the root cause (child A's error) gives the caller actionable information. Collecting all errors would require a multi-error type (`std::exception_ptr` list, error vector, or nested exception) that adds vocabulary burden for a case that is rarely useful.

The companion ask paper *Combinators*<sup>[1]</sup> Section 6.1 states the tradeoff. A future `when_all_settled` variant that collects all results regardless of success or failure is a natural extension if demand materializes.

### 3.4 Cancellation Timing

`when_all` does not cancel children on its own initiative. It cancels only in two cases:

1. A child failed (Section 3.3).
2. The caller's stop token was triggered externally.

Otherwise, every child runs to completion. This is the expected behavior for parallel composition - the caller wants all results.

---

## 4. `when_any` Design

### 4.1 Why First-Completes-Wins

The defining property of `when_any` is that the caller wants the first available result. The use cases are structural:

- **Timeout.** Race an I/O operation against a timer. Whichever completes first determines the outcome.
- **Graceful shutdown.** Race an accept loop against a signal handler. The signal cancels the loop.
- **Redundant requests.** Send the same query to two backends. Use the first response.

In each case, the remaining children are waste once a winner exists. Cancelling them immediately is both correct (the caller does not want their results) and efficient (no resources are consumed after the decision is made).

### 4.2 Cancellation of Siblings

When the first child completes:

1. `when_any` triggers a combinator-internal stop source.
2. Each remaining child's effective stop token is a composite of the caller's stop token and the combinator-internal stop source. Triggering either source triggers the child's token.
3. Each remaining child observes the stop request and exits cooperatively.
4. `when_any` waits for all remaining children to exit before resuming the caller.

Step 4 is the structured guarantee. Without it, a cancelled child could outlive the `when_any` scope and access destroyed state. Every structured concurrency framework enforces this constraint.

### 4.3 Symmetric Transfer for Cancellation

When `when_any` cancels a sibling, the cancellation path may resume a coroutine on a different thread. The IoAwaitable protocol uses symmetric transfer (`await_suspend` returning `coroutine_handle<>`) to handle this without stack buildup. If the sibling can be resumed on the current thread, `await_suspend` returns its handle for direct resumption. If not, the sibling is posted to its executor and `await_suspend` returns `std::noop_coroutine()`.

This is not a new mechanism. It is the same symmetric transfer that [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[7]</sup> uses for all coroutine resumption. The combinator inherits the protocol; it does not extend it.

### 4.4 Result Delivery

The first child's result is the result of the `when_any` expression. The return type depends on the number and types of children:

- **Homogeneous children** (all return the same type `T`): The result type is `T`.
- **Heterogeneous children** (different return types): The result type is `std::variant<result_of_t<Awaitables>...>`.

The homogeneous case avoids the variant overhead for the common pattern (e.g. racing two instances of the same operation). The heterogeneous case preserves full type information. The caller uses `std::visit` or `std::get_if` to inspect the result.

---

## 5. Convergence

Five ecosystems provide combinator primitives with the same semantics. The shapes were arrived at independently.

| Ecosystem | All | Any | Cancellation model |
|-----------|-----|-----|-------------------|
| Go | `errgroup.Group.Go` + `Wait` | `select` | Context cancellation |
| Rust (Tokio) | `tokio::join!` | `tokio::select!` | Drop-based cancellation |
| .NET | `Task.WhenAll` | `Task.WhenAny` | `CancellationToken` |
| Python (asyncio) | `asyncio.gather` | `asyncio.wait(FIRST_COMPLETED)` | `Task.cancel()` |
| Swift | `async let` / `TaskGroup` | `TaskGroup` + first result | Structured concurrency |

### 5.1 Go

Go's `errgroup` package provides `Go` (launch a goroutine) and `Wait` (wait for all goroutines, return the first error). `select` blocks until one of several channel operations can proceed. The `context` package provides cancellation propagation through `context.WithCancel`.

Go's `select` is a language construct, not a library function. It operates on channels, not on coroutines. The semantic intent - "wait for the first of N events" - is identical.

### 5.2 Rust

Tokio's `join!` macro awaits all futures concurrently. `select!` macro awaits the first future to complete and drops the rest. Cancellation is implicit: Dropping a future cancels it. The Rust ownership model makes this safe - a dropped future cannot be accessed.

C++ does not have Rust's drop semantics. The combinator must explicitly cancel siblings via stop tokens and wait for cooperative exit. The structured guarantee is the same; the mechanism differs because the languages differ.

### 5.3 .NET

`Task.WhenAll` returns a task that completes when all input tasks complete. `Task.WhenAny` returns a task that completes when any input task completes. Cancellation uses `CancellationToken`, which is compositional - a child's token can be linked to a parent's token. The C++ stop token model follows the same compositional pattern.

### 5.4 Python

`asyncio.gather` runs awaitables concurrently and returns all results. `asyncio.wait` with `return_when=FIRST_COMPLETED` returns when the first task completes. Cancellation uses `Task.cancel()`, which raises `CancelledError` in the task. Python's cooperative cancellation via exceptions is analogous to C++'s cooperative cancellation via stop tokens - both require the task to check and respond.

### 5.5 Swift

Swift's structured concurrency uses `async let` for static fork-join (analogous to `when_all`) and `TaskGroup` for dynamic fork-join. Cancellation propagates through the task tree automatically. `TaskGroup` supports "first result wins" patterns. Swift's model is the closest analogue to the structured guarantees in this paper.

**Five ecosystems. Same two operations. Same cancellation requirement.**

---

## 6. Anticipated Objections

### 6.1 "But `std::execution` `when_all` already exists"

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[8]</sup> defines `execution::when_all` as a sender algorithm that completes when all child senders complete. The algorithm operates on senders, not on awaitables. It serves the sender composition model.

The combinators in this paper operate on `IoAwaitable` - the coroutine execution protocol defined in [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[7]</sup>. They propagate the executor, stop token, and frame allocator through `await_suspend`. They use symmetric transfer for zero-overhead context switching. They return results through `co_await`.

Two combinator families for two async models is the same principle as two condition variable types for two lock models (`std::condition_variable` and `std::condition_variable_any`). Domain separation is not duplication.

A bridge is straightforward: A `sender_awaitable` adapter could allow a sender to be used as a child in `io::when_all`. The combinators do not preclude interoperability; they provide the native vocabulary for the coroutine model.

### 6.2 "But these should be sender algorithms"

The position that all async composition should be expressed as sender algorithms is one design philosophy. The coroutine-native model is another.

The gap is structural. Sender algorithms compose at compile time through template metaprogramming. Coroutine combinators compose at runtime through frame allocation and symmetric transfer. Forcing coroutine composition through a sender layer loses the properties documented in [P4088R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r0.pdf)<sup>[9]</sup>: structural type erasure, amortized-zero-allocation frame propagation, and zero-cost context switching.

[P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[10]</sup> documents the structural gaps at the sender-coroutine boundary. The symmetric transfer gap documented in [P2583R4](https://isocpp.org/files/papers/P2583R4.pdf)<sup>[11]</sup> is directly relevant to combinator cancellation paths.

### 6.3 "But cancellation semantics are underspecified"

The cancellation model in this paper inherits entirely from [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[7]</sup>'s IoAwaitable protocol and from `std::stop_token`. No new cancellation mechanism is introduced. The combinators compose existing mechanisms:

- Each child inherits a stop token from its `io_env`.
- `when_any` creates an internal `std::stop_source` and composes it with the inherited token.
- Cancellation is cooperative: Children must check their stop token and exit.

The cooperativity is a feature. Forceful cancellation - destroying a coroutine frame while its local variables have active destructors - is undefined behavior. Cooperative cancellation is the only correct model for C++ coroutines. Swift, Kotlin, and Python all use cooperative cancellation for the same reason.

### 6.4 "But two combinators are not enough"

Two combinators are not all. They are enough.

`when_all` and `when_any` implement the two fundamental join conditions: all-complete and first-complete. Every production concurrent networking application the author has built or examined uses one of these two patterns at its concurrency boundaries. More sophisticated patterns exist and are deferred (Section 7). The standard should ship what is proven and used, not what is imaginable and untested.

Lewis Baker's [cppcoro](https://github.com/lewissbaker/cppcoro)<sup>[12]</sup> shipped `when_all` and `when_all_ready` for C++20 coroutines. Asio's `experimental::parallel_group` ships both patterns. Tokio ships `join!` and `select!`. In each case, two primitives have been sufficient for the ecosystem to build on.

---

## 7. Deferrals

The following combinators are recognized as useful but are not proposed in this paper. Each requires additional design work or usage evidence before standardization.

### 7.1 `race`

A variant of `when_any` that does not wait for cancelled siblings to exit. `race` trades the structured guarantee for lower latency. It is appropriate when children are stateless or when the caller can tolerate dangling work. The safety implications require careful specification and possibly a naming convention (Section 7 of [P4035R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4035r1.pdf)<sup>[13]</sup> discusses escape-hatch naming).

### 7.2 `first_success`

A variant of `when_any` that skips errors and returns the first successful result. If all children fail, it reports the last error (or an aggregate). Useful for redundant-backend patterns. Requires a policy for error collection.

### 7.3 Timeout Combinator

A convenience wrapper around `when_any(operation, timer.wait())` that returns an `error_code` on timeout. Useful but easily composed from `when_any` and a timer. The convenience does not justify additional vocabulary until the timer (Paper 8) ships.

### 7.4 Task Groups and Nurseries

Dynamic structured concurrency - launching a variable number of children determined at runtime. The Trio nursery model (Python), Swift `TaskGroup`, and Go `errgroup.Group` all provide this. It is the natural successor to the static variadic combinators in this paper and is planned for a future paper once the variadic primitives have been reviewed.

---

## 8. Why Now

Paper 7 completes Stage One of the Network Endeavor. The claim in [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[2]</sup> Section 7.1 is that Stage One papers deliver the vocabulary for the entire async I/O ecosystem. That claim is false without combinators.

After Papers 1-6, a user has:
- `task<T>` for coroutine bodies (Paper 2).
- `thread_pool` and `system_context` for execution (Paper 2).
- `strand` for serialization (Paper 3).
- Buffer vocabulary for data handling (Papers 4, 5).
- Stream concepts for byte I/O (Paper 6).

What is missing is concurrency within a single coroutine. The programmer who wants to accept connections while waiting for a shutdown signal must launch fire-and-forget tasks and synchronize by hand. `when_any` makes that a one-liner:

```cpp
co_await io::when_any(
    accept_loop(acceptor, handler),
    signal_set.wait());
```

The programmer who wants to fetch two resources in parallel must serialize the fetches or introduce manual synchronization. `when_all` makes that a one-liner:

```cpp
auto [resp1, resp2] = co_await io::when_all(
    fetch(stream1, "/api/users"),
    fetch(stream2, "/api/orders"));
```

Without these primitives, Stage One delivers sequential I/O with good vocabulary. With them, it delivers concurrent I/O with good vocabulary. The difference is the difference between a library and a foundation.

---

## 9. Closing

Every concurrent networking application does the same two things: Wait for all children, or wait for the first child. Five ecosystems ship the same two primitives. The shapes are forced by the constraints of structured concurrency. The standard should ship them.

---

## Appendix A: Synopsis

```cpp
namespace std::io {

  // [io.when_all], when_all
  template<IoAwaitable... Awaitables>
  /* unspecified */ when_all(Awaitables&&... awaitables);

  // Preconditions: sizeof...(Awaitables) >= 1.
  // Effects: launches each awaitable concurrently on
  //   the caller's executor. Returns an awaitable
  //   that completes when every child has completed.
  // Returns: an IoAwaitable yielding
  //   std::tuple<result_of_t<Awaitables>...>.
  // Error handling: cancels remaining children on
  //   first failure; propagates first error.

  // [io.when_any], when_any
  template<IoAwaitable... Awaitables>
  /* unspecified */ when_any(Awaitables&&... awaitables);

  // Preconditions: sizeof...(Awaitables) >= 1.
  // Effects: launches each awaitable concurrently on
  //   the caller's executor. Returns an awaitable
  //   that completes when the first child completes,
  //   cancelling remaining children.
  // Returns: an IoAwaitable yielding the first
  //   child's result.
  // Error handling: propagates the first child's
  //   result, whether value or error.

}
```

---

## Appendix B: Capy Headers

The combinator implementation in Capy:

| Header | Contents |
|--------|----------|
| `capy/io/when_all.hpp` | `when_all` function template, `when_all_awaitable` implementation |
| `capy/io/when_any.hpp` | `when_any` function template, `when_any_awaitable` implementation |
| `capy/io/detail/combinator_state.hpp` | Shared state for child tracking, stop token composition, result storage |
| `capy/io/detail/child_task.hpp` | Child coroutine wrapper with stop token forwarding |

Corosio usage:

| File | Usage |
|------|-------|
| `corosio/tcp_server.hpp` | `when_any(accept_loop, signal_set.wait())` for graceful shutdown |
| `corosio/examples/echo_server.cpp` | `when_all` for per-connection read/write concurrency |
| `corosio/examples/parallel_fetch.cpp` | `when_all` for concurrent HTTP resource retrieval |

---

## Acknowledgments

Lewis Baker designed `cppcoro::when_all` and `cppcoro::when_all_ready`, demonstrating that C++20 coroutine combinators could be both correct and efficient.

Christopher Kohlhoff's `asio::experimental::parallel_group` explored the design space in a callback model, providing evidence that both all-complete and first-complete patterns are fundamental.

Nathaniel J. Smith articulated the structured concurrency discipline in the Trio project. Roman Elizarov brought structured concurrency to Kotlin coroutines. Martin S&uuml;strik pioneered structured concurrency in libdill.

The authors of `std::execution` - Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators - designed `std::stop_token` and `std::stop_source`. The combinators in this paper inherit that mechanism without modification.

---

## References

[1] *Combinators* (Vinnie Falco, 2026). Companion ask paper. D0013R0.

[2] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[3] D0003R0 - "Coroutine Task" (Vinnie Falco, 2026). Companion ask paper for `task<T>` and launch functions.

[4] D0004R0 - "Coroutine Task: Design Rationale" (Vinnie Falco, 2026). Companion design paper for the task type.

[5] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[6] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[7] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[8] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[9] [P4088R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r0.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[10] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Senders and Coroutines" (Vinnie Falco, Mungo Gill, 2026).

[11] [P2583R4](https://isocpp.org/files/papers/P2583R4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).

[12] [cppcoro](https://github.com/lewissbaker/cppcoro) - A library of coroutine abstractions for C++ (Lewis Baker, 2017-2020).

[13] [P4035R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4035r1.pdf) - "The Need for Escape Hatches" (Vinnie Falco, 2026).
