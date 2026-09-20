---
title: "Correction Capacity: The Networking Arc Under Two Rule Sets"
document: P4239R0
date: 2026-07-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Five decisions, each locally reasonable, each producing the same initial outcome under either rule set. The difference is in the aftermath. SD-4 allows individually reasonable decisions to accumulate into an irreversible trajectory that no feedback mechanism can correct. The ISO Directives do not prevent any of the five decisions examined here. They prevent the open loop.

This paper applies the governance framework from [P4201R0](https://wg21.link/p4201r0)<sup>[1]</sup> to the networking timeline documented in [P4099R1](https://wg21.link/p4099r1)<sup>[2]</sup>. For each decision, it asks two questions: Would the initial decision differ under the ISO Directives? Would the aftermath differ? The answers form a gradient. At the early decisions (2014, 2019), the evidence for different outcomes is weak. At the later decisions (2021-2026), it is strong. The gradient is the finding.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[4]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[5]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

The author is the author of [P4201R0](https://wg21.link/p4201r0)<sup>[1]</sup>, the governance analysis this paper applies. The reader should be aware that this paper tests a framework the author constructed. If the framework fails the test, the author has an interest in not reporting that failure. The author reports the gradient honestly: The framework's predictions are weak at decisions 1-2 and strong at decisions 3-5.

The author is a co-author of [P2469R0](https://wg21.link/p2469r0)<sup>[6]</sup>, "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not," which argued in October 2021 that the Networking TS was more mature than P2300. The author had a prior published position on the relationship between the Networking TS and [P2300R10](https://wg21.link/p2300r10)<sup>[7]</sup>. The author no longer believes the Networking TS would have been right for C++. The author agrees with the committee's conclusion and disagrees with the rationale.

This paper asks for nothing.

---

## 2. The Thesis

The ISO Directives would not have prevented the committee from choosing senders over networking. The committee was entitled to make that technical judgment under either rule set. Each of the five decisions in the networking arc was locally reasonable. The people who made them were experienced practitioners working under real constraints.

What the ISO Directives would have prevented is the accumulation of individually reasonable decisions into an irreversible trajectory that no feedback mechanism can correct.

The Directives provide structural capacity to course-correct when accumulated consequences become visible:

- **Directive 2.5.6** - Consensus requires reconciliation of conflicting arguments. Objectors are directed to the appeal chain. No characterization of minority positions as inappropriate.
- **Directive 5.1** - Three-level appeal chain provides a structural remedy for the minority.
- **Directive 2.1.6** - Projects are cancelled after 5 years without progress.
- **Directive 1.12.1** - Fixed 3-year terms with NB confirmation create periodic accountability moments.
- **Directive 1.8.2d** - The chair sums up all views.

SD-4 removes every one of these mechanisms. No appeal chain. No forced reconciliation. No project cancellation requirement. No fixed terms. No constraint on the consensus ratchet. The result is that five individually reasonable decisions chain together into a decade without networking - and no structural mechanism exists to ask whether the trajectory achieved its claimed benefits.

The evidence supports this thesis with different strength at each decision point. The paper is honest about the gradient.

---

## 3. Decisions 1-2: Unification (2014) and the Cologne Pivot (2019)

### What Happened

In September 2014, SG1 directed three independent executor models - networking (Kohlhoff), GPU dispatch (Hoberock/Garland), and thread pools (Mysen) - to unify into a single abstraction. [N4199](https://wg21.link/n4199)<sup>[8]</sup> records the straw poll: "Start with Chris Mysen's proposal?" (SF:9 / WF:5 / N:4 / WA:0 / SA:2). The result was [P0443R0](https://wg21.link/p0443r0)<sup>[9]</sup> (2016), which went through fourteen revisions over four years and was never deployed as unified.

In July 2019 at Cologne, SG1 acted on three papers published simultaneously: [P1525R0](https://wg21.link/p1525r0)<sup>[10]</sup> (the diagnosis), [P1658R0](https://wg21.link/p1658r0)<sup>[11]</sup> (the prescription), and [P1660R0](https://wg21.link/p1660r0)<sup>[12]</sup> (the sketch). The poll to apply P1658's changes passed unanimously (SF:12 / F:13 / N:4 / A:0 / SA:0). The alternative approach - [P1791R0](https://wg21.link/p1791r0)<sup>[13]</sup> (Kohlhoff/Allsop) - failed to achieve consensus (SF:4 / F:6 / N:9 / A:7 / SA:6). SG1 directed [P0443R11](https://wg21.link/p0443r11)<sup>[14]</sup> to implement the changes.

### Would the Initial Decisions Differ?

No. SG1's straw poll in 2014 was a legitimate subgroup direction under either rule set. The Cologne votes in 2019 were legitimate consensus determinations. P1791 failed and P1660 passed. The committee is entitled to prefer one design over another under both SD-4 and the ISO Directives.

### Would the Aftermath Differ?

Moderately. Under the ISO Directives:

- **Directive 2.1.6** would impose a progress requirement on the unified executor project. P0443 persisted through fourteen revisions over six years (2016-2020) before being superseded. Under the Directives, the 5-year clock would have required a progress review.
- **Directive 2.5.6** would preserve the institutional standing of Kohlhoff's position after the Cologne vote. Under SD-4, the failed consensus on P1791 simply meant the paper did not advance - no further procedural remedy existed. The continuation framing dropped out of the published analysis permanently.

The ISO mechanisms here do not prevent the decisions. They prevent the decisions from becoming permanent without review.

---

## 4. Decision 3: The P2464R0 Diagnosis (2021)

### What Happened

In October 2021, Ville Voutilainen published [P2464R0](https://wg21.link/p2464r0)<sup>[15]</sup>, "Ruminations on networking and executors," on behalf of the Finnish National Body. The paper identified three deficiencies in [P0443R14](https://wg21.link/p0443r14)<sup>[16]</sup>'s `execute(F&&)` and concluded the Networking TS should be set aside. [P2469R0](https://wg21.link/p2469r0)<sup>[6]</sup> was published as a rebuttal. Both were presented at a joint LEWG/Concurrency telecon on October 4, 2021.

The procedural record from [cplusplus/papers#1113](https://github.com/cplusplus/papers/issues/1113)<sup>[17]</sup> documents the session:

- P2464R0 was presented for approximately 32 minutes.
- P2469R0 (the rebuttal) was presented for approximately 11 minutes.
- The chair - Bryce Adelstein Lelbach, a co-author of [P2300R10](https://wg21.link/p2300r10)<sup>[7]</sup> - recused from consensus determination on the subsequent polls. Ben Craig and Fabio Fracassi determined consensus.
- Five electronic polls followed.

The committee did not achieve consensus to kill the Networking TS outright (Poll 3: SF:13 / WF:13 / N:8 / WA:6 / SA:10 - no consensus). The guidance to the Networking Study Group was: Before bringing networking papers back to LEWG, address TLS/DTLS and the sender/receiver model.

### Would the Initial Decision Differ?

Possibly, but not certainly. P2464R0's analysis was procedurally correct under both rule sets - it analyzed the specification as written and identified real deficiencies in `execute(F&&)` under the work framing. The committee was entitled to evaluate it and vote.

### Would the Aftermath Differ?

Yes. The structural differences are mechanistically clear:

| Property | Under SD-4 | Under ISO Directives |
|---|---|---|
| P2469R0's arguments | Heard, then voted over | Reconciliation required (2.5.6) |
| Minority's remedy | Accept the outcome | Directed to three-level appeal chain (5.1) |
| Revisiting the direction | Characterized as "not appropriate" | No such characterization exists |
| Direction reversibility | Consensus ratchet locks it | No ratchet mechanism in the Directives |
| Outcome measurement | None required | Forced feedback (2.5.3, 2.6.5) |

Under the Directives, the P2469R0 authors would have been directed to the appeal chain rather than told their position "erodes credibility." The direction would not have become irreversible through a single poll. Reconciliation - substantive engagement with the minority's technical arguments, not merely a vote count - would have been required before declaring consensus.

---

## 5. Decision 4: The "Including Networking" Poll (2021)

### What Happened

[P2453R0](https://wg21.link/p2453r0)<sup>[18]</sup> documents the October 2021 electronic poll:

> "The sender/receiver model (P2300) is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs."
>
> SF:24 / WF:16 / N:3 / WA:6 / SA:3 - Consensus in favor.

The published voter comments include delegates who explicitly stated they could not evaluate the networking component:

> "I think this is a good basis for parallelism/GPUs but can't judge its suitability for networking." - Weakly Favor.
>
> "My vote is weakly in favor as I am not familiar enough with the networking requirements to be sure that it satisfies those." - Weakly Favor.

No published prototype of sender-based networking existed at the time of the vote. No deployment. One hypothetical example using a placeholder `NN::` namespace in [P2300R2](https://wg21.link/p2300r2)<sup>[19]</sup> Section 1.4.

### Would the Initial Decision Differ?

Probably not. The poll was electronic, reducing conformity pressure. The committee was entitled to express a directional preference. The Directives do not prohibit directional polls.

### Would the Aftermath Differ?

Yes. Under SD-4, the October 2021 poll became a direction lock. Five years later, the poll is still cited as the stated direction for networking. No sender-based networking has shipped. No mechanism requires asking whether the direction achieved its claimed benefits. The bird-in-hand doctrine gives structural priority to the direction set by this poll. Alternative proposals must overcome the heightened burden of "strong motivation" to revisit (see Section 7).

Under the ISO Directives:

- **No bird-in-hand doctrine.** A new paper with new evidence competes on equal procedural footing regardless of prior polls.
- **No irreversible direction lock.** A directional poll expresses preference; it does not foreclose alternatives.
- **Directive 2.1.6** would require measurable progress on the sender-based networking direction within 5 years - or the project lapses.

---

## 6. Decision 5: The Open Loop (2021-2026)

### The Fact

No sender-based networking has shipped. The procedural record from [cplusplus/papers#1447](https://github.com/cplusplus/papers/issues/1447)<sup>[20]</sup> documents the trajectory of [P2762R2](https://wg21.link/p2762r2)<sup>[21]</sup>, "Sender/Receiver Interface For Networking" (Kuhl, 2023):

- February 2023, Issaquah: one educational presentation. No polls taken.
- Marked "high priority (B1)" by LEWG.
- Current status: "Waiting to get the paper from SG4."

Five years from the October 2021 direction. Twenty-one years from [N1925](https://wg21.link/n1925)<sup>[22]</sup> (2005), the first networking proposal. Networking is not in the C++ standard.

### Under SD-4

No mechanism exists to ask "did this direction achieve its claimed benefits?" No revisit trigger was set. No outcome measurement was required. No project cancellation deadline applies. The direction persists indefinitely.

### Under ISO Directives

Directive 2.1.6 requires project cancellation after 5 years without progress. The sender-based networking direction, set in October 2021, would face mandatory review in 2026. The committee would be required to demonstrate progress - a paper, a prototype, a deployment, a vote forwarding wording to LWG - or the project lapses and the design space reopens.

The 5-year rule is unambiguous. The absence of progress is documented in the public record. This is the strongest evidence in the paper that the two rule sets produce different outcomes.

---

## 7. Coda: The Ratchet in 2026

On March 11, 2026, SG14 held its monthly Low Latency Finance telecon. The main agenda item was a review of [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[23]</sup>, "Open Issues in `std::execution::task`." The [meeting notes](https://lists.isocpp.org/sg14/att-1312/SG14_2026_03_11.pdf)<sup>[24]</sup> document the session. The room chair explicitly invited the P2300 authors.

A poll was taken:

> "I/O completions that carry both an error code and a byte count present a design challenge for the three-channel completion model."
>
> SF:8 / F:2 / N:0 / A:2 / SA:7
>
> Number of participants: 25. No consensus.

Zero neutral votes. The distribution is bimodal. The room chair's invitation to P2300 authors may or may not explain the distribution. The author notes this without drawing a conclusion.

Guy Davidson stated during the session:

> "2023 consensus means you need strong motivation, not that the door is permanently closed."

This is the SD-4 bird-in-hand doctrine stated by a senior committee member. Under the ISO Directives, no such heightened burden exists. A paper with new evidence competes on equal procedural footing regardless of prior polls. The Directives contain no first-mover doctrine.

Inbal Levi stated:

> "We are in NB comments time now... We are past the finish line."

Ville Voutilainen stated:

> "If someone finds a stinker at any point... we have the ability to fix that stinker, even if it requires removing half of the things we've adopted."

The claim that the process is self-correcting. The test: Five years from the "including networking" direction, no sender-based networking has shipped. The open loop persists.

The presenter stated:

> "This format is not very good for me because so many things were said that I'm not able to respond."

Multiple sequential rebuttals from four committee members, each raising distinct points, with no structured response opportunity. Under ISO Directive 1.8.2d, the chair is required to sum up all views. The format that produces one-against-many without response structure is not the format the Directives contemplate.

The ratchet is not historical. It operates in 2026.

---

## 8. The Accumulation

No single decision examined in this paper was wrong. The SG1 unification direction was a reasonable technical judgment. The Cologne pivot was a legitimate vote. P2464R0's analysis was procedurally correct. The October 2021 poll was an honest expression of committee preference. Each decision was made by experienced practitioners under real constraints.

The dysfunction is not in any one decision. It is in the absence of correction mechanisms that would allow the committee to revisit accumulated consequences when those consequences become visible. Five locally reasonable decisions, each individually defensible, chained together into a decade without networking in the C++ standard - and no structural mechanism required anyone to notice.

| Decision | Year | Would the initial outcome differ? | Would the aftermath differ? |
|---|---|---|---|
| Unification direction | 2014 | No | Moderately (progress requirement) |
| Cologne pivot | 2019 | No | Moderately (minority standing) |
| P2464R0 diagnosis | 2021 | Possibly | Yes (reconciliation, appeal, no ratchet) |
| "Including networking" poll | 2021 | Probably not | Yes (no direction lock, no bird-in-hand) |
| The open loop | 2021-2026 | N/A | Yes (5-year cancellation, mandatory review) |

The ISO Directives do not produce better technical decisions. They produce feedback loops. The feedback loops produce correction capacity. The correction capacity is what the networking arc lacked.

---

## Acknowledgments

The author thanks Ville Voutilainen for [P2464R0](https://wg21.link/p2464r0), which provided the analytical framework that led to the 2021 direction; Christopher Kohlhoff for the executor model and for co-authoring [P2469R0](https://wg21.link/p2469r0); Jamie Allsop, Richard Hodges, and Klemens Morgenstern for co-authoring [P2469R0](https://wg21.link/p2469r0); Bryce Adelstein Lelbach for the published poll outcomes in [P2453R0](https://wg21.link/p2453r0) and for recusing from consensus determination; Guy Davidson for the candid statement at the March 2026 SG14 session; Inbal Levi for the LEWG process perspective; Michael Wong for chairing the SG14 session; Dietmar Kuhl for [P2762R2](https://wg21.link/p2762r2); Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, and Michal Dominiak for [P2300R10](https://wg21.link/p2300r10); and Steve Gerbino for feedback on this paper.

---

## References

[1] [P4201R0](https://wg21.link/p4201r0) - "Two Systems, One Committee: A Game-Theoretical Analysis of ISO Governance vs. SD-4" (Vinnie Falco, 2026).

[2] [P4099R1](https://wg21.link/p4099r1) - "The Twenty-One Year Networking Arc" (Vinnie Falco, 2026).

[3] [P4100R0](https://wg21.link/p4100r0) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[4] [cppalliance/capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library.

[5] [cppalliance/corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library.

[6] [P2469R0](https://wg21.link/p2469r0) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not" (Christopher Kohlhoff, Jamie Allsop, Vinnie Falco, Richard Hodges, Klemens Morgenstern, 2021).

[7] [P2300R10](https://wg21.link/p2300r10) - "std::execution" (Michal Dominiak, Lewis Baker, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[8] [N4199](https://wg21.link/n4199) - "Minutes of Sept. 4-5, 2014 SG1 meeting in Redmond, WA" (Hans-J. Boehm, 2014).

[9] [P0443R0](https://wg21.link/p0443r0) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, 2016).

[10] [P1525R0](https://wg21.link/p1525r0) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[11] [P1658R0](https://wg21.link/p1658r0) - "Suggestions for Consensus on Executors" (Jared Hoberock, Bryce Adelstein Lelbach, 2019).

[12] [P1660R0](https://wg21.link/p1660r0) - "A Compromise Executor Design Sketch" (Jared Hoberock, Michael Garland, Bryce Adelstein Lelbach, Michal Dominiak, Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, David S. Hollman, Gordon Brown, 2019).

[13] [P1791R0](https://wg21.link/p1791r0) - "Evolution of the P0443 Unified Executors Proposal to accommodate new requirements" (Christopher Kohlhoff, Jamie Allsop, 2019).

[14] [P0443R11](https://wg21.link/p0443r11) - "A Unified Executors Proposal for C++" (Jared Hoberock et al., 2019).

[15] [P2464R0](https://wg21.link/p2464r0) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[16] [P0443R14](https://wg21.link/p0443r14) - "A Unified Executors Proposal for C++" (Jared Hoberock et al., 2020).

[17] [cplusplus/papers#1113](https://github.com/cplusplus/papers/issues/1113) - GitHub issue tracking P2464.

[18] [P2453R0](https://wg21.link/p2453r0) - "2021 October Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[19] [P2300R2](https://wg21.link/p2300r2) - "std::execution" (Michal Dominiak et al., 2021).

[20] [cplusplus/papers#1447](https://github.com/cplusplus/papers/issues/1447) - GitHub issue tracking P2762.

[21] [P2762R2](https://wg21.link/p2762r2) - "Sender/Receiver Interface For Networking" (Dietmar Kuhl, 2023).

[22] [N1925](https://wg21.link/n1925) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[23] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Open Issues in std::execution::task" (Vinnie Falco, 2026).

[24] [SG14 2026-03-11 Meeting Notes](https://lists.isocpp.org/sg14/att-1312/SG14_2026_03_11.pdf) - SG14 Low Latency Finance Monthly Meeting (Michael Wong, chair; Mark Hoemmen, scribe).

[25] ISO/IEC. "ISO/IEC Directives, Part 1 - Consolidated JTC 1 Supplement." 2023.

[26] Davidson, G. "SD-4: WG21 Practices and Procedures." ISO/IEC JTC1/SC22/WG21/SD-4, 2026-05-11.
