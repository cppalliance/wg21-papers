---
title: "The Return of Networking TS Executors in P3552"
document: P4286R0
date: 2026-07-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The executor property rejected in 2021 returned, in 2026, as a requirement.

In 2021 the committee set aside the Networking TS; one stated deficiency was that its executors had no way to report a failure. In 2026 `std::execution::task` requires the schedulers that drive it to have no way to report a failure. The two constraints have the same shape. This paper traces the path from one to the other through the distinction between scheduling work and scheduling a continuation. P4094, P4095, and P4096 identified that distinction before P3941R4 established the infallibility requirement. P3941R4 confirms the framing analysis.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial revision.

---

## 1. The Diagnosis

Two papers, six years apart, diagnosed the same deficiency in the executor model.

In 2019, [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf)<sup>[6]</sup> examined the one-way executor concept of the unified executors proposal<sup>[7]</sup>, whose basis operation accepted a callable and returned nothing:

```cpp
void execute(F&& f);
```

The first deficiency the paper named was error propagation. Errors arising during or after submission were handled, it observed, in an implementation-defined manner that varied from one executor to the next:

> "The implication is that no generic code can respond to asynchronous errors in a portable way."

In 2021, [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[8]</sup>, written on behalf of the Finnish national body, applied the same standard to the Networking TS and reached three deficiencies. The first was the absence of an error channel. In October 2021, LEWG polled electronically on the Networking TS ([P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[14]</sup>). The poll on discontinuing the TS reached no consensus; a second poll on basing networking on the sender/receiver model reached weak consensus in favor, and the committee's asynchronous work moved toward P2300. The Networking TS was set aside, and a missing error channel led the list of reasons.

## 2. The Framing

Why was the missing channel a deficiency? [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[3]</sup> documents that `execute(F&&)` replaced three older primitives - `dispatch`, `post`, and `defer` - that scheduled a continuation rather than submitting work. The replacement was the executor unification itself: P0443 reconciled the Networking TS executors descended from Kohlhoff's Asio with the parallel algorithms executors, and collapsed both lineages into a single `execute(F&&)`. The framing determines whether the missing channel is a defect. Two readings of the same signature follow. Under the work framing, the callable is a unit of work, the caller is still running, and a missing error channel strands any failure with nowhere to go. Under the continuation framing, the callable is a resumption handle, the caller has suspended or returned, and there is no live caller waiting to receive an error.

[P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[4]</sup> and [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[5]</sup> show that both P1525R0 and P2464R0 analyzed the operation under the work framing alone. P4094R1, P4095R1, and P4096R1 predate P3941R4. The continuation framing - Kohlhoff's original definition in [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html)<sup>[9]</sup> - had been erased from the API surface by the time either paper was written.

P1525R0's own definition confirms the framing it assumed:

> "For the purpose of this document, by 'one-way execute,' we mean a void-returning function that accepts a nullary Invocable and eagerly submits it for execution on an execution agent that the executor creates for it."<sup>[6]</sup>

"Eagerly submits." "Execution agent that the executor creates." The language is work submission throughout. The continuation primitives that `execute` replaced - `dispatch`, `post`, `defer` - do not appear in P1525R0. P1525R0's four authors participated in the executor unification that collapsed those primitives; all four co-authored P2300<sup>[10]</sup>. The authors who analyzed `execute(F&&)` under the work framing were the same four authors who had collapsed the continuation framing into it. The continuation framing documented in P0113R0 remained in the public record.

Under the continuation framing, an infallible scheduling operation is not a defect. It is the correct shape. A suspended coroutine does not need a channel to receive an error, because it is not running to act on one.

Two readings of the missing channel are possible: the operation may need to report failure but the API does not allow it, or the operation never fails and the API reflects that. Under the continuation framing, the distinction does not survive. A caller that has suspended cannot act on a failure regardless of whether one occurs. The shape of the API follows from the state of the caller.

## 3. The Return

The deficiency diagnosed in 2021 was resolved by the sender/receiver model. The resolution reintroduced the constraint.

The sender/receiver model, [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[10]</sup>, shipped in C++26 as `std::execution`. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[11]</sup> added `task`, a coroutine type with one defining guarantee: scheduler affinity. After a `co_await`, a task resumes on the same scheduler it suspended on. `task` implements the guarantee by wrapping every awaited expression in `affine_on` (since renamed `affine`) - a sender adaptor that schedules the continuation back onto the task's scheduler.

That scheduling operation must not fail. [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html)<sup>[12]</sup> establishes the requirement, in its own words:

> "If this scheduling operation fails, i.e., it completes with `set_error(e)`, or if it gets cancelled, i.e., it completes with `set_stopped()`, the execution agent on which the scheduling operation resumes is unclear and `affine_on` cannot guarantee its promise. Thus, it seems reasonable to require that a scheduler used with `affine_on` is infallible."

A scheduler used with `affine_on` may complete only with `set_value()`. No `set_error`. No `set_stopped`. The scheduling operation that drives `task` has no way to report a failure.

## 4. The Coroutine Executor

A third executor, designed for coroutines, takes the same shape.

[P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[13]</sup> constrains the argument to `continuation` - a coroutine handle paired with an intrusive list pointer:

```cpp
std::coroutine_handle<> dispatch(
    continuation& c) const;

void post(continuation& c) const;
```

`dispatch` returns a handle for symmetric transfer. `post` defers. Both accept a suspended coroutine and resume it on a context. Neither delivers a value.

## 5. The Symmetry

Three executors, separated by a decade of committee work, share one shape.

| Property | P0443R14 executor | Infallible scheduler (P3941R4) | Coroutine executor (P4003R3) |
| --- | --- | --- | --- |
| Error channel | None | None - `set_error` omitted | None after acceptance. `post` throws before. |
| Cancellation | None | None - `set_stopped` omitted | `destroy()` on the handle |
| Value delivered | None | None - `set_value()` nullary | None |
| Encoded in the type by | `void` return | completion signatures | `continuation` argument type |
| Scope | every executor | schedulers used with `affine_on` | every coroutine executor |
| Why the caller tolerates it | it has returned | it is suspended | it is suspended |

The match across three columns is not exact. P0443R14 required infallibility of every executor and said so nowhere - the `void` return left no room to report a failure. P3941R4 requires infallibility of one scheduler in one role and says so in the completion signatures. P4003R3 constrains the argument type to a coroutine handle, making infallibility a consequence of the continuation framing rather than a separate requirement.

The old constraint was universal and implicit. The new ones are narrow and explicit. That the committee chose to make the constraint explicit in P3941R4 - where P0443R14 left it implicit - confirms that the constraint is recognized as correct for this role, not that it is a different constraint.

## 6. A Possible Objection

A possible objection distinguishes incapability from selective constraint. P0443R14's `void` return left no room for an error channel in any executor. P3941R4's completion signatures exclude `set_error` for one scheduler in one role while the model retains the channel elsewhere. The distinction between incapability and selective constraint is real.

The distinction answers a question the paper does not ask. The question is not whether the model surrounding the operation improved - it did. The question is whether the scheduling operation changed its requirements. It did not. Both designs answer the same question - should a continuation-scheduling operation report errors? - and both answer no.

The objection treats P0443R14's `void` return as a limitation the operation inherited from the model. P1525R0 defined the operation as work submission. The `void` return matched the framing the authors assumed - not a limitation of the model, but a consequence of how they read the operation. Kohlhoff designed `dispatch`, `post`, and `defer` with no error channel because the caller had suspended. The `void` return encoded a judgment about the operation's role. P3941R4 encodes the same judgment in completion signatures. The encoding improved. The judgment did not change.

If the objection is that P3941R4's infallibility is a deliberate design choice for a specific role, the objection concedes the paper's claim. The role - scheduling a continuation onto an execution context - is the role `dispatch`, `post`, and `defer` filled. "This time we chose it on purpose" is not a rebuttal. It is an acknowledgment that the choice was available the first time as well.

## 7. The Shape

The shape of the scheduling operation follows from the state of the caller. A caller that is running needs an error channel; a caller that has suspended does not.

Two independent lines of work confirm this. The executor lineage - P0443R14 through P2300 to P3941R4 - discovered the shape through evolution: each revision changed how the constraint was encoded, from `void` return to completion signatures, but the constraint survived every redesign. The coroutine executor in P4003R3 discovered the same shape from first principles of the coroutine model, without sender/receiver concepts and without completion signatures. The two derivations share no abstraction machinery. They share the shape - because they share the caller's state.

Convergence from unrelated starting points eliminates the explanation that the shape is an artifact of any one model's expressiveness. The sender/receiver model did not produce the constraint; neither did the coroutine model. The caller's state produced it, and each model re-encoded what was already there. Kohlhoff's continuation-framed executor carried the same shape in Asio over two decades ago - P0113R0 documented it, but the design predates either model.

P4094, P4095, and P4096 identified the framing distinction before P3941R4 was written. P3941R4 confirmed it. **The committee rediscovered that continuations need a continuation-framed executor.**

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the coroutine model's adoption.

Three earlier papers in this series ([P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[3]</sup>, [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[4]</sup>, [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[5]</sup>) identified the work/continuation framing distinction before P3941R4 was written. This paper shows that P3941R4's infallibility requirement confirms the analysis those papers established.

This paper asks for nothing.

## Acknowledgments

The author thanks Dietmar K&uuml;hl for P3941R4, which specifies the infallibility requirement and states its rationale precisely; Christopher Kohlhoff for the continuation framing in P0113R0 and for the Networking TS; Ville Voutilainen for P2464R0; Eric Niebler, Kirk Shoop, Lewis Baker, and Lee Howes for P1525R0 and the sender/receiver model that resolved the deficiencies they identified; and Steve Gerbino and Mungo Gill for co-developing the coroutine executor in P4003R3.

## References

[1] [Capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library (Vinnie Falco).

[2] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library (Vinnie Falco).

[3] [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[4] [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[5] [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).

[6] [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[7] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, David Hollman, 2020).

[8] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[9] [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html) - "Executors and Asynchronous Operations, Revision 2" (Christopher Kohlhoff, 2015).

[10] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[11] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[12] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[13] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[14] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution Polling Outcomes on Networking and Executors" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).
