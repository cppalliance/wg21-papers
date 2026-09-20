---
title: "A Behavioral Detection Model for Unchecked Institutional Proposals"
document: P4196R0
date: 2026-09-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

[P4195R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4195r0.pdf)<sup>[1]</sup> identifies the incentive structures that [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)'s consensus mechanism creates for proposal authors. This companion paper derives observable behavioral profiles from those structures and provides a detection criteria table with falsification conditions that can be applied to the documented record of any proposal's passage through WG21. The distinguishing characteristic is the author's relationship to feedback: The system works when feedback modifies the design, and fails when the author's institutional position allows feedback to be neutralized instead. The model identifies three author profiles, describes what structural conditions enable unchecked institutional behavior, and provides a diagnostic checklist that distinguishes normal procedural fluency from behavior that exceeds norms the system has no mechanism to enforce.

## Revision History

### R0: September 2026

- Initial version.

## 1. The Model

P4195R0 analyzes the game that SD-4's rules produce. Three mechanisms drive outcomes:

1. Consensus is chair judgment, not a formula applied to poll numbers, so the author's optimization target is the chair's willingness to advance;
2. Polls function as state transitions whose reversal cost grows monotonically, creating path dependence that protects early decisions regardless of their quality; and
3. The institutional record preserves the author's papers but not a minutes register of opposing arguments, so the winning side's case survives as a durable artifact while the losing side's case collapses to a vote tally.

These mechanisms interact with procedural fluency, the ability to convert technical merit into institutional action, which simultaneously increases the probability of adoption and decreases its cost. This advantage compounds for funded, repeat players. The result is an advocacy equilibrium in which many motivated advocates cross-examining each other under capable chair judgment approximate the best design, but which fails when review costs are high, opposition is unfunded, and the record preserves only one side of the argument.

Three behavioral profiles cover the range of how authors operate within this system.

### Profile 1: New Author (Technical Correctness Only)

An individual who:

- Has technical merit but limited institutional resources,
- Treats feedback as substantive and engages it at face value, and
- Lacks procedural fluency to convert merit into institutional action

This author engages substantively with objections, welcomes comparison with competing designs, openly discusses weaknesses, and does not think about burden-of-proof management, or about direction polls as state transitions. The author may produce excellent work that cannot advance because it was submitted to the wrong group, lacks required motivation, or arrives after scheduling decisions. Technical merit is necessary but not sufficient.

### Profile 2: Senior Author (Procedural Fluency)

An individual who:

- Has deep technical expertise and accumulated procedural fluency,
- Treats feedback as strategic input and adjusts their design to build consensus, and
- Operates within institutional norms

This author revises tactically to move experts from SA to WA/N, seeks direction polls deliberately, builds coalitions through reciprocal accommodation, and provides the chair with tractable decisions. The author distinguishes between competitors worth accommodating and those worth outlasting. This is the "ideal author" of P4195R0 - the profile the system is designed to reward.

### Profile 3: Unchecked Institutional Author

An individual who:

- Has institutional backing sufficient to sustain a multi-year campaign,
- Treats feedback as adversarial rather than informative, and
- Directs procedural fluency toward protecting the design, not refining it

The Profile 2 author lets feedback change the design, controlling how much it changes. The Profile 3 author changes the institutional environment to protect the design from feedback. This is the distinguishing characteristic, and it is observable: The C2 response to an objection is technical (the design moves), while the C3 response is political (the environment moves). Objections are decomposed into sub-issues without revisiting the premise, competitors are denied agenda time and discussion polls, repeated objections are characterized as "already addressed" even when the core concern was never answered, and persistent opposition is moralized as blocking progress. Whether these moves reflect conviction or calculation is outside the model's scope; the behavioral pattern is the same.

---

## 2. What the Incentive Structure Produces

The following ten moves are what an unchecked institutional author does when the incentives P4195R0 identifies are unconstrained by committee norms.

1. **Capture the consensus-determination function itself.** Consensus is the chair's call. The author whose institution pays the chair controls the call. Technical objections stop mattering because they never change the outcome.

2. **Manufacture the appearance of independent agreement.** The system approximates the best design by counting independent advocates. Create duplicate votes through employer-bloc polling where employees feel pressure to conform. These satisfy the mechanism on paper while corrupting what it measures. The polls count hands and cannot verify independence.

3. **Control the routing topology.** Route your paper to the group where your coalition is strongest. Influence which group gets jurisdiction over the design space before the competitor arrives. Dissolve the study group if the opportunity permits. The competitor prepared to fight in Room A finds the battle has moved to Room B.

4. **Create prerequisites your competitors must overcome.** Author the foundational infrastructure that competing designs must build on. Your competitor's proposal is now dependent on your machinery. You control what the machinery requires, how it evolves, and what architectures it permits.

5. **Seal the pipeline asymmetrically.** Secure the fastest ship vehicle for your proposal while steering competitors toward slower tracks. Your feature ships in C++29. The competition is still writing position papers for C++32.

6. **Raise review costs structurally.** Present large papers not in the review system and made available days before a meeting, containing significant wording and cross-cutting dependencies such that thorough review exceeds the effort unpaid reviewers are willing to exert. Too long to evaluate, too late to prepare for, too informal to cite against. The system under-produces scrutiny on the proposals that need it most.

7. **Decompose architectural challenges so the premise never receives a direct vote.** "The architecture is wrong" becomes "concerns about X," then "concerns about Y," then individual fixable issues. When the chair is aligned with the author, the question "Should this architecture exist?" is never polled.

8. **Shift the burden of proof deliberately.** First, label the competing design as an alternative. Then characterize the alternative as an objection. Then treat the objection as reopening a settled question. The institutional framing changes while the technical content stays the same.

9. **Script the historical record.** Report favorable polls in your paper's history. Omit unfavorable ones. When objections arise, move to a poll, record the tally, and change the subject. The substance of the objection never enters the written record. Twenty years later, your 40 papers are the institutional memory. The opposition is "SA=4" in the minutes.

10. **Moralize continued opposition.** Characterize opposition as blocking progress, refusing to accept the committee's decision, harming C++. Make the social cost of dissent exceed the technical cost of a bad decision. Whether the author acts from conviction or from institutional strategy, the observable behavior is the same: Technical disagreement is reframed as a character deficiency.

These ten moves are what the incentive structure produces when institutional backing exceeds what the system's safeguards can detect and correct for.

---

## 3. Detection Criteria Table

The following table turns the three profiles into observable behaviors. Column C1 scores Profile 1, column C2 scores Profile 2, and column C3 scores Profile 3. For each criterion, it describes how each profile would characteristically act - providing a diagnostic checklist that can be applied to the documented record of any proposal's passage through WG21.

| # | Detection Criterion | C1: New Author | C2: Senior Author | C3: Unchecked Institutional |
|---|---|---|---|---|
| 1 | Response to architectural objections | Engages substantively; may redesign if convinced | Names a specific technical element from the objection and engages with it | Response is political: process dismissal, assertion without evidence, or extinction framing. No technical element named or engaged |
| 2 | Treatment of competing designs | Welcomes comparison; may not know how to get a joint discussion scheduled | Characterizes competing designs technically (mechanism named, tradeoffs compared) | Competing designs dismissed without technical characterization. Polls pass the substitution test or decide WHETHER rather than HOW |
| 3 | Pursuit of early directional polls | Does not seek them; may not know they exist as a strategic tool | Cites poll results proportionally; characterization matches actual numbers | Poll cited to dismiss a concern that post-dates the poll, or poll result mischaracterized |
| 4 | Treatment of minority objections | Takes them seriously regardless of vote outcome | Engages technically; response names specific elements of the objection | Engages politically: process dismissal, standing questioned, resolution through vote override without technical engagement |
| 5 | Written record behavior | Produces a paper; may not produce rebuttals | Characterizes opposition technically; opponent's mechanism named; unfavorable results documented | Opposition characterized only in political terms or omitted entirely. Opponent's technical mechanism never stated |
| 6 | Relationship with chair | Minimal; may not understand what the chair needs to declare consensus | Chair co-authors and gives priority; competing approaches receive hearings and fair polls | Chair co-authors AND takes discretionary actions that specifically disadvantage competing approaches |
| 7 | Moralization of opposition | "They raise a good point" | Sharp language targeting the design or argument; harsh but argument-focused | Language delegitimizing the act of objecting. Opposition framed as process abuse, comprehension failure, social harm, or conduct violation |
| 8 | Response to committee reversals | Confused; may not understand what happened procedurally | Design-relevant reversal acknowledged in revision history; author revises and returns | Design-relevant reversal omitted from paper history. Paper proceeds as if it did not happen |
| 9 | Burden of proof management | Does not think in these terms | Invites evidence; objecting is cheap; author absorbs the burden | Makes objection expensive. Requires production (paper, implementation, benchmarks). "No new information" invoked for concerns discussed but never resolved |
| 10 | Use of procedural moves | Unaware of most available moves | Aggressive toolkit use; fast iteration, strategic timing | Pace exceeds reviewing body's stated absorption capacity. Documented complaints about inadequate review time, AND proposal proceeds despite complaints |
| 11 | Response to committee instructions | Does it, even at high personal cost | Instruction satisfied in substance within 1-2 meeting cycles; purpose served | Instruction ignored or satisfied through reinterpretation (letter addressed, purpose not served). Proposal proceeds as if satisfied |
| 12 | Behavior between meetings | Works on the paper; may not engage politically | Maintains relationships, coordinates with co-authors, prepares papers | Between-meeting activity produces fait-accompli presentations. Decisions presented as already made before deliberation occurs |
| 13 | Observable cost structure | High cost, low fluency, low probability of success | Normal employer backing; company employs people, they attend under company name, listed in one NB | Cost structure exceeds normal employer backing. Complexity, layering, or opacity beyond "company sends engineers" |
| 14 | What happens if they win | A technically sound feature enters the standard, possibly with rough edges | Pre-adoption claims based on deployment of the actual design; post-adoption, third-party implementations emerge | Pre-adoption claims based on analogous-but-different systems. Post-adoption, no third-party implementation, or advertised capabilities do not materialize |

The distinguishing signal for C3 is the combination of criteria 1, 2, and 7: The author declines to engage architectural objections technically, dismisses competitors without naming their mechanisms, and moralizes opposition rather than engaging it. Any one of these in isolation is common. All three together, sustained across multiple meetings, is the detection signature.

---

## 4. Falsification Conditions

An evidence item scores C3 only when the C2 explanation is insufficient. The following list defines, for each criterion, what normal behavior looks like (the C2 baseline), what exceeds normal (the C3 signal), and a binary test that operationalizes the distinction. If no falsifier fires, the item scores C2.

**Falsification principle:** The bright line between C2 and C3 is the type of response to feedback. A C2 author responds technically: The design changes. A C3 author responds politically: The institutional environment changes to protect the design. If a reasonable observer could attribute the behavior entirely to procedural competence and strategic design revision - the author adjusting the proposal to build consensus - the item scores C2. A C3 score requires behavior where the author adjusts the environment instead of the design: suppressing legitimate alternatives procedurally, engineering burden-of-proof shifts, or ensuring the chair's path of least resistance is always "advance." These are observable acts, not inferences about motivation.

1. **Response to architectural objections**
   - *C2 baseline:* The response names a specific technical element from the objection and engages with it. Demonstrates understanding of the competing mechanism.
   - *C3 signal:* The response is political. Process dismissal, assertion without evidence, or extinction framing. No technical element from the objection is named or engaged.
   - *Test:* Does the response contain at least one specific technical element from the objection? Yes = C2. Zero = C3.

2. **Treatment of competing designs**
   - *C2 baseline:* Competing designs are characterized technically (mechanism named, tradeoffs compared). Polls reference architecture-specific content.
   - *C3 signal:* Competing designs are dismissed without technical characterization. Polls pass the substitution test (could apply to any paper) or decide WHETHER rather than HOW.
   - *Test:* Substitution test on polls (replace paper number - still makes sense = political). Does the paper name the competitor's specific mechanism? Yes = C2. No = C3.

3. **Pursuit of early directional polls**
   - *C2 baseline:* Poll results cited proportionally. Characterization matches actual numbers. Poll used against concerns it could have addressed.
   - *C3 signal:* Poll cited to dismiss a concern that post-dates the poll, OR poll result mischaracterized (more consensus than numbers show, qualifiers dropped).
   - *Test:* Two binary checks. (1) Does the dismissed concern post-date the cited poll? (2) Does the characterization match the actual poll numbers? Either failing = C3.

4. **Treatment of minority objections**
   - *C2 baseline:* Minority objections engaged technically. Response names specific elements of the objection. Evidence of back-and-forth (minutes, revisions, reflector exchanges).
   - *C3 signal:* Minority objections engaged politically. Process dismissal, standing questioned, resolution through vote override without technical engagement.
   - *Test:* Does the response contain technical content addressing the objection's substance? Yes = C2. Only process/political content = C3.

5. **Written record behavior**
   - *C2 baseline:* The written record characterizes opposition technically. Opponent's mechanism named. Unfavorable results documented.
   - *C3 signal:* Opposition characterized only in political terms or omitted entirely. Opponent's technical mechanism never stated. Unfavorable results absent while favorable ones from the same period are included.
   - *Test:* Does the paper state the opponent's technical mechanism? Does it include unfavorable results from the same period as favorable ones? Absence of either = C3.

6. **Relationship with chair**
   - *C2 baseline:* Chair co-authors and gives priority. Normal in WG21 study groups. Competing approaches receive hearings and fair polls.
   - *C3 signal:* Chair co-authors AND takes discretionary actions that specifically disadvantage competing approaches.
   - *Test:* Two conditions, both required. (1) Chair has structural relationship (co-authorship). (2) A specific discretionary action disadvantaged a competitor. Missing either = C2.

7. **Moralization of opposition**
   - *C2 baseline:* Sharp language targeting the design or argument. Harsh but argument-focused.
   - *C3 signal:* Language delegitimizing the act of objecting. Framing opposition as process abuse, comprehension failure, social harm, or conduct violation.
   - *Test:* Does the critique target the argument's substance, or the opponent's standing to object? Substance = C2. Standing = C3.

8. **Response to committee reversals**
   - *C2 baseline:* Design-relevant reversal acknowledged in revision history. Author revises and returns. Escalation via SD-4 is legitimate.
   - *C3 signal:* Design-relevant reversal omitted from paper history. Paper proceeds as if it did not happen. Concern never addressed.
   - *Test:* After a documented design-relevant "no" event, does the next revision acknowledge it? Yes = C2. Omitted = C3. Procedural-only setbacks (wording, timing) being omitted is normal.

9. **Burden of proof management**
   - *C2 baseline:* Author invites evidence. Objecting is cheap. Author absorbs the burden. Normal: "I'll look into it."
   - *C3 signal:* Author makes objection expensive. Requires production (paper, implementation, benchmarks, spec changes). "No new information" invoked for concerns discussed but never resolved.
   - *Test:* What does the author demand from the objector? Information (cheap) = C2. Production (expensive) = C3. For "no new information": Can the invoker cite a written RESOLUTION (not just discussion)? Resolution exists = C2. Only discussion = C3.

10. **Use of procedural moves**
    - *C2 baseline:* Aggressive procedural toolkit use. Fast iteration, strategic timing. Speed alone not diagnostic.
    - *C3 signal:* Pace exceeds reviewing body's stated absorption capacity. Documented complaints about inadequate review time, AND proposal proceeds despite complaints.
    - *Test:* Documented complaint about pace + proceeding anyway. Both required. No complaint = C2. Complaint + slowdown = C2. Complaint + proceed = C3.

11. **Response to committee instructions**
    - *C2 baseline:* Committee instruction satisfied in substance within 1-2 meeting cycles. Purpose served. Normal compliance near 100%.
    - *C3 signal:* Instruction ignored or satisfied through reinterpretation (letter addressed, purpose not served). Proposal proceeds as if satisfied.
    - *Test:* Was the instruction's PURPOSE served, or only its LETTER? Purpose served = C2. Letter only = C3. Ignored entirely = C3.

12. **Behavior between meetings**
    - *C2 baseline:* Author maintains relationships, coordinates with co-authors, prepares papers. Employer-funded teams are normal.
    - *C3 signal:* Between-meeting activity produces fait-accompli presentations. Decisions presented as already made before deliberation occurs. Coordinated messaging across multiple participants within hours of opposition activity.
    - *Test:* Does between-meeting activity produce outcomes presented as settled before the reviewing body deliberates? Yes = C3. Normal paper production and coordination = C2.

13. **Observable cost structure**
    - *C2 baseline:* Normal employer backing. Company employs people, they attend under company name, listed in one NB. Transparent.
    - *C3 signal:* Cost structure exceeds normal employer backing. Complexity, layering, or opacity beyond "company sends engineers."
    - *Test:* Compare documented funding structure to C2 baseline (single employer, single NB, disclosed). Anything structural that does not fit = C3.

14. **What happens if they win**
    - *C2 baseline:* Feature's pre-adoption claims based on deployment of the actual design. Post-adoption, third-party implementations emerge and feature works as advertised.
    - *C3 signal:* Pre-adoption claims based on analogous-but-different systems. Post-adoption, actual design has no third-party implementation, proposer's own use case requires non-standard extensions, or advertised capabilities do not materialize.
    - *Test:* Does the cited pre-adoption evidence implement the same architectural elements as the standardized design? Same = C2. Different = check post-adoption reality. Capabilities did not materialize = C3.

---

## 5. What The Model Cannot Distinguish

The C2/C3 distinction is behavioral, and the tests are bright-line. A C2 author responds to feedback technically: The design changes. A C3 author responds politically: The institutional environment changes to protect the design from feedback. These are different observable behaviors. A C2 author, no matter how capable, well-funded, or convinced, responds by adjusting the design - that is what makes them C2. No amount of skill, resources, or conviction converts a political response into a technical one. The detection criteria in Section 3 and the falsification conditions in Section 4 operationalize this distinction across fourteen criteria.

What the model cannot distinguish is *motivation within C3*. A Profile 3 author who sincerely believes their design is correct and whose political behavior flows from that conviction (the true believer) produces a behavioral record identical to a Profile 3 author who uses institutional position to advance a design for reasons that are not purely technical (the institutional operator). The model does not and cannot determine which. Neither can WG21.

That limitation is irrelevant to the diagnosis. P4195R0's advocacy equilibrium requires many motivated advocates cross-examining each other under capable chair judgment to approximate the best design. C3 behavior breaks this approximation regardless of motivation, because:

- Expert cross-examination is defeated when competitors are denied a hearing
- Chair judgment is captured when advancing becomes the chair's path of least resistance
- The review public-goods problem is exploited when review cost is high and the equilibrium becomes Push/Abstain

The system's only correction mechanisms are implementer revolt (refusing to ship the feature) or a senior committee member absorbing the personal cost of sustained opposition. Both are expensive, unreliable, and activate only after the damage is done.

The Code of Conduct requires an assumption of good faith, but the system has no structural defense against C3 behavior. The model diagnoses the behavior. The motivation is the author's own affair.

---

## 6. Application

This model can be applied to the documented record of any proposal's passage through WG21 by:

1. Collecting evidence items from papers, wiki minutes, reflector posts, and trip reports. Each item receives a sequential label (G1, G2, ...) for traceability.
2. Scoring each item against the detection criteria table using the falsification tests: An item scores C3 only when the C2 baseline explanation fails
3. Challenging every C3 score by searching for counter-evidence that would restore the C2 baseline
4. Tallying hits per column within each criterion and computing a global C3 percentage using unique G#s (each item counts once regardless of how many criteria tag it)
5. Evaluating the combination signal: criteria 1 (architectural objections), 2 (competing designs), and 7 (moralization) all showing C3 simultaneously across multiple meetings

### Evidence Sources

Not all evidence is equal. The following table classifies source types by what they can establish.

| Source | Classification | Use |
|---|---|---|
| Official minutes and poll records (N-documents) | Primary | Direct evidence of outcomes, vote tallies, and chair determinations |
| Numbered P-papers by principals | Primary | Direct evidence of positions, design rationale, and stated responses to objections |
| SD-4 and standing documents | Primary | Establishes the rules under which behavior is evaluated |
| Reflector posts by participants present in the room | Corroborating | Independent confirmation of what occurred; contemporaneous accounts |
| NB comments filed through the formal process | Corroborating | Independent institutional objections with formal standing |
| Implementation reports from vendors | Corroborating | Independent verification of post-adoption outcomes |
| GitHub issue discussions (e.g. cplusplus/papers) | Corroborating | Contemporaneous records of committee-adjacent deliberation |
| D-papers (drafts without P-numbers) | Indirect | The paper itself is not citable, but minutes recording its presentation are. The existence of large D-papers provided just before meetings is evidence for criterion 10 |
| Trip reports and blog posts by participants | Supporting | Context, pattern recognition, and insight into how participants experienced the process |
| Conference journals and talks | Supporting | Public statements by participants outside the committee record |
| Implementation repository history | Supporting | Timeline of engineering investment and design changes |
| Reflector posts summarizing what others said | Supporting | Hearsay; useful for establishing pattern but not for individual scoring |

### Methodology

A single analyst performs the scoring. Two requirements make the work checkable:

1. **Per-criterion assessment.** Before listing evidence items for a criterion, the analyst states whether C2 does or does not explain the record for that criterion, and why. This forces the analyst to commit to a reading before presenting evidence, making the analytical framework transparent.

2. **Per-item citation.** Every scored item cites the specific source document with URL or P-number and date, states the C2 baseline it was tested against, and explains why C2 was insufficient (for C3 scores) or sufficient (for C2 scores).

A second analyst reading the same sources should be able to verify or dispute each individual score without re-reading the entire record.

### Threshold

A finding exists when the global C3 percentage exceeds 20% of total unique scored items across all 14 criteria. Each G# counts once in the global percentage regardless of how many criteria tag it.

Findings are not equal. The strength of a finding is proportional to the extent that the behavior blocks competitors from receiving a fair hearing or shields the proposal from scrutiny. The analyst's report should make the qualitative weight self-evident from the evidence presented.

The combination signal (criteria 1, 2, and 7 all showing C3 simultaneously across multiple meetings) is a separate, stronger threshold indicating systematic rather than isolated C3 behavior.

### Scope

This model diagnoses process capture. It does not prescribe remedies.

The model does not determine whether a proposal's design is good or bad. A technically excellent design can be adopted through C3 behavior, and a technically poor design can fail despite C2 behavior. The model evaluates the *process* of adoption, not the *quality* of the result. A system that produces good outcomes through captured processes is still captured.

This analysis surfaces structural dynamics that are not discussed in the committee's normal discourse. It is a starting point for conversation. Readers who see a framework should discuss how to formalize one. Readers who want to apply the model to a specific proposal's record should do so. The purpose is to make the invisible visible.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains Capy and Corosio, coroutine-native I/O libraries under the C++ Alliance. The author advocates for the coroutine model. The competing model, `std::execution`, is in the C++26 working draft.

This paper asks for nothing.

## References

[1] [P4195R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4195r0.pdf) - "WG21 Game Theory: The Culture That Emerges From SD-4" (Vinnie Falco, 2026).
