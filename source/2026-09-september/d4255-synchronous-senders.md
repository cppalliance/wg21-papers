---
title: "Awaitables and Senders for Synchronous I/O"
document: P4255R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The sender protocol suspends a coroutine and constructs an operation state for a result that is already in memory; the awaitable protocol lets the operation check readiness and return.

C++20 awaitables and `std::execution` senders are both consumed from coroutines through `co_await`, and both carry the same inherent suspension for an asynchronous operation; they differ when the operation completes synchronously - a buffered write, a cached read, bytes already in user-space memory before `co_await` evaluates. One synchronous write is traced through both protocols, with the sender granted every affordance the standard provides: the inline-completing sender the task type itself specifies, and a task environment that bypasses scheduler affinity. The awaitable fixture has work in three of the seven phases of `co_await`; Capy's erased stream forwards readiness and takes the same three-phase path when the stream reports ready, and the shipped paths that suspend have work in six, resuming by symmetric transfer. The generic `sender-awaitable` path has work in all seven, because its `await_ready` returns `false` unconditionally and `connect` has already run before readiness is asked. The cost recurs at every iteration of a composed I/O loop. A concrete sender can sidestep the generic path with its own `as_awaitable` member, but that customization is manual, per-sender, and lost under type erasure; lifting the cost from the protocol itself requires a readiness query, a direct value-extraction path, and virtual dispatch for type erasure - three mechanisms whose counterparts are `await_ready`, `await_resume`, and the awaitable's own function-table dispatch, on top of the `connect` and `start` the protocol already carries.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## Introduction

The comparison here is of what `co_await` executes when an I/O operation completes synchronously under two protocols: the C++20 awaitable protocol as constrained by the IoAwaitable protocol of P4003R3,<sup>[1]</sup> and the `std::execution` sender protocol consumed through `execution::task` as P3552R3<sup>[2]</sup> specifies it. No wording is proposed.

Related work. P3552R3 specifies `execution::task` and its `await_transform`; P3941R2<sup>[3]</sup> specifies scheduler affinity for it; P3796R1<sup>[4]</sup> collects open issues with the task type, affinity among them; P3206R0<sup>[5]</sup> proposes a query by which a sender advertises inline completion. P4088R1<sup>[6]</sup> examines the design fork between coroutine-native and sender-native I/O; P4093R1<sup>[7]</sup> and P4092R1<sup>[8]</sup> bridge awaitables into sender pipelines and senders into coroutine-native code; P4126R1<sup>[9]</sup> removes the bridge's allocation.

Contributions:

1. A phase-by-phase trace of one synchronous write under both protocols, with senders in the most favorable configuration the standard provides (Sections 5-7).
2. A record of how the shipped awaitable libraries handle the synchronous case and the cost they carry for it (Section 6).
3. The composed-I/O multiplier that makes the per-operation difference recur (Section 10).
4. The modifications the sender protocol would need to match the awaitable protocol on this case, and a survey of the mechanisms that exist today (Section 11).

Assumptions. The sender trace follows the working draft N5054<sup>[10]</sup> and P3552R3,<sup>[2]</sup> with the task's environment naming `inline_scheduler` under both spellings of that knob (`scheduler_type` in P3552R3, `start_scheduler_type` in the working draft) so that no affinity cost is counted. The unit of comparison is the phase, defined in Section 5. No heap-allocation elision is assumed on either side. Runtime cost is measured only where Section 11.5 says so; elsewhere the comparison is of what the protocols specify.

## 1. The Abstraction

A synchronous write stream has one operation: accept a string and store it. No error codes, no byte counts, no partial writes. The abstraction is intentionally minimal - a test fixture that isolates the protocol's behavior from the I/O operation's complexity. Two concrete types implement it.

`string_sink` appends to a `std::string`. The operation is synchronous. The data is already in memory. No kernel transition occurs.

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

`tcp_sink` writes to a TCP socket. The operation is asynchronous. The kernel accepts the data, the coroutine suspends, the reactor resumes it when the write completes.

Both expose the same `write(std::string_view)` signature. The return type differs. The algorithm that calls `co_await sink.write(...)` does not.

## 2. Recompilation

The awaitable protocol provides two mechanisms for handling synchronous I/O without changing the algorithm's source. The first is recompilation: the same coroutine template compiled against different sink types produces different execution models.

The following illustrative algorithm writes a span of lines to a generic sink:

```cpp
template<class Sink>
task<> log_lines(Sink& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

Compile against `tcp_sink`. The awaitable returned by `write` suspends. The reactor resumes. The algorithm is asynchronous.

Recompile against `string_sink`. The awaitable returned by `write` has `await_ready() == true`. No suspension occurs. The algorithm is synchronous.

The source is identical. The awaitable type varies. The execution model is selected at compile time.

## 3. Relinking

The second mechanism is relinking: the same algorithm compiled once against a type-erased stream, with the execution model selected at link time. Where recompilation varies the template argument, relinking varies the object file behind a function table.

The following illustrative algorithm compiles against a type-erased stream. The shape follows Capy's `any_write_stream`:<sup>[11]</sup> `write` is not itself virtual, because a virtual function cannot return an implementation-specific awaitable type; it returns a fixed awaitable that calls through a function table. Capy's table is a struct of function pointers, not a C++ virtual table; this paper says function table for it and reserves virtual for the hypothetical sender base of Section 11.5:

```cpp
class write_stream
{
    struct vtable;
    void* impl_;            // the concrete stream
    vtable const* vt_;      // its function table
    void* cached_;          // storage for its awaitable, allocated once

public:
    // returns an IoAwaitable that calls through vt_
    auto write(std::string_view sv);
};

task<> log_lines(write_stream& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

The algorithm's object code is fixed. It does not know whether the stream is synchronous or asynchronous. It does not need to know.

Link against an object file that provides `tcp_sink` behind the function table. The algorithm is asynchronous.

Link against a different object file that provides `string_sink` behind the function table. The algorithm is synchronous.

Relinking requires no recompilation and costs zero allocations per write: the concrete stream's awaitable is constructed into storage the erased stream allocated once. The erased awaitable constructs the concrete awaitable inside its own `await_ready()` (Capy commit `9200ddc`) and forwards the answer. A ready stream completes without suspending, through four function-table calls (`construct_awaitable`, `await_ready`, `await_resume`, `destroy_awaitable`) and no scheduler. A pending stream suspends, a fifth call, `await_suspend`, forwards through the table, and the coroutine resumes by symmetric transfer - `await_suspend` returning the handle to resume, so the resumption is a tail call rather than a nested one. On either path no operation state, receiver, or nested resume exists. The algorithm was compiled once, and the execution model was chosen by the linker.

## 4. What Senders Provide

Before examining the sender path for synchronous I/O, this section records three properties `std::execution` provides that the awaitable protocol does not.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. Coroutines do not match this property for multi-stage pipelines.<sup>[12]</sup>

**Compile-time work graphs.** The sender algebra encodes directed acyclic graphs (DAGs) of work at the type level. `when_all`, `then`, `let_value` compose into a static structure the optimizer can see through. Domain customization via `transform_sender` retargets the same graph to CPU or GPU by swapping the scheduler.<sup>[13]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes.<sup>[14]</sup>

The comparison that follows grants senders every affordance: `inline_scheduler::schedule()` as the sender - the standard's own facility for inline completion<sup>[2]</sup> - synchronous completion inside `start`, the minimal `completion_signatures<set_value_t()>`, and a task whose environment names `inline_scheduler` as its scheduler type, so that `await_transform` skips the affinity wrapping (`affine_on` in P3552R3 `[task.promise]` p10; `affine` in the working draft `[task.promise]` p6) and no scheduler affinity step is counted. The `sender-awaitable` path that remains is imposed by the sender protocol on every sender that neither provides its own `as_awaitable` member nor supplies an await-completion adaptor, and on every sender consumed through `any_sender`, which erases both (Section 12). `any_sender` is this paper's name for the erased sender wrappers libraries ship, such as stdexec's `any_sender` (header `exec/any_sender_of.hpp`);<sup>[13]</sup> the working draft specifies none.

## 5. The Sender Path

Sections 2 and 3 showed the awaitable protocol's two mechanisms for synchronous I/O. This section traces the sender protocol's path for the same operation - a synchronous write to an in-memory string - using the best-case sender the standard provides.

Both traces use the same unit. A phase is one stage of `co_await` that the protocol's specification names: transform, connect, readiness, suspend, launch, complete, extract. Each trace lists all seven; a protocol with no work in a phase says so. The unit is the phase rather than the function call, so that wrapper forwarding on either side (a `transform_awaiter` calling through to the awaitable it wraps, a `sender-awaitable` calling `connect`) does not change the count. Four of the names are `[expr.await]`'s own stages (transform, readiness, suspend, extract); three are the sender protocol's (connect, `start` - called launch here - and completion), and a protocol that has no such stage leaves the phase empty. The sender's launch and complete phases both run inside the awaitable's suspend stage, which is why the sender-named phases are listed separately: the count is of protocol stages, and it is stated so that a reader who prefers `[expr.await]`'s four can recount. A readiness check counts as work whatever it answers, on both sides.

`string_sink::write` returns the sender produced by `inline_scheduler::schedule()`, the exposition-only `inline-sender` type from P3552R3<sup>[2]</sup>:

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
        return std::execution::
            inline_scheduler{}.schedule();
    }
};
```

The sender's `start` calls `set_value` on the receiver immediately. No kernel transition. No suspension on the sender side. This sender is not a hand-rolled type; it is the one P3552R3<sup>[2]</sup> specifies for inline completion.

A coroutine returning `execution::task` consumes it. The task's environment names `inline_scheduler` so that `[task.promise]` p10 skips affinity wrapping; the default environment uses `task_scheduler` and would wrap every awaited sender in `affine_on`:<sup>[2]</sup>

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

What happens inside `co_await sink.write(line)`, per the working draft<sup>[10]</sup> and P3552R3:<sup>[2]</sup>

1. Transform. `await_transform` receives the sender. P3552R3 `[task.promise]` p10 checks `same_as<inline_scheduler, scheduler_type>`;<sup>[2]</sup> the working draft `[task.promise]` p6 checks `same_as<inline_scheduler, start_scheduler_type>`.<sup>[10]</sup> The task's environment satisfies both, so the affinity wrapper (`affine_on` in P3552R3, `affine` in the working draft) is bypassed and `as_awaitable(sndr, *this)` is returned directly.

   `as_awaitable` then applies `transform_sender(sndr, get_env(p))` and `adapt-for-await-completion`, which queries `get_await_completion_adaptor` on the sender's environment and applies the adaptor when one is present; `inline-sender` supplies none, so the sender passes through unchanged. A `sender-awaitable` is constructed from the result (`[exec.as.awaitable]` p7-p8).<sup>[10]</sup>

2. Connect. The `sender-awaitable` constructor calls `connect(sndr, awaitable-receiver)`.<sup>[10]</sup> The operation state is materialized. The receiver is wired.

3. Readiness. `await_ready()` returns `false`.<sup>[10]</sup> Unconditionally.

4. Suspend. The coroutine suspends.

5. Launch. `await_suspend` calls `start(state)`.<sup>[10]</sup> Inside `start`, `set_value(receiver)` fires synchronously.

6. Complete. The receiver stores the result in a `variant` and calls `.resume()` on the coroutine handle, nested inside `await_suspend`.<sup>[10]</sup> The coroutine resumes.

7. Extract. `await_resume()` reads the value from the `variant`.<sup>[10]</sup>

All seven phases have work. One suspension and one resumption. One operation state construction. One receiver instantiation. One `variant` emplacement. No scheduler affinity wrapping. For an operation that completes synchronously.

The bypass in the transform phase belongs to the task's environment: every sender awaited from a task whose environment names `inline_scheduler` skips `affine_on`, a user-defined synchronous sender included.<sup>[2]</sup> Under the default environment the same `co_await` wraps the sender in `affine_on`<sup>[3]</sup> (P3941R2, "Scheduler Affinity," which specifies scheduler affinity enforcement for sender-based coroutines) and adds that operation's cost. Seven phases is therefore the floor for any sender that neither customizes `as_awaitable` nor supplies an await-completion adaptor (Section 4), in the most favorable task configuration the standard provides.

## 6. The Awaitable Path

The same operation traced through the awaitable protocol. Where Section 5 returned a sender from `write`, this section returns an IoAwaitable - a type satisfying the three-member protocol defined in P4003R3<sup>[1]</sup> (a minimal coroutine execution model that specifies executor affinity, stop-token propagation, and frame-allocator delivery for coroutines).

`string_sink::write` returns an IoAwaitable:

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
        return immediate{};
    }

private:
    struct immediate
    {
        bool await_ready() const noexcept
        {
            return true;
        }

        void await_suspend(
            std::coroutine_handle<>,
            io_env const*) noexcept
        {
        }

        void await_resume() noexcept {}
    };
};
```

A coroutine returning a task type that satisfies the IoAwaitable protocol<sup>[1]</sup> consumes it:

```cpp
task<> log_lines(
    string_sink& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

What happens inside `co_await sink.write(line)`:

1. Transform. `await_transform` delegates to `transform_awaitable`, which wraps the IoAwaitable in a `transform_awaiter`.<sup>[11]</sup>

2. Connect. No work.

3. Readiness. `await_ready()` returns `true`.

4. Suspend. No work. The coroutine does not suspend.

5. Launch. No work.

6. Complete. No work.

7. Extract. `await_resume()` returns.

Three phases have work: transform, readiness, extract. No suspension, no operation state construction, no receiver instantiation, no `variant` emplacement, no scheduler affinity wrapping.

`immediate` is the protocol's ceiling: `await_ready()` returns `true` because the fixture knows the result before `co_await` evaluates. The shipped libraries reach the same end by two paths. Corosio's socket awaitables return `true` from `await_ready()` only when a stop has been requested; `await_suspend` issues the syscall speculatively and, when it completes at once, returns the caller's own coroutine handle, so the coroutine suspends and resumes by symmetric transfer without a scheduler round-trip<sup>[15]</sup> (`native/native_tcp_socket.hpp`, `native/detail/reactor/reactor_stream_socket.hpp`). Capy's `any_write_stream` forwards the concrete awaitable's readiness through its function table<sup>[11]</sup> (`io/any_write_stream.hpp`, commit `9200ddc`): a ready stream takes the fixture's path through erasure, and a pending one suspends and resumes the same tail-call way; it issues no speculative syscall of its own. The fixture's `await_resume()` returns nothing; a shipped awaitable returns an `io_result` carrying an error code, which adds a return value and no phase. Corosio caps consecutive inline completions at an adaptive budget of 2 to 16, or 4 when no other thread has been woken to share the work, and posts the next completion through the queue, because unbounded inline completion starves other coroutines on the same executor. Inline completion is turned off entirely when the context is constructed from `io_context_options` at their defaults and the concurrency hint exceeds one. The budget is a cost of Corosio's shipped path that the fixture does not carry. On every path, no operation state, receiver, or `variant` exists; where a suspension occurs, the resumption is a tail call with no nested frame, and where the stream reports ready, Capy's erased path does not suspend at all.

## 7. Comparison

| Phase | Awaitable, fixture | Awaitable, shipped path | Sender |
| --------- | ------------------ | ----------------------- | ------ |
| Transform | `await_transform` wraps in `transform_awaiter` | same | `await_transform`, `as_awaitable`, `sender-awaitable` constructed |
| Connect | none | none | `connect(sndr, awaitable-receiver)`: operation state and receiver |
| Readiness | `await_ready()` is `true` | `await_ready()` is `false` on both: stop-based (Corosio) or forwarded from a pending stream (Capy) | `await_ready()` is `false`, unconditionally |
| Suspend | none | suspend | suspend |
| Launch | none | `await_suspend` issues the syscall speculatively (Corosio) or forwards through the function table (Capy) | `await_suspend` calls `start(state)` |
| Complete | none | returns the caller's handle: symmetric transfer | `set_value`, `variant` emplace, `resume()` nested in `await_suspend` |
| Extract | `await_resume()` | `await_resume()` | `await_resume()` reads the `variant` |

Table 1. The seven phases of a single `co_await sink.write(line)` on a synchronous `string_sink`. The fixture column is the `immediate` awaitable of Section 6. The shipped-path column covers Corosio's speculative-syscall socket awaitable and Capy's erased `any_write_stream` over a pending stream; a ready stream takes the fixture column through erasure. The sender column is the `sender-awaitable` path of Section 5 as the working draft specifies it, whose exposition-only `await_suspend` returns `void` and so resumes nested; stdexec's shipped awaiters, generic and inline alike, return the handle instead (Section 11.1, Table 4). A cell reading "none" means the protocol has no work in that phase.

| Property | Awaitable, fixture | Awaitable, shipped path | Sender |
| ----------------------------- | ------------------ | ----------------------- | ------ |
| Phases with work | 3 | 6 | 7 |
| Coroutine suspensions | 0 | 1 | 1 |
| Coroutine resumptions | 0 | 1, symmetric transfer | 1, nested inside `await_suspend` |
| Operation state constructions | 0 | 0 | 1 |
| Receiver instantiations | 0 | 0 | 1 |
| `variant` emplacements | 0 | 0 | 1 |
| Scheduler affinity wrappings | 0 | 0 | 0 |
| Type erasure allocations per write | not erased | 0 (Capy `any_write_stream`; four function-table calls when ready, five when it suspends - Section 3) | 0-1 (`any_sender::connect`; its erased `connect`, `start`, and completion calls are not counted here) |

Table 2. Objects and control transfers per write for the three paths of Table 1. Zero means the mechanism is not instantiated.

The connect and complete phases are where the sender column constructs what the other two columns never do: an operation state, a receiver, and a `variant`. The shipped awaitable path shares the suspend and launch phases with the sender only when readiness cannot be answered before launch - Corosio's stop-based `await_ready`, or Capy's erased stream over a pending concrete stream - and it constructs nothing in them, completing by tail call where the sender's completion is nested. When the concrete stream reports ready, Capy's erased path takes the fixture column: since commit `9200ddc` the wrapper forwards readiness and skips the suspension.

## 8. Interoperation

The awaitable protocol and the sender protocol are not mutually exclusive. An IoAwaitable can be wrapped as a sender and consumed by sender pipelines, and a sender can be consumed from coroutine-native code without `execution::task`.

P4093R1<sup>[7]</sup> (awaitable-to-sender bridge) provides `as_sender`, which wraps any IoAwaitable as a `std::execution` sender:

```cpp
auto sndr = as_sender(sink.write(line))
    | ex::then([] { /* next step */ });
```

The sender algebra works. `when_all` composes bridged IoAwaitables into parallel work. `let_value` sequences them. `upon_error` handles failures. The IoAwaitable is a leaf node in the sender's work graph. Structured concurrency is inherited from the sender pipeline.

Without callback handles, the bridge allocates one coroutine frame per bridged operation - the frame exists only to produce a `coroutine_handle<>`, the only type the awaitable protocol accepts. P4126R1<sup>[9]</sup> (callback handles for zero-cost bridging) shows this allocation is eliminable. A callback handle - three pointers matching the coroutine frame prefix, zero heap allocation - gives senders a `coroutine_handle<>` without allocating a frame.

The I/O layer is awaitable-native. Sender pipelines compose those awaitables into parallel work through the bridge. With P4126R1's callback handles,<sup>[9]</sup> the bridge imposes no allocation.

## 9. Overhead by Consumer and I/O Shape

Section 8 shows IoAwaitables entering sender pipelines via `as_sender`.<sup>[7]</sup> P4092R1<sup>[8]</sup> (sender-to-awaitable bridge) provides `await_sender`, through which senders are consumed from coroutine-native code without `execution::task`. P4088R1<sup>[6]</sup> (which documents the properties C++20 coroutines provide for stream I/O) examines the broader design fork between the two models.

The question is which implementation shape minimizes total cost when both consumers - coroutines and sender pipelines - exist.

| Consumer / I/O shape | Awaitable | Sender |
| -------------------- | --------- | ------ |
| **Coroutine** | | |
| Synchronous | transform, readiness, and extract (Section 6) | all seven phases (Section 5) |
| Asynchronous | no phase beyond the inherent suspend | connect and complete phases beyond the inherent suspend |
| **Sender pipeline** | | |
| Synchronous | none, given [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf)<sup>[9]</sup> | none |
| Asynchronous | none, given [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf)<sup>[9]</sup> | none |

Table 3. Protocol overhead per operation by consumer (coroutine or sender pipeline) and I/O shape (synchronous or asynchronous), for I/O primitives implemented as awaitables versus senders. The two awaitable-column pipeline cells assume the callback handles of P4126R1.

The awaitable path imposes no phase beyond `[expr.await]`'s own in any cell. For synchronous I/O, the sender column carries the connect, suspend, launch, and complete phases of Section 5. For asynchronous I/O, the sender protocol adds `connect`, receiver wiring, and `variant` emplacement atop the inherent suspend; the asynchronous operation itself requires none of the three.

For asynchronous I/O these added steps are a step count, not a separately observable runtime cost: once the operation suspends to a scheduler, the suspension dominates and the steps are not measurable above it. The case under comparison is synchronous completion, where no suspension absorbs them.

## 10. Composed I/O

Composed I/O algorithms call lower-level operations in a loop. This section examines how the protocol cost from Sections 5-7 multiplies across layered I/O stacks - the dominant pattern in protocol implementations such as TLS, HTTP, WebSocket, SMTP, and DNS resolution.

`read` fills a buffer by looping `read_some`. TLS decrypts by looping encrypted reads. HTTP sequences header parsing with body reads. Each layer is a coroutine composing awaitables. These algorithms are generic - constrained on concepts, agnostic to execution context.

Under the sender protocol, each iteration of such a loop executes every phase of Section 5 independently - even when the operation completes synchronously. Each synchronous completion constructs an operation state, instantiates a receiver, suspends the coroutine, calls `start`, fires `set_value` on the receiver, emplaces the result into a `variant`, and resumes the coroutine. For a 64 KB read from a stream that hands back 4 KB per `read_some`, this is sixteen iterations. On a buffered stream where every completion is synchronous, that is sixteen operation states, sixteen receivers, sixteen suspensions, sixteen resumptions - for data already in user-space memory.

The sender model's construction-before-launch separation is a strength during pipeline building: aggregate state, let the optimizer see the full graph. Inside a composed I/O loop, the pipeline is already built and running. The connect phase that serves construction-time visibility persists into execution, where it is no longer needed.

If the protocol can detect that the result is already available, the coroutine need not suspend. The suspension and resumption disappear. If the protocol can skip connection when the result is available, the operation state and the receiver disappear - the machinery that shuttles a value across a suspension boundary ceases to exist when no boundary exists. If the protocol expresses readiness through a single boolean - true: the value is here, take it directly; false: the value requires work, suspend, resume when ready - both cases are handled through one mechanism.

This is `await_ready`.

The following algorithm is `read` as implemented in Capy<sup>[11]</sup> (`include/boost/capy/read.hpp`). It composes `read_some` into `read` through `co_await`; the result is itself awaitable, and TLS composes `read`, and HTTP composes TLS:

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

Composition nests without sender algebra. When `read_some` completes synchronously, no allocation occurs, no operation state is constructed, no receiver is wired; the protocol adds nothing to what the hardware delivers. The requirement surface at each `co_await` is three members: `await_ready`, `await_suspend`, `await_resume`. The protocol is conditionally lazy: `await_ready() == false` defers, `await_ready() == true` proceeds. The concept constraint defines the interface, the awaitable defines execution semantics, the coroutine body defines composition logic - three concerns, no coupling. The algorithm accepts any type satisfying `ReadStream`, works across execution contexts without recompilation or runtime overhead, and imposes minimal requirements on user types. The coroutine frame outlives every `co_await` within it; activations nest, destructors run on every exit path, cancellation propagates downward.

When the stream is synchronous, no iteration leaves the coroutine's call chain: the fixture's `await_ready()` returns `true` - as does Capy's erased stream over a ready concrete stream - or, within Corosio's inline budget (Section 6), a shipped stream's `await_suspend` returns the caller's handle. On these paths no completion is scheduled and no operation state is constructed; the generic algorithm adds no protocol machinery to the copy.

Stepanov's iterator concepts do not impose indirection when dereferencing a pointer. A `T*` satisfies `random_access_iterator` and dereferences in one instruction. The concept does not require constructing an intermediate state object, wiring a callback, or performing a two-phase access protocol - even though a disk-backed iterator requires all of those internally. The cost is proportional to what the underlying data access requires.

The awaitable protocol has this property. `await_ready() == true` is the pointer dereference: the value is there, take it. `await_ready() == false` is the disk-backed iterator: the value requires work and the coroutine waits for it. The cost tracks the operation.

## 11. Closing the Gap

An already-available result is a case the committee has specified before. [P0159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0159r0.html)<sup>[16]</sup> (2015), the draft Concurrency TS, specifies `make_ready_future`, a future whose shared state is ready at construction. The sender protocol specifies a construction-side counterpart, `just()`, a sender whose value is ready at construction - but no consumption-side one. Awaited from a coroutine, `just()` takes the full `sender-awaitable` path like any other sender; inside a running pipeline, where the construction-before-launch property that motivates the design has already been used, a synchronous completion still takes it.

The sender model, as specified, does not match the awaitable model for synchronous I/O through the generic `sender-awaitable` path that every sender inherits unless it provides an escape. A concrete sender can sidestep that path by providing its own member `as_awaitable` or an await-completion adaptor<sup>[10]</sup> - manual, per-sender customizations that `any_sender` erases. The modifications below are what would lift the costs from the generic protocol itself, for every sender, including type-erased senders. Each addresses one layer of the gap.

### 11.1. A Readiness Query

`sender-awaitable::await_ready()` returns `false` unconditionally.<sup>[10]</sup><sup>[17]</sup> To skip suspension for senders that complete synchronously, a readiness query is required. The sender must advertise, at compile time or at run time, that its `start` will call `set_value` before returning.

The `await_transform` of P3552R3<sup>[2]</sup> does bypass `affine_on` when the task's environment names `inline_scheduler` (Section 5, transform phase). It does not bypass the `sender-awaitable` path. The six phases that follow - connect, readiness, suspend, launch, complete, extract - execute regardless.

| Mechanism | Where | What it provides | What it leaves |
| --------- | ----- | ---------------- | -------------- |
| `get_completion_behaviour` query | Proposed in P3206R0;<sup>[5]</sup> shipped as `get_completion_behavior` in stdexec<sup>[13]</sup> (`exec/completion_behavior.hpp`) | A sender advertises at compile time that it completes inline; stdexec's `task` answers the query | Not in the working draft; a query the working draft's `sender-awaitable::await_ready()` does not consult |
| Inline `__sender_awaiter` | stdexec<sup>[13]</sup> (`__as_awaitable.hpp`) | For a sender the query marks inline, `connect` and `start` move into `await_suspend` and the operation state does not outlive it; both stdexec awaiters, generic and inline, return the continuation handle from `await_suspend`, so the resume is a symmetric transfer | `await_ready()` still returns `false`; the coroutine still suspends; the operation state and receiver are still constructed |
| `get_await_completion_adaptor` | Working draft `[exec.get.await.adapt]`<sup>[10]</sup> | A sender's attributes supply an adaptor applied to it before `sender-awaitable` is built; the adapted sender may provide its own `as_awaitable`, reaching a custom awaitable without an `as_awaitable` member on the original sender | Per-sender, like the member, and lost under `any_sender` like the member; the generic `sender-awaitable` keeps its unconditional `false` |
| `affine_on` member | P3941R2<sup>[3]</sup> s3.4; `affine()` in the working draft `[exec.affine]`<sup>[10]</sup> | A sender opts out of rescheduling | Affinity only (Section 11.4) |

Table 4. Readiness and inline-completion mechanisms in the sender ecosystem, with what each closes of the gap traced in Sections 5-7 and what remains.

stdexec is the closest of the four: both of its awaiters avoid the nested resume, and the inline one additionally delivers the deferred connection of Section 11.3; it keeps the suspension, the operation state, and the receiver. None of the four gives `sender-awaitable` a readiness query; the working draft has none. What is required is a trait, a tag, or a constexpr query in the shape P3206R0 proposes, consulted by `sender-awaitable::await_ready()`.

### 11.2. Conditional Suspension

With a readiness query in place, `sender-awaitable::await_ready()` can return `true` when the sender advertises synchronous completion. The coroutine no longer suspends.

But `connect` was already called in the `sender-awaitable` constructor.<sup>[10]</sup> The operation state was already materialized. The receiver was already wired. The `variant` was already allocated. The suspend phase was saved. The connect and complete phases were not.

### 11.3. Deferred Connection

To skip those steps, `connect` must be moved from the `sender-awaitable` constructor into `await_suspend`, where it can be bypassed when `await_ready()` returns `true`.

But the value needs to come from somewhere. `await_resume` must return the result. If `connect` and `start` did not execute, no receiver received the value. The sender needs a second value-delivery mechanism - a `get_value()` member, a direct extraction path, a way to produce the result without constructing an operation state, wiring a receiver, calling `start`, routing through `set_value`, and emplacing into a `variant`.

The sender model then carries two value-delivery mechanisms: channels for asynchronous completion, direct extraction for synchronous completion.

### 11.4. Affinity Wrapping Is Already Conditional

Scheduler affinity is not part of the gap. `[task.promise]` (P3552R3 p10, working draft p6) skips the affinity wrapper for every sender when the task's environment names `inline_scheduler`,<sup>[2]</sup> and P3941R2<sup>[3]</sup> lets an individual sender opt out of rescheduling through an `affine_on` member function. Neither mechanism reaches the `sender-awaitable` path of Sections 11.1-11.3: with affinity wrapping removed, `await_ready()` still returns `false`, the coroutine still suspends, and the operation state is still constructed. The remaining modifications concern that path alone.

### 11.5. Zero-Allocation Type Erasure

`any_sender::connect` produces a type-erased operation state whose size is unknown at compile time. The current implementations use small-buffer optimization (64 bytes in stdexec) or heap allocation.<sup>[13]</sup> The per-operation cost is zero or one allocation.

Measured in the Capy benchmark suite<sup>[11]</sup> (`bench/beman`, commit `d45ae3e`) on a type-erased no-op read, single thread, 20,000,000 operations per cell, clang 22.1.5 release build: the type-erased awaitable consumed by a `capy::task` coroutine allocates zero times per operation; the type-erased `any_sender` consumed by a `beman::execution::task` coroutine allocates once. Wall-clock was 37 ns per operation for the awaitable and 55 ns for the sender on a machine that was not recorded; a rerun of the same source on 2026-08-28 with clang 22.1.8 on an Intel Core i9-13900H gave 36.2 ns and 54.7 ns with the same allocation counts. The wall-clock figure spans two coroutine frameworks and is reported for context; the allocation count is the structural result.

The awaitable model's type erasure adds no allocation on either path, at the call counts of Section 3. To match this, the sender needs a base class with a virtual function that returns the value directly - without constructing an operation state, without wiring a receiver, without calling `start`.

### 11.6. The Result

The preceding sections trace the modifications the sender model would require to match the awaitable model for synchronous I/O. The following hypothetical type collects them:

```cpp
struct sync_ready_sender
{
    using sender_concept = sender_t;
    using completion_signatures =
        completion_signatures<set_value_t()>;

    // 11.1: readiness query
    static constexpr            // cf. await_ready()
        bool is_synchronous = true;

    // 11.3: direct extraction (bypass connect)
    void get_value()            // cf. await_resume()
        const noexcept;

    // 11.5: virtual base for type erasure
    virtual void                // cf. virtual
        get_value_erased()      //     await_resume()
        const;

    // original protocol (retained for async)
    template<class Receiver>
    struct state { /* ... */ };

    template<class Receiver>
    state<Receiver> connect(Receiver&&) const;
};
```

The awaitable that already provides the same capabilities:

```cpp
struct immediate
{
    bool await_ready() const noexcept;
    void await_suspend(
        std::coroutine_handle<>,
        io_env const*) noexcept;
    void await_resume() noexcept;
};
```

Each modification in the sender column has a direct counterpart in the awaitable's three members. The sender protocol arrives at a readiness query (`is_synchronous` maps to `await_ready`), a direct extraction path (`get_value` maps to `await_resume`), and virtual dispatch for type erasure (maps to the function-table call of Section 3).

## 12. Concerns

**"P4126R1 is unshipped. The bridge cost is hypothetical."** Both sender-pipeline cells in the awaitable column of Section 9 depend on P4126R1.<sup>[9]</sup> Callback handles would allow sender pipelines to consume awaitables without allocation. The core finding (Sections 5-7) rests on normative text; the bridge zeros are what callback handles would add.

**"A sender can provide a member `as_awaitable` and skip the `sender-awaitable` phases. No protocol change is needed."** True. `[exec.as.awaitable]` p7 uses a sender's own `as_awaitable` when the sender provides one, and otherwise an awaitable produced by the environment's await-completion adaptor when that is well-formed, before it falls back to constructing the generic `sender-awaitable`. The following is a paraphrase of p7 that omits the two awaiter-passthrough branches:<sup>[10]</sup>

```cpp
// paraphrase of [exec.as.awaitable] p7; adapt is adapt-for-await-completion
template<class Expr, class Promise>
decltype(auto) as_awaitable(Expr&& e, Promise& p)
{
    if constexpr (requires { e.as_awaitable(p); })
        return e.as_awaitable(p);                        // (7.1) the sender's own
    else if constexpr (requires {
        adapt(transform_sender(e, get_env(p))).as_awaitable(p); })
        return adapt(transform_sender(e, get_env(p)))
            .as_awaitable(p);                            // (7.2) the adaptor's
    else
        return sender-awaitable{
            adapt(transform_sender(e, get_env(p))), p};  // (7.4) every phase
}
```

In `execution::task` with an `inline_scheduler` environment (Section 5), `await_transform` passes the sender to `as_awaitable` unwrapped, and a sender whose `as_awaitable` returns a synchronous awaitable then takes the path of Section 6.<sup>[2]</sup> `connect`, the receiver, `start`, and the `variant` are never instantiated. Only the transform, readiness, and extract phases remain. Under the default environment the sender is first wrapped in `affine_on`, and the member check in `[exec.as.awaitable]` runs on the wrapper rather than on the sender that defines the member.

The affinity bypass and the `as_awaitable` member are independent mechanisms: the first is a property of the task's environment and applies to every awaited sender, the second is per-sender. Only the second reaches `sender-awaitable`, and it is lost under type erasure.

The synchronous fast path the sender reaches through `as_awaitable` is an awaitable: the sender hands one back, and the awaitable does the work. Closing the gap for one concrete sender, awaited from a coroutine, is one existing customization point returning the three-member struct of Section 6.

Two costs remain. The `as_awaitable` member is manual and per-sender; a sender that omits it inherits every phase of Section 5. And it is lost under type erasure: `any_sender` erases the concrete sender and the member with it, and `any_sender::connect` materializes the operation state of Section 11.5. Type erasure is the one sender-specific cost no `as_awaitable` member reaches.

The scope is the coroutine consumer. A sender pipeline never enters `as_awaitable`; Section 9 records no protocol phase for either synchronous pipeline cell.

**"The protocol cannot know at compile time whether a given co_await will always complete synchronously. The operation state must be constructed because the protocol must handle the general case."** The awaitable protocol handles this case at runtime. `await_ready()` is evaluated at the point of `co_await`: if the result is available, return `true` - no suspension; if work is required, return `false` - suspend. The protocol does not need compile-time knowledge. It asks the operation at the point of evaluation. For senders that are always synchronous (like `inline-sender`), the property is known at compile time - a constexpr trait could express it. The working draft has no such trait; P3206R0<sup>[5]</sup> proposes one and stdexec ships it, and neither is consulted by the working draft's `sender-awaitable::await_ready()` (Section 11.1, Table 4). The "cannot know" argument applies equally to awaitables, yet an awaitable whose `await_ready()` depends on runtime state handles both cases through the same three-member protocol: when ready, no suspension, no operation state, no receiver; when not ready, a suspension until the work completes. One protocol, two behaviors, selected at the point of evaluation.

**"The optimizer eliminates the protocol overhead."** The nested resumption is observable at runtime as stack growth, independent of optimization. When `await_ready()` returns `false`, `await_suspend` calls `start`; for an inline completion, `set_value` calls `resume()` on the coroutine handle from inside `await_suspend`, so the coroutine resumes nested on the same stack, before `await_suspend` returns. That nested resumption is the stack-growth hazard P2583R4<sup>[17]</sup> documents, and it occurs whether or not the optimizer inlines `connect` and `start`. `[exec.as.awaitable]` specifies unconditional suspension for `sender-awaitable`;<sup>[10]</sup> the as-if rule would let an implementation elide it only where nothing observable depends on it, and the one shipped implementation Table 4 surveys, stdexec, does not. Making the skip part of the protocol requires a specification change, which is Section 11.1.

**"Operation state construction delivers structured concurrency guarantees."** Genuine for asynchronous operations where the coroutine suspends and work executes concurrently. For a synchronous write where the data is in the string before `co_await` evaluates, there is no concurrent lifetime to manage. The operation state guarantees a property that was never at risk.

**"Protocol step counts are not runtime costs."** True for `connect`, `start`, and `set_value` when sender and receiver are fully visible to the optimizer and the optimizer is sufficiently aggressive. Not true for the resumption, which under the working draft's `sender-awaitable` is a nested call inside `await_suspend` regardless of inlining; stdexec's awaiters return the handle instead (Table 4), the shipped awaitable paths resume by symmetric transfer when they suspend, and the fixture and a ready erased stream do not suspend at all. Not true across type-erasure boundaries, where `any_sender::connect` materializes an operation state outside the optimizer's view.

**"Awaitables do not compose into work graphs."** They do, through the bridge. Section 8 shows IoAwaitables consumed by sender pipelines via `as_sender`.<sup>[7]</sup> The sender algebra - `when_all`, `let_value`, `upon_error` - works. The bridge cost is eliminable with P4126R1.<sup>[9]</sup>

**"Unconditional suspension is the sound default."** The awaitable protocol solved this in C++20 with a single boolean. `await_ready()` provides the override. The sender protocol has no equivalent conditional path.

**"The composed algorithm is sequential - real composition requires parallelism."** Sequential composition over a single stream is expressed as a coroutine loop. Parallel composition across multiple streams - scatter-gather, concurrent requests, fan-out/fan-in - is expressed through the sender algebra via the bridge of Section 8. Sequential I/O composition is the pattern Section 10 names. Each layer is a coroutine composing awaitables, and each inner await that completes synchronously executes the connect, suspend, launch, and complete phases independently under the sender protocol. The multiplier is proportional to the protocol's depth: HTTP over TLS over TCP is three layers of composed coroutines, each with its own `read_some` loop, each iteration incurring the cost independently.

**"The composed read loop has no cancellation propagation."** Stop tokens propagate transparently through `io_env` - the execution environment bundle passed to every IoAwaitable via `await_suspend(coroutine_handle<>, io_env const*)`.<sup>[1]</sup> Each child operation inherits the caller's stop token without explicit wiring. Every stream operation observes the stop token and may complete early with an operation-cancelled error. The mechanism is defined in P4003R3<sup>[1]</sup>.

**"The bridge concedes the dependency."** The bridge operates in both directions. P4093R1<sup>[7]</sup> bridges IoAwaitables into sender pipelines. P4092R1<sup>[8]</sup> bridges senders into coroutine-native code without `execution::task`. Section 9 shows the cost is asymmetric: if I/O is an awaitable, neither consumer incurs protocol overhead; if I/O is a sender, coroutine consumers incur it.

**"The comparison measures the wrong case."** Synchronous completion is not a corner case in I/O. Buffered writes, cached reads, DNS cache hits, and in-memory operations complete synchronously. A protocol that adds cost to the common fast path repeats that cost on every operation on a connection.

**"Senders retarget via scheduler swap; awaitables require recompilation."** Section 3 demonstrates retargeting by relinking: the linker swaps the object file behind the function table.

**"The modifications in Section 11 are natural evolution."** Each modification introduces a new mechanism: a readiness query, a second value-delivery path, virtual dispatch for type erasure. The awaitable protocol provides the same capability with three members.

**"The type erasure comparison is asymmetric."** Both paths use type erasure at the same boundary. The awaitable path makes four function-table calls when the stream reports ready, five with a symmetric-transfer resume when it suspends, and constructs no operation state; `any_sender` makes its own erased calls to `connect`, `start`, and the completion, and materializes an operation state the compiler cannot see through, in a small buffer or on the heap. The count that separates the two is the allocation, and Section 11.5 measures it.

**"The falsification criteria measure senders on the awaitable's own terms."** The Disclosure names the limitation: coroutine-native I/O cannot express compile-time work graphs. Section 4 credits senders with three properties awaitables do not match, and Section 9 covers both synchronous and asynchronous I/O. The criteria in Section 13 cover synchronous protocol cost, which is the claim under test.

## 13. Falsification

The observations documented in this paper would no longer hold if any of the following were demonstrated:

- A sender protocol mechanism, equivalent to `await_ready`, that skips `connect` and `start` for trivially ready senders without introducing a second value-delivery path.

- A `sender-awaitable` implementation in which `await_ready()` returns `true` when the sender is known to complete synchronously, without requiring `connect` to have already executed. stdexec's inline awaiter (Table 4) defers `connect` and keeps `await_ready()` at `false`, so it does not meet this criterion.

- A type-erasure mechanism for senders that achieves zero allocations per operation without constructing an operation state and without reintroducing virtual dispatch.

## 14. Conclusion

For a result already in memory, the sender protocol connects, suspends, launches, completes through a receiver, and resumes nested. The awaitable fixture checks readiness and returns, and the shipped libraries avoid the sender's construction on this path: Capy's erased stream forwards readiness and skips the suspension when the stream reports ready, and Corosio, whose `await_ready` answers only a stop request, suspends and resumes by tail call, at the cost of an inline budget. The gap is in the generic `sender-awaitable` path: `await_ready()` is specified as `false`, `connect` runs in the constructor, and the receiver's `set_value` resumes the coroutine from inside `await_suspend`. Sections 11.1, 11.3, and 11.5 name what would close it - a readiness query consulted before suspension, an extraction path that does not pass through a receiver, and an erased base that returns the value through one virtual call - and each is the sender-side spelling of `await_ready`, `await_resume`, and the function-table call of Section 3.

The per-operation difference is multiplied by composition. Section 10 shows a `read` that loops `read_some` and completes synchronously on every iteration; under the sender protocol each of those iterations constructs and tears down an operation state, and TLS and HTTP each add a loop of their own above it.

The two protocols interoperate. IoAwaitables enter sender pipelines through `as_sender`;<sup>[7]</sup> senders enter coroutine-native code through `await_sender`.<sup>[8]</sup> P4126R1's callback handles<sup>[9]</sup> eliminate the bridge's allocation cost. If I/O primitives are awaitables, neither coroutine consumers nor sender-pipeline consumers incur protocol overhead. If I/O primitives are senders, coroutine consumers incur it.

The wording that would change this is `[exec.as.awaitable]` and `[task.promise]` in the working draft,<sup>[10]</sup> which came from P2300R10<sup>[12]</sup> and from P3552R3<sup>[2]</sup> with P3941R2;<sup>[3]</sup> a change there is a paper against those sections, reviewed by LEWG. Until the wording changes, a sender awaited from a coroutine carries a suspension and an operation state for a result that is already in memory.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[11]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[15]</sup>, coroutine-native I/O libraries under the C++ Alliance.

This paper documents the protocol-level cost difference between awaitables and senders when I/O operations complete synchronously.

Capy and Corosio implement I/O using the coroutine-native model. They compete with sender-based networking frameworks. The author advocates for the coroutine-native model. The sender model is the competing paradigm examined in this paper. The author has a stake in the coroutine model's adoption.

The write-side readiness forwarding described in Sections 3 and 6 is recent: Capy commit `9200ddc` (August 2026), applied during the drafting of this paper, aligned `any_write_stream` with the immediate-completion behavior its documentation and the read-side wrapper already specified. The core finding does not rest on that path; the fixture and the normative sender text carry it.

Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation.

This paper belongs to the Network Endeavor series. Companion papers in the series include P4003R3<sup>[1]</sup> (the IoAwaitable protocol), P4088R1<sup>[6]</sup> (coroutine advantages for stream I/O), P4093R1<sup>[7]</sup> (awaitable-to-sender bridge), P4092R1<sup>[8]</sup> (sender-to-awaitable bridge), P4126R1<sup>[9]</sup> (callback handles for zero-cost bridging), and P2583R4<sup>[17]</sup> (symmetric transfer in sender pipelines).

This paper was drafted and revised with machine assistance (Claude), under the author's direction; the technical claims were verified against the cited sources and repositories.

This paper asks for nothing.

## Acknowledgments

Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators for `std::execution` and the sender algebra. Dietmar K&uuml;hl and Maikel Nadolski for [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[2]</sup> (`std::execution::task`). Dietmar K&uuml;hl for reviewing an earlier draft and remarking that the sender example was wrong. Investigating that remark led to a closer reading of P3552R3's `await_transform` and of the environment-level affinity bypass in `[task.promise]` (p10 in P3552R3, p6 in the working draft), which informed the task configuration used in Section 5. Robert Leahy for the AIO-to-sender bridge.

## References

[1] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[2] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[3] [P3941R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r2.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[4] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[5] [P3206R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3206r0.pdf) - "A sender query for completion behaviour" (Maikel Nadolski, 2025).

[6] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[7] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[8] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[9] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[10] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages &mdash; C++" (Thomas K&ouml;ppe, 2026).

[11] [Capy](https://github.com/cppalliance/capy) (C++ Alliance, 2025).

[12] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[13] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - "A reference implementation of `std::execution`" (NVIDIA, 2021).

[14] [P3149R11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3149r11.html) - "async_scope &ndash; Creating scopes for non-sequential concurrency" (Ian Petersen, Jessica Wong, 2025).

[15] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance, 2026).

[16] [P0159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0159r0.html) - "Draft of Technical Specification for C++ Extensions for Concurrency" (Artur Laksberg, 2015).

[17] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).
