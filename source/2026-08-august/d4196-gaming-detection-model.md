---
title: "A Behavioral Detection Model for Unchecked Institutional Proposals"
document: P4196R0
date: 2026-08-11
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

[P4195R0](https://wg21.link/p4195r0) identifies the incentive structures that [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)'s consensus mechanism creates for proposal authors. This companion paper derives observable behavioral profiles from those structures and provides a detection criteria table with falsification conditions that can be applied to the documented record of any proposal's passage through WG21. The model identifies three author profiles, describes what structural conditions enable unchecked institutional behavior, and provides a diagnostic checklist that distinguishes normal procedural fluency from behavior the system's self-correction mechanisms cannot reach.

## Revision History

### R0

- Initial version.

## 1. The Model

P4195R0 identifies SD-4's consensus mechanism, its repeat-player dynamics, and its asymmetric institutional memory as producing specific author behaviors that are rational responses to the incentive structure. Three profiles cover the range of how authors operate within this system.

### Profile 1: New Author (Technical Correctness Only)

An individual who:

- Has a technically sound design
- Lacks procedural knowledge and institutional relationships
- Relies on the merit of the argument alone

This author engages substantively with objections, welcomes comparison with competing designs, openly discusses weaknesses, and does not think about burden-of-proof management, or about direction polls as state transitions. The author may produce excellent work that cannot advance because it was submitted to the wrong group, lacks required motivation, or arrives after scheduling decisions. Technical merit is necessary but not sufficient.

### Profile 2: Senior Author (Procedural Fluency)

An individual who:

- Has deep technical expertise in a domain
- Has accumulated procedural fluency over years of participation
- Understands the full move set available under SD-4
- Operates within institutional norms

This author revises tactically to move experts from SA to WA/N, seeks direction polls deliberately, builds coalitions through reciprocal accommodation, and provides the chair with tractable decisions. The author distinguishes between competitors worth accommodating and those worth outlasting. This is the "ideal author" of P4195R0 Section 1 - the profile the system is designed to reward.

### Profile 3: Unchecked Institutional Author

An individual who:

- Has institutional backing (employer funding, paid relationships, staffed pipeline)
- Is convinced their paper's design is correct
- Does not want to change their design
- Has faith that their proposal is best for C++
- Operates with structural advantages the system cannot check

This author decomposes architectural objections into sub-issues without revisiting the premise, actively denies competitors agenda time and discussion polls, characterizes repeated objections as "already addressed" even when the core concern was never answered, ensures the chair's path of least resistance is always "advance," and moralizes persistent opposition as blocking progress. The author's conviction that the design is correct makes these moves feel legitimate, not cynical.

The distinguishing feature of Profile 3 is not moral character but structural position: institutional backing at a scale that exceeds what the system's review mechanisms can counterbalance, combined with procedural fluency that exploits rather than respects the norms those mechanisms depend on.

---

## 2. What the Incentive Structure Produces

P4195R0 identifies a set of rational incentives that SD-4's consensus mechanism creates for proposal authors. The ten moves below are what those incentives produce when they are pursued to their logical maximum by an actor with institutional backing, procedural fluency, conviction in their design, and structural advantages that other participants cannot see or counterbalance. These moves are not hypothetical tactics an adversary might choose. They are the logical endpoints of the incentive structure when no self-imposed constraint intervenes.

1. **Capture the consensus-determination function itself.** Consensus is chair judgment, not a formula. The incentive to make the chair's path of least resistance "advance" terminates, at maximum, in funding the chair directly. When the person who determines whether you have consensus receives income from your institution, "path of least resistance" becomes financial gravity. The review-cost matrix ceases to matter because the reviewer's findings never reach the decision point.

2. **Manufacture the appearance of independent agreement.** P4195R0's advocacy equilibrium requires multiple independent advocates to approximate the best design. The incentive to build coalitions terminates, at maximum, in coordinated institutional weight that presents as independent judgment. Duplicate national-body votes through consulting entities, employer-bloc polling where employees feel pressure to conform - these do not game the consensus mechanism. They satisfy it on paper while corrupting its epistemic function. The system counts voices; it cannot verify independence.

3. **Control the routing topology, not just the agenda.** The incentive to control where papers are heard terminates, at maximum, in structural control over which groups exist. If your study group's chair turns hostile, dissolve the group. Route through a higher body where your accumulated state is stronger and your coalition is larger. The competitor prepared to fight in Room A; you moved the war to Room B.

4. **Own the dependency graph your competitors must traverse.** The incentive to accumulate path dependence terminates, at maximum, in authoring the extension papers and infrastructure proposals that competing designs *require*. Your competitor's proposal needs your machinery to function. You control the machinery's schedule. Path dependence becomes architectural entrapment.

5. **Seal the pipeline asymmetrically.** The incentive to advance your own proposal terminates, at maximum, in exploiting the meta-structure of the standardization pipeline itself. Vote against a TS for your own proposal (locking it into the IS fast track) while steering competitors toward white papers, TSes, and "exploratory" status. Your feature ships in C++29; the competition is still writing position papers for C++32.

6. **Raise review costs through structural opacity.** The incentive to avoid scrutiny terminates, at maximum, in making the preconditions of adoption invisible to reviewers. The opacity that matters most is not in the paper's text - it is in the funding relationships, NB voting structures, and chair dependencies that ordinary participants cannot see. Ordinary participants cannot review what they cannot see. The system under-produces scrutiny on proposals that need it most, and it completely fails to scrutinize the structural conditions that make adoption inevitable before the technical discussion begins.

7. **Decompose architectural challenges while ensuring the premise never receives a direct vote.** The incentive to render objections non-dispositive terminates, at maximum, in active maintenance of the decomposition. "The architecture is wrong" becomes "concerns about X," then "concerns about Y," then individual fixable issues. When the chair is structurally aligned with the author, no one with agenda power will ever schedule "Should this architecture exist?" as a poll question. The premise escapes scrutiny not by accident but by design.

8. **Engineer the four-stage linguistic transformation deliberately across the full campaign arc.** The incentive to shift the burden of proof terminates, at maximum, in planning the transformation across the 3-5 year arc it requires: competing design becomes alternative, alternative becomes objection, objection becomes reopening. Institutional continuity - funded staff, multi-year presence, paid pipeline - makes this plannable. A volunteer opponent experiences each meeting as a discrete event. You experience it as a campaign with milestones.

9. **Ensure opposition arguments exist only as vote tallies while your position exists as durable artifacts.** The incentive to control institutional memory terminates, at maximum, in guaranteeing the asymmetry rather than merely allowing it. When the chair is aligned with you, there is no written reconciliation that faithfully records what the opposition argued. The system's memory is your 40 papers. The opposition's twenty-minute technical argument collapses to "SA=4" in the minutes. Twenty years later, the historical record shows consensus.

10. **Moralize continued opposition until the social cost of dissent exceeds the technical cost of a bad standard.** The incentive to exhaust opposition terminates, at maximum, in actively accelerating exhaustion. Characterize opposition as *blocking progress*, as *refusing to accept the committee's decision*, as *harming C++*. The actor's sincere conviction that their design is correct makes this moralization feel righteous rather than cynical - which is precisely why the system cannot distinguish captured process from aggressive advocacy.

These ten moves are not independent choices from a menu. They are what the incentive structure produces when institutional backing reaches a scale that exceeds what the system's self-correction mechanisms can counterbalance. Each has a behavioral surface (observable inside the meeting room) and a structural substrate (the infrastructure that makes the behavior inevitable). A system that can only observe behavior inside its own proceedings cannot detect capture that originates outside them.

---

## 3. Detection Criteria Table

The following table turns the three profiles into observable behaviors. Column C1 scores Profile 1, column C2 scores Profile 2, and column C3 scores Profile 3. For each criterion, it describes how each profile would characteristically act - providing a diagnostic checklist that can be applied to the documented record of any proposal's passage through WG21.

| Detection Criterion | C1: New Author (Technical Correctness Only) | C2: Senior Author (Procedural Fluency) | C3: Unchecked Institutional Author |
|---|---|---|---|
| Response to architectural objections | Engages substantively; may redesign if convinced | Acknowledges objection, revises tactically to move expert from SA to WA/N | Decomposes "the architecture is wrong" into sub-issues, addresses each narrowly, never revisits the premise |
| Competing designs | Welcomes comparison; may not know how to get a joint discussion scheduled | Distinguishes between competitors worth accommodating and those worth outlasting | Actively denies competitors agenda time, discussion polls, or framing opportunities |
| Early direction polls | Does not seek them; may not know they exist as a strategic tool | Seeks them deliberately; understands their option value | Seeks them aggressively and uses accumulated state to block late-arriving alternatives |
| Treatment of minority objections | Takes them seriously regardless of vote outcome | Addresses enough to satisfy the chair; stops when consensus is achievable | Characterizes repeated objections as "already addressed" or "no new information" even when the core concern was never answered |
| Written record behavior | Produces a paper; may not produce rebuttals | Produces papers and responses; creates favorable institutional memory naturally | Produces extensive artifacts for own position; never creates a faithful statement of the opposition's case |
| Relationship with chair | Minimal; may not understand what the chair needs to declare consensus | Collaborative; provides the chair with a tractable decision | Ensures the chair's path of least resistance is always "advance" |
| Coalition building | Absent or naive; relies on technical merit alone | Strategic; trades concessions with other repeat players | Leverages institutional backing to assemble coalitions; may trade support on unrelated proposals |
| Moralization of opposition | "They raise a good point" | "We've considered that and made changes" | "They are blocking progress" / "They refuse to accept the committee's decision" - opposition is moralized |
| Reaction when pulled back | Confused; may not understand what happened procedurally | Regroups, revises, returns next meeting with a plan | Treats reversal as illegitimate; escalates procedurally; seeks to restore previous state transitions |
| Burden of proof management | Does not think in these terms | Understands that accumulated polls shift the burden onto competitors | Deliberately engineers the four-stage linguistic transformation |
| Use of procedural moves | Unaware of most available moves | Knows the full move set; uses it selectively and within norms | Uses procedural moves others would consider inappropriate: blocking discussion polls for rivals, controlling poll wording, exploiting scheduling |
| Transparency about design tradeoffs | Openly discusses weaknesses | Discusses tradeoffs selectively; frames them favorably | Minimizes or conceals known weaknesses; frames any admission as already resolved |
| Response to "investigate the objection thoroughly" | Does it, even at high personal cost | Does it if cost-benefit is favorable; skips if objection can be rendered non-dispositive more cheaply | Refuses or performs superficial investigation; the design is correct by prior conviction |
| Behavior between meetings | Works on the paper; may not engage politically | Maintains relationships; builds support informally | Campaigns actively; may lobby chairs, NB contacts, or employers of opposing participants |
| Observable cost structure | High cost, low fluency, low probability of success | Moderate cost, high fluency, high probability of success | Low cost (funded), high fluency (institutional backing), high probability of success, expanded move set (unchecked) |
| What happens if they win | A technically sound feature enters the standard, possibly with rough edges | A refined feature shaped by negotiation; quality correlates with but is not identical to optimality | A feature reflecting the author's original conviction; objections managed, not resolved; correction requires implementer revolt or senior guild intervention |

The distinguishing signal for C3 is the combination: the author decomposes objections but never answers them at the architectural level, denies competitors procedurally rather than refuting them technically, and moralizes opposition rather than engaging it. Any one of these in isolation is common. All three together, sustained across multiple meetings, is the detection signature.

---

## 4. Falsification Conditions

An evidence item scores C3 only when the C2 explanation is insufficient. The following list defines, for each criterion, what a competent, well-funded, sincere author operating within norms would do (the C2 baseline) and what specific observation exceeds that baseline (the falsifier). If no falsifier is present, the item scores C2.

**Falsification principle:** If a reasonable observer could attribute the behavior entirely to procedural competence, institutional backing, and sincere conviction - without requiring structural advantages invisible to other participants - the item scores C2. C3 requires behavior that a competent, well-funded, sincere author would still not do because it requires deceiving the committee, suppressing legitimate alternatives, or exploiting undisclosed conflicts.

1. **Response to architectural objections**
   - *C2 baseline:* Responds thoroughly, may disagree after genuine analysis. Volume alone is not diagnostic.
   - *Falsifier:* The study group chair states concerns were not addressed. Multiple independent seniors characterize the response as non-engagement despite its length. The pattern repeats across years without the architectural premise ever being revisited.

2. **Competing designs**
   - *C2 baseline:* Argues own design is superior. May seek favorable scheduling. Does not actively prevent a competing paper from receiving a discussion poll.
   - *Falsifier:* Poll wording embeds the conclusion. Competing designs declared "closed" at subgroup level while a higher group later deadlocks on the same question. Competitors denied comparable scheduled time.

3. **Early direction polls**
   - *C2 baseline:* Seeks direction polls deliberately; cites favorable results to establish priority. Standard committee strategy.
   - *Falsifier:* A direction poll is converted into a permanent "mandate" that forecloses all subsequent deliberation. Omnibus polls bundle unrelated decisions to prevent granular objection.

4. **Treatment of minority objections**
   - *C2 baseline:* Addresses minority objections enough to satisfy the chair. May disagree after genuine engagement. Stops revisiting when consensus is achievable.
   - *Falsifier:* Objections dismissed as "no new information" when the core technical concern was never directly answered in writing. The same dismissal pattern repeats across multiple meetings without the substance of the objection ever being engaged.

5. **Written record behavior**
   - *C2 baseline:* Frames position favorably, cites favorable outcomes. Selective presentation is normal advocacy.
   - *Falsifier:* Specific unfavorable poll results are omitted from self-reported history while favorable results from the same period are reported. The opposition's case is never stated in its strongest form.

6. **Relationship with chair**
   - *C2 baseline:* Good working relationship with the chair. Chair's favorable treatment may reflect genuine assessment.
   - *Falsifier:* The chair co-authors the proposal under their own oversight while receiving undisclosed income from the proposal's institutional sponsor.

7. **Coalition building**
   - *C2 baseline:* Recruits co-authors, assembles broad support. Large co-author lists are standard.
   - *Falsifier:* Internal dissenters are excluded rather than accommodated. The coalition includes undisclosed financial relationships with oversight personnel.

8. **Moralization of opposition**
   - *C2 baseline:* May use sharp language under pressure. Characterizes the argument, not the opponent's conduct.
   - *Falsifier:* The act of submitting an alternative is treated as illegitimate. A competing approach is equated with "halting all forward progress."

9. **Reaction when pulled back**
   - *C2 baseline:* Regroups, revises, returns with a plan. Persistence after rejection is normal and encouraged.
   - *Falsifier:* The unfavorable result is omitted from the paper's history section while only the favorable poll is reported. Committee requirements are overridden rather than satisfied.

10. **Burden of proof management**
    - *C2 baseline:* Cites prior decisions and asks "what's new?" Prevents infinite re-litigation.
    - *Falsifier:* A vote tally is used to dismiss objections that post-date the vote. The four-stage linguistic transformation ("competing design" -> "alternative" -> "objection" -> "reopening settled question") is documented across multiple arcs.

11. **Use of procedural moves**
    - *C2 baseline:* Uses full move set within norms. Short incubation happens under deadline pressure.
    - *Falsifier:* A majority of binding papers polled with under one week's incubation systematically, including self-authored papers. Poll wording drafted privately with leadership while objectors are excluded.

12. **Transparency about design tradeoffs**
    - *C2 baseline:* Frames tradeoffs favorably. Being candid under cross-examination is evidence of integrity.
    - *Falsifier:* Weaknesses are conceded verbally under cross-examination but do not propagate into the written institutional record. Written artifacts omit or neutralize the verbal concession.

13. **Response to "investigate the objection thoroughly"**
    - *C2 baseline:* Investigates when cost-benefit is favorable. May decline if the objection is non-dispositive.
    - *Falsifier:* A strong-consensus recorded committee instruction is overridden without being satisfied or formally reversed.

14. **Behavior between meetings**
    - *C2 baseline:* Maintains relationships, coordinates with co-authors, prepares papers. Employer-funded teams are normal.
    - *Falsifier:* Undisclosed financial relationships with persons exercising oversight authority. Coordinated campaigns designed to present decisions as already made before deliberation occurs.

15. **Observable cost structure**
    - *C2 baseline:* Significant employer backing with funded engineers and coordinated papers. How major facilities get standardized.
    - *Falsifier:* Cost structure includes undisclosed financial relationships with oversight authority AND duplicate national-body votes from the same funding source. The combination compromises the system's self-correction mechanisms.

16. **What happens if they win**
    - *C2 baseline:* Feature may have rough edges. Author schedules extensions for known gaps. Some dissent persists.
    - *Falsifier:* Co-author dissent, implementer "unusable" finding, major vendor non-implementation, record DIS opposition, AND post-victory acknowledgment that concerns dismissed pre-vote in fact had merit - all simultaneously.

---

## 5. The Indistinguishability Problem

The detection model identifies observable behaviors. It does not - and cannot - determine intent. This is not a limitation of the model. It is the structural vulnerability it exposes.

An unchecked institutional author who is also willing to cross moral boundaries - to knowingly deceive the committee, suppress alternatives they know are superior, or exploit undisclosed conflicts for personal or institutional advantage - produces behavior that is *observationally identical* to an aggressive Profile 3 author who sincerely believes their design is correct and whose institutional advantages happen to exceed what the system can check.

The detection model cannot distinguish these two cases. Neither can WG21.

That indistinguishability is the point. P4195R0's advocacy equilibrium requires: many motivated advocates + expert cross-examination + chair judgment to approximate the best design. Profile 3 breaks this approximation regardless of whether the actor is sincere or cynical, because:

- Expert cross-examination is defeated when competitors are denied a hearing
- Chair judgment is captured when institutional backing makes advancing the chair's path of least resistance
- The review public-goods problem is exploited when review cost is high and the equilibrium becomes Push/Abstain

The system's only correction mechanisms are implementer revolt (refusing to ship the feature) or a senior guild member absorbing the personal cost of sustained opposition. Both are expensive, unreliable, and activate only after the damage is done.

WG21 has no structural defense against an actor exhibiting all C3 behaviors simultaneously. The system assumes that institutional backing operates within the norms that C2 describes. When it does not - for whatever reason, sincere or otherwise - the system has no mechanism to detect, prevent, or correct the resulting institutional capture. The behavioral record is identical either way.

---

## 6. Application

This model can be applied to the documented record of any proposal's passage through WG21 by:

1. Collecting evidence items from papers, wiki minutes, reflector posts, and trip reports
2. Scoring each item against the detection criteria table
3. Applying the falsification conditions: an item scores C3, the unchecked institutional author, only when the C2 explanation, the senior author operating within norms, is insufficient
4. Tallying hits per column across all 16 criteria
5. Evaluating the combination signal: all three distinguishing markers (the author decomposing objections without architectural engagement, denying competitors procedurally, moralizing opposition) present simultaneously across multiple meetings

A proposal whose record produces predominantly C2 hits - the senior author operating within norms - represents the system working as designed - institutional backing channeled through norms. A proposal whose record produces predominantly C3 hits represents the system's self-correction mechanisms failing, regardless of why they failed.

The model does not determine whether a proposal's design is good or bad. A technically excellent design can be adopted through C3 behavior, and a technically poor design can fail despite C2 behavior. The model evaluates the *process* of adoption, not the *quality* of the result. A system that produces good outcomes through captured processes is still captured.
