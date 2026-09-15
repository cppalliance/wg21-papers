---
title: "Awaitables Are Synchronous Too"
document: P4255R0
date: 2026-09-15
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

A coroutine that awaits a synchronously-completing sender through the working draft's generic bridge suspends for a result that is already in memory, and the wording fixes that behavior.

P2300R10 calls the extra allocations and indirections of coroutine frames "a deal-breaker" for generic async algorithms on hot code paths, and the same document specifies the bridge between senders and coroutines. The bridge's generic fallback connects the sender and wires the receiver in its constructor, before the language evaluates `await_ready`. It answers `await_ready` with `false` for every object and starts the operation from `await_suspend`, so a sender that completes inside `start` resumes the coroutine it just suspended, even though the sender model permits synchronous completion and the coroutine language has had a hook for it since C++20. Four proposals across six years described a completion-behavior query without producing wording, and the two public implementations that track the working draft reduce state and coordination after the false answer. The reference implementation's own issue tracker records the cost: a stack-overflow regression test over a million ready completions, a same-thread deadlock, and a use-after-free, each traced to completing inline from inside the suspension path, which the awaiter protocol handles through the return value of `await_suspend` and the bridge does not use. The comparison counts the protocol steps the wording names, and no benchmark result is used. The repair is a readiness query consulted before suspension, a connection deferred past the answer, and a second value-delivery path beside the completion channels - the awaiter protocol's `await_ready`, `await_suspend`, and `await_resume`.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. Introduction

The working draft's `inline_scheduler` completes every operation inside `start`. A coroutine that awaits its sender through the generic bridge suspends before receiving the result.<sup>[1]</sup><sup>[2]</sup>

P2300R10 proposes `std::execution` as the basis for standard asynchrony, and it reaches that position by weighing the alternatives. Section 1.9.2, "Coroutines", delivers its verdict: coroutines are "a poor choice for a basis of all standard async."<sup>[1]</sup> The same document specifies the bridge between the two models, and N5054 contains its wording.<sup>[1]</sup><sup>[2]</sup> On the sender side, connecting a sender to a receiver produces an operation state, and `start` launches the operation. `execution::task` joins the models by translating an awaited sender into an awaiter through `as_awaitable` ([exec.as.awaitable]).<sup>[2]</sup><sup>[3]</sup> The generic fallback on that path, the exposition-only `sender-awaitable`, declares `static constexpr bool await_ready() noexcept { return false; }`, and so does the `suspend-complete` awaiter in the adapter for the other direction.<sup>[1]</sup><sup>[2]</sup>

P2300R10 section 1.9.2 calls coroutine-frame "allocations and indirections" a deal-breaker for generic async algorithms on hot code paths.<sup>[1]</sup> The bridge the same document specifies adds five protocol steps to every iteration of every composed loop above a ready sender, and the criterion that decided 1.9.2 was not applied to it (Sections 6 and 7).

The related work spans completion timing, task integration, and control transfer. P2257R0 and P3206R0 examine completion guarantees and a completion-behavior query.<sup>[4]</sup><sup>[5]</sup> P3570R2 supplied the composition case that led to the forwarding await-completion adaptor now in the working draft.<sup>[6]</sup> P3552R3, P3796R1, and P3941R4 develop task integration, task issues, and scheduler affinity.<sup>[3]</sup><sup>[7]</sup><sup>[8]</sup> P0443R14 defined executor properties, including a blocking guarantee; P2300R10 left properties out.<sup>[9]</sup><sup>[1]</sup> P3801R0 and P2583R4 examine the recursive behavior of inline sender completions resuming task coroutines.<sup>[10]</sup><sup>[11]</sup> P4003R3 defines the IoAwaitable protocol used here, while P4092R1, P4093R1, and P4126R1 examine both bridge directions and their continuation requirements.<sup>[12]</sup><sup>[13]</sup><sup>[14]</sup><sup>[15]</sup>

Four contributions follow:

1. A demonstration that one coroutine body serves synchronous and asynchronous streams, and a vocabulary separating synchronous completion, inline completion, per-instance pre-start readiness, and a coroutine fast path (Sections 2 and 4).
2. The I/O fixture that separates a result known before initiation from completion discovered during initiation, and a normative trace of the path a synchronously-completing sender takes through the generic bridge (Sections 5 and 6).
3. The proposal record for completion-behavior queries and the implementation record in both public implementations of the working-draft bridge, quoted from pinned commits and public issue trackers (Sections 8 and 9).
4. The mechanisms a repair requires, a survey of the alternatives, and falsification criteria (Sections 6.1, 10, and 13).

The assumptions bound what the traces claim. The sender trace follows N5054<sup>[2]</sup> and P3552R3,<sup>[3]</sup> with the task's environment naming `inline_scheduler` under both spellings of that knob (`scheduler_type` in P3552R3, `start_scheduler_type` in the working draft) so that no affinity work is counted. The unit of comparison is the protocol step the wording names. No heap-allocation elision is assumed on either side. No benchmark result is used as evidence, and phase counts are not a performance model. Source claims use immutable stdexec, Beman.Execution, and libunifex commits.<sup>[16]</sup><sup>[17]</sup><sup>[18]</sup>

The scope is coroutine-centric I/O: operations whose primary consumer is a coroutine body and whose higher-level buffering can make a result available before initiation. Sender-native pipelines, direct receiver consumers, and system calls whose completion becomes known only during initiation remain in the comparison but are not covered by the central conclusion.

The author maintains awaitable-native libraries and has a professional interest in the result (Disclosure).

## 2. One Coroutine Serves Both Streams

Two concrete stream types and one generic algorithm establish what the coroutine language gives an I/O library before any sender machinery enters: one coroutine body that runs synchronously or asynchronously depending on which stream it awaits. Sections 3 through 6 measure the sender bridge against this baseline.

A synchronous write stream has one operation: accept a string and store it. It offers no error codes, byte counts, or partial writes. The abstraction is intentionally minimal: a test fixture that isolates the protocol's behavior from the I/O operation's complexity. Two concrete types implement it.

`string_sink` appends to a `std::string`. The operation is synchronous, the data is already in memory, and no kernel transition occurs.

```cpp
class string_sink
{
    std::string& out_;

public:
    explicit string_sink(std::string& s)
        : out_(s) {}

    auto write(std::string_view sv)
    {
        out_.append(sv.data(), sv.size());
        // returns an awaitable or sender
    }
};
```

`tcp_sink` writes to a TCP (Transmission Control Protocol) socket. The operation is asynchronous. The kernel accepts the data, the coroutine suspends, and the reactor resumes it when the write completes.

Both expose the same `write(std::string_view)` signature. The return type differs, but the algorithm that calls `co_await sink.write(...)` does not.

```cpp
template<class Sink>
task<> log_lines(Sink& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

Compiled against `tcp_sink`, `log_lines` awaits an awaitable whose `await_ready()` returns `false`; the coroutine suspends, and the reactor resumes it when the write completes. Compiled against `string_sink`, the same template awaits an awaitable whose `await_ready()` returns `true`; the coroutine never suspends. The source is identical, the awaitable type varies, and the compiler selects the execution model. A type-erased stream achieves the same selection at link time: the erased awaitable constructs the concrete awaitable inside its own `await_ready()` and forwards the answer, so a ready stream completes without suspending through a fixed table of function pointers.<sup>[19]</sup>

Streams a program talks to every day complete synchronously by nature: stdin and stdout on a terminal, a regular file on a local filesystem, an in-memory string, and the loopback harness behind a test suite all deliver results without a kernel wait, and a buffered socket delivers them from user space whenever its buffer holds enough bytes.

Readiness is a property of the awaiter instance, decided at the `co_await`, and the same coroutine body serves both streams.

## 3. Senders Provide Five Properties Awaitables Do Not

Before the costs come the properties: `std::execution` provides five things no awaitable provides, and each one does work in the sections that follow.

1. **Static composition.** Adaptors such as `then`, `let_value`, and `when_all` form typed work graphs whose connected operation state owns the state of its children. P2300R10 section 1.9.2 states the constraint it weighs against coroutines: "In a suite of generic async algorithms that are expected to be callable from hot code paths, the extra allocations and indirections are a deal-breaker."<sup>[1]</sup>

2. **Three completion channels.** A receiver accepts a value, an error, or a stopped completion, and a sender's completion signatures describe those possibilities in an environment. A generic algorithm acts on the distinction without inspecting a value whose domain it does not know.

3. **Operation ownership.** Connecting a sender and a receiver produces an operation state, and `start` begins the operation.<sup>[2]</sup> The operation state gives the operation stable storage for its whole lifetime, and destroying it while the operation is live is undefined behavior.

4. **Environments.** An environment provides the schedulers, allocators, stop tokens, and domain information that transform or execute the operation.

5. **Structured concurrency.** The counting-scope facilities track associated work and require the scope to reach an allowed state before destruction; premature destruction invokes `terminate`.<sup>[2]</sup><sup>[20]</sup>

The sender model also permits synchronous completion itself. P2300R10's model text states ([async.ops]): "An asynchronous operation can in fact execute synchronously; that is, it can complete during the execution of its start operation on the thread of execution that started it."<sup>[1]</sup> Its `inline_scheduler` is (section 1.6.1) "a trivial scheduler that completes immediately and synchronously on the thread that calls `std::execution::start` on the operation state produced by its sender."<sup>[1]</sup> Its `just`, `just_error`, and `just_stopped` factories produce senders "whose asynchronous operations complete synchronously in their start operation" ([exec.just]).<sup>[1]</sup> Its motivating Windows socket example (section 1.4) has a branch commented `// Completed synchronously (assuming FILE_SKIP_COMPLETION_PORT_ON_SUCCESS has been set)`, which calls `set_value` from inside `start` when `WSARecv` reports immediate completion.<sup>[1]</sup><sup>[21]</sup>

A sender may finish inside `start`, and P2300R10 says so in its model text, its factories, and its examples.

## 4. Completion Has Four Properties; P2300R10 Names Two

"Completed synchronously" can mean four different things at a coroutine boundary, and which thing it means decides what the coroutine can skip. This section names the four properties and the two protocol objects the remaining sections use.

| Term | Meaning in this paper |
| --- | --- |
| **Synchronous completion** | The operation delivers its completion before `start()` returns. |
| **Inline completion** | The operation delivers its completion before `start()` returns, on the execution agent that called `start()`. |
| **Per-instance pre-start readiness** | This operation object already holds its result before initiation, although another object of the same type may not. |
| **Coroutine fast path** | The coroutine obtains the result without being considered suspended by [expr.await].<sup>[2]</sup> |
| **Awaiter** | The object on which the language evaluates `await_ready`, `await_suspend`, and `await_resume`. |
| **Operation state** | The object produced by connecting a sender and receiver and passed to `start`. |

Table 1. The four completion properties and the two protocol objects used throughout the paper. The definitions separate completion discovered during initiation (the first two rows) from a result known before initiation (the third row).

The working draft defines synchronous completion through timing relative to `start`.<sup>[2]</sup> Different instances of one sender type may complete during `start` or after it returns, and the definition gives a coroutine no way to ask which instance it holds.

The coroutine language asks a different question. After promise transformation and awaiter selection, [expr.await] evaluates `await_ready()` before deciding whether the coroutine is considered suspended.<sup>[2]</sup> A `true` result proceeds to `await_resume`; a `false` result enters the suspension path and evaluates `await_suspend`. The answer is a property of the awaiter object, so two objects of the same type can answer differently.

Completion behavior and pre-start readiness can correlate without being equivalent: a sender may guarantee inline completion because its `start` performs the work immediately, even though no result exists beforehand. P2300R10 specifies synchronous and inline completion, and it names neither per-instance readiness nor a coroutine fast path.<sup>[1]</sup>

## 5. Buffered I/O Holds Its Result Before Initiation

Three I/O shapes separate a result known before suspension from completion discovered during initiation. Keeping them separate prevents an eager fixture from standing in for every synchronous I/O operation and locates the one case where the two protocols differ. An operation that performs its work before returning its operation object, such as an in-memory append, is the narrowest case; it isolates consumption of an already-produced result and nothing more.

Overlapped `WSARecv` supplies the mixed-completion case. Microsoft specifies that return zero means the operation completed immediately, while `SOCKET_ERROR` with `WSA_IO_PENDING` means successful initiation followed by later completion.<sup>[21]</sup> P2300R10's `recv_sender` handles both outcomes in the `start` of one operation state, with the immediate branch assuming `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`.<sup>[1]</sup><sup>[22]</sup> An awaiter handles the same distinction from `await_suspend`: initiate, store an immediate result, and return `false` or transfer directly to the continuation. The operation result does not exist before initiation in either model, so true pre-start readiness is unavailable, and socket readiness does not change that: Microsoft warns that a readiness event can be followed by a receive returning `WSAEWOULDBLOCK`.<sup>[23]</sup>

A buffered stream supplies the pre-start case. One `read_some` object may find enough bytes in a user-space buffer, while another object of the same type must initiate an asynchronous receive. The cache-hit result can be copied and counted before suspension is considered. The following illustrative projections share one operation implementation:

```cpp
struct buffered_read_awaiter {
    bool await_ready() {
        return stream.try_read(buffer, result);
    }

    bool await_suspend(std::coroutine_handle<> h) {
        return stream.start_read(buffer, result, h);
    }

    std::size_t await_resume() {
        return result;
    }
};

struct buffered_read_sender {
    template<class Receiver>
    operation_state<Receiver> connect(Receiver);
    // operation_state::start first checks the same user-space buffer,
    // then calls set_value or starts the pending receive.
};
```

This is illustrative code rather than wording or a production implementation. It assumes the stream controls access to its user-space buffer so the readiness decision remains valid through extraction.

Both projections support ready and pending instances. The awaiter exposes the decision to [expr.await]; its cache-hit object proceeds directly to `await_resume`. The sender exposes the decision through the timing of receiver completion after `start`. When that sender reaches the generic bridge of Section 6, `await_ready` remains `false` for both objects.

The decision recurs because composed I/O is a loop. `read` fills a buffer by looping `read_some`; TLS (Transport Layer Security) decrypts by looping encrypted reads; HTTP (Hypertext Transfer Protocol) sequences header parsing with body reads. Each layer is a coroutine composing awaitables, and each layer's loop asks the readiness question once per iteration. A 64 KB read from a stream that hands back 4 KB per `read_some` asks it sixteen times. The following algorithm is `read` as implemented in Capy<sup>[19]</sup> (`include/boost/capy/read.hpp` at commit `75e1bed`):

```cpp
template <typename S, typename MB>
  requires ReadStream<S> && MutableBufferSequence<MB>
auto
read(S& stream, MB buffers) ->
        io_task<std::size_t>
{
    consuming_buffers consuming(buffers);
    std::size_t const total_size = buffer_size(buffers);
    std::size_t total_read = 0;

    while(total_read < total_size)
    {
        auto [ec, n] = co_await stream.read_some(consuming.data());
        consuming.consume(n);
        total_read += n;
        // A contingency that still completed the transfer is a success:
        // report it only when the buffer was not filled.
        if(ec && total_read < total_size)
            co_return {ec, total_read};
    }

    co_return {std::error_code(), total_read};
}
```

When the stream reports ready, no iteration leaves the coroutine's call chain: `await_ready()` returns `true`, no scheduler is consulted, and the generic algorithm adds no protocol machinery to the copy. The relationship mirrors [random.access.iterators]: a `T*` satisfies `random_access_iterator` and dereferences in one instruction, even though a disk-backed iterator requires state, callbacks, and a two-phase access protocol internally.<sup>[2]</sup> The concept imposes only what the underlying access requires. `await_ready() == true` is the pointer dereference: the value is there, take it.

A shipped library covers the ready path with a policy. Corosio caps consecutive inline completions at an adaptive budget of 2 to 16, or 4 when no other thread absorbed queued work, and posts the next completion through the queue when the budget runs out (`native/detail/reactor/reactor_scheduler.hpp` at commit `039fe65`).<sup>[24]</sup> The budget exists because unbounded inline completion starves other coroutines on the same executor; the readiness question and the fairness policy are separate decisions.

The per-instance decision recurs at every iteration of a composed loop, and only the buffered fixture presents it.

## 6. The Bridge Connects Before It Asks

P2300R10 specifies how a coroutine consumes a sender, and N5054 has the same wording.<sup>[1]</sup><sup>[2]</sup> Three parts of that mechanism matter here: the routes from an expression to an awaiter, the fallback awaiter P2300R10 wrote, and the path a synchronous sender takes through it.

Inside `execution::task`, `await_transform` first handles scheduler affinity. If the task's `start_scheduler_type` is `inline_scheduler`, it passes the sender directly to `as_awaitable`; otherwise it applies `affine` first.<sup>[2]</sup><sup>[3]</sup> Affinity is therefore a separate concern from readiness.

`as_awaitable(expr, promise)` then selects among five ordered results ([exec.as.awaitable] p7):<sup>[2]</sup>

1. The expression's own `as_awaitable` member.
2. An `as_awaitable` member on the transformed and await-completion-adapted sender.
3. The original expression when it is already an awaiter.
4. The exposition-only `sender-awaitable` for a compatible single-value sender.
5. The original expression otherwise.

The first three routes can avoid the generic bridge. The fourth route constructs the exposition-only `sender-awaitable`. Its relevant shape is:<sup>[2]</sup>

```cpp
variant<monostate, result-type, exception_ptr> result{};

connect_result_t<Sndr, awaitable-receiver> state;

sender-awaitable(Sndr&& sndr, Promise& p);
static constexpr bool await_ready() noexcept { return false; }
void await_suspend(coroutine_handle<Promise>) noexcept { start(state); }
value-type await_resume();
```

This is working-draft exposition from [exec.as.awaitable]. The constructor initializes `state` with `connect`, so connection precedes the language's readiness question. `await_ready()` then returns `false` for every object. `await_suspend()` starts the operation.

Completion reaches an `awaitable-receiver`. Value or error completion emplaces a result or exception in the stored variant, then evaluates `continuation.resume()`; stopped completion resumes the handle selected by the promise's `unhandled_stopped` operation.<sup>[2]</sup> `await_resume()` rethrows the stored exception or extracts the stored value.

P2300R10 wrote the same constant into the adapter for the other direction. `connect` on an awaitable runs an exposition-only coroutine, `connect-awaitable`, which delivers the completion through a local awaiter named `suspend-complete`:<sup>[1]</sup>

```cpp
static constexpr bool await_ready() noexcept { return false; }
void await_suspend(coroutine_handle<>) noexcept { fn(); }
[[noreturn]] void await_resume() noexcept { unreachable(); }
```

The awaiter protocol has exactly one hook for "the result is already here", and P2300R10's two coroutine adapters both hardwire it to `false`.

A coroutine awaiting the standard's own inline sender takes the following path through that wording. The task's environment names `inline_scheduler` as its scheduler, so `await_transform` skips the `affine` wrapper ([task.promise] p6)<sup>[2]</sup> and passes the sender to `as_awaitable` directly:

```cpp
struct inline_env
{
    // P3552R3 names the knob scheduler_type; the working draft names it
    // start_scheduler_type. Declaring both satisfies either text.
    using scheduler_type       = execution::inline_scheduler;
    using start_scheduler_type = execution::inline_scheduler;
};

execution::task<void, inline_env> log_lines(
    string_sink& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

This task configuration is illustrative; `write` returns `inline_scheduler{}.schedule()`, the sender the working draft specifies for inline completion ([exec.inline.scheduler]).<sup>[2]</sup> The working draft then describes, in order:

1. **Transform.** `await_transform` receives the sender; the affinity check passes, so the sender reaches `as_awaitable` unwrapped, and a `sender-awaitable` is constructed ([exec.as.awaitable] p7).<sup>[2]</sup>
2. **Connect.** The `sender-awaitable` constructor calls `connect(sndr, awaitable-receiver)`. The operation state is materialized, and the receiver is wired.<sup>[2]</sup>
3. **Readiness.** `await_ready()` returns `false` unconditionally.<sup>[2]</sup>
4. **Suspend.** The coroutine suspends.
5. **Launch.** `await_suspend` calls `start(state)`. Inside `start`, `set_value(receiver)` fires synchronously.<sup>[2]</sup>
6. **Complete.** The receiver stores the result in the variant and calls `continuation.resume()`, nested inside `await_suspend`. The coroutine resumes.<sup>[2]</sup>
7. **Extract.** `await_resume()` reads the value from the variant.<sup>[2]</sup>

All seven phases have work. For an operation that completes synchronously, the path incurs one suspension and one resumption, one operation state construction, one receiver instantiation, and one variant emplacement; only the scheduler affinity wrapping is avoided. These are steps the wording names, counted so a reader can recount them; their runtime cost is a separate question, and no measurement appears here.

The generic fallback connects before readiness, reports false readiness, starts from `await_suspend`, and completes through its receiver. Those four statements describe the fourth of the five routes, and only that route.

### 6.1. The Repair Is a Query and a Second Path

Closing the gap takes four mechanisms.

A readiness query saves the suspension. If `sender-awaitable::await_ready()` returned `true` for a sender that advertises synchronous completion, the coroutine would not suspend. But the constructor already ran, and it materialized the operation state, wired the receiver, and constructed the variant. The query saves the suspension and saves nothing else.

Deferred connection saves the construction. Moving `connect` from the constructor into `await_suspend` lets a `true` answer from `await_ready()` bypass the connection. A `true` answer then needs a result for `await_resume`, and three designs supply one. The first is static: a completion-behavior attribute marks the sender inline-always and never stopped, `await_ready` connects and starts, the value arrives through the receiver, and the answer is `true`. This is stdexec's specialized awaiter with its answer moved from `await_suspend` to `await_ready` (Section 9.1). The second is dynamic: `await_ready` connects and starts any sender and reports whether it completed. The operation may complete before `await_suspend` runs, and resuming a coroutine that is not yet suspended is undefined, so this design keeps the atomic handshake. The third is direct extraction: the awaiter reads a held result without a receiver. Of the three, it alone reaches a per-instance answer without a type-level attribute and without an atomic on every iteration of the loops in Section 5.

A stopped completion constrains the answer. `await_resume` returns a value or throws; it cannot express the stopped channel, which the working draft routes through the promise's `unhandled_stopped` and a replacement continuation - a selection only `await_suspend`'s returned handle can perform.<sup>[2]</sup> The query therefore answers per result: a held value or error answers `true`, and a held stopped completion answers `false` and takes the suspension path, where `unhandled_stopped` redirects the continuation. Both implementations of Section 9 perform that redirection from `await_suspend` today.

The model then has two value-delivery mechanisms: channels for asynchronous completion, direct extraction for synchronous completion. The awaiter protocol already has both. `await_ready` asks, and `await_resume` extracts.

Completion discovered during initiation (Table 1, second row) takes one more: when `start` completes inside `await_suspend`, the awaiter returns `false` or the continuation rather than resuming a coroutine that has not finished suspending, as stdexec's specialized awaiter does (Section 9.1).

Four mechanisms close the gap: ask before suspending, connect only when the answer is false, return from `await_suspend` instead of nesting a resumption when completion arrives during initiation, and deliver a held value without a receiver. An awaiter has done all four since C++20.

## 7. Section 1.9.2's Criterion, Applied to the Bridge

P2300R10 section 1.9.2 asked whether the generic async algorithms should be coroutines, and answered on hot-path cost: "In a suite of generic async algorithms that are expected to be callable from hot code paths, the extra allocations and indirections are a deal-breaker. It is for these reasons that we consider coroutines a poor choice for a basis of all standard async."<sup>[1]</sup> The reasons named are the frame's: dynamic allocation, indirect calls, separate compilation, and the limits of heap-allocation elision. That answer stands.

The bridge is a different question, on the consumer side, and 1.9.2 did not address it. Applied there, the same criterion counts the five steps of Section 6 on every iteration of every composed loop above a ready sender: a suspension, a nested resumption, a connection, a receiver instantiation, and a result-variant emplacement. None can be skipped, because the readiness answer is fixed at `false`. Whether a step is an allocation or an indirection in a given implementation is a separate question, and no measurement appears here.

## 8. Six Years of Queries, Zero Wording

A consumer-side readiness property has a history on both sides of P2300R10, and the history is uniform: every proposal describes the query, and none produces wording.

| Proposal | Year | Content | Wording |
| --- | --- | --- | --- |
| P0443R14<sup>[9]</sup> | 2020 | A `blocking` property on executors; `blocking.always` requires that an execution function "shall block until completion of all invocations of submitted function object" | Dropped by P2300R10 |
| P2257R0<sup>[4]</sup> | 2020 | Completion guarantees: "we think senders should first and foremost be described by their completion guarantees" | None; never revised |
| P3206R0<sup>[5]</sup> | 2025 | A completion-behaviour query with combination rules for the standard adaptors | "There is no wording in this paper yet." |
| P3669R4<sup>[25]</sup> | 2026 | A non-blocking query for `std::execution` | Not adopted |

Table 2. Four proposals across six years address completion behavior at the consumer boundary. None produced wording, and the working draft contains no completion-behavior facility. (Method: open-std.org paper index, searched 2026-09-15 for blocking, completion-guarantee, or completion-behavior queries.)

P2300R10 states the omission directly: "Properties are not included in this paper. We see them as a possible future extension, if the committee gets more comfortable with them."<sup>[1]</sup> P3206R0 states the consequence from the query author's side: "Awaitables have a very similar way to convey this information by returning true or false for await_ready(). Without this proposal senders in std::execution are missing a tool to do so."<sup>[5]</sup> The same paper observes of the bridge: "The current specification of as_awaitable transforms senders into awaitable that can not use symmetric transfer, even if it would be feasible, because the necessary information is not available."<sup>[5]</sup> P3206R0 remains the only revision, twenty months after publication.

The reference implementation has the query. Stdexec added a `get_completion_behavior` query in October 2025, described by its author as "like in P3206", and uses it to select a specialized awaiter (Section 9).<sup>[26]</sup> The working draft has none. (Method: the N5054 LaTeX source at cplusplus/draft tag `n5054`, searched 2026-09-15 for `completion_behavior`, `completion behaviour`, and `completes_inline`: zero matches. The three `await_ready` occurrences in [exec] are the `is-awaiter` requirement and the two constant-false awaiters quoted in Section 6.)

## 9. The Implementations Already Know

Two public implementations of the working-draft bridge retain sender connection and receiver completion while changing state lifetime and coroutine transfer; neither changes the answer the wording fixes at `false`. The two are NVIDIA's stdexec, the reference implementation, and Beman.Execution, selected because both track the current working draft. Their source, their commit history, and their issue trackers record what the bridge costs and what it cannot express. libunifex ships a coroutine bridge for an earlier sender design and appears here as prior art.

### 9.1. stdexec Works Around the Answer It Cannot Change

In February 2026, stdexec's maintainer added a specialized awaiter for senders statically known to complete inline. The pull request states the motivation:<sup>[27]</sup>

> awaiting a coroutine such as:
> ```c++
>   auto burn_cycles() -> ex::task<int>
>   {
>     int result = 42;
>     for (int i = 0; i < 1'000'000; ++i)
>     {
>       result += co_await ex::just(42);
>     }
>     co_return result;
>   }
> ```
> will no longer cause a stack overflow. for this optimization to kick in, the sender being `co_await`-ed must be known statically to complete inline always, but never complete with `set_stopped`.

The specialized awaiter connects and starts inside `await_suspend` and returns the continuation, removing the generic path's atomic handshake. Its source comments describe the maneuver (`include/stdexec/__detail/__as_awaitable.hpp` at commit `2c56ffe7`, lines 363-364 and 385-387):<sup>[16]</sup>

```cpp
// When the sender is known to complete inline, we can connect and start the operation
// in await_suspend.
```

```cpp
// The following call to start will complete synchronously, writing its result
// into the __result_ variant.
STDEXEC::start(__opstate);
```

The same file's base awaiter, shared by the generic and specialized paths, answers the readiness question (lines 118-123):<sup>[16]</sup>

```cpp
static constexpr auto await_ready() noexcept -> bool
{
  return false;
}
```

The optimization removes everything except the suspension. The coroutine still suspends and resumes for a result already in memory, because the answer the wording fixes is `false`.

The generic path's comment block records why the machinery exists (lines 161-162): "When the sender is not statically known to complete inline, we need to use atomic state to guard against too many inline completions causing a stack overflow."<sup>[16]</sup> The hazard has a five-year history. In October 2021, the maintainer opened an issue quoting Lewis Baker on `as_awaitable`:<sup>[28]</sup>

> I am still a little concerned about the potential for unbounded recursion and stack-overflow if someone awaits a sender that completes synchronously in a loop with this formulation.

The recursion Baker describes, and the two failures below, are the first hazard: completion during `start`, reached from inside the suspension path (Table 1, second row). Any protocol that initiates from `await_suspend` and can complete synchronously meets it; awaitable-native code answers with the return value of `await_suspend`, a `bool` or a continuation, and a fairness budget (Section 5). stdexec's specialized awaiter now uses the return value, and libunifex never did (Section 9.3). A result held before initiation is a different gap, and the one the bridge cannot express at all.

The failure modes since are on the public tracker. April 2026: a same-thread deadlock, because the receiver's stopped path never signals the awaiter's atomic flag - "Since nobody ever set it to true, this is a permanent deadlock on the same thread that called `start()`."<sup>[29]</sup> The same month: a use-after-free in which an inline stopped completion "destroys the currently executing task coroutine frame, including the sender awaiter whose `await_suspend()` has not returned yet."<sup>[30]</sup> The test suite includes a regression test that awaits `just(42)` one million times in a loop, named "test task can await a just_int sender without stack overflow" (`test/stdexec/types/test_task.cpp` at commit `2c56ffe7`, lines 671-682).<sup>[16]</sup>

### 9.2. Beman.Execution Has the Same Constant

Beman.Execution's `sender_awaitable` connects in its constructor, coordinates completion with an atomic Boolean, and answers readiness with the same constant (`include/beman/execution/detail/sender_awaitable.hpp` at commit `a20a6f63`, line 110):<sup>[17]</sup>

```cpp
static constexpr bool     await_ready() noexcept { return false; }
```

The repository's history records the same hazard and its remediation: three pull requests between November 2025 and February 2026 implement and refine stack-overflow prevention for inline completions, and `examples/stackoverflow.cpp` exercises up to thirty thousand iterations of `co_await ex::just(i)` through the bridge.<sup>[31]</sup> The working draft's own adaptation hook is present but inert: the repository's implementation-status page marks [exec.as.awaitable] p1's `has-queryable-await-completion-adaptor` with a warning icon and the note "this name appears to be is unused", and no sender in the library provides the query.<sup>[17]</sup> No file in the snapshot at commit `a20a6f63` names `completion_behavior` or `completes_inline`.

### 9.3. libunifex Shows the Flaw Is Inherited

Libunifex ships the coroutine bridge for the sender design that preceded P2300. Its sender awaiter has the same constant (`include/unifex/await_transform.hpp` at commit `effb7527`, line 176):<sup>[18]</sup>

```cpp
bool await_ready() const noexcept { return false; }
```

Its receiver's `complete()` calls `continuation_.resume()` directly, so repeated synchronous completions grow the stack with no symmetric transfer at all (lines 95-104).<sup>[18]</sup> The same library's task-to-task awaiter uses handle-returning `await_suspend`. The technique existed in the same codebase and was never applied to the sender bridge.

### 9.4. The Standard Specifies a Bridge Its Own Ecosystem Routes Around

The working draft leaves it unspecified whether a standard-library sender provides a member `as_awaitable` ([exec.snd.expos]/2), and portable code has no way to require that member.<sup>[2]</sup> The reference implementation selects a specialized awaiter for its own statically-inline senders and leaves the generic fallback - and its atomic handshake - for everything else. A user-defined sender with the same completion behavior receives the fallback, because the query that selects the fast path exists only inside the implementation (Section 8).

Source structure is not a performance measurement: the source answers where connection and start occur, which state is stored, and which abstract-machine atomics are present, and it says nothing about instruction counts or latency. What the record shows is where the engineering effort goes. Both implementations reduce state and coordination after a false readiness result, both implementations include regression tests and fixes for the hazards of completing inline from the suspension path, and neither adds a readiness result.

## 10. Every Alternative Bypasses the Bridge; None Changes It

The generic fallback is not the only coroutine path available to a sender. Current wording and published proposals provide five ways to select a different awaiter or describe completion behavior, and each operates outside the bridge.

A member `as_awaitable` on the sender returns its own awaiter, which can answer readiness per instance ([exec.as.awaitable] p7).<sup>[2]</sup> The sender then exposes two projections - `connect` for sender consumers, the awaiter for coroutine consumers - and the two must agree on values, errors, stopped behavior, cancellation, environment, affinity, lifetime, and concurrency.

The forwarding `get_await_completion_adaptor` query, added in response to P3570R2's composition case, lets an adaptor supply a common coroutine representation through ordinary unary adaptors.<sup>[6]</sup><sup>[2]</sup> Standard unary parents forward forwarding attributes by default; multi-child parents have empty attributes, because one child's await policy does not describe the combined operation; behavior-changing adaptors need their own policy.

A domain's `transform_sender` receives the complete sender expression and can supply a coroutine representation for a recognized family of expressions, centralizing the translation without removing it.<sup>[2]</sup>

A completion-behavior attribute in the style of P3206R0 describes when receiver completion occurs relative to `start`, with combination rules and a dynamic answer for `split`.<sup>[5]</sup> The attribute alone produces no result; a pre-start fast path still needs an awaiter that initiates or extracts before [expr.await] proceeds.

A type that is already an awaiter qualifies as a sender and needs no bridge at all.<sup>[2]</sup>

Erasure preserves what it declares. Stdexec parameterizes `any_sender` with a list of erased queries, and the default list is empty (commit `2c56ffe7`); a fixed I/O eraser can declare an outer `as_awaitable` or forward `await_ready` through its function table, as Capy's erased streams do.<sup>[16]</sup><sup>[19]</sup> An interface containing only sender connection and selected attributes provides no awaiter projection it omits.

Each of the five alternatives operates outside the generic bridge, and the bridge itself is unchanged by any of them.

## 11. The DIS Ballot Runs Through September 2026

C++26 is in its Draft International Standard ballot. The Brno admin telecon minutes record the schedule: a twelve-week ballot period, approximately early July to September 2026.<sup>[32]</sup> The convenor's business plan of July 2026 states that the next edition of ISO/IEC 14882 is in DIS ballot, on schedule to be completed in 2026.<sup>[33]</sup>

At this stage of an ISO ballot, the mechanism by which the draft's wording changes is a national-body comment. National-body comments removed the P2786 trivial relocation facility from C++26 at the Committee Draft stage, and three national bodies voted No on the Committee Draft ballot.<sup>[34]</sup> The Committee Draft comments included sender and receiver comments from five national bodies, dispositioned as customization and renaming fixes; no comment on the public record names [exec.as.awaitable].<sup>[35]</sup> The one recorded poll on the adjacent question asked the Library Evolution Working Group (LEWG) whether the stack-overflow behavior documented in P3801R0 section 3.1 is "an issue with the current design of std::execution::task"; the result was SF 4, F 3, N 5, A 5, SA 1, with 22 attending - no consensus (August 2025).<sup>[36]</sup>

Absent a national-body comment, the bridge wording of Section 6 ships in the C++26 International Standard, and a wording change after publication targets C++29, whose first meeting was Brno in June 2026 and whose schedule is already running.<sup>[37]</sup> Section 8 records the pace at which completion-behavior queries have become wording since 2020.

No national-body comment on record names the bridge.

## 12. Objections

Nine objections remain after the preceding sections, stated in their strongest form and answered from evidence already presented.

### "P2300R10 handles synchronous completion."

On the producer side, it does. `inline_scheduler` completes inside `start`; the `just` factories complete synchronously in their start operations; the WSARecv example calls `set_value` from inside `start` on immediate completion (Section 3). The consumer side is what the bridge specifies, and there the same sender's coroutine consumer suspends (Section 6). Producing a synchronous completion and observing one before suspension are different properties (Section 4). The default is not at issue; the missing override is.

### "Section 1.9.2 weighs allocation, not readiness."

Correctly, for the basis question. Section 7 applies the same criterion to the bridge, a question 1.9.2 did not address.

### "Senders already support synchronous I/O."

The working draft permits completion during `start`, `inline_scheduler` completes that way, and P2300R10's `recv_sender` covers immediate and pending `WSARecv` outcomes with one sender type whose operation state resolves the difference in `start`.<sup>[1]</sup><sup>[2]</sup> Those mechanisms expose completion timing through a receiver. They do not give the fourth route a different answer to `await_ready`.

### "The generic bridge can be repaired without changing the sender concept."

Stdexec's specialized awaiter is that repair: it moves connection into `await_suspend`, removes the generic atomic handshake, and returns a continuation, all without changing the sender concept (Section 9.1).<sup>[16]</sup><sup>[27]</sup> Its `await_ready()` still returns `false`, because the wording fixes that answer. An implementation repair addresses state lifetime, coordination, and transfer after false readiness; it does not add a query for whether this sender object already holds a result.

### "P3206R0 can return runtime completion behavior."

P3206R0 gives `split` a dynamic answer after shared completion and proposes combination rules for standard adaptors.<sup>[5]</sup> It remains the only revision, twenty months after publication, and its abstract states there is no wording (Section 8). The query exists in the reference implementation and nowhere in the standard. With connection moved into `await_ready`, the attribute is a complete repair for statically-inline senders; the case it leaves is per-instance readiness (Section 6.1).

### "await_ready cannot answer true, because stopped completions need await_suspend's returned handle."

A stopped completion redirects the continuation through the promise's `unhandled_stopped`, and only `await_suspend` can return the replacement handle; both implementations perform that redirection today (Sections 6.1 and 9).<sup>[2]</sup><sup>[16]</sup> The repair answers readiness per result: a held value or error answers `true`, and a held stopped completion answers `false` and takes the suspension path. The constraint shapes the query; it does not require the answer to be `false` for values.

### "Protocol steps are not runtime overhead, and the optimizer removes them."

The seven phases of Section 6 are steps the wording names, and runtime cost is a separate question. [exec.as.awaitable] specifies `false` for `sender-awaitable`, so a conforming implementation cannot return `true` without the change in Section 6.1.<sup>[2]</sup> One step is observable whether or not the optimizer inlines `connect` and `start`: the nested resumption from inside `await_suspend`, the behavior P2583R4 and P3801R0 document.<sup>[10]</sup><sup>[11]</sup>

### "Operation state construction delivers structured concurrency guarantees."

For asynchronous operations, where the coroutine suspends and work executes concurrently, yes. For a synchronous write where the data is in the string before `co_await` evaluates, there is no concurrent lifetime to manage. The operation state guarantees a property that was never at risk.

### "Synchronous completion is a corner case."

Buffered writes, cached reads, DNS (Domain Name System) cache hits, and in-memory operations all complete synchronously, and Section 5's composed loops ask the readiness question at every iteration. The reference implementation's own regression test awaits a ready sender one million times in a loop, and Beman.Execution's example awaits one in a loop of up to thirty thousand (Section 9).<sup>[16]</sup><sup>[31]</sup> P3801R0 states the hazard of getting the loop wrong: "Having iterative code that is actually recursive is a potential security vulnerability."<sup>[10]</sup>

## 13. Falsification

The claims above would be discharged - that is, explained by causes other than a bridge that connects before it asks - if any of the following were demonstrated:

- A conforming generic bridge that reaches a per-instance readiness decision without a member `as_awaitable`, an await-completion adaptor, or a domain transformation: a fourth-route awaiter whose `await_ready` can answer `true`.

- A channel-only bridge that reaches a per-instance readiness decision without a type-level completion-behavior attribute and without an atomic handshake per await.

- A standard multi-child adaptor policy under which a leaf's readiness survives composition.

- A passage in P2300R10 that applies the hot-path criterion of section 1.9.2 to the consumer bridge.

## 14. Conclusion

When a coroutine awaits a sender through the generic fallback, the fourth of `as_awaitable`'s five routes, the awaiter's constructor connects before the language asks, the readiness answer the wording hardwires is `false`, and the coroutine suspends and resumes for every completion - including completions that happened before the question was asked, once per iteration of every composed loop above them (Section 6). P2300R10 counted coroutine-frame allocations and indirections as a deal-breaker for hot paths when it weighed coroutines as a basis; the same document's bridge gives the coroutine consumer no way to skip its own protocol steps when the result is already present, and the criterion that decided the basis question was not applied to the bridge (Section 7).

The record is uniform in both venues. Four proposals across six years describe a completion-behavior query, and none produced wording; the query lives in the reference implementation and nowhere in the standard (Section 8). The two public implementations that track the working draft optimize everything after the false answer, and their issue trackers record what the answer costs: a regression test that awaits a ready sender a million times, a same-thread deadlock, and a use-after-free on a frame whose `await_suspend` had not returned (Section 9).

Closing the bridge takes the four things the awaiter protocol has had since C++20: a readiness question asked before suspension, an initiation that runs only when the answer is false, a return from `await_suspend` when completion arrives during initiation, and a value delivered without a receiver (Section 6.1). The wording a repair touches is [exec.as.awaitable] and [task.promise], and a change there is a paper against those sections.<sup>[2]</sup> The C++26 DIS ballot runs through September 2026; after publication, a change targets C++29 (Section 11).

The authors of `task`, of domains, and of the networking libraries now choosing a leaf protocol are the ones placed to act on what the wording says.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[19]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[24]</sup>, coroutine-native I/O libraries under the C++ Alliance.

This paper records a finding about the protocol boundary used when coroutine-centric I/O returns sender-valued operations.

Capy and Corosio use awaitable-native I/O. The author advocates the awaitable-native model and has a professional interest in its adoption. The comparison does not measure a complete networking framework, it does not rank sender-native consumers, and it presents no benchmark result. Awaitable leaves also require an adapter when consumed by a sender pipeline.

Coroutine-native I/O expresses no compile-time work graph, a limitation, and not the only one. C++ says in [class.dtor] that "A destructor shall not be a coroutine",<sup>[2]</sup> so asynchronous clean-up needs a library facility instead of RAII (Resource Acquisition Is Initialization).

This paper belongs to the Network Endeavor series. Companion papers include P4003R3 on IoAwaitable,<sup>[12]</sup> P4092R1 and P4093R1 on both bridge directions,<sup>[13]</sup><sup>[14]</sup> P4126R1 on callback handles,<sup>[15]</sup> and P2583R4 on symmetric transfer through sender composition.<sup>[11]</sup>

The method compares public working-draft wording, published WG21 papers, official operating-system documentation, public issue trackers, and source pinned to immutable public repository commits. N5054 wording was verified against the cplusplus/draft repository at the `n5054` tag, the source from which the N5054 PDF is built. No benchmark result is used.

The paper was drafted and revised with machine assistance under the author's direction.

This paper asks for nothing.

## Acknowledgments

Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, and Bryce Adelstein Lelbach specified the sender model and published the Windows receive example used to distinguish completion during initiation.<sup>[1]</sup> Dietmar K&uuml;hl and Maikel Nadolski specified `execution::task` and its scheduler-affinity integration.<sup>[3]</sup><sup>[8]</sup> Dietmar K&uuml;hl reviewed an earlier draft and remarked that its sender example was wrong; investigating that remark led to the environment-level affinity bypass in [task.promise] p6, which Section 6 uses. Fabio Fracassi documented the composition problem that motivated the await-completion adaptor.<sup>[6]</sup> Dalton M. Woodard and Maikel Nadolski developed the completion-timing classifications examined here.<sup>[4]</sup><sup>[5]</sup> Jonathan M&uuml;ller documented the recursion hazard in `task` and its security framing.<sup>[10]</sup> Mika Fischer reported the deadlock and use-after-free traced in Section 9.<sup>[29]</sup><sup>[30]</sup> Mungo Gill, Steve Gerbino, and Klemens Morgenstern developed the companion coroutine and bridge analyses. Steve Gerbino contributed the seven-phase unit and the mechanism survey. Mungo Gill edited the September revision and integrated Lori's line edits into it.

## References

[1] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[2] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2026).

[3] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[4] [P2257R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2257r0.html) - "Blocking is an insufficient description for senders and receivers" (Dalton M. Woodard, 2020).

[5] [P3206R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3206r0.pdf) - "A sender query for completion behaviour" (Maikel Nadolski, 2025).

[6] [P3570R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3570r2.html) - "optional variants in sender/receiver" (Fabio Fracassi, 2025).

[7] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[8] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[9] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Daisy Hollman, Lee Howes, Kirk Shoop, Lewis Baker, Eric Niebler, 2020).

[10] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of std::execution::task" (Jonathan M&uuml;ller, 2025).

[11] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).

[12] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[13] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[14] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[15] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[16] [stdexec](https://github.com/NVIDIA/stdexec/tree/2c56ffe7f8a2b8b5221918159092be379ae8b40f) - "stdexec: Senders/receivers reference implementation" (NVIDIA, 2026). Quoted at commit `2c56ffe7`: `include/stdexec/__detail/__as_awaitable.hpp` and `test/stdexec/types/test_task.cpp`.

[17] [Beman.Execution](https://github.com/bemanproject/execution/tree/a20a6f636be4e8d0588521670a178f342695ece8) - "Beman.Execution: Building Block For Asynchronous Programs" (Beman Project, 2026). Quoted at commit `a20a6f63`: `include/beman/execution/detail/sender_awaitable.hpp` and `docs/implementation-status.md`.

[18] [libunifex](https://github.com/facebookexperimental/libunifex/tree/effb7527401b32b5a2d82fdf6d1a8e8810cbdb07) - "libunifex: A prototype implementation of the C++ sender/receiver async programming model" (Meta, 2026). Quoted at commit `effb7527`: `include/unifex/await_transform.hpp`.

[19] [Capy](https://github.com/cppalliance/capy/tree/75e1bed88770bfb392c3bece73e113a29c083796) - Coroutine-native I/O library (C++ Alliance, 2026).

[20] [P3149R11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3149r11.html) - "async_scope - Creating scopes for non-sequential concurrency" (Ian Petersen, Jessica Wong, 2025).

[21] [WSARecv function (winsock2.h)](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsarecv) (Microsoft, 2026).

[22] [SetFileCompletionNotificationModes function (winbase.h)](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setfilecompletionnotificationmodes) (Microsoft, 2026).

[23] [WSAEventSelect function (winsock2.h)](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsaeventselect) (Microsoft, 2026).

[24] [Corosio](https://github.com/cppalliance/corosio/tree/039fe65491a0be138cd6dfaf99cd11e49d865966) - Coroutine-native I/O library (C++ Alliance, 2026).

[25] [P3669R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3669r4.html) - "Non-Blocking Support for `std::execution`" (Detlef Vollmann, 2026).

[26] [stdexec PR #1658](https://github.com/NVIDIA/stdexec/pull/1658) - "add a `get_completion_behavior` query like in P3206" (Eric Niebler, 2025).

[27] [stdexec PR #1901](https://github.com/NVIDIA/stdexec/pull/1901) - "make `as_awaitable` savvy to senders that are known to complete inline" (Eric Niebler, 2026).

[28] [stdexec issue #212](https://github.com/NVIDIA/stdexec/issues/212) - "recursion, inline completion, and stack usage" (Eric Niebler, quoting Lewis Baker, 2021).

[29] [stdexec issue #2036](https://github.com/NVIDIA/stdexec/issues/2036) - "Deadlock in stdexec::task destructor when affine sender completes synchronously with set_stopped" (Mika Fischer, 2026).

[30] [stdexec issue #2047](https://github.com/NVIDIA/stdexec/issues/2047) - "Another crash with stdexec::task (again probably premature coro destruction)" (Mika Fischer, 2026).

[31] [Beman.Execution examples/stackoverflow.cpp](https://github.com/bemanproject/execution/blob/a20a6f636be4e8d0588521670a178f342695ece8/examples/stackoverflow.cpp) - with pull requests [#191](https://github.com/bemanproject/execution/pull/191), [#192](https://github.com/bemanproject/execution/pull/192), and [#224](https://github.com/bemanproject/execution/pull/224) (Beman Project, 2025-2026).

[32] [N5049](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5049.pdf) - "WG21 2026-06 Brno Admin Telecon Minutes" (Braden Ganetsky, 2026).

[33] [N5056](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5056.pdf) - "Business Plan and Convenor's Report: ISO/IEC JTC 1/SC 22/WG 21 (C++)" (Guy Davidson, 2026).

[34] [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[35] [N5047](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5047.html) - "Editors' Report, Programming Languages - C++" (Thomas K&ouml;ppe, Jens Maurer, Dawn Perchik, Richard Smith, 2026).

[36] [cplusplus/papers issue #2405](https://github.com/cplusplus/papers/issues/2405) - "P3801R0 Concerns about the design of std::execution::task" (WG21 paper tracker, 2025).

[37] [P1000R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p1000r8.pdf) - "Proposed C++ IS schedule" (Guy Davidson, 2026).
