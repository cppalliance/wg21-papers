---
title: "Infallible Scheduling: The Missing Error Channel From P0443R14 to P3941R4"
document: P4286R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Three scheduling operations, specified in 2020 and 2026 and encoded three different ways, declare no typed error channel.

Between 2019 and 2021, three documents named the same deficiency in the executor model, one of them the unified executors proposal itself. An executor could fail with no channel on which to report the failure. The sender/receiver model answered it and made the channels part of the type. The absence of an error channel is then a defect only under one reading of the operation. If the operation schedules a unit of work, the caller still runs and can act on a failure. If it schedules a continuation, the caller is suspended, and only a resumption lets it act. This paper compares three designs under that distinction. They are the one-way `execute` of the unified executors proposal, the scheduler that `affine_on` requires, and a coroutine executor from outside that model. Their encodings differ and their scopes differ. One of the three is the author's own. Two of the three inherit the profile from an earlier design. P3941R4 supplies only a rationale, and it also specifies the fallible alternative it rejected and a path to relax the constraint later.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## Introduction

This paper compares one scheduling operation across three executor designs. The three are the one-way `execute` of the unified executors proposal, the scheduler that P3941R4 requires for use with `affine_on`, and the coroutine executor of P4003R3. Sections 1 through 5 compare the three channels that each design offers its caller: error, cancellation, and value. Those sections also show where the shared shape came from. The paper applies one distinction throughout. An operation either schedules a unit of work, or it schedules a continuation. This paper calls the first reading the work framing and the second the continuation framing. Section 2 sets out both.

The related work falls into four groups. P1525R0, P0443R14 itself, and P2464R0 named the missing error channel as a deficiency of the one-way operation, and P2453R0 records the polls that followed. P0113R0 specifies the submission operations that `execute` replaced. P3552R3 specifies `task`, and P3941R4 specifies the infallibility requirement and states its rationale. P4094R1, P4095R1, and P4096R1, by this author, analyze the unification and the diagnoses of P1525R0 and P2464R0 through the work and continuation framings that this paper applies.

Contributions:

1. The outcomes of the five 2021 Library Evolution and Concurrency polls on networking and executors, with the reasons P2453R0 records for them. The chairs' summary and the voters' own comments are kept separate.
2. The work framing and the continuation framing, set out as two readings of one signature, with what each one implies about a missing error channel.
3. A channel-by-channel comparison of three scheduling operations, specified in 2020, 2026, and 2026, whose encodings share no vocabulary, though two of the three designs share ancestry.
4. The scope and the encoding of P3941R4's infallibility requirement, with the fallible-scheduler alternative that P3941R4 itself specifies.

Assumptions:

1. A scheduling operation offers its caller three channels: error, cancellation, and value. That profile is a design property worth a comparison across operations whose encoding mechanisms are unrelated, whatever ancestry the designs share.
2. The text of a paper is evidence of the framing that its authors applied to the operation they analyzed.
3. P3941R4's stated rationale is taken at its word: The requirement exists so that `affine_on` can guarantee scheduler affinity.

## 1. Three Documents Named a Missing Error Channel

Three documents named the missing error channel of the one-way executor, in 2019, in 2020, and in 2021. The second of the three is the unified executors proposal itself. This section records what that proposal provided, the three diagnoses, the published response to the third, and the polls that followed. Sections 6 and 7 draw on that record.

The unified executors proposal provided three things that generic asynchronous code did not have. First, it reconciled three independent proposals under a single concept. P0688R0 later used that description. The three were the Networking Technical Specification (TS) executors that descend from Asio, the executors of the parallel algorithms, and thread-pool executors. One generic algorithm could then target all of them.

Second, it made the behavior of an executor requestable at the call site instead of fixed by its type. A caller uses `require` and `prefer` over a set of properties. That set covers blocking, work tracking, bulk execution guarantees, the mapping of agents onto threads, allocation, and the continuation relationship.

Third, it provided `bulk_execute`, which in P0443R14's words "creates a group of function invocations in a single operation" (section 1.3).

In 2019, [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf)<sup>[1]</sup> examined the one-way executor concept of the unified executors proposal, then at P0443R10. P0443R14<sup>[2]</sup>, the final revision, gives the expression `execution::execute(e, f)` the return type `void` in the `executor_of` requirements table (section 2.2.9). The member form appears in the `any_executor` synopsis (section 2.4.3):

```cpp
template<class Function>
void execute(Function&& f) const;
```

P1525R0 named error propagation as the first deficiency of that operation. Each executor handled errors that arose during or after submission in its own implementation-defined manner (abstract, page 1):

> "The implication is that no generic code can respond to asynchronous errors in a portable way."

By 2020, P0443R14 named the same gap in its own text. Its section 1.4, "Senders and Receivers Represent Work", turns on the same `void` return. That return leaves the executor abstraction with "no generic way to chain operations and thereby propagate values, errors, and cancellation signals downstream". It also leaves "no way to handle scheduling errors occurring between when work submission and execution". [P0443R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0443r10.html)<sup>[3]</sup>, the revision P1525R0 had examined, carried no senders and no receivers. A text search of it finds no occurrence of `sender`, `receiver`, `set_error`, or `connect`. By P0443R14 the proposal had taken up both the diagnosis and a remedy for it. Its section 1.2 names executors and senders and receivers together as the proposal's two key components.

In 2021, [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[4]</sup>, written on behalf of the Finnish national body, applied the same standard to the Networking TS. It named three parts to the problem. The first is the one this paper follows, and it concerned two different failures. An I/O operation can report success or failure to a completion handler. The executor can fail on its own, and it has no mechanism or channel to report that failure.

A published response followed six days later. [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[5]</sup>, "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not.", disputed the conclusions of P2464R0. It also set out the continuation reading in its own terms, and section 2 quotes it. The author of the present paper is one of the five authors of P2469R0. The reading that follows was therefore a party's position in the 2021 dispute.

Table 1: The five October 2021 electronic decision polls on networking and executors. The Library Evolution and Concurrency groups conducted them. [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[6]</sup> reports the outcomes, and records 56 participants with abstentions on individual polls. Poll 3 was the only one that proposed to stop work on the Networking TS design. P2453R0 adds two notes under poll 1. Its result does not mean that the Networking TS model is a poor fit for networking. The authors would also build consensus more easily with a focus on networking than on general asynchrony.

| Poll | SF | WF | N | WA | SA | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| 1. The Networking TS and Asio asynchronous model is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs | 5 | 10 | 6 | 14 | 18 | Weak consensus against |
| 2. The sender/receiver model is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs | 24 | 16 | 3 | 6 | 3 | Consensus in favor |
| 3. Stop pursuing the Networking TS and Asio design as the standard library's answer for networking | 13 | 13 | 8 | 6 | 10 | No consensus |
| 4. Networking in the C++ standard library should be based on the sender/receiver model | 17 | 11 | 10 | 4 | 6 | Weak consensus |
| 5. It is acceptable to ship socket-based networking in the C++ standard library that does not support secure sockets (TLS or DTLS) | 9 | 13 | 5 | 6 | 13 | No consensus |

P2453R0 states polls 1, 2, and 4 in terms of the specific papers that propose each model. The chairs' summary under poll 3 records that the committee will continue work on networking in this general form. It names two positions held among those in favor of a stop. The first is a preference to build networking on senders and receivers. The second is opposition to the absence of Transport Layer Security (TLS). A separate section carries the guidance to the Networking Study Group. That guidance names the same two areas, security and the sender/receiver model, as the ones to address before networking papers return to Library Evolution. The missing error channel appears in neither text.

The missing error channel does appear in the voters' own comments. Under poll 1, P2453R0 section 4.1 records "I have been convinced that the error handling around work submission is not sufficient as a building block", "It doesn't support rich error channels or cancellation", and "it does not provide good handling for scheduling error". One comment cites P2464R0 by number, and states that the model "loses the information about scheduling errors, which makes layering senders on top of it infeasible". Under poll 2, section 4.2 records that the sender/receiver model "has first-class support for rich error channels and cancellation, which are must-have features to certain users".

The three diagnoses were therefore not isolated, and one of them belongs to the design under diagnosis. The reasons that the chairs recorded and the reasons that individual voters gave differ. The error channel appears in the second set and not in the first.

## 2. One Signature, Two Readings: Work or Continuation

A missing error channel is a defect only under one reading of the operation. This section sets out the two available readings, and identifies the reading that each diagnosis applied.

[P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[7]</sup> documents that `execute(F&&)` replaced three older submission primitives: `dispatch`, `post`, and `defer`. [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html)<sup>[8]</sup> separates the three by eagerness, and by the relationship that each one declares to the caller. It does this in its rationale (section 9) and in the executor requirements (section 12.3.3, table 4). `dispatch` can run the callable before it returns. `post` submits the callable for later execution and does not block the caller. `defer` carries the further meaning that the submitted function object is a continuation of the caller. P0113R0 also states the default for a low-level operation that cannot tell the two cases apart. That default assumes a new fork in the control flow and uses `post`. Of the three, only `defer` declares the continuation relationship in the API.

The replacement was the executor unification itself, which collapsed all three models into a single `execute(F&&)`. Two readings of that one signature follow. Under the work framing, the callable is a unit of work, the caller still runs, and a missing error channel strands any failure. Under the continuation framing, the callable is a resumption handle, the caller is suspended or has returned, and no live caller waits for an error.

[P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[9]</sup> and [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[10]</sup> read P1525R0 and P2464R0 as papers that analyze the operation under the work framing. P1525R0 states its error-propagation arguments in terms of work submitted to an agent that the executor creates. Where that paper turns to coroutines, in section 4.1, its argument is about allocation. P2464R0 is the harder case for the reading. It describes Networking TS executors as the mechanism that users customize to run continuations for I/O events. It still finds the missing channel a defect, on the ground that the executor can fail on its own. Section 6 takes up that objection.

The record already carried the continuation reading in 2021. P2469R0 put it in terms of the tail call (section "Error handling within the tail call"):

> "After a synchronous function call returns, any errors that subsequently arise are obviously somebody else's problem. Similarly, by definition, any errors that occur following the asynchronous 'tail call' do not return back to the asynchronous operation, as it has ceased to exist, just like the scope of the analogous synchronous function call that we returned from. Consequently, the 'tail call' customisation point relates only to submission."

That passage states the continuation framing, applied to the same dispute, four and a half years before P3941R4 required infallibility. It also fixes the standing of the framing. P2469R0 is a response paper that argues one side of a disagreement, and the present author is one of its five authors. What follows therefore applies a party's analytical lens. The channel-by-channel comparison in section 5 does not depend on acceptance of that lens.

P0443R14 did keep a queryable form of the continuation framing. Its synopsis carries the property `relationship_t`, under the comment that the property indicates whether submitted tasks represent continuations. Section 2.2.12.2 specifies the nested value `relationship_t::continuation_t`, whose requirement reads that function objects submitted through the executor represent continuations of the caller. The nested value carries the requirable and preferable flags, and the enclosing property type does not. A caller can therefore impose the value through `require`, or hint at it through `prefer`. What the framing lost was its place in the signature. `execute` returns `void` in either case.

P1525R0's own definition states the framing that it applied (section 1.1.1, page 1):

> "For the purpose of this document, by 'one-way execute,' we mean a void-returning function that accepts a nullary Invocable and eagerly submits it for execution on an execution agent that the executor creates for it."<sup>[1]</sup>

The phrases "eagerly submits" and "an execution agent that the executor creates for it" describe submission to a new agent. Neither describes the resumption of a suspended caller. None of `dispatch`, `post`, or `defer` appears in P1525R0 as an operation name. A text search of the document finds the word "defer" twice, and both instances carry its ordinary English sense. [P0688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0688r0.html)<sup>[11]</sup> had replaced `defer` with a `prefer(is_continuation)` hint two years earlier, and reduced the execution functions of P0443R1 from sixteen to six. It records that the presence of `defer` in P0443R1 "was controversial". `dispatch` plays no part in P0688R0's account. P0688R0 offered the continuation relationship as a preference, and in its words "executors are under no obligation to satisfy user preferences" (section 1.3).

Under the continuation framing, the absence of an error channel is not automatically a defect. A scheduling operation that failed cannot itself resume the caller on the agent that it was promised.

The missing channel admits two further interpretations. In the first, the operation can need to report a failure, and the API does not permit this. In the second, the operation never fails, and the API shows that. Under the continuation framing the difference between them narrows. Under either interpretation, the caller does not return to the agent that it was promised. What reaches the caller, if anything, is notice of a broken promise and not a condition that it can retry.

## 3. P3941R4 Excludes `set_error` From Schedulers Used With `affine_on`

This section states what the sender/receiver model added in place of the missing channel, and what P3941R4 then withheld from one scheduler in one role.

The sender/receiver model, [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[12]</sup>, became `std::execution`. P3552R3 records that C++26 added it as a general interface to asynchronous operations.

The model provided what the three diagnoses had asked for. P0443R14 had proposed senders and receivers alongside the executor whose limits it named, and P2300R10 is the design that shipped. A failure now propagates through generic code as a typed completion, and no executor handles it in a manner of its own. Every operation declares its channels, but not every operation carries an error channel. An operation that cannot fail declares no error completion, and the schedule sender of `inline_scheduler` carries `set_value_t()` alone (P3552R3 section 9.2). The split of submission into `connect` and `start` also lets the operation state sit in the frame of the caller. A coroutine that awaits a scheduler therefore need not allocate, which is the gap P1525R0 named in its section 4.1.

[P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[13]</sup> added `task`, a coroutine type that is scheduler affine by default. After a `co_await`, a task resumes on the same scheduler on which it suspended. P3552R3 also provides a way to disable affinity through the task's context parameter, which its proposed wording names `Environment`. It describes as prior work the `unifex::task<T>` of libunifex, which is scheduler affine in the same sense (section 2.4). `task` implements affinity in `await_transform`, which wraps the awaited expression in `affine_on`. That sender adaptor schedules the continuation back onto the scheduler of the task. The wrap does not occur where the scheduler of the task is `inline_scheduler`. P3941R4 observes that the name can merit a change, and [P4151R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4151r1.pdf)<sup>[14]</sup> proposes `affine`. This paper uses the name `affine_on` throughout, and follows its sources.

[P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html)<sup>[15]</sup> provides three things for that guarantee, which P3552R3 had stated without a constraint on the schedulers that must deliver it. First, it gives the guarantee a mechanism, an exposition-only concept, so that compilation rejects a scheduler that cannot meet it. The rejection occurs in two places. One is the constructor for `task_scheduler`. The other is completion-signature computation for `affine_on`, where a scheduler that fails the concept makes `get_completion_signatures` exit with an exception. Second, it states what the guarantee costs, and names the completions that a conforming scheduler can use. Third, it surveys the four schedulers of the working draft, and states for each one whether it can be made infallible.

P3941R4 requires that a scheduler used in that role be infallible, and states the rationale (section 3.3):

> "However, if this scheduling operation fails, i.e., it completes with `set_error(e)`, or if it gets cancelled, i.e., it completes with `set_stopped()`, the execution agent on which the scheduling operation resumes is unclear and `affine_on` cannot guarantee its promise. Thus, it seems reasonable to require that a scheduler used with `affine_on` is infallible, at least when used appropriately (i.e., when providing a receiver whose associated stop token is an `unstoppable_token`)."

The wording of P3941R4 carries the requirement in an exposition-only concept, *infallible-scheduler* (section 4). The concept admits two completion-signature sets. The first is `set_value_t()` alone. The second is `set_value_t()` together with `set_stopped_t()`, and it applies where the environment's stop token permits a request to stop. The concept excludes `set_error` from both sets. Where that stop token is an `unstoppable_token`, the first set is the only form the concept admits. The constructor of `task_scheduler`, the type-erased scheduler that `task` uses, mandates the concept with an empty environment. The stop token of that environment is unstoppable, so the strict form governs there.

P3941R4 removes the failure in three places at once. It excludes `set_error` from the type of the scheduler, through the concept. It strikes a sentence from the specification of `affine_on`. That sentence, which P3552R3 had put there, sent an error completion to the receiver on an unspecified execution agent. P3941R4 also removes the case from compilation, because a scheduler that fails the concept makes `get_completion_signatures` exit with an exception.

The analogous sentence survives for `on`. That algorithm makes a related promise: it remembers the scheduler obtained from `get_start_scheduler` and transfers execution back to that scheduler's execution resource. It keeps its error completion notwithstanding. What separates the two is the grain of the promise. `on` names an execution resource, while `affine_on` names the execution agent on which the operation was started, and P3941R4's rationale turns on that agent being unclear after a failure. A delegate may reasonably hold that `on` shows a promise of this kind can coexist with an error path.

The survey is not uniformly favorable to the requirement. P3941R4 records that the current specification of `run_loop::run-loop-scheduler` permits its scheduling operation to fail with `set_error_t(std::exception_ptr)`. It records that the interface of `parallel_scheduler` permits the same failure, and that a constraint on that interface seems unlikely. Two of the four schedulers in the working draft therefore declare a typed error channel on `schedule` today. The requirement narrows where such a scheduler can be used. It does not describe the model as a whole.

## 4. P4003R3 Reaches the Same Profile From Outside the Model

A third executor fixes the same profile by its argument type rather than by a requirement, and it comes from outside the sender/receiver model. [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[16]</sup> attributes its lineage plainly. The design borrows from Boost.Asio, and its acknowledgments record that its `execution_context`, executor, and service model derive directly from that library. The operations below carry Asio's names for that reason.

P4003R3 constrains the argument to `continuation`, a coroutine handle paired with an intrusive list pointer (section 4.3):

```cpp
std::coroutine_handle<> dispatch(
    continuation& c) const;

void post(continuation& c) const;
```

`dispatch` returns a handle for symmetric transfer, and `post` defers. Both operations accept a suspended coroutine and resume it on a context. Neither one delivers a value. Neither one carries `noexcept`, so either one can report a submission failure by a throw. Cancellation in P4003R3 is not an operation on the handle. A coroutine obtains a `std::stop_token` when it awaits `get_stop_token` (section 3.3).

The absence of a value channel here follows from the argument type and not from a stated requirement.

## 5. Three Encodings, One Missing Typed Error Channel

Each of the three operations of sections 1, 3, and 4 fixes its channel profile by a different mechanism. This section compares the three profiles.

Table 2: The channel profile of three scheduling operations, with the mechanism that fixes each profile in the type system and the scope over which it holds. The designs date from 2020, 2026, and 2026. "In the type" marks a channel that a caller can see in the signature or the completion signatures of the operation, as distinct from a failure that a thrown exception delivers.

| Property | P0443R14 `execute` | Infallible scheduler (P3941R4) | Coroutine executor (P4003R3) |
| --- | --- | --- | --- |
| Error channel | None in the type. `execute` is not `noexcept`, so submission may throw (P1525R0 section 2.2), and the treatment of exceptions from the callable is implementation-defined | None. `set_error` excluded from both signature sets the concept admits, and P3941R4 strikes `affine_on`'s own error completion on an unspecified agent. Two of the four standard schedulers currently declare one | None in the type. Neither operation is `noexcept`, so submission may throw |
| Cancellation | None | `set_stopped` permitted only where the receiver's stop token is stoppable | Not on the handle. `std::stop_token` awaited by the coroutine |
| Value delivered | None. `void` return | None. `set_value()` is nullary | None |
| Encoded in the type by | `void` return | Completion signatures | `continuation` argument type |
| Scope | Every executor | Schedulers used with `affine_on`, unconditionally for `task_scheduler` | Every coroutine executor |

The columns agree row by row to different degrees. Only P3941R4 excludes a typed error completion outright. In the other two, an exception stays available at submission. P1525R0 section 2.2 sets this out for `execute`, under the heading that one-way execute cannot be `noexcept` in general. The older constraint was universal and unstated. The newer one is narrow and stated. The three columns differ in scope and in mechanism, and agree only on the row Table 2 records first.

## 6. Expected Objections

Three objections bear on the comparison in section 5. This section states each objection in the form that an objector would use, and answers it from evidence already presented.

### 6.1 "Incapability and selective constraint are different things"

P0443R14's `void` return left no room for an error channel in any executor. P3941R4's completion signatures exclude `set_error` for one scheduler in one role, and the model keeps the channel everywhere else. The distinction is real, and section 5 records it column by column.

What the two designs share is narrower than the objection allows for. In each design, the operation that resumes a suspended caller has no channel to report a failure to that caller. Both the scope of the condition and the mechanism that encodes it changed. A `void` return could not carry a scope of one role. Completion signatures can carry one, and they do.

### 6.2 "P3941R4 itself specifies the fallible alternative"

P3941R4 considered fallible schedulers and specified how they would work. Section 3.3.2, titled "Allow Fallible Schedulers For `affine_on`", sets out the option. `affine_on` could complete with `set_error(rcvr, scheduling_error{e})` when the scheduling operation fails, and that completion would make the wrong-scheduler outcome detectable instead of prohibited. The same section notes that a caller who needs a specific scheduler is served in either case, since "in that case the user will need to make sure that the used scheduler is infallible", and that no static check enforces it. Section 3.3.3 adds that if the constraint proves too strong, "the constraint can be relaxed in a future revision of the standard by explicitly opting out". P3552R3 also permits a task to disable scheduler affinity through its context parameter.

The objection follows. The proposing paper presents the constraint as one of two options, and offers to relax it. A constraint of that kind is a scoped design decision, and not a property that the state of the caller forces.

The reason that P3941R4 gives answers part of that objection. The rationale quoted in section 3 turns on what the resumed caller can be told. A failed scheduling operation leaves the execution agent on which it resumes unclear, so `affine_on` cannot guarantee its promise. That reason concerns the position of the caller and not the expressiveness of the model. The record does not settle whether the reason generalizes past `affine_on`, and the comparison in section 5 does not extend that far.

### 6.3 "If we standardize an executor abstraction, that's what programmers will use"

P2464R0 states the objection to a narrowly scoped infallibility requirement four and a half years before the requirement existed. Two items of a three-item list carry it, a list distinct from the three-fold problem of section 1:

> "the Networking TS effectively requires that the executors never fail between work submission and continuation invocation, but if we standardize an executor abstraction, that's what programmers will use, beyond their limited use in the Networking model and its APIs."

The same paper describes Networking TS executors as the mechanism that users customize to run continuations for I/O events. The continuation reading was therefore available to that diagnosis, and it did not change the conclusion. The objection is about generalization. A requirement that executors never fail is tolerable only while the executors are few. P2464R0 puts the count at dozens for the Networking TS against thousands for a standardized executor.

Three things in the record answer part of the objection. First, P3941R4's requirement is not an abstraction offered to programmers. It is a constraint on one algorithm and one type-erased scheduler, checked during compilation. P3941R4 also surveys the four schedulers of the working draft instead of leaving the requirement open-ended. Second, P2469R0 argued in 2021 for adaptation instead of a channel. An executor whose submission can fail binds a failure handler and presents the tail-call interface that the customization point requires. The failure then reaches whoever composed the operation, and not the resumed coroutine. That answer addresses the error-channel diagnosis and not the generalization objection, and the present author co-wrote the paper that makes it. Third, P2464R0's own minimal remedy replaces the P0443 executor in the Networking TS model with a scheduler, and polls 2 and 4 encouraged that direction. P2453R0's guidance to the Networking Study Group records that networking papers were to address security and the sender/receiver model before a return to Library Evolution.

The record does not answer the scope question itself. Section 6.2 records that P3941R4 leaves it open as well.

The remaining disagreement is whether the failure should be reportable or absent. Section 3.3.2 of P3941R4 shows that the reportable answer is available. The objection therefore survives a denial that a suspended caller can be told anything. What holds under both answers is narrower: Neither one returns the caller to the agent that it was promised. That is the condition that section 5 compares.

## 7. Conclusion: The Profile Recurs Without Being Derived

One reading ties the channel profile of a scheduling operation to the state of the caller that it serves. A caller that runs can act on an error, and needs a channel to receive one. A caller that is suspended cannot act on one until it resumes.

The record supports a narrow form of that reading. Three designs give the operation that resumes a caller no typed error channel. P0443R14 does this through a `void` return that left no room for one. P3941R4 does it through completion signatures that exclude `set_error` from every scheduler used with `affine_on`. P4003R3 does it through an argument type that carries a coroutine handle and a list pointer, and no place for a value or an error. The encodings differ, the scopes differ, and in P3941R4 the cancellation channel survives wherever a stop of the awaiting operation is possible. What does not differ is that none of the three lets the resumption report a failure in the type.

The profile is not a property of scheduling operations in general. Section 3 records two schedulers of the working draft whose `schedule` operation currently declares `set_error_t(std::exception_ptr)`: `run_loop::run-loop-scheduler` and `parallel_scheduler`. P3941R4 excludes such a scheduler from `affine_on`, from the constructor of `task_scheduler`, and therefore from `task`, and leaves it available elsewhere. What recurs across the three operations compared here is therefore not the shape of scheduling as such. It is the shape of the operation that promises to resume a caller on a particular agent.

The record also shows the limits of that reading. P2464R0 analyzed executors that run continuations and asked for a channel notwithstanding. P3941R4 specifies a fallible alternative that it rejected, and states a path to relax the constraint later. In P0113R0 the continuation relationship belonged to `defer` and not to all three submission primitives. The committee record also has two halves. The missing error channel appears in the voters' comments that P2453R0 preserves under polls 1 and 2. It appears in none of the chairs' summaries of the five. What the committee is on record as having decided about it therefore depends on which half a reader takes.

The same profile appears in three encodings that share no vocabulary: a `void` return, a set of completion signatures, and an argument type. The designs are less separate than their encodings. P0443R14 specifies both the one-way executor and a design for senders and receivers, and names the two together as its subject (section 1.2). P2300R10's introduction states that it is "based on the ideas in A Unified Executors Proposal for C++ and its companion papers", so the second column descends from the first column's document. P4003R3 attributes its execution model directly to Boost.Asio, from which P0443R14's Networking TS executors also descend. The recurrence is therefore not a property of one model's expressiveness, and it is not evidence of three separate arrivals either.

Two of the three inherit the profile rather than arrive at it. P0443R14 and P4003R3 both descend from Asio. The affinity guarantee that P3941R4 constrains has two precedents in P3552R3's own survey of prior work: libunifex, whose `unifex::task<T>` is scheduler affine, and stdexec, whose `exec::task` P3552R3 describes as "also scheduler affine" (sections 2.4 and 2.5). P3552R3 names those two and Folly as influences on its design (section 7).

The precedent covers the guarantee and not the constraint. P3552R3 records neither surveyed implementation as one that requires the schedulers that deliver affinity to be infallible. Its own wording for `affine_on` admits a failure and says where it is reported. P3941R4 introduces the requirement, strikes that sentence, sets the requirement against the fallible alternative in its section 3.3.2, and chooses. What P3941R4 supplies, then, is a reason rather than a precedent. Its stated ground to exclude `set_error` refers to the situation of the caller. A failed scheduling operation leaves the execution agent on which it resumes unclear. That rationale is the strongest support in the record for the reading. It is one paper's rationale and not an independent derivation.

The sources already name two consequences. P3941R4 records that all current standard schedulers can be made infallible except, possibly, `parallel_scheduler`. That exception would put `parallel_scheduler` outside the set usable with `affine_on`, and therefore outside the set usable with `task`. P3941R4's relaxation path would also need a matching mechanism in `task` before a fallible scheduler could drive an affine coroutine. Both questions fall to the authors of P3941R4's successors, and to anyone who proposes a fallible scheduler for this role. The record assembled here is where such a paper starts.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author, with Steve Gerbino, developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[17]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[18]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the adoption of the coroutine model.

The intent of this paper is informational. It places a comparison in the record and requests nothing.

P4003R3, one of the three designs compared in section 5, is the author's own proposal. The work and continuation framings applied throughout are also the author's, from P4094R1, P4095R1, and P4096R1. The author is one of the five authors of P2469R0, the 2021 response to P2464R0. This paper therefore revisits a dispute in which the author was a named party, on the side that the continuation reading favors. Of the eighteen references, five are papers that the author wrote or co-wrote, and two are software that the author maintains.

One limitation of the method: P4003R3 is the author's own proposal, and it attributes its execution model directly to Boost.Asio. Its column in section 5 therefore records descent as much as separate agreement.

This paper belongs with P4094R1, P4095R1, and P4096R1.

Selection: The three operations compared in section 5 were chosen on two grounds. The specification of each one fixes its channel profile in the type. The three do so by unrelated mechanisms: a `void` return, completion signatures, and an argument type. The designs themselves are not unrelated, and two of them descend from Asio. The three are not a survey of scheduling operations either. Section 3 names two schedulers of the working draft that fix no such profile.

Method: Every claim about a cited paper was checked against that paper's own published text, with a section number given wherever a quotation is used. Poll outcomes and tallies come from P2453R0's table of outcomes. The voters' reasons come from its section 4, which records selected comments per poll.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

## Acknowledgments

The author thanks Dietmar K&uuml;hl for P3941R4. That paper supplied the *infallible-scheduler* concept, the `task_scheduler` mandate, and the fallible-scheduler alternative that section 6.2 answers. The author thanks Christopher Kohlhoff for the continuation framing in P0113R0 and for the Networking TS, and Ville Voutilainen for P2464R0.

Thanks also to Robert Leahy for P4151R1, and to Eric Niebler, Kirk Shoop, Lewis Baker, and Lee Howes for P1525R0. The nine authors of P2300R10 built the model that answered the deficiencies P1525R0 identified. Steve Gerbino and Mungo Gill co-developed the coroutine executor in P4003R3.

## References

[1] [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[2] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Daisy Hollman, Lee Howes, Kirk Shoop, Lewis Baker, Eric Niebler, 2020).

[3] [P0443R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0443r10.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, David Hollman, 2019).

[4] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[5] [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not." (Jamie Allsop, Vinnie Falco, Richard Hodges, Christopher Kohlhoff, Klemens Morgenstern, 2021).

[6] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution and Concurrency Networking and Executors Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[7] [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[8] [P0113R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0113r0.html) - "Executors and Asynchronous Operations, Revision 2" (Christopher Kohlhoff, 2015).

[9] [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[10] [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).

[11] [P0688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0688r0.html) - "A Proposal to Simplify the Unified Executors Design" (Chris Kohlhoff, Jared Hoberock, Chris Mysen, Gordon Brown, 2017).

[12] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[13] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[14] [P4151R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4151r1.pdf) - "Rename affine_on" (Robert Leahy, 2026).

[15] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[16] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[17] [Capy](https://github.com/cppalliance/capy) - IoAwaitable protocol implementation (Vinnie Falco, Steve Gerbino).

[18] [Corosio](https://github.com/cppalliance/corosio) - Coroutine-native I/O library (Vinnie Falco, Steve Gerbino).
