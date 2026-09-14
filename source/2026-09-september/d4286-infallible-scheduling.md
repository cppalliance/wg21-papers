---
title: "Infallible Schedulers: What Unconditional Task Affinity Costs"
document: P4286R0
date: 2026-09-01
intent: info
audience: SG1, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Making scheduler affinity checkable at compile time bars the working draft's thread pool scheduler from the role a `task` resumes on, and removes the error channel of two other schedulers from every algorithm.

A `task` coroutine promises that it resumes on the execution agent it suspended on, and `affine_on`, the adaptor that carries it back, can fail at three points. Two mechanisms close one of those points, the return step itself: a concept that excludes an error completion, and an unstoppable receiver that excludes a stopped one. So what a caller gives up is the ability to observe a failed return trip rather than a failed `co_await`. Because `parallel_scheduler` is expected to stay fallible, it cannot be the scheduler a `task` resumes on, though a task can still reach the pool by awaiting work sent to it. Only the concept check is confined to that role. The constructor mandate on `task_scheduler` and the signature rewrites that make it and `run_loop`'s scheduler admissible reach programs that never name a coroutine, and both schedulers lose `set_error` in every environment and so in every algorithm, `on` and `sync_wait` included.

---

## Revision History

### R0: September 2026

- Initial revision.

---

## Introduction

[P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html)<sup>[1]</sup> constrains the scheduler that a `task` coroutine resumes on. The scheduling operation that returns the coroutine to its own execution agent may declare no error completion, and compilation rejects a scheduler that declares one. Section 1 locates that constraint inside the operation, section 2 states how the closure is encoded and how far the encoding reaches, and section 3 enumerates the cost. Section 4 answers the objections the result raises.

The sender/receiver model answered a deficiency that three documents had named in the one-way executor: a failure between submission and execution with no channel on which to report it. [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf)<sup>[2]</sup> named it in 2019, [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html)<sup>[3]</sup> named it in its own section 1.4 in 2020, and [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[4]</sup> named it for the Networking Technical Specification (TS) in 2021. [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[5]</sup> made every completion an operation declares part of its type, which is the general answer. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[6]</sup> adds `task`, a coroutine type that resumes on the scheduler it suspended on, and P3941R4 supplies the constraint that guarantee needs. [P4151R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4151r1.pdf)<sup>[7]</sup> proposes a new name for the adaptor named `affine_on` in its sources, which is the name used throughout here.

Contributions:

1. The three points at which an `affine_on` operation can fail, which one P3941R4 closes, the two separate mechanisms that close it, and the execution agent that delivers each completion that survives.
2. The encoding of the constraint as three changes of two reaches: a concept check confined to `affine_on`'s start scheduler, and two changes that are not confined to it, the constructor mandate on `task_scheduler` and the signature rewrites that remove `set_error` from two standard schedulers in every algorithm.
3. The cost P3941R4 records: the standard scheduler it expects to fail the constraint, the two schedulers that give up their error completions to meet it, the opt-out that does not exist for a coroutine needing a fallible scheduler, and the mechanism `task` would need before the constraint could be relaxed.

Assumptions:

1. P3941R4's stated rationale is taken at its word. The constraint exists so that `affine_on` can guarantee scheduler affinity.
2. P3941R4's proposed wording is read as proposed, against the working draft it targets.
3. The completion signatures of an operation are the interface generic code programs against, so a failure absent from that set is a failure generic code cannot handle.

## 1. An `affine_on` Operation Can Fail at Three Points and Report Two

`affine_on` is the adaptor through which a `task` returns to its own scheduler after a `co_await`. The constraint P3941R4 adds closes one point in that adaptor and leaves two open, so this section locates all three before section 2 states how the closure is encoded.

P3941R4 provides more than the constraint. It supplies `get_start_scheduler`, a query that yields the scheduler an operation was started on, and it makes that scheduler a requirement rather than an inference. It changes the shape of `affine_on`, which previously took the scheduler as a second argument. It removes `change_coroutine_scheduler`, whose scheduler changes persisted to the end of the coroutine. It adds a `transform_sender` customization that lets `affine_on` elide the scheduling operation entirely for senders known to complete on the agent they started on, so for such an await none of the failure points below need arise. The permission is soft: The wording leaves it unspecified whether a standard sender offers the member the elision keys on, and names `just`, `just_error`, `just_stopped`, `read_env`, and `write_env` only under Recommended Practice. Between them those changes answer five United States national body comments on `affine_on`, US 232-366, 233-365, 234-364, 235-363, and 236-362, whose underlying issues [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[8]</sup> discusses.

Where P3552R3 wrote `affine_on(sndr, sch)`, P3941R4 strikes the scheduler parameter and obtains the scheduler from the receiver instead, through `get_start_scheduler` (sections 3.1, 3.2, and 3.8). The operation therefore has a child sender and a scheduling operation built from the start scheduler, connected to two internal receivers: one that stores the child's result and starts the scheduling operation, and one for the scheduling operation whose stop token is unstoppable. The stored result is forwarded to the external receiver at the end.

Section 3.6 specifies the order in which those pieces run. The scheduling operation state is created when `affine_on` is connected, before any work starts, so a failure to build it is reportable: The main work has not started and the agent has not changed. P3941R4 draws that consequence in section 3.3, writing that when `connect(schedule(sch), rcvr)` throws, "`affine_on` can avoid starting the main work and fail on the execution agent where it was started". The child is then started on the current agent, and two consecutive items of section 3.6's enumeration state what follows:

> "Upon completion of the child operation the kind of completion and the parameters, if any, are stored. If this operation throws, the storage is set up to be as if `set_error(current_exception)` were called. Once the parameters are stored, the scheduling operation is started. Upon completion of the scheduling operation, the appropriate completion function with the respective arguments is invoked."

That ordering fixes an acceptance boundary. Once the scheduling operation starts, it is the only route back. The child has already completed, its result sits in storage, and the receiver waits on an agent the operation promised to return it to. A scheduling operation that completes with `set_error` has no agent on which to deliver that error, which is the rationale P3941R4 gives (section 3.3):

> "However, if this scheduling operation fails, i.e., it completes with `set_error(e)`, or if it gets cancelled, i.e., it completes with `set_stopped()`, the execution agent on which the scheduling operation resumes is unclear and `affine_on` cannot guarantee its promise. Thus, it seems reasonable to require that a scheduler used with `affine_on` is infallible, at least when used appropriately (i.e., when providing a receiver whose associated stop token is an `unstoppable_token`)."

The child's own failure is a separate case, and it survives the constraint. P3941R4 states this in the same section: "Note that `affine_on` can fail and get cancelled (due to the main work failing or getting cancelled) but `affine_on` can still guarantee that execution resumes on the expect execution agent when it uses an infallible scheduler." That error is delivered after the rescheduling succeeds, and therefore on the scheduler the task started on.

Two mechanisms close the third point, and they are not the same mechanism. The concept of section 2 excludes `set_error`. A `set_stopped` from the scheduling operation is excluded separately, because section 3.6 requires the receiver that `affine_on` connects the scheduling operation to carry an `unstoppable_token`, and the proposed default implementation wraps the start scheduler: For an `UNSTOPPABLE-SCHEDULER` `e` wrapping a scheduler `sch`, `schedule(e)` is `unstoppable(schedule(sch))`. The distinction matters inside a `task`, where the environment's stop token is an `inplace_stop_token` and is therefore stoppable: The concept alone would admit a `set_stopped` there, and the unstoppable receiver is what keeps it out.

Table 1: The three points at which an `affine_on` operation can fail, in the order of section 3.6, with what reaches the receiver and on which agent. Only the third point is closed.

| Point | How it fails | What reaches the receiver | Agent |
| --- | --- | --- | --- |
| Building the scheduling operation state, during `connect` | Allocation or `connect` throws | The main work never starts, and P3941R4 states that `affine_on` can fail here | "the execution agent where it was started" (section 3.3) |
| The awaited work completes | `set_error` or `set_stopped` from the child | The child's own completion, stored and then forwarded | The scheduler the task started on |
| The scheduling operation completes | `set_error(e)`, or `set_stopped()` | Neither. The concept excludes `set_error`; the unstoppable receiver and `UNSTOPPABLE-SCHEDULER` exclude `set_stopped` | None |

Two of the three points remain reportable, and the one that closes is the step that carries the receiver back to its agent. A caller that loses this channel keeps the ability to observe a failed `co_await`. What it gives up is the ability to observe a failed return trip.

## 2. The Concept Closes the Scheduling Step During Compilation

The constraint is not a run-time contract on the scheduling operation. It is a concept the scheduler's completion signatures satisfy or fail, checked in two places. This section states the encoding, the scope, and the wording P3941R4 strikes to match.

The exposition-only concept added to [exec.sched] admits two completion signature sets and excludes `set_error` from both:

```cpp
template <class Sch, class Env>
concept infallible-scheduler =
    scheduler<Sch> &&
    (same_as<completion_signatures<set_value_t()>,
             completion_signatures_of_t<
                 decltype(schedule(declval<Sch>())), Env>> ||
     (!unstoppable_token<stop_token_of_t<Env>> &&
      (same_as<completion_signatures<set_value_t(), set_stopped_t()>,
               completion_signatures_of_t<
                   decltype(schedule(declval<Sch>())), Env>> ||
       same_as<completion_signatures<set_stopped_t(), set_value_t()>,
               completion_signatures_of_t<
                   decltype(schedule(declval<Sch>())), Env>>)));
```

The second set, which permits `set_stopped_t()`, is available only where the environment's stop token can be stopped. Both rejections happen during compilation, and they attach to different things. The first attaches to the algorithm: [exec.affine.on] paragraph 5 makes `get_completion_signatures` exit with an exception when the start scheduler does not satisfy the concept. The second attaches to a type: The constructor of `task_scheduler` carries `Mandates: Sch satisfies infallible-scheduler<env<>>`. The stop token of `env<>` is a `never_stop_token`, which is unstoppable, so the strict set is the only one that constructor accepts, and inside an `affine_on` the environment may be stoppable, which is why section 1 gives a separate mechanism for `set_stopped` there.

P3941R4 also removes the error path from the wording that described it. [exec.affine.on] paragraph 5 had carried a sentence, put there by P3552R3, sending a scheduling failure to the receiver on an unspecified execution agent. P3941R4 strikes it. The same paper rewrites the completion signatures of `task_scheduler`'s exposition-only sender from `set_value_t()`, `set_error_t(error_code)`, `set_error_t(exception_ptr)`, and `set_stopped_t()` to a form that depends on the environment: `set_value_t()` alone where the environment's stop token is unstoppable, and `set_value_t()` with `set_stopped_t()` otherwise. It rewrites `run_loop`'s sender the same way, from `set_value_t()`, `set_error_t(exception_ptr)`, and `set_stopped_t()`.

The analogous sentence survives in [exec.on] paragraph 9: "If any scheduling operation fails, an error completion on `out_rcvr` shall be executed on an unspecified execution agent." `on` makes a related promise, remembering the scheduler an operation was started on and transferring execution back to that scheduler's execution resource, and it keeps its error completion while doing so. What the two algorithms are taken to promise separates them, though the normative text does not say so on its face. [exec.on] paragraph 9 promises transfer back to an execution resource and does not promise that an error completion lands there. [exec.affine.on] paragraph 5 uses the same resource-level language, and it is P3941R4's rationale, quoted in section 1, that reads the promise at the grain of the execution agent. The distinction the strike rests on therefore sits in the rationale rather than in the paragraph it edits. The paragraph is in fact left weaker than that: The same edit strikes the scheduler parameter from `affine_on(sndr, sch)` while leaving two later references to *sch* standing, so the surviving text names a scheduler it no longer introduces.

One of the three changes is confined to the `affine_on` role and two are not. The concept check on `affine_on`'s start scheduler is confined: It governs what a `task` may resume on and leaves `on` and every other use of a scheduler alone. The mandate on `task_scheduler`'s constructor is not. `task_scheduler` is a general type-erased scheduler, so `task_scheduler sch(parallel_scheduler{});` becomes ill-formed in any program, including one that writes only `sync_wait(on(sch, work))` and never names `task` or `affine_on`. The signature rewrites are not confined either: `run_loop::run-loop-scheduler` and `task_scheduler` lose `set_error` from their senders in every environment and therefore in every algorithm that consumes them, `on` and `sync_wait` included.

## 3. The Cost Is a Scheduler a `task` Cannot Resume On and Two Channels the Draft Loses

A constraint checked during compilation has a cost that can be counted: the set of schedulers a `task` can resume on, and the channels the working draft gives up to enlarge that set. P3941R4 surveys the four schedulers of the working draft, and the items below come from that survey and from its proposed wording.

Three of the four can meet the constraint, and P3941R4's wording makes two of them meet it. `inline_scheduler` already completes with `set_value()` alone. `task_scheduler` reduces to allocation during `connect`, which the section 3.6 ordering performs before anything starts. `run_loop::run-loop-scheduler` currently permits `set_error_t(std::exception_ptr)`, a permission that lets an implementation use `std::mutex` and `std::condition_variable`, and P3941R4 observes that the same logic admits an implementation in atomic operations that cannot throw.

The fourth is `parallel_scheduler`, the working draft's interface to a replaceable thread pool implementation. Its interface permits `set_error_t(std::exception_ptr)` and `set_stopped_t()`, and P3941R4 writes of it: "It seems unlikely that this interface can be constrained to make it infallible." The proposed wording changes `task_scheduler` and `run_loop` and leaves `parallel_scheduler` as it stands. Under P3941R4 as written, therefore, the working draft's own thread pool scheduler fails the concept, and a `task` cannot be started on it.

What that forbids is narrower than losing the pool, and the line falls in an awkward place. The concept check reads `get_start_scheduler(get_env(out_rcvr))`, the task's own scheduler, and never inspects a scheduler named inside an awaited sender. A task started on an admissible scheduler may therefore `co_await on(parallel_scheduler{}, sndr)` for a plain sender `sndr`: The work runs on the pool, and a scheduling failure inside that child reaches the receiver as the child's own completion, which is the second row of Table 1. Nesting a coroutine is the case that fails. Both `starts_on(parallel_scheduler, nested_task)` and `on(parallel_scheduler, nested_task)` make the nested task's own start scheduler `parallel_scheduler`, so its `task_scheduler` construction is ill-formed ([task.state] paragraph 4).

That boundary runs against P3941R4's own advice. Section 3.5 removes `change_coroutine_scheduler` and offers nesting in its place, writing that "replacing the used scheduler for an existing `task` by nesting it within `on(s, t)` or `starts_on(s, t)` is fairly straightforward" and giving `co_await ex::starts_on(s, [](parameters)->task<T, E> { logic }(arguments));` as the form. For the one standard scheduler the same paper expects to stay fallible, the recommended replacement does not compile. Work still reaches the pool; a coroutine that runs on it does not.

P3941R4 states the general form of that consequence directly (section 3.3):

> "In general it seems unlikely that all schedulers can be constrained to be infallible. As a result `affine_on` and, by extension, `task` won't be usable with all schedulers if `affine_on` insists on using only infallible schedulers. If there are fallible schedulers, there aren't any good options for using them with a `task`."

Two routes past the constraint exist, and P3941R4 states the cost of both. The first is adaptation, which section 4.1 takes up. The second is an opt-out, and it does not exist yet. Inside a `task` the only route past `affine_on` in the proposed wording is the start scheduler type being `inline_scheduler`, which skips the adaptor instead of relaxing it ([task.promise] paragraph 9). Section 3.3.3 describes what a relaxation would take. The constraint "can be relaxed in a future revision of the standard by explicitly opting out of that constraints, e.g., using an additional argument", and P3941R4 adds: "For `task` to make use of it, it too would need an explicit mechanisms to indicate that its `affine_on` use should opt out of the constraint, e.g., by adding a suitable `static` member to the environment template argument."

The survey also settles what the other two schedulers give up to qualify. Neither `run_loop::run-loop-scheduler` nor `task_scheduler` withholds its error channel only in the `affine_on` role while keeping it elsewhere. The wording strikes `set_error` from their senders outright, so `on`, `sync_wait`, and any other consumer of those senders sees an operation that declares no error either. Making two schedulers admissible to one algorithm removes a typed completion from every algorithm that uses them.

What decides the survey's outcome, then, is the proposed wording rather than the concept. The concept states a test; which schedulers pass it is settled by the signature rewrites P3941R4 applies to two of them and withholds from the third.

## 4. Expected Objections

Three objections bear on sections 2 and 3. Each is stated in the form an objector would use, and answered from evidence already presented.

### 4.1 "A fallible scheduler can be adapted"

The constraint excludes a scheduler from the role a `task` resumes on, and it does not exclude the execution resource behind it. A user who wraps a fallible scheduler in an adapting scheduler that never reports failure satisfies the concept and keeps the pool.

P3941R4 states the cost of that adaptation in section 3.3.1, and gives it two forms. The first transforms a scheduling failure into a call to `std::terminate`. The second resumes on an agent the adapting scheduler can reach infallibly, which need not be the agent the task was started on:

> "In that case the scheduling operation would just succeed without necessarily running on the correct execution agent. However, there is no indication that scheduling to the adapted scheduler failed and the scheduler affinity may be impacted in this failure case."

Neither form preserves what the constraint exists to guarantee. The first ends the program instead of resuming the coroutine; the second resumes it on the wrong agent and reports nothing. The comparison worth drawing is with the wording before the strike, under which a fallible scheduler could be used directly and its failure reached the receiver as an error completion. P3941R4 removes that route, so the same failure now reaches the receiver only through an adaptation the user writes, and the second form of that adaptation reports nothing by construction. P3941R4 adds that the standard library provides no easy way to adapt a scheduler, though it can be done. Under either form the failure leaves the type system and stays in the program.

### 4.2 "The constraint is scoped, and a future revision can relax it"

A scheduler's `schedule` keeps its error channel in the model generally. P3941R4 offers the fallible alternative in its own section 3.3.2, where `affine_on` completes with `set_error(rcvr, scheduling_error{e})` and the wrong-agent outcome becomes detectable instead of prohibited, and section 3.3.3 offers to relax the constraint later. A design decision presented with its alternative and an exit is a scoped tradeoff.

Neither half holds as stated. On scope, section 2 records that only the concept check on `affine_on`'s start scheduler is confined to the role: The mandate on `task_scheduler`'s constructor and the signature rewrites to `run_loop` and `task_scheduler` reach programs that never name `task` or `affine_on`. On the exit, section 3.3.2's alternative is available to a future revision, and section 3.3.3 states the two changes it needs, an opt-out on `affine_on` and a second mechanism on `task`'s environment template argument before a coroutine could use it. Neither is proposed here. An exit that two unwritten changes stand behind is a plan, and the wording in front of the committee is the unconditional form.

### 4.3 "An infallible scheduler has no failure to report"

The constraint does not silence a report of a failure that occurs. It admits only schedulers whose scheduling operation cannot fail, and for such a scheduler an error completion would be dead weight in the type. On this reading nothing is lost, because `set_error` is removed only where it could never be sent.

The reading holds for one of the two schedulers that can fail and not for the other, and the difference is worth stating in P3941R4's own terms. `run_loop::run-loop-scheduler` may fail so that an implementation can use `std::mutex` and `std::condition_variable`, and P3941R4 observes that the same logic admits an implementation in atomic operations that cannot throw. For that scheduler the objection largely lands: What the working draft gives up is implementation freedom and a declared signature, not a failure a conforming program could count on seeing. `parallel_scheduler` is the harder case, because P3941R4 expects its interface to stay fallible, so the failure is real and what is given up is affinity to it. The objection therefore narrows the cost rather than dissolving it, and section 3 is where the remainder sits.

## 5. Conclusion: One Static Check, and What the Draft Gives Up for It

Scheduler affinity is a run-time promise, and P3941R4 turns it into a property a compiler can check. That is the achievement, and the sections above take it as given. What the record then shows is the cost, which the proposing paper names in two forms.

The first is affinity. A scheduler whose `schedule` can fail cannot be the one a `task` resumes on, so `parallel_scheduler` is expected to sit outside that set, and adapting it by hand leads to `std::terminate` or to a resumption on the wrong agent with nothing reported. The pool itself stays reachable, through `co_await on(parallel_scheduler{}, sndr)`, whose failures arrive on the awaited side; what is barred is a coroutine that runs on it, including the nesting idiom P3941R4 section 3.5 recommends in place of the `change_coroutine_scheduler` it removes. The second cost is the working draft's own vocabulary. Two schedulers were made admissible by striking `set_error` from their senders outright, so `run_loop::run-loop-scheduler` and `task_scheduler` now declare no error to any algorithm, `on` and `sync_wait` included, and `task_scheduler`'s constructor mandate makes wrapping a fallible scheduler ill-formed in programs that never mention a coroutine. Only the concept check on `affine_on`'s start scheduler is confined to the role it was written for. A reading on which the constraint stops at `affine_on` accounts for one of the three changes.

Neither cost is permanent, and neither is presently escapable. Section 3.3.2 of P3941R4 sketches a fallible `affine_on` under which a resumption on the wrong agent would become something a caller can detect, and section 3.3.3 sets out the opt-out that would relax it. Reaching that alternative takes two changes nobody has written: the opt-out itself, and a mechanism on `task`'s environment before a coroutine could reach it. Until those exist, a `task` resumes on the schedulers the concept admits, and the committee is voting on the unconditional form.

The ordering in section 3.6 is what a delegate can check first and fastest. It puts the connect before the work and the rescheduling after it, so a failure to build the operation state is reportable, an awaited operation's own error is reportable on the right agent, and only the return trip is closed. The next document on the subject is the one that constrains `parallel_scheduler`, or writes the opt-out, or shows that a scheduler which cannot report a failure is a scheduler worth having.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author, with Steve Gerbino, developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[9]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[10]</sup>, coroutine-native I/O libraries under the C++ Alliance. The author has a stake in the adoption of the coroutine model.

The intent of this paper is informational. It places an analysis in the record and requests nothing.

The author is the lead author of [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[11]</sup>, a coroutine execution model that competes with the design analyzed here, and one of the five authors of [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[12]</sup>, the 2021 response to P2464R0, and therefore a named party to the dispute in which the executor error channel was argued.

One limitation of the method: The paper reads P3941R4 as written, against the working draft it targets. P3941R4 is at revision 4, and any later revision supersedes the readings here.

This paper belongs with [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[13]</sup>, [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[14]</sup>, and [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[15]</sup>.

Method: Every claim about a cited paper was checked against that paper's own published text, with a section or paragraph number given wherever a quotation is used. The wording claims in section 2 were read from P3941R4's proposed wording, including which sentences it marks as struck.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

## Acknowledgments

The author thanks Dietmar K&uuml;hl for P3941R4, which supplied the *infallible-scheduler* concept, the `task_scheduler` mandate, the survey of the four standard schedulers, and the two adaptation options section 4.1 answers. The author thanks Ville Voutilainen for P2464R0, which named the deficiency for the Networking TS.

Thanks also to Robert Leahy for P4151R1, which proposes the rename this paper follows its sources in not adopting, and to Eric Niebler, Kirk Shoop, Lewis Baker, and Lee Howes for P1525R0. The nine authors of P2300R10 built the model that answered the deficiency P1525R0 identified.

## References

[1] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[2] [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[3] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Daisy Hollman, Lee Howes, Kirk Shoop, Lewis Baker, Eric Niebler, 2020).

[4] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[5] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[6] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[7] [P4151R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4151r1.pdf) - "Rename affine_on" (Robert Leahy, 2026).

[8] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).

[9] [Capy](https://github.com/cppalliance/capy) (Vinnie Falco, Steve Gerbino, 2025).

[10] [Corosio](https://github.com/cppalliance/corosio) (Vinnie Falco, Steve Gerbino, 2026).

[11] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[12] [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not" (Jamie Allsop, Vinnie Falco, Richard Hodges, Christopher Kohlhoff, Klemens Morgenstern, 2021).

[13] [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[14] [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[15] [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).
