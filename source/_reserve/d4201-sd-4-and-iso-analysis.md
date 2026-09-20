---
title: "Two Systems, One Committee: A Game-Theoretical Analysis of ISO Governance vs. SD-4"
document: P4201R0
date: 2026-04-20
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Two procedural documents govern WG21. One was designed by the international standards system over decades of institutional evolution across hundreds of working groups. The other was written by one person on a private foundation's website. They produce different systems. The systems produce different outcomes. The outcomes serve different constituencies.

This paper applies game-theoretic reasoning, six institutional forces documented in published research from 1911 to 2003, ten principles of human action from Ludwig von Mises, five diagnostic tests from Great Founder Theory, and more than twenty empirical studies on committee decision-making and the social cost of visible dissent to both systems. For each of eight player classes, it identifies the dominant strategy each system creates, the mechanism that creates it, and what the reader should look for in WG21's published record to observe the effect. Every central claim is accompanied by a falsification criterion - a named condition under which the claim would be wrong. The institutional prognosis distinguishes three layers: a living technical tradition, a dead governance tradition, and a direction-setting process that exhibits cargo cult properties.

---

## Revision History

### R0: August 2026 (post-St. Louis mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder and principal of the C++ Alliance and maintains competing proposals in the `std::execution` space: [P4003R0](https://wg21.link/p4003r0), [P4007R0](https://wg21.link/p4007r0), and [P4100R0](https://wg21.link/p4100r0). The author's first attended WG21 meeting was in 2018. The institutional-theory literature presented here applies to every consensus body, including bodies whose decisions the author agrees with.

The C++ Alliance funded Sean Baxter's Safe C++ project to determine whether rigorous Rust-style memory safety is achievable within C++. The research concluded that full safety requires changes to the template model incompatible with C++ - templates are a form of duck typing, and the type system would have to change. The C++ Alliance agrees with the committee's decision to pursue profiles over the Rust safety model.

This paper asks for nothing.

---

## 2. Executive Summary

The ISO/IEC Directives create a multi-principal oversight system - a constitutional republic of sovereign National Bodies with separated powers, fixed terms, formal appeals, forced feedback loops, and transparency obligations. SD-4 replaces this with a single-principal delegation model: unilateral chair appointments with no terms, a by-invitation Direction Group whose priority list and patronage credentials shape chair scheduling through focal-point dynamics rather than formal authority - influence without accountability and without any appealable decision, consensus determined by the chair alone using a 2:1 threshold absent from the Directives, meeting records sealed from public quotation, and no retrospective mechanism to evaluate whether shipped features achieved their claimed benefits.

The gap between these two systems is the structural explanation for what the committee has become. The ISO system was designed to prevent the concentration of procedural power in a self-replicating appointment chain. SD-4 does not violate those prevention mechanisms - it locates the committee's entire working machinery inside a working group, the one organizational space the Directives leave unregulated, where none of the mechanisms reach. What grew in that space is a peerage - a system of rank in which titles confer authority independent of technical contribution, patronage determines advancement, and social trust substitutes for independent evaluation. The peerage was not designed. It was the predictable institutional outcome of removing structural safeguards in a body where the median delegate is rationally ignorant about 90% of the polls they vote on, and where consensus-as-silence converts that rational ignorance into procedural legitimacy.

The institutional prognosis requires a three-layer distinction. The technical tradition is living: The committee ships world-class features, implementers carry genuine expertise, four consecutive on-time releases demonstrate real engineering capacity. The governance tradition is dead: Participants follow SD-4 without knowing the Directives, perform consensus ceremonies without the structural safeguards that give consensus meaning. The direction-setting process exhibits cargo cult properties: The committee performs the ceremony of shipping a language feature (coroutines, C++20) and the ceremony of advancing a library framework (senders, C++26), but never performs the engineering act of asking whether the two are compatible. The process measures ceremonies completed, not outcomes achieved.

---

## 3. Analytical Framework

### 3.1 Game-Theoretic Foundations

The analysis identifies players, payoff functions, dominant strategies, and equilibria for each of eight player classes under both rule sets. It assumes purposeful action (Mises 1949) - each player acts to remove their most pressing uneasiness given what they know - rather than classical rationality. The WG21 game is sequential within meetings, simultaneous across six parallel tracks, repeated indefinitely since 1990, and played under incomplete information (papers public; reflector discussions, scheduling rationales, and subgroup votes sealed).

Every analytical claim is accompanied by an observability statement - what the reader should look for in WG21's published record to confirm or disconfirm the stated effect. Claims that cannot be connected to observable evidence are not made. Specifically, the following conditions would disconfirm the central claims:

- If process-reform papers that constrain chair discretion survive at the same rate as papers that reduce chair burden, the "immune system" claim is wrong.
- If the next convener restructures the appointment chain without external pressure, the "self-replicating" claim is wrong.
- If Direction Group-endorsed priorities receive scheduling time at the same rate as non-endorsed items, the focal-point mechanism (Section 6.2) is wrong - chairs are not converging on the DG list. If DG-endorsed items receive disproportionate scheduling but this is fully explained by corporate backing and author-team size rather than DG status, the DG credential is epiphenomenal and the "zero-power influence" claim collapses to a corporate-capture claim (Stigler 1971).
- If competing proposals receive scheduling priority comparable to incumbents, the "bird-in-hand" claim is wrong.

### 3.2 Institutional Forces

Six academic forces act on consensus-driven institutions. Each names a mechanism and predicts an observable effect tested against WG21's published record (P4171R0, Falco 2026).

1. **Goal Displacement** (Merton 1940): Procedures become more important than their objective. WG21 has no requirement on implementation experience to adopt a proposal (P2274R0).
2. **Professional Socialization** (Lave & Wenger 1991): Newcomers internalize community norms. Implementer feedback is "often introduced late, treated as adversarial" (P3962R0).
3. **Representational Capture** (Stigler 1971): Entities that participate most consistently shape output. Five companies hold the majority of chair positions across EWG, LEWG, CWG, and LWG.
4. **The Iron Law** (Michels 1911, Pournelle 2006): Procedural skill predicts advancement more reliably than deployment evidence.
5. **Shifting Baseline Syndrome** (Pauly 1995): Each generation accepts current conditions as normal. Twenty-one-year networking/executor timeline described internally as a consequence of the problem's difficulty.
6. **Going Native** (Checkel 2003): Sustained engagement produces genuine preference change. Profiles endorsed unanimously by the Direction Group, voted 47-2, reaffirmed by six senior members in P3970R0 - and not in C++26.

### 3.3 Praxeological Principles

Ten principles from Mises' *Human Action* (1949) provide the economic foundations. The essential ones for this analysis:

- **Uncertainty is built into action (#1).** Every committee vote is speculative; delegates rely on heuristics.
- **Methodological individualism (#2).** Groups do not act. Specific individuals vote, schedule, and determine consensus.
- **Division of cognitive labor (#3).** The median delegate contributes deeply in their own domain and is rationally ignorant about the rest. This is specialization, not moral failure.
- **Effort at the margin (#4).** When marginal cost of engagement exceeds marginal benefit, rational disengagement follows on that issue.
- **Practical ignorance permits purposeful choice (#5).** Delegates acting on coarse information are still acting purposefully. Each vote is a genuine choice, not random noise.
- **Coordination control is outcome control (#6).** Whoever controls scheduling, poll framing, and consensus determination controls outcomes without needing to do the thinking. The pattern is publicly documented: David Abrahams (Boost mailing list, 2006) reported that a proposal he submitted in 2002 had received no serious consideration while a competing proposal had been scheduled in the evolution working group at least three times; Peter Dimov (Boost mailing list, 2024) identified the structural gatekeeping created by the LEWG chair position. Both are committee members speaking on a public list - the only quotable record, because WG21's own reflectors are sealed.
- **Rules substitute for discretion where feedback is absent (#7).** The ISO Directives are exactly this substitution. SD-4 reverses it - removes the rules, restores discretion. The Misesian prediction: Discretion without feedback will be exercised to minimize the officer's personal cost.

### 3.4 Great Founder Theory Diagnostic Tests

Five tests from Samo Burja's GFT separate functional institutions from institutions that merely imitate them: **Live Player** (can the institution do something it has never done?), **Social Technology** (living tradition vs. dead tradition), **Power Source** (owned vs. borrowed), **Functionality** (produces what it claims?), **Imitation Distance** (how many copies from the original?). Applied symmetrically to both systems in Section 8.

---

## 4. About SD-4

SD-4 creates a governance system with five compounding effects, each individually defensible, each structurally consequential, and none visible from any single rule:

**All power flows from a single appointment chain.** The Convener appoints subgroup chairs with no elections, no fixed terms, and no National Body confirmation. The chairs control scheduling, framing, and consensus determination. A by-invitation Direction Group produces a priority list that functions as a Schelling focal point for chair scheduling - the DG has no formal authority over chairs, but chairs converge on its list because deviating requires justification while following requires none (Schelling 1960). Membership is a convener-dispensed credential that doubles as a reputational multiplier in a body where the uncommitted middle votes on heuristics. Every structural filter traces back to the Convener. The chain reproduces its own composition because existing gatekeepers select the next gatekeepers (Michels 1911).

**The consensus definition is the load-bearing flaw.** SD-4 quotes the ISO consensus definition but applies it in a system where the vast majority of voters have no informed opinion on any given poll. The committee generates 300-500 papers per year; the median delegate reads 20-40. On approximately 90% of plenary polls, the median delegate is rationally ignorant (Downs 1957). SD-4's consensus mechanism counts this knowledge deficit as agreement. Even informed delegates face systematic conformity pressure under show-of-hands voting: The 2017 Italian Parliament natural experiment is the cleanest demonstration - during a secret ballot, a technical malfunction briefly displayed individual votes on a large screen; within 8 seconds at least 62 members (15% of those voting) switched (Mattozzi & Nakaguma 2023). Brazil's 2013 switch from secret to public voting on congressional expulsions nearly doubled votes in favor, in the predictable direction when the person being voted on can see the dissenter. The FDA observed the same dynamic in expert advisory committees and switched to simultaneous voting (Newham & Midjord 2019; Levy 2007). SD-4's consensus mechanism therefore operates under both the bandwidth gap and the conformity gap.

**The rules create a consensus ratchet.** Once a chair declares consensus, reversing it is procedurally nearly impossible. SD-4 says the minority must "accept group decisions" and attributes this to the ISO Code of Conduct. The phrase does not appear in the ISO Code of Ethics and Conduct (PUB100011, March 2023); it appears only on a JTC 1 presentation slide. The actual Code says "we accept and respect *consensus* decisions" - a narrower obligation paired with explicit appeal and escalation rights. SD-4 drops the word "consensus," broadens the obligation, and severs it from the rights the Code pairs it with, then uses the broadened version to characterize minority positions as Code violations. Ballot comments that revisit past decisions are "not appropriate." Repeated escalation "erodes credibility." The bird-in-hand rule gives structural priority to first-movers. Each rule is individually reasonable. Together they create a one-way valve.

SD-4's escalation provisions may address a legitimate practical concern - participants who repeatedly invoke technical dispute processes as a form of procedural obstruction. That concern is real; WG21 has experienced it. But the text connects escalation behavior to the ISO Code of Conduct and attaches normative consequences - credibility erosion and deadline forfeiture - that the Code does not authorize and the Directives do not provide for. Whether the provisions address a real problem does not determine whether they operate within the Directives' framework.

**There is no feedback loop.** No procedure exists for asking "did this feature achieve its claimed benefits?" A search of the entire WG21 paper corpus (1.4 million indexed records) returns zero papers proposing retrospectives, post-adoption evaluation, or outcome measurement for shipped features. The mailing list archives similarly contain no evidence of systematic outcome tracking. The committee measures process completion but never measures outcome quality. The compounding errors are never self-correcting (Mises #7). The coroutines arc illustrates the gap: P0975R0 (2018) called task-type library support "minimal" for a "great out of the box experience"; P2247 (2020) sounded the alarm that this plenary-approved priority was stalling; P3552 (2025) found that P2506's scheduled LEWG discussion left no discussion notes. Seven years later the "minimal" support still hasn't shipped, and no retrospective was conducted.

**The transparency regime prevents external accountability.** Meeting records cannot be quoted publicly. This is anomalous: WG14, WG5, and WG9 publish their minutes; TC39 publishes verbatim transcripts; the IETF publishes recordings. The ISO Directives themselves (Clause SF.10, 2024 edition) provide a consent-based framework for meeting recordings, and JTC 1 Standing Document 19 (2022), Section 9 explicitly adopts that framework by reference: "JTC 1 follows the ISO policy on recording technical meetings which are included in the Consolidated ISO Supplement, Annex SF Clause 10." ISO published guidance in 2025 explicitly permitting AI transcription under this framework. WG21's information seal operates outside not only the ISO framework but the framework JTC 1 has explicitly adopted - it is an SD-4 invention, not an inherited ISO norm.

---

## 5. The Organizational Question

The Directives describe working groups as comprising "a restricted number of Experts individually appointed by the P-members" (1.12.1)<sup>[1]</sup>. A working group should be "reasonably limited in size" and is "brought together to deal with the specific task allocated to the working group." On completion of its tasks, the working group is disbanded. On subgroups, the Directives provide a single sentence: "Working Groups may establish subgroups" (1.12.1) - no appointment procedure, no term limits, no oversight requirements. The silence is deliberate and literal: The Directives impose no rules on working group subgroups at all. Subgroups are neither required to have chairs nor forbidden from having them; their internal arrangements are entirely a matter for the working group.

WG21 operates at a scale the Directive model did not anticipate. Plenary attendance at recent meetings: 180+ (St. Louis, July 2024), 220+ (Wroclaw, November 2024), ~200 (Kona, November 2025), ~210 (London/Croydon, March 2026), drawn from 20-31 nations per meeting. The committee maintains 4 permanent main subgroups (CWG, LWG, EWG, LEWG), 13+ study groups, 3 advisory/administrative groups, and runs multiple parallel tracks simultaneously across full-week meetings three times per year.

### 5.1 What the Silence Means

An earlier line of analysis asked whether WG21's main subgroups are working groups in all but name, and whether the working group governance requirements of 1.12.1 (committee appointment, three-year terms, NB confirmation) therefore ought to apply to their chairs. That reading does not survive contact with the text. The 1.12.1 governance requirements attach to working group convenors - the WG21 convenorship itself - and to nothing inside the working group. The subgroup sentence was added precisely to settle that subgroups exist outside the Directive rule set. There is no deviation to authorize under 1.4, because there is no rule to deviate from.

The consequence of the silence cuts the other way, and it is sharper than any deviation claim. ISO does not recognize WG-internal structure. In ISO terms there is no such thing as a "WG21 plenary," an EWG consensus, or a Direction Group priority. None of these bodies or decisions has any procedural standing under the Directives. They cannot create obligations for National Bodies, cannot narrow NB ballot rights (2.6.2-2.6.5), and cannot characterize an NB ballot comment as improper. The first decision in the C++ standardization pipeline that exists in ISO terms is the SC 22 ballot, where National Bodies vote.

| What WG21 treats as a decision | ISO procedural standing |
|---|---|
| Subgroup poll (EWG, LEWG, CWG, LWG, SGs) | None - internal working method |
| "WG21 plenary" consensus | None - ISO recognizes no WG-internal plenary |
| Direction Group priority list | None - internal advisory practice |
| SD-4 provisions | None - internal practice document, binding on no NB |
| SC 22 DIS/FDIS ballot | Full - NB votes under 2.6.3/2.7.3, comments under 2.6.2-2.6.5, appeals under 5.1 |

### 5.2 Organizational Taxonomy

The Directives define three types of subsidiary body:

**Working groups (1.12).** Established by a committee for specific tasks. Convenors appointed by the committee for up to three-year terms with NB confirmation and no limit on reappointment. Comprise experts individually appointed by P-members. Operate by consensus. Disbanded on task completion.

**Advisory groups (1.13).** Established by a committee "to assist the Chair and secretariat in tasks concerning coordination, planning and steering of the committee's work." Available to committees (TCs/SCs), not to working groups. Require committee approval of convenor, membership, and terms of reference (1.13.2).

**Ad hoc groups (1.14).** Study a "precisely defined problem" and report to the parent committee. In JTC 1, working groups may create ad hoc groups. Require committee-approved convenors, terms of reference, and a target completion date. Disbanded when the work is complete.

WG21's four main subgroups match none of these types, and that is the point: They are not ISO bodies. The taxonomy stops at the working group boundary. Everything inside - the subgroup chairs, the polls, the forwarding decisions, the "plenary" - is internal working method with no existence in the ISO organizational framework. The committee is free to organize itself this way. What it is not free to do is treat the outputs of that internal structure as carrying ISO authority over National Bodies.

### 5.3 Comparable Bodies

| Working Group | Parent SC | Typical Attendance | Internal Subgroups | Meeting Format |
|---|---|---|---|---|
| WG14 (C) | SC 22 | ~30-35 | Standing study groups (e.g. CFP) with long-serving chairs and independent meeting schedules, structurally similar to WG21's subgroups; differs in topic coverage and scale, not in kind | 2x/year |
| WG5 (Fortran) | SC 22 | ~23 | None; delegates to US national body J3 | 2x/year |
| WG9 (Ada) | SC 22 | Small | 3 rapporteur groups meeting between sessions | 1-day meetings, 2x/year |
| SC 27 WGs | SC 27 | Small per WG | None per WG; structure is at the SC level (5 WGs) | 2x/year |
| SC 7 WGs | SC 7 | Small per WG | None per WG; 14 WGs at SC level | 2x/year |
| SC 42 WGs | SC 42 | Small per WG | None per WG; 5 WGs at SC level | 2x/year |
| **WG21 (C++)** | **SC 22** | **200+** | **23 subgroups, multiple parallel tracks** | **3x/year, full week** |

Internal subgroup structures with long-serving chairs are not unique to WG21 - WG14 runs the same model at smaller scale, and nothing in the Directives discourages it. The structural observation is about scale and where decisions live: In every other JTC 1 context examined, when a technical domain requires hundreds of experts and parallel work streams, the work is organized as a subcommittee with multiple focused working groups - each an ISO body whose decisions carry ISO standing. No other JTC 1 working group maintains a procedural supplement comparable to SD-4; WG9 states that all its standards are "developed in accordance with the JTC1 Directives"<sup>[66]</sup> - no supplement needed.

### 5.4 The MPEG Precedent

The other JTC 1 working group that developed an internal subgroup structure at comparable scale, with permanent chairs running multi-day parallel sessions, was MPEG (SC 29/WG 11)<sup>[67]</sup>. Established in 1988, MPEG grew from 100 members within 18 months to 200 within two years, eventually reaching several hundred participants per meeting. Like WG21, MPEG developed permanent internal subgroups with appointed chairs - Audio, Video, Systems, Test, Requirements. Like WG21, MPEG's subgroup chairs set agendas, ran multi-day sessions, and exercised de facto authority over their technical domains.

In 2020, SC 29 formally restructured MPEG<sup>[68]</sup>. Its subgroups were elevated into proper SC 29-level working groups (WG 2 through WG 8) and advisory groups. The JTC 1 Strategic Business Plan describes the restructuring as "deconstructing a very large working group into 7 working groups of more manageable size" for "improved governance and greater agility"<sup>[69]</sup>. SC 29's Chair observed that MPEG "had become too diversified to be a working group"<sup>[70]</sup>.

ISO/TC 211 (Geographic Information) published internal documentation addressing this structural question<sup>[71]</sup>:

> "According to ISO directives and how most of the support IT-system is built, ISO expects a working group to work on one Standard. Within ISO/TC 211, we have working groups that have more than one project within the same area of expertise. Our working groups have then more the function of what in ISO Directives is described as subcommittees."

TC 211 considers having multiple projects per working group unusual enough to explain. WG21's four main subgroups collectively process hundreds of proposals across the entire C++ language and standard library.

---

## 6. Per-Player Analysis

Each entry below presents the SD-4 dominant strategy and the ISO counterfactual. The same players adapt differently under different rules.

### 6.1 The Convener

**Under SD-4:** Preserve the appointment chain. Avoid controversy. Unilateral appointment power with no committee vote, no term limit, no NB confirmation means the selection criterion is institutional alignment, not technical contribution (Michels 1911, Mises #7). The convenership was held by a single occupant for more than two decades. The structural relationships survived the 2026 transition intact.

**Under ISO:** The convenorship is the one office inside WG21 that ISO actually governs: appointed by SC 22 for three-year terms, confirmed by the National Body, reappointable without limit (1.12.1), implementing TMB policy (1.8.2h). The Directives impose nothing on subgroup chairs - any term structure or reappointment cycle for them would be a voluntary WG21 policy choice, not an ISO requirement. The counterfactual is what such a cycle does to incentives: Where an appointing body evaluates performance at reappointment, selection shifts from loyalty-based to merit-based.

### 6.2 The Direction Group

**Under SD-4:** The DG has no structural power. It cannot direct chairs to schedule anything, cannot veto a proposal, cannot mandate a priority. It produces a "priority list" that chairs may or may not follow, and it confers a credential - "Direction Group member" - on its appointees. In practical terms, membership is a reward the convener dispenses. The anticipated defense - "the DG is purely advisory; it has no power" - is precisely the structural feature that makes the DG unchallengeable. Formal authority can be appealed, term-limited, reformed, constrained. Advisory influence through a patronage credential cannot be checked because there is no decision to appeal, no authority to constrain, no term to expire.

Five game-theoretic mechanisms explain how zero structural power produces real scheduling effects:

1. **Schelling focal point** (Schelling 1960). The DG priority list is the salient coordination default for chairs scheduling hundreds of papers per cycle. Deviating requires justification; following requires none.
2. **Strategic information transmission** (Crawford & Sobel 1982; applied to committees by Gilligan & Krehbiel 1987). Costless messages influence when sender and receiver interests are aligned. DG members and chairs are selected by the same appointment chain. The advice is credible because the adviser and the decision-maker were chosen by the same patron.
3. **Rank-order tournament** (Lazear & Rosen 1981; applied to committee leadership by Fong & McCrain 2025). When a prize (the credential) is awarded by a single decision-maker, aspirants compete on the dimension the decision-maker values - institutional alignment - producing self-censorship on governance questions without any explicit rule requiring it.
4. **Heuristic amplifier** (Bikhchandani et al. 1992). "DG member endorses X" is a low-cost, high-credibility signal for the rationally ignorant uncommitted middle (Section 6.7), tilting the starting conditions of informational cascades.
5. **Distributed irresponsibility.** When a DG-endorsed priority consumes years of bandwidth and fails to deliver (Section 6.9; [P4099R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r2.pdf)<sup>[54]</sup>), the DG only advised, the chair only scheduled voluntarily, and the convener only appointed. Each actor behaved locally rationally. The system-level outcome has no accountable author.

The DG does not violate any Directive - the Directives do not reach inside a working group, and the advisory-group rules of 1.13 are available to committees, not to WGs, so they neither authorize nor constrain it. The correct characterization is jurisdictional: The DG has no existence in the ISO framework. Its priority list has no ISO procedural status, binds no chair and no National Body, and produces no appealable decision. It has no terms of reference, no committee-approved membership, no sunset clause, and no reporting obligation - not because those were required and omitted, but because no ISO rule applies to it at all.

**Under ISO:** An advisory function with ISO standing would live at the committee level: SC 22 advisory groups require committee approval of convenor, membership, and terms of reference (1.13.2), must be disbanded when tasks are complete (1.13.6), and produce recommendations only (1.13.3). Each of those constraints is also an accountability surface - a decision that can be reviewed, a term that expires, a mandate that ends. The DG, existing outside the framework, has influence without any of them.

### 6.3 Subgroup Chairs

**Under SD-4:** Maximize throughput. Minimize conflict. Deprioritize difficult work. SD-4 grants unconstrained discretion over scheduling, time-boxing, poll ordering, and consensus determination with no fixed terms and no ex-post review (Mises #7, Romer & Rosenthal 1978). The chair roster maps directly to employer names (Stigler 1971; Kanevskaia et al. 2023 document the same pattern at IETF and 3GPP):

| Company | Positions |
|---------|-----------|
| NVIDIA | EWG chair, DG rotating chair |
| Microsoft | LEWG chair |
| IBM/Red Hat | CWG vice-chair, LWG chair |

The institutional immune system operates through chairs: Reforms that address chair pain points succeed (P2138R4 progressed through 5 revisions in ~1 year and was adopted, shifting burden from chairs to design groups); reforms that constrain chair discretion die in the scheduling queue. The same corpus search (Section 4) returns zero papers proposing term limits for subgroup chairs, election of chairs, scheduling transparency requirements, or chair accountability mechanisms. The absence is itself data: The immune system operates not by rejecting reforms but by ensuring they are never proposed. P2138R4 is a partial counterexample - the system can adopt process reforms when they align with chair incentives. The narrower claim is that reforms against chair incentives face structural headwinds, and the test is the differential survival rate.

**Under ISO:** The Directives impose none of this on subgroup chairs - the accountability package (three-year terms, NB confirmation, 1.12.1) attaches to convenors, consensus-in-consultation (2.5.6) and summing up all views (1.8.2d) to committee officers. The counterfactual is a committee that voluntarily adopts the same package for its internal chairs: The immune system is then checked by the periodic accountability moment.

### 6.4 National Bodies and Corporate Delegations

**Under SD-4:** NBs ratify rather than challenge, making "good enough" judgments from coarse signals filtered through the information seal (Mises #5, #9). SD-4 declares two categories of ballot comments "not appropriate" and redefines the "No" vote as a kill vote for the entire project, compressing the ballot to a near-binary choice. Corporate delegations staff chair positions, send consistent delegations, and establish bird-in-hand priority. The gains are concentrated (employer product roadmap, competitive positioning), so heavy investment is individually rational (Mises #9 inverted, Stigler 1971).

**Under ISO:** NBs become active principals. The rights they already hold are the operative ones: Unrestricted ballot comments (2.6.2), all comments must be addressed (2.6.5), and appeal rights at three levels (5.1) provide a credible outside option that no WG-internal document can narrow. NB confirmation of the convenor appointment (1.12.1) is the structural check ISO actually provides; extending an equivalent check to internal chair positions would be a WG21 policy choice. Corporate participants still dominate through expertise and travel capacity, but the NB ballot remains the one decision point with ISO standing, and it belongs to the NBs alone.

### 6.6 Paper Authors

**Under SD-4 (Incumbent):** Accumulate procedural momentum. After years of revision, marginal cost of abandonment exceeds marginal cost of continuing (Mises #4). The revision count becomes a proxy for quality (Merton 1940). The follow-up paper exception lets the incumbent revise in real time while the challenger waits.

**Under SD-4 (Challenger):** Start extremely early or do not challenge at all. Every procedural force works against late entry: one-meeting delay window, leftover scheduling time, bird-in-hand disadvantage (Mises #4).

**Under ISO:** Authors invest in addressing minority concerns because unresolved opposition retains institutional standing and appeal rights (2.5.6). Challengers get a fair hearing - the Directives contain no first-mover doctrine.

### 6.7 The Uncommitted Middle

**Under SD-4:** Vote with the room. Minimize personal exposure. Three Mises principles converge: Uncertainty (#1) makes heuristics dominate; division of labor (#3) makes the bandwidth gap structural; marginal effort (#4) makes full engagement irrational. The conformity mechanisms documented in Section 4 - sequential voting, observability pressure, stigmatization of dissent - apply with full force here. WG21's five-way poll (SF/WF/N/WA/SA) makes SA the most stigmatized position, and the convergent prediction across the conformity literature<sup>[35]</sup><sup>[37]</sup><sup>[38]</sup><sup>[39]</sup><sup>[42]</sup><sup>[43]</sup> is that SA is systematically underrepresented in show-of-hands counts. SD-4's consensus-as-silence converts the resulting default mild agreement into procedural legitimacy.

Each individual vote is purposeful (Mises #5). The critique is not that individual votes are random. It is that the aggregation mechanism stamps "consensus" on a collection of purposeful-but-coarse choices, implying informed collective agreement the inputs do not support.

**Under ISO:** The voter pool shifts from "each person in the room" to NB-appointed registered experts (1.12.1). The bandwidth gap still exists, but the evaluation pool is curated by NBs rather than self-selected by attendance.

A documented case from a comparable standards body corroborates the structural concern. In 2024-2025, cryptographer Daniel J. Bernstein filed formal appeals to the IETF Internet Engineering Steering Group alleging that TLS Working Group chairs censored technical objections during "last call" periods by delaying dissenting messages, reducing their impact (Bernstein 2025). Bernstein's appeal documented that participants worried "speaking up will result in retaliation by the WG chairs." The IETF's appeals mechanism exists precisely so this concern can be tested in a process visible to the broader community via a public datatracker. SD-4 contains no comparable mechanism: Dissent suppression, if it occurred, would not surface on a public datatracker because there is no public datatracker.

### 6.8 The C++ Public

**Under SD-4:** Voice (Reddit, blogs, conference talks) transitioning to exit. Five million developers cannot vote, cannot submit papers, and experience the committee's output as accomplished facts in compiler release notes. The public-good structure means individual engagement cost exceeds individual benefit (Olson 1965).

The Hirschman (1970) exit trajectory is visible in two distinct layers that should not be conflated. The first is memory-safety exit, driven by a genuine technical gap in C++ that exists regardless of WG21's governance structure:

- Microsoft announced a dedicated team building AI-powered tools to migrate C/C++ to Rust at scale, targeting 2030, with 36K lines of Windows kernel and 152K lines of DirectWrite already rewritten.
- Google Android documented 1000x reduction in memory safety vulnerability density with Rust vs. C++. Chrome policy: Handling untrustworthy data in C++ violates security requirements for privileged processes.

These are evidence of technical pressure on C++, not evidence of governance failure. C++ would face the same memory-safety pressure under any procedural regime.

The second layer is process exit - where individuals or teams disengage because they believe the WG21 process will not produce what they need. This is the relevant evidence for the governance argument:

- The C++ Alliance funded Sean Baxter's Safe C++ project to determine whether Rust-style memory safety is achievable in C++. The research concluded it is not - templates are duck typing, and the type system would have to change. The committee was right to pursue profiles (Section 1). Baxter's exit ("The Rust safety model is unpopular with the committee. Further work on my end won't change that") is the correct conclusion of funded research, not a governance failure. The governance failure is that the endorsed direction (profiles) still has not shipped (Section 7).
- Modules shipped in C++20 on a trajectory insiders describe as "borderline unimplementable," with critics "shot down by a group of higher-up people" (see Section 6.9 parallel cases).
- Implementers in P3962R0 document that features accumulate faster than they can implement; the natural response of repeated, sustained complaints from the implementation community is itself a process-exit signal.

The information seal prevents the public from seeing the structure. They correctly identify dysfunction but misattribute its causes to individual actors or corporate conspiracies because the structural understanding is sealed behind the information barriers the structure creates.

**Under ISO:** The information seal is broken. Decisions in writing during meetings (1.8.2e), posted within 48 hours (1.9.2c), electronic platform for transparency (1.12.6). The Hirschman trajectory shifts from exit back toward voice because voice has a verifiable target.

### 6.9 Case Study: Coroutines and Senders

The coroutines/senders arc demonstrates all four SD-4 mechanisms operating on a single technical trajectory - the open-loop failure at its most damaging.

The committee shipped coroutines in C++20. The natural next step - exploring what a coroutine-native asynchronous programming model looks like, what library support it needs, how it composes, what a standard task type built around coroutine primitives would be - was never taken. Instead, the committee invested four years and enormous bandwidth into P2300, a sender/receiver framework designed around a different computational model that treats coroutines as a thing you plug in at the edges rather than the foundation you build on.

**Bird-in-hand:** P2300 had a paper, authors, revisions, and directional consensus from the October 2021 polls. A coroutine-native async model had no paper with comparable institutional momentum. Under SD-4, the concrete proposal advances; the hypothetical alternative "does not exist."

**Consensus ratchet:** The October 2021 poll ("sender/receiver is a good basis for most asynchronous use cases" - SF:24/WF:16/N:3/WA:6/SA:3) locked direction before the alternative was explored. P4129R1 Exhibit N documents that five years later, no sender-based networking shipped, but the directional poll remained the stated direction.

**Scheduling funnel:** P2300 was a Direction Group priority - not a mandate (the DG has no scheduling authority), but a focal point that chairs converged on because following the credentialed list requires no justification while deviating from it does (Section 6.2). It consumed LEWG bandwidth across multiple cycles. A coroutine-native alternative competed for whatever time remained. If no time remained, it was never heard. Nobody rejected it. It simply never arrived. The full evidence chain is documented in [P4099R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r2.pdf)<sup>[54]</sup>.

**Bandwidth gap:** The October 2021 poll had 52 voters deciding whether sender/receiver was the right async basis when the alternative - the language feature just shipped in C++20 - had never been prototyped as a complete framework within the committee process. The room voted on a question it lacked the information to answer.

What users got: std::execution::task with 16+ known issues cataloged by its own designer (P3796R1), including stack overflow from iterative co_await, broken RAII guarantees, and dangling references (P3801R0) - shipped known-flawed under time pressure. std::generator still missing from libc++ as of mid-2026, five years after C++20 coroutines. A P2300 co-author acknowledging the framework is "challenging to work with and difficult to fully understand" and "as voted is incomplete." Four structural gaps when senders meet coroutines (P4007R0) characterized as inherent design trade-offs, not fixable defects.

The loop was never closed because it was never opened. No retrospective asked: "we shipped coroutines three years ago - did we build the library support that makes them useful?"

### Parallel Cases: Modules and Contracts

The same four SD-4 mechanisms appear in two other recent trajectories, without the author conflict that colors the senders example.

**Modules (C++20):** Shipped in C++20 with zero practical tooling. Jussi Pakkanen (Meson author, 2025): "There were no implementations, no test code, no prototypes, nothing." An insider reported that "there were people who knew about the implementation difficulty and were quite vocal that modules as specified are borderline unimplementable. They were shot down by a group of higher-up people." CMake module support remains incomplete in 2026 (Ropert 2026); Visual Studio IntelliSense is still flagged as "experimental" seven years after Microsoft pushed for standardization. The loop was never closed: No retrospective asked whether modules achieved the build-time improvements they promised.

**Contracts (C++26):** Adopted into the C++26 Working Draft at Hagenberg (Feb 2025). Twenty-plus NB comments from 19 of 26 national bodies followed (O'Dwyer 2025). Spain, the US, France, and Finland requested complete removal; Romania requested removal conditional on redesign of the "ignore" semantic. P4005R0 (guaranteed enforcement) was rejected by EWG (14 SA). P4043R0 questioned readiness. The final DIS vote was non-unanimous. The consensus ratchet operated as predicted: Directional consensus was declared, and NBs who object are told their comments are "not appropriate" or "out of harmony with the ISO Code of Conduct."

Both exhibit the same pattern as senders - bird-in-hand, consensus ratchet, scheduling funnel, no feedback loop - without the author conflict that colors the coroutines example.

---

## 7. Case Study: Profiles and the Direction Group

The senders/networking arc (Section 6.9) demonstrates the DG focal-point mechanism producing a shipped framework whose key claim was unevidenced. The profiles arc demonstrates something more revealing: the DG focal-point mechanism failing to deliver the DG's *own* endorsed direction, even when the architect of that direction sits on the DG.

| Date | Event | Result |
|------|-------|--------|
| Jan 2023 | DG unanimous opinion [P2759R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2759r1.pdf)<sup>[58]</sup> | Profiles named as safety mechanism; SG23 created |
| Feb 2023 | Issaquah: [P2816R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2816r0.pdf)<sup>[59]</sup> presented to SG23/EWG | 47 for, 2 against |
| Jun 2023 | Varna: competing Rust-model papers | Consensus against further work |
| Nov 2024 | Wroclaw: Profiles vs Safe C++ priority poll | 19 Profiles, 9 Safe C++ |
| Nov 2024 | Wroclaw: initialization profile [P3081R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3081r0.pdf)<sup>[60]</sup> | 18-1 consensus, forwarded to EWG |
| Feb 2025 | Hagenberg: language safety white paper | SF:32/F:31/N:6/A:4/SA:4 |
| Jan 2026 | [P3970R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3970r0.pdf)<sup>[61]</sup> call to action (five current/former DG) | "SG23 and EWG have repeatedly... pointed to Profiles" |
| Jun 2026 | Result | Not in C++26 |

### The alternative was correctly rejected

The C++ Alliance funded Safe C++ (Section 1). The research answered the question: Rigorous Rust-style memory safety requires changes to the template model that would make C++ no longer C++. The committee was right to pursue profiles. This forecloses the defense that non-delivery was caused by a bad bet.

### Endorsement over engineering

Without the DG credential, the architect's dominant strategy would have been the same as Baxter's or Kohlhoff's: Build a working implementation, produce measurable evidence, let the work speak. That is the engineering path - the path that produced Asio (20 years of deployment), Circle (working borrow checker), Capy and Corosio (3 months).

With the DG credential, the dominant strategy shifted to endorsement-first. A 47-2 vote takes one meeting. A working profile checker takes years. Game theory predicts agents take the cheapest path to their goal. The DG made ceremonial endorsement cheaper than engineering evidence. The architect took the cheaper path - not because of any personal failing, but because the incentive structure made it rational. The DG is optimized for direction-setting and alternative-killing. It has no mechanism for delivery. The credential substituted for the compiler.

### Policy-based evidence making

The UK House of Commons Select Committee on Science and Technology coined the term "policy-based evidence making" in 2006 to describe decision-makers who "selectively pick pieces of evidence which support an already agreed policy." The DG's recurring directions paper (P2000 series) is the evidence base. Chairs selectively amplify DG directions that align with their preferences and silently ignore the rest.

When a chair's interests align with a DG direction, the direction provides cover: "I scheduled X because it's a DG priority." The chair's discretionary power becomes invisible. When a chair's interests conflict with a DG direction, the chair simply does not schedule it. The cost is zero - the DG has no enforcement mechanism, meeting records are sealed, and the "purely advisory" framing is the chair's own shield.

The DG endorsed profiles three times. The chairs who control EWG and LEWG scheduling prioritized senders, contracts, and other work. The endorsement was loud. The scheduling response was silent. And the silence was invisible.

### Falsification criterion

If profiles ship in C++29 with compiler enforcement and empirical coverage evidence (the PAVE methodology in [P4137R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4137r0.pdf)<sup>[62]</sup> or equivalent), the "DG hindered delivery" claim was premature - the timeline was normal for a feature of this scope. If profiles ship without empirical coverage evidence, the ceremony-over-engineering diagnosis stands regardless of the ship date.

---

## 8. The Gap

The ISO system provides seven structural properties that serve as countermeasures to the forces identified in Section 3: distributed authority (no single person holds appointment, scheduling, priority-setting, and consensus-determination simultaneously), fixed terms as accountability moments (3-year convenor terms with committee reappointment and NB confirmation, 1.12.1), consensus as negotiated outcome (requiring reconciliation of conflicting arguments, 2.5.6), the appeal chain as credible outside option (three levels, 5.1), NB sovereignty (inherent rights not narrowable by committee-level documents), forced feedback loops (comments must be addressed, negative votes resolved, projects cancelled after 5 years, 2.5.3/2.6.5/2.1.6), and no punishment for objection (objectors directed to appeals, 2.5.6).

Every one of these countermeasures operates at the committee level. None reaches inside a working group - and SD-4 locates the committee's entire effective decision-making inside one:

| Peerage Property | ISO Countermeasure (committee level) | Under SD-4 (out of the countermeasure's reach) |
|---|---|---|
| Titles confer authority independent of contribution | Fixed terms force periodic re-earning (1.12.1, convenors) | Subgroup chairs: "No fixed term" |
| Patronage determines advancement | Committee appoints, NB confirms (1.12.1, convenors) | Convener appoints alone |
| Social trust substitutes for evaluation | Chair must sum up all views (1.8.2d); consensus in consultation (2.5.6) | Chair determines alone; 2:1 threshold |
| Objection is penalized | No penalty; objectors directed to appeals (2.5.6) | "Erodes credibility" |
| The room reads the person, not the paper | Decisions in writing, posted within 48 hours (1.8.2e, 1.9.2c) | Meeting records sealed |
| Priority follows patronage | TMB allocates priorities (1.1f) | DG focal point (by-invitation, zero authority, un-appealable) |
| System cannot distinguish consensus from compliance | Forced feedback: comments addressed, negative votes resolved (2.5.3, 2.6.5) | No retrospective; revisiting decisions "inappropriate" |

### GFT Prognosis

**Live Player**

- *ISO:* Untested but structurally enabled. The appeal chain (5.1), fixed-term reappointment (1.12.1), and multi-principal structure mean governance novelty can originate from any NB, not only from the officers being challenged. Structural capacity, not demonstrated behavior in WG21.
- *SD-4:* Tested, and the answer is no. The system has never adopted a governance reform against officer incentives. P2138R4 - the only process reform found - aligned with chair incentives. Three Profiles endorsements, zero structural change.

**Social Technology**

- *ISO:* Living tradition. The Foreword explicitly states the six WTO principles the rules exist to safeguard.
- *SD-4:* The technical social technology is living - implementers carry genuine expertise, the committee ships real features. The governance social technology is dead tradition: Participants follow SD-4 without knowing the Directives. The direction-setting process exhibits cargo cult properties: The committee shipped coroutines (C++20) and invested six years into a library framework built on a different computational model without asking whether they compose (Section 6.9). The process measures ceremonies completed, not outcomes achieved.

**Power Source**

- *ISO:* Mixed correctly. NB sovereignty is owned (inherent in P-member status), officer authority is borrowed (revocable at reappointment).
- *SD-4:* Structurally contradictory. Chair authority is owned power (no term, no review), but the legitimacy that makes WG21's output an ISO standard is borrowed from the ISO framework. Metastable: Persists as long as no one tests the borrowed component.

**Functionality**

- *ISO:* Functional - the system produces what it claims.
- *SD-4:* Technically productive (ships standards, on-time, high quality) and governance-non-functional: The consensus mechanism does not produce the informed collective agreement it claims. The dysfunction surfaces downstream: NB comments, implementer complaints (P3962R0), the coroutines/senders open-loop failure, and the Hirschman exit that Microsoft's 2030 Rust migration and Google's Chrome policy represent.

**Imitation Distance**

- *ISO:* First generation - the Directives are the original.
- *SD-4:* Third-generation copy. SD-4 quotes the ISO consensus definition while replacing every structural safeguard the definition was designed to operate within.

---

## 9. References

1. ISO/IEC. "ISO/IEC Directives, Part 1 - Consolidated JTC 1 Supplement." 2023.
2. ISO/IEC. "ISO/IEC Directives, Part 1 - Consolidated ISO Supplement." Edition 2024.
3. Davidson, G. "SD-4: WG21 Practices and Procedures." ISO/IEC JTC1/SC22/WG21/SD-4, 2026-05-11. (SD-4 provisions quoted in this paper predate the current convenor and were authored and maintained by Herb Sutter during his tenure as convenor through 2025.)
4. Ballman, A. P2274R0. 2020.
5. Ranns, N. et al. P3962R0. 2026.
6. Voutilainen, V. P2138R4. 2021.
7. Dominiak, M. et al. P2300R10. 2024.
8. Vandevoorde, D. et al. P3970R0. 2026.
9. K&uuml;hl, D. P3796R1. 2025.
10. Lewis Baker. P3801R0. 2025.
11. Falco, V. P4007R0. 2025.
12. Falco, V. P4129R1. 2025.
13. Falco, V. P4171R0. 2026.
14. Merton, R.K. "Bureaucratic Structure and Personality." *Social Forces* 18(4). 1940.
15. Lave, J. & Wenger, E. *Situated Learning*. Cambridge UP. 1991.
16. Stigler, G. "The Theory of Economic Regulation." *Bell J. Econ.* 2(1). 1971.
17. Michels, R. *Political Parties*. 1911.
18. Pauly, D. "Shifting Baseline Syndrome." *Trends Ecol. Evol.* 10(10). 1995.
19. Checkel, J.T. "'Going Native' in Europe?" *Comp. Pol. Stud.* 36(1-2). 2003.
20. Mises, L. von. *Human Action*. 1949.
21. Bikhchandani, S. et al. "Informational Cascades." *J. Pol. Econ.* 1992.
22. Newham, M. & Midjord, R. "Do Expert Panelists Herd? Evidence from FDA Committees." DIW Discussion Papers, No. 1825, 2019.
23. Lorenz, J. et al. "Social influence undermines wisdom of crowds." *PNAS*. 2011.
24. Feddersen, T. & Pesendorfer, W. "Convicting the Innocent." *APSR* 92(1). 1998.
25. Visser, B. & Swank, O.H. "On Committees of Experts." *QJE* 122(1). 2007.
26. Downs, A. *An Economic Theory of Democracy*. 1957.
27. Barbera, S. et al. "Generalized Median Voter Schemes." *J. Econ. Theory*. 1993.
28. Romer, T. & Rosenthal, H. "Controlled Agendas." *Public Choice*. 1978.
29. Olson, M. *The Logic of Collective Action*. 1965.
30. Hirschman, A.O. *Exit, Voice, and Loyalty*. 1970.
31. Arrow, K.J. *Social Choice and Individual Values*. 1951.
32. Burja, S. *Great Founder Theory*.
33. Teodorescu, L.R. "Senders/Receivers in C++." lucteo.ro. 2024.
34. Levy, G. "Decision Making in Committees: Transparency, Reputation, and Voting Rules." *American Economic Review* 97(1), 2007.
35. Mattozzi, A. & Nakaguma, M.Y. "Public versus Secret Voting in Committees." *Journal of the European Economic Association* 21(3), 2023. (Documents the 2017 Italian Parliament incident and the 2013 Brazil expulsion-procedure change.)
36. Name-Correa, A.J. & Yildirim, H. "Social Pressure, Transparency, and Voting in Committees." *Journal of Economic Theory* 184, 2019.
37. Funk, P. "Social Incentives and Voter Turnout: Evidence from the Swiss Mail Ballot System." *Journal of the European Economic Association* 8(5), 2010.
38. Schachter, S. "Deviation, Rejection, and Communication." *Journal of Abnormal and Social Psychology* 46(2), 1951, pp. 190-207.
39. Marques, J.M., Yzerbyt, V.Y. & Leyens, J.-P. "The 'Black Sheep Effect': Extremity of Judgments towards Ingroup Members as a Function of Group Identification." *European Journal of Social Psychology* 18(1), 1988.
40. Janis, I.L. *Victims of Groupthink*. Houghton Mifflin, 1972; revised as *Groupthink: Psychological Studies of Policy Decisions and Fiascoes*, 1982.
41. Noelle-Neumann, E. *The Spiral of Silence: Public Opinion - Our Social Skin*. University of Chicago Press, 1993.
42. Matthes, J., Knoll, J. & von Sikorski, C. "The 'Spiral of Silence' Revisited: A Meta-Analysis on the Relationship Between Perceptions of Opinion Support and Political Opinion Expression." *Communication Research* 45(1), 2018.
43. Braghieri, L., Bursztyn, L. & Fasnacht, J. "Threshold Disclosure in Collective Decisions." NBER Working Paper 34827, 2026.
44. Asch, S.E. "Studies of Independence and Conformity: I. A Minority of One Against a Unanimous Majority." *Psychological Monographs: General and Applied* 70(9), 1956.
45. Banerjee, A. "A Simple Model of Herd Behavior." *Quarterly Journal of Economics* 107(3), 1992.
46. Bernstein, D.J. "Appeal v2 - Complaint to IESG regarding censorship of dissent." IETF IESG Appeals, 2025. [https://datatracker.ietf.org/group/iesg/appeals/artifact/226](https://datatracker.ietf.org/group/iesg/appeals/artifact/226)
47. ISO. "Code of Ethics and Conduct." PUB100011, First Edition, March 2023.
48. JTC 1. Standing Document 19, "Meetings," 2022, Section 9 "Recording of meetings."
49. Pakkanen, J. "We need to seriously think about what to do with C++ modules." Nibble Stew, 2025.
50. Ropert, M. "Can we finally use C++ Modules in 2026?" 2026.
51. O'Dwyer, A. "The C++26 NB comments have arrived." 2025.
52. Adelstein Lelbach, B. P2247R1. "2020 Library Evolution Report." 2020.
53. Karotkin, D. & Paroush, J. "Optimum Committee Size: Quality-versus-Quantity Dilemma." *Social Choice and Welfare* 20(3), 2003.
54. [P4099R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4099r2.pdf) - "The Twenty-One Year Networking Arc" (Vinnie Falco, 2026).
55. Schelling, T.C. *The Strategy of Conflict*. Harvard UP, 1960.
56. Crawford, V.P. & Sobel, J. "Strategic Information Transmission." *Econometrica* 50(6), 1982.
57. Lazear, E.P. & Rosen, S. "Rank-Order Tournaments as Optimum Labor Contracts." *Journal of Political Economy* 89(5), 1981.
58. [P2759R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2759r1.pdf) - "DG Opinion on Safety for ISO C++" (Michael Wong, Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, 2023).
59. [P2816R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2816r0.pdf) - "Safety Profiles: Type-and-resource Safe programming in ISO Standard C++" (Bjarne Stroustrup, Gabriel Dos Reis, 2023).
60. [P3081R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3081r0.pdf) - "Core safety Profiles: Specification, adoptability, and impact" (2024).
61. [P3970R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3970r0.pdf) - "Profiles and Safety: a call to action" (Daveed Vandevoorde, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, Michael Wong, 2026).
62. [P4137R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4137r0.pdf) - "PAVE: Profile Analysis and Verification Evidence" (Vinnie Falco, 2026).
63. Gilligan, T.W. & Krehbiel, K. "Collective Decision-Making and Standing Committees: An Informational Rationale for Restrictive Amendment Procedures." *Journal of Law, Economics, and Organization* 3(2), 1987.
64. Fong, C. & McCrain, J. "A Tournament Theory of Congressional Committee Leadership." *Public Choice* 202(1), 2025.
65. Kanevskaia, O. et al. "Wearing Multiple Hats: The Role of Working Group Chairs' Affiliation in Standards Development." *Research Policy* 52(9), 2023.

[66] [WG9 Organization](https://open-std.org/JTC1/SC22/WG9/organize.htm) (WG9).

[67] [MPEG Subgroups](https://blog.chiariglione.org/the-mpeg-special-forces-subgroups/) - "The MPEG Special Forces: Subgroups" (Leonardo Chiariglione, 2020).

[68] [Future of SC 29](https://jtc1info.org/future-of-sc-29-with-jpeg-and-mpeg/) - "Future of SC 29 with JPEG and MPEG" (JTC 1, 2020).

[69] [JTC 1 Strategic Business Plan](https://www.iso.org/files/live/sites/isoorg/files/developing_standards/who_develops_standards/docs/JTC%201%20Strategic%20Business%20Plan%20November%202020.pdf) - "JTC 1 Strategic Business Plan" (JTC 1, 2020).

[70] [The Way Forward in SC 29](https://jtc1info.org/the-way-forward-in-sc-29/) - "The Way Forward in SC 29" (JTC 1). Interview with Gary Sullivan and Toshiyasu Suzuki.

[71] [TC 211 Good Practices](https://committee.iso.org/sites/tc211/home/resolutions/isotc-211-good-practices/--roles-in-committee-work.html) - "Roles in Committee Work" (ISO/TC 211).
