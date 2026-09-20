---
title: "The Dynamics of Voting in WG21"
document: P4129R0
date: 2026-03-21
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "C++ Alliance Proposal Team"
---

## Abstract

The committee votes by show of hands. The published record contains the tallies.

This paper surveys WG21's published poll record across three decades. It documents six observable patterns: attendance-dependent outcome reversals, social pressure on participation, directional persistence, subgroup-plenary disagreements, the disproportionate weight of Strongly Against votes under the consensus threshold, and the influence of poll wording on outcomes. Every exhibit is drawn from published N-numbered minutes, P-numbered papers, or public mailing list archives. The paper makes no theoretical claims about what causes the observed patterns. The evidence is public. The conclusions are the reader's.

---

## Revision History

### R0: March 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author has papers in the mailing and has observed committee dynamics as a participant. The author developed and maintains [Corosio](https://github.com/cppalliance/corosio)<sup>[1]</sup> and [Capy](https://github.com/cppalliance/capy)<sup>[2]</sup> and is a co-author of [P2469R0](https://wg21.link/p2469r0)<sup>[3]</sup>. The analysis in this paper is structural, not personal. Every decision examined was made by experienced practitioners under real constraints. The intent is to document the published record, not to assign blame.

This paper is a companion to [P4050R0](https://wg21.link/p4050r0)<sup>[4]</sup>, which documents process failure modes in large-scale standardization. That paper examines what happens when the process does not scale with the consequence. This paper examines the voting mechanism itself.

---

## 2. How Polls Work

WG21 conducts polls at two levels: subgroup and plenary.

In subgroups (EWG, LEWG, LWG, CWG, and the study groups), everyone present may vote. The voting scale has five positions: Strongly Favor (SF), Weakly Favor (WF), Neutral (N), Weakly Against (WA), and Strongly Against (SA). The chair reads the result and determines whether consensus exists. There is no fixed threshold. The general guideline is a 2:1 ratio of favor to against, but the chair has discretion<sup>[5]</sup>. For forwarding decisions, a stronger 3:1 ratio is expected<sup>[6]</sup>.

In plenary, only those registered in the ISO Global Directory may vote, one person one vote<sup>[7]</sup>. Plenary motions use a simpler In Favour / Opposed / Abstain scale, and national body positions are recorded separately.

The distinction between straw polls and formal votes is older than the committee's current membership. The earliest recorded procedural statement, from the committee's 1991 founding meeting, established that "straw votes are designed to give a good indication of how formal votes will turn out" and therefore "follow the same rules as formal votes"<sup>[8]</sup>.

### 2.1 What the Positions Mean

The five positions are not interchangeable with abstention. A Neutral vote means the voter understands the proposal, has evaluated it diligently, and is actively undecided. Abstention - not voting at all - means the voter does not wish to express an opinion, either because they lack sufficient familiarity or because they choose not to participate in that particular poll. N votes should be rare; they represent informed indecision, not ignorance.

There is also an implicit, unrecorded form of abstention: participants who choose not to be in the room for a particular discussion. The effective voter pool for any given poll is a subset of the meeting's total attendance, filtered by self-selection into the relevant session.

### 2.2 Chair Discretion

The definition of "consensus" is not codified in a formula. The chair of each subgroup determines what constitutes consensus within their group<sup>[5]</sup>. The chair also controls the wording of each poll question. Different framings of the same underlying question can produce different vote distributions. The poll result is therefore a function of two inputs that the chair controls - the question asked and the interpretation of the answer - in addition to the votes themselves.

### 2.3 The Role of Presentation

The votes in a subgroup poll follow a presentation and question-and-answer session. The quality and persuasiveness of the presentation influence the outcome. This is by design: Deliberation is the mechanism by which the committee evaluates proposals. It also means that the poll result is not purely a measure of the proposal's technical merit. It is a composite of the proposal, the presentation, the Q&A, and the room.

---

## 3. National Body Voting

WG21 operates within ISO/IEC JTC 1/SC 22. At the working group level, individuals vote. At the international level, countries vote.

### 3.1 The Two-Tier Structure

From 1990 through 2014, WG21 conducted Friday plenary polls at two levels: first a poll of U.S. members where each company had one vote to determine the U.S. position, then a poll of WG21 heads of delegation (HoDs) where each country had one vote<sup>[9]</sup>.

In 2014, ISO changed its rules and eliminated delegations at the working group level. Each person in the ISO Global Directory became an individual participant. WG21 switched to a flat poll of all participants where each person had one vote<sup>[9]</sup>.

### 3.2 The Weighting Problem

The published minutes document what happened next:

> Since 2014, ISO switched to not having delegations (and therefore no HoDs) at the WG level. Instead, each person in the ISO Global Directory is an individual participant. So we switched to having Friday polls be a flat poll of all participants in the Global Directory where each person has one vote. This has been somewhat unwieldy to conduct polls numerically with our large group, and it has also weighted the U.S., and U.S.-domiciled companies, much more strongly than WG21 has ever done in the past.<sup>[9]</sup>

The U.S. recognized the problem. In 2016, the U.S. caucused and by unanimous consent agreed to return to the previous polling structure. Starting at the Issaquah meeting, Friday polls returned to one vote per U.S. company<sup>[10]</sup>.

### 3.3 The Asymmetry

The U.S. sends hundreds of participants from dozens of companies. Some participating countries send one to three delegates. At the national body level, each country has one vote regardless of delegation size.

Lionel Penrose established in 1946 that in a two-tier voting system, a priori voting power should scale as the square root of the constituency size to give each individual equal indirect influence<sup>[11]</sup>. The current system does not follow this principle. A participant from a country with three delegates has substantially more indirect influence on the national body vote than a participant from a country with three hundred.

### 3.4 National Body Votes in Practice

The Coroutines TS merge vote at San Diego (2018) illustrates the two-tier dynamic. The individual vote was 34 in favour, 17 opposed, 10 abstaining. The national body vote was 5 in favour, 6 opposed, 1 abstaining. The motion failed<sup>[12]</sup>. The individual majority and the national body majority pointed in opposite directions.

At the FDIS level, the rules are strict: If more than 25% of national body votes are "No," the FDIS fails outright<sup>[13]</sup>. A small number of national bodies can block a standard that the individual participants overwhelmingly support.

---

## 4. The Published Record

The following exhibits are drawn from the committee's published record: meeting minutes published as N-numbered documents on open-std.org, poll outcome papers published as P-numbered documents, and public mailing list archives. Each exhibit is independently verifiable. The paper presents these exhibits without theoretical claims about what causes the observed patterns.

### 4.1 Attendance-Dependent Outcomes

When the same question is polled at different meetings with different attendees and no change in the proposal's content, the published record sometimes shows different outcomes.

**Exhibit A (P2511).** The October 2022 electronic poll on P2511R2 ("Beyond `operator()`: NTTP Callables in Type-Erased Call Wrappers") produced SF:4 / WF:7 / N:3 / WA:1 / SA:2 - no consensus<sup>[14]</sup>. At the Kona in-person LEWG session in November 2022, the same paper received SF:2 / WF:4 / N:3 / WA:3 / SA:0. The paper could not advance in either venue, but the vote distributions differed: The electronic poll had SA votes that disappeared in person, while the in-person poll had WA votes that were absent electronically. The author's own account: "in different meeting you need to face different people in the room."

**Exhibit B (Contracts removal).** At Kona in February 2019, the poll on P1426 "Pull the Plug on Contracts?" received SF:2 / F:7 / N:4 / A:14 / SA:7 - no consensus to remove<sup>[15]</sup>. Five months later at Cologne in July 2019, P1823R0 "Remove Contracts from C++20" achieved consensus. The plenary vote was 68 in favour, 0 opposed, 4 abstaining<sup>[15]</sup>. The same fundamental question - should contracts be in C++20 - reversed from "no" to "yes" for removal.

**Exhibit C (P2300 direction vs. shipping).** The October 2021 electronic poll asked whether the sender/receiver model (P2300) is a good basis for most asynchronous use cases. The result was SF:24 / WF:16 / N:3 / WA:6 / SA:3 - consensus in favor<sup>[16]</sup>. Three months later, the January 2022 electronic poll asked to send P2300R4 to LWG for C++23. The result was SF:23 / WF:14 / N:0 / WA:6 / SA:11 - no consensus<sup>[17]</sup>. The SA count nearly quadrupled. The published outcome noted "sustained strong opposition against including such a large proposal into C++23 at such a late stage."

**Exhibit D (`inplace_vector` allocator).** The question of allocator support for `inplace_vector` was polled at Tokyo in 2024 and received SF:6 / WF:6 / N:4 / WA:5 / SA:6 - no consensus. At Hagenberg in 2025, the same question received SF:3 / WF:5 / N:1 / WA:9 / SA:11 - consensus against<sup>[18]</sup>.

**Exhibit E (Executors ad-hoc meeting).** At an ad-hoc executors meeting in Bellevue, WA in September 2018, the poll "For the long-term direction for executors we like senders/receivers" received SF:9 / F:10 / N:6 / A:2 / SA:0<sup>[19]</sup>. Twenty-seven self-selected attendees at a two-day side meeting set the direction for what became P2300 and the trajectory of C++ asynchronous programming.

**Exhibit F (Networking TS telecons).** On September 20, 2021 (36 attendees), the poll "Continue considering shipping P2300 senders/receivers in C++23" received SF:11 / WF:6 / N:5 / WA:5 / SA:4. Eight days later on September 28 (approximately 48 attendees), the same question received SF:11 / WF:9 / N:6 / WA:6 / SA:6<sup>[16]</sup>. The additional attendees shifted the distribution.

**Exhibit G (SG16 chrono locale).** SG16 polled P2372 (fixing locale handling in chrono formatters) in April 2021 and did not reach consensus. Two weeks later in May 2021, SG16 polled the revised paper and reached strong consensus: SF:5 / F:2 / N:1 / A:0 / SA:0<sup>[20]</sup>. The SG16 chair attributed the reversal to two factors: new information that arrived after the initial poll, and a different framing of the target (C++23 and C++20 as a DR, rather than C++23 alone).

**Exhibit H (Electronic vs. in-person).** [P3468R0](https://wg21.link/p3468r0)<sup>[21]</sup> (October 2024 poll outcomes) documents the committee's own debate about the tension between electronic and in-person polls. One voter comment: "It doesn't make much sense to vote twice for the same paper if the voting audience is also the same."

| Exhibit | Topic                      | Poll 1                | Poll 2                | Change              |
| ------- | -------------------------- | --------------------- | --------------------- | ------------------- |
| A       | P2511 callables            | 4/7/3/1/2 (none)      | 2/4/3/3/0 (none)      | Shifted             |
| B       | Contracts in C++20         | 2/7/4/14/7 (keep)     | 68/0/4 (remove)       | Reversed            |
| C       | P2300 as async basis       | 24/16/3/6/3 (cons)    | 23/14/0/6/11 (none)   | SA quadrupled       |
| D       | `inplace_vector` allocator | 6/6/4/5/6 (none)      | 3/5/1/9/11 (agst)     | Hardened            |
| E       | Executors direction        | 9/10/6/2/0 (cons)     | (27 self-selected)    | Direction set       |
| F       | P2300 for C++23 (telecons) | 11/6/5/5/4 (36 att.)  | 11/9/6/6/6 (48 att.)  | Shifted             |
| G       | SG16 chrono locale         | No consensus           | 5/2/1/0/0 (cons)      | Reversed (reframed) |

### 4.2 Social Pressure and Participation

The published record documents instances where the visibility of individual votes affected participation.

**Exhibit I (Named voting).** When WG21 introduced electronic straw polls during the virtual meeting era, individual votes were initially attributed by name. The published record states: "This policy change could (and actually did) cause some people to feel they could not participate, which is anathema to building technical consensus. ISO requires that participants be able to give their technical opinion freely, and forbids recording meetings for that reason." The policy was reversed<sup>[22]</sup>.

**Exhibit J (Transparency vs. consensus).** The published rationale for non-anonymous voting presents the other side of the tension: "If your vote is anonymous, it is useless for consensus building. If we don't know who voted a certain way, how can we possibly try to overcome disagreements and increase consensus?"<sup>[23]</sup> The committee chose consensus-building over anonymity, accepting the participation cost.

**Exhibit K (Self-disqualification).** Published voter comments in [P2459R0](https://wg21.link/p2459r0)<sup>[17]</sup> document self-disqualification: "I do not feel that I have sufficient information to meaningfully vote here." Another: "TL;DR I'm concerned about bake time, but feel I don't have a right to vote." These voters chose not to participate despite having opinions.

**Exhibit L (The social layer).** In a filmed interview for the Boost documentary (November 2025, Kona), Jens Maurer - the CWG Chair and C++ Standard Draft Editor, a committee member since October 2000 - was asked about whether proposals advance based on personal relationships rather than technical merit. He paused, grimaced, and said "such a question requires a very careful response." He then described how socializing with chairs helps, how being friends with a chair helps scheduling, and that a colleague "would do himself a favor for his library if he worked the social circuit rather than just being a diligent maintainer arriving and following the letter of the rules"<sup>[24]</sup>.

**Exhibit M (The honor system).** WG21 does not vet voters for familiarity with the proposal under discussion. The Direction Group's own paper ([P2000R5](https://wg21.link/p2000r5)<sup>[25]</sup>) explicitly warns against voting on proposals the voter has not reviewed, voting based on friendship or rivalry, and voting based on whether a proposal competes with the voter's own work. Compliance is on the honor system.

### 4.3 Directional Persistence

Once a proposal achieves directional consensus through a poll, the published record shows cases where that direction persisted even as circumstances changed. Alternative explanation: The direction may reflect genuine continued agreement.

**Exhibit N (Networking direction).** The October 2021 poll "Networking in the C++ Standard Library should be based on the sender/receiver model" received SF:17 / WF:11 / N:10 / WA:4 / SA:6 - weak consensus<sup>[16]</sup>. The published outcome document noted that many of the 10 neutral voters "wanted to see a concrete paper before choosing sides." Five years later, no sender-based networking library has shipped. The directional poll remains the stated direction.

**Exhibit O (Contracts removal and return).** The contracts feature was removed from C++20 in July 2019 (Exhibit B). Bjarne Stroustrup wrote in [P1711R0](https://wg21.link/p1711r0)<sup>[26]</sup>: "Status quo represents a set of tradeoffs among the concerns of people involved; starting from scratch, we'd have to balance a new set of concerns." The contracts feature returned as P2900 and accumulated directional consensus across multiple subgroup polls through 2023-2024, eventually being forwarded to LWG for C++26 with SF:23 / WF:9 / N:1 / WA:0 / SA:5<sup>[27]</sup>.

**Exhibit P (Trivial relocation).** The trivial relocation feature (P2786R13) was forwarded by subgroups and incorporated into the C++26 working paper at Hagenberg. At the Kona 2025 plenary, a procedural motion to postpone the removal vote received In Favour: 5, Opposed: 86, Abstain: 20 - overwhelmingly rejected<sup>[28]</sup>. The removal itself then passed: In Favour: 80, Opposed: 5, Abstain: 28. In this case, implementer consensus was strong enough to overcome the directional inertia.

**Exhibit Q (Status quo paradox).** Arthur O'Dwyer described a pattern on his blog: "the paradoxical result is that everyone altruistically agrees to continue with the status quo, even though the participants in the discussion all believe that the status quo is *worse* than the alternative"<sup>[29]</sup>. The mechanism: Uncertainty about whether enough others have changed their minds leads each individual to defer.

### 4.4 Subgroup and Plenary Disagreements

The published record documents cases where subgroups and plenary reached different conclusions on the same question.

**Exhibit R (Concepts for C++17).** At Jacksonville in February 2016, the plenary motion to merge the Concepts TS into C++17 received 25 in favour, 31 opposed, 8 abstaining. The motion failed<sup>[30]</sup>. Bjarne Stroustrup observed: "discussions have happened for some time in Evolution with positive results, but negative votes were only seen at plenary." Another participant noted: "sometimes at plenary only cons are heard, which might sway votes"<sup>[30]</sup>.

**Exhibit S (`std::byte`).** [P0583R0](https://wg21.link/p0583r0)<sup>[31]</sup> documents that `std::byte` "failed to pass plenary motion at the Fall 2016 Issaquah meeting, after passing all working subgroups straw polls. The failure in plenary was solely based on naming, an issue raised by the Canadian National Body."

**Exhibit T (Coroutines TS merge).** EWG voted to merge coroutines directly into C++17. The full plenary overrode that decision and sent it to a TS instead. EWG then re-approved the merge at Rapperswil in 2018, but the plenary motion failed: 29 in favour, 15 opposed, 8 abstaining, with 4 national bodies opposed<sup>[38]</sup>. At San Diego later that year, the motion failed again: 34 in favour, 17 opposed, 10 abstaining, with 6 national bodies opposed<sup>[12]</sup>. Coroutines were finally merged at Cologne in 2019.

**Exhibit U (Trivial relocation).** The trivial relocation feature was forwarded by subgroups and added to the working paper. At the Kona 2025 plenary, it was removed (Exhibit P). The published minutes note: "this motion did not represent an attempt to override subgroups. Instead, the intent was to give plenary the chance to decide whether it felt the procedure had been handled properly"<sup>[28]</sup>.

| Exhibit | Topic              | Subgroup outcome | Plenary outcome          |
| ------- | ------------------ | ---------------- | ------------------------ |
| R       | Concepts for C++17 | Positive in EWG  | 25/31/8 - failed         |
| S       | `std::byte`        | Passed all SGs   | Failed (naming)          |
| T       | Coroutines merge   | EWG approved     | Failed twice, then pass  |
| U       | Trivial relocation | Forwarded        | Removed                  |

### 4.5 The Consensus Threshold

The consensus threshold gives SA votes disproportionate weight relative to SF votes. This is a structural property of the mechanism.

**Exhibit V (P2300 for C++23).** The January 2022 poll to send P2300R4 to LWG for C++23 received SF:23 / WF:14 / N:0 / WA:6 / SA:11<sup>[17]</sup>. Thirty-seven voters favored the proposal. Seventeen opposed. The published outcome was "no consensus" with "sustained strong opposition." Under a simple majority rule, the proposal would have advanced. Under the consensus threshold, 11 SA votes blocked it.

**Exhibit W (Consensus definition).** The published schedule paper [P1000R6](https://wg21.link/p1000r6)<sup>[6]</sup> states that "strong consensus" requires a 3:1 ratio of favor to against. A voter whose true preference is Weakly Against has a structural incentive to vote Strongly Against if the consensus threshold makes SA votes more powerful than WA votes in determining the outcome. This is rational behavior under the rules as written.

**Exhibit X (Networking deadlock).** The October 2021 electronic poll produced three related results on the same topic in the same poll cycle<sup>[16]</sup>:

| Poll                                | SF | WF | N  | WA | SA | Outcome              |
| ----------------------------------- | -- | -- | -- | -- | -- | -------------------- |
| Asio is a good async basis          |  5 | 10 |  6 | 14 | 18 | Weak consensus agst  |
| S/R is a good async basis           | 24 | 16 |  3 |  6 |  3 | Consensus in favor   |
| Stop pursuing Networking TS         | 13 | 13 |  8 |  6 | 10 | No consensus         |

The committee voted against Asio as a general async model, in favor of sender/receiver as a general async model, but could not reach consensus to stop pursuing the Asio design. The three polls are internally consistent only if the SA bloc on the third poll (10 voters) was sufficient to prevent consensus on abandoning a design the committee had already voted against endorsing.

### 4.6 Poll Wording and Framing

The chair controls the wording of each poll question. The published record shows cases where different framings of related questions produced different vote distributions.

**Exhibit Y (Networking polls).** The five networking/executors polls in the October 2021 electronic poll cycle<sup>[16]</sup> asked subtly different questions about the same underlying topic:

| Question                                                   | SF | WF | N  | WA | SA | Outcome             |
| ---------------------------------------------------------- | -- | -- | -- | -- | -- | ------------------- |
| Asio is a good basis for most async use cases              |  5 | 10 |  6 | 14 | 18 | Weak consensus agst |
| S/R is a good basis for most async use cases               | 24 | 16 |  3 |  6 |  3 | Consensus in favor  |
| Stop pursuing Networking TS/Asio design                    | 13 | 13 |  8 |  6 | 10 | No consensus        |
| Networking should be based on S/R                          | 17 | 11 | 10 |  4 |  6 | Weak consensus      |
| Acceptable to ship networking without TLS                  |  9 | 13 |  5 |  6 | 13 | No consensus        |

The same voters, in the same poll cycle, produced five different distributions. The framing of each question - "is X a good basis" vs. "stop pursuing X" vs. "Y should be based on X" - shaped the result.

**Exhibit Z (SG16 chrono locale).** The SG16 chair explicitly attributed the reversal on P2372 to "different framing" of the target: C++23 and C++20 as a DR rather than C++23 alone (Exhibit G)<sup>[20]</sup>.

**Exhibit AA (Contracts framing).** Two contracts polls at different meetings asked related but differently framed questions<sup>[27]</sup><sup>[32]</sup>:

| Question                                         | SF | WF | N | WA | SA | Outcome        |
| ------------------------------------------------ | -- | -- | - | -- | -- | -------------- |
| P2900's MVP shall incorporate stricter contracts  | 10 |  6 | 3 | 14 | 16 | Consensus agst |
| P2900R6 should have enforce semantics only        |  6 |  1 | 3 | 15 | 24 | Consensus agst |

Both questions concerned the scope of the contracts MVP, but the second framing ("enforce semantics only") produced a much stronger SA bloc (24 vs. 16) and a near-total collapse of support (SF+WF = 7 vs. 16).

---

## 5. Limitations

This paper presents the published poll record. It does not claim the numbers tell the whole story.

Bimodal vote distributions on contentious topics are the expected result, not an anomaly. When committee members hold strong, informed opinions on both sides of a question, the votes naturally cluster at SF and SA. This paper does not present bimodal distributions as evidence of a pathology.

Different outcomes at different meetings may reflect genuine learning. New information, revised papers, and the deliberation process itself can legitimately change minds. Not every reversal is explained by room composition alone.

Deliberation is designed to create dependence between voters. The preceding presentation and Q&A session are supposed to influence votes. A persuasive presenter gets favorable votes; an unpersuasive one does not. This is a feature of the process, not a defect. It also means that the poll tallies alone cannot distinguish between a proposal that failed on technical merit and one that failed on presentation quality.

Poll wording matters. The chair controls the question, and different framings of the same topic produce different vote distributions (Exhibits Y, Z, AA). This paper's own exhibits are organized by the questions as worded. The reader should consider how the wording may have shaped each result.

The published poll tallies are an incomplete record. The presentation quality, the Q&A, the room dynamics, the social context, and the chair's framing are not captured in the numbers. Drawing conclusions from tallies alone is inherently limited. The numbers are the public record, not the full story. As Peter Dimov observed during review of R0: Meaningful conclusions require having been there and observed the process.

This paper presents the published record because it is the only public artifact. Simpler explanations may exist for every pattern shown. The conclusions are the reader's.

---

## 6. Corporate Influence

The structural incentives for corporate influence on standards voting are documented in the academic literature on standard-setting organizations.

Bjarne Stroustrup described the one-company-one-vote rule as an anti-stuffing measure: "Each company participating has one vote, just like each individual, so a company cannot stuff the committee with employees"<sup>[33]</sup>. The rule addresses one form of corporate influence. The literature documents others.

Walter Mattli (2017) identified two primary mechanisms of regulatory capture in transnational standard-setting: information capture (where the regulated entities possess the technical expertise and the regulator depends on them for information) and representational capture (where the regulated entities dominate the membership of the standard-setting body)<sup>[34]</sup>. Baron and Kanevskaia (2023) found that working groups chaired by employees of leading stakeholders produce standards that are less cited and less referenced than those chaired by university affiliates<sup>[35]</sup>.

Timothy Simcoe (2012) modeled standards committees using IETF data and found that distributional conflicts from commercialization slow consensus<sup>[36]</sup>. Joseph Farrell and Timothy Simcoe (2009) described consensus standardization as bargaining without side payments, producing "wars of attrition" that select through delay rather than through merit<sup>[37]</sup>.

The Direction Group's own paper ([P2000R5](https://wg21.link/p2000r5)<sup>[25]</sup>) explicitly warns against opposing a proposal "because it is seen as competing with your favorite proposal for time/resources" or because "it is not coming from your friends."

---

## 7. Future Work

Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz proposed during review of R0 a methodology for systematic analysis: Construct a dataset of all published polls, classify positive polls as successful or unsuccessful based on hard facts - rejected at a later stage, deprecated, removed, or superseded due to design problems - and then analyze correlations with voting set size, N count, evolution over time, and other measurable variables. This is the rigorous empirical approach the paper should aspire to in a future revision.

The committee's published record contains hundreds of polls across three decades. A systematic survey would move beyond the spot-check presented here and allow quantitative analysis of the patterns documented in Section 4.

---

## Acknowledgements

This paper is substantially shaped by the critique of Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz and Peter Dimov.

L&oacute;pez Mu&ntilde;oz identified that Arrow's Impossibility Theorem does not apply to WG21's single-question approval scale, proposed the Condorcet Jury Theorem as a potentially applicable framework for analyzing poll convergence, and proposed the dataset methodology described in Section 7.

Dimov demonstrated that the Condorcet Jury Theorem is inapplicable because committee members do not form opinions independently - the preceding presentation and Q&A session are designed to influence votes. He established that bimodal vote distributions are the expected result for contentious topics, not evidence of voter correlation. He clarified the distinction between Neutral votes (informed indecision) and abstention (choosing not to express an opinion). He confirmed that chair control of poll wording is a significant structural factor in outcomes.

An earlier draft attempted a theoretical approach: Apply social choice theory as a predictive framework, derive predictions, and test them against the data. That approach was tested by peer review and found wanting. This paper presents the published record without interpretive claims. It is stronger for the critique.

---

## References

- [1] Corosio: https://github.com/cppalliance/corosio
- [2] Capy: https://github.com/cppalliance/capy
- [3] [P2469R0](https://wg21.link/p2469r0): "Asio and Sender/Receiver." https://wg21.link/p2469r0
- [4] [P4050R0](https://wg21.link/p4050r0): "Failure Modes in Large-Scale Standardization." https://wg21.link/p4050r0
- [5] [P1338R1](https://wg21.link/p1338r1): WG21 2018-11 San Diego Record of Discussion. "Chair can decide what is consensus within their subgroup." https://wg21.link/p1338r1
- [6] [P1000R6](https://wg21.link/p1000r6): "C++ IS schedule." Sutter. "Strong consensus means 3:1 #favor:#against." https://wg21.link/p1000r6
- [7] N4985: WG21 2024-06 St Louis Minutes. "For plenary polls, you have to be in the ISO global directory to vote. One person, one vote." https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf
- [8] X3J16_91-0092 / WG21_N0013: Minutes of the founding meeting, 1991. "Straw votes are designed to give a good indication of how formal votes will turn out. Thus, they follow the same rules as formal votes."
- [9] N4615: WG21 2016-10-28 Telecon Minutes. Documents the 2014 ISO rule change and its effect on U.S. weighting. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4615.pdf
- [10] N4623: WG21 2016-11 Issaquah Minutes. "Starting in this meeting, for Friday polls we will be returning to one vote per U.S. company." https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4623.pdf
- [11] Penrose, L. S. "The Elementary Statistics of Majority Voting." *Journal of the Royal Statistical Society* 109: 53-57, 1946.
- [12] N4802: WG21 2018-11 San Diego Minutes. Coroutines TS merge vote. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/n4802.pdf
- [13] N1134: Minutes of J16, WG21, 10-14 November 1997. "If more than 25% of NB FDIS votes are No, the FDIS fails."
- [14] [P2649R0](https://wg21.link/p2649r0): "2022 October Library Evolution Poll Outcomes." P2511 electronic and in-person poll results. https://wg21.link/p2649r0
- [15] [P1823R0](https://wg21.link/p1823r0): "Remove Contracts from C++20." Josuttis, Voutilainen, Orr, Vandevoorde, Spicer, Di Bella. Documents the Kona 2019 P1426 poll and the Cologne 2019 removal. https://wg21.link/p1823r0
- [16] [P2453R0](https://wg21.link/p2453r0): "2021 October Library Evolution Poll Outcomes." Contains the five Networking/Executors polls with full vote tallies. https://wg21.link/p2453r0
- [17] [P2459R0](https://wg21.link/p2459r0): "2022 January Library Evolution Poll Outcomes." Contains P2300R4 for C++23 poll. https://wg21.link/p2459r0
- [18] [P3581R0](https://wg21.link/p3581r0): "No, `inplace_vector` shouldn't have an Allocator." Compiles `inplace_vector` poll history from Tokyo 2024 and Hagenberg 2025. https://wg21.link/p3581r0
- [19] [P1194R0](https://wg21.link/p1194r0): "Report on the Ad-Hoc Executors Meeting." Howes, Niebler, Shoop, Lelbach, Hollman. Bellevue, WA, September 2018. https://wg21.link/p1194r0
- [20] [P2372R1](https://wg21.link/p2372r1): "Fixing locale handling in chrono formatters." Honermann. SG16 poll history and chair attribution of reversal. https://wg21.link/p2372r1
- [21] [P3468R0](https://wg21.link/p3468r0): "2024 October Library Evolution Poll Outcomes." Voter comments on electronic vs. in-person polling. https://wg21.link/p3468r0
- [22] [P2195R0](https://wg21.link/p2195r0): "On Electronic Straw Polls." "This policy change could (and actually did) cause some people to feel they could not participate." https://wg21.link/p2195r0
- [23] [P2195R2](https://wg21.link/p2195r2): "Electronic Straw Polls." Lelbach. "If your vote is anonymous, it is useless for consensus building." https://wg21.link/p2195r2
- [24] Jens Maurer, filmed interview for the Boost documentary, November 4, 2025, Kona, HI. Filmed by Ray Nowosielski. https://vimeo.com/1140852773/f4f135ef24
- [25] [P2000R5](https://wg21.link/p2000r5): "Direction for ISO C++." Stroustrup, Hinnant, Orr, Vandevoorde, Wong. https://wg21.link/p2000r5
- [26] [P1711R0](https://wg21.link/p1711r0): "What to do about contracts?" Stroustrup. "Status quo represents a set of tradeoffs." https://wg21.link/p1711r0
- [27] [P3499R1](https://wg21.link/p3499r1): "Exploring strict contract predicates." Wroclaw 2024 EWG poll results. https://wg21.link/p3499r1
- [28] N5031: WG21 2025-11 Kona Minutes. Trivial relocation removal vote (P3920R0). https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf
- [29] O'Dwyer, Arthur. "WG21 and the National Popular Vote Compact." Blog post, April 26, 2018. https://quuxplusone.github.io/blog/2018/04/26/wg21-and-the-popular-vote-compact
- [30] N4586: WG21 2016-02 Jacksonville Minutes. Concepts TS merge vote. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4586.pdf
- [31] [P0583R0](https://wg21.link/p0583r0): "The Rationale for `std::byte`." Dos Reis. "Failed to pass plenary motion... after passing all working subgroups straw polls." https://wg21.link/p0583r0
- [32] [P3197R0](https://wg21.link/p3197r0): "Response to Tokyo EWG polls on Contracts MVP." Tokyo 2024 poll results. https://wg21.link/p3197r0
- [33] Stroustrup, B. "Evolving a language in and for the real world: C++ 1991-2006." https://www.stroustrup.com/hopl-almost-final.pdf
- [34] Mattli, W. "Industry Regulatory Capture and Transnational Standard Setting." *Cambridge Core*, 2017. https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8CAADFDDA77852E9D24958C2F9E24C5E/S2398772317000290a.pdf
- [35] Baron, J. and Kanevskaia, O. "Wearing Multiple Hats - The Role of Working Group Chairs' Affiliation in Standards Development." *Research Policy* 52(9), 2023. https://ideas.repec.org/a/eee/respol/v52y2023i9s0048733323001063.html
- [36] Simcoe, T. "Standard Setting Committees: Consensus Governance for Shared Technology Platforms." *American Economic Review* 102(1): 305-336, 2012.
- [37] Farrell, J. and Simcoe, T. "Choosing the Rules for Consensus Standardization." Working Paper, 2009. https://people.bu.edu/tsimcoe/documents/published/ConsensusRules_v2-4.pdf
- [38] N4781: WG21 2018-06 Rapperswil Minutes. Coroutines TS merge vote. https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/n4781.pdf
