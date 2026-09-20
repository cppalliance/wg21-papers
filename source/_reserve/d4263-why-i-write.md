---
title: "Why I Write"
document: P4263R0
date: 2026-07-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The committee voted that senders cover networking. No sender-based networking has shipped.

Between February and May 2026, twenty-six papers from the author entered the WG21 mailings addressing the networking domain. They ask for nothing. They build the public record for an ask the author considers enormous: a second task type for byte-oriented I/O, complementary to `std::execution::task`.

---

## Revision History

### R0: July 2026 (Post-Brno)

- Initial revision.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy)<sup>[1]</sup> and [Corosio](https://github.com/cppalliance/corosio)<sup>[2]</sup> and believes coroutine-native I/O is a practical foundation for networking in C++.

Coroutine-native I/O and `std::execution` are complementary. Each serves the domain where its design choices pay off.

The author maintains proposals in the coroutine I/O space that address the same problem domain as sender-based networking. The networking endeavor proposes `std::io::task` alongside `std::execution::task` - two task types, one domain boundary, an implicit acknowledgment that `std::execution::task` is scoped. This is an enormous ask. The author discloses it here because it determines the scale of the evidentiary record this paper explains.

Coroutine-native I/O cannot express compile-time work graphs. That domain belongs to senders, and the author's bridge papers ([P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[3]</sup>, [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[4]</sup>) connect both models at the boundary so that neither forecloses the other.

This paper is drafted with AI.

This paper asks for nothing.

---

## 2. The Question

Why did you write so many papers, and what do you want?

The author writes to build the evidentiary record for networking that the committee did not demand - because the ask he is building toward, a second task type that acknowledges the first is scoped, is enormous enough that the evidence must arrive years before the vote.

In October 2021, LEWG polled: "The sender/receiver model (P2300) is a good basis for most asynchronous use cases, including networking" - consensus in favor ([P2453R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[5]</sup>). The word "networking" entered the consensus. No networking evidence accompanied it. The chair's published interpretation: "In the short term, this poll result doesn't mean much. We don't have a paper in hand that proposes networking based on the [P2300R2] model." Five years later, no such paper has shipped a networking implementation. The evidence column, for this domain, remains empty. The author fills it from outside.

The shape of the question is itself a finding. Twenty-six of these papers are information-only: They request no floor time, ask for no polls, and compete with no proposal for a slot in any working draft. The question they draw is not "which claims are wrong?" - no specific claim in any of the twenty-six has been challenged in any committee venue. The question is "why do they exist?" A body that evaluated papers by content would ask the first. The body asks the second.

**The asked question challenges a person. The unasked question examines a record.**

---

## 3. Two Task Types

The technical center of the networking story is a domain boundary between two task types - each real, each shipping, each serving the domain where its design choices pay off.

### 3.1. What `std::execution::task` serves

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[6]</sup>, now `std::execution` in C++26, provides compile-time sender composition with completion signatures checked by the compiler. It enables structured concurrency with cancellation propagated through stop tokens. It serves heterogeneous compute dispatch, with deployments in GPU and infrastructure settings documented in the record. P3552R3 adds `std::execution::task` - a coroutine type that participates in the sender protocol through an environment parameter, an allocator query, and affine scheduling. These properties are real. They ship in the reference implementation. The author's own bridge papers consume them.

### 3.2. What `std::io::task` serves

The author's networking endeavor proposes a complementary task type for byte-oriented serial I/O: symmetric transfer (O(1) stack composition where senders accumulate O(N) frames), zero allocation per operation through frame recycling, type-erased I/O at 36.4 ns against 53.4 ns for the sender equivalent ([P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf)<sup>[7]</sup>). At ten thousand connections performing one hundred operations per second each, the difference is a million allocations per second. The `retry` algorithm that P2300R10's own text presents at approximately 125 lines as a sender is seven lines as a coroutine ([P4178R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4178r0.pdf)<sup>[8]</sup>). A derivatives-exchange port measured the coroutine-native path at 21-27% lower P99 latency ([P4125R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4125r1.pdf)<sup>[9]</sup>). The implementation runs on three platforms.

### 3.3. The domain boundary

The standard already accommodates complementary solutions: `stdio` and `iostream`, `printf` and `std::format`. Two task types follow the same pattern. `std::execution::task` owns structured concurrency, work graphs, and heterogeneous dispatch. `std::io::task` owns byte-oriented serial I/O, connection-per-coroutine servers, and type-erased streams. The bridges ([P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[3]</sup>, [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[4]</sup>) connect them at the boundary at approximately 10-14 ns with zero allocations - partnership, not tolerance.

### 3.4. Why two is enormous

Accepting a second task type retroactively converts the first's universal claim into a scoped one. The 2021 poll said "most asynchronous use cases, including networking." A second task type says: Networking was not included after all. The P2300 architects have structural reason to oppose `std::io::task` regardless of evidence, because its acceptance is a concession about their design's scope. The incentive exists independent of the people who hold it.

At the SG14 video conference in March 2026, the room split bimodally on the networking question - the pattern Section 5 predicts when a universal claim meets a scoped alternative backed by evidence.

**Two task types. One domain boundary. The boundary is the fight.**

---

## 4. The Thin Record

The whole argument rests on one observable fact: The published record behind the networking claim does not contain the evidence the claim was announced as resting on.

### 4.1. The search

The author's interest is byte-oriented serial I/O on C++20 coroutines. P2300R10<sup>[6]</sup> entered the working draft carrying a wider claim - "most asynchronous use cases, including networking" - that extends over the author's domain. The author went into the historical record expecting to find the evidence behind the claim. The result of that search is six published papers tracing the decision chain end to end: the unification of executors ([P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[10]</sup>), the basis-operation pivot ([P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[11]</sup>), the P2464R0 diagnosis of the Networking TS ([P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[12]</sup>), the networking poll ([P4097R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4097r1.pdf)<sup>[13]</sup>), the claims-versus-evidence survey ([P4098R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4098r1.pdf)<sup>[14]</sup>), and the assembled causal chain ([P4099R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r1.pdf)<sup>[15]</sup>).

### 4.2. What the search found

The unification that preceded the poll rests on one code example. [P0761R2](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0761r2.pdf)<sup>[16]</sup>, the Executors Design Document, argued that separate executor models force an N x M explosion, illustrated by a hypothetical `parallel_for` constructed by the proposal's own authors. [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[10]</sup> searched the record and found that this snippet is the only code-level evidence published for any unification rationale.

[P4098R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4098r1.pdf)<sup>[14]</sup> tabulated twenty years of published claims about executors and networking against the published evidence for each. The GPU and infrastructure deployments are real and documented. The networking cells are empty.

C++20 coroutines prevent unbounded stack growth through symmetric transfer: A coroutine that awaits N synchronously-completing senders in a loop accumulates O(N) stack frames, while with symmetric transfer the same loop executes in O(1) stack space ([P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf)<sup>[17]</sup>). The phrase "symmetric transfer" appears in no revision of P2300R10, R0 through R10.

The field experience of the model's largest production deployment points the same way. Ian Petersen, a maintainer of Meta's libunifex, [wrote](https://github.com/facebookexperimental/libunifex/issues/586#issuecomment-1845934903)<sup>[18]</sup> in December 2023: "Our experience at Meta has been that coroutines are easier to read, write, debug, and just generally maintain than composition-of-sender algorithms-style code... The advice we give to internal teams adopting Unifex is that they should prefer coroutines until they know that the overheads are unacceptable."

[P4041R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4041r0.pdf)<sup>[19]</sup> surveys the post-adoption ecosystem: twenty-four sender items against zero coroutine items; the reference implementation has 1,300 stars; the sender I/O ecosystem totals 21.

### 4.3. The gap persists

The Direction Group's [P5000R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p5000r0.pdf)<sup>[20]</sup> (February 2026) lists networking as a carry-over priority and notes: "there is still no standard framework for run-of-the-mill networking tasks." The most advanced sender-based networking implementation, beman.net, remains experimental - poll(2) only, with no epoll, io_uring, or IOCP backends.

Twenty-one years after the first networking proposal (N1925, 2005), the standard contains no sockets, no DNS, and no TLS.

**The vote is in the minutes. The evidence is not.**

---

## 5. Why the Record is Thin

The record is thin because thinness is rational - specifically in the front groups (EWG and LEWG) when two designs compete for one slot.

### 5.1. The tournament

When two designs address the same problem, the committee's process selects one. The other does not ship smaller; it does not ship at all. Papers therefore compete in a zero-sum tournament within the front groups, and the tournament has a dominant strategy with two halves.

Claim maximally. Every domain a paper claims is territory a rival cannot enter. A proposal scoped to GPU dispatch leaves networking open for a competitor; a proposal claiming "most asynchronous use cases, including networking" forecloses the competitor without ever producing a networking design.

Evidence minimally. Every benchmark, every disclosed tradeoff, every named limitation beyond the minimum needed to advance is ammunition for opponents. The rational author discloses exactly enough to pass the next gate.

The dynamic has a cost that implementers have named directly. Eighteen implementers across every major compiler asked, in [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[32]</sup>, for "ways of slowing down the addition of features into the standard to allow implementers to catch up, and to allow the existing features to improve in quality." A tournament that rewards claiming maximally and disclosing minimally ships faster than the language can be implemented.

### 5.2. The author's ask sharpens this

`std::io::task` makes the domain boundary explicit. Its acceptance converts the universal claim into a scoped one. The architects of P2300 have structural reason to oppose it regardless of its evidence - because the cost of accepting it is not a technical concession but a reputational one: The universal model was not universal after all. Non-engagement is the dominant strategy. The evidence does not need to be refuted if its author can be dismissed on other grounds.

This does not reflect a moral failing in any individual. It represents rational behavior given the incentive structure. For this to change, the rules that make non-engagement a dominant strategy must be adjusted.

**The record is thin because thinness wins polls.**

---

## 6. Three Responses

Game theory predicts how a tournament responds to a player who publishes evidence anyway. For every other player, engaging the substance is the worst available move: Engagement legitimizes the evidence and risks losing on the merits. The dominant strategies, in order of cost, are three.

### 6.1. Attack the volume

Reframe the evidence as flooding. When quantity becomes the offense, content never has to be read; the act of publishing is converted into the violation.

### 6.2. Attack the provenance

Dismiss on authorship. The author's papers are AI-assisted and disclose it. The dismissal converts the disclosure into the charge. The bar is asymmetric: A single imperfect citation in an AI-assisted paper is presented as proof of hallucination; the mailing archives contain decades of human-authored papers with citation errors, treated with errata lists and corrected revisions.

### 6.3. Go silent

Non-engagement. Silence is free, carries no poll risk, and under a consensus model reads as the absence of support - the system scores an unengaged paper and a refuted paper identically.

### 6.4. The live confirmation

The author sent a pre-publication courtesy email to the author of [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3552r3.pdf)<sup>[21]</sup> (`std::execution::task`) regarding [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf)<sup>[22]</sup>. At the Brno meeting, the author greeted the P3552R3 author, mentioned the paper, and was told it is "AI slop" - repetitive, contains errors, not worth engaging with. No specific error was identified. No specific claim was challenged. The benchmarks of Section 3.2 and a working coroutine-native networking implementation - the artifact the universal model has not produced for its claimed domain in five years - remain unengaged.

This does not reflect a moral failing. It represents rational behavior. Engaging the substance would mean engaging the domain boundary, and engaging the domain boundary means acknowledging that the universal claim has a scope. For this to change, the structural incentives must be shifted by adjusting the rules that make non-engagement a dominant strategy.

**A bar that moves with provenance is a gate, not a standard.**

---

## 7. Why Papers

The strategy follows from the position. The author returned to the committee after a long absence. He holds newcomer standing on a body that prices seniority. He cannot win polls: He commands no bloc, chairs no subgroup, and employs no delegation. Sections 5 and 6 describe the game such a participant loses by playing. There is exactly one game the structure cannot take away: the record.

Ask for nothing, document everything. Write the retrospectives the committee does not write for itself. Tabulate the claims against the evidence on file when the claims prevailed. Score the predictions. Publish the benchmarks, the field experience, the bridges, the staged proposal - and let them sit in the permanent record where every future participant finds them.

### 7.1. Why not a blog?

The subject is the record, so the examination belongs in the record. The corpus audits decisions whose primary sources live in the mailing archive. A correction filed in the same archive travels with the claims it examines.

The wager (Section 8) requires immutability and dating. A mailing paper is numbered, dated, and immutable once published. A blog can be edited after the fact.

The archive reader exists in only one venue. The mailing is preserved for the life of the standard and read by every future participant who researches how a feature came to be.

The mailing is the institution's public channel. Work addressed to the institution belongs in the channel the institution owns.

### 7.2. The networking corpus

| | Paper | What it documents |
| :--- | :---- | :---------------- |
| **Retrospectives** | [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf)<sup>[10]</sup> | The 2014-2020 unification of executors. |
| | [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf)<sup>[11]</sup> | The 2019 basis-operation pivot. |
| | [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf)<sup>[12]</sup> | The P2464R0 diagnosis of the Networking TS. |
| | [P4097R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4097r1.pdf)<sup>[13]</sup> | The October 2021 networking poll. |
| | [P4098R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4098r1.pdf)<sup>[14]</sup> | Twenty years of async claims against published evidence. |
| | [P4099R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r1.pdf)<sup>[15]</sup> | The four-decision causal chain. |
| | [P4041R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4041r0.pdf)<sup>[19]</sup> | The universality claim audited post-adoption. |
| | [P4048R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4048r0.pdf)<sup>[23]</sup> | The twenty-one-year networking gap. |
| **Constructive** | [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[24]</sup> | The IoAwaitable execution model. |
| | [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf)<sup>[7]</sup> | What C++20 coroutines already provide; benchmarks. |
| | [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf)<sup>[3]</sup> | Consuming senders from coroutine-native code. |
| | [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf)<sup>[4]</sup> | Producing senders from coroutine-native code. |
| | [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[25]</sup> | The Network Endeavor: the staged path to C++29. |
| | [P4125R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4125r1.pdf)<sup>[9]</sup> | Field experience at a derivatives exchange. |
| | [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf)<sup>[26]</sup> | A universal continuation model beneath both worlds. |
| | [P4172R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r1.pdf)<sup>[27]</sup> | IoAwaitable for byte-oriented I/O. |
| **Methodology** | [P4047R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4047r0.pdf)<sup>[28]</sup> | Predictions scored against the record. |
| | [P4207R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4207r0.pdf)<sup>[29]</sup> | Adversarial review of a committee paper. |

Information-only is the mechanism. An info-paper requests no floor time, so it cannot be denied scheduling. It competes with no proposal, so it cannot lose a poll. It asks for nothing, so there is nothing to refuse. Within the tournament, it is the one move that is not a play.

**One paper is a complaint; twenty-six are an audit.**

---

## 8. The Wager

The papers appear to accomplish little today. Their term is C++29.

### 8.1. The prediction

C++29 is the cycle in which the committee's answer on networking comes due. If that answer is sender-based, it will arrive into a world that already contains published benchmarks, a working coroutine-native networking implementation on three platforms, and a dated decision-by-decision record of how the universal claim advanced and on what evidence. Any gap between what ships and what the working implementations deliver will be measurable, and the measurement will have a paper trail that predates the outcome. If instead the shipped answer matches or exceeds the working implementations, [P4047R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4047r0.pdf)<sup>[28]</sup>'s method scores the author's predictions with the same table it applies to everyone else's.

### 8.2. Early signs the record travels

[P4223R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4223r0.pdf)<sup>[30]</sup> (Petersen, May 2026) - a sender-side proposal - introduces a frame-allocator query described as "inspired by Vinnie Falco et al.'s work in P4003," adopting into the sender model a finding the coroutine-native corpus published first. SG14, the study group for low latency, games, finance, and embedded systems, formally advises in [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[31]</sup> that "Networking (SG4) should not be built on top of P2300." The Direction Group's [P5000R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p5000r0.pdf)<sup>[20]</sup> suggests C++29 "be considered a 'maintenance release'" - the absorption constraint, now in the committee's own direction papers.

### 8.3. What the author wants

Three conditions under which this corpus stops being necessary:

1. **A symmetric evidence bar for networking.** The same questions asked of the Networking TS applied to any sender-based networking proposal. The retrospective half of the corpus exists because that symmetry currently has no other corrective.

2. **A networking decision on the record.** Rationale documented, alternatives analyzed, evidence cited - not just a poll tally. The decision-archaeology half of the corpus exists because no one writes these records inside.

3. **The domain boundary acknowledged.** If `std::io::task` is rejected, the rejection carries published evidence that `std::execution::task` serves byte-oriented serial I/O - the evidence the 2021 poll lacked.

If these conditions arrive, the corpus becomes what it is on its face: benchmarks, retrospectives, and proposals, useful to the readers they serve. If they do not, the corpus keeps doing the one thing the structure cannot do for itself in this domain.

**The corpus forgets nothing and serves no faction.**

---

## Acknowledgments

Thanks to Eric Niebler, Kirk Shoop, Lewis Baker, and their collaborators for [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[6]</sup>, whose achievements in its domains this paper affirms, and whose presence in the standard the author's bridge papers serve.

Thanks to Ian Petersen for [P4223R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4223r0.pdf)<sup>[30]</sup>, which demonstrates what happens when the record reaches across the domain boundary.

Thanks to Peter Dimov for structural feedback that reshaped this paper.

The title borrows from George Orwell's 1946 essay of the same name.

---

## References

[1] [Capy](https://github.com/cppalliance/capy)

[2] [Corosio](https://github.com/cppalliance/corosio)

[3] [P4092R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4092r1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[4] [P4093R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4093r1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[5] [P2453R0](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2022).

[6] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[7] [P4088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4088r1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[8] [P4178R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4178r0.pdf) - "Trade-offs in Asynchronous Abstraction Design" (Vinnie Falco, 2026).

[9] [P4125R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4125r1.pdf) - "Coroutine-Native I/O at a Derivatives Exchange" (Mungo Gill, 2026).

[10] [P4094R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4094r1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[11] [P4095R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4095r1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[12] [P4096R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4096r1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).

[13] [P4097R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4097r1.pdf) - "The Networking Claim and P2453R0" (Vinnie Falco, 2026).

[14] [P4098R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4098r1.pdf) - "Async Claims and Evidence" (Vinnie Falco, 2026).

[15] [P4099R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r1.pdf) - "The Twenty-One Year Networking Arc" (Vinnie Falco, 2026).

[16] [P0761R2](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0761r2.pdf) - "Executors Design Document" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Michael Wong, 2018).

[17] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).

[18] [libunifex issue #586](https://github.com/facebookexperimental/libunifex/issues/586#issuecomment-1845934903) - Ian Petersen, comment of December 7, 2023.

[19] [P4041R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4041r0.pdf) - "Is `std::execution` a Universal Async Model?" (Vinnie Falco, 2026).

[20] [P5000R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p5000r0.pdf) - "Direction for ISO C++29" (Daveed Vandevoorde, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, Michael Wong, 2026).

[21] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3552r3.pdf) - "std::execution::task" (Lewis Baker, 2026).

[22] [P4255R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4255r0.pdf) - "Awaitables And Senders For Synchronous I/O" (Vinnie Falco, 2026).

[23] [P4048R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4048r0.pdf) - "Networking for C++29: A Call to Action" (Vinnie Falco, 2026).

[24] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[25] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, 2026).

[26] [P4126R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4126r1.pdf) - "A Universal Continuation Model" (Vinnie Falco, Klemens Morgenstern, 2026).

[27] [P4172R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4172r1.pdf) - "IoAwaitable for Coroutine-Native Byte-Oriented I/O" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[28] [P4047R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4047r0.pdf) - "CRYSTAL BALL: Checking Predictions Against the Record" (Vinnie Falco, 2026).

[29] [P4207R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4207r0.pdf) - "Prosecute Your Paper To Improve It" (Vinnie Falco, 2026).

[30] [P4223R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4223r0.pdf) - "Towards Senders in Interfaces" (Ian Petersen, 2026).

[31] [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf) - "The SG14 Priority List for C++29" (Michael Wong, 2026).

[32] [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf) - "Implementation reality of WG21 standardization" (Nina Ranns, et al., 2026).
