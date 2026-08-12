---
title: "WG21 Game Theory: The Adversarial Culture That Emerges From SD-4"
document: P4195R0
date: 2026-08-11
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

WG21's consensus process optimizes for survivability through the committee's represented veto structure, not for technical quality or user welfare.

This report applies game theory to the incentive structures created by [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)'s rules: consensus as chair judgment, polls that record numbers without written reconciliation, and repeat-player dynamics across decades of meetings. It finds that procedural fluency, asymmetric institutional memory, and path dependence are first-order determinants of which proposals enter the C++ standard. Six case histories (contracts, std::execution, networking, trivial relocation, default comparisons, and coroutines) ground the analysis in public WG21 records. The system works well when funded advocates cross-examine each other and a capable chair reads the room; it fails when review costs are high, opposition is unfunded, and the institutional record preserves only one side of the argument.

## Revision History

### R0

- Initial version.

## Executive Summary

The three dynamics identified in the abstract produce a specific cultural pattern. The committee develops a collegial surface over an adversarial undercurrent. Participants remain personally cordial while conducting very long intellectual conflicts, because open confrontation is expensive in a body where you will encounter the same people for decades. Disputes end not when one side is persuaded, but when the minority's willingness to spend social capital is exhausted. The gap between "consensus was achieved" and "we lost the poll" becomes a standing source of institutional tension.

Each participant's behavior is rational given the incentive structure. Authors optimize for adoption, not for discovering whether their design is inferior. Reviewers specialize in domains they care about and abstain elsewhere, because review is a public good nobody wants to provide privately. Chairs optimize for closure, not truth, because the role demands converting conflict into decisions. The minority is asked not "are you right?" but "how strongly are you willing to resist?" - a question that turns a technical judgment into a social one.

The case histories confirm that these dynamics are not occasional failures but equilibrium outcomes. Contracts ([P2900](https://wg21.link/p2900)) illustrates the ideal-author playbook executed to completion. Coroutines illustrates a minority technically vindicated after the fact - C++20 shipped with zero library support, exactly as opponents predicted. The std::execution vote (57-20-27, "numerically this is a weak consensus, but it is a consensus") illustrates chair judgment at the boundary. Networking illustrates a direction poll setting the conceptual framework two years before the chosen path had a concrete proposal. Trivial relocation illustrates a competing design denied even a discussion poll while the established-direction proposal was being reconsidered.

For the C++ community, the practical consequence is that features entering the standard reflect the priorities of funded, persistent, procedurally fluent authors - a group that overlaps with but is not identical to the group best positioned to judge what C++ users need.

## Key Judgments

1. WG21's consensus process settles into an equilibrium that optimizes for survivability through the committee's represented veto structure, not for technical quality or user welfare. The system selects proposals that outlast organized opposition, which correlates with but is not identical to selecting the best design. (Likelihood: almost certain. Confidence: high - structural analysis of SD-4 rules, corroborated by multiple case histories.)

2. Procedural fluency functions as WG21's principal form of political capital. Technical expertise determines whether a participant has something worth proposing; procedural fluency determines whether the institution can hear it, schedule it, or safely ignore it. (Likelihood: almost certain. Confidence: high - observable across every case studied.)

3. The absence of mandatory written reconciliation creates an asymmetry in institutional memory: proponents leave durable intellectual artifacts (papers), while opponents' arguments collapse to vote tallies. This asymmetry compounds over time, making it progressively harder to evaluate whether past decisions were technically sound. (Likelihood: very likely. Confidence: high - structural feature of SD-4, observable in the [P2300](https://wg21.link/p2300) and P2900 records.)

4. WG21's consensus mechanism, because it converts technical disagreement into a social question ("how strongly will you resist?"), produces suppressed rather than resolved conflict. Disputes end without either side being persuaded, and the gap between "consensus was achieved" and "we lost the poll" becomes a standing source of institutional tension. (Likelihood: very likely. Confidence: medium - based on structural analysis and reported dynamics; direct measurement of participant sentiment is not available.)

5. Path dependence is a first-order effect, not a secondary bias. Once a proposal accumulates favorable direction polls, the competing design must demonstrate not merely that \( B > A \), but that \( B - A > C_{\text{reversal}} \), where \( C_{\text{reversal}} \) includes discarded wording, abandoned implementations, schedule risk, and reputational cost to previous decisions. This burden shift frequently determines outcomes independently of technical merit. (Likelihood: likely. Confidence: high - directly observable in trivial relocation and networking cases.)

6. The repeat-player dynamics of WG21 sustain cooperation (mutual accommodation, coalition stability) when the discount factor is sufficiently high, but the same dynamics produce logrolling and complexity ratchets. Features acquire concentrated sponsors while their removal costs are spread across millions of users who cannot organize. (Likelihood: likely. Confidence: medium - the cooperation mechanism is well-established in game theory; the specific WG21 manifestation is inferred from structural analysis.)

7. The public-goods problem in review is severe and structural. Review is expensive, benefits are diffuse, and the probability that any single reviewer's effort changes the outcome is small. The system therefore under-produces critical scrutiny relative to the social optimum, and technically opaque proposals backed by funded, persistent authors face systematically less resistance. (Likelihood: very likely. Confidence: medium - the mechanism is textbook; the magnitude in WG21 specifically is estimated, not measured.)

## 1. The Ideal Author

Picture a standards committee that gets it right. SD-4 defines consensus as the absence of sustained opposition from an important represented interest - not unanimity, not a fixed majority threshold. A proposal enters the system when someone states an idea precisely enough for others to criticize. The author publishes a numbered paper, secures agenda time, remains present through repeated reviews, revises enough to remove organized sustained opposition, and survives successive scrutiny. The fluent author responds to prior objections, avoids surprising the room, consults wording experts, respects scheduling, and gives the chair a tractable decision. On paper, this is a system designed to refine technical ideas through deliberation.

What it selects for in practice is a specific profile: persistence, institutional funding, procedural knowledge, coalition-building, modularity, technical opacity, chair confidence, existing momentum, and compatibility with active constituencies. "The resulting system is stable and difficult to capture in a single dramatic vote. But it systematically rewards persistence, attendance, procedural fluency, employer support, coalition-building, and chair confidence." The successful strategy is compact enough to state in a single sentence: "Publish, attend, persist, compromise selectively, build legitimacy, and eliminate organized opposition."

The ideal author optimizes for adoption. The ideal reviewer optimizes for the domain the reviewer cares about. The ideal user optimizes for nothing, because the cost of participation exceeds the probability of influence. The institution therefore hears from people who can afford to play, filters their contributions through procedural gates, and delivers the result to a population that had no seat at the table.

- Authors optimize: adoption probability, reputation, employer value
- Reviewers optimize: domain protection, future reciprocal influence
- Users optimize: nothing - rational exit follows from low influence probability and high participation cost

SD-4's consensus definition, the absence of sustained opposition from an important represented interest, creates these incentives structurally. "Sustained" requires attendance across meetings. "Important" and "represented" require institutional standing. "Opposition" must be organized. The rules do not explicitly exclude anyone, but they weight the game toward players who can afford to persist.

**The broader C++ population is a beneficiary or victim of the result, but is only weakly represented in the game.**

The contracts saga illustrates the profile. SG21 formed after [P0542](https://wg21.link/p0542)'s removal from C++20 at Cologne 2019 ([P1823R0](https://wg21.link/p1823r0)). [P2182](https://wg21.link/p2182) introduced the "MVP" concept: start from P0542, strip controversial features. The authors who set the roadmap ([P2695R0](https://wg21.link/p2695r0)) and defined "minimal" controlled which features were in scope. [P2961](https://wg21.link/p2961) (Doumler, Maurer) proposed "natural syntax" and argued against alternatives; the group adopted it into the MVP. When SG21 polled on whether to ship as a TS on 2024-05-30, consensus was against - the same group that controlled the proposal also controlled the ship-vehicle decision. P2900R6 moved from SG21 to EWG on 2024-02-29 with consensus. EWG forwarded P2900R11 to CWG/LEWG for C++26 at Wroclaw in November 2024 (LEWG: SF:23, F:9, N:1, A:0, SA:5). Plenary adopted P2900R14 into the C++26 Working Paper on 2025-02-16. At every stage, the authors who persisted, attended, built coalitions, and maintained chair confidence advanced the proposal. The mechanism worked as designed.

**Excellence is not what the mechanism directly optimizes. Survivability through the committee's represented veto structure is.**

## 2. What Culture Emerges

The culture that grows from this mechanism is not primarily adversarial. It is managed consensus among repeat players. Open confrontation is expensive because participants encounter the same people at the next meeting, and perhaps for decades. Rational participants learn to distinguish "I prefer B" from "I am willing to prevent A from proceeding." The second statement consumes considerably more social and institutional capital than the first.

WG21 resembles a functional peerage - "an elective technical aristocracy with earned, informal peer status," albeit one "considerably more interested in template metaprogramming than most historical nobility." Status accrues to people who can master a technical domain, write credible papers, absorb criticism without becoming impossible to work with, recognize which fights matter, persuade respected participants, understand when consensus exists, avoid surprising the institution, and shepherd work over multiple years.

**The natural unit of power is not the argument, but the argument plus a person willing to carry it through the institution.**

The incentive structure rewards a specific combination of technical competence and institutional durability:

- Master a technical domain deeply enough to write proposals that survive expert scrutiny
- Build and maintain a reputation for reasonable conduct over years
- Recognize which objections can be accommodated and which must be opposed
- Invest in relationships that translate into coalition support
- Understand when the chair will read the room as having reached consensus

SD-4's consensus mechanism and repeat-player dynamics create a culture where "A technically compelling position without a champion is weak. An imperfect position with several persistent, respected champions can be strong." The system functions well when the peerage's senior members absorb the cost of repair. The default comparisons saga shows this. Stroustrup's [P0221R2](https://wg21.link/p0221r2) proposed generating all six comparison operators by default and passed EWG review. Plenary rejected it at Oulu 2016: operator< should not be generated by default for types where ordering is meaningless, and no opt-out mechanism existed ([P0432R0](https://wg21.link/p0432r0), [P1190R0](https://wg21.link/p1190r0)). The rejection forced a complete redesign. Sutter's [P0515](https://wg21.link/p0515) (operator<=>, the spaceship operator) took a fundamentally different approach using three-way comparison and explicit opt-in via `= default`. The system worked as intended - plenary caught a design flaw that subgroup consensus had not resolved. But note: it took Herb Sutter to pick up the pieces. The peerage functions well when a senior member absorbs the cost.

## 3. How the Objectors Feel

The minority experiences a specific asymmetry. The majority can point to polls. The authors can point to years of work. The chair can point to consensus. The minority can only point to the argument. If the argument is not preserved in the institutional record, participants who hold it may conclude that the process is converting failure to persuade the room into failure of the argument itself.

The minority may believe: "The technical problem is still there. Nothing about a poll made it disappear." The reactions are predictable and documented. Some withdraw: "Fine. Do whatever you want." Some become more forceful: "You still have not answered the objection." Some start documenting everything. Some produce competing papers. Some appeal to another subgroup or national body. Some become suspicious of the institution itself. A vicious feedback loop develops: the minority feels unheard, the minority becomes more forceful, the majority perceives obstruction, the majority discounts the minority, the minority feels even less heard.

**The person remains respected while the person's objection becomes socially obsolete.**

Each player responds rationally to the incentive structure:

- The minority optimizes for: having the objection heard and answered on its merits
- The majority optimizes for: reaching closure and making progress
- The chair optimizes for: a clean decision that can be recorded as consensus

SD-4 creates the conditions for this dynamic in three ways: it requires no reconciliation, it treats consensus as chair judgment rather than measured agreement, and it preserves poll numbers without written responses to dissent. When an outsider raises a late objection, "the institution hears, implicitly: 'Discard accumulated consensus, invalidate previous work, spend scarce meeting time reconsidering it, and trust someone who has not participated in the process that generated those decisions.'"

The coroutines case made this concrete. The Coroutines TS ([P0057](https://wg21.link/p0057), Gor Nishanov) was voted into C++20 despite organized opposition. Google proposed an alternative: "Core Coroutines" ([P1063R1](https://wg21.link/p1063r1), Romer/Dennett/Carruth). VMware filed [P1329R0](https://wg21.link/p1329r0) arguing the TS should not be merged, citing heap allocation reliance on optimization, confusing terminology, and lack of standard library support. The merge succeeded over these objections. C++20 shipped coroutines with zero standard library components. `std::generator` did not arrive until C++23 ([P2502](https://wg21.link/p2502)). No standard task type exists as of C++26. The heap-allocation-elision concern persists: compilers cannot guarantee elision in many real-world use cases. The minority's concerns proved partially correct. Nobody wrote up why they lost.

**What humans want most in serious disagreement is evidence that the other side actually understood the argument before rejecting it.**

## 4. How the Authors Feel

The people whose design is moving forward tend to experience themselves as having already done the work. They have written papers, attended meetings, answered questions, revised repeatedly, obtained favorable polls, and produced implementations. Over time, they stop perceiving the opposing design as an equal alternative. The language changes: "That is an interesting alternative." Then: "We already discussed that." Then: "We cannot keep reopening settled questions." Then: "At some point we have to make progress." That progression can occur even if the technical objection has never actually been resolved.

Persistent opposition begins to look less like useful technical criticism and more like refusal to accept a legitimate decision. Everyone involved learns, implicitly, that there is a distinction between being technically unconvinced and being willing to spend the social capital necessary to continue opposing consensus.

**The majority will often still be friendly to the minority personally. But intellectually, the minority's position gradually loses legitimacy because it has lost procedurally.**

The author's incentive structure drives the shift in perception:

- The author has invested years of effort, reputation, and institutional capital
- Each favorable poll increases the perceived cost of reversal
- Each revision cycle consumes time and goodwill
- Reopening feels like an attack on accumulated work, not a technical contribution

SD-4 creates this pressure through direction polls that accumulate state, a consensus definition that converts objection into a question of social willingness, and a timeliness norm that penalizes late-arriving alternatives. The system provides no mechanism for distinguishing "we resolved this objection" from "we outvoted this objection."

The P2300 `std::execution` story from the author's seat illustrates the frustration. The broader executors effort spans roughly eight years from [P0443](https://wg21.link/p0443) (2016). P2300R0 was published in 2021. It failed for C++23 - LEWG polled ([P2459R0](https://wg21.link/p2459r0)) SF:23, WF:14, N:0, WA:6, SA:11, "No consensus. Sustained strong opposition." Timing was the major factor. Weak forwarding to C++26 followed: SF:12, WF:6, N:2, WA:2, SA:3, "Weak consensus in favor" ([P2575R0](https://wg21.link/p2575r0)). The plan paper ([P3109R0](https://wg21.link/p3109r0)) was approved in February 2024: SF:6, WF:6, N:1, WA:0, SA:0, "Strong consensus." Plenary adopted P2300 in June 2024: 57-20-27. Sutter called it: "Numerically this is a weak consensus, but it is a consensus." LWG consumed the majority of its bandwidth for months reviewing P2300 wording. Wakely warned: "We won't be able to process everything we need for C++26. There will be disappointment." From the authors' perspective: eight years of work, multiple revisions, repeated reviews, implementation experience (stdexec, libunifex), and 57 in favor - and the result is still called "weak."

## 5. How the Chair Feels

The chair normally does not want to determine "Alice is technically correct and Bob is technically wrong." That would require the chair to become the supreme technical authority. The chair is incentivized to determine: "Is there enough agreement for the committee to proceed?" The chair will usually try to lower the temperature rather than adjudicate the truth. The chair's objective becomes: convert conflict into a decision, rather than establish which side's technical claim is correct.

**The minority is increasingly being asked not "Are you right?" but "How strongly are you willing to resist?"**

That question subtly turns a technical judgment into a social one. "A person who continues voting Strongly Against must repeatedly assert: 'Yes, I believe my judgment is important enough to impede everyone else's work.' That is psychologically expensive. Especially in a community of colleagues."

**"We have given this concern extensive consideration" can be true even when "We have conclusively answered this concern" is false. That distinction is central.**

The chair faces a constrained optimization:

- Advance too aggressively: accusations of railroading, risk of NB opposition
- Defer too readily: frustrated authors, slipping schedules, accusations of allowing one or two people to veto progress
- The equilibrium: advance proposals that have passed expected stages, show substantial support, and lack organized sustained opposition

SD-4 places the chair at the center of the consensus determination. Consensus is chair judgment, not a formula applied to poll numbers. A chair who repeatedly refuses to advance faces costs. A chair who advances over substantial expert opposition risks different costs. The role demands closure, not truth.

The same P2300 moment from the chair's seat shows the trap. Sutter at plenary: "Numerically this is a weak consensus, but it is a consensus. I'm not hearing any NB concerns at this time, and it's been many months and there would have been time for NBs to raise concerns." One NB reported individual members had concerns and requested postponement. Their concerns were "mostly about teachability." Two other NBs reported individual member concerns but "did not determine national opposition at that time." No NB filed formal opposition. Sutter admonished: "We want to hear your concerns, but we really appreciate not hearing them for the first time in the plenary. Please raise your concerns early so we can front load them." The chair must weigh: eight years of work, 57 in favor, 20 against, 27 abstaining, no formal NB opposition, months of LWG bandwidth consumed, schedule pressure. An evening session was organized specifically to address committee members' unfamiliarity with the framework. Senior committee members expressed concern about the proposal's complexity and drew unfavorable comparisons to the coroutines experience. The chair is not positioned to determine who is technically right. The chair is positioned to determine whether the institution can proceed.

## 6. How the Objectors Perceive the Authors

The opposing side may come to believe the advancing coalition is invested in its own work, unwilling to admit architectural mistakes, using procedure instead of argument, benefiting from relationships and accumulated status, and defining "consensus" as whatever permits the proposal to continue. The disagreement gradually becomes moralized. Neither interpretation needs to be entirely true. Both can arise rationally from each side's experience of the same process.

**When the author says "We've addressed this concern," the opponent hears "We've made enough changes that the chair will no longer let your objection stop us."**

The objector's perception is shaped by specific incentives:

- The objector has invested analysis and reputation in the competing position
- Each accommodation that does not address the architectural concern looks like procedural evasion
- The burden of proof has shifted: the objector must now demonstrate the forwarded proposal should be withdrawn
- Coalition dynamics favor the advancing group, which has more invested participants

The structural conditions for this perception come from three sources: SD-4's forwarding mechanism, its lack of mandatory written responses to dissent, and the accumulated state of favorable polls.

The P2900 contracts case from [P3573](https://wg21.link/p3573)'s perspective illustrates the gap. P3573R0, "Contract concerns" (January 2025), authored by Stroustrup, Dos Reis, Voutilainen, Vandevoorde, Spicer, Garcia, Hava, van Winkel, and Regev, stated "grave concerns about the current design." [P3506R0](https://wg21.link/p3506r0) (Dos Reis) argued "P2900 Is Still not Ready for C++26." These papers were filed after EWG had already forwarded to wording groups. The objectors had to demonstrate that the already-forwarded proposal should be withdrawn, not that it was unready. NB comments followed: ES-050, US-26-051, US-25-052, FR-004-053. From the objectors' perspective: years of closed-loop SG21 development, alternatives denied fair hearing, late objections called "already addressed," and the burden shifted to challengers. The TS ship vehicle was rejected by the same group that controlled the proposal.

## 7. How the Authors Perceive the Objectors

The advancing side may come to believe the opponents are perfectionists, unwilling to compromise, protecting their own design, repeatedly reopening decisions, preventing C++ from making progress, and demanding an impossible standard of certainty. "When the opponent says: 'The fundamental issue remains,' the author hears: 'No amount of accommodation will ever satisfy you.'" Both sides may be sincere.

Section 4 named the distinction that both sides learn: being technically unconvinced is not the same as being willing to spend the social capital needed to keep opposing consensus. The social norm becomes: "We can disagree strongly, but eventually somebody has to accept that the group has moved on."

**For the winning coalition, that feels like mature governance. For a technically serious minority whose objections were never reconciled, it can feel like politely administered exclusion.**

The author's perception follows from the same incentive structure as the objector's, viewed from the other side:

- The author has responded to feedback, revised, and obtained favorable polls
- Each continued objection looks like refusal to accept legitimate institutional decisions
- The author's coalition has invested more person-hours than the objectors
- Progress on C++26 depends on closure

SD-4 provides no mechanism for determining whether a repeated objection reflects an unresolved technical flaw or a participant's refusal to accept the group's direction. The distinction matters enormously, and the institution cannot make it.

The same P2900 contracts case from [P3846R0](https://wg21.link/p3846r0)'s perspective closes the circle. P3846R0/R1, "C++26 Contracts, reasserted" (Doumler, Berne), responds to NB comments by characterizing objections as repeating "earlier objections ([P3173R0](https://wg21.link/p3173r0), P3506R0, P3573R0) already considered repeatedly in EWG. No new information has been presented since." EWG polled at Hagenberg on 2025-02-11: "Remove P2900 from CWG's consideration for C++26, find a different ship vehicle" - consensus against. N5007 (Hagenberg minutes): "Consensus on contracts has increased since the last meeting." From the authors' perspective: years of SG21 work, multiple EWG reviews, favorable polls at every stage, wording complete, NB comments addressed - and the same people are still objecting with the same arguments. Same controversy as section 6. Irreconcilable readings. Same process, two experiences. The system provides no mechanism for determining which reading is correct. That is the finding.

## 8. Procedural Fluency as Political Capital

Procedural fluency is the ability to convert technical merit into institutional action. "Technical expertise determines whether you have something worth saying. Procedural fluency determines whether the institution can hear it, act on it, or safely ignore it." The distinction matters because the two capacities are independent. A brilliant implementer with no procedural knowledge and a mediocre programmer with deep procedural fluency face radically different odds.

Fluency serves five functions. First, it reduces transaction costs: the expert loses less energy to the machinery. A newcomer may spend months on excellent work that cannot advance because it was submitted to the wrong group, lacks required motivation, or arrives after scheduling decisions. Second, it expands the available move set: formally everyone has similar rights; practically only fluent participants know all available moves. Third, it controls framing. Poll construction determines which question is being decided. "Do we like this direction?" versus "Forward this paper for C++29" - same proposal, different institutional consequences.

Fourth, fluency produces legitimacy: fluent authors signal they are safe institutional counterparties. Chairs rationally prefer such authors because advancing their papers presents less risk. Fifth, it converts attendance into cumulative power: procedural knowledge is partly tacit. Repeated participation teaches which objections are considered serious, which prior decisions may be reopened, and how much revision is enough.

The feedback loop is direct: fluency yields chair confidence, which yields agenda access, which yields successful papers, which yield reputation, which yields greater fluency and access. The cycle compounds over meetings.

Procedural fluency is not neutral. It redistributes influence toward repeat attendees, employer-funded participants, chairs, prolific authors, and people with established relationships. It disadvantages independent experts, implementers who cannot attend regularly, users encountering the process for the first time, and critics who appear only when a proposal becomes publicly visible. "The crucial inequality is therefore not necessarily: 'Insiders are allowed to vote and outsiders are forbidden.' It is: 'Insiders know when a consequential decision is actually being made, what language will influence it, and what must have happened beforehand for their intervention to count.'"

The trivial relocation case shows what happens when fluency is distributed unequally. [P1144](https://wg21.link/p1144) (Arthur O'Dwyer, first revision 2018) defines relocation as equivalent to move+destroy with trivial relocation as optimization. [P2786](https://wg21.link/p2786) (Gill, Meredith, first revision 2023) defines trivial relocation as a separate language primitive. At Tokyo in March 2024, EWG forwarded P2786 to CWG by vote 7-9-6-0-2. At St. Louis in June 2024, EWG voted 21-15-3-6-5 that P2786 was not ready and pulled it back. [P3233](https://wg21.link/p3233), "Issues with P2786," triggered the reconsideration. P1144R12 states: at St. Louis, the author asked whether EWG would schedule P1144 for discussion or even poll whether to discuss it. The EWG chair said no. The P2786 authors had procedural access; the P1144 author did not. The competing design could not get a hearing while the established-direction proposal was being reconsidered.

## 9. Polls as State Transitions

A poll looks like information - 17/8/4/3/2. Its principal function is often state mutation. Before the poll: "This design question is open." After the poll: "The committee has direction." At the next meeting, the conversation begins from the new state. The distinction matters because information can be re-evaluated but state changes are costly to reverse.

An author has strong incentive to obtain favorable state transitions as early as possible. A competitor arriving at state \( S_3 \) is no longer competing against the original paper. The competitor is competing against the paper plus three previous committee decisions. "Early polls have option value far beyond the particular question being asked."

Three possible polls for the same proposal illustrate the mechanism: "Do we like this general direction?" or "Should the author continue working?" or "Forward this paper for inclusion in C++29." A proposal may receive strong support on the first two and fail the third. An "encourage further work" poll can generate momentum, legitimacy, and an expectation of eventual adoption. "This is agenda power disguised as grammatical precision."

The networking and executors case shows the full cycle. In October 2021, LEWG took five polls of 56 participants ([P2452R0](https://wg21.link/p2452r0), [P2453R0](https://wg21.link/p2453r0)). Poll 1: "Networking TS/Asio async model is a good basis for most async use cases, including networking, parallelism, and GPUs." SF:5, WF:10, N:6, WA:14, SA:18 - weak consensus against. Poll 2: "Sender/receiver model (P2300) is a good basis for most async use cases, including networking, parallelism, and GPUs." SF:24, WF:16, N:3, WA:6, SA:3 - consensus in favor. Poll 4: "Networking in the C++ Standard Library should be based on sender/receiver model (P2300)." SF:17, WF:11, N:10, WA:4, SA:6 - weak consensus in favor.

The polls presumed a single-model world. A separate straw poll on "We must have a single async model" had yielded no consensus. P2453R0 commentary stated: "For paper authors, this poll is encouragement to do work in the area of networking based on senders and receivers, or to be prepared with compelling new information on why networking should use a different model." [P2469R0](https://wg21.link/p2469r0) (Kohlhoff, Allsop, Falco, Hodges, Morgenstern) observed: "No specific proposal has been presented showing how a networking API based on sender/receiver would look." LEWG set the direction before either a reference implementation or a design paper existed. [P2762R1](https://wg21.link/p2762r1) (K&uuml;hl, 2023), the first concrete sender/receiver networking proposal, arrived two years after the direction poll. The Networking TS (Asio) had 18+ years of deployment experience. The direction poll set the conceptual framework before the chosen path had a concrete proposal.

## 10. The Asymmetry of Institutional Memory

The proposal itself is typically a substantial document: the author's motivation, requirements, examples, alternatives considered, responses to feedback, and wording. The proponent leaves a durable intellectual artifact. Suppose a highly qualified opponent gives a twenty-minute argument explaining why the architecture is wrong. The poll reads 18/9/5/3/4 and the record says: "Consensus in favor." Twenty years later, the author's 40-page P-paper remains. The opposition has collapsed into SA=4.

**Future participants encounter the historical record as though the winning side possessed an argument and the losing side possessed votes. That is epistemically very different from what actually happened.**

No malign intent is required. From the author's perspective, a written chair's reconciliation creates future liabilities. Without that record, the historical fact is merely "the committee achieved consensus." The latter is much harder to reopen. The losing side would have to create that record itself - by writing another paper. Opposition also requires authorship, time, procedural fluency, and persistence. The equilibrium gives the winning coalition little incentive to create an excellent permanent statement of the losing coalition's case.

**The author need not win the argument in the historical record. The author need only survive it in the room.**

The P2300 `std::execution` record shows the asymmetry. The plenary vote was 57-20-27. The 20 "against" votes had specific reasons: complexity, teachability, compile time, breadth of implementation experience (mostly Meta), and lack of complementary library features. Senior committee members raised these concerns during the evening session, with some drawing unfavorable comparisons to the coroutines experience. These reasons live in oral discussion and in scattered paper comments. The permanent record is: P2300R10 (the 40-page paper) and "Motion 12: 57-20-27, consensus." Twenty years from now, the paper survives. The opposition is "SA=20" in the minutes.

## 11. Path Dependence and the Burden-of-Proof Flip

Two mutually exclusive designs A and B, both technically credible. The actual game is sequential, not simultaneous. A acquires institutional state: three meetings of discussion, favorable direction polls, implementation work, an R7 paper, wording review, endorsements. B appears with excellent design at that point. The comparison becomes: "continue A" versus "reverse several previous decisions and adopt B." The burden shifts. B must demonstrate not merely that \( B > A \), but that \( B - A > C_{\text{reversal}} \), where \( C_{\text{reversal}} \) includes discarded wording, abandoned implementations, schedule risk, and reputational cost to previous decisions.

A four-stage linguistic transformation tracks the shift: "A and B are competing designs." Then "A is the committee direction; B is an alternative." Then "A is the proposal; B is an objection to the proposal." Then "A is the status quo; B wants to reopen the question." "The technical content may not have changed at all. The institutional position has."

The game becomes a war of attrition: who is willing to pay the cost for longer? Persistence changes the probability of winning independently of technical quality. "Showing up again is itself a move." A skilled author will often withdraw, revise, negotiate, or postpone rather than demand "A or B. Vote now." The losing design may not receive a dramatic rejection. It may experience: less agenda time, then no forwarding poll, then another revision requested, then the champion loses interest, then nothing. "B simply stopped moving."

The trivial relocation case shows the full cycle. P1144 (2018) and P2786 (2023): two competing designs for trivial relocation. [P2814](https://wg21.link/p2814) (2023) provided a formal comparison, originating from EWGI direction at Issaquah. At Tokyo in March 2024, EWG forwarded P2786 to CWG (7-9-6-0-2). P2786 became "committee direction." At St. Louis in June 2024, EWG pulled P2786 back (21-15-3-6-5). P3233, "Issues with P2786," triggered reconsideration. Meanwhile, P1144 was denied even a discussion poll. P2786 re-advanced and merged into the C++26 working draft (visible in N5008, March 2025). Then at Kona in 2025, joint EWG-LEWG reached consensus to remove. N5031: "the implementers of our major tools unanimously and independently were unable to support this particular version." Plenary poll 3a (postpone removal vote to UK meeting) did not pass. Plenary poll 3b (apply [P3920R0](https://wg21.link/p3920r0) for removal) passed 80-5-28. The feature was deferred to C++29. LEWG wiki: all relocatability NB comments marked "Rejected (feature pulled from 26)." Post-removal, [P4197R0](https://wg21.link/p4197r0) proposes establishing consensus on underlying design questions before choosing a concrete proposal. [P3937R0](https://wg21.link/p3937r0) argues bitwise relocation must be the basis. Design-question decomposition was invoked retroactively as repair, not proactively as a decision tool. The four-stage transformation played out in real time across 18 months. The system eventually reversed itself, but only after implementers unanimously refused support.

## 12. The Mathematics

Everything described in sections 1 through 11 - the incentives, the culture, the structural dynamics - follows from a small set of payoff functions and strategic interactions. The math that follows starts simple and builds. Each subsection introduces one layer of complexity and ends by naming the variable the participants are unconsciously optimizing. The reader who stops after the first subsection still understands the ledger. The reader who finishes the fourth sees the full machine.

### What Each Player Wants

The structure of WG21 is a multi-player game with asymmetric payoffs. Each participant's behavior follows from a simple ledger: benefits on the left, costs on the right.

The author's payoff function:

\[
U_A = pV + R + E - C_p - C_r - C_a - D
\]

where:
- \( pV \): probability of adoption times value of adoption
- \( R \): reputation and influence
- \( E \): employer or organizational benefit
- \( C_p \): paper and implementation cost
- \( C_r \): revision cost
- \( C_a \): attendance and coalition cost
- \( D \): delay cost

The author enters when the expected payoff exceeds zero. \( C_a \) - attendance cost - gates entry. Only funded people can afford to play, because \( C_a \) includes travel, lodging, and the opportunity cost of weeks per year.

The reviewer's payoff function:

\[
U_R = Q + I + F - C_s - C_c
\]

where:
- \( Q \): improvement in C++
- \( I \): protection of the reviewer's technical interests
- \( F \): future reciprocal influence
- \( C_s \): study and review cost
- \( C_c \): social and political conflict cost

Reviewers specialize. They invest heavily in domains they care about (\( I \) is high) and abstain elsewhere (\( C_s \) exceeds \( I + F \)).

The user's payoff function reveals why the broader population is absent:

\[
U_{\text{user}} \approx \Pr(\text{my review changes result}) \times \Delta Q - C
\]

The probability term is usually very small, while \( C \) may involve weeks of study and travel. Rational nonparticipation follows even where the collective value of review is enormous. Review is a public good that nobody wants to provide privately.

The variable they are unconsciously optimizing: authors optimize \( V \) (adoption value). Reviewers optimize \( I \) (domain interest). Users optimize nothing - they rationally leave.

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

Fluency simultaneously increases the probability of adoption and decreases the cost of pursuing it. This double advantage is the mechanism through which the informal peerage forms. The fluent participant does not necessarily produce better designs; the fluent participant loses less energy to the machinery and gets more attempts.

The feedback loop is a causal chain:

\[
\text{fluency} \rightarrow \text{chair confidence} \rightarrow \text{agenda access} \rightarrow \text{successful papers} \rightarrow \text{reputation} \rightarrow \text{greater fluency}
\]

Each successful paper earned through fluency increases fluency further. The system compounds advantage for repeat players. A newcomer with a superior design faces both a lower probability of success and a higher cost of pursuit - the inequality runs on both sides of the ledger.

The variable they are unconsciously optimizing: \( F \) (procedural fluency) - the dominant investment.

### What Happens in the Room

Individual optimization produces collective dynamics. Three matrices capture the strategic interactions that shape outcomes.

**Matrix A: Author versus Reviewer.** The author chooses Revise or Push unchanged. The reviewer chooses Scrutinize or Abstain. Let \( c \) = cost of serious review.

|  | Reviewer scrutinizes | Reviewer abstains |
|---|---:|---:|
| Author revises | 3, 3-c | 4, 1 |
| Author pushes unchanged | 1, 2-c | 5, -2 |

When \( c < 2 \): the equilibrium is Revise, Scrutinize - the system works as intended. When \( c > 4 \): the equilibrium is Push, Abstain - proposals advance without adequate review. At intermediate costs, mixed strategies produce unpredictable quality. "A proposal need not defeat every possible objection. It must outlast the objections whose holders are willing to pay the cost of sustaining them." The review cost \( c \) is not a constant. It increases with the proposal's technical opacity, length, and interaction with existing standard wording. The system therefore under-produces scrutiny on the proposals that need it most.

**Matrix B: Repeat-player accommodation.** Two durable proposal coalitions, each can Accommodate or Block.

|  | B accommodates | B blocks |
|---|---:|---:|
| A accommodates | 3, 3 | 0, 4 |
| A blocks | 4, 0 | 1, 1 |

One-shot: Block, Block is the Nash equilibrium. Indefinitely repeated with grim-trigger: cooperation is rational when \( \delta \geq \frac{1}{3} \). Long-term participants who expect to return for many meetings easily value the future that highly. "This can produce healthy cooperation. It can also produce logrolling, in which the aggregate standard acquires features that would not survive an independent, population-wide cost-benefit test."

**Matrix C: Chair and organized opposition.** The chair chooses Advance or Defer. The room chooses Acquiesce or Organize.

|  | Room acquiesces | Room organizes |
|---|---:|---:|
| Chair advances | 4, 3 | 0, 2 |
| Chair defers | 1, 0 | 2, 3 |

Two pure equilibria: Advance/Acquiesce and Defer/Organize. This is a coordination game. Early signals determine which equilibrium is selected. That explains the procedural emphasis on surfacing objections before plenary. The chair's move selects the equilibrium. Once a proposal reaches plenary with years of work, subgroup approval, and wording, the focal equilibrium has usually become Advance/Acquiesce. A late opponent is attempting to move the entire room to the alternative equilibrium - a coordination problem that grows harder the more institutional state has accumulated.

The variable they are unconsciously optimizing: \( \delta \) (the future) - cooperate because you will be back. The discount factor determines whether mutual accommodation or mutual blocking prevails.

### The Machine

The full optimization target:

\[
\Pr(\text{chair declares consensus}) \rightarrow \max
\]

Every behavior described in sections 1 through 11 follows from this single objective. The author who revises tactically, the reviewer who specializes, the chair who advances, the repeat player who accommodates - each is maximizing the probability that the chair declares consensus for their preferred outcome.

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

A competitor arriving at \( S_3 \) competes against the paper plus three previous committee decisions.

The reversal cost inequality:

\[
B - A > C_{\text{reversal}}
\]

where \( C_{\text{reversal}} \) includes: lost committee time, discarded wording, abandoned implementations, reputational cost to previous decisions, schedule risk, reopening settled debates, and antagonizing A's coalition.

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

- Authors: enter only when private value exceeds cost; once entered, persist, attend, revise tactically, construct a coalition
- Reviewers: specialize; review aggressively where personal interest is high; abstain elsewhere; reserve strong opposition for issues sufficiently important to justify its cost
- Chairs: advance proposals that have passed expected stages, show substantial support, lack organized sustained opposition, and present manageable NB risk
- Repeat players: maintain relationships, trade concessions, avoid gratuitous opposition
- National bodies: intervene selectively where salient enough to justify coordination

The variable they are unconsciously optimizing: \( \Pr(\text{consensus}) \) - not truth, not quality, but survivability through the represented veto structure. That distinction is the whole game.

## 13. Disclosure

The author of this paper is a co-author of P2469R0, cited in section 9, and participated in the networking and executors discussions that section analyzes.
