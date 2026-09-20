---
title: "A Reader's Guide to the September 2026 Mailing"
document: P4199R1
date: 2026-09-15
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Eight papers, built entirely from published documents, show how C++26 reached its ballot with sixteen of eighteen objections to contract assertions still open and an unanalyzed dangling reference in its asynchronous model.

This paper summarizes eight papers published in the September 2026 mailing. It is a reading guide: an executive summary that identifies the logical series within the collection, describes what each series delivers, and provides individual summaries of every paper. It asks for nothing.

---

## Revision History

### R1: September 2026

- Regenerated for the September 2026 mailing. R0 covered the ten papers of the August 2026 mailing; this revision covers the eight papers of the September 2026 mailing.
- Rebuilt the executive summary, the individual paper summaries, and the references from the September sources.

### R0: August 2026

- Initial version, covering the August 2026 mailing.

---

## 1. Executive Summary

These eight papers share a method before they share a subject: every claim resolves to a document with a number, a date, or a commit hash. One paper excludes committee minutes and reflector posts by rule and works from seven public sources spanning 2017 to 2026. Another pins each source claim to an immutable commit, stdexec at `2c56ffe7` and Beman.Execution at `a20a6f63`. A third quotes fifteen assertions with page numbers attached. Three series emerge: the record behind C++26 contract assertions, the asynchronous model the working draft already carries, and the procedural rules that governed both. Every author disclosure appears in the papers themselves, including coauthorship of the paper that asks national bodies to return the draft.

Three papers put the C++26 ballot in front of the national bodies as a question of record rather than a question of taste. P4238R1<sup>[1]</sup>, written by four committee participants including the chair who ran the sessions it examines, reconstructs how contract assertions reached the ballot without a single rule being broken: 63 papers handled in ten months, a majority merged into P2900<sup>[2]</sup> less than a week after publication, a Tokyo poll marked nonbinding with no result recorded, and a failed 1/17/10/18/14 poll absent from its own proposal's published history. Its remedy is arithmetic - seven No votes among twenty-six P-members, the mechanism that removed concepts from C++0x in 2009 and trivial relocation from C++26, at a price of one cycle. P4272R0<sup>[3]</sup> audits the twenty-two-author consolidated response and returns a split verdict: no response rated Unsupported or Contradicted, yet fifteen objections Partly Answered and one Unresolved, including a count of five implementation-defined properties against the seven the working draft itself indexes. P4240R0<sup>[4]</sup> resolves the build identifiers behind prototypes cited as evidence and finds that 151 of the last 300 GCC commits and 153 of 300 Clang commits carry the same address that appears in the proposal's reply-to field, more than twelve times the next most frequent author, then closes with eight falsifiable predictions. Read together, the three separate two claims that are usually fused: that the process was followed, and that the objections were answered.

Three papers examine the asynchronous model the working draft already carries, and one of them ends with an asynchronous read holding storage that has been freed. P4253R0<sup>[5]</sup> traces that outcome to a single line of C++26 wording - a variant emplace in [exec.let] that destroys the `let_value` predecessor operation state before the user's sender factory runs, where `then` keeps the same predecessor alive - and shows the factory shape is the only shape an Asio initiating function can take. Five asynchronous I/O contracts are quoted on the identical requirement, from Boost.Asio 1.92.0 through Windows `ReadFileEx`, `io_uring`, and POSIX `aio_read`, and four public implementations disagree today on the order of destruction: stdexec invokes the factory first, libunifex destroys first, Beman.Execution has not implemented the change. P4286R0<sup>[6]</sup> follows a different property across six years, setting the 2020 P0443R14<sup>[7]</sup> executor beside the infallible scheduler of P3941R4<sup>[8]</sup> and the coroutine executor of P4003R3<sup>[9]</sup> and finding the same absent error channel encoded three ways - as a `void` return, as completion signatures, and as a constrained argument type - with `run_loop`, the one concrete scheduler in the standard, already omitting `set_error_t`. P4255R0<sup>[10]</sup> walks all five ordered routes through `as_awaitable` to the generic fallback, branch 7.4, which connects the sender before readiness is ever asked and returns `false` from `await_ready` for every instance, then splits four properties normally collapsed into the word "synchronous" and tests them against an eager in-memory append, an overlapped `WSARecv`, and a buffered `read_some`. The series leaves a map of where lifetime, error reporting, and readiness are load-bearing in the standardized design, and notes that no document in the record analyzes the first hazard at all.

Two papers ask why the other six were necessary, and one of them supplies draft wording. P4195R0<sup>[11]</sup> derives the game that SD-4's rules induce, with formal payoff functions and three ordinal game matrices, and rebuilds five case histories with the numbers intact: the 57-20-27 plenary vote that carried `std::execution` alongside the chair's verdict that a numerically weak consensus is still a consensus, the October 2021 direction poll that settled networking on sender/receiver roughly fifteen months before any concrete sender/receiver networking API existed, and Oulu 2016, where plenary caught a default-comparison flaw that subgroup consensus had passed. An appendix reconstructs the P2900 record across nineteen months and finds rebuttals dated December 2025 preceding the opposition papers published in February 2026. P4302R2<sup>[12]</sup> isolates one mechanism and proposes one sentence of procedure: before a poll on an unmailed revision is recorded, the chair asks whether anyone objects, and a single objection keeps the tally out of the minutes while leaving the discussion, an informal poll, and a qualitative record of sentiment fully intact. Its evidence is chronological - an EWG poll of 16 strongly favor, 15 favor, and 2 against on P3100R7<sup>[13]</sup>, a revision that no mailing had yet carried, and six of nineteen tracked papers changing during a single meeting week - and its author observes that the rule would have bound his own papers equally.

The collection rewards three depths of reading, and each depth pays differently. A single paper supplies a specific artifact: P4253R0 alone gives a reproducible hazard, a Compiler Explorer example presented to LEWG before the wording was forwarded, and the exact line of wording that produces it. A series supplies something no member of it contains: the three contract assertion papers together let a reader distinguish procedural regularity from substantive resolution and check either one without asking anyone, and the three asynchronous papers together show a single design commitment propagating through lifetime, error reporting, and readiness in three unrelated corners of the specification.

Read across the clusters and a picture appears that no cluster produces alone. The October 2021 direction poll examined in P4195R0 and the returning executor property traced in P4286R0 are the same decision seen from the procedural end and the wording end. The nineteen-month P2900 reconstruction and the eighteen-response audit are the same record at two resolutions. The plenary disposition in P4253R0 whose three sentences are shared with 34 of the 38 LWG motions that day and the unmailed revision in P4302R2 are two observations about the same thing: what a record preserves, and what a later reader can therefore recover. The technical findings and the procedural findings in this mailing explain each other, and the explanation is only visible from above.

Three entry points suit three readers. A national body delegate preparing a ballot position should begin with P4238R1, which states the arithmetic, names two precedents for returning a draft, and puts the cost at one cycle, then continue to P4272R0 for the page-numbered audit that supports it. An implementer or library author working on senders and coroutines should begin with P4253R0, because the code compiles today, four shipping implementations disagree on the behavior, and no analysis of the hazard exists in the record. A delegate more interested in how the committee decides than in what it decides should begin with P4195R0 for the model and the five case histories, then read P4302R2 for the smallest concrete change that follows from it, complete with draft SD-4 wording and a narrow final-meeting exception.

---

## 2. Individual Papers

### 2.1. P4195R0 - WG21 Game Theory: The Culture That Emerges From SD-4

Adoption into the C++ standard is evidence that a proposal outlasted organized opposition, not that the design was best - and the record SD-4 requires cannot tell a later reader which of the two occurred. This report derives the game that SD-4's rules actually induce: consensus as a chair call rather than a finding that an objection was answered, poll tallies published without the minutes register of opposing argument that ISO/IEC Directives clause 2.5.6 describes, and repeat players who know they will face each other for decades. Five case histories are rebuilt from the public record with the numbers intact - the 57-20-27 plenary vote that carried `std::execution` and the chair's verdict that a numerically weak consensus is still a consensus, the October 2021 direction poll that settled networking on sender/receiver roughly fifteen months before any concrete sender/receiver networking API existed, and Oulu 2016, where plenary caught a default-comparison flaw that subgroup consensus had passed. Formal payoff functions and three ordinal game matrices then explain why critical review is under-produced on exactly the proposals that need it most, why a competing design ends up votable only as an amendment to its rival, and why the rational play for a large feature is the smallest installable piece that forecloses the alternatives. An appendix reconstructs the P2900 contracts record paper by paper across nineteen months and finds the three-beat cycle of poll, opposition, rebuttal inverting by the third turn, with rebuttals dated December 2025 preceding the opposition papers published in February 2026; the paper asks for nothing, and closes with a falsifiable test its author invites others to run.

### 2.2. P4238R1 - Returning C++26 for the Evaluation It Skipped

Every C++ DIS ballot from C++11 through C++23 passed unanimously, and this paper asks the National Bodies to end that run by voting No on C++26. Four committee participants - among them the chair who ran the SG21 sessions the paper examines - reconstruct how Contracts reached the ballot without a single rule being broken: a roadmap clause that made forward motion the default, a Technical Specification path declined twice, 63 papers handled in ten months with a majority merged into P2900 less than a week after publication, and poll tallies recorded as consensus over standing Strongly Against blocs. The documentary findings are specific - a Tokyo poll the committee marked nonbinding and recorded no result for, reproduced in the authors' rationale paper beside polls that carry results, and a failed 1/17/10/18/14 poll on a successor proposal omitted from that proposal's own published history. The remedy is arithmetic: seven No votes among twenty-six P-members return the draft, the same mechanism that took concepts out of C++0x in 2009 and trivial relocation out of C++26, at a price the paper puts at one cycle.

### 2.3. P4240R0 - Who Needs P3400?

A proposal, P3400R4<sup>[14]</sup>, calls its own feature "essential" to the adoption of Contracts and cites compiler prototypes as evidence - this paper resolves the build identifiers and finds the prototypes live in the proposal author's personal GitHub forks, committed from his employer's address. The case is built entirely from quotable public sources, seven of them in chronological order from 2017 to 2026, with committee minutes and reflector posts excluded by rule: a paper titled "Business Requirements for Modules," a disclosure that management appointed personnel to verify ISO proposals against those requirements, a CTO-backed plan to deploy four "business-critical" features before ratification, and a parenthetical in which one company states it intends to fund the GCC and Clang implementations itself. The arithmetic is the sharpest part - of the most recent 300 commits on each fork, 151 on GCC and 153 on Clang carry the same corporate address that appears in the proposal's own reply-to field, more than twelve times the next most frequent author. From there the paper turns predictive, offering eight falsifiable statements about how an entity that needs this feature will behave in committee, each one testable against the record. The disclosure section is unusually candid: the author names his own co-authorship of a paper urging National Bodies to vote No on the C++26 DIS, and concedes that part of his evidence is personal observation no reader can check.

### 2.4. P4253R0 - Two Ends of One Dangling Reference: Coroutine Parameters and let_value Predecessors

Two senders with identical completion signatures compile against stdexec trunk with no diagnostic, and one of them hands an asynchronous read storage that has already been freed. The paper traces the difference to a single line of C++26 wording - a variant emplace in [exec.let] that destroys the `let_value` predecessor operation state before the user's sender factory runs, where `then` keeps that same predecessor alive for the whole operation - and shows that the factory shape is the only shape an Asio initiating function can take. Five asynchronous I/O contracts are quoted on the identical requirement, from Boost.Asio 1.92.0 through Windows `ReadFileEx`, `io_uring`, and POSIX `aio_read`, and a row-by-row table sets the hazard against the coroutine parameter problem, which has a note in the standard, an enforceable Core Guideline, and a Clang attribute where the `let_value` end has none. The record is assembled in eight items: four polls with no vote against, a plenary disposition whose three sentences are shared with 34 of the 38 LWG motions that day, a Compiler Explorer example of this exact hazard presented to LEWG before the wording was forwarded, and four public implementations that disagree on the order of destruction - stdexec invokes the factory first, libunifex destroys first, and Beman.Execution has not implemented the change at all. No document in the record analyzes the hazard, and the paper asks for nothing.

### 2.5. P4255R0 - Awaitables as the Natural Leaf Protocol for Coroutine-Centric Input/Output

A buffered read that already holds its bytes must still tell the coroutine language that it is not ready. P4255R0 walks all five ordered routes through `as_awaitable` and lands on the generic fallback, branch 7.4, which connects the sender before readiness is ever asked and then returns `false` from `await_ready` for every instance - branch 7.4 carries no preinitiation query for whether a particular operation already holds a buffered result. The paper splits four properties normally collapsed into the single word "synchronous" and tests them against three fixtures: an eager in-memory append, an overlapped `WSARecv` whose immediate completion becomes known only during initiation, and a buffered stream where one `read_some` object hits the user-space cache while the next must reach the network. Every source claim is pinned to an immutable commit - stdexec at `2c56ffe7`, Beman.Execution at `a20a6f63` - and the paper declines to overclaim: no benchmark result appears anywhere, the author discloses maintaining the awaitable-native Capy and Corosio, and the objections section concedes that a member `as_awaitable`, the forwarding await-completion adaptor, and domain transformation each escape the generic bridge, though never uniformly.

### 2.6. P4272R0 - Addressed but Unresolved: P3846R1's Eighteen Responses on C++26 Contract Assertions

A paper written to close eighteen objections to C++26 contract assertions closed two. P4272R0 audits P3846R1<sup>[15]</sup>, the twenty-two-author consolidated response, against the public record at two cutoff dates and returns a split verdict: on support the scores favor the authors, with no response rated Unsupported or Contradicted, while on resolution fifteen objections stand Partly Answered and one Unresolved. Table 2 quotes, with page numbers, the fifteen assertions the record does not support - a count of "exactly five implementation-defined properties" against the seven the working draft itself indexes, a claim that no deep-const proposal has ever been brought forward, and a categorical sentence that its own section falsifies one page later. The paper then measures the adoption arc against the ISO/IEC Directives' duty to attempt resolution in good faith, and against a five-part record of a discharged duty already in force at WG14, at ASTM, and in WG21's own Library Evolution group, which once found no consensus on a proposal carrying a better than two-to-one margin and saw it return four months later with strong opposition down from eleven votes to three. The author declares a material stake as a coauthor of the paper asking national bodies to return the C++26 draft.

### 2.7. P4286R0 - The Return of Networking TS Executors in P3552

The executor property that helped retire the Networking TS in 2021 returned in 2026 as a requirement: the schedulers driving the `std::execution::task` of P3552R3<sup>[16]</sup> must have no way to report a failure. The paper traces that reversal to a single distinction - scheduling work against scheduling a continuation - and argues that a suspended caller can be handed an error only by being resumed on an agent the failed operation could not select. A three-column table sets the 2020 P0443R14 executor beside the infallible scheduler of P3941R4 and the coroutine executor of P4003R3 and finds the same absent channels in all three, encoded in turn as a `void` return, as completion signatures, and as a constrained argument type. `run_loop`, the one concrete scheduler in the standard, already omits `set_error_t` entirely; three earlier papers named the framing distinction before P3941R4 was written, and P3941R4's own rationale, quoted verbatim, confirms it.

### 2.8. P4302R2 - Any Delegate May Object to a Poll on an Unmailed Revision

On 2026-06-10 EWG recorded a consensus poll - 16 strongly favor, 15 favor, 2 against - on a revision of P3100 that no WG21 mailing had yet carried, and that revision reached delegates only in the mailing published after the meeting ended. The proposal is a single procedural question: before a poll on an unmailed revision is recorded, the chair asks whether anyone objects, and one objection keeps the tally out of the minutes while leaving the discussion, an informal poll, and a qualitative record of sentiment fully intact. The evidence is chronological rather than rhetorical - six of the nineteen papers the author tracked into the March 2026 Croydon meeting changed during the week, and the adopted revisions of "Scheduler Affinity" and "Fix Sender Algorithm Customization" first appeared in the April mailing, one of them recorded 9 in favor and none opposed on wording that three other papers had already been rebased upon. The mechanism the paper isolates is a reversal of burden: under SD-4's two-to-one threshold, a design that arrives after the mailing becomes the status quo, so the absent stakeholder must assemble consensus to remove it rather than the proposer assembling consensus to add it. Draft SD-4 wording is supplied with a narrow final-meeting exception for wording corrections and feature removal, prior art includes the "Tentatively Plenary" state that LEWG supported 19 to 12 and short of consensus, and the author - who maintains competing `std::execution` proposals and discloses that conflict - observes that the rule would have bound his own papers equally.

---

## 3. Conclusion

This reading guide covers eight papers from the September 2026 mailing. The author hopes it helps the reader find the papers most relevant to their work and interests.

---

## Disclosure

The author provides information and serves at the pleasure of the committee.

This paper asks for nothing.

---

## References

[1] [P4238R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r1.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[2] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025).

[3] [P4272R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4272r0.pdf) - "Addressed but Unresolved: P3846R1's Eighteen Responses on C++26 Contract Assertions" (Vinnie Falco, 2026).

[4] [P4240R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4240r0.pdf) - "Who Needs P3400?" (Vinnie Falco, 2026).

[5] [P4253R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4253r0.pdf) - "Two Ends of One Dangling Reference: Coroutine Parameters and let_value Predecessors" (Vinnie Falco, 2026).

[6] [P4286R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4286r0.pdf) - "The Return of Networking TS Executors in P3552" (Vinnie Falco, 2026).

[7] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Daisy Hollman, Lee Howes, Kirk Shoop, Lewis Baker, Eric Niebler, 2020).

[8] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[9] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[10] [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf) - "Awaitables as the Natural Leaf Protocol for Coroutine-Centric Input/Output" (Vinnie Falco, 2026).

[11] [P4195R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4195r0.pdf) - "WG21 Game Theory: The Culture That Emerges From SD-4" (Vinnie Falco, 2026).

[12] [P4302R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4302r2.pdf) - "Any Delegate May Object to a Poll on an Unmailed Revision" (Vinnie Falco, 2026).

[13] [P3100R7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r7.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026).

[14] [P3400R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3400r4.pdf) - "Controlling Contract-Assertion Properties" (Joshua Berne, 2026).

[15] [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, Peter Bindels, Peter Dimov, Louis Dionne, Eric Fiselier, Mungo Gill, Pablo Halpern, Tom Honermann, Corentin Jabot, John Lakos, Nevin Liber, Lisa Lippincott, Ryan McDougall, Jason Merrill, Roger Orr, Nina Dinka Ranns, Ren&eacute; Ferdinand Rivera Morell, Oliver Rosten, Iain Sandoe, Hui Xie, 2025).

[16] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).
