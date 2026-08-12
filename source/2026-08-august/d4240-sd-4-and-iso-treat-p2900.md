---
title: "Did ISO or SD-4 Govern the P2900 Ballot?"
document: P4240R0
date: 2026-08-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Internal committee rules were presented to ballot participants as if they carried ISO force.

P3846R1 quotes SD-4: "we do not significantly delay progress on concrete proposals in order to wait for alternative proposals we might get in the future." The ISO/IEC Directives say: consensus is "a process that involves seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments." These are not two readings of one rulebook. They are two rule sets operating at different levels: the Directives govern the SC-level ballot (2.5.6, 2.6.2, 2.6.5) where National Body comments live, while SD-4 governs WG21-internal practice and has no ISO procedural standing.

The dates frame the question: strong consensus was declared at Hagenberg in February 2025, the National Body objections arrived at the October 2025 ballot, and the twenty-two-author defense was finalized five days after the ballot closed - a reconciliation that followed the decision rather than producing it.

Nineteen of twenty-six National Bodies filed comments on P2900. Spain, the United States, France, and Finland requested removal. This paper applies each rule set, at its own level, to the same NB comment phase and documents what each produces. One requires reconciliation. The other provides a mechanism for dismissal. Both are publicly available. The comparison is systematic.

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper asks for nothing.

---

## 2. What P2900 Achieved

SG21 spent five years gathering use cases<sup>[1]</sup>, exploring the design space, and refining the proposal before forwarding it to EWG, where it was examined for another year. [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2900r14.html)<sup>[2]</sup> was adopted with strong consensus<sup>[3]</sup> into the C++26 working draft at Hagenberg in February 2025. Complete implementations exist in publicly available forks of GCC and Clang<sup>[4]</sup>. The implementers reported P2900's specification as "clear and implementable."

P3846R1<sup>[5]</sup> addresses eighteen concerns raised in NB comments and opposition papers. It carries twenty-two co-authors, including implementers from GCC and Clang, static analysis vendors, library authors, and committee veterans. Each concern receives a structured treatment: summary, discussion status, response, and detailed analysis with citations. The paper is thorough, systematic, and represents the largest coordinated defense of a single feature in WG21's published record.

The quality of the technical work and the depth of the procedural defense are not in question. What is in question is which rule set operates at which level: the ISO Directives govern the SC-level ballot where NB comments live, while SD-4 governs WG21-internal practice and carries no ISO procedural standing at the ballot.

---

## 3. The Quote

Doumler et al. write in P3846R1<sup>[5]</sup>, Concern 15:

> Procedurally, delaying the standardisation of P2900 due the concerns of [P3829R0] about interactions with hypothetical proposals would be against WG21 practice. According to [SD4], 'we do not significantly delay progress on concrete proposals in order to wait for alternative proposals we might get in the future'.

P3846R1 invokes this principle to argue that P3829R0's<sup>[6]</sup> concerns about P2900's interactions with deep const and generic decorators cannot justify delay. The principle is cited as settled WG21 practice.

---

## 4. What the Principle Says

SD-4<sup>[7]</sup> states, under "Delay vs. bird in the hand":

> We cannot act on ideas without papers, and we do not significantly delay progress on concrete proposals in order to wait for alternative proposals we might get in the future. If we have an active proposal that is making progress, and an objection is raised that a different competing approach would be better but that other approach does not yet have a paper, the EWG or LEWG subgroup chair may elect to delay the progress of the active proposal by one meeting to give the objector(s) opportunity to bring an on-time proposal paper. Otherwise, if a competing alternative does not have a paper, it does not exist and will not block progress of a proposal that we do have before us.

A following paragraph extends the same logic to the TS-to-IS pipeline:

> If by the time the TS is ready to be considered for merging into the IS we do not have alternative proposals actively progressing, the default action is to move forward with the proposal we have, we will not wait indefinitely for something better.

The principle establishes structural priority for first-movers. The concrete proposal advances. The alternative that has not materialized as a paper does not procedurally exist. The chair may grant a one-meeting delay. Beyond that, the incumbent proceeds.

This principle was deployed during the P2900 ballot. On 2025-10-23, Nevin Liber quoted it on the SG15 mailing list, asking opponents: "What is the paper number of the proposal of the contract feature which the C++26 CD is blocking later adoption of?"<sup>[8]</sup> John Spicer responded that the bird-in-hand principle does not apply "when the feature in hand is itself harmful," citing P3829R0 and P3835R0 as new technical information<sup>[9]</sup>. Spicer also noted historical precedent: C++0x concepts were pulled in 2009 and not replaced until 2017; contracts were removed from C++20 in 2019 without a replacement<sup>[10]</sup>.

---

## 5. What the ISO Directives Say at the Ballot

The ISO/IEC Directives, Part 1<sup>[11]</sup> contain no first-mover doctrine. No provision anywhere in the Directives establishes priority based on order of arrival, revision count, or accumulated procedural momentum.

The Directives define consensus (Clause 2.5.6):

> General agreement, characterized by the absence of sustained opposition to substantial issues by any important part of the concerned interests and by a process that involves seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments.

Seven properties of this system bear on the P2900 NB comment phase:

**1. Consensus requires reconciliation.** The definition is not "absence of opposition." It is "absence of sustained opposition" achieved through "a process that involves seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments" (Clause 2.5.6)<sup>[11]</sup>. The reconciliation obligation is structural, not optional.

**2. Negative votes require technical comments.** A P-member voting negative must provide technical reasons (Clause 2.6.2)<sup>[11]</sup>. The Directives do not restrict the content of technical comments. No category of ballot comment is declared "not appropriate."

**3. Every comment must be addressed.** The Consolidated JTC 1 Supplement requires committees "to respond to all comments received" (Clause 2.6.5)<sup>[11]</sup>, and the ISO/IEC Directives, Part 1 direct that "every attempt shall be made to resolve negative votes." The obligation is on the project, not on the objector.

**4. Disagreement triggers mandatory discussion.** If two or more P-members disagree with the chair's decision on comment disposition, discussion at a meeting is required (Clause 2.6.5)<sup>[11]</sup>.

**5. Objection carries no credibility penalty.** The Directives treat objection as information, not disruption. Those with sustained opposition are explicitly directed to the appeals process (Clause 2.5.6)<sup>[11]</sup>. No Directive provision states that repeated objection "erodes credibility."

**6. The appeal chain provides a credible outside option.** National Bodies may appeal any action or inaction to the parent TC, TMB, or council board within eight weeks (Clause 5.1)<sup>[11]</sup>. The existence of the appeal chain disciplines the inside game without being exercised.

**7. No first-mover doctrine.** The Directives contain no equivalent of SD-4's "bird in the hand." A competing or alternative approach receives the same procedural access as the incumbent. The system selects for designs that reconcile conflicting arguments, not designs that arrived first.

Two clarifications keep this honest. These are duties of process, not of outcome: 2.5.6 and the comment-resolution obligation require that objecting views be sought and addressed, not that they prevail or that a decision be reversed. A comment can be fully addressed and then rejected on the merits. That is exactly why sequence matters. The duty to respond to comments (2.6.5) can be discharged after the ballot; the duty to form consensus by reconciliation (2.5.6) cannot be discharged by a defense assembled after the consensus has already been declared.

---

## 6. The Sequence

The order in which events occurred is itself evidence. The consensus was declared before the objections existed, and the defense was finalized before the objections could be reconciled.

| Date | Event |
|---|---|
| February 2025 | P2900R14 adopted into the C++26 working draft at Hagenberg, "with strong consensus"<sup>[3]</sup>. |
| 2025-10-01 | The C++26 CD ballot closes. Nineteen of twenty-six National Bodies comment; Spain, the United States, France, and Finland request removal<sup>[12]</sup><sup>[13]</sup>. |
| 2025-10-02 to 27 | On the public SG15 list, the P3835 mixed-mode thread runs for roughly 298 messages across twenty-five days<sup>[17]</sup>. No position is conceded and no resolution is recorded; the mixed-mode concerns remain open at thread end. |
| 2025-10-06 | P3846R0, the twenty-two-author defense answering the recurring concerns, is published - five days after the ballot closed, four days into the live SG15 debate<sup>[16]</sup>. |
| 2025-11-03 | P3846R1 follows with minor edits<sup>[5]</sup>. |
| March 2026 | EWG confirms contracts in the C++26 CD at Croydon<sup>[15]</sup>. |

Two intervals carry the argument.

**Eight months.** The "strong consensus" at Hagenberg predates the National Body objections by eight months. Under the Directives, consensus is "a process that involves seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments" (2.5.6)<sup>[11]</sup>. A consensus declared before the objecting views existed cannot have been formed by reconciling them.

**Five days.** The twenty-two-author defense was finalized on 2025-10-06, five days after the ballot closed and while the SG15 mixed-mode debate was still live. A coordinated response to nineteen National Bodies' collated comments, structured concern by concern, cannot be assembled from those comments in five days; its substance must largely predate them. P3846R0's own abstract confirms the position: "Almost all objections are repetitions of those raised in earlier papers"<sup>[16]</sup>. The defense was not a reconciliation of the ballot comments. It was a restatement of positions held before the ballot.

One counter is that the concerns genuinely were repetitions, so a fast restatement is legitimate rather than evasive. The public record answers it. P3829R0, "Contracts Do Not Belong in the Language," and P3835R0 were presented as new technical information during the ballot period<sup>[6]</sup><sup>[9]</sup>, and the SG15 mixed-mode thread was still unresolved on 2025-10-27<sup>[17]</sup> - three weeks after P3846R0 was finalized. A defense dated 2025-10-06 cannot have reconciled a technical dispute that was still open on 2025-10-27. Turnaround alone is circumstantial; turnaround plus a live, unreconciled concern is the finding.

---

## 7. The Same NB Comments, Two Systems

The C++26 Committee Draft ballot closed on 2025-10-01. N5028<sup>[12]</sup> records the official collated comments. Nineteen of twenty-six P-member National Bodies responded: Austria, Brazil, Bulgaria, Canada, China, Czech Republic, Finland, France, Germany, Italy, Netherlands, Poland, Romania, Russia, Spain, Sweden, Switzerland, United Kingdom, and the United States<sup>[13]</sup>.

Of these nineteen, the following filed comments requesting removal of P2900 from the C++26 working draft: Spain (ES-049, ES-050), the United States (US-051, US-052), France (FR-053, FR-054), and Finland (FI-071). Romania (RO-056) requested removing the "ignore" semantic or removing contracts entirely<sup>[13]</sup>.

Ville Voutilainen, a co-author of P2900, characterized the response in P4009R0<sup>[14]</sup>: "We have never had this much and this strong opposition to a feature in a DIS."

P3846R1<sup>[5]</sup> addresses these comments across eighteen structured sections. Each section includes a "Discussion Status" subsection. In the portions of P3846R1 the author was able to verify, the phrase "No new information has been presented since" appears eight times. Other Discussion Status sections conclude with "no concerns raised by that group" or equivalent language indicating prior resolution. P3846R1's abstract states: "Almost all objections are repetitions of those raised in earlier papers, addressed in subsequent responses, and extensively discussed in EWG."

EWG confirmed contracts in the C++26 CD at Croydon in March 2026<sup>[15]</sup>.

| Procedural Event | SD-4 Treatment | ISO Directives Treatment |
|---|---|---|
| P2900 adopted at Hagenberg with strong consensus (February 2025) | Directional consensus declared. Reversing it is procedurally near-impossible: ballot comments that revisit past decisions are "not appropriate" (SD-4)<sup>[7]</sup> | Consensus requires ongoing reconciliation of conflicting arguments (2.5.6)<sup>[11]</sup>. NB ballot comments may raise any technical concern (2.6.2)<sup>[11]</sup> |
| 19 of 26 NBs file comments; 5 request removal | Concerns are "repetitions of those raised in earlier papers" (P3846R1)<sup>[5]</sup>. "No new information has been presented since" (P3846R1)<sup>[5]</sup> | Committees are required to "respond to all comments received" (2.6.5)<sup>[11]</sup>. The obligation is on the project |
| Opponents lack a complete alternative proposal | "If a competing alternative does not have a paper, it does not exist" (SD-4)<sup>[7]</sup>. Liber: "What is the paper number?"<sup>[8]</sup> | No first-mover doctrine exists. The Directives contain no provision that conditions procedural standing on having a replacement ready |
| Objectors escalate repeatedly | Repeated escalation "erodes credibility" (SD-4)<sup>[7]</sup> | Objection carries no credibility penalty. Objectors are directed to the appeals process (2.5.6)<sup>[11]</sup> |
| Concerns were previously discussed in SG21 and EWG | Prior discussion satisfies procedural due diligence. "These concerns have been heard and considered, and they have been at each stage in the past" (P3846R1)<sup>[5]</sup> | Prior discussion does not extinguish NB ballot comment rights. Comments must be addressed (2.6.5)<sup>[11]</sup>. If 2+ P-members disagree with disposition, meeting discussion is required (2.6.5)<sup>[11]</sup> |
| A co-author of P2900 writes: "We have never had this much and this strong opposition to a feature in a DIS" (P4009R0)<sup>[14]</sup> | The level of opposition does not alter the procedural outcome. The concrete proposal has a paper. Alternatives do not. The proposal advances | The level of opposition is itself a signal. "Sustained opposition to substantial issues by any important part of the concerned interests" is the definitional boundary of consensus (2.5.6)<sup>[11]</sup> |

### 7.1 "Not Appropriate" Belongs to a Different Level

SD-4's claim that a repeat ballot comment is "not appropriate" echoes real ISO language, but from the wrong level. Effective 1 January 2014, JTC 1 Resolution 30A rewrote clause 1.12 of the Consolidated JTC 1 Supplement so that working groups are composed of individual experts acting in a personal capacity, not National Body delegations<sup>[18]</sup>. The accompanying JTC 1 Secretariat communication drew the line explicitly: National Body contributions "are not appropriate at the WG level and should not be accepted," and, once the working group elevates a draft to committee draft, "National Body input ... will be sought"<sup>[18]</sup>.

That is the inversion SD-4 performs. The "not appropriate" principle governs National Body input inside the working group, where experts, not delegations, do the work. SD-4 redirects it at the SC-level ballot - the one stage the same rule reserves for National Bodies. The level where NB input is not appropriate is the WG; the level where it is the reserved channel is the ballot. SD-4 aims the first rule at the second stage.

The 2014 rewrite was JTC 1 aligning to the model the rest of ISO/IEC already used, not a fresh restriction. The point is not that the rule is new. It is that the rule has a level, and SD-4 applies it at the wrong one.

---

## 8. The Chain

The table in Section 7 treats each mechanism in isolation. The finding is that P3846R1 relies on no single one; it chains them, and the order compounds their effect. Each link is individually cited and individually reasonable.

1. **Bird-in-hand** gives the incumbent structural priority: an alternative without a paper "does not exist"<sup>[7]</sup>. Invoked at Concern 15<sup>[5]</sup>.
2. **Prior consideration** reclassifies the ballot comments as repetitions: "No new information has been presented since," eight times<sup>[5]</sup>.
3. **Consensus ratchet** makes the Hagenberg decision hard to reverse: comments that revisit it are "not appropriate"<sup>[7]</sup>. The NB comments arrive after the ratchet has engaged.
4. **Credibility cost** makes persistence expensive: repeated escalation "erodes credibility"<sup>[7]</sup>.
5. **No feedback loop**: no procedure asks, after adoption, whether the decision was correct. P3846R1 defends what was decided; nothing requires re-examining it.

None is unreasonable alone. Together they form a system that cannot be moved from inside: bird-in-hand gives the incumbent priority, prior consideration reclassifies objection as repetition, the consensus ratchet makes the decision irreversible, the credibility cost penalizes objection, and the absence of a feedback loop closes the system.

The ISO Directives supply countermeasures where they have jurisdiction - the SC-level ballot. The duty to respond to every comment answers prior consideration (2.6.5)<sup>[11]</sup>. Unrestricted ballot comments answer the consensus ratchet (2.6.2)<sup>[11]</sup>. Protected objection and the appeal path answer the credibility cost (2.5.6, 5.1.2)<sup>[11]</sup>. Bird-in-hand operates entirely inside WG21, where the Directives specify no rules; its only counterweight is that nothing decided under it carries ISO standing until the ballot.

---

## 9. Conclusion

One system asks the proposal author to reconcile conflicting arguments. The other asks the objector for a paper number.

The dates make the point concrete. Consensus was declared in February, the objections arrived in October, and the defense was finalized five days after the ballot closed while the technical dispute was still live. Reconciliation, in the sense the Directives require, would have had to come first.

Both rule sets are real, and they operate at different levels. SD-4 governs WG21-internal practice; within the committee room it functions as designed, and nothing in the ISO Directives forbids it. The Directives govern the SC-level ballot, where National Body comments live and where the only decisions with ISO standing are made. SD-4 cannot bind National Bodies, cannot categorize their ballot comments, and carries no procedural weight at the stage where the comment-resolution obligations of 2.6.5 apply. The P2900 comment phase shows what happens when the first set of rules is presented to participants as if it operated at the second level.

---

## References

[1] [P1995R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1995r1.html) - "Contracts - Use Cases" (Timur Doumler, Joshua Berne, 2020).

[2] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2900r14.html) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andr&eacute; Maurer, 2024).

[3] [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf) - "2025-02 Hagenberg Meeting Minutes" (Nina Dinka Ranns, 2025).

[4] [P3460R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3460r0.html) - "Contracts Implementation Report" (Timur Doumler, 2024).

[5] [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, Peter Bindels, Peter Dimov, Louis Dionne, Eric Fiselier, Mungo Gill, Pablo Halpern, Tom Honermann, Corentin Jabot, John Lakos, Nevin Liber, Lisa Lippincott, Ryan McDougall, Jason Merrill, Roger Orr, Nina Dinka Ranns, Ren&eacute; Ferdinand Rivera Morell, Oliver Rosten, Iain Sandoe, Hui Xie, 2025).

[6] [P3829R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3829r0.pdf) - "Contracts Do Not Belong in the Language" (David Chisnall, John Spicer, Ville Voutilainen, Gabriel Dos Reis, Carlos Garcia Sanchez, 2025).

[7] [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Guy Davidson, 2026).

[8] Nevin Liber on the SG15 mailing list, 2025-10-23. [https://lists.isocpp.org/sg15/2025/10/2933.php](https://lists.isocpp.org/sg15/2025/10/2933.php)

[9] John Spicer on the SG15 mailing list, 2025-10-23. [https://lists.isocpp.org/sg15/2025/10/2936.php](https://lists.isocpp.org/sg15/2025/10/2936.php)

[10] John Spicer on the SG15 mailing list, 2025-10-23. [https://lists.isocpp.org/sg15/2025/10/2931.php](https://lists.isocpp.org/sg15/2025/10/2931.php)

[11] ISO/IEC. "ISO/IEC Directives, Part 1 - Consolidated JTC 1 Supplement." 2023. [https://jtc1info.org/wp-content/uploads/2023/11/ISO-IEC-Consolidated-JTC-1-Supplement-2023.pdf](https://jtc1info.org/wp-content/uploads/2023/11/ISO-IEC-Consolidated-JTC-1-Supplement-2023.pdf)

[12] [N5028](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5028.pdf) - "C++26 CD Collated Comments" (2025).

[13] Arthur O'Dwyer. "The C++26 NB comments have arrived." 2025-10-12. [https://quuxplusone.github.io/blog/2025/10/12/nb-comments/](https://quuxplusone.github.io/blog/2025/10/12/nb-comments/)

[14] [P4009R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4009r0.html) - "A Proposal for Solving All of the Contracts Concerns" (Ville Voutilainen, 2026).

[15] [cplusplus/papers Issue #2455](https://github.com/cplusplus/papers/issues/2455) - P3846R1 tracking issue, closed March 2026.

[16] [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, et al., 2025-10-06). The twenty-two-author defense, published five days after the C++26 CD ballot closed.

[17] P3835 discussion thread, SG15 mailing list (public archive), 2025-10-02 to 2025-10-27. [https://lists.isocpp.org/sg15/2025/10/2637.php](https://lists.isocpp.org/sg15/2025/10/2637.php)

[18] ISO/IEC JTC 1 N12032 / SC22 N4919 - "Communication from the JTC 1 Chair and Secretariat regarding new text for clause 1.12 of the Consolidated JTC 1 Supplement 2014 concerning WG participation" (2014-04-17). Enacted by JTC 1 Resolution 30A, effective 1 January 2014. [https://wg5-fortran.org/N2001-N2050/N2032.pdf](https://wg5-fortran.org/N2001-N2050/N2032.pdf)
