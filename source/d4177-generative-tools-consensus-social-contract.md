---
title: "Info: Generative Tools and the Social Contract of Consensus Standards"
document: P4177R0
date: 2026-04-02
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
audience: WG21
---

## Abstract

Generative tools meet consensus standardization first as a problem of trust and provenance, not only as a problem of technical correctness.

This paper begins from a personal observation in a public C++ discussion venue, then places the resulting questions against published institutional theory and against WG21's own recent documentary record. It restates six forces already collected in D4171R0, derives six conditional predictions at the interface between generative tools and consensus practice, and supplies a partially filled observation table with intentional empty cells. The empty cells are an invitation to the record, not an accusation.

---

## Revision History

### R0: April 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the [C++ Alliance](https://cppalliance.org/)<sup>[1]</sup> and maintains proposals in the `std::execution` and coroutine I/O design space. The author has attended WG21 meetings since 2018. This paper documents how consensus institutions process novelty in authorship and tooling. The same institutional forces apply whether the reader welcomes generative tools, rejects them, or sits undecided.

The author has used generative tools in drafting and revision of technical work, including assistance with routine prose in this paper. The substantive judgments, structure, and claims remain the author's responsibility.

The author asks for nothing.

---

## 2. Why this paper exists

In a public C++ chat venue whose operators state that many participants are implementers, WG21 members, and paper authors, the author watched a conversation turn quickly toward provenance when synthetic or tool-assisted material was disclosed. Technical content that would ordinarily draw design questions instead drew questions about how the text was produced. The pattern was familiar from committee culture, but the speed and the temperature of the shift caught the author's attention.

That observation is not evidence of how WG21 will vote. Informal chat is not a sample of a plenary. It is not a measure of implementer opinion across the ecosystem. It is simply the reason the author opened the books again.

**The thread was a question, not a verdict.**

---

## 3. Act 1 - What consensus work already asks of people

Consensus standardization is a remarkable human achievement. It produces portable specifications under competing interests, finite attention, and genuine uncertainty. The committee's craft - reading papers, running polls, reconciling national body comments, preserving continuity across releases - is difficult work done mostly by volunteers and specialists who care about the language. Nothing in this paper is offered to diminish that craft.

Generative tools still land awkwardly inside the social system that craft built.

### 3.1 Legitimacy, trust, and cost

Deliberative legitimacy rests on reasons that participants can examine. In a large body, full independent review of every claim is impossible. Members reasonably lean on authorship reputation, coalition signals, prior polls, and the procedural history of a proposal. Those shortcuts are not laziness. They are how humans scale cooperation.

They also mean that **provenance is never a neutral footnote**. When a reader cannot place a paragraph in a known human trajectory - apprenticeship in the community, a track record of shipped work, a face in the room - the paragraph enters through a different gate. The gate is social before it is technical.

That is uncomfortable. It is still predictable.

### 3.2 Six forces (from the permanent record)

[D4171R0](https://wg21.link/d4171r0)<sup>[2]</sup> collects six documented forces from six disciplines that act on consensus-driven institutions. The full exposition and primary citations live there. This paper uses only the names and the intuition:

| Force                      | Short intuition                                                                 |
| -------------------------- | --------------------------------------------------------------------------------- |
| Goal displacement          | Procedure becomes easier to reward than outcomes.                               |
| Professional socialization | Newcomers learn what "serious" means from the community they join.              |
| Representational capture   | Who shows up shapes what gets built.                                            |
| Iron law                   | Navigation of internal process becomes a competitive skill.                       |
| Shifting baseline            | Each cohort calibrates "normal" against what it inherited.                        |
| Going native                 | Sustained peer deliberation moves preferences toward institutional frames.      |

Generative tools do not erase those forces. They press on them. A tool that can produce fluent technical prose in seconds changes the relative cost of drafting, review, suspicion, and disclosure. The institution still runs on trust.

**Trust scales; attention does not.**

---

## 4. Act 2 - Six conditional predictions

Each prediction below is conditional. It says what the author expects to observe **if** the forces in Section 3.2 apply to WG21's social system as they apply to other consensus bodies. Each prediction is paired with a disconfirmation - a pattern that would show the model is wrong or incomplete.

The predictions are guesses about incentives and observable signals in public artifacts and public speech.

### 4.1 From goal displacement

**Prediction A.** Formal rules and standing documents about document format, copyright, and tool use will receive sustained attention even while technical disagreement about a feature continues. Observers will sometimes argue procedure when substantive resolution feels costly.

**Disconfirmation.** Procedure rarely appears in public debate about generative tools; only technical merits are discussed.

### 4.2 From professional socialization

**Prediction B.** Long-tenured participants and newcomers will use different language to evaluate tool-assisted papers - "process," "serious," "respect for the room" on one side; "shipping evidence," "field experience," "implementation cost" on the other. The same split will appear around AI that appeared around other flashpoints.

**Disconfirmation.** Homogeneous vocabulary across tenure levels in published statements.

### 4.3 From representational capture

**Prediction C.** Public debate about generative tools will overrepresent participants whose employers fund standards engagement and underrepresent developers who consume the standard but never travel to a meeting.

**Disconfirmation.** Documented participation in the debate proportional to the global developer population.

### 4.4 From the iron law

**Prediction D.** Authors and coalitions skilled at navigating document requirements and mailing norms will adapt faster than isolated contributors, independent of the underlying technical quality of their engineering.

**Disconfirmation.** Adoption of tool-assisted workflows spreads evenly across resource levels with no correlation to procedural experience.

### 4.5 From shifting baseline syndrome

**Prediction E.** What counts as "normal authorship" will drift across cohorts. Participants who entered before wide tool use will apply a different default than participants whose professional lives always included assistants.

**Disconfirmation.** Stable, cohort-independent definitions of authorship in public statements over several years.

### 4.6 From going native

**Prediction F.** Participants whose careers are tied to committee standing will internalize institutional discomfort with opaque provenance and will express that discomfort as personal priority, not only as institutional compliance.

**Disconfirmation.** No correlation between career embedding in the committee process and public intensity of provenance concern.

---

## 5. Strong objections, stated fairly

**Objection 1 - "You are calling skeptics backward."**  
Reasonable skeptics fear noise, misattribution, and unequal access to powerful tools. Those fears deserve respect. The predictions above describe incentives and history.

**Objection 2 - "Informal chat should not appear in a committee paper."**  
Agreed as proof. Section 2 is motivation only. The table in Section 6 relies on published sources or honest blanks.

**Objection 3 - "The committee only needs technical criteria."**  
Technical criteria remain necessary. They are not sufficient for how humans actually read under time pressure. The gap is the subject here.

---

## 6. Act 3 - Observation table (partial, intentional gaps)

The table is the spine. Empty cells are deliberate. They mark questions the mailing may answer next.

| Prediction | Expected public signal | Observed to date (dated source) | Property of a healthy practice (not ranked) | Open |
| ---------- | ---------------------- | -------------------------------- | -------------------------------------------- | ---- |
| A | Updates to standing documents; procedural debate alongside technical debate | [P3702R1](https://wg21.link/p3702r1)<sup>[3]</sup> (2025-08-14) quotes ISO guidance: do not use generative images or text in ISO content; WG21 submission rules moving toward alignment | Disclosure that matches actual risk; human accountability for claims | Whether draft assistance without publication of raw model output satisfies evolving norms |
| B | Split vocabulary in papers and polls | [P3962R0](https://wg21.link/p3962r0)<sup>[4]</sup> (2026) documents implementers describing outcome feedback reframed as obstruction; [P2138R4](https://wg21.link/p2138r4)<sup>[5]</sup> (2021) deployment gate failed LEWG poll per [P2435R0](https://wg21.link/p2435r0)<sup>[6]</sup> | Same respect for implementation cost whether the author used tools or not | Tool disclosure as substitute for or supplement to technical engagement |
| C | Affiliation-skewed participation in debate | (no published affiliation census located for this row) | Invite voices without travel budgets into written record | |
| D | Faster adaptation by resourced coalitions | | Pair procedural help for newcomers with clear, written guidance | |
| E | Cohort drift in "normal authorship" | | Teachable norms anchored in examples, not nostalgia | |
| F | Embedded participants echo institutional provenance priority | | Separate institutional compliance from personal stigma toward individuals | |

The author repeats: informal observation motivated the paper. It does not fill the table.

---

## 7. Properties of possible responses (no ranking)

Different communities will adopt different bundles. The following properties are described side by side without recommendation.

| Property | Provides | Costs |
| -------- | -------- | ----- |
| Strict prohibition of generative text in submitted papers | Clear bright line for reviewers | Drafting burden; edge cases in grammar tools and translation assistance |
| Disclosure of tool use in paper metadata | Transparency; reduces guessing games | Disclosure can dominate discussion if readers skip technical content |
| Blinded review of technical claims independent of provenance | Focus on mathematics and wording | Hard to operate in a public mailing culture |
| Heavy reliance on implementation and deployment evidence | Grounds decisions in user-visible outcomes | Slower cycles; burdens implementers |

The reader chooses the tradeoffs. The paper does not choose for them.

---

## 8. Conclusion

The committee is not a model zoo. It is a room full of people who carry reputations, friendships, grudges, and pride in craft. Generative tools enter that room as a question about **whose voice** the reader hears. That question arrives before the reader finishes the technical paragraph.

If the predictions misfire, the table will show it. If they land, the cost is still measured in **patience** with one another, not in victory over a model.

**We can disagree about tools and still recognize the same humanity across the aisle.**

---

## 9. Acknowledgements

The author thanks every committee member who has ever explained a procedural rule patiently to a newcomer; that labor is easy to overlook and hard to forget.

---

## References

1. [C++ Alliance](https://cppalliance.org/) - nonprofit supporting C++ open-source libraries and standards engagement. https://cppalliance.org/

2. [D4171R0](https://wg21.link/d4171r0) - Vinnie Falco. "Info: Institutional-Theory Predictions About Standards Bodies." 2026-03-30. https://wg21.link/d4171r0

3. [P3702R1](https://wg21.link/p3702r1) - Jan Schultke. "Stricter requirements for document submissions (SD-7)." 2025-08-14. https://wg21.link/p3702r1

4. [P3962R0](https://wg21.link/p3962r0) - Nina Ranns et al. "Implementation reality of WG21 standardization." 2026. https://wg21.link/p3962r0

5. [P2138R4](https://wg21.link/p2138r4) - Ville Voutilainen. "Rules of Design and Specification engagement." 2021. https://wg21.link/p2138r4

6. [P2435R0](https://wg21.link/p2435r0) - Bryce Adelstein Lelbach. "2021 Summer Library Evolution Poll Outcomes." 2021. https://wg21.link/p2435r0
