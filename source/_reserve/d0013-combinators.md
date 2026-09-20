---
title: "Combinators"
document: D0013R0
date: 2026-05-15
intent: info
audience: LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper asks the committee to advance two structured concurrency combinators - `when_all` and `when_any` - as standard library vocabulary for coroutine-native I/O.

The combinators are the final primitives needed to write a complete concurrent networking application against the standard. `when_all` awaits every child and returns when all complete. `when_any` awaits the first to complete and cancels the rest. Both propagate errors and integrate with `std::stop_token`. The shapes ship in [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> today and are used in [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>'s `tcp_server` for concurrent accept loops.

The companion paper *Combinators: Design Rationale*<sup>[7]</sup> provides the design rationale, the convergence record across five ecosystems, anticipated objections, and the deferrals. Read this paper for the proposal; read the companion when you need the audit trail.

This paper is Paper 7 in the series defined by [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[3]</sup>. It depends on Paper 2 (Coroutine Task, D0003R0<sup>[4]</sup> / D0004R0<sup>[5]</sup>) for `task<T>` and the IoAwaitable protocol.

---

## Revision History

### R0: May 2026 (post-Brno mailing)

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author develops [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper is the proposal-only ask paper for the combinator vocabulary. The design rationale, convergence evidence, and anticipated objections live in the companion *Combinators: Design Rationale*<sup>[7]</sup>. The task type and IoAwaitable protocol these combinators build on live in D0003R0<sup>[4]</sup> and D0004R0<sup>[5]</sup>.

This paper asks for nothing.

---

## 2. What This Paper Asks

The committee is asked to advance the following vocabulary for the standard library:

```cpp
namespace std::io {

  template<IoAwaitable... Awaitables>
  /* see Section 3 */ when_all(Awaitables&&... awaitables);

  template<IoAwaitable... Awaitables>
  /* see Section 4 */ when_any(Awaitables&&... awaitables);

}
```

Two function templates. One awaits all children. One awaits any child and cancels the rest.

After Papers 1-7, a user can write a complete concurrent networking application against the standard:

```cpp
namespace io = std::io;

io::task<> run_server(io::any_stream& control)
{
    io::tcp_acceptor acceptor(/* ... */);
    io::signal_set signals(/* ... */);

    // Graceful shutdown: accept loop + signal handler.
    co_await io::when_any(
        accept_loop(acceptor),
        signals.wait());
}
```

---

## 3. `when_all`

`when_all` takes a variadic pack of awaitables, launches all of them concurrently, and suspends the caller until every child has completed. The result is a `std::tuple` of each child's result type.

### 3.1 Synopsis

```cpp
template<IoAwaitable... Awaitables>
auto when_all(Awaitables&&... awaitables)
    -> /* IoAwaitable yielding
          std::tuple<result_of_t<Awaitables>...> */;
```

### 3.2 Semantics

**Launch.** Each awaitable is started concurrently on the caller's executor. The order of initiation is unspecified. All children inherit the caller's `io_env` - executor, stop token, and frame allocator - through the IoAwaitable protocol.

**Completion.** The caller resumes when every child has completed. The results are returned as a `std::tuple` in the same positional order as the argument pack.

**Cancellation.** If the caller's stop token is triggered, all children receive the stop request through their inherited stop tokens. `when_all` does not complete until every child has acknowledged the cancellation and exited.

### 3.3 Example

```cpp
io::task<> handle_client(io::any_stream& stream)
{
    // Fetch two resources concurrently.
    auto [resp1, resp2] = co_await io::when_all(
        fetch(stream, "/api/users"),
        fetch(stream, "/api/orders"));

    auto merged = merge(resp1, resp2);
    co_await send_response(stream, merged);
}
```

---

## 4. `when_any`

`when_any` takes a variadic pack of awaitables, launches all of them concurrently, and suspends the caller until the first child completes. The remaining children are cancelled.

### 4.1 Synopsis

```cpp
template<IoAwaitable... Awaitables>
auto when_any(Awaitables&&... awaitables)
    -> /* IoAwaitable yielding
          first completed result */;
```

### 4.2 Semantics

**Launch.** Each awaitable is started concurrently on the caller's executor. All children inherit the caller's `io_env`.

**Completion.** The caller resumes when the first child completes. The result of that child is the result of the `when_any` expression.

**Cancellation of siblings.** When the first child completes, `when_any` triggers the stop token of every remaining child. `when_any` does not complete until every remaining child has acknowledged the cancellation and exited. This is the structured guarantee: No child outlives the `when_any` scope.

**Stop token propagation.** Each child receives a stop token that is triggered in two cases: (a) a sibling completed first, or (b) the caller's own stop token was triggered. The child's stop token is a composite of both sources.

### 4.3 Example

```cpp
io::task<> run_server(
    io::tcp_acceptor& acceptor,
    io::signal_set& signals)
{
    // Run until signal received.
    co_await io::when_any(
        accept_loop(acceptor, handle_client),
        signals.wait());

    // Both children have exited.
    // Acceptor loop was cancelled by the signal.
}
```

---

## 5. Cancellation Semantics

Structured concurrency requires that no child outlives its parent scope. Both combinators enforce this.

### 5.1 `when_any` Cancellation

When the first child completes:

1. `when_any` triggers the stop token of every remaining child.
2. Each remaining child observes the stop request through `std::stop_token::stop_requested()` or through a stop callback registered on its inherited stop token.
3. Each remaining child exits cooperatively - the combinator does not force-destroy frames.
4. `when_any` completes only after all children have exited.

The mechanism is cooperative. A child that ignores its stop token delays the `when_any` completion. This is by design - forceful cancellation would violate RAII guarantees inside child coroutines.

### 5.2 External Cancellation

If the caller's stop token is triggered while a combinator is running:

- **`when_all`**: Every child receives the stop request. `when_all` waits for all children to exit.
- **`when_any`**: Every child receives the stop request. `when_any` waits for all children to exit. The result is the first child that completed (which may be due to cancellation).

In both cases, the combinator does not complete until all children have exited.

### 5.3 Stop Token Composition

Each child's effective stop token is a composite of:

1. The caller's stop token (external cancellation).
2. A combinator-internal stop source (sibling cancellation, `when_any` only).

The composition uses `std::stop_callback` to forward a stop request from either source to the child. This matches the pattern in `std::jthread` and in `std::execution`'s stop token forwarding.

---

## 6. Error Handling

### 6.1 Errors in `when_all`

If one child fails (throws or returns an error), the remaining children are cancelled via their stop tokens. `when_all` waits for all children to exit and then propagates the first error. If multiple children fail, `when_all` propagates the first error that was observed; subsequent errors are discarded after the children exit.

The alternative - collecting all errors - was considered and deferred. A multi-error type adds vocabulary that may not justify itself for the common case. The companion paper *Combinators: Design Rationale*<sup>[7]</sup> Section 3 records the tradeoff.

### 6.2 Errors in `when_any`

If the first child to complete does so with an error, `when_any` cancels the remaining children and propagates that error. The combinator does not try a second child - it reports the first completion, whether that completion is a value or an error.

The alternative - `first_success`, which skips errors and tries the next child - is a different combinator. It is deferred (see *Combinators: Design Rationale*<sup>[7]</sup> Section 7).

---

## Suggested Straw Poll

> LEWG agrees that the structured concurrency combinators `when_all` and `when_any` documented in this paper and its companion *Combinators: Design Rationale* should be advanced as standard library vocabulary for coroutine-native I/O.

---

## Acknowledgments

Christopher Kohlhoff's `asio::experimental::parallel_group` and earlier `when_all` prototypes explored this design space in Asio. Lewis Baker's `cppcoro::when_all` demonstrated the pattern for C++20 coroutines. The structured concurrency model draws on work by Martin S&uuml;strik (libdill), Nathaniel J. Smith (Trio), and Roman Elizarov (Kotlin coroutines).

The authors of `std::execution` - Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators - provided the stop token composition model that these combinators inherit.

---

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine-native I/O abstractions for C++20 (Vinnie Falco, 2023-2026).

[2] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O on epoll, kqueue, and IOCP (Vinnie Falco, 2024-2026).

[3] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] D0003R0 - "Coroutine Task" (Vinnie Falco, 2026). Companion ask paper for `task<T>` and launch functions.

[5] D0004R0 - "Coroutine Task: Design Rationale" (Vinnie Falco, 2026). Companion design paper for the task type.

[6] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[7] *Combinators: Design Rationale* (Vinnie Falco, 2026). Companion design paper. D0014R0.
