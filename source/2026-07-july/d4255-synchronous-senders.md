---
title: "Awaitables And Senders For Synchronous I/O"
document: P4255R0
date: 2026-07-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The awaitable protocol handles synchronous I/O at zero cost. The sender protocol does not.

C++20 awaitables provide two mechanisms for synchronous I/O: recompilation (swap the awaitable type, the algorithm goes from async to sync) and relinking (compile once against a type-erased stream, swap the object file). Both work today. This paper implements the simplest possible synchronous write operation under both models, grants senders every affordance, and sets the two implementations side by side.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial revision.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the coroutine model's adoption.

Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation.

This paper asks for nothing.

## 2. The Abstraction

A synchronous write stream has one operation: accept a string and store it. No error codes, no byte counts, no partial writes. Two concrete types implement it.

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

## 3. Recompilation

A generic algorithm written as a coroutine template:

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

## 4. Relinking

The same algorithm compiled once against a type-erased stream:

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

## 5. What Senders Provide

Before examining the sender path for synchronous I/O, three genuine achievements of `std::execution` deserve recognition.

**Zero-allocation composition.** Sender pipelines collapse into a single `operation_state` at compile time. No heap allocation, no virtual dispatch, no reference counting. This is a real property that coroutines do not match for multi-stage pipelines.<sup>[3]</sup>

**Compile-time work graphs.** The sender algebra encodes DAGs of work at the type level. `when_all`, `then`, `let_value` compose into a static structure the optimizer can see through. Domain customization via `transform_sender` retargets the same graph to CPU or GPU by swapping the scheduler.<sup>[4]</sup>

**Structured concurrency.** `counting_scope` tracks dynamically spawned work and prevents scope destruction until all work completes.<sup>[3]</sup>

The comparison that follows grants senders every affordance: `inline_scheduler` as the completion scheduler, synchronous completion inside `start`, and the minimal `completion_signatures<set_value_t()>`.

## 6. The Sender Path

`string_sink::write` returns a sender:

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
        return write_sender{};
    }

private:
    struct write_sender
    {
        using sender_concept =
            std::execution::sender_t;
        using completion_signatures =
            std::execution::completion_signatures<
                std::execution::set_value_t()>;

        template<class Receiver>
        struct state
        {
            using operation_state_concept =
                std::execution::
                    operation_state_t;
            Receiver rcvr_;

            void start() & noexcept
            {
                std::execution::set_value(
                    std::move(rcvr_));
            }
        };

        template<class Receiver>
        state<std::decay_t<Receiver>>
            connect(Receiver&& rcvr) const
        {
            return {std::forward<Receiver>(
                rcvr)};
        }
    };
};
```

The sender completes synchronously. `start` calls `set_value` on the receiver immediately. No kernel transition. No suspension on the sender side. This is the most favorable implementation possible.

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

1. `await_transform` receives the sender.<sup>[5]</sup> The promise type's `await_transform` is constrained to `sender`.<sup>[5]</sup> `[task.promise]` p10.

2. The sender is wrapped with `affine`.<sup>[6]</sup> `[exec.affine.on]`. `await_transform` checks for a member `as_awaitable` first; this sender provides none, so it takes the wrapping branch.<sup>[5]</sup>

3. `as_awaitable` constructs a `sender-awaitable`.<sup>[3]</sup> `[exec.as.awaitable]`.

4. The `sender-awaitable` constructor calls `connect(sndr, awaitable-receiver)`.<sup>[3]</sup> The operation state is materialized. The receiver is wired.

5. `await_ready()` returns `false`.<sup>[3]</sup> Unconditionally. The coroutine suspends.

6. `await_suspend` calls `start(state)`.<sup>[3]</sup> Inside `start`, `set_value(receiver)` fires synchronously.

7. The receiver stores the result in a `variant` and calls `.resume()` on the coroutine handle.<sup>[3]</sup> The coroutine resumes.

8. `await_resume()` extracts the value from the `variant`.<sup>[3]</sup>

Eight protocol steps. One suspension and one resumption. One operation state construction. One receiver instantiation. One `variant` emplacement. One scheduler affinity check. To append bytes to a string.

## 7. The Awaitable Path

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

Three protocol steps. No suspension. No operation state. No receiver. No `variant`. No scheduler affinity check. The bytes were appended to the string.

## 8. Comparison

| Property | Awaitable | Sender |
| --------------------------------- | --------- | ------ |
| Protocol steps per write | 3 | 8 |
| Coroutine suspensions | 0 | 1 |
| Coroutine resumptions | 0 | 1 |
| Operation state constructions | 0 | 1 |
| Receiver instantiations | 0 | 1 |
| `variant` emplacements | 0 | 1 |
| Scheduler affinity checks | 0 | 1 |
| Type erasure cost | 1 vtable call, 0 allocations | `any_sender`: 0-1 allocations |

## 9. Interoperation

The awaitable protocol and the sender protocol are not mutually exclusive. An IoAwaitable can be wrapped as a sender and consumed by sender pipelines.

[P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[9]</sup> provides `as_sender`, which wraps any IoAwaitable as a `std::execution` sender:

```cpp
auto sndr = as_sender(sink.write(line))
    | ex::then([] { /* next step */ })
    | ex::upon_error(
        [](std::error_code ec) {
            // reachable
        });
```

The sender algebra works. `when_all` composes bridged IoAwaitables into parallel work. `let_value` sequences them. `upon_error` handles failures. The IoAwaitable is a leaf node in the sender's work graph. Structured concurrency is inherited from the sender pipeline.

Without callback handles, the bridge allocates one coroutine frame per bridged operation - the frame exists only to produce a `coroutine_handle<>`, the only type the awaitable protocol accepts. [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf)<sup>[10]</sup> shows this allocation is eliminable. A callback handle - three pointers matching the coroutine frame prefix, zero heap allocation - gives senders a `coroutine_handle<>` without allocating a frame. The bridge cost drops to zero.

IoAwaitables own the I/O layer. Sender pipelines own the composition layer. The bridge connects them. With callback handles, the bridge is free.

## 10. The Case for Coroutine I/O

Section 9 shows IoAwaitables entering sender pipelines via `as_sender`.<sup>[9]</sup> [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[11]</sup> shows senders consumed from coroutine-native code without `execution::task`. The bridge goes both ways. The broader design fork is documented in [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf).<sup>[12]</sup>

The question is not which model is more powerful. It is which implementation shape minimizes total cost when both consumers exist.

| Consumer / I/O shape | Awaitable | Sender |
| -------------------- | --------- | ------ |
| **Coroutine** | | |
| Synchronous | Zero (no suspend) | 8-step ceremony (Section 6) |
| Asynchronous | Zero protocol overhead (inherent suspend only) | Inherent suspend + ceremony |
| **Sender pipeline** | | |
| Synchronous | Zero (P4126R1)<sup>[10]</sup> | Zero |
| Asynchronous | Zero (P4126R1)<sup>[10]</sup> | Zero |

The awaitable column is four zeros. For synchronous I/O, the sender column carries the full eight-step ceremony of Section 6. For asynchronous I/O, the sender protocol adds ceremony - `connect`, receiver wiring, `variant` emplacement, affinity wrapping - atop the inherent suspend. The ceremony is not inherent to the async operation. It is inherent to the sender protocol.

The sender pipeline cells in the awaitable column depend on P4126R1<sup>[10]</sup> callback handles. Without callback handles, senders consuming an awaitable allocate one coroutine frame per operation. Two of the awaitable column's four zeros require P4126R1.

The awaitable is the implementation shape where neither consumer pays a protocol tax.

## 11. Closing The Gap

The sender model, as specified, does not match the awaitable model for synchronous I/O through the generic `sender-awaitable` path that every sender inherits. A concrete sender can sidestep that path by hand, by providing its own member `as_awaitable`,<sup>[3]</sup> a manual customization that is lost under type erasure. The modifications below are what would lift the costs from the generic protocol itself, for every sender, type-erased included. Each is presented in order.

### 11.1. A Readiness Query

`sender-awaitable::await_ready()` returns `false` unconditionally.<sup>[3]</sup><sup>[8]</sup> To skip suspension for senders that complete synchronously, a readiness query is required. The sender must advertise, at compile time or at run time, that its `start` will call `set_value` before returning.

P3552R3's `await_transform` could detect synchronous senders before they enter `as_awaitable` and bypass the `sender-awaitable` path entirely. It does not.

This requires a new concept requirement on senders. A trait, a tag, or a constexpr query. The sender model now has a readiness query.

### 11.2. Conditional Suspension

With the readiness query in place, `sender-awaitable::await_ready()` returns `true` when the sender advertises synchronous completion. The coroutine no longer suspends.

But `connect` was already called in the `sender-awaitable` constructor.<sup>[3]</sup> The operation state was already materialized. The receiver was already wired. The `variant` was already allocated. The suspension was saved. The ceremony was not.

### 11.3. Deferred Connection

To skip the ceremony, `connect` must be moved from the `sender-awaitable` constructor into `await_suspend`, where it can be bypassed when `await_ready()` returns `true`.

But the value needs to come from somewhere. `await_resume` must return the result. If `connect` and `start` did not execute, no receiver received the value. The sender needs a second value-delivery mechanism - a `get_value()` member, a direct extraction path, a way to produce the result without constructing an operation state, wiring a receiver, calling `start`, routing through `set_value`, and emplacing into a `variant`.

The sender model now has two value-delivery mechanisms: channels for asynchronous completion, direct extraction for synchronous completion.

### 11.4. Conditional Affinity Wrapping

`await_transform` wraps every sender that does not customize `as_awaitable` in `affine` to enforce scheduler affinity.<sup>[5]</sup> For a sender that completes synchronously - whose bytes are already in the string before `co_await` evaluates - the affinity check serves no purpose.

[P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[5]</sup> contemplates detecting `inline_scheduler` in `await_transform` and bypassing the wrap. But the detection is type-based. Custom senders that complete synchronously need to opt in via the readiness query from Section 11.1 or a new completion-behavior tag.

The sender model now carries a readiness query, a direct extraction path, two value-delivery mechanisms, and conditional affinity wrapping.

### 11.5. Zero-Allocation Type Erasure

`any_sender::connect` produces a type-erased operation state whose size is unknown at compile time. The current implementations use small-buffer optimization (64 bytes in stdexec) or heap allocation.<sup>[3]</sup> The per-operation cost is 0-1 allocations.

The awaitable model's type erasure is one virtual function call and zero allocations. To match this, the sender needs a base class with a virtual function that returns the value directly - without constructing an operation state, without wiring a receiver, without calling `start`.

The sender model now has virtual dispatch.

### 11.6. The Result

The sender model, modified to match the awaitable model for synchronous I/O:

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

The awaitable:

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

## 12. Concerns

**"The comparison measures the wrong case."** Synchronous completion is not a corner case in I/O. Buffered writes, cached reads, DNS cache hits, and in-memory operations complete synchronously. A protocol that penalizes the common fast path compounds the cost across thousands of operations per connection.

**"The optimizer eliminates the ceremony."** The suspension/resumption pair is observable behavior. `sender-awaitable::await_ready()` returns `false` unconditionally per `[exec.as.awaitable]`.<sup>[3]</sup> The optimizer cannot elide a coroutine suspend/resume across a type-erased boundary.

**"Awaitables don't compose into work graphs."** They do, through the bridge. Section 9 shows IoAwaitables consumed by sender pipelines via `as_sender`.<sup>[9]</sup> The sender algebra - `when_all`, `let_value`, `upon_error` - works. The bridge cost is eliminable.<sup>[10]</sup>

**"The modifications in Section 11 are natural evolution."** Each modification introduces a new mechanism: a readiness query, a second value-delivery path, conditional affinity wrapping, virtual dispatch for type erasure. The awaitable protocol provides the same capability with three members.

**"A sender can provide a member `as_awaitable` and skip the ceremony. No protocol change is needed."** True. `[exec.as.awaitable]` uses a sender's own `as_awaitable` when the sender provides one, in preference to constructing the generic `sender-awaitable`:<sup>[3]</sup>

```cpp
// [exec.as.awaitable], reduced to the relevant branch
template<class Expr, class Promise>
decltype(auto) as_awaitable(Expr&& e, Promise& p)
{
    if constexpr (requires { e.as_awaitable(p); })
        return e.as_awaitable(p);        // the sender's own awaitable
    else
        return sender-awaitable{e, p};   // the eight steps of Section 6
}
```

In `execution::task`, `await_transform` makes this same check before it wraps anything in `affine`: a sender that provides `as_awaitable` is used directly, so the affinity wrap of Section 6 is skipped as well.<sup>[5]</sup> A sender whose `as_awaitable` returns a synchronous awaitable then takes the path of Section 7. `connect`, the receiver, `start`, the `variant`, and the affinity wrap are never instantiated. Three protocol steps, not eight.

This is the paper's thesis arrived at from the sender side. The synchronous fast path the sender reaches here is an awaitable: the sender hands one back, and the awaitable does the work. Closing the gap for one concrete sender, awaited from a coroutine, is one existing customization point returning the three-member struct of Section 7.

Two costs remain. The member is manual and per-sender; a sender that omits it inherits the eight-step path. And it is lost under type erasure: `any_sender` erases the concrete sender and the member with it, and `any_sender::connect` materializes the operation state of Section 11.5. Type erasure is the one sender-specific cost no `as_awaitable` member reaches.

The scope is the coroutine consumer. A sender pipeline never enters `as_awaitable`; Section 10 records zero for both synchronous pipeline cells.

**"Senders retarget via scheduler swap; awaitables require recompilation."** Section 4 demonstrates retargeting by relinking. One vtable call, zero allocations. The linker swaps the object file.

**"Protocol step counts are not runtime costs."** True when the sender and receiver are fully visible to the optimizer. Not true across type-erasure boundaries, where `any_sender::connect` materializes an operation state the compiler cannot see through.

**"Unconditional suspension is the sound default."** The paper does not argue the default is unsound. It argues the sender protocol provides no override. The awaitable protocol solved this in C++20 with a single boolean. The question is not whether the default is correct but why the protocol has no conditional path.

**"Operation state construction delivers structured concurrency guarantees."** Genuine for asynchronous operations where the coroutine suspends and work executes concurrently. For a synchronous write where the data is in the string before `co_await` evaluates, there is no concurrent lifetime to manage. The operation state guarantees a property that was never at risk.

**"The type erasure comparison is asymmetric."** Both paths use type erasure at the same boundary. The awaitable path produces one indirect call and zero allocations. `any_sender::connect` materializes an operation state the compiler cannot see through.

**"The bridge concedes the dependency."** The bridge goes both directions. [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[9]</sup> bridges IoAwaitables into sender pipelines. [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[11]</sup> bridges senders into coroutine-native code without `execution::task`. Section 10 shows the cost is asymmetric: if I/O is an awaitable, both consumers pay zero; if I/O is a sender, coroutines pay the ceremony.

**"The falsification criteria measure senders on the awaitable's home turf."** The paper says so in Section 1: "Coroutine-native I/O cannot express compile-time work graphs. This is a genuine limitation." Section 5 credits senders with three achievements awaitables do not match. Section 10 covers both synchronous and asynchronous I/O. The falsification criteria are scoped to the paper's claim, not to a universal comparison.

## 13. Falsification

The observations documented in this paper would be discharged if any of the following were demonstrated:

- A sender protocol mechanism, equivalent to `await_ready`, that skips `connect` and `start` for trivially-ready senders without introducing a second value-delivery path.

- A `sender-awaitable` implementation in which `await_ready()` returns `true` when the sender is known to complete synchronously, without requiring `connect` to have already executed.

- A type-erasure mechanism for senders that achieves virtual-dispatch cost - one indirect call, zero allocation per operation - without reintroducing virtual dispatch.

## Acknowledgements

Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators for `std::execution` and the sender algebra. Dietmar K&uuml;hl and Maikel Nadolski for P3552R3 (`std::execution::task`). Robert Leahy for the AIO-to-sender bridge and P2583R4 (symmetric transfer).

## References

[1] [Capy](https://github.com/cppalliance/capy) (C++ Alliance).

[2] [Corosio](https://github.com/cppalliance/corosio) (C++ Alliance).

[3] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Eric Niebler, Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Bryce Adelstein Lelbach, 2024).

[4] [NVIDIA/stdexec](https://github.com/NVIDIA/stdexec) - Reference implementation of `std::execution` (NVIDIA, 2024).

[5] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[6] [P3941R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r2.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[7] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "Ask: A Minimal Coroutine Execution Model" (Vinnie Falco, 2026).

[8] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Vinnie Falco, 2026).

[9] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[10] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[11] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[12] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).
