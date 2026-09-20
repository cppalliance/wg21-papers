---
title: "A Better WG21"
document: P4134R0
date: 2026-03-21
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Five papers examined five facets of the same system. None of them broke it. All of them documented it.

[P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> extracted fourteen failure modes from the executor and networking arc and proposed proportional deliberation. [P4129R1](https://wg21.link/p4129r1)<sup>[2]</sup> surveyed the published poll record and documented six observable patterns in WG21 voting. [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> documented the structural powers of the convenership and the institutional wisdom of senior committee members on how those powers operate in practice. [P4131R0](https://wg21.link/p4131r0)<sup>[4]</sup> tested the train model's claims against the published record for each release from C++14 through C++26. [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> defined what a healthy feedback loop would contain and found ten of twelve elements absent. This paper shows how those five facets interlock into a single reinforcing system and presents nine directions for reform. Each direction is a suggestion. The committee is sovereign.

---

## Revision History

### R0: March 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author has papers in the WG21 mailing and participates in the committee process. The author developed and maintains [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup> and [Capy](https://github.com/cppalliance/capy)<sup>[7]</sup> and is a co-author of [P2469R0](https://wg21.link/p2469r0)<sup>[8]</sup>. The author's preferred asynchronous model competes with [P2300R10](https://wg21.link/p2300r10)<sup>[9]</sup> (`std::execution`). Coroutine-native I/O cannot express compile-time work graphs. That is a real limitation. The author is telling you this so you can calibrate everything that follows.

This paper synthesizes five companion papers. The author wrote all five. The failure modes, the voting patterns, the structural powers, the train model assessment, and the feedback loop audit are drawn from the published record. They stand or fall on the sources, not on who assembled them. But the reader should know that one person chose which sources to assemble and in what order. That choice is itself a framing.

The analysis is structural, not personal. Every decision examined was made by experienced practitioners under real constraints. The intent is to give the committee better tools, not a verdict.

---

## 2. What the Companion Papers Found

Each companion paper examined one facet of the committee's process. This section summarizes the structural property each paper reveals. The evidence is in the companion papers. This paper does not re-present it.

### 2.1 Failure Modes (P4050R0)

[P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> extracted fourteen failure modes from the executor and networking arc, organized into five categories: evidence, knowledge transfer, scope management, analytical framing, and governance. It generalized each failure mode beyond the executor arc and proposed proportional deliberation - a framework of decision sizing, missing artifacts, domain coverage, and tooling that gives the chair structured tools for running sessions where the process scales with the consequence.

The structural property: WG21 has no proportional-deliberation requirement. A decision that sets aside years of work gets the same process as a decision to add `[[nodiscard]]` to a function.

### 2.2 Voting Dynamics (P4129R1)

[P4129R1](https://wg21.link/p4129r1)<sup>[2]</sup> surveyed the published poll record across three decades and documented six observable patterns: attendance-dependent outcome reversals, social pressure on participation, directional persistence, subgroup-plenary disagreements, the disproportionate weight of Strongly Against votes under the consensus threshold, and the influence of poll wording on outcomes.

The structural property: The poll result is a function of three inputs the chair controls - the question asked, the interpretation of the answer, and the scheduling that determines who is in the room - in addition to the votes themselves.

### 2.3 Appointment Is Policy (P4130R0)

[P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> documented the structural powers of the WG21 convenership - appointment of all subgroup chairs, creation and disbandment of study groups, control of plenary, and the meeting schedule - and presented on-camera testimony from senior committee members describing how those powers operate in practice. It presented the 2026 convenership transition as an opportunity for visible fairness, and identified five directions the new convener can take using powers the role already holds.

The structural property: The convener appoints every chair. The chairs control every schedule. The schedule determines what ships. No open competition exists for any of these positions.

### 2.4 The Train Model (P4131R0)

[P4131R0](https://wg21.link/p4131r0)<sup>[4]</sup> tested the train model's five claims - ship what is ready, pull features that are not ready, eliminate "now or never" pressure, higher specification quality, and closer compiler tracking - against the published record for each release from C++14 through C++26. It documented the implementers' own assessment ([P3962R0](https://wg21.link/p3962r0)<sup>[10]</sup>) that features accumulate faster than they can be implemented.

The structural property: The train model promised that features would be pulled when not ready. The record shows they are pushed when almost ready. The safety valve is rarely used for large features because the social cost of pulling exceeds the social cost of shipping.

### 2.5 The Missing Feedback Loop (P4133R0)

[P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> defined what a healthy feedback loop would contain for both library and language proposals - twelve elements including evidence of need, complete implementation, steel man arguments, post-adoption metrics, forced retrospectives, decision records, domain coverage, prediction registries, symmetric evidence bars, knowledge continuity, and outcome tracking. It audited the published record and found that ten of twelve elements are absent.

The structural property: The committee measures whether the train runs on time. It does not measure whether the passengers arrived at the right destination.

---

## 3. The Interlocking System

Each companion paper's findings are individually explainable by simpler causes. Attendance-dependent outcomes may reflect genuine learning. Chair discretion may reflect necessary flexibility. The train model's deadline pressure may be an acceptable tradeoff for schedule predictability. The missing feedback loop may reflect volunteer bandwidth constraints. Taken individually, each finding admits a benign interpretation.

Taken together, they describe a system.

### 3.1 The Reinforcing Loop

The five facets connect into a single cycle:

1. The convener appoints all chairs ([P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> Section 3). No open competition. No term limits. Chairs serve until they choose to stop.

2. The chairs control scheduling and poll wording ([P4129R1](https://wg21.link/p4129r1)<sup>[2]</sup> Section 2.2; [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> Section 4.2). Scheduling determines who is in the room. Poll wording shapes the vote distribution. Different framings of the same question produce different outcomes.

3. Scheduling determines what reaches the train ([P4131R0](https://wg21.link/p4131r0)<sup>[4]</sup> Section 7.1). The three-year cadence creates real urgency. Features that miss the deadline wait three years. The pressure to ship is structural.

4. The train ships on a fixed cadence ([P4131R0](https://wg21.link/p4131r0)<sup>[4]</sup> Section 2). The safety valve - pull what is not ready - is rarely used for large features. The culture says ship. The model says pull. The culture wins.

5. No feedback loop checks whether what shipped was correct ([P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> Section 9). No post-adoption metrics. No forced retrospectives. No prediction registry. No outcome tracking. The process runs open-loop.

6. Failure modes accumulate without correction ([P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> Section 3). Predictions are made and never followed up. Design rationale is lost across paper boundaries. Evidence bars are applied non-uniformly. Affected stakeholders are absent from pivotal decisions.

The cycle repeats. Each iteration compounds the previous one. The convener who appoints the chairs is also the Foundation chairman who funds the meetings. The chairs who control scheduling are also co-authors of the proposals they schedule. The train that ships on time ships features whose readiness was assessed by the same chairs who scheduled them. The feedback loop that would catch the errors does not exist.

### 3.2 Why the System Persists

The system persists because each participant acts rationally within their local constraints.

The convener appoints qualified people. The chairs schedule important work. The authors push to meet deadlines. The voters vote on what is presented. The implementers implement what is standardized. Each actor's behavior is locally reasonable. The system-level outcome - twenty-one years without networking, proposal-sized defects in C++20, implementers asking the committee to slow down - is not the intent of any individual actor. It is the emergent property of the system they collectively operate.

This is not a conspiracy. It is a process that was designed for a fifty-person committee in the 1990s and has not been redesigned for a two-hundred-fifty-person committee in the 2020s.

---

## 4. What the System Produces

The observable outputs of the system described in Section 3, drawn from the published record:

- **Twenty-one years without networking.** [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[11]</sup> proposed networking in 2005. The Networking TS was published as ISO/IEC TS 19282:2018. It has not been merged into the C++ standard. The committee voted against Asio as a general async model, in favor of sender/receiver as a general async model, and could not reach consensus to stop pursuing the Networking TS - all in the same poll cycle ([P2453R0](https://wg21.link/p2453r0)<sup>[12]</sup>).

- **Contested features shipped under deadline pressure.** C++26 carries three features that each generated substantial published opposition: contracts (P2900), `std::execution` (P2300), and `std::execution::task` (P3552). Ville Voutilainen wrote: "And all this with our noses pressed against a deadline"<sup>[13]</sup>. Jonathan M&uuml;ller documented that `std::execution::task` was forwarded after the feature freeze deadline<sup>[14]</sup>.

- **Implementers asking the committee to slow down.** Eighteen implementers from GCC, Clang, MSVC, EDG, libc++, and libstdc++ wrote in [P3962R0](https://wg21.link/p3962r0)<sup>[10]</sup>: "We would like the committee to consider ways of slowing down the addition of features into the standard to allow implementers to catch up."

- **Proposal-sized defects.** Nina Ranns documented in 2021 that C++20 had "quite a few 'defects'... that are too large to be handled via the issues list"<sup>[15]</sup>.

- **Directional persistence without follow-up.** The October 2021 poll "Networking in the C++ Standard Library should be based on the sender/receiver model" achieved weak consensus<sup>[12]</sup>. Five years later, no sender-based networking library has shipped. The directional poll remains the stated direction.

- **Selective non-compliance.** Daveed Vandevoorde predicted that "most of the principal C++ implementations will opt not to be standard compliant for the better part of a decade"<sup>[16]</sup>.

These outputs are not the intent of any individual actor. They are the published record of the system described in Section 3.

---

## 5. What the System Does Well

The system also produces genuine achievements. The recommendations in Section 6 are designed to preserve them.

**Schedule predictability.** C++14, C++17, C++20, and C++23 shipped on time. Four consecutive on-time releases. No previous era of C++ standardization achieved this. The five-year model produced C++98, then a five-year gap to C++03 (a bug-fix release), then an eight-year gap to C++11. The train runs on time. That is real.

**Compiler tracking.** By C++17, major compilers were shipping conforming implementations within months of publication. The predictable cadence transformed the relationship between the standard and its implementations. Herb Sutter documented this achievement: "never before have all the major compilers tracked the standard so closely"<sup>[17]</sup>.

**Consensus as a brake.** The consensus model prevents premature adoption. The SA votes that blocked P2300 for C++23 gave the proposal two additional years of refinement. The contracts removal from C++20 - plenary vote 68/0/4 - demonstrated that the safety valve works when the evidence is overwhelming. The consensus threshold is a feature, not a bug, when it protects the standard from features that are not ready.

**Extraordinary volunteer work.** The C++ standard is produced by volunteers. The technical quality of the work - modules, concepts, ranges, coroutines, `std::expected`, `std::print`, `std::mdspan` - is extraordinary by any measure. The people who produce this work do so because they care about the language. That commitment is the committee's most valuable asset.

**Open participation.** Anyone can write a paper. Anyone can attend a meeting. Anyone can vote. The barriers to participation are time and travel, not credentials. The committee's openness has produced contributions from individuals, small companies, and major corporations alike.

These achievements are real. The directions in Section 6 are designed to strengthen the system's weaknesses without sacrificing its strengths.

---

## 6. Directions for Reform

The following directions are presented as a menu. Each addresses one or more failure modes documented in the companion papers. Each preserves the system's strengths. The committee evaluates the tradeoffs. The committee orders.

### Direction A: Proportional Deliberation

Scale the process with the consequence. [P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> Sections 5-8 describe the full framework.

- **What it changes.** Decisions are sized into four tiers based on observable criteria (years of prior work, paper chain depth, deployed codebases, reversibility, domain breadth). Each tier has a required artifact set. The chair uses a one-page brief and a checklist to assess readiness before scheduling consequential decisions.
- **Failure modes addressed.** F1 (missing artifacts), A1-A4 (evidence gaps), D1-D4 (analytical framing), E1-E2 (governance gaps).
- **What it preserves.** The chair's authority. The consensus model. The volunteer structure. Tier 1 decisions (the vast majority) require only the paper itself.
- **What it costs.** Authors of consequential proposals must produce artifacts before the meeting. Chairs must review a one-page brief. The framework must be maintained as a standing document.

### Direction B: Domain Coverage Attestation

Attach domain coverage information to poll records. [P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> Section 6 describes the stakeholder registry.

- **What it changes.** Stakeholders self-register their relationship to the domain. The poll record includes a coverage annotation: "Of N self-registered networking practitioners, the distribution was X." The annotation is metadata, not a weighting function.
- **Failure modes addressed.** A3 (bundled-domain consensus), D3 (absent stakeholders), G1-G2 (domain coverage).
- **What it preserves.** One person, one vote. No credentialing. No vote weighting. The committee still decides. The record is richer.
- **What it costs.** A self-registration mechanism (an open issue or reflector thread per paper). The chair's pre-meeting report adds one artifact.

### Direction C: Decision Rationale Capture

Record why the committee voted as it did, not just how. [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> Section 3.7.

- **What it changes.** For Tier 3+ decisions, the chair or a designated recorder publishes a decision rationale document: reasoning, alternatives considered, dissenting views, and conditions for revisiting the decision.
- **Failure modes addressed.** B1-B2 (knowledge transfer), E1 (proceeding without consensus).
- **What it preserves.** The poll mechanism. The chair's discretion. The volunteer structure.
- **What it costs.** A structured template filled out after consequential votes. Minutes of work per decision, not hours.

### Direction D: Forced Retrospectives

Close the feedback loop. [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> Sections 3.5-3.6, 3.9.

- **What it changes.** A mandatory look-back for every feature adopted into the standard, published no later than two releases after adoption. The retrospective asks: Did the claimed benefits materialize? Did users adopt the feature? Did implementers ship it on time? What was learned? A prediction registry records claims made during adoption with falsifiable criteria and a revisit date.
- **Failure modes addressed.** A4 (predictions without follow-up), E2 (non-uniform evidence bar).
- **What it preserves.** The adoption process. The train model. The committee's authority to adopt features.
- **What it costs.** One paper per adopted feature, two releases later. The original author or a volunteer writes it.

### Direction E: Implementation Requirement

Require working code before committee time. [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> Sections 3.2, 4.2, 5.

- **What it changes.** Library proposals without a complete implementation (benchmarks, unit tests, documentation) are deferred until the implementation exists. Language proposals without a proof-of-concept compiler fork are deferred. The chair applies the requirement using existing scheduling power.
- **Failure modes addressed.** A1 (architecture without demonstration), C2 (iteration without deployment).
- **What it preserves.** The paper process. The committee's evaluation. The chair's scheduling authority.
- **What it costs.** Authors must build before they propose. Generative AI has collapsed the cost of producing proof-of-concept code. The excuse of cost is gone.

### Direction F: Symmetric Evidence Bar

Apply the same standard of evidence to the incumbent and the challenger. [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup> Section 6.2.

- **What it changes.** When a directional decision is contested, the chair verifies that the same evidence bar has been applied to each side. If one side is required to demonstrate deployment, the other side is required to demonstrate deployment. If one side is required to answer "I don't know," the other side is required to answer the same question.
- **Failure modes addressed.** A4 (predictions without follow-up), E2 (non-uniform evidence bar).
- **What it preserves.** The committee's authority to set direction. The consensus model. The chair's discretion.
- **What it costs.** The chair asks one additional question before a directional poll: "Has the same evidence bar been applied to both sides?"

### Direction G: Open Competition for Officer Appointments

Replace appointment-without-competition with a structured selection process.

- **What it changes.** Subgroup chairs and study group chairs are selected through a process that includes: a public call for candidates, a statement of qualifications from each candidate, and a selection mechanism (appointment by the convener from the candidate pool, or election by the subgroup). Term limits ensure rotation. The convener retains the appointment power but exercises it from a candidate pool rather than by sole discretion.
- **Failure modes addressed.** The structural concentration documented in [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> Sections 3-6.
- **What it preserves.** The convener's authority. The chair's powers within the subgroup. The volunteer structure.
- **What it costs.** A selection process that runs once per term. Administrative overhead measured in hours, not days.

### Direction H: Role Separation

Separate the convenership from foundation leadership and active paper authorship.

- **What it changes.** The convener does not simultaneously serve as chairman of the Standard C++ Foundation or as an active paper author on proposals under committee consideration. The separation is a norm, not a rule - the committee establishes the expectation and the convener honors it.
- **Failure modes addressed.** The role concentration documented in [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> Sections 3-6.
- **What it preserves.** The convener's formal powers. The Foundation's mission. The individual's right to participate.
- **What it costs.** The convener forgoes two roles. The Foundation elects a different chairman. The cost falls on one person's portfolio, not on the committee's structure.

### Direction I: Consolidation Cycles

Alternate feature-focused and consolidation-focused releases. The implementers' own recommendation from [P3962R0](https://wg21.link/p3962r0)<sup>[10]</sup>.

- **What it changes.** Every other release (or every third release) is designated a consolidation cycle. During a consolidation cycle, the committee prioritizes defect resolution, conformance improvements, and portability work over new features. The train still runs on time. The cargo changes.
- **Failure modes addressed.** The implementation gap documented in [P4131R0](https://wg21.link/p4131r0)<sup>[4]</sup> Sections 6-7. The implementers' assessment that "features accumulate faster than they can be fully implemented"<sup>[10]</sup>.
- **What it preserves.** The three-year cadence. The train model's schedule predictability. The committee's ability to adopt features in feature-focused cycles.
- **What it costs.** Features that are ready during a consolidation cycle wait one additional release. The "now or three years from now" pressure becomes "now or six years from now" for features that arrive at the wrong point in the cycle. The train model's author anticipated this: "Knowing that another ship train is coming is a nice pressure release valve"<sup>[18]</sup>.

---

## 7. The Mapping

Each direction addresses specific failure modes. The following table maps the nine directions to the seventeen checklist items from [P4050R0](https://wg21.link/p4050r0)<sup>[1]</sup> and the twelve scorecard items from [P4133R0](https://wg21.link/p4133r0)<sup>[5]</sup>.

| Direction | D4050 Failure Modes Addressed         | D4132 Scorecard Items Addressed                     |
| --------- | ------------------------------------- | --------------------------------------------------- |
| A         | A1-A4, D1-D4, E1-E2, F1              | 1 (evidence), 2 (implementation), 7 (decision rec.) |
| B         | A3, D3, G1, G2                        | 8 (domain coverage)                                 |
| C         | B1, B2, E1                            | 7 (decision record), 11 (knowledge continuity)      |
| D         | A4, E2                                | 5 (post-adoption), 6 (retrospective), 9 (registry)  |
| E         | A1, C2                                | 2 (implementation)                                   |
| F         | A4, E2                                | 10 (symmetric evidence bar)                          |
| G         | (P4130 structural patterns)           | (governance, not in D4132 scorecard)                 |
| H         | (P4130 structural patterns)           | (governance, not in D4132 scorecard)                 |
| I         | (P4131 implementation gap)            | 12 (outcome tracking)                                |

No single direction addresses every failure mode. The directions are designed to compose. A committee that adopts A, B, C, and D has addressed fifteen of seventeen D4050 checklist items and ten of twelve D4132 scorecard items. A committee that adopts all nine has addressed every documented failure mode.

A committee that adopts none has the published record to explain why.

---

## 8. What This Paper Does Not Propose

This paper does not propose abolishing the consensus model. The consensus model's structural properties - including the disproportionate weight of SA votes - are documented in [P4129R1](https://wg21.link/p4129r1)<sup>[2]</sup>. Those properties also protect the standard from premature adoption. The directions in Section 6 work within the consensus model, not against it.

This paper does not propose weighted voting. Domain coverage (Direction B) is metadata on the record, not a weighting function. Every vote counts equally.

This paper does not propose removing any officer. The structural concentration documented in [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup> is a property of the system, not a criticism of the individuals who operate it. Directions G and H address the system. They do not address the people.

This paper does not propose changing the train model's three-year cadence. Direction I changes the cargo, not the schedule. The train still runs on time.

This paper does not propose mandatory adoption of any direction. The directions are a menu. The committee is sovereign. The paper provides information, asks nothing, and serves at the pleasure of the chair.

---

## 9. Limitations

The five companion papers present the published record. This paper synthesizes them. The synthesis is the author's framing. A different author, examining the same record, might frame it differently.

The interlocking system described in Section 3 is a model, not a proof. The reinforcing loop is one interpretation of the published record. Simpler explanations may exist for every connection drawn. The convener may have appointed the best available candidates. The chairs may have scheduled the most important work. The train model may have shipped the features that were genuinely ready. The missing feedback loop may reflect volunteer bandwidth, not institutional blindness.

Correlation is not causation. The structural connections documented in the companion papers are real. The causal claims are the reader's to make or to withhold.

The directions in Section 6 are untested. No standards body has adopted proportional deliberation, forced retrospectives, or prediction registries. The directions are drawn from the failure modes - each direction is the inverse of a documented failure - but the inverse of a failure is not guaranteed to be a success. The committee should evaluate each direction on its merits, not on the strength of the diagnosis.

The author wrote all five companion papers. The synthesis is therefore not independent of the analysis. A synthesis written by a different author, drawing on the same sources, would provide a stronger test of the findings. The author welcomes that test.

The conclusions are the reader's.

---

## Acknowledgements

The author thanks Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz and Peter Dimov for their critique of [P4129R1](https://wg21.link/p4129r1)<sup>[2]</sup>, which forced the removal of theoretical frameworks that did not survive peer review and produced a stronger paper. The author thanks Nina Ranns and the seventeen co-authors of [P3962R0](https://wg21.link/p3962r0)<sup>[10]</sup> for documenting the implementers' assessment in a public paper - the most important single exhibit in the companion papers. The author thanks Jens Maurer and John Spicer for their candor on camera in the Boost documentary interviews cited in [P4130R0](https://wg21.link/p4130r0)<sup>[3]</sup>, and Daisy Hollman for her participation in the same interviews. The author thanks Herb Sutter for documenting the train model's rationale and claims in [P1000R2](https://wg21.link/p1000r2)<sup>[19]</sup> through [P1000R6](https://wg21.link/p1000r6)<sup>[20]</sup>, providing the baseline against which the record can be examined. The author thanks Steve Gerbino for feedback on the directions.

---

## References

- [1] [P4050R0](https://wg21.link/p4050r0): "Failure Modes in Large-Scale Standardization." Falco. https://wg21.link/p4050r0
- [2] [P4129R1](https://wg21.link/p4129r1): "The Dynamics of Voting in WG21." Falco. https://wg21.link/p4129r1
- [3] [P4130R0](https://wg21.link/p4130r0): "Appointment Is Policy." Falco. https://wg21.link/p4130r0
- [4] [P4131R0](https://wg21.link/p4131r0): "Retrospective: Effects of the WG21 Train Model." Falco. https://wg21.link/p4131r0
- [5] [P4133R0](https://wg21.link/p4133r0): "The Missing Feedback Loop." Falco. https://wg21.link/p4133r0
- [6] Corosio: https://github.com/cppalliance/corosio
- [7] Capy: https://github.com/cppalliance/capy
- [8] [P2469R0](https://wg21.link/p2469r0): "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not." Kohlhoff, Allsop, Falco, Hodges, Morgenstern. https://wg21.link/p2469r0
- [9] [P2300R10](https://wg21.link/p2300r10): "`std::execution`." Dominiak, Evtushenko, Baker, Teodorescu, Howes, Shoop, Garland, Niebler, Lelbach. https://wg21.link/p2300r10
- [10] [P3962R0](https://wg21.link/p3962r0): "Implementation reality of WG21 standardization." Ranns, Keane, Serebrennikov, Ballman, Sandoe, Caves, DaCamara, Dos Reis, Brito, Meerwald, Xu, Yaghmour, Miller, Childers, Waffl3x, Cardoso Lopes, Tong, Dionne. https://wg21.link/p3962r0
- [11] N1925: "A Proposal to Add Networking Utilities to the C++ Standard Library." Kohlhoff. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf
- [12] [P2453R0](https://wg21.link/p2453r0): "2021 October Library Evolution Poll Outcomes." Lelbach, Fracassi, Craig. https://wg21.link/p2453r0
- [13] [P3608R0](https://wg21.link/p3608r0): "C++26 is not ready." Voutilainen. https://wg21.link/p3608r0
- [14] [P3801R0](https://wg21.link/p3801r0): "Concerns about the design of `std::execution::task`." M&uuml;ller. https://wg21.link/p3801r0
- [15] N4890: "WG21 2021-05 Admin telecon minutes." Ranns. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/n4890.pdf
- [16] [P3590R0](https://wg21.link/p3590r0): "Constexpr Coroutines Burdens." Vandevoorde. https://wg21.link/p3590r0
- [17] Sutter, H. "Trip report: Winter ISO C++ standards meeting." Blog post, March 11, 2016. https://herbsutter.com/2016/03/11/trip-report-winter-iso-c-standards-meeting/
- [18] N3316: "Minutes, PL22.16 Meeting No. 57, WG21 Meeting No. 52, 15-19 August 2011 Bloomington, Indiana, USA." Kloepper. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2011/n3316.pdf
- [19] [P1000R2](https://wg21.link/p1000r2): "C++ IS schedule." Sutter. https://wg21.link/p1000r2
- [20] [P1000R6](https://wg21.link/p1000r6): "C++ IS schedule." Sutter. https://wg21.link/p1000r6
