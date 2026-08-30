---
title: "Awaitables And Senders For Synchronous I/O"
document: P4255R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

C++20 awaitables and `std::execution` senders both express asynchronous operations consumed from coroutines through `co_await`. They differ in what happens when the operation completes synchronously - when the bytes are already in memory before `co_await` evaluates.

This paper implements the simplest possible synchronous write under both protocols, grants senders every affordance the standard provides, and traces the protocol steps that execute at the point of `co_await`. The comparison reveals a structural asymmetry in how the two protocols handle the synchronous case - and traces what the sender protocol would need to close it.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial revision.

---

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

The second mechanism is relinking: the same algorithm compiled once against a type-erased stream, with the execution model selected at link time. Where recompilation varies the template argument, relinking varies the object file behind a vtable.

The following illustrative algorithm compiles against a virtual base class:

```cpp
class write_stream
{
public:
    virtual ~write_stream() = default;
    virtual /* IoAwaitable */
        write(std::string_view sv) = 0;
};

task<> log_lines(write_stream& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

The algorithm's object code is fixed. It does not know whether the stream is synchronous or asynchronous. It does not need to know.

Link against an object file that provides `tcp_sink` behind the vtable. The algorithm is asynchronous.

Link against a different object file that provides `string_sink` behind the vtable. The algorithm is synchronous.

No recompilation. One indirect call per write. Zero allocation per write.

**The algorithm was compiled once. The execution model was chosen by the linker.**

## 4. What Senders Provide

Before examining the sender path for synchronous I/O, three genuine achievements of `std::execution` deserve recognition.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. This is a real property that coroutines do not match for multi-stage pipelines.<sup>[3]</sup>

**Compile-time work graphs.** The sender algebra encodes DAGs of work at the type level. `when_all`, `then`, `let_value` compose into a static structure the optimizer can see through. Domain customization via `transform_sender` retargets the same graph to CPU or GPU by swapping the scheduler.<sup>[4]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes.<sup>[3]</sup>

The comparison that follows grants senders every affordance: `inline_scheduler::schedule()` as the sender - the standard's own facility for inline completion<sup>[5]</sup> - synchronous completion inside `start`, and the minimal `completion_signatures<set_value_t()>`. P3552R3's `await_transform` bypasses the `affine_on` wrapping for this sender (`[task.promise]` p10), removing one step. The `sender-awaitable` path that remains is unavoidable; the sender protocol imposes it.

## 5. The Sender Path

Sections 2 and 3 showed the awaitable protocol's two mechanisms for synchronous I/O. This section traces the sender protocol's path for the same operation - a synchronous write to an in-memory string - using the best-case sender the standard provides.

`string_sink::write` returns the sender produced by `inline_scheduler::schedule()`, the exposition-only `inline-sender` type from P3552R3<sup>[5]</sup>:

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

The sender's `start` calls `set_value` on the receiver immediately. No kernel transition. No suspension on the sender side. This sender is the standard's own facility for inline completion - not a hand-rolled type, but the facility P3552R3 provides for exactly this case.

A coroutine returning `execution::task` consumes it:

```cpp
execution::task<> log_lines(
    string_sink& sink,
    std::span<std::string_view> lines)
{
    for (auto line : lines)
        co_await sink.write(line);
}
```

What happens inside `co_await sink.write(line)`, per the specification:

1. `await_transform` receives the sender.<sup>[5]</sup> The sender is an `inline-sender`. `[task.promise]` p10 detects this and bypasses `affine_on`, returning `as_awaitable(sndr, *this)` directly.

2. `as_awaitable` constructs a `sender-awaitable`.<sup>[3]</sup> `[exec.as.awaitable]`.

3. The `sender-awaitable` constructor calls `connect(sndr, awaitable-receiver)`.<sup>[3]</sup> The operation state is materialized. The receiver is wired.

4. `await_ready()` returns `false`.<sup>[3]</sup> Unconditionally. The coroutine suspends.

5. `await_suspend` calls `start(state)`.<sup>[3]</sup> Inside `start`, `set_value(receiver)` fires synchronously.

6. The receiver stores the result in a `variant` and calls `.resume()` on the coroutine handle.<sup>[3]</sup> The coroutine resumes.

7. `await_resume()` extracts the value from the `variant`.<sup>[3]</sup>

Seven protocol steps. One suspension and one resumption. One operation state construction. One receiver instantiation. One `variant` emplacement. No scheduler affinity check. For an operation that completes synchronously.

The `inline-sender` bypass in step 1 is type-specific: `await_transform` checks `same_as<remove_cvref_t<Sender>, inline-sender>`.<sup>[5]</sup> A user-defined sender that completes synchronously does not match this check and takes the full path, including `affine_on` wrapping<sup>[6]</sup> (P3941R2, "Scheduler Affinity," which specifies scheduler affinity enforcement for sender-based coroutines) - eight steps. Seven is the best case, achieved only by using the standard's own facility.

## 6. The Awaitable Path

The same operation traced through the awaitable protocol. Where Section 5 returned a sender from `write`, this section returns an IoAwaitable - a type satisfying the three-member protocol defined in P4003R4<sup>[7]</sup> (a minimal coroutine execution model that specifies executor affinity, stop-token propagation, and frame-allocator delivery for coroutines).

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

A coroutine returning a task type that satisfies the IoAwaitable protocol<sup>[7]</sup> consumes it:

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

1. `await_transform` delegates to `transform_awaitable`, which wraps the IoAwaitable in a `transform_awaiter`.<sup>[1]</sup>

2. `await_ready()` returns `true`. The coroutine does not suspend.

3. `await_resume()` returns.

Three protocol steps. No suspension, no operation state construction, no receiver instantiation, no `variant` emplacement, no scheduler affinity check.

## 7. Comparison

The following table summarizes the per-write protocol costs from Sections 5 and 6. Each row is a protocol mechanism that executes (or does not) during a single `co_await sink.write(line)` call on a synchronous `string_sink`.

| Property | Awaitable | Sender |
| --------------------------------- | --------- | ------ |
| Protocol steps per write | 3 | 7 |
| Coroutine suspensions | 0 | 1 |
| Coroutine resumptions | 0 | 1 |
| Operation state constructions | 0 | 1 |
| Receiver instantiations | 0 | 1 |
| `variant` emplacements | 0 | 1 |
| Scheduler affinity checks | 0 | 0 |
| Type erasure cost | 1 vtable call, 0 allocations | `any_sender`: 0-1 allocations |

## 8. Interoperation

The awaitable protocol and the sender protocol are not mutually exclusive. An IoAwaitable can be wrapped as a sender and consumed by sender pipelines, and a sender can be consumed from coroutine-native code without `execution::task`.

P4093R2<sup>[9]</sup> (awaitable-to-sender bridge) provides `as_sender`, which wraps any IoAwaitable as a `std::execution` sender:

```cpp
auto sndr = as_sender(sink.write(line))
    | ex::then([] { /* next step */ })
    | ex::upon_error(
        [](std::error_code ec) {
            // reachable
        });
```

The sender algebra works. `when_all` composes bridged IoAwaitables into parallel work. `let_value` sequences them. `upon_error` handles failures. The IoAwaitable is a leaf node in the sender's work graph. Structured concurrency is inherited from the sender pipeline.

Without callback handles, the bridge allocates one coroutine frame per bridged operation - the frame exists only to produce a `coroutine_handle<>`, the only type the awaitable protocol accepts. P4126R2<sup>[10]</sup> (callback handles for zero-cost bridging) shows this allocation is eliminable. A callback handle - three pointers matching the coroutine frame prefix, zero heap allocation - gives senders a `coroutine_handle<>` without allocating a frame.

The I/O layer is awaitable-native. Sender pipelines compose those awaitables into parallel work through the bridge. With P4126R2's callback handles, the bridge imposes no allocation.

## 9. The Case for Coroutine I/O

Section 8 shows IoAwaitables entering sender pipelines via `as_sender`.<sup>[9]</sup> P4092R2<sup>[11]</sup> (sender-to-awaitable bridge) shows senders consumed from coroutine-native code without `execution::task`. The bridge operates in both directions. P4088R2<sup>[12]</sup> (which documents the properties C++20 coroutines provide for stream I/O) examines the broader design fork between the two models.

The question is which implementation shape minimizes total cost when both consumers - coroutines and sender pipelines - exist.

| Consumer / I/O shape | Awaitable | Sender |
| -------------------- | --------- | ------ |
| **Coroutine** | | |
| Synchronous | Zero (no suspend) | 7-step protocol sequence (Section 5) |
| Asynchronous | Zero protocol overhead (inherent suspend only) | Inherent suspend + protocol sequence |
| **Sender pipeline** | | |
| Synchronous | Zero ([P4126R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r2.pdf)<sup>[10]</sup>) | Zero |
| Asynchronous | Zero ([P4126R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r2.pdf)<sup>[10]</sup>) | Zero |

The awaitable path imposes no protocol overhead in any cell. For synchronous I/O, the sender column carries the seven-step protocol sequence of Section 5. For asynchronous I/O, the sender protocol adds `connect`, receiver wiring, and `variant` emplacement atop the inherent suspend. These steps are not inherent to the async operation. They are inherent to the sender protocol.

For asynchronous I/O these added steps are a step count, not a separately observable runtime cost: once the operation suspends to a scheduler, the suspension dominates and the steps are not measurable above it. The case this paper isolates is synchronous completion, where no suspension absorbs them.

The sender pipeline cells in the awaitable column depend on P4126R2<sup>[10]</sup> callback handles. Without callback handles, senders consuming an awaitable allocate one coroutine frame per operation. Two of the awaitable column's four zeros require [P4126R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r2.pdf).

## 10. Composed I/O

Composed I/O algorithms call lower-level operations in a loop. This section examines how the protocol cost from Sections 5-7 multiplies across layered I/O stacks - the dominant pattern in protocol implementations such as TLS, HTTP, WebSocket, SMTP, and DNS resolution.

`read` fills a buffer by looping `read_some`. TLS decrypts by looping encrypted reads. HTTP sequences header parsing with body reads. Each layer is a coroutine composing awaitables. These algorithms are generic - constrained on concepts, agnostic to execution context.

Under the sender protocol, each iteration of such a loop executes the protocol sequence of Section 5 independently - even when the operation completes synchronously. Each synchronous completion constructs an operation state, instantiates a receiver, suspends the coroutine, calls `start`, fires `set_value` on the receiver, emplaces the result into a `variant`, and resumes the coroutine. For a 64 KB read with a 4 KB kernel buffer, this is sixteen iterations. On a buffered stream where most completions are synchronous, that is sixteen operation states, sixteen receivers, sixteen suspensions, sixteen resumptions - for data already in user-space memory.

The sender model's construction-before-launch separation is a strength during pipeline building: aggregate state, let the optimizer see the full graph. Inside a composed I/O loop, the pipeline is already built and running. The protocol steps that serve construction-phase visibility persist into execution where they are no longer needed.

If the protocol can detect that the result is already available, the coroutine need not suspend. The suspension and resumption disappear. If the protocol can skip connection when the result is available, the operation state and the receiver disappear - the machinery that shuttles a value across a suspension boundary ceases to exist when no boundary exists. If the protocol expresses readiness through a single boolean - true: the value is here, take it directly; false: the value requires work, suspend, resume when ready - both cases are handled through one mechanism.

This is `await_ready`.

The following algorithm is representative of composed I/O as implemented in Capy<sup>[1]</sup>. It composes `read_some` into `read` through `co_await`; the result is itself awaitable, and TLS composes `read`, and HTTP composes TLS:

```cpp
template <typename S, typename MB>
  requires ReadStream<S> && MutableBufferSequence<MB>
auto
read(S& stream, MB buffers) ->
        io_task<std::size_t>
{
    auto consuming = buffer_slice(buffers);
    std::size_t const total_size =
        buffer_size(buffers);
    std::size_t total_read = 0;

    while(total_read < total_size)
    {
        auto [ec, n] = co_await stream.read_some(
            consuming.data());
        consuming.remove_prefix(n);
        total_read += n;
        if(ec)
            co_return {ec, total_read};
    }

    co_return {{}, total_read};
}
```

Composition nests without sender algebra. When `read_some` completes synchronously, no allocation occurs, no operation state is constructed, no receiver is wired; the protocol adds nothing to what the hardware delivers. The requirement surface at each `co_await` is three members: `await_ready`, `await_suspend`, `await_resume`. The protocol is conditionally lazy: `await_ready() == false` defers, `await_ready() == true` proceeds. The concept constraint defines the interface, the awaitable defines execution semantics, the coroutine body defines composition logic - three concerns, no coupling. The algorithm accepts any type satisfying `ReadStream`, works across execution contexts without recompilation or runtime overhead, and imposes minimal requirements on user types. The coroutine frame outlives every `co_await` within it; activations nest, RAII works, cancellation propagates downward.

When the stream is synchronous, the loop runs without suspension - `await_ready()` returns `true` at every iteration, no scheduler is consulted, no operation state is constructed, and the generic algorithm has the same cost as a hand-written `while` loop calling `memcpy`.

Stepanov's iterator concepts do not impose indirection when dereferencing a pointer. A `T*` satisfies `random_access_iterator` and dereferences in one instruction. The concept does not require constructing an intermediate state object, wiring a callback, or performing a two-phase access protocol - even though some iterators require all of those internally. The cost is proportional to what the underlying data access requires.

The awaitable protocol has this property. `await_ready() == true` is the pointer dereference: the value is there, take it. `await_ready() == false` is the disk-backed iterator: the value requires work, suspend, resume when ready. The cost tracks the operation, not the protocol.

## 11. Closing The Gap

The desire for immediately-ready asynchronous facilities is not new. [P0159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0159r0.html)<sup>[13]</sup> (2015) proposed `make_ready_future` specifically to avoid suspension when the result is already available - the same concern documented in Sections 5-7 of this paper. The sender model did not overlook the synchronous case. It did not optimize for it, and its architecture does not allow optimizing for it - even inside a running pipeline where the construction-before-launch property that motivates the design is no longer needed.

The sender model, as specified, does not match the awaitable model for synchronous I/O through the generic `sender-awaitable` path that every sender inherits. A concrete sender can sidestep that path by providing its own member `as_awaitable`<sup>[3]</sup> - a manual customization that is lost under type erasure. The modifications below are what would lift the costs from the generic protocol itself, for every sender, including type-erased senders. Each modification addresses one layer of the gap; together they trace the full distance between the two protocols.

### 11.1. A Readiness Query

`sender-awaitable::await_ready()` returns `false` unconditionally.<sup>[3]</sup><sup>[8]</sup> To skip suspension for senders that complete synchronously, a readiness query is required. The sender must advertise, at compile time or at run time, that its `start` will call `set_value` before returning.

P3552R3<sup>[5]</sup>'s `await_transform` does bypass `affine_on` for `inline-sender` (Section 5, step 1). It does not bypass the `sender-awaitable` path. The six steps that follow - `connect`, `await_ready() == false`, suspension, `start`, resumption, `await_resume` - execute regardless.

To skip that path, a readiness query is required. A trait, a tag, or a constexpr query.

### 11.2. Conditional Suspension

With a readiness query in place, `sender-awaitable::await_ready()` can return `true` when the sender advertises synchronous completion. The coroutine no longer suspends.

But `connect` was already called in the `sender-awaitable` constructor.<sup>[3]</sup> The operation state was already materialized. The receiver was already wired. The `variant` was already allocated. The suspension was saved. The remaining protocol steps were not.

### 11.3. Deferred Connection

To skip those steps, `connect` must be moved from the `sender-awaitable` constructor into `await_suspend`, where it can be bypassed when `await_ready()` returns `true`.

But the value needs to come from somewhere. `await_resume` must return the result. If `connect` and `start` did not execute, no receiver received the value. The sender needs a second value-delivery mechanism - a `get_value()` member, a direct extraction path, a way to produce the result without constructing an operation state, wiring a receiver, calling `start`, routing through `set_value`, and emplacing into a `variant`.

The sender model then carries two value-delivery mechanisms: channels for asynchronous completion, direct extraction for synchronous completion.

### 11.4. Conditional Affinity Wrapping

`await_transform` wraps every sender that does not customize `as_awaitable` in `affine` to enforce scheduler affinity.<sup>[5]</sup> For a sender that completes synchronously - whose bytes are already in the string before `co_await` evaluates - the affinity check serves no purpose.

P3552R3<sup>[5]</sup> already provides conditional affinity wrapping: `[task.promise]` p10 checks `same_as<remove_cvref_t<Sender>, inline-sender>` and bypasses `affine_on` when the sender is the exposition-only type returned by `inline_scheduler::schedule()`. The mechanism is a type check for one specific sender, not a general protocol query. A user-defined sender that completes synchronously cannot opt into this bypass. The awaitable protocol handles this generically: `await_ready()` is evaluated on every awaitable, and any awaitable can return `true`.

Generalizing the type check into a concept - any sender that declares inline completion behavior - is straightforward. But the concept only solves affinity wrapping. It does not reach the `sender-awaitable` path of Sections 11.1-11.3: `await_ready()` still returns `false`, the coroutine still suspends, and the operation state is still constructed.

### 11.5. Zero-Allocation Type Erasure

`any_sender::connect` produces a type-erased operation state whose size is unknown at compile time. The current implementations use small-buffer optimization (64 bytes in stdexec) or heap allocation.<sup>[3]</sup> The per-operation cost is zero or one allocation.

Measured in the Capy benchmark suite<sup>[1]</sup> (`bench/beman`) on a type-erased no-op read, single thread, 20,000,000 operations per cell, clang 22.1.5 release build: the type-erased awaitable consumed by a coroutine allocates zero times per operation; the type-erased `any_sender` consumed by a coroutine allocates once. Wall-clock was 37 ns per operation for the awaitable and 55 ns for the sender; that figure spans two coroutine frameworks and is reported for context, while the allocation count is the structural result.

The awaitable model's type erasure is one virtual function call and zero allocations. To match this, the sender needs a base class with a virtual function that returns the value directly - without constructing an operation state, without wiring a receiver, without calling `start`.

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

    // 11.4: completion-behavior tag
    static constexpr auto       // cf. !await_suspend()
        completion_behavior =
        completion_behavior_t::always_inline;

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

Each modification in the sender column has a direct counterpart in the awaitable's three members. The sender protocol arrives at a readiness query (`is_synchronous` maps to `await_ready`), a direct extraction path (`get_value` maps to `await_resume`), a completion-behavior tag (maps to `await_suspend` returning without scheduling), and virtual dispatch for type erasure (maps to a virtual `await_resume`). Four mechanisms. Three members.

## 12. Concerns

**"P4126R2 is unshipped. The bridge cost is hypothetical."** Two of the awaitable column's four zeros in Section 9 depend on P4126R2.<sup>[10]</sup> The dependency is real. It is an argument for collaboration. Callback handles would allow sender pipelines to consume awaitables for free. The core finding (Sections 5-7) rests on normative text; the bridge zeros are the prize collaboration unlocks.

**"A sender can provide a member `as_awaitable` and skip the protocol sequence. No protocol change is needed."** True. `[exec.as.awaitable]` uses a sender's own `as_awaitable` when the sender provides one, in preference to constructing the generic `sender-awaitable`:<sup>[3]</sup>

```cpp
// [exec.as.awaitable], reduced to the relevant branch
template<class Expr, class Promise>
decltype(auto) as_awaitable(Expr&& e, Promise& p)
{
    if constexpr (requires { e.as_awaitable(p); })
        return e.as_awaitable(p);        // the sender's own awaitable
    else
        return sender-awaitable{e, p};   // the seven steps of Section 5
}
```

In `execution::task`, `await_transform` makes this same check before it wraps anything in `affine`: a sender that provides `as_awaitable` is used directly, so the affinity wrap is skipped as well.<sup>[5]</sup> A sender whose `as_awaitable` returns a synchronous awaitable then takes the path of Section 6. `connect`, the receiver, `start`, the `variant`, and the affinity wrap are never instantiated. Three protocol steps, not seven.

A separate mechanism exists for `inline-sender` specifically: `[task.promise]` p10 checks `same_as<remove_cvref_t<Sender>, inline-sender>` and bypasses `affine_on`, but not `sender-awaitable`. This is a type check in `await_transform`, not a sender-provided customization. Both mechanisms are per-sender; both are lost under type erasure.

The synchronous fast path the sender reaches through `as_awaitable` is an awaitable: the sender hands one back, and the awaitable does the work. Closing the gap for one concrete sender, awaited from a coroutine, is one existing customization point returning the three-member struct of Section 6.

Two costs remain. The `as_awaitable` member is manual and per-sender; a sender that omits it inherits the seven-step path. And it is lost under type erasure: `any_sender` erases the concrete sender and the member with it, and `any_sender::connect` materializes the operation state of Section 11.5. Type erasure is the one sender-specific cost no `as_awaitable` member reaches.

The scope is the coroutine consumer. A sender pipeline never enters `as_awaitable`; Section 9 records zero for both synchronous pipeline cells.

**"The protocol cannot know at compile time whether a given co_await will always complete synchronously. The operation state must be constructed because the protocol must handle the general case."** The awaitable protocol handles this case exactly. `await_ready()` is evaluated at runtime: if the result is available, return `true` - no suspension; if work is required, return `false` - suspend. The protocol does not need compile-time knowledge. It asks the operation at the point of evaluation. For senders that are always synchronous (like `inline-sender`), the property is known at compile time - a constexpr trait could express it. The sender model has no such trait; Section 11.1 describes one. The "cannot know" argument applies equally to awaitables, yet an awaitable whose `await_ready()` depends on runtime state handles both cases through the same three-member protocol: when ready, no suspension, no operation state, no receiver; when not ready, suspend, resume when ready. One protocol, two behaviors, selected at the point of evaluation.

**"The optimizer eliminates the protocol overhead."** The suspension is observable behavior independent of optimization. When `await_ready()` returns `false`, the coroutine suspends and other coroutines in the executor's queue may run. The scheduling interleave is a behavioral property that `std::execution::task` already ships. A conforming implementation cannot return `true` from `sender-awaitable::await_ready()` when `[exec.as.awaitable]` specifies `false`.<sup>[3]</sup> An implementation that does so is non-conforming. An implementation that wishes to do so requires a specification change - which is Section 11.1.

**"Operation state construction delivers structured concurrency guarantees."** Genuine for asynchronous operations where the coroutine suspends and work executes concurrently. For a synchronous write where the data is in the string before `co_await` evaluates, there is no concurrent lifetime to manage. The operation state guarantees a property that was never at risk.

**"Protocol step counts are not runtime costs."** True for `connect`, `start`, and `set_value` when sender and receiver are fully visible to the optimizer and the optimizer is sufficiently aggressive. Not true for the suspension/resumption pair, which remains observable regardless of inlining. Not true across type-erasure boundaries, where `any_sender::connect` materializes an operation state the compiler cannot see through.

**"Awaitables don't compose into work graphs."** They do, through the bridge. Section 8 shows IoAwaitables consumed by sender pipelines via `as_sender`.<sup>[9]</sup> The sender algebra - `when_all`, `let_value`, `upon_error` - works. The bridge cost is eliminable with P4126R2.<sup>[10]</sup>

**"Unconditional suspension is the sound default."** The awaitable protocol solved this in C++20 with a single boolean. `await_ready()` provides the override. The sender protocol has no equivalent conditional path.

**"The composed algorithm is sequential - real composition requires parallelism."** Sequential composition over a single stream is expressed as a coroutine loop. Parallel composition across multiple streams - scatter-gather, concurrent requests, fan-out/fan-in - is expressed through the sender algebra via the bridge of Section 8. Sequential I/O composition is the dominant pattern in protocol implementations (TLS, HTTP, WebSocket, SMTP, DNS resolution). Each layer is a coroutine composing awaitables, and each inner await that completes synchronously executes the protocol sequence independently under the sender protocol. The multiplier is proportional to the protocol's depth: HTTP over TLS over TCP is three layers of composed coroutines, each with its own `read_some` loop, each iteration paying independently.

**"The composed read loop has no cancellation propagation."** Stop tokens propagate transparently through `io_env` - the execution environment bundle passed to every IoAwaitable via `await_suspend(coroutine_handle<>, io_env const*)`.<sup>[7]</sup> Each child operation inherits the caller's stop token without explicit wiring. Every stream operation observes the stop token and may complete early with an operation-cancelled error. The mechanism is defined in P4003R4<sup>[7]</sup>.

**"The bridge concedes the dependency."** The bridge operates in both directions. P4093R2<sup>[9]</sup> bridges IoAwaitables into sender pipelines. P4092R2<sup>[11]</sup> bridges senders into coroutine-native code without `execution::task`. Section 9 shows the cost is asymmetric: if I/O is an awaitable, both consumers pay zero; if I/O is a sender, coroutines pay the protocol overhead.

**"The comparison measures the wrong case."** Synchronous completion is not a corner case in I/O. Buffered writes, cached reads, DNS cache hits, and in-memory operations complete synchronously. A protocol that penalizes the common fast path compounds the cost across thousands of operations per connection.

**"Senders retarget via scheduler swap; awaitables require recompilation."** Section 3 demonstrates retargeting by relinking. One vtable call, zero allocations. The linker swaps the object file.

**"The modifications in Section 11 are natural evolution."** Each modification introduces a new mechanism: a readiness query, a second value-delivery path, conditional affinity wrapping, virtual dispatch for type erasure. The awaitable protocol provides the same capability with three members.

**"The type erasure comparison is asymmetric."** Both paths use type erasure at the same boundary. The awaitable path produces one indirect call and zero allocations. `any_sender::connect` materializes an operation state the compiler cannot see through.

**"The falsification criteria measure senders on the awaitable's home turf."** The paper says so in the Disclosure: "Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation." Section 4 credits senders with three achievements awaitables do not match. Section 9 covers both synchronous and asynchronous I/O. The falsification criteria are scoped to the paper's claim: synchronous I/O protocol cost.

## 13. Falsification

The observations documented in this paper would be discharged if any of the following were demonstrated:

- A sender protocol mechanism, equivalent to `await_ready`, that skips `connect` and `start` for trivially-ready senders without introducing a second value-delivery path.

- A `sender-awaitable` implementation in which `await_ready()` returns `true` when the sender is known to complete synchronously, without requiring `connect` to have already executed.

- A type-erasure mechanism for senders that achieves virtual-dispatch cost - one indirect call, zero allocation per operation - without reintroducing virtual dispatch.

## 14. Conclusion

The synchronous write traces three protocol steps under awaitables and seven under senders. The gap is structural: the sender protocol's generic `sender-awaitable` path returns `false` from `await_ready()` unconditionally, constructs an operation state and receiver for every invocation, and suspends and resumes the coroutine even when the result is already in memory. Closing the gap requires the sender protocol to acquire a readiness query, a direct value-extraction path, conditional affinity wrapping, and virtual dispatch for type erasure - four mechanisms that map, one to one, onto the awaitable's three members.

Synchronous completion is not a corner case. Buffered writes, cached reads, DNS cache hits, and in-memory operations complete synchronously. Composed I/O algorithms - `read` looping `read_some`, TLS looping encrypted reads, HTTP sequencing headers and bodies - pay the per-operation cost at every iteration that completes without suspending. The multiplier is proportional to the protocol stack's depth.

The two protocols interoperate. IoAwaitables enter sender pipelines through `as_sender`;<sup>[9]</sup> senders enter coroutine-native code through `await_sender`.<sup>[11]</sup> P4126R2's callback handles<sup>[10]</sup> eliminate the bridge's allocation cost. If I/O primitives are awaitables, both coroutine consumers and sender-pipeline consumers pay zero protocol overhead. If I/O primitives are senders, coroutine consumers pay the protocol overhead.

A protocol that cannot express "the result is already here" will always pay to shuttle the result across a suspension boundary that the synchronous case does not require.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, coroutine-native I/O libraries under the C++ Alliance.

This paper documents the protocol-level cost difference between awaitables and senders when I/O operations complete synchronously.

Capy and Corosio implement I/O using the coroutine-native model. They compete with sender-based networking frameworks. The author advocates for the coroutine-native model. The sender model is the competing paradigm examined in this paper. The author has a stake in the coroutine model's adoption.

This paper belongs to the Network Endeavor series. Companion papers in the series include P4003R4<sup>[7]</sup> (the IoAwaitable protocol), P4088R2<sup>[12]</sup> (coroutine advantages for stream I/O), P4093R2<sup>[9]</sup> (awaitable-to-sender bridge), P4092R2<sup>[11]</sup> (sender-to-awaitable bridge), P4126R2<sup>[10]</sup> (callback handles for zero-cost bridging), and P2583R5<sup>[8]</sup> (symmetric transfer in sender pipelines).

This paper asks for nothing.

## Acknowledgements

Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators for `std::execution` and the sender algebra. Dietmar K&uuml;hl and Maikel Nadolski for [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) (`std::execution::task`). Dietmar K&uuml;hl for dismissing an earlier draft and remarking that the sender example was wrong. Investigating that remark led to a closer reading of P3552R3's `await_transform` and the discovery of the `inline-sender` bypass, which informed improvements throughout the paper that strengthened its argument. Robert Leahy for the AIO-to-sender bridge and [P2583R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r5.pdf) (symmetric transfer).

## References

[1] [Capy](https://github.com/cppalliance/capy) (C++ Alliance).

[2] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance).

[3] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, 2024).

[4] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution` (NVIDIA, 2024).

[5] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[6] [P3941R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r2.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[7] [P4003R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r4.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, 2026).

[8] [P2583R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r5.pdf) - "Symmetric Transfer and Sender Composition" (Vinnie Falco, 2026).

[9] [P4093R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r2.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[10] [P4126R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r2.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[11] [P4092R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r2.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[12] [P4088R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r2.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[13] [P0159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0159r0.html) - "Draft of Technical Specification for C++ Extensions for Concurrency" (Artur Laksberg, 2015). Section "futures.make_ready_future" documents the need for immediately-ready asynchronous facilities.
