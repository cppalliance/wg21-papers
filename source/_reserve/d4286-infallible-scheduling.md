---
title: "The Return of Networking TS Executors in P3552"
document: P4286R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The executor property rejected in 2021 returned in 2026 as a requirement. In 2021, the committee set aside the Networking TS; one stated deficiency was that its executors had no way to report a failure. In 2026, `std::execution::task` requires that the schedulers driving it lack any way to report a failure. The operation is the same; only the verdict changed. This paper traces the path from one verdict to the other through the distinction between scheduling work and scheduling a continuation. P4094R1, P4095R1, and P4096R1 identified that distinction before P3941R4 established the infallibility requirement; P3941R4 confirms the framing analysis's prediction.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## 1. The Diagnosis

Two papers, six years apart, diagnosed the same deficiency in the executor model. In 2019, [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf)<sup>[1]</sup> examined the one-way executor concept of the unified executors proposal<sup>[2]</sup>, whose basis operation accepted a callable and returned nothing:

```cpp
void execute(F&& f);
```

That signature was itself the product of a simplification. [P0688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0688r0.html)<sup>[9]</sup> had removed three older primitives (`dispatch`, `post`, and `defer`) from the API surface two years earlier, retaining the continuation semantics only as an optional `prefer(is_continuation)` hint. What remained was `execute(F&&)`, and what it described was work submission.

The first deficiency the paper named was error propagation. Errors arising during or after submission were handled, it observed, in an implementation-defined manner that varied from one executor to the next:

> "The implication is that no generic code can respond to asynchronous errors in a portable way."

In 2021, [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[3]</sup>, written on behalf of the Finnish national body, applied the same standard to the Networking TS and identified three deficiencies. The first was the absence of an error channel. In October 2021, LEWG polled electronically on the Networking TS ([P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[4]</sup>). The poll on discontinuing the TS reached no consensus. A second poll on basing networking on the sender/receiver model reached weak consensus in favor, and the committee's asynchronous work moved toward P2300. The Networking TS was set aside, and a missing error channel led the list of reasons.

## 2. The Framing

Why was the missing channel a deficiency? [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[5]</sup> documents that `execute(F&&)` replaced the three continuation primitives with a single basis operation. The replacement was the executor unification itself: P0443 reconciled the Networking TS executors descended from Kohlhoff's Asio with the parallel algorithms executors and collapsed both into a single `execute(F&&)`. The framing determines whether the missing channel is a defect. Two readings of the same signature follow. Under the work framing, the callable is a unit of work, the caller is still running, and a missing error channel strands any failure. Under the continuation framing, the callable is a resumption handle, the caller has suspended or returned, and no live caller is waiting to receive an error.

[P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[6]</sup> and [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[7]</sup> show that both P1525R0 and P2464R0 analyzed the operation under the work framing alone. P4094R1, P4095R1, and P4096R1 predate P3941R4. The continuation framing, Kohlhoff's original definition in [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html)<sup>[8]</sup>, was already absent from the API surface when each paper was written.

P1525R0's own definition confirms the framing it assumed:

> "For the purpose of this document, by 'one-way execute,' we mean a void-returning function that accepts a nullary Invocable and eagerly submits it for execution on an execution agent that the executor creates for it."<sup>[1]</sup>

"Eagerly submits." "Execution agent that the executor creates." Both phrases describe submitting work to a newly created agent, not resuming a caller that has suspended. The continuation primitives that `execute` replaced do not appear in P1525R0. By the time it analyzed the operation, the framing was documented in P0113R0 but no longer visible in the signature.

Under the continuation framing, an infallible scheduling operation is not a defect; it is what the operation's role requires. A suspended coroutine receives a completion in one way only: by being resumed. A scheduling operation exists to choose the agent on which that resumption occurs. If it fails, it has not chosen one, and a failure completion delivered to the continuation resumes it on an agent the operation could not determine. Every instruction the continuation then executes, including its unwinding, runs where the operation was meant to keep it from running. The channel is not unneeded. Using it would break the guarantee the operation exists to provide.

Two readings of the missing channel are possible. In the first, the operation may need to report failure, but the API does not allow it. In the second, the operation never fails, and the API reflects that. Under the continuation framing, the distinction does not survive. A report of failure can reach a suspended caller only by resuming it, and a scheduling operation that has failed cannot say where. Whether the failure is impossible or merely unreported, the continuation cannot be handed it without resuming on an agent the operation did not select.

## 3. The Coroutine Executor

A third executor, designed for coroutines, omits the same channels. [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[10]</sup> constrains the argument to `continuation`, a coroutine handle paired with an intrusive list pointer:

```cpp
std::coroutine_handle<> dispatch(
    continuation& c) const;

void post(continuation& c) const;
```

`dispatch` returns a handle for symmetric transfer, and `post` defers. Both accept a suspended coroutine and resume it on a context. Neither delivers a value. Neither reports a scheduling failure to the continuation: `post` throws when it cannot accept the continuation, before acceptance, and after acceptance there is no channel at all. This executor was designed from the coroutine model's first principles, without sender/receiver concepts and without completion signatures, and it arrived at the condemned shape directly.

## 4. The Discovery

The sender/receiver model reached the same wall from the other side.

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[11]</sup> shipped in C++26 as `std::execution`. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[12]</sup> added `task`, a coroutine type with one defining guarantee: scheduler affinity. After a `co_await`, a task resumes on the same scheduler on which it suspended. `task` implements the guarantee by wrapping every awaited expression in `affine_on` (since renamed `affine`), a sender adaptor that schedules the continuation back onto the task's scheduler.

That scheduling operation must not fail. [P3941R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3941r0.html)<sup>[18]</sup> establishes the requirement on 2025-12-14, in section 3.2 "Infallible Schedulers", and the passage is carried unchanged through [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html)<sup>[13]</sup>. The concept is named earlier still: [P3796R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r0.html)<sup>[19]</sup>, dated 2025-07-15, defines a wrapper called `infallible_scheduler` and gives the same rationale.

> "If this scheduling operation fails, i.e., it completes with `set_error(e)`, or if it gets cancelled, i.e., it completes with `set_stopped()`, the execution agent on which the scheduling operation resumes is unclear and `affine_on` cannot guarantee its promise. Thus, it seems reasonable to require that a scheduler used with `affine_on` is infallible."

A scheduler used with `affine_on` may complete only with `set_value()`, not `set_error` or `set_stopped`. For continuation scheduling, fallibility is not merely unneeded; it is unworkable, because a failed or cancelled scheduling operation leaves the resumption agent unknown. The model that resolved the 2021 deficiency discovered that it needed the condemned property.

## 5. The Return

The scheduling operation that drives `task` has no way to report a failure. Neither does the coroutine executor of P4003R3. Neither did Kohlhoff's continuation primitives. The property condemned as a defect in 2021 is required in 2026, for the same operation, for the reason the continuation framing gives and P3941R4 states: the caller has suspended, a failure report could reach it only by resuming it, and a scheduling operation that has failed cannot say on which agent.

The 2021 diagnosis was wrong about the operation. A missing error channel is a defect for work submission, whose caller is still running to receive the report; continuation scheduling can deliver a report only by resuming the caller on an agent the operation failed to select. The property the diagnosis condemned was the correct shape for the operation, and the committee's own later work reimposed it: by design in P4003R3's coroutine executor, and by requirement in P3941R4. The 2021 decision to set the Networking TS aside rested on more than this diagnosis, and this paper does not revisit it. The diagnosis, it does.

## 6. The Symmetry

The shape of a scheduling operation is the profile of channels it offers the caller: error, cancellation, and value. Three executors, separated by a decade of committee work, share one shape.

| Property | P0443R14 Executor | Infallible Scheduler (P3941R4) | Coroutine Executor (P4003R3) |
| --- | --- | --- | --- |
| Error channel | None | None; `set_error` omitted | None after acceptance. `post` throws before. |
| Cancellation | None | None; `set_stopped` omitted | `destroy()` on the handle |
| Value delivered | None | None; `set_value()` nullary | None |
| Encoded in the type by | `void` return | Completion signatures | `continuation` argument type |
| Scope | Every executor | Schedulers used with `affine_on` | Every coroutine executor |
| Why the caller tolerates it | It has returned | It is suspended | It is suspended |

The match across three columns is not exact. P0443R14 required infallibility of every executor but omitted any such statement; the `void` return left no room to report a failure. P3941R4 requires infallibility of one scheduler in one role and states the requirement in the completion signatures. P4003R3 constrains the argument type to a coroutine handle, making infallibility a consequence of the continuation framing rather than a separate requirement. P4003R3's `post` can throw when it cannot accept the continuation, so its infallibility holds after acceptance rather than unconditionally.

The old constraint was universal and implicit. The new ones are narrow and explicit. That the committee chose to make the constraint explicit in P3941R4, where P0443R14 left it implicit, confirms that the constraint is recognized as correct for this role, not that it is a different constraint.

## 7. Two Possible Objections

The first objection distinguishes incapability from selective constraint. P0443R14's `void` return left no room for an error channel in any executor. P3941R4's completion signatures exclude `set_error` for one scheduler in one role, while the model retains the channel elsewhere. The distinction between incapability and selective constraint is real.

The distinction answers a question the paper does not ask. The question is not whether the model surrounding the operation improved; it did. The question is whether the scheduling operation changed its requirements; it did not. Both designs answer the same question: Should a continuation-scheduling operation report errors? Both answer no.

The objection treats P0443R14's `void` return as a limitation the operation inherited from the model. P1525R0 defined the operation as work submission. The `void` return matched the framing the authors assumed: not a limitation of the model, but a consequence of how they read the operation. Kohlhoff designed `dispatch`, `post`, and `defer` with no error channel because the caller had suspended. The `void` return encoded a judgment about the operation's role. P3941R4 encodes the same judgment in completion signatures; the encoding improved, and the judgment did not change.

That P3941R4's infallibility is a deliberate choice for a specific role narrows the claim without rebutting it. The role, scheduling a continuation onto an execution context, is the role `dispatch`, `post`, and `defer` filled. The deliberate choice improves on the inherited one in explicitness and scope; the requirement it encodes is the same.

The second objection concerns what happens when scheduling does not happen. In the sender/receiver model, an asynchronous operation, once started, "eventually completes exactly once," and if the lifetime of its operation state ends before the operation completes, the behavior is undefined ([exec.async.ops])<sup>[16]</sup>. An infallible scheduler therefore has one terminal outcome: `set_value()`. The Networking TS has two. A handler is invoked once, or it is destroyed without being invoked. On destruction of an `io_context`, "uninvoked handler objects that were scheduled for deferred invocation on the `io_context`, or any associated strand, are destroyed" ([io_context.io_context.dtor])<sup>[17]</sup>. P4003R3's `execution_context` inherits the same discipline. The objection holds that these are different contracts, and that a table placing them in one shape conflates them.

The contracts differ, and the difference is one decision encoded twice. The question the caller's state poses is whether the scheduling operation reports failure to the continuation. Both models answer no. Sender/receiver, having removed destruction as a terminal outcome, can keep that answer only by making the operation unable to fail: `set_value()` is the sole completion, and the requirement falls on the scheduler as a precondition. The Networking TS, having kept destruction as a terminal outcome, can let the operation fail by not occurring: the handler is released through its owner, and the continuation receives nothing. Neither hands the suspended continuation an error. The shape defined in Section 6 is the profile of channels offered to the continuation. Destruction is not a channel offered to the continuation; it is the owner's disposal of it, and it falls outside the profile in both models.

What each model does when the context goes away with work pending confirms the reading. The Networking TS destroys the handlers. The `run_loop` destructor in `std::execution` invokes `terminate()` if the loop's count is not zero or its state is running ([exec.run.loop.ctor])<sup>[16]</sup>. One model releases the continuation; the other ends the program. Neither reports to the continuation, because there is no channel on which to do so, and under the continuation framing a report could be delivered only by resuming the continuation on an agent the operation did not select. The run-loop scheduler's own completion signatures omit `set_error_t` entirely ([exec.run.loop.types])<sup>[16]</sup>; the one concrete scheduler in the standard already cannot report an error.

## 8. The Shape

The shape of the scheduling operation follows from the state of the caller. A caller that is running can receive an error where it stands. A caller that has suspended can receive one only by being resumed, and a scheduling operation that has failed cannot say where.

Two independent lines of work confirm this. The executor lineage runs from P0443R14 through P2300R10 to P3941R4. It discovered the shape through evolution: each revision changed how the constraint was encoded, from `void` return to completion signatures, but the constraint survived every redesign. The coroutine executor in P4003R3 discovered the same shape from first principles of the coroutine model, without sender/receiver concepts and without completion signatures. The two derivations share no abstraction machinery. They converge because they share the caller's state.

Convergence from unrelated starting points eliminates the explanation that the shape is an artifact of any one model's expressiveness. The sender/receiver model did not produce the constraint; neither did the coroutine model. The caller's state produced it, and each model re-encoded what was already there. Kohlhoff's continuation-framed executor omitted the same three channels in Asio over two decades ago. P0113R0 documented it, but the design predates either model.

P4094R1, P4095R1, and P4096R1 identified the framing distinction before P3941R4 was written. P3941R4 confirmed the prediction. *The committee rediscovered that continuations need a continuation-framed executor.*

## Disclosure

The author provides information and serves at the pleasure of the committee. This paper asks for nothing.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[14]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[15]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the coroutine model's adoption.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

## Acknowledgments

The author thanks Dietmar K&uuml;hl for P3796R0 and P3941R0, which name the infallibility requirement and state its rationale precisely, and for carrying that text unchanged through P3941R4; Christopher Kohlhoff for the continuation framing in P0113R0 and for the Networking TS; Ville Voutilainen for P2464R0; Eric Niebler, Kirk Shoop, Lewis Baker, and Lee Howes for P1525R0 and the sender/receiver model that resolved the deficiencies they identified; and Steve Gerbino and Mungo Gill for co-developing the coroutine executor in P4003R3.

## References

[1] [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[2] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, David Hollman, 2020).

[3] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[4] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution Polling Outcomes on Networking and Executors" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[5] [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[6] [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[7] [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).

[8] [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html) - "Executors and Asynchronous Operations, Revision 2" (Christopher Kohlhoff, 2015).

[9] [P0688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0688r0.html) - "A Proposal to Simplify the Unified Executors Design" (Chris Kohlhoff, Jared Hoberock, Chris Mysen, Gordon Brown, 2017).

[10] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[11] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[12] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[13] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[14] [Capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library (Vinnie Falco).

[15] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library (Vinnie Falco).

[16] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2026).

[17] [N4771](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4771.pdf) - "Working Draft, C++ Extensions for Networking" (Jonathan Wakely, 2018).

[18] [P3941R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3941r0.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2025).

[19] [P3796R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r0.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).
