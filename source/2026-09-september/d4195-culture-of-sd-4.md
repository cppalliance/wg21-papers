---
title: "WG21 Game Theory: The Culture That Emerges From SD-4"
document: P4195R0
date: 2026-09-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

WG21's consensus process selects for survivability through the committee's represented veto structure. It cannot certify technical quality or user welfare. The distinction is testable: Post-adoption correction rates for large contested features, compared against a baseline, would reveal whether the system's selection correlates with quality or substitutes for it. That measurement is future work. The consequence is that adoption is evidence that the proposal outlasted organized opposition, not that the design was best.

This report applies game theory to the incentive structures created by [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)<sup>[1]</sup>'s rules: consensus as chair judgment, polls that record numbers without a minutes register of opposing arguments, and repeat-player dynamics across decades of meetings. It finds that procedural fluency, asymmetric institutional memory, and path dependence are first-order determinants of which proposals enter the C++ standard. Five case histories (contracts, std::execution, networking, default comparisons, and coroutines) ground the analysis in public WG21 records. The system works well when funded advocates cross-examine each other and a capable chair reads the room; it fails when review costs are high, opposition is unfunded, and the institutional record preserves only one side of the argument.

## Revision History

### R0: September 2026

- Initial version.

## Executive Summary

The three dynamics identified in the abstract produce a specific cultural pattern. The committee develops a collegial surface over an adversarial undercurrent. Participants remain personally cordial while conducting very long intellectual conflicts, because open confrontation is expensive in a body where you will encounter the same people for decades. Disputes end not when one side is persuaded, but when the minority's willingness to spend social capital is exhausted. The gap between "consensus was achieved" and "we lost the poll" becomes a standing source of institutional tension.

Each participant's behavior is rational given the incentive structure. Authors optimize for adoption. Reviewers specialize in domains they care about and abstain elsewhere, because review is a public good nobody wants to provide privately. Chairs optimize for closure, because the role demands converting conflict into decisions. The minority is asked not "are you right?" but "how strongly are you willing to resist?" This question turns a technical judgment into a social one.

The case histories confirm that these dynamics are equilibrium outcomes. Contracts ([P2900](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf)<sup>[18]</sup>) illustrates the ideal-author playbook executed through plenary adoption. Coroutines illustrates a minority partially vindicated after the fact: C++20 shipped only language-support primitives, with no high-level coroutine types. The std::execution vote ([N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[2]</sup>: 57-20-27, "numerically this is a weak consensus, but it is a consensus") illustrates chair judgment at the boundary. Networking illustrates a direction poll setting the conceptual framework about fifteen months before the chosen path had a concrete proposal. Default comparisons illustrates plenary catching a design flaw that subgroup consensus missed.
revision
For the C++ community, the practical consequence is that features entering the standard reflect the priorities of funded, persistent, procedurally fluent authors. That group overlaps with, but is not identical to, the group best positioned to judge what C++ users need.

## Key Judgments

1. WG21's consensus process equilibrium selects for proposals that outlast organized opposition. This can be the best design or an inferior design, and the record SD-4 requires, typically a tally and an outcome label, does not encode which of the two occurred. Likelihood: almost certain. Confidence: high (structural analysis of SD-4 rules, corroborated by multiple case histories).

2. Procedural fluency and technical expertise correlate over time without being identical. Expertise determines whether a participant has something worth proposing; fluency determines whether the institution can hear it. Doing the work builds fluency (section 9), which is why the system appears to select for quality. The separation produces the failure mode: A brilliant outsider with no fluency and a mediocre insider with deep fluency face radically different odds, and SD-4's gates cannot distinguish the two cases. Likelihood: almost certain. Confidence: high (structural feature of SD-4's rules).

3. SD-4 does not require the minutes register in ISO/IEC Directives clause 2.5.6<sup>[9]</sup>. The record it requires is typically a tally and an outcome label. Papers on both sides preserve arguments; they are not a finding that an objection was reconciled. A later reader cannot tell from the tally whether objections were answered or outvoted, and the gap compounds as people who were in the room leave. Likelihood: almost certain. Confidence: high (structural feature of SD-4).

4. SD-4 makes consensus a chair call, not a finding that the remaining objection has been answered. The chair is incentivized to produce a decision rather than to adjudicate the technical claims, so the live question often becomes how strongly the minority will resist rather than whether a defect remains. Consensus does not require persuasion. People can therefore lose a poll without being convinced, and "consensus was achieved" versus "we lost the poll" stays as institutional tension. Likelihood: very likely. Confidence: medium (chair incentives follow from SD-4; sentiment is not measured).

5. Path dependence governs the framing a challenger is heard in, not the merits it is judged on. Once a proposal accumulates favorable direction polls, a competitor is evaluated as an amendment or an objection to it rather than as an equal design, and must show not only that \( B > A \) but that \( B - A > C_{\text{reversal}} \), where \( C_{\text{reversal}} \) includes discarded wording, abandoned implementations, schedule risk, and reputational cost to previous decisions. Merit still decides outcomes, but accumulated state decides the terms on which merit is presented. Likelihood: likely. Confidence: high (the framing appears in the document titles and poll text of the contracts and networking cases).

6. The incentive to protect an institutional investment scales with its size. A three-page paper has negligible reversal cost; a multi-year, employer-funded feature has reversal cost proportional to years of work, reputation, and coalition capital. The proposals that matter most to users are the ones whose authors are most incentivized to lock in early and resist late correction. This is rational investment protection, not moral failure. Likelihood: likely. Confidence: high (follows from the reversal-cost inequality in section 12 and the payoff functions in section 13; requires only that authors are rational).

7. Review is a public good: It is expensive, its benefits are diffuse, and any one reviewer's chance of changing the outcome is small. The system therefore under-produces critical scrutiny relative to the social optimum. Review cost rises with opacity, length, and entanglement with existing wording, so the proposals that need scrutiny most are the ones most likely to be under-reviewed. Likelihood: very likely. Confidence: medium (the mechanism is textbook; the magnitude in WG21 is estimated, not measured).

8. Direction polls happen earliest, when design maturity is lowest. Reversal cost grows monotonically from each state transition, creating maximum lock-in at minimum information. An early architectural mistake becomes progressively harder to correct, not because it becomes less wrong, but because the institutional state surrounding it becomes more expensive to discard. The penalty for an early mistake is catastrophic for users; the incentive to make it irreversible is maximal for authors. Likelihood: likely. Confidence: high (follows from sections 10 and 12; the timing observation is structural).

## 1. What Reconciliation Looks Like In ISO Versus SD-4

The ISO/IEC Directives, Part 1<sup>[9]</sup>, import consensus from ISO/IEC Guide 2:2004:

> consensus: General agreement, characterized by the absence of sustained opposition to substantial issues by any important part of the concerned interests and by a process that involves seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments.
>
> NOTE Consensus need not imply unanimity.

Clause 0.7(b) states that consensus "requires the resolution of substantial objections." Clause 2.5.6 then says what that looks like in the record. Sustained oppositions are "views expressed at minuted meetings." If leadership does not treat the opposition as sustained, "the leadership will register the opposition (i.e. in the minutes, records, etc.) and continue to lead the work on the document." If it does, "it is required to try and resolve it in good faith." A sustained opposition "is not akin to a right to veto." "The obligation to address the sustained oppositions does not imply an obligation to resolve them successfully." If work continues, "the leadership will register the opposition and continue the work."

[SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)<sup>[1]</sup> reprints the same Guide 2 sentence. Its next move is different. "A proposal normally advances if there are more than twice as many in favor of a proposal as against, after discussion of the concerns of those voting against and possibly a re-poll to see if opinions have improved." Consensus in a design subgroup is "as determined by the subgroup chair." "Anyone voting Against, especially Strongly Against, may be asked for their reasons by the chair. They should be prepared to articulate their rationale, including either what change(s) would address their concern and change their position, or else that they are opposed to pursuing the proposal in any form and no change would change their position." SD-4 does not require the chair to publish the strongest opposing argument, a response to it, or why consensus was declared despite it.

Both texts begin from reconciliation of conflicting arguments. ISO's next sentences put opposition in the minutes and require a good-faith attempt to resolve it. SD-4's next sentences put a ratio, a chair call, and a duty on the person voting Against. Fluency, path dependence, and the cost of review are separate mechanisms. Author papers and opposition papers are advocacy. The usual inference is that because the authors responded, the objections were reconciled.

ISO uses the verb, not the noun. This paper uses "reconciliation" for the record state clause 2.5.6 describes, and tests it in three parts.

**Reconciliation.** A sustained opposition on a substantial issue is reconciled when the record contains the objection stated in terms its holder would recognize, a response addressing its substance, and a finding by the leadership, recorded at the time, that the objection no longer stands or that the work proceeds despite it.

Each part is a property of the record rather than of anyone's state of mind, so a later reader can check all three without having been in the room. Persuasion is not among them. The clause quoted above is explicit that the obligation to address a sustained opposition does not imply an obligation to resolve it successfully. An objection registered, answered, and then overruled in a recorded finding is reconciled. An objection outvoted in silence is not. The three parts are, item for item, the three things the SD-4 sentence above declines to require, and a poll tally supplies none of them. By the same test, a rebuttal paper is not reconciliation.

A companion paper in this mailing, [P4272R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4272r0.pdf)<sup>[58]</sup>, applies this test to one rebuttal paper, P3846R1, concern by concern, and finds that the record contains replies for eighteen objections and reconciliation for two.

## 2. The Ideal Author

A proposal enters the system when someone states an idea precisely enough for others to criticize. The author publishes a numbered paper, secures agenda time, remains present through repeated reviews, revises enough to remove organized sustained opposition, and survives successive scrutiny. On the surface, this is a system designed to refine technical ideas through deliberation.

What it selects for in practice is a specific profile: persistence, institutional funding, procedural fluency, coalition-building, technical opacity, chair confidence, existing momentum, and compatibility with active constituencies. The successful strategy is compact enough to state in a single sentence: Publish, attend, persist, compromise selectively, build legitimacy, and eliminate organized opposition.

The ideal author optimizes for adoption. The ideal reviewer optimizes for the domain the reviewer cares about. The ideal user optimizes for nothing, because the cost of participation exceeds the probability of influence. The institution therefore hears from people who can afford to play, filters their contributions through procedural gates, and delivers the result to users who are structurally excluded from influencing the direction of C++.

"Sustained" requires attendance across meetings. "Important" and "represented" require institutional standing. "Opposition" must be organized. The rules do not explicitly exclude anyone, but they weight the game toward players who can afford to persist.

The contracts saga illustrates the profile. [P0542](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0542r5.html)<sup>[19]</sup> was removed from C++20 at Cologne 2019 ([P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf)<sup>[20]</sup>, adopted in the Cologne minutes, [N4826](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/n4826.pdf)<sup>[8]</sup>). [P2695R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2695r0.pdf)<sup>[22]</sup> records that SG21 was established after that removal. [P2182](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2182r1.html)<sup>[21]</sup> defined the MVP from the uncontroversial part of C++20 contracts. P2695R0 also set the C++26 MVP schedule. [P2961](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2961r2.pdf)<sup>[23]</sup> (Doumler, Maurer) proposed "natural syntax"; SG21 adopted it into the MVP. P2900R6 moved from SG21 to EWG and LEWG on 2024-02-29 with consensus. When SG21, which had developed the MVP, polled on 2024-05-30 whether the ship vehicle should be a TS rather than the IS, consensus was against. EWG forwarded P2900R11 to CWG and LEWG for C++26 at Wroclaw in November 2024. LEWG then forwarded to LWG (SF:23, F:9, N:1, A:0, SA:5). Plenary adopted P2900R14 into the C++26 Working Paper on 2025-02-15, and the feature appears in the working draft published the following month ([N5008](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5008.pdf)<sup>[4]</sup>). At every stage, the authors who persisted, attended, built coalitions, and maintained chair confidence advanced the proposal. The mechanism worked as designed.

The mechanism selects for survivability through the committee's represented veto structure. It cannot tell whether the survivor was excellent.

## 3. What Culture Emerges

The culture that grows from this mechanism is not primarily adversarial. It is managed consensus among repeat players. Open confrontation is expensive because participants encounter the same people at the next meeting, and perhaps for decades. Rational participants learn to distinguish "I prefer B" from "I am willing to prevent A from proceeding." The second statement consumes considerably more social and institutional capital than the first.

WG21 resembles a functional peerage: an elective technical aristocracy with earned, informal peer status. Status accrues to people who can master a technical domain, write credible papers, absorb criticism without becoming impossible to work with, recognize which fights matter, persuade respected participants, understand when consensus exists, avoid surprising the institution, and shepherd work over multiple years.

The natural unit of power is the argument, plus a person willing to advance it through the institution. A technically compelling position without a champion is weak. An imperfect position with several persistent, respected champions can be strong. The system functions well when the peerage's senior members absorb the cost of repair. The default comparisons saga is the contrast case: Plenary overturned a subgroup consensus with unresolved design concerns. It is not an illustration of the ISO/SD-4 gap. Stroustrup's N4475, with wording in Maurer's [P0221R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0221r2.html)<sup>[24]</sup>, proposed generating all six comparison operators by default and passed EWG review. The plenary motion to apply its wording was withdrawn at Oulu 2016 after a 16-31-20 poll: operator< should not be generated by default for types where ordering is meaningless, the proposal was opt-out where EWG had supported opt-in, and no way remained to request the C++14 behavior ([N4597](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4597.pdf)<sup>[25]</sup>). The failed motion forced a complete redesign. Sutter's [P0515](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0515r3.pdf)<sup>[26]</sup> (operator<=>, the spaceship operator) took a fundamentally different approach using three-way comparison and explicit opt-in via `= default`. Plenary caught a design flaw that subgroup consensus had not resolved. It took Herb Sutter to pick up the pieces. The peerage functions well when a senior member absorbs the cost.

## 4. How the Objectors Feel

The minority experiences a specific asymmetry. The majority can point to polls. The authors can point to years of work. The chair can point to consensus. The minority can only point to the reasons for their objection. If those reasons are not preserved in the institutional record, participants who hold them may conclude that the process is converting failure to persuade the room into failure of the argument itself.

The minority may believe, "The technical problem is still there. Nothing about a poll made it disappear." The reactions are predictable and documented: withdrawal ("Fine. Do whatever you want."), escalation ("You still have not answered the objection."), documentation, competing papers, appeals to another subgroup or national body, and institutional suspicion. A vicious feedback loop develops: The minority feels unheard, the minority becomes more forceful, the majority perceives obstruction, the majority discounts the minority, the minority feels even less heard. The person who objects remains respected, while their objection becomes institutionally irrelevant.

SD-4 creates the conditions for this dynamic in three ways: It requires no minutes register of opposing arguments, it treats consensus as chair judgment rather than measured agreement, and it preserves poll numbers without written responses to dissent. When an outsider raises a late objection, the implicit request is to discard accumulated consensus, invalidate previous work, spend scarce meeting time reconsidering it, and trust someone who has not participated in the process that generated those decisions.

The coroutines case made this concrete. The Coroutines TS ([P0057](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0057r8.pdf)<sup>[27]</sup>, Gor Nishanov) was merged into C++20 via [P0912R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0912r5.html)<sup>[28]</sup> despite organized opposition. Google proposed an alternative: "Core Coroutines" ([P1063R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r1.pdf)<sup>[29]</sup>, Romer/Dennett/Carruth). [P1329R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1329r0.pdf)<sup>[30]</sup> (Mihaylov, Vassilev) argued the TS should not be merged, citing interface, terminology, and performance, including heap allocation that relies on optimization. The merge succeeded over these objections. C++20 shipped only language-support primitives in `<coroutine>`, with no high-level coroutine types. `std::generator` did not arrive until C++23 ([P2502](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2502r2.pdf)<sup>[31]</sup>). A standard task type did not arrive until C++26, when `std::execution::task` was adopted via [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[7]</sup>. The heap-allocation-elision concern persists: The language does not guarantee elision. The minority's concerns proved partially correct. Opposition papers exist. They are not the minutes register in section 1. The decision record does not contain that register of why they lost. What humans need most in serious disagreement is evidence that the other side actually understood the argument before rejecting it.

## 5. How the Authors Feel

The people whose design is moving forward tend to experience themselves as having already done the work. They have written papers, attended meetings, answered questions, revised repeatedly, obtained favorable polls, and produced implementations. Over time, they stop perceiving the opposing design as an equal alternative. The language changes: "That is an interesting alternative." Then: "We already discussed that." Then: "We cannot keep reopening settled questions." Then: "At some point we have to make progress." That progression can occur even if the technical objection has never actually been resolved.

Persistent opposition begins to look less like useful technical criticism and more like refusal to accept a legitimate decision. Everyone involved learns, implicitly, that there is a distinction between being technically unconvinced and being willing to spend the social capital necessary to continue opposing consensus. The majority will often still be friendly to the minority personally. But the procedural outcome gradually substitutes for a technical verdict: The position lost the poll, so the position must have been wrong.

The author has invested years of effort, reputation, and institutional capital. Accumulated revision and implementation evidence has legitimate weight; it is not merely psychological momentum. But reopening feels like an attack on accumulated work, not a technical contribution. SD-4 creates this pressure through direction polls that accumulate state, a consensus definition that converts objection into a question of social willingness, and a timeliness norm that penalizes late-arriving alternatives. The system provides no mechanism for distinguishing "we resolved this objection" from "we outvoted this objection."

The P2300 `std::execution` story from the author's seat illustrates the frustration. The broader executors effort spans roughly eight years from [P0443](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html)<sup>[32]</sup> (2016). P2300R0 was published in 2021. It failed for C++23. LEWG polled ([P2459R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2459r0.html)<sup>[33]</sup>) SF:23, WF:14, N:0, WA:6, SA:11. Outcome: "No consensus. There is sustained strong opposition against including such a large proposal into C++23 at such a late stage. Timing is a major factor in the lack of consensus." The chair, a P2300 co-author, recused; vice chairs determined consensus. Weak forwarding to C++26 followed: SF:12, WF:6, N:2, WA:2, SA:3, "Weak consensus in favor" ([P2575R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2575r0.html)<sup>[34]</sup>). The plan paper ([P3109R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3109r0.html)<sup>[35]</sup>) was approved in February 2024 ([P3124R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3124r0.html)<sup>[6]</sup> Poll 5): SF:6, WF:6, N:1, WA:0, SA:0, "Strong consensus in favor." Plenary adopted P2300R10 in June 2024 ([N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[2]</sup> LWG motion 12): 57-20-27. Sutter's plenary characterization is in section 6. Wakely reported that like every telecon for the past few months, most of the meeting was spent reviewing P2300 ([N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[2]</sup>). From the authors' perspective: eight years of work, multiple revisions, repeated reviews, implementation experience (stdexec, libunifex), and 57 in favor, yet the result is still called "weak."

## 6. How the Chair Feels

The chair normally does not want to determine "Alice is technically correct and Bob is technically wrong." That would require the chair to become the supreme technical authority. The chair is incentivized to determine, "Is there enough agreement for the committee to proceed?" The chair will usually try to lower the temperature rather than adjudicate the truth. The chair's objective becomes: Convert conflict into a decision, rather than establish which side's technical claim is correct.

The minority is increasingly being asked not "Are you right?" but "How strongly are you willing to resist?" That question turns a technical judgment into a social one. A person who continues voting Strongly Against must repeatedly assert, "Yes, I believe my judgment is important enough to impede everyone else's work." That is psychologically expensive, especially in a community of colleagues.

"We have given this concern extensive consideration" can be true even when "We have conclusively answered this concern" is false. That distinction is central.

The chair faces a constrained optimization:

- Advance too aggressively: accusations of railroading, risk of NB opposition
- Defer too readily: frustrated authors, slipping schedules, accusations of allowing one or two people to veto progress
- The equilibrium: Advance proposals that have passed expected stages, show substantial support, and lack organized sustained opposition

SD-4 places the chair at the center of the consensus determination. Consensus is chair judgment, not a formula applied to poll numbers. A chair who repeatedly refuses to advance faces costs. A chair who advances over substantial expert opposition risks different costs. A chair may also be motivated by protecting technical quality; the role does not preclude that. But the role structurally incentivizes closure.

The same P2300 plenary from the chair's seat shows the trap. Before the vote, Sutter ([N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[2]</sup>): "We have a standing document about procedures. We want to hear your concerns, but we really appreciate not hearing them for the first time in the plenary. Please raise your concerns early so we can front load them." After the vote: "Numerically this is a weak consensus, but it is a consensus. I'm not hearing any NB concerns at this time, and it's been many months and there would have been time for NBs to raise concerns. Please talk about this and find answers to the questions." One NB requested postponement; two others reported concerns "but did not determine national opposition at that time." An evening session was organized ([wiki](https://wiki.isocpp.org/2024-06_St_Louis:SendersReceivers) St. Louis Senders/Receivers); participants expressed concern about complexity and drew unfavorable comparisons to coroutines. The chair is not positioned to determine who is technically right. The chair is positioned to determine whether the institution can proceed.

## 7. How the Objectors Perceive the Authors

The opposing side may come to believe the advancing coalition is invested in its own work, unwilling to admit architectural mistakes, using procedure instead of argument, benefiting from relationships and accumulated status, and defining "consensus" as whatever permits the proposal to continue. The disagreement gradually becomes moralized. Neither interpretation needs to be entirely true. Both can arise rationally from each side's experience of the same process.

When the author says "We've addressed this concern," the opponent hears "We've made enough changes that the chair will no longer let your objection stop us." The objector has invested analysis and reputation in the competing position. Each accommodation that does not address the architectural concern looks like procedural evasion. The burden of proof has shifted: The objector must now demonstrate the forwarded proposal should be withdrawn. Coalition dynamics favor the advancing group, which has more invested participants. The structural conditions for this perception come from SD-4's forwarding mechanism, its lack of mandatory written responses to dissent, and the accumulated state of favorable polls.

The P2900 contracts case from [P3573](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3573r0.pdf)<sup>[36]</sup>'s perspective illustrates the gap. P3573R0, "Contract concerns" (January 2025), authored by Hava, Garcia Sanchez, Regev, Dos Reis, Spicer, Stroustrup, van Winkel, Vandevoorde, and Voutilainen, stated "grave concerns about the current design (P2900, the so called MVP == Minimal Viable Product) and its direction." [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf)<sup>[37]</sup> (Dos Reis), "P2900 Is Still Not Ready for C++26," is dated 2024-11-19, the same day as the EWG forward. P3573R0 was filed after EWG had already forwarded to wording groups. The objectors had to demonstrate that the already-forwarded proposal should be withdrawn, not that it was unready. NB comments followed: ES-050, US 26-051, US 25-052, FR-004-053. From the objectors' perspective: years of closed-loop SG21 development, late objections called "already addressed," and the burden shifted to challengers. SG21, which had developed the MVP, polled TS versus IS and recorded consensus against. The subgroup's chair has since published his own account of that period: participants "complained throughout the SG21 work that the pace was too fast," he "heard those complaints" and "did not change course," and he kept his technical objections to private conversations with the authors until the paper had left SG21, a choice he now calls "a failure of chairing" ([P4381R0](https://isocpp.org/files/papers/P4381R0.html)<sup>[59]</sup>). That account is the chair's, so it is evidence of how the process felt from the office that ran it, not only from the objectors' seats.

## 8. How the Authors Perceive the Objectors

The advancing side may come to believe the opponents are perfectionists, unwilling to compromise, protecting their own design, repeatedly reopening decisions, preventing C++ from making progress, and demanding an impossible standard of certainty. When the opponent says "The fundamental issue remains," the author hears "No amount of accommodation will ever satisfy you." Both sides may be sincere.

Section 5 named the distinction that both sides learn: Being technically unconvinced is not the same as being willing to spend the social capital needed to keep opposing consensus. The social norm becomes, "We can disagree strongly, but eventually somebody has to accept that the group has moved on."

For the winning coalition, that feels like mature governance. For a technically serious minority whose objections were never reconciled, it can feel like politely administered dismissal.

The author has responded to feedback, revised, and obtained favorable polls. Each continued objection looks like refusal to accept legitimate institutional decisions. The author's coalition has invested more person-hours than the objectors. Progress on C++26 depends on closure. SD-4 provides no mechanism for determining whether a repeated objection reflects an unresolved technical flaw or a participant's refusal to accept the group's direction. The distinction matters enormously, and the institution cannot make it.

The same P2900 case from [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf)<sup>[11]</sup>'s perspective closes the circle. P3846R0/R1, "C++26 Contract Assertions, Reasserted" (Doumler, Berne, et al.), responds to NB comments by characterizing one concern as repeating "earlier objections ([P3173R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3173r0.pdf)<sup>[38]</sup>, [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf)<sup>[37]</sup>, [P3573R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3573r0.pdf)<sup>[36]</sup>) already considered repeatedly in EWG. No new information has been presented since." EWG polled at Hagenberg on 2025-02-11: "Remove P2900 from CWG's consideration for C++26, find a different ship vehicle" (consensus against). [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf)<sup>[3]</sup> (Hagenberg minutes): "Consensus on contracts has increased since the last meeting." From the authors' perspective: wording complete, NB comments addressed, and the same people still objecting with the same arguments. These are irreconcilable readings of the same process. P3846 is a rebuttal paper in the sense of section 1; the system provides no mechanism for determining which reading is correct. Appendix A records the complete sequence. Between January 2025 and July 2026, the P2900 author group published eight papers the record reads as rebuttals (Appendix A shows the record miscounts P2899R0 among them); each appeared after the favorable poll whose outcome it defended, timed for the meeting at which that outcome would next be challenged.

## 9. Procedural Fluency as Political Capital

Procedural fluency is the ability to convert technical merit into institutional action. This is analytically separable from expertise, though the feedback loop below produces correlation over repeated cycles. A brilliant implementer with no procedural knowledge and a mediocre programmer with deep procedural fluency face radically different odds.

Fluency serves five functions. First, it reduces transaction costs: The expert loses less energy to procedure. A newcomer may spend months on excellent work that cannot advance because it was submitted to the wrong group, lacks required motivation, or arrives after scheduling decisions. Second, it expands the available move set: Formally everyone has similar rights; practically only fluent participants know all available moves. Third, it controls framing. Poll construction determines which question is being decided: "Do we like this direction?" versus "Forward this paper for C++29?" This is the same proposal, but with different institutional consequences.<!-- dcp: NB. Does this convey the intended meaning?-->

Fourth, fluency produces legitimacy: Fluent authors signal they are safe institutional counterparties. Chairs rationally prefer such authors because advancing their papers presents less risk. Fifth, it converts attendance into cumulative power: Procedural knowledge is partly tacit. Repeated participation teaches which objections are considered serious, which prior decisions may be reopened, and how much revision is enough.

The feedback loop is direct: Fluency yields chair confidence, which yields agenda access, which yields successful papers, which yield reputation, which yields greater fluency and access. The cycle compounds over meetings.

Procedural fluency is not neutral. It redistributes influence toward repeat attendees, participants whose attendance is paid for, chairs, prolific authors, and people with established relationships. The source of the funding is not the discriminator: an employer, one's own business, consulting or training income, a national body, or independent means all purchase the same attendance. What matters is whether the cost can be absorbed year after year. Fluency disadvantages those who cannot absorb it, implementers who cannot attend regularly, users encountering the process for the first time, and critics who appear only when a proposal becomes publicly visible. The crucial inequality is not that insiders are allowed to vote and outsiders are forbidden. It is that insiders know when a consequential decision is actually being made, what language will influence it, and what must have happened beforehand for their intervention to count.

## 10. Polls as State Transitions

A poll looks like information: 17/8/4/3/2. Its principal function is frequently state mutation. Before the poll: "This design question is open." After the poll: "The committee has direction." At the next meeting, the conversation begins from the new state. The distinction matters because information can be re-evaluated but state changes are costly to reverse.

An author has strong incentive to obtain favorable state transitions as early as possible. A competitor arriving at state \( S_3 \) is no longer competing against the original paper. The competitor is competing against the paper plus three previous committee decisions. Early polls have option value far beyond the particular question being asked.

Three possible polls for the same proposal illustrate the mechanism: "Do we like this general direction?" or "Should the author continue working?" or "Forward this paper for inclusion in C++29." A proposal may receive strong support on the first two and fail the third. An "encourage further work" poll can generate momentum, legitimacy, and an expectation of eventual adoption. This is agenda power disguised as grammatical precision.

The networking and executors case shows the sequence. In October 2021, LEWG and SG1 took five electronic polls of 56 participants (questions: [P2452R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2452r0.html)<sup>[39]</sup>; outcomes: [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[40]</sup>). Poll 1: "The Networking TS/Asio async model [P2444R0] is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs." SF:5, WF:10, N:6, WA:14, SA:18 (weak consensus against). Poll 2: "The sender/receiver model [P2300R2] is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs." SF:24, WF:16, N:3, WA:6, SA:3 (consensus in favor). Poll 4: "Networking in the C++ Standard Library should be based on the sender/receiver model [P2300R2]." SF:17, WF:11, N:10, WA:4, SA:6 (weak consensus in favor).

A Poll 4 Strongly Against comment observed that no concrete sender/receiver networking API had been proposed. [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[41]</sup> (Allsop, Falco, Hodges, Kohlhoff, Morgenstern) argued that the Networking TS was already deployed: Asio had 18+ years of deployment experience; the TS itself was about six years old. [P2762R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r0.pdf)<sup>[42]</sup> (K&uuml;hl, January 2023), the first concrete sender/receiver networking proposal, arrived about fifteen months after the direction poll. The direction poll set the conceptual framework before the chosen path had a concrete proposal.

## 11. The Asymmetry of Institutional Memory

The proposal itself is typically a substantial document: the author's motivation, requirements, examples, alternatives considered, responses to feedback, and wording. The proponent leaves a durable intellectual artifact. Suppose a highly qualified opponent gives a twenty-minute oral argument explaining why the architecture is wrong. The poll reads 18/9/5/3/4 and the record of the decision says, "Consensus in favor." Twenty years later, the author's 40-page P-paper remains. The oral dissent is a tally.

Future participants encounter the historical record as though the winning side possessed an argument and the losing side possessed votes. That is epistemically very different from what actually happened.

No malign intent is required. From the author's perspective, a written chair's reconciliation creates future liabilities. Without that record, the historical fact is merely "the committee achieved consensus." The latter is much harder to reopen. Writing another paper is how SD-4 preserves dissent. It is not the minutes register in section 1. Opposition also requires authorship, time, procedural fluency, and persistence. The equilibrium gives the winning coalition little incentive to create an excellent permanent statement of the losing coalition's case.

The author need not win the argument in the historical record. The author need only survive it in the room.

The P2300 record in section 5 shows the asymmetry. N4985 records teachability as an NB concern. The evening session records complexity, unfavorable comparisons to coroutines, and missing complementary library features. These reasons live in oral discussion and in scattered paper comments. The permanent record is P2300R10 and LWG motion 12: 57 in favor, 20 opposed, 27 abstain, consensus ([N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[2]</sup>). Twenty years from now, the paper survives. The opposition is "Opposed: 20" in the minutes.

## 12. Path Dependence and the Burden-of-Proof Flip

Assume two mutually exclusive designs, A and B, both technically credible. The actual game is sequential, not simultaneous. A acquires institutional state: three meetings of discussion, favorable direction polls, implementation work, an R7 paper, wording review, endorsements. At that point, B appears with an excellent design. The comparison becomes, "continue A" versus "reverse the accumulated decisions and adopt B." The burden shifts. B must demonstrate not merely that \( B > A \), but that \( B - A > C_{\text{reversal}} \), where \( C_{\text{reversal}} \) includes discarded wording, abandoned implementations, schedule risk, and reputational cost to previous decisions.

A four-stage linguistic transformation tracks the shift: "A and B are competing designs." Then "A is the committee direction; B is an alternative." Then "A is the proposal; B is an objection to the proposal." Then "A is the status quo; B wants to reopen the question." The technical content may not have changed at all. The institutional position has.

The game becomes a war of attrition: Who is willing to pay the cost for longer? Persistence changes the probability of winning independently of technical quality. Showing up again is itself a move. A skilled author will typically withdraw, revise, negotiate, or postpone rather than demand "A or B. Vote now." The losing design may not receive a dramatic rejection. It may experience less agenda time, then no forwarding poll, then another revision requested, then the champion loses interest, then nothing. B simply stopped moving.

The contracts case shows the transformation in the documents themselves. [P2680R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2680r1.pdf)<sup>[43]</sup> (Dos Reis) proposed that contract predicates be free of side effects and free of undefined behavior, a different design basis from the MVP that became [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf)<sup>[18]</sup>. It arrived into a study group whose work item was already defined as the MVP, and the record names it accordingly. Eight SG21 participants, three of them P2900 authors, answered it with [P2700R1](https://open-std.org/JTC1/SC22/WG21/docs/papers/2022/p2700r1.pdf)<sup>[44]</sup>, "Questions on P2680." [P3362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3362r0.html)<sup>[45]</sup> (Voutilainen, Corden) argues for Dos Reis's direction and is titled "Static analysis and 'safety' of Contracts, P2900 vs. P2680/P3285", the incumbent named first by the paper advocating against it.

The poll text completes the sequence. When EWG polled the direction at Wroclaw on 2024-11-19, the question was not which design was better. It asked whether "the contracts proposal in P2900's Minimal Viable Product shall be changed to incorporate stricter contracts in addition to regular contracts": SF:10, F:6, N:3, A:14, SA:16, consensus against. A second poll the same day, on whether to make strict contracts the default or a forced opt-in, returned 6-7-9-20-7, also against ([P3499R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3499r1.pdf)<sup>[46]</sup>). Two years after publication, the competing design was votable only as an amendment to the design it competed with. Whether stricter predicates were the better basis was never the question on the floor.

## 13. The Incentive Structure

SD-4 specifies a game form: players, stages, permissible actions, and decision procedures. It does not specify numerical utilities. There is no unique Nash equilibrium until payoffs are assumed. The object is a subgame-perfect equilibrium of a repeated sequential process. The matrices below are ordinal illustrations, not measurements.

### What Each Player Wants

The structure of WG21 is a multi-player game with asymmetric payoffs. Each participant's behavior follows from a simple ledger: benefits on the left, costs on the right.

The author's payoff function:

\[
U_A = pV + R + E - C_p - C_r - C_a - D
\]

where:
- \( pV \): probability of adoption times value of adoption
- \( R \): reputation and influence
- \( E \): benefit accruing to an employer, an organization, or the author's own business or practice
- \( C_p \): paper and implementation cost
- \( C_r \): revision cost
- \( C_a \): attendance and coalition cost
- \( D \): delay cost

The author enters when the expected payoff exceeds zero. \( C_a \), the attendance cost, gates entry. Only those who can absorb \( C_a \) can afford to play, because it includes travel, lodging, and the opportunity cost of weeks per year, recurring every year. An employer, one's own business, consulting or training income, a national body, or independent means all clear that threshold; the absence of any of them does not.

The reviewer's payoff function:

\[
U_R = Q + I + K - C_s - C_c
\]

where:
- \( Q \): improvement in C++
- \( I \): protection of the reviewer's technical interests
- \( K \): future reciprocal influence
- \( C_s \): study and review cost
- \( C_c \): social and political conflict cost

Reviewers specialize. They invest heavily in domains they care about (\( I \) is high) and abstain elsewhere (\( C_s \) exceeds \( I + K \)).

The user's payoff function reveals why the broader population is absent:

\[
U_{\text{user}} \approx \Pr(\text{my review changes result}) \times \Delta Q - C
\]

The probability term is usually very small, while \( C \) may involve weeks of study and travel. Rational nonparticipation follows even where the collective value of review is enormous. Review is a public good that nobody wants to provide privately.

### Why Fluency Beats Merit

The previous subsection treated each player's costs and benefits as fixed. They are not. Procedural fluency \( F \) is a multiplier on everything.

The fluency-adjusted payoff:

\[
U_i = p_i(F) \times V_i - C_i(F)
\]

where \( F \) is procedural fluency. The key partial derivatives:

\[
\frac{\partial p_i}{\partial F} > 0 \quad \text{(fluency increases probability of success)}
\]

\[
\frac{\partial C_i}{\partial F} < 0 \quad \text{(fluency decreases cost)}
\]

Fluency simultaneously increases the probability of adoption and decreases the cost of pursuing it. This double advantage is the mechanism through which the informal peerage forms. The fluent participant does not necessarily produce better designs; the fluent participant loses less energy to procedure and gets more attempts.

The feedback loop is a causal chain:

\[
\text{fluency} \rightarrow \text{chair confidence} \rightarrow \text{agenda access} \rightarrow \text{successful papers} \rightarrow \text{reputation} \rightarrow \text{greater fluency}
\]

Each successful paper earned through fluency increases fluency further. The system compounds advantage for repeat players. A newcomer with a superior design faces both a lower probability of success and a higher cost of pursuit: The inequality runs on both sides of the ledger.

### What Happens in the Room

Individual optimization produces collective dynamics. Three matrices capture the strategic interactions that shape outcomes.

**Matrix A: Author versus Reviewer.** The author chooses Revise or Push unchanged. The reviewer chooses Scrutinize or Abstain. Let \( c \) = cost of serious review.

|  | Reviewer scrutinizes | Reviewer abstains |
|---|---:|---:|
| Author revises | 3, 3-c | 4, 1 |
| Author pushes unchanged | 1, 2-c | 5, -2 |

When \( c < 2 \), the equilibrium is Revise, Scrutinize: The system works as intended. When \( c > 4 \), the equilibrium is Push, Abstain: Proposals advance without adequate review. At intermediate costs, mixed strategies produce unpredictable quality. A proposal need not defeat every possible objection. It must outlast the objections whose holders are willing to pay the cost of sustaining them. The review cost \( c \) is not a constant. It increases with the proposal's technical opacity, length, and interaction with existing standard wording. The system therefore under-produces scrutiny on the proposals that need it most.

**Matrix B: Repeat-player accommodation.** Two durable proposal coalitions, each can Accommodate or Block.

|  | B accommodates | B blocks |
|---|---:|---:|
| A accommodates | 3, 3 | 0, 4 |
| A blocks | 4, 0 | 1, 1 |

One-shot: Block, Block is the Nash equilibrium. Indefinitely repeated with grim-trigger: Cooperation is rational when \( \delta \geq \frac{1}{3} \) (illustrative; multi-year participation easily clears this threshold regardless of exact payoffs). Long-term participants who expect to return for years of meetings easily value the future that highly. This can produce healthy cooperation. It can also produce logrolling, in which the aggregate standard acquires features that would not survive an independent, population-wide cost-benefit test.

**Matrix C: Chair and organized opposition.** The chair chooses Advance or Defer. The room chooses Acquiesce or Organize.

|  | Room acquiesces | Room organizes |
|---|---:|---:|
| Chair advances | 4, 3 | 0, 2 |
| Chair defers | 1, 0 | 2, 3 |

Two pure equilibria: Advance/Acquiesce and Defer/Organize. This is a coordination game. Early signals determine which equilibrium is selected. That explains the procedural emphasis on surfacing objections before plenary. The chair's move selects the equilibrium. Once a proposal reaches plenary with years of work, subgroup approval, and wording, the focal equilibrium has usually become Advance/Acquiesce. A late opponent is attempting to move the entire room to the alternative equilibrium, a coordination problem that grows harder the more institutional state has accumulated.

### The Optimization Target

The full optimization target:

\[
\Pr(\text{chair declares consensus}) \rightarrow \max
\]

Under SD-4, author and chair tactics in the room follow from this objective. Fluency, path dependence, and the missing minutes register are separate mechanisms. The author who revises tactically, the reviewer who specializes, the chair who advances, and the repeat player who accommodates are each maximizing the probability that the chair declares consensus for their preferred outcome.

"Answering the objection" and "rendering the objection non-dispositive" are substitutes in the author's optimization. The author's response options, ranked by cost and poll effect:

| Author response | Cost | Poll effect |
|---|---:|---|
| Redesign architecture | Very high | Expert becomes SF |
| Thoroughly investigate objection | High | Unknown |
| Add narrow accommodation | Moderate | Expert becomes WA |
| Persuade room objection is non-blocking | Low-moderate | Expert remains SA |
| Clarify scope/document caveat | Low | Expert becomes N |
| Do nothing | Zero | Expert remains SA |

If the proposal already has 24 Favor and 2 Against, the institution gives the author surprisingly little marginal payoff for discovering whether those two people are correct.

Polls function as state transitions:

\[
S_0 \xrightarrow{\text{poll}} S_1 \xrightarrow{\text{poll}} S_2 \xrightarrow{\text{poll}} S_3
\]

The reversal cost inequality:

\[
B - A > C_{\text{reversal}}
\]

where \( C_{\text{reversal}} \) includes lost committee time, discarded wording, abandoned implementations, reputational cost to previous decisions, schedule risk, reopening settled debates, and antagonizing A's coalition.

Architectural objections decompose under institutional pressure:

\[
\text{reject architecture} \rightarrow \sum_i \text{fix issue}_i
\]

"The conceptual model is wrong" becomes "concerns about customization," then "concerns about diagnostics," then "a question regarding cancellation." Once that transformation occurs, the premise that the architecture should exist has quietly ceased to be under discussion.

The advocacy equilibrium, when it works:

\[
\text{many motivated advocates} + \text{expert cross-examination} + \text{chair judgment} \approx \text{best design}
\]

The subgame-perfect equilibrium strategy profile:

- Authors: Enter only when private value exceeds cost; once entered, persist, attend, revise tactically, construct a coalition
- Reviewers: Specialize; review aggressively where personal interest is high; abstain elsewhere; reserve strong opposition for issues sufficiently important to justify its cost
- Chairs: Advance proposals that have passed expected stages, show substantial support, lack organized sustained opposition, and present manageable NB risk
- Repeat players: Maintain relationships, trade concessions, avoid gratuitous opposition
- National bodies: Intervene selectively where salient enough to justify coordination

The variable they are unconsciously optimizing is \( \Pr(\text{consensus}) \): survivability through the represented veto structure. That distinction is the whole game.

## 14. Conclusion and Further Research

SD-4 is a design. Like all rulesets it creates incentives. The culture described above is what rational actors produce under this one. This paper has identified three mechanisms: procedural fluency gating access, path dependence resisting correction, and the missing minutes register preventing the institutional record from distinguishing answered objections from outvoted ones. They are not independent pathologies. They form a single optimization surface whose equilibrium this paper has characterized.

The stakes of that optimization are not uniform. A small paper creates small incentives. A large, employer-funded, multi-year feature creates incentives proportional to the investment: years of work, reputation, coalition capital, and employer resources. The rational response is proportional effort to secure the outcome. A competent institutional operator will seek to control scheduling, chair confidence, direction polls, and the study group's committed time before the investment is made, not after. This is not corruption. It is the expected behavior of rational actors facing the reversal-cost inequality.

Direction polls happen when designs are least mature. The author's rational strategy is to accumulate favorable state transitions as early as possible, because reversal cost grows monotonically from each transition. But early is when the design is least tested, least reviewed, and most likely to contain the architectural mistakes whose correction will later be prohibitively expensive. The system creates maximum lock-in at minimum information. The penalty for an early mistake in a large feature is enormous, and the incentive to make early lock-in irreversible is equally enormous, at the worst possible time.

### Minimum Viable Lock-In Is The Most Rational Proposal

The timing trap and scaling insight together predict a specific equilibrium strategy for large features. The rational author does not deploy the full architecture at once. That exposes too much attack surface and triggers organized opposition. Instead, the rational author decomposes the architecture and identifies the smallest installable piece that forecloses competing designs.

The predicted characteristics of the minimum viable lock-in:

- It is framed as conservative. "Doesn't change existing semantics." "Just installs the foundation." "Minimal."
- It passes beneath the review threshold. The apparent stakes are low, so the cost of discovering what it forecloses exceeds what most reviewers will spend. Matrix A at high \( c \): Push unchanged, Abstain is the equilibrium.
- It occupies the design space. Once adopted, competing architectures face the reversal-cost inequality, competing not against the minimal paper but against the paper plus accumulated consensus plus the extension roadmap.
- It is defended through accumulated state. The authors invoke prior consensus on the foundation and resist reopening, because the institutional investment is now protected by every previous poll.
- The committee becomes an obstacle course to navigate rather than a collaborative partner, because the optimization target is \( \Pr(\text{consensus}) \), not \( \Pr(\text{the room evaluated what the foundation forecloses}) \).

This is a predicted equilibrium strategy. It requires no bad actors. It requires only rational authors facing the incentive structure SD-4 creates for large, employer-funded features. The three mechanisms compound: early lock-in (section 10), under-review due to conservative framing (section 13, Matrix A), and protection via reversal cost (section 12). The strategy is rational. Its consequence for the standard is that design-space foreclosure can happen before the room has evaluated the full architecture that depends on it.

### Limitations of This Analysis

This paper shares a limitation with the system it describes. It cannot distinguish, from the outside, between a proposal that survived because it was excellent and a proposal that survived because its authors were persistent, funded, and procedurally fluent. The system cannot make that distinction either. Both observations may be true of the same proposal simultaneously. A design can be sound, its authors can be competent, and the process can be followed correctly at every stage, yet the institutional record still cannot certify that the outcome reflects quality rather than survivability.

However, the distinction is not unfalsifiable. If the system selects for quality, large contested features should show post-adoption defect rates comparable to or lower than smaller, less contested features, because they received more scrutiny. If the system selects for survivability independent of quality, large contested features should show higher post-adoption correction rates, because path dependence resisted correction during development and review was under-produced relative to the stakes.

The metric: For each large feature adopted since C++11, count the defect reports, correction papers, post-adoption revisions, and removals, normalized by feature scope. Compare contested features against uncontested features of similar size. That measurement is future work. The data exists.

A different design would produce a different culture. This one produces what rational actors optimizing under these rules would produce. When funded advocates cross-examine each other and a capable chair reads the room, the system delivers. Its failure mode is not that bad proposals succeed. Its failure mode is that large proposals with concentrated sponsors and diffuse costs face structural incentives to make their own reversal impossible, and the system provides no mechanism proportional to the stakes for ensuring that early lock-in reflects early correctness.<!-- dcp: NB. Does this rewording successfully convey the intended meaning?-->

This paper asks for nothing.

## 15. Disclosure

The author provides information and serves at the pleasure of the committee.

The author co-authored [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[41]</sup> and participated in the discussions it addresses. That paper is cited in section 10, and the networking case is also one of the two cases behind key judgment 5. In 2021 that paper's position was right; it is no longer a design recommendation. Both treatments are process cases, not a brief for any async model.

The author does not believe Contracts in its current form is the right mechanism for run-time safety in C++, and has papers to that effect. The author also has papers covering Profiles. P2900 was chosen as a primary case because it is the most heavily documented recent controversy with public records on both sides. Sections 7 and 8 present both perspectives without adjudicating the Contracts design.

Machine-assisted drafting was used in the preparation of this paper. The incentive model was elicited by asking a language model to derive the game induced by SD-4. The case histories, poll numbers, and characterizations of the record are the author's and were checked against the cited documents.

\newpage

## References

[1] [SD-4](https://web.archive.org/web/20260125120311/https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Herb Sutter, 2024). Revision of 2024-12-30, the text in force throughout the period this paper analyses; the current revision is dated 2026-05-11 and names Guy Davidson as reply-to.

[2] [N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf) - "WG21 2024-06 St Louis Minutes of Meeting" (Nina Ranns, 2024).

[3] [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf) - "WG21 2025-02 Hagenberg Minutes of Meeting" (Nina Ranns, 2025).

[4] [N5008](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5008.pdf) - "Working Draft, Programming Languages - C++" (Thomas Koeppe, 2025).

[5] [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf) - "WG21 2025-11 Kona Minutes of Meeting" (Nina Ranns, 2025).

[6] [P3124R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3124r0.html) - "2024-02 Library Evolution Poll Outcomes" (Inbal Levi, Fabio Fracassi, Ben Craig, Billy Baker, Nevin Liber, Corentin Jabot, 2024).

[7] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[8] [N4826](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/n4826.pdf) - Cologne 2019 minutes.

[9] [ISO/IEC Directives, Part 1](https://www.iso.org/sites/directives/current/consolidated/index.html) - Consolidated ISO Supplement (2024), clauses 0.7 b) and 2.5.6.

[10] [P3591R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3591r0.pdf) - "Contextualizing Contracts Concerns" (Joshua Berne, Timur Doumler, 2025).

[11] [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, et al., 2025).

[12] [P3912R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3912r0.pdf) - "Design considerations for always-enforced contract assertions" (Timur Doumler, Joshua Berne, et al., 2025).

[13] [P3946R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3946r0.html) - "Designing enforced assertions" (Andrzej Krzemie&nacute;ski, 2025).

[14] [EWG Hagenberg wiki page](https://wiki.isocpp.org/index.php?title=2025-02_Hagenberg:EvolutionWorkingGroup) - "2025-02 Hagenberg: Evolution Working Group," revision 19059. The Contracts (C++26) block lists P3573, P3506, P3591, and P3500 under "Papers considered"; the P3591 entry links its tracker issue as `issues/xxx`.

[15] [cplusplus/papers issue 2250](https://github.com/cplusplus/papers/issues/2250) - P3591R0 tracker issue, created 2025-03-19; comment by the paper's co-author, 2025-03-28.

[16] [P2899R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r0.pdf) - "Contracts for C++ - Rationale" (Joshua Berne, Timur Doumler, Rostislav Khlebnikov, Andrzej Krzemie&nacute;ski, 2025).

[17] [EWG Kona contracts removal notes](https://wiki.isocpp.org/index.php?title=2025-11_Kona:EWGContractsRemovalAndNonRemoval) - "2025-11 Kona: EWG Contracts Removal and Non-Removal," revision 356. Records the seven removal polls, the Netherlands poll, and the session notes in which P3846R0 is listed after NL 6.11 without a presentation marker.

[18] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025).

[19] [P0542R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0542r5.html) - "Support for contract based programming in C++" (G. Dos Reis, J. Daniel Garcia, J. Lakos, A. Meredith, N. Myers, B. Stroustrup, 2018).

[20] [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf) - "Remove Contracts from C++20" (Nicolai Josuttis, Ville Voutilainen, Roger Orr, Daveed Vandevoorde, John Spicer, Christopher Di Bella, 2019).

[21] [P2182R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2182r1.html) - "Contract Support: Defining the Minimum Viable Feature Set" (Andrzej Krzemie&nacute;ski, Joshua Berne, Ryan McDougall, 2020).

[22] [P2695R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2695r0.pdf) - "A proposed plan for Contracts in C++" (Timur Doumler, John Spicer, 2022).

[23] [P2961R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2961r2.pdf) - "A natural syntax for Contracts" (Timur Doumler, Jens Maurer, 2023).

[24] [P0221R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0221r2.html) - "Proposed wording for default comparisons, revision 4" (Jens Maurer, 2016).

[25] [N4597](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/n4597.pdf) - "WG21 2016-06 Oulu Minutes" (Jonathan Wakely, 2016).

[26] [P0515R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0515r3.pdf) - "Consistent comparison" (Herb Sutter, Jens Maurer, Walter E. Brown, 2017).

[27] [P0057R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0057r8.pdf) - "Working Draft, C++ Extensions for Coroutines" (Gor Nishanov, 2018).

[28] [P0912R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0912r5.html) - "Merge Coroutines TS into C++20 working draft" (Gor Nishanov, 2019).

[29] [P1063R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1063r1.pdf) - "Core Coroutines" (Geoff Romer, James Dennett, Chandler Carruth, 2018).

[30] [P1329R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1329r0.pdf) - "On the Coroutines TS" (Mihail Mihaylov, Vassil Vassilev, 2018).

[31] [P2502R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2502r2.pdf) - "std::generator: Synchronous Coroutine Generator for Ranges" (Casey Carter, 2022).

[32] [P0443R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p0443r14.html) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, Gordon Brown, Daisy Hollman, Lee Howes, Kirk Shoop, Lewis Baker, Eric Niebler, 2020).

[33] [P2459R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2459r0.html) - "2022 January Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[34] [P2575R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2575r0.html) - "2022-05 Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, Inbal Levi, 2022).

[35] [P3109R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3109r0.html) - "A plan for std::execution for C++26" (Lewis Baker, Eric Niebler, Kirk Shoop, Lucian Radu Teodorescu, 2024).

[36] [P3573R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3573r0.pdf) - "Contract concerns" (Michael Hava, J. Daniel Garcia Sanchez, Ran Regev, Gabriel Dos Reis, John Spicer, Bjarne Stroustrup, J.C. van Winkel, David Vandevoorde, Ville Voutilainen, 2025).

[37] [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf) - "P2900 Is Still Not Ready for C++26" (Gabriel Dos Reis, 2025).

[38] [P3173R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3173r0.pdf) - "P2900R6 May Be Minimal, but It Is Not Viable" (Gabriel Dos Reis, 2024).

[39] [P2452R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2452r0.html) - "2021 October Library Evolution and Concurrency Polls on Networking and Executors" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[40] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution and Concurrency Networking and Executors Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[41] [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not." (Jamie Allsop, Vinnie Falco, Richard Hodges, Christopher Kohlhoff, Klemens Morgenstern, 2021).

[42] [P2762R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r0.pdf) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023).

[43] [P2680R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2680r1.pdf) - "Contracts for C++: Prioritizing Safety" (Gabriel Dos Reis, 2022).

[44] [P2700R1](https://open-std.org/JTC1/SC22/WG21/docs/papers/2022/p2700r1.pdf) - "Questions on P2680 'Contracts for C++: Prioritizing Safety'" (Timur Doumler, Andrzej Krzemie&nacute;ski, John Lakos, Joshua Berne, Brian Bi, Peter Brett, Oliver Rosten, Herb Sutter, 2022).

[45] [P3362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3362r0.html) - "Static analysis and 'safety' of Contracts, P2900 vs. P2680/P3285" (Ville Voutilainen, Richard Corden, 2024).

[46] [P3499R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3499r1.pdf) - "Exploring strict contract predicates" (Timur Doumler, Lisa Lippincott, Joshua Berne, 2025).

[47] [P3829R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3829r0.pdf) - "Contracts do not belong in the language" (David Chisnall, John Spicer, Ville Voutilainen, Gabriel Dos Reis, J. Daniel Garcia Sanchez, 2025). The paper's own header misnumbers it "P3929R0"; P3829R0 is the number under which it was published.

[48] [P3835R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3835r0.html) - "Contracts make C++ less safe - full stop" (John Spicer, Ville Voutilainen, J. Daniel Garcia Sanchez, 2025).

[49] [P3849R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3849r0.pdf) - "SIS/TK611 considerations on Contract Assertions" (Harald Achitz, 2025).

[50] [P3851R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3851r0.pdf) - "Position on contracts assertion for C++26" (J. Daniel Garcia, et al., 2025).

[51] [P4005R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4005r0.html) - "A proposal for guaranteed-(quick-)enforced contracts" (Ville Voutilainen, 2026).

[52] [P4009R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4009r0.html) - "A proposal for solving all of the contracts concerns" (Ville Voutilainen, 2026).

[53] [P2900R7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2900r7.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2024).

[54] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Timur Doumler, Joshua Berne, Andrzej Krzemie&nacute;ski, Rostislav Khlebnikov, 2025).

[55] [P3911R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3911r2.html) - "RO 2-056 6.11.2 [basic.contract.eval] Make Contracts Reliably Non-Ignorable" (Darius Nea&tcedil;u, Andrei Alexandrescu, Lucian Radu Teodorescu, Radu Nichita, Herb Sutter, 2026). The tally appears on the EWG wiki page 2025-11_Kona:EWGContractsPreNot, whose result field is blank; the "consensus for change" label is from section 1.2 of the proponents' own paper.

[56] [cplusplus/papers issue 2641](https://github.com/cplusplus/papers/issues/2641#issuecomment-4018920377) - EWG telecon poll record for P4005, posted by the EWG vice-chair, 2026-03-08. The comment labels the paper D4005R1; the telecon minutes of 2026-02-05 ([EWG Telecon 2026 February 5th](https://wiki.isocpp.org/index.php?title=EWG_Telecon_2026_February_5th), revision 19120) label it D4005R0, and no R1 exists in the paper store.

[57] [cplusplus/papers issue 2645](https://github.com/cplusplus/papers/issues/2645#issuecomment-4018919102) - EWG telecon poll record for P4009, posted by the EWG vice-chair, 2026-03-08. The comment labels the paper D4009R1; the telecon minutes of 2026-02-12 ([EWG Telecon 2026 February 12th](https://wiki.isocpp.org/index.php?title=EWG_Telecon_2026_February_12th), revision 19175) label it D4009R0, and no R1 exists in the paper store.

[58] [P4272R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4272r0.pdf) - "Addressed but Unresolved: P3846R1's Eighteen Responses on C++26 Contract Assertions" (Vinnie Falco, 2026). Companion paper in the same mailing.

[59] [P4381R0](https://isocpp.org/files/papers/P4381R0.html) - "Chairing SG21 and then objecting to Contracts" (John Spicer, 2026). The SG21 chair's account of the pace of the C++26 Contracts work and of his own chairing.

[60] [P2900R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2900r4.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2024). Dated 2024-01-16; its Introduction and bibliography cite the rationale paper as [D2899R0].

[61] [EWG Croydon RO 2-056 notes](https://wiki.isocpp.org/index.php?title=2026-03_Croydon:EvolutionWorkingGroup:RO2-056) - "2026-03 Croydon: EWG RO 2-056, P3912R0, P3919R0, P4044R0," revision 19882, 2026-03-23. Records the P4044R0 forward poll and the co-author's statement on P3912's purpose. The Croydon EWG schedule ([2026-03 Croydon: Evolution Working Group](https://wiki.isocpp.org/index.php?title=2026-03_Croydon:EvolutionWorkingGroup), revision 20783) lists P3912R0 and P3946R0 in the same "Enforced contracts" session.

[62] [EWG Telecon 2026 January 15th](https://wiki.isocpp.org/index.php?title=EWG_Telecon_2026_January_15th) - telecon minutes, revision 19119, section "P3911R2 'Make Contracts Reliably Non-Ignorable'"; the same five polls are recorded on [cplusplus/papers issue 2536](https://github.com/cplusplus/papers/issues/2536) by the EWG vice-chair, 2026-01-15. The tracker issue was created by the EWG chair on 2025-11-04 during the Kona session.

\newpage

## Appendix A. P2900 Rebuttal Paper Timeline

| Date | Event | Type |
|------|-------|------|
| 2024-11-19 | EWG forwards P2900R11 to CWG/LEWG for C++26 (SF:25, F:17, N:0, A:3, SA:12) | POLL |
| 2024-11-19 | [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf)<sup>[37]</sup> "P2900 Is Still Not Ready for C++26" (Dos Reis). Published in the January 2025 mailing | OPPOSITION |
| 2025-01-12 | [P3573R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3573r0.pdf)<sup>[36]</sup> "Contract concerns" (Hava, Garcia, Regev, Dos Reis, Spicer, Stroustrup, et al.) | OPPOSITION |
| 2025-01-13 | [P2899R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r0.pdf)<sup>[16]</sup> "Contracts for C++ - Rationale" (Berne, Doumler, Khlebnikov, Krzemie&nacute;ski) | RATIONALE (filed one day after P3573R0; see below) |
| 2025-02-03 | [P3591R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3591r0.pdf)<sup>[10]</sup> "Contextualizing Contracts Concerns" (Berne, Doumler). Dated seven days before Hagenberg; published in the post-meeting mailing | REBUTTAL |
| 2025-02-11 | EWG Hagenberg lists P3573, P3506, and P3591 as "Papers considered" in one session;<sup>[14]</sup> poll "Remove P2900 from CWG's consideration for C++26, find a different ship vehicle" (SF:9, F:8, N:3, A:19, SA:41), consensus against | POLL |
| 2025-02-15 | Plenary adopts P2900R14 into C++26 Working Draft (100 in favor, 14 opposed, 12 abstain) | POLL |
| 2025-09-02 | [P3829R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3829r0.pdf)<sup>[47]</sup> "Contracts do not belong in the language" (Chisnall, Spicer, Dos Reis, et al.) | OPPOSITION |
| 2025-09-03 | [P3835R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3835r0.html)<sup>[48]</sup> "Contracts make C++ less safe - full stop" (Spicer, Voutilainen, Garcia) | OPPOSITION |
| 2025-09-27 | [P3849R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3849r0.pdf)<sup>[49]</sup> "SIS/TK611 considerations on Contract Assertions" (Achitz) | OPPOSITION |
| 2025-09-29 | [P3851R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3851r0.pdf)<sup>[50]</sup> "Position on contracts assertion for C++26" (Garcia et al.) | OPPOSITION |
| 2025-10-06 | [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf)<sup>[11]</sup> "C++26 Contract Assertions, Reasserted" (Doumler, Berne, et al.). Same mailing as P3849R0 and P3851R0 | REBUTTAL |
| 2025-11-04 | EWG Kona: seven NB removal comments all fail (~9 SF vs ~40 SA each); P3846R0 listed as the response material after the Netherlands comment, not presented;<sup>[17]</sup> [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf)<sup>[5]</sup> records "Rejected all but 2 requests" | POLL |
| 2025-11-04 | [D3911R0](https://isocpp.org/files/papers/D3911R0.html)<sup>[55]</sup> "Make Contracts Reliably Non-Ignorable" (Nea&tcedil;u, Alexandrescu, Teodorescu, Nichita). Presented at Kona as a draft; tracker issue created by the EWG chair the same day | OPPOSITION |
| 2025-11-04 | EWG Kona: D3911R0 non-ignorable pre! (SF:18, F:25, N:22, A:7, SA:0), consensus for change<sup>[55]</sup> | POLL |
| 2025-12-14 | [P3946R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3946r0.html)<sup>[13]</sup> "Designing enforced assertions" (Krzemie&nacute;ski) | REBUTTAL |
| 2025-12-15 | [P3912R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3912r0.pdf)<sup>[12]</sup> "Design considerations for always-enforced contract assertions" (Doumler, Berne, et al.) | REBUTTAL |
| 2026-01-15 | EWG telecon: "EWG approves of the direction of P3911R2 to resolve RO 2-056 for C++26, and encourages more work in said direction" (SF:4, F:4, N:9, A:13, SA:12), consensus against<sup>[62]</sup> | POLL |
| 2026-02-02 | [P4005R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4005r0.html)<sup>[51]</sup> "A proposal for guaranteed-(quick-)enforced contracts" (Voutilainen) | OPPOSITION |
| 2026-02-05 | EWG telecon: D4005R0 not consensus<sup>[56]</sup> | POLL |
| 2026-02-09 | [P4009R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4009r0.html)<sup>[52]</sup> "A proposal for solving all of the contracts concerns" (Voutilainen) | OPPOSITION |
| 2026-02-12 | EWG telecon: D4009R0 strong consensus against<sup>[57]</sup> | POLL |
| 2026-03-23 | EWG Croydon: P3912R0 and P3946R0 first discussed, in the session that polls P4044R0 "Just pre!" (SF:3, F:4, N:0, A:22, SA:23), not consensus<sup>[61]</sup> | POLL |

The sequence shows a three-step cycle:

1. A state-change poll secures the position (forwarding, adoption, or NB rejection).
2. Opposition papers follow, challenging the secured state.
3. Rebuttal papers are dated for the next meeting, where the secured state will be challenged, and reach the room alongside the opposition: as a pre-publication draft, or in the same mailing.

The cycle ran three times between November 2024 and March 2026.

- The Wroclaw forward (November 2024) was followed by P3506/P3573 opposition in the January mailing, which was met by P3591 for Hagenberg (February 2025), where the removal poll failed and plenary adopted. P3591R0 is dated 2025-02-03. It was on the EWG Hagenberg agenda as a paper "considered" before it appeared in any mailing and before its tracker issue existed; the agenda has a placeholder link where the issue number would go.<sup>[14]</sup> The tracker issue, opened after the meeting, describes it in its co-author's words: "Response paper to P3573 'Contracts concerns' published for the Hagenberg meeting. Discussed in EWG in Hagenberg, no further action needed on this paper."<sup>[15]</sup> The rationale paper P2899R0, filed 2025-01-13, one day after P3573R0, is not part of this cycle. P2900R4 named "[D2899R0] - Contracts for C++ - Rationale" as "the sister-paper to this one" on 2024-01-16, 362 days before P3573R0; R5 and R6 repeat the same reference, and P2900R7 cites it under its published number "[P2899R0]" on 2024-05-22.<sup>[60]</sup><sup>[53]</sup> P3573 appears nowhere in its 160 pages.<sup>[16]</sup> Its own authors name the response: P2899R1 records that "A comprehensive response to all these concerns was published in [P3591R0]."<sup>[54]</sup><sup>[10]</sup>
- After the Hagenberg adoption (February 2025), the NB opposition arrived as P3829, P3835, P3849, and P3851; P3846R0 answered them in the same October mailing as P3849R0 and P3851R0. At Kona, EWG organized the contracts day by National Body comment. P3846R0 was listed after the Netherlands "Contracts are important" comment as the response material; the notes record no presentation of it. Its co-author told the room: "All the really important points have actually been made today, so we can skip this entire thing and assume that everyone read the papers in this mailing."<sup>[17]</sup> All seven removal comments then failed.
- The Kona removal polls (November 2025) secured the state for the third time. The opposition arrived the same day. D3911R0 was presented as a draft and polled to consensus for change. P3912 and P3946 answered it in the December mailing, ahead of the January telecons that would test the change. P3912's co-author later described its purpose: "written after reviewing the Romanian comment the first time," and "intended as input to the telecons we had."<sup>[61]</sup> The January telecon polled P3911R2's direction to consensus against.<sup>[62]</sup> The residual attempts, D4005R0 and D4009R0 in February and P4044R0 at Croydon, each failed,<sup>[56]</sup><sup>[57]</sup><sup>[61]</sup> and P3912 and P3946 were first discussed at Croydon in the session that polled P4044R0.<sup>[61]</sup>

The rebuttal papers arrive after the state-change they defend, timed to the meeting where that state will next be challenged. The room receives opposition and rebuttal together, and at Kona the record shows the rebuttal going unpresented. Matrix A applies: Verifying a lengthy rebuttal against a detailed opposition paper is expensive, and reviewers who are not parties to the dispute face the same cost threshold that produces the Push/Abstain equilibrium. The direction is already established, so the apparent benefit of scrutinizing the rebuttal is low. Only the objectors are motivated to find errors in it, and their continued challenges face the reversal-cost inequality. The institutional record that results (state-change, opposition paper, rebuttal paper, state survives) reads to a later audience like the reconciliation described in section 1. It is not reconciliation. It is an untested claim that the objection was answered, preserved by the same memory asymmetry described in section 11.
