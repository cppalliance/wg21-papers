---
title: "Awaitables as the Natural Leaf Protocol for Coroutine-Centric Input/Output"
document: P4255R0
date: 2026-09-07
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

For coroutine-centric input/output (I/O), awaitables are the natural leaf protocol because sender-valued operations add a second composition model whose generic coroutine bridge lacks per-instance readiness.

Senders provide static composition, completion channels, operation ownership, environments, and structured concurrency, which sender-native consumers use directly. When a coroutine consumes a sender-valued I/O leaf through the generic bridge, translation adds connection, operation state, receiver completion, and an awaiter that always reports not ready. Custom awaiters, await-completion adaptors, domain transformations, and declared erased interfaces can select a different coroutine path, while completion-behavior queries and implementation techniques can reduce state and synchronization after a false readiness result. Branch 7.4 itself contains no pre-initiation query for whether a particular operation already holds a buffered result, whereas an awaitable exposes that decision directly.

## Revision History

### R0: September 2026

- Initial revision.

## Introduction

C++ now has two standardized composition surfaces that meet at `co_await`. The coroutine language consumes an awaiter through readiness, conditional suspension, and extraction; `std::execution` constructs asynchronous operations through senders, receivers, connection, and start.<sup>[1]</sup> `execution::task` joins them by translating an awaited sender into an awaiter.<sup>[2]</sup>

P2300R10 defines the sender model and its generic sender-to-awaitable bridge.<sup>[3]</sup> P2257R0 and P3206R0 examine completion timing, with P3206R0 proposing static, environment-dependent, and dynamic completion behavior.<sup>[4]</sup><sup>[5]</sup> P3570R2 supplied the composition case that led to the forwarding await-completion adaptor now in the working draft.<sup>[6]</sup> P3552R3, P3796R1, and P3941R4 develop task integration, stack bounding, and scheduler affinity.<sup>[2]</sup><sup>[7]</sup><sup>[8]</sup>

Coroutine control transfer has its own history. P0913R1 added symmetric coroutine transfer, P1056R1 applied it to lazy tasks, and P2583R4 examines its absence from intermediate sender receivers.<sup>[9]</sup><sup>[10]</sup><sup>[11]</sup> P3801R0 separately identifies recursive behavior when sender completions resume task coroutines inline.<sup>[12]</sup> P4003R3 defines the IoAwaitable protocol used here, while P4092R1, P4093R1, and P4126R1 examine both bridge directions and their continuation requirements.<sup>[13]</sup><sup>[14]</sup><sup>[15]</sup><sup>[16]</sup>

1. A vocabulary separating synchronous completion, inline completion, per-instance pre-start readiness, and a coroutine fast path.
2. A side-by-side account of the language awaiter surface and the sender-to-awaitable translation surface.
3. A normative trace that includes every `as_awaitable` branch and the implementation freedom available to standard-library senders.
4. Three I/O fixtures separating an already-materialized result, completion discovered during initiation, and a pending operation.
5. A survey of completion behavior, await-completion adaptation, domain transformation, composition, erasure, and two public implementations.

The scope is coroutine-centric I/O: operations whose primary consumer is a coroutine body and whose higher-level buffering can make a result available before initiation. Sender-native pipelines, direct receiver consumers, and system calls whose completion becomes known only during initiation remain in the comparison but are not covered by the central conclusion.

The term "natural leaf protocol" has four criteria: direct language integration, a per-instance readiness decision, one operation representation for coroutine consumption, and no sender-to-awaitable translation layer. The criteria are the author's analytical standard and are applied to both protocols in Table 2. The author maintains awaitable-native libraries and has a professional interest in the result. If a delegate rejects the word "natural" or these criteria, the normative fallback finding remains: branch 7.4 connects before readiness and returns `false` from `await_ready` for every instance.<sup>[1]</sup>

"Wording burden" means additional standardized entities and semantic interactions. It does not mean generated runtime cost.

N5054 and the current public draft rendering supply the normative basis.<sup>[1]</sup> Source claims use immutable stdexec and Beman.Execution commits from September 2026. Phase counts are not used as a performance model, and no benchmark result is used as evidence.

## Sender Composition Solves a Different Problem

Sender and receiver provide a general model for constructing and composing asynchronous operations. The properties that make that model useful remain relevant when its coroutine-consumption path is examined.

The sender model provides static composition. Adaptors such as `then`, `let_value`, and `when_all` form typed work graphs whose connected operation state owns the state of its children. P2300R10 describes the performance requirement as avoiding allocations and indirections in generic asynchronous algorithms expected on hot paths.<sup>[3]</sup> This is a property of sender-native composition rather than of one leaf operation.

The model also provides three completion channels. A receiver accepts value, error, or stopped completion, and completion signatures describe those possibilities for a sender in an environment. Environments provide schedulers, allocators, stop tokens, and domain information used to transform or execute the operation. The native protocol therefore describes more than suspension and resumption.

Operation states give the connected operation a lifetime. The working draft says that connecting a sender and receiver creates an asynchronous operation, while `start` begins it.<sup>[1]</sup> Destroying an operation state while its operation is still live has undefined behavior. This ownership boundary is necessary when work remains pending after initiation.

The model permits an asynchronous operation to execute synchronously. The working draft states that an operation can complete during `start` on the starting thread, and `inline_scheduler` completes by calling `set_value` directly from `start`.<sup>[1]</sup> Synchronous execution is therefore part of the sender model.

Structured concurrency is another sender-side facility. The counting-scope facilities track associated work and require the scope to reach an allowed state before destruction; premature destruction invokes `terminate` rather than preventing destruction.<sup>[1]</sup><sup>[17]</sup>

Sender-native composition provides static work graphs, explicit completion channels, operation ownership, environmental customization, and structured concurrency. The awaitable leaf protocol does not replace those properties.

## Completion and Readiness Are Different Properties

Synchronous execution is not one property. Four separate properties determine what a coroutine can avoid, and using one name for all four conflates distinct protocol properties.

| Term | Meaning in this analysis |
| --- | --- |
| **Synchronous completion** | The operation executes a completion operation before `start()` returns. |
| **Inline completion** | The operation completes before `start()` returns on the execution agent that called `start()`. |
| **Per-instance pre-start readiness** | This operation object already has its result before initiation, although another object of the same type may not. |
| **Coroutine fast path** | The coroutine obtains the result without being considered suspended by `[expr.await]`. |
| **Awaiter** | The object on which the language evaluates `await_ready`, `await_suspend`, and `await_resume`. |
| **Operation state** | The object produced by connecting a sender and receiver and passed to `start`. |

Table 1. The four completion properties and the two protocol objects used throughout the comparison. The definitions separate completion discovered during initiation from a result known before initiation.

The working draft defines synchronous completion through timing relative to `start`.<sup>[1]</sup> Different instances of one sender type may complete during `start` or later. The definition does not provide a pre-start result or a way for a coroutine to ask whether one exists.

The coroutine language asks a different question. After promise transformation and awaiter selection, `[expr.await]` evaluates `await_ready()` before deciding whether the coroutine is considered suspended.<sup>[1]</sup> A true result proceeds to `await_resume`; a false result enters the suspension path and evaluates `await_suspend`. The result is a property of the awaiter object, so two objects of the same type can return different values.

P3206R0 proposes completion behavior as a sender attribute.<sup>[5]</sup> Its categories describe whether receiver completion occurs before `start` returns and whether it occurs inline. The proposal permits static type information, environment-dependent queries, and a dynamic result for `split` after its shared operation has completed. It contains no wording, and the working draft's generic sender awaiter does not query it.

Completion behavior and pre-start readiness can correlate without being equivalent. A sender may guarantee inline completion because `start` performs work immediately, even though no result exists beforehand. Conversely, a shared or cached operation may already hold a result and still expose that result through `start` and receiver completion.

Synchronous completion, inline completion, per-instance readiness, and a coroutine fast path are four distinct properties. Only the third represents whether a particular result is already available before initiation.

## Awaitables and Senders Expose Different Consumption Surfaces

The two protocols expose different surfaces to a coroutine consumer. The protocol difference concerns specification structure and semantic obligations; entity counts do not establish runtime cost.

An awaitable reaches the language through one awaiter. The language evaluates `await_ready`, conditionally evaluates `await_suspend`, then evaluates `await_resume`.<sup>[1]</sup> P4003R3 extends the suspend member with an I/O environment that provides executor, stop-token, and allocator information, while retaining the same readiness and extraction boundary.<sup>[13]</sup>

A sender reaches the same language protocol after a second composition model has been translated. A compatible sender describes completion signatures in an environment, transforms through its domains, may acquire scheduler affinity, may apply an await-completion adaptor, connects to a receiver, stores a resulting operation state, starts it, accepts one completion channel, stores the result for the coroutine, and finally presents an awaiter to `[expr.await]`.<sup>[1]</sup> Each mechanism provides a sender property; the translation is additional only for a coroutine consumer.

| Concern | Awaitable leaf | Sender-valued leaf awaited by `execution::task` | Sender capability provided |
| --- | --- | --- | --- |
| Result alternatives | `await_resume` return or throw | Completion signatures and value, error, stopped channels | Generic composition over completion alternatives |
| Consumer context | Promise and I/O environment | Receiver environment, sender attributes, domains, task promise | Scheduler, allocator, cancellation, and domain customization |
| Operation creation | Awaiter construction | `connect(sender, receiver)` produces an operation state | Separate graph construction from activation |
| Activation | `await_suspend` when not ready | `start(operation_state)` from the bridge's `await_suspend` | Uniform lazy start |
| Pre-suspension decision | `await_ready()` on this awaiter object | Custom awaiter, or fixed `false` in the generic fallback | The native sender protocol specifies completion timing instead |
| Coroutine translation | None after awaiter selection | `await_transform`, optional `affine`, `as_awaitable`, transformation, adaptation, then awaiter selection | Interoperation with sender-valued expressions |

Table 2. The protocol surfaces used when a coroutine consumes an awaitable leaf or a sender-valued leaf. The right column records why the sender mechanism exists; the table measures wording requirements and semantic obligations rather than generated instructions.

A sender pipeline uses completion signatures, connection, and receiver channels directly. A coroutine body already supplies sequencing, lifetime, and conditional suspension, so sender-valued I/O must cross both protocol surfaces before the language can consume it.

Awaitables expose per-instance readiness directly, while the native sender path exposes completion after an operation has been connected and started.

## The Generic Bridge Has No Per-Instance Readiness Branch

The working draft provides five routes from an expression to an awaiter. The generic sender fallback is only the last sender-specific route, and its exact placement prevents the trace from being generalized to every conforming sender.

Inside `execution::task`, `await_transform` first handles scheduler affinity. If the task's `start_scheduler_type` is `inline_scheduler`, it passes the sender directly to `as_awaitable`; otherwise it applies `affine` first.<sup>[1]</sup><sup>[2]</sup> Affinity is therefore a separate concern from readiness.

`as_awaitable(expr, promise)` then selects among five ordered results:<sup>[1]</sup>

1. The expression's own `as_awaitable` member.
2. An `as_awaitable` member on the transformed and await-completion-adapted sender.
3. The original expression when it is already an awaiter.
4. The exposition-only `sender-awaitable` for a compatible single-value sender.
5. The original expression otherwise.

The first three routes can avoid the generic bridge. The second route applies `transform_sender` before consulting the forwarding `get_await_completion_adaptor` query, so a domain or attribute adaptor can supply a common coroutine representation for more than one concrete sender type.

The fourth route constructs the exposition-only `sender-awaitable`. Its relevant shape is:

```cpp
variant<monostate, result-type, exception_ptr> result{};
connect_result_t<Sndr, awaitable-receiver> state;

sender-awaitable(Sndr&& sndr, Promise& p);
static constexpr bool await_ready() noexcept { return false; }
void await_suspend(coroutine_handle<Promise>) noexcept { start(state); }
value-type await_resume();
```

This is working-draft exposition from `[exec.as.awaitable]`.<sup>[1]</sup> The constructor initializes `state` with `connect`, so connection precedes the language's readiness question. `await_ready()` then returns `false` for every object. `await_suspend()` starts the operation.

Completion reaches an `awaitable-receiver`. Value or error completion emplaces a result or exception in the stored variant, then evaluates `continuation.resume()`; stopped completion resumes the handle selected by the promise's `unhandled_stopped` operation.<sup>[1]</sup> `await_resume()` rethrows the stored exception or extracts the stored value. The variant is a subobject whose alternative is emplaced; its presence does not imply heap allocation.

`[expr.await]` considers the coroutine suspended before evaluating `await_suspend`.<sup>[1]</sup> An implementation may optimize generated code when observable behavior permits, but phase counting does not establish the resulting instruction or latency cost.

Standard-library sender types have additional implementation freedom. `[exec.snd.expos]/2` makes it unspecified whether a standard-library sender provides `sndr.as_awaitable(p)` and requires any such expression to meet `as_awaitable` semantics.<sup>[1]</sup> A conforming implementation can therefore give `inline-sender` a member that selects the first branch. Portable code cannot require that member.

The generic fallback connects before readiness, reports false readiness, starts from `await_suspend`, and completes through its receiver. Those statements describe branch 7.4 only.

## Three I/O Cases Locate the Boundary

Three I/O shapes separate a result known before suspension from completion discovered during initiation. The distinction prevents an eager fixture from standing in for every synchronous I/O operation.

### A result produced before the operation object returns

The smallest fixture performs an in-memory append before returning its awaitable or sender:

```cpp
auto write(std::string_view text)
{
    out_.append(text.data(), text.size());
    // Return an immediate awaitable or inline-completing sender.
}
```

This is hypothetical fixture code. It isolates consumption of an already-produced, value-less result. An immediate awaitable returns `true` from `await_ready`; an inline sender reports completion from `start`. If the sender reaches the generic fallback, the language still receives false readiness.

The fixture is intentionally narrow. The append occurs even when the returned operation object is discarded, so it does not represent the lazy execution convention of standard sender adaptors. Its result concerns protocol consumption after work has already happened.

### Completion discovered during initiation

Overlapped `WSARecv` supplies a sender-native mixed-completion example. Microsoft specifies that return zero means the operation completed immediately, while `SOCKET_ERROR` with `WSA_IO_PENDING` means successful initiation followed by later completion.<sup>[18]</sup> P2300R10 contains one `recv_sender` type whose `start` handles both outcomes.<sup>[3]</sup>

The sender protocol directly represents this operation. `start` calls `WSARecv`; immediate success calls `set_value`, while the operation state for a pending result persists until completion-port processing. P2300R10's immediate branch assumes `FILE_SKIP_COMPLETION_PORT_ON_SUCCESS`, which suppresses the completion-port entry that an immediate operation would ordinarily produce.<sup>[19]</sup> The operation result does not exist before initiation, so true pre-start readiness is unavailable.

An awaiter handles the same distinction from `await_suspend`. It initiates `WSARecv`, stores an immediate result when return zero is observed, then returns `false` or transfers directly to the continuation. For a pending result, the coroutine remains suspended. Both implementations need stable state and a race-safe handshake when completion can occur concurrently with initiation.

Socket readiness does not convert this case into pre-start completion. Microsoft warns that a readiness event can be followed by a receive returning `WSAEWOULDBLOCK`.<sup>[20]</sup> Readiness predicts whether initiation might complete; it is not the result of a particular receive.

### A user-space result ready in one instance and pending in another

A buffered stream supplies the pre-start case. One `read_some` object may find enough bytes in a user-space buffer, while another object of the same type must initiate an asynchronous receive. The cache-hit result can be copied and counted before suspension is considered.

The following illustrative projections share one operation implementation:

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

Both projections support ready and pending instances. The awaiter exposes the decision to `[expr.await]`; its cache-hit object proceeds directly to `await_resume`. The sender exposes the decision through the timing of receiver completion after `start`. When that sender reaches the generic bridge, `await_ready` remains false for both objects.

The three cases differ in when the result becomes available. A result produced before construction is an eager fixture, immediate system-call completion is discovered during initiation, and a user-space buffered result supports a genuine per-instance pre-start decision.

## Existing Alternatives Are Available but Non-Universal

The generic fallback is not the only coroutine path available to a sender. Current wording and published proposals provide multiple ways to select a different awaiter or describe completion behavior.

### A member can return a ready awaiter

The highest-priority `as_awaitable` branch invokes the expression's own member.<sup>[1]</sup> A `buffered_read_sender` can use that member to return the awaiter above. On a cache hit, no generic connection, receiver, operation state, or result variant is constructed for coroutine consumption.

The sender exposes both interfaces explicitly. Sender consumers use `connect` and `start`; coroutine consumers use the awaiter returned by `as_awaitable`. The two projections must agree on values, errors, stopped behavior, cancellation, environment, affinity, lifetime, and concurrency.

### Await-completion adaptation is preserved by ordinary unary composition

P3570R2 identified that a raw member on a leaf is unavailable after a sender adaptor changes the expression's type.<sup>[6]</sup> The working draft's response is `get_await_completion_adaptor`, a forwarding attribute query applied after domain transformation.<sup>[1]</sup> Standard unary parent senders forward forwarding attributes by default, so an await-completion adaptor can receive the transformed pipeline rather than only the original leaf.

A claim that every `then` necessarily discards await customization is no longer correct. Multi-child parents have empty attributes by default, behavior-changing adaptors may need a different policy, and user-defined wrappers preserve forwarding attributes only when their `get_env` participates in the convention.

### Domains can transform the whole expression

`transform_sender` gives completion and start domains the complete sender expression and recursively transforms the result when its type changes.<sup>[1]</sup> An I/O domain can therefore recognize a family of sender expressions and supply a common coroutine representation. This is broader than adding one member to each leaf type.

A transformation that recognizes `then`, `let_value`, or a multi-child operation must preserve the expression's value, error, stopped, environment, cancellation, affinity, and lifetime semantics. The domain centralizes that work without removing it.

### Completion behavior can be static or dynamic

P3206R0 proposes a sender attribute describing inline, synchronous, asynchronous, or unknown completion.<sup>[5]</sup> The proposal gives standard adaptors explicit combination rules and gives `split` a dynamic result after its shared operation has completed. It therefore demonstrates that an optional runtime attribute does not require a new member on every sender type.

Completion behavior alone does not produce a result. A consumer can use it to select state lifetime, synchronization, trampoline, or coroutine-transfer strategies. A true pre-start fast path still needs an awaiter or another rule that initiates the sender and stores its completion before `[expr.await]` proceeds to `await_resume`.

### Already-awaitable senders need no bridge

The sender concepts recognize qualifying awaitables as senders, and `as_awaitable` returns an expression that is already an awaiter before selecting `sender-awaitable`.<sup>[1]</sup> One type can therefore participate in both sets of concepts without passing through the generic fallback.

Existing customization paths can avoid the generic bridge, preserve await adaptation through ordinary unary composition, or specialize a whole domain. No current working-draft rule makes branch 7.4 itself inspect per-instance readiness.

## Capability Preservation Under Composition and Erasure

An optional capability matters only where the surrounding abstraction preserves it. Sender attributes, domain transformation, and configurable erased interfaces provide preservation mechanisms, but each boundary has a different rule.

### Composition needs semantic combination

A standard parent with one child forwards attributes whose queries opt into forwarding.<sup>[1]</sup> This rule preserves `get_await_completion_adaptor` across ordinary unary adaptors. A parent with multiple children has empty attributes by default, because selecting one child's await policy would not describe the combined operation.

P3206R0 specifies that `then` preserves predecessor behavior, `when_all` combines every child conservatively, `let_value` considers every sender the function may return, and `split` can change its answer after shared completion.<sup>[5]</sup> These are semantic rules, not mechanical forwarding.

User-defined adaptors follow the same preservation rule. A wrapper that follows the standard unary-parent attribute convention preserves forwarding queries. Adding an optional query does not give an existing wrapper with unrelated `get_env` behavior that preservation. Nonparticipating senders remain valid and use the fallback, so the compatibility effect is partial optimization coverage rather than source breakage.

### Erasure preserves a declared interface

A closed erased interface preserves the operations and queries it declares. Current stdexec parameterizes `any_sender` with a list of erased sender queries; the default list is empty.<sup>[21]</sup> An erased wrapper can include a completion-behavior query with a fixed signature. It does not automatically reproduce an arbitrary promise-dependent `as_awaitable` member from the hidden sender.

A fixed I/O eraser can expose its own outer `as_awaitable`. Capy's public benchmark code contains an erased read sender with both `connect` and `as_awaitable`, while its erased awaitable stream reserves concrete awaiter storage and forwards `await_ready` through a function table.<sup>[22]</sup> These examples establish that erasure itself does not erase readiness when readiness is part of the declared interface.

The fixed stream and a general erased sender solve different storage problems. A fixed stream is defined for one operation family and one result shape, with a storage policy fixed at wrapper construction. A general erased sender accepts compatible sender expressions whose receiver-dependent operation states may have different sizes and alignments.

### Operation state and allocation are independent

An operation state can be constructed in caller storage, in a coroutine frame, in an inline erasure buffer, in preallocated storage, or in storage acquired for that operation. Current stdexec requests an inline buffer for its erased operation state and allocates only when the concrete model does not fit its small-buffer criteria.<sup>[21]</sup> Constructing an operation state therefore does not imply allocating it.

An interface containing only sender connection and selected attributes cannot provide an awaiter projection that it omits. Semantic alignment is required when an interface contains both projections.

Attribute forwarding preserves compatible queries through ordinary unary boundaries, while behavior-changing composition and closed erasure require explicit semantics.

## Implementations Optimize Inline Completion Without Adding Readiness

Two public implementations show that false readiness does not determine generated cost. Their source structures retain sender connection and receiver completion while changing state lifetime and coroutine transfer.

### stdexec selects a statically inline awaiter

At NVIDIA/stdexec commit `2c56ffe7`, both the generic and statically inline sender awaiters return `false` from `await_ready()`.<sup>[21]</sup>

| Source property | Generic stdexec awaiter | Statically inline stdexec awaiter |
| --- | --- | --- |
| Selection | Completion behavior is not statically inline for every possible channel | Every possible channel is absent or reports inline completion |
| Stored before `await_suspend` | Connected operation state and thread-ID handshake | Sender |
| `connect` | Awaiter constructor | Local to `await_suspend` |
| `start` | `await_suspend` | `await_suspend` |
| Coordination | Atomic thread-ID exchange and cross-thread defense | No atomic handshake member |
| Transfer from `await_suspend` | Continuation or `noop_coroutine` | Selected continuation |

Table 3. The source-level differences between stdexec's generic and statically inline sender awaiters at commit `2c56ffe7`. The table describes code structure rather than optimizer output or latency.

The specialized path relies on completion behavior that establishes that the local operation state cannot outlive `await_suspend`. It then connects, starts, and returns the continuation. This removes the generic handshake without making readiness true, skipping the operation state, or bypassing receiver completion.

stdexec's deployed completion behavior is compile-time and per completion channel.<sup>[21]</sup> A missing query produces `unknown`; `just`, `just_error`, and `just_stopped` publish inline behavior. This implementation is narrower than P3206R0's dynamic `split` result.<sup>[5]</sup>

### Beman.Execution uses one guarded path

At Beman.Execution commit `a20a6f63`, `sender_awaitable` connects in its constructor, reports false readiness, starts in `await_suspend`, and coordinates completion with an atomic Boolean.<sup>[23]</sup> Inline completion causes `await_suspend` to return the continuation; pending completion returns `noop_coroutine` and later resumes the continuation.

Beman's `inline_scheduler` calls `set_value` directly from `start`, but its attributes do not report completion behavior at that revision.<sup>[23]</sup> On 2026-09-07, a complete snapshot at commit `a20a6f63` was scanned case-insensitively for `completion_behavior`, `completion behavior`, `completes_inline`, `any_sender`, and `any_receiver`; no match occurred. This search establishes exact token absence in that revision, not semantic absence under every possible name. The inline sender uses the same guarded awaiter.

### Source structure is not a performance measurement

The source establishes where connection and start occur, which state is stored, which abstract-machine atomics are present, and which coroutine handle is returned. It does not establish instruction counts, latency, cache effects, devirtualization, or whether a particular erased operation allocates.

Both implementations also avoid the working draft's direct nested `.resume()` for completion discovered during `start`. They return a continuation handle from `await_suspend`, providing symmetric transfer at the coroutine boundary. The protocol operation is symmetric transfer; a compiler may implement it as a tail transfer.

stdexec demonstrates a lower-state path for statically inline completion without demonstrating per-instance pre-start readiness in the generic fallback.

## Objections Define the Scope

The objections below separate sender execution from pre-start readiness, identify repairs the finding permits, and exclude consumers that never enter the coroutine bridge.

### "Senders already support synchronous I/O"

The working draft permits completion during `start`, `inline_scheduler` completes that way, and P2300R10's `recv_sender` handles immediate and pending `WSARecv` outcomes in one sender type.<sup>[1]</sup><sup>[3]</sup> Those mechanisms expose completion timing through a receiver. They do not give branch 7.4 a different answer to `await_ready`.

### "Immediate I/O completion is normally discovered only after initiation"

Immediate completion of overlapped `WSARecv` becomes known only during initiation.<sup>[18]</sup> An awaiter for that operation initiates from `await_suspend`, while a sender initiates from `start`. The pre-start advantage applies to higher-level user-space buffering and cached results, not to every operation that might complete immediately.

### "The generic bridge can be repaired without changing the sender concept"

stdexec's specialized awaiter moves connection into `await_suspend`, avoids the generic atomic handshake, and returns a continuation handle.<sup>[21]</sup> A working-draft change could adopt that structure without changing the base sender concept.

Such a repair addresses state lifetime, coordination, and transfer after false readiness. It does not add a query to the generic bridge for whether this sender object already contains a result. The distinction is semantic rather than a claim that the current bridge cannot improve.

### "P3206R0 can return runtime completion behavior"<sup>[5]</sup>

P3206R0 gives `split` a dynamic answer after shared completion and proposes combination rules for standard adaptors.<sup>[5]</sup> An optional query would leave existing senders valid and could provide incremental optimization wherever preserved.

P3206R0 describes when receiver completion occurs relative to `start`; it does not specify how a coroutine obtains a value when connection and receiver completion are skipped.<sup>[5]</sup> The proposed query is also absent from the current generic bridge. A future bridge could initiate from `await_ready` or select another awaiter, but that design would add wording beyond the adopted path.

### "Forwarding queries and domains avoid per-sender customization"

The await-completion adaptor query forwards through ordinary unary standard adaptors, and a domain can transform a complete expression before awaiter selection.<sup>[1]</sup><sup>[6]</sup> These facilities refute a claim that every concrete sender needs its own member.

Behavior-changing adaptors still need semantics for the transformed expression, multi-child parents need a combination policy, and closed erasure needs an interface entry. Centralizing the policy in a domain reduces duplication while retaining the translation boundary.

### "Every co_await operand becomes an awaiter"

Producing an awaiter is the required translation target, so the presence of an awaiter does not establish which native protocol an I/O API ought to expose. The relevant difference is whether the leaf already implements the language-facing readiness and extraction operations or reaches them after sender transformation, adaptation, connection, and receiver completion.

### "One operation can expose both sender and awaitable projections"

The member `as_awaitable` path, qualifying awaitables recognized as senders, and fixed dual-protocol erasure all support this design.<sup>[1]</sup><sup>[22]</sup> A dual projection can serve sender pipelines and coroutine consumers from one underlying operation implementation.

The design has a larger contract than either projection alone. Values, errors, cancellation, stopped behavior, affinity, environment, lifetime, and concurrency must remain equivalent across both public paths.

### "Protocol steps do not establish runtime overhead"

The stdexec specialization retains false readiness, connection, an operation state, `start`, receiver completion, and extraction while removing a synchronization protocol from its source.<sup>[21]</sup> Runtime claims require controlled measurements and generated-code inspection for the implementation and erasure boundary being discussed.

The normative evidence establishes wording requirements and observable control-flow rules; it does not establish runtime cost.

### "Pending operations need state in either model"

A pending `WSARecv` needs stable buffers, overlapped state, cancellation state, and a continuation.<sup>[18]</sup> A sender places those objects in an operation state; an awaiter can place equivalent objects in the coroutine frame or another stable owner. Neither model has a state advantage once the operation remains pending.

### "Skipping every suspension can harm fairness"

A long chain of ready operations can delay other work. An executor or I/O context may impose an inline-completion budget or scheduling boundary. That policy is independent of whether the leaf protocol can observe readiness; a ready path makes the decision available to the execution policy.

### "Sender-native consumers never pay for sender-to-awaitable translation"

A sender pipeline, direct receiver, scope, or `sync_wait` consumer never enters `as_awaitable`. Conversely, an awaitable leaf crossing into a sender pipeline needs an awaitable-to-sender bridge, and published bridge designs have their own continuation and storage requirements.<sup>[15]</sup><sup>[16]</sup>

Only coroutine-centric I/O leaves are covered. Sender-native work graphs are outside the comparison, and no leaf protocol is claimed to minimize every consumer's cost.

The objections narrow the comparison to coroutine-centric I/O with results available before initiation. Sender-native consumers and completion discovered only during initiation remain outside that boundary.

## Conclusion

Buffered I/O needs an object-specific decision before suspension. The awaiter interface exposes that decision through readiness, conditional initiation, and extraction. A sender-valued leaf first presents a graph-construction protocol, which `execution::task` translates before the language can consume it.

The sender model's graph, completion, ownership, environment, domain, and concurrency facilities remain available to sender-native consumers. At a coroutine leaf, the generic bridge reports false readiness for every instance.

The current wording provides concrete alternatives to the generic fallback. A member, forwarding await-completion adaptor, or domain transformation can supply another awaiter; P3206R0 sketches static and dynamic completion behavior;<sup>[5]</sup> a fixed erased interface can retain either facility when it declares it. Those mechanisms correct claims that customization is always per-leaf, that optional attributes are ineffective, or that erasure necessarily loses readiness. Behavior-changing composition needs combination rules, closed erasure needs an interface entry, and dual projections need one semantic contract.

Implementations can improve the false-ready path without adding readiness. stdexec moves connection and start into `await_suspend` for statically inline senders, removes its generic handshake, and returns the continuation.<sup>[21]</sup> Beman uses one guarded path.<sup>[23]</sup> These structures demonstrate that named protocol steps do not determine runtime cost.

On the stated criteria, direct implementation of the language-facing awaiter makes awaitables the natural leaf protocol for coroutine-centric I/O. A sender-valued interface introduces a second composition model before reaching the same language boundary, while its generic translation omits the object-specific pre-start decision. Sender pipelines can consume awaitable leaves through an explicit bridge when static graphs or sender-native concurrency are required. Designers of future networking libraries, task implementations, domains, and erased wrappers can use the boundary documented here to choose the primary protocol and its adapter.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[22]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[24]</sup>, coroutine-native I/O libraries under the C++ Alliance.

The paper records a finding about the protocol boundary used when coroutine-centric I/O returns sender-valued operations.

Capy and Corosio use awaitable-native I/O. The author advocates the awaitable-native model and has a professional interest in its adoption.

The comparison does not measure a complete networking framework. It does not rank sender-native consumers, and it presents no benchmark result. Awaitable leaves also require an adapter when consumed by a sender pipeline.

This paper belongs to the Network Endeavor series. Companion papers include P4003R3 on IoAwaitable,<sup>[13]</sup> P4092R1 and P4093R1 on both bridge directions,<sup>[14]</sup><sup>[15]</sup> P4126R1 on callback handles,<sup>[16]</sup> and P2583R4 on symmetric transfer through sender composition.<sup>[11]</sup>

The method compares public working-draft wording, published WG21 papers, official operating-system documentation, and source pinned to immutable public repository commits. No benchmark result is used.

The paper was drafted and revised with machine assistance under the author's direction. Every quotation and technical claim is subject to verification against the cited public source.

This paper asks for nothing.

## Acknowledgments

Eric Niebler, Lewis Baker, Kirk Shoop, and the P2300R10 authors specified the sender model and published the Windows receive example used to distinguish completion during initiation. Dietmar K&uuml;hl and Maikel Nadolski specified `execution::task` and its scheduler-affinity integration. Fabio Fracassi documented the composition problem that motivated the await-completion adaptor. Dalton M. Woodard and Maikel Nadolski developed the public completion-timing classifications examined here. Mungo Gill, Steve Gerbino, and Klemens Morgenstern developed the companion coroutine and bridge analyses.

## References

[1] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages &mdash; C++" (Thomas K&ouml;ppe, 2026).

[2] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[3] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&#322; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[4] [P2257R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2257r0.html) - "Blocking is an insufficient description for senders and receivers" (Dalton M. Woodard, 2020).

[5] [P3206R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3206r0.pdf) - "A sender query for completion behaviour" (Maikel Nadolski, 2025).

[6] [P3570R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3570r2.html) - "optional variants in sender/receiver" (Fabio Fracassi, 2025).

[7] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[8] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[9] [P0913R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0913r1.html) - "Add symmetric coroutine control transfer" (Gor Nishanov, 2018).

[10] [P1056R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1056r1.html) - "Add lazy coroutine (coroutine task) type" (Lewis Baker, Gor Nishanov, 2018).

[11] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).

[12] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of std::execution::task" (Jonathan M&uuml;ller, 2025).

[13] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[14] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[15] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[16] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[17] [P3149R11](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3149r11.html) - "`async_scope` &ndash; Creating scopes for non-sequential concurrency" (Ian Petersen, Jessica Wong, 2025).

[18] [WSARecv](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsarecv) - "WSARecv function (winsock2.h)" (Microsoft, 2018).

[19] [SetFileCompletionNotificationModes](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setfilecompletionnotificationmodes) - "SetFileCompletionNotificationModes function (winbase.h)" (Microsoft, 2018).

[20] [WSAEventSelect](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-wsaeventselect) - "WSAEventSelect function (winsock2.h)" (Microsoft, 2018).

[21] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec/tree/2c56ffe7f8a2b8b5221918159092be379ae8b40f) - "`std::execution` reference implementation" (NVIDIA, 2026).

[22] [Capy](https://github.com/cppalliance/capy) - "C++20 coroutine I/O foundation and sender benchmarks" (C++ Alliance, 2026).

[23] [Beman.Execution](https://github.com/bemanproject/execution/tree/a20a6f636be4e8d0588521670a178f342695ece8) - "`std::execution` implementation" (Beman Project, 2026).

[24] [Corosio](https://github.com/cppalliance/corosio) - "Coroutine-native networking library" (C++ Alliance, 2026).
