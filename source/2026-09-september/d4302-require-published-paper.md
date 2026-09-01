---
title: "Any Delegate May Object to a Poll on an Unmailed Revision"
document: P4302R2
date: 2026-09-10
intent: ask
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

WG21 sometimes records polls on paper revisions that did not appear in a pre-meeting mailing. When an in-meeting revision changes the design, recording the poll can shift the consensus burden before national body experts have seen the change. This paper proposes that, before such a poll is recorded, the chair ask whether anyone objects; one objection keeps the tally out of the minutes while allowing discussion, an informal poll, and a qualitative record. A narrow final-meeting exception permits wording corrections and feature removal when waiting would cost a release.

## Revision History

### R1: August 2026

- Replaced R0's flat prohibition with an objection right. An unmailed revision may receive a recorded poll when nobody objects.
- Reorganized the rationale around the shift in consensus burden caused by adopting an unmailed design change, and added the supporting SD-4 consensus-threshold citation.
- Stated the cost of deferral directly, including repeated review, schedule pressure, and the risk of missing a release train.
- Confined the final-meeting exception to defined wording corrections and a separate feature-removal case, while acknowledging the limited chair judgment the exception requires.
- Corrected the Brno account. P3100R7 was published in the 2026-07 mailing; the relevant fact is that no mailing contained R7 on the date of the 2026-06-10 poll.
- Moved supporting cases to an appendix, removed speculative objections and rebuttals, and shortened the paper throughout.

### R0: July 2026 (post-Brno mailing)

- Initial version.

## 1. The Problem

The pre-meeting mailing gives national body experts time to review the papers WG21 will decide.<sup>[5]</sup><sup>[6]</sup> An in-meeting revision can improve a proposal by incorporating early feedback, correcting wording, or resolving a choice among alternatives. The problem arises when the committee records a poll on that new revision before the wider review chain has seen it. Delegates who prepared from the mailing then prepared against text other than the text being decided.

At the March 2026 Croydon meeting, six of the nineteen papers I had prepared in my areas changed during the week. Some changes were necessary wording corrections. Others recorded design decisions or changed public interfaces. The proposed rule does not restrict early feedback or in-meeting revision. It gives any participant a way to keep a counted result from becoming committee precedent until the revision has appeared in a mailing.

## 2. An Unmailed Change Flips the Consensus Burden

SD-4 states the normal threshold: "A proposal normally advances if there are more than twice as many in favor of a proposal as against."<sup>[5]</sup> That threshold makes the timing of a design change consequential.

Suppose an option first appears in an in-meeting revision and the group forwards it. A stakeholder may have reviewed the mailed paper, seen no such option, and not attended the meeting. That stakeholder must later assemble the consensus needed to remove the option, because the option has become the status quo. Had the option waited for the next mailing, those seeking to add it would have carried the consensus burden. The same disagreement can therefore resolve in opposite directions depending only on whether the change entered before or after national body review.

A "forward with the following changes" poll can have the same effect. If the specified changes include a design decision absent from every mailed revision, the recorded poll establishes that decision before the wider review chain has seen it. Requiring one mailed revision before a tally becomes part of the record keeps the burden on those proposing the change.

## 3. The Rule

Before taking a poll on a paper revision that did not appear in a pre-meeting mailing, the chair asks whether any participant objects to recording the poll. If anyone objects, no tally enters the record. The group may still discuss the revision, take an informal poll, and minute the direction of sentiment.

Mailing status is easy to verify. In the ordinary case, the revision was mailed and the chair proceeds normally. If it was not mailed, the chair asks the question and does not require the objector to defend a technical position. Objecting is low-cost because it answers a required procedural question and does not interrupt the discussion.

The recorded tally is the boundary because later sessions use counted results as evidence of committee support. A qualitative record can still say that the group discussed a revision and favored its direction. It cannot include SF/F/N/A/SA numbers or another counted result when a participant has objected.

SD-4 permits "followup papers to an on-time paper, such as late or in-meeting rebuttal/elaboration/update papers."<sup>[5]</sup> The proposed rule leaves that permission intact. Authors may circulate, present, discuss, and revise late papers. The only new condition concerns whether a counted poll on such material enters the minutes.

### 3.1. Application in the Room

A mailed revision requires no additional question:

```
Chair:     We will poll P1234R3, which appeared in the February mailing.
           "EWG approves the direction of P1234R3."
           (Poll taken and recorded.)
```

For an unmailed revision, the chair asks before recording the result:

```
Chair:     We will poll P1234R5. R5 is not in a mailing; R3 is the last mailed
           revision. Is there any objection to recording this poll?
Delegate:  I object.
Chair:     Then no tally will enter the minutes. We will still take the poll to
           inform the discussion.
           "EWG approves the direction of P1234R5."
           (Show of hands. The minutes record that R5 was discussed and the room
           favored the direction.)
```

After R5 appears in the next mailing, the group can take and record the poll without this question.

### 3.2. Final-Meeting Exception

At the last meeting before a standard's publication deadline, waiting for another mailing can cost a feature an entire release. The chair therefore does not sustain an objection against a wording correction that preserves the mailed design. The exception also covers a poll to remove a feature from the working draft. The exception treats removal separately so the train model can exclude a feature that is not ready to ship.

The general rule uses an objective mailing-status test. This exception requires limited chair judgment about whether a change meets the definition of a wording correction. That judgment is confined to one class of change at one meeting. If specification review finds that the design must change, the paper returns to EWG or LEWG and appears in a mailing before a recorded poll.

## 4. The Cost

An objection can make a paper wait for another recorded poll. The next meeting may have different participants, the author may need to reintroduce the proposal, and repeated review consumes time that could have gone to other papers. With nine meetings in a three-year cycle, one additional meeting can also determine whether a feature reaches the next standard. These costs are real.

Recording the poll anyway also has a cost. Recording an unmailed design change can establish a new status quo before absent stakeholders know that the change exists. Correcting it later requires those stakeholders to overcome the committee's normal consensus threshold. That burden is harder to see than an extra meeting, but it affects both legitimacy and technical review.

The proposed rule is intended to change author incentives before an objection occurs. A mailed revision is the only revision assured of a recorded poll, so authors who need schedule certainty have reason to make the mailing version complete. Early feedback remains valuable and can still improve the paper before or during the meeting. If that feedback produces a material design change, one participant may require the new revision to pass through the mailing before its tally becomes committee precedent.

The proposed rule will not eliminate delay. It trades some visible re-review for wider notice and a consensus burden that does not turn on timing. The committee should adopt it only if that trade is worth making.

## 5. Prior Art

WG21 has considered a stronger cooling period before. P2138R4 proposed a "Tentatively Plenary" state between specification review and a plenary poll. LEWG supported the proposal by 19 to 12, short of consensus.<sup>[7]</sup><sup>[8]</sup> In 2026, eighteen implementers asked WG21 to slow the addition of features so implementations and implementation feedback could catch up.<sup>[9]</sup> WG14 also uses a four-week document deadline and normally schedules later papers for the subsequent meeting.<sup>[10]</sup> The proposed rule is narrower because it restricts only the recording of a tally and allows the room to proceed when nobody objects.

## 6. Proposed Amendment to SD-4

> **Mailing discipline for committee polls.** Before taking a poll on a paper, the chair determines whether the revision under consideration appeared in a pre-meeting mailing published before the meeting. If it did not, the chair asks whether any participant objects to the poll being recorded. On any objection, no tally may enter the record, and the poll is recorded only as permitted under Qualitative record below. This applies to every poll on a paper, whether the poll concerns direction, design, specification, or a request to forward, regardless of the subgroup, and equally to a poll on material for which no paper exists. Presentation and discussion of any document, including drafts and revisions not in a mailing, remain unrestricted, as does the taking of the poll itself; the constraint applies only to the recording of a tally.

> **Qualitative record.** A chair may record in the minutes that a document was discussed and the direction of sentiment expressed. A qualitative record is not a poll. A poll is a counted vote, recorded with a tally. Where an objection bars a tally, the qualitative record is what the minutes contain.

> **Final-meeting exception.** At the last meeting before a standard's publication deadline, an objection is not sustained against a poll on a wording correction that preserves the mailed design, so that defects found in specification review can be repaired without deferring a feature a full release. A wording correction preserves the mailed design when it does not add, remove, or rename any public-facing interface; does not change observable behavior or semantics; and does not narrow or eliminate options presented in the mailed revision. A poll to remove a feature from the working draft falls under this exception as a separate case, since removal reverts the draft to a known prior state. At every earlier meeting no exception applies, because the next pre-meeting mailing is available.

> **Group boundary.** CWG and LWG are specification groups. When specification review during a meeting determines that a design change, rather than a wording correction, is needed, the paper returns to EWG or LEWG. A paper that returns to an evolution group for a design change appears in the next pre-meeting mailing with a new revision number before any recorded poll is taken on it.

> **Open question.** The interaction between this rule and national body comment resolution during the CD/DIS cycle is left as an open question for committee discussion. A comment resolution can require a normative design change under an external ISO deadline. The committee is best placed to determine whether comment resolution needs a distinct exception or whether the group-boundary mechanism above provides sufficient flexibility.

A poll could read: "Adopt the mailing-discipline amendment to SD-4 in P4302R1."

## 7. Disclosure

The author provides information and serves at the pleasure of the committee. He is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space. They are [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[1]</sup>, [P4007R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4007r3.pdf)<sup>[2]</sup>, [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf)<sup>[3]</sup>, and [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup>, a coroutine-native model for byte-oriented I/O. His preferred asynchronous model competes with `std::execution`. Readers should weigh the argument with that conflict in mind.

The proposed rule applies to every paper in every feature area, including the author's own. Had it been in effect, an objection could have kept a tally on an unmailed revision of any of those papers out of the record.

## Appendix A. Evidence

The two cases below show two forms of the same process gap. A.1 covers the March 2026 Croydon meeting, where WG21 adopted revisions first mailed after the meeting. A.2 covers the EWG poll of 2026-06-10, which recorded a direction poll on a revision not yet distributed in a mailing.

### A.1. Croydon

The cases below were adopted at the March 2026 Croydon meeting in revisions first mailed in April. That chronology establishes that the adopted revisions did not appear in a pre-meeting mailing. The open-std.org annual papers index gives a mailing date and disposition for each paper. The chronology does not establish that any individual change was mistaken.

**Selecting one of three options.** P3980R0, "Task's Allocator Use," appeared in the February mailing with three wording options.<sup>[11]</sup> Croydon selected an option and adopted P3980R1, which omitted the rejected alternatives and first appeared in the April mailing.<sup>[12]</sup> Selecting among mailed alternatives is normal design review. The process concern is narrower: the recorded adoption poll named a revision that had not passed through a mailing.

**Removing public names.** P4159R0, "Make sender_to and receiver_of exposition-only," was written and adopted at the meeting, then first mailed in April.<sup>[13]</sup> Making the concepts exposition-only simplified the public interface and may have been the correct change. No national body expert outside the room could review that paper before adoption.

**Revisions beyond the mailed version.** P3941R2, "Scheduler Affinity," was the last mailed revision.<sup>[14]</sup> Croydon adopted P3941R4 after in-meeting rebasing connected to other `std::execution` changes.<sup>[15]</sup> P3826R3, "Fix Sender Algorithm Customization," appeared in the January mailing. Croydon adopted P3826R5 after two further revisions.<sup>[16]</sup><sup>[17]</sup> The relevant evidence is the amount of connected material that changed between the mailing and the recorded polls.

The revisions also depended on one another. P3927R1 rebased its wording on the in-meeting Scheduler Affinity revision.<sup>[18]</sup> P3826R5 removed `write_env` for consistency with that revision, and P4154R0 depended on P3826R5 having been applied.<sup>[19]</sup> The public tracker records the P3826R5 adoption poll as 9 in favor and none against or neutral.<sup>[20]</sup> A reader reconstructing the decision must review several interdependent revisions first published after the meeting.

### A.2. Brno

P3100R6, "A framework for systematically addressing undefined behaviour in the C++ Standard," appeared in the May 2026 mailing.<sup>[21]</sup> On 2026-06-10, EWG recorded this poll:

> EWG Approves of the overall direction of P3100R7, agrees to attend/spend time reviewing every line item in Telecons, and re-consider this in B&uacute;zios.

The tally was 16 strongly favor, 15 favor, 6 neutral, 2 against, and 0 strongly against, and the tracker records consensus.<sup>[23]</sup>

P3100R7 carries a document date of 2026-06-01 but was submitted and published in the July 2026 mailing.<sup>[22]</sup> P3100R7 may therefore have existed as an in-meeting draft when EWG voted. The durable point is limited to the mailing record: on the date of the poll, R6 was the last revision distributed through a WG21 mailing, while the poll named R7. The later publication of R7 does not change what the pre-meeting mailing contained.

The Brno poll concerned direction rather than adoption into the working draft. It nevertheless recorded a committee position and committed meeting time to line-by-line review. Later sessions can build on that result. A rule limited to wording or forwarding polls would leave this case untouched, so the proposed rule applies to every recorded poll on a paper revision, whether the poll concerns direction, design, specification, or a request to forward.

The Croydon and Brno cases show two forms of the same process gap. Croydon adopted revisions first mailed after the meeting. Brno recorded a direction poll on a revision not yet distributed in a mailing. Neither chronology proves that the resulting decisions were technically wrong. Both show that WG21 can establish a recorded position on text before its wider review chain receives that text.

## References

[1] [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[2] [P4007R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4007r3.pdf) - "Open Issues in std::execution::task" (Vinnie Falco, Mungo Gill, 2026).

[3] [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf) - "Symmetric Transfer and Sender Composition" (Mungo Gill, Vinnie Falco, 2026).

[4] [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[5] [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Guy Davidson, 2026).

[6] [SD-7](https://isocpp.org/std/standing-documents/sd-7-mailing-procedures-and-how-to-write-papers) - "Mailing Procedures and How to Write Papers" (Nevin Liber, 2023).

[7] [P2138R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.html) - "Rules of Design<=>Specification engagement" (Ville Voutilainen, 2021).

[8] [P2435R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2435r0.html) - "2021 Summer Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2021).

[9] [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf) - "Implementation reality of WG21 standardization" (Nina Ranns, Erich Keane, Vlad Serebrennikov, Aaron Ballman, Iain Sandoe, Jonathan Caves, Cameron DaCamara, Gabriel Dos Reis, Gonzalo Brito, Christof Meerwald, Chuanqi Xu, Shafik Yaghmour, Cody Miller, Wyatt Childers, Waffl3x (Alex), Bruno Cardoso Lopes, Hubert Tong, Louis Dionne, 2026).

[10] [WG14 N1829](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1829.htm) - "WG14 and PL22.11 (C) Joint Mailing and Meeting Information (WG14 Standing Document 1)" (John Benito, 2014).

[11] [P3980R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3980r0.html) - "Task's Allocator Use" (Dietmar K&uuml;hl, 2026).

[12] [P3980R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3980r1.html) - "Task's Allocator Use" (Dietmar K&uuml;hl, 2026).

[13] [P4159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4159r0.html) - "Make sender_to and receiver_of exposition-only" (Tim Song, 2026).

[14] [P3941R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r2.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[15] [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html) - "Scheduler Affinity" (Dietmar K&uuml;hl, 2026).

[16] [P3826R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r3.html) - "Fix Sender Algorithm Customization" (Eric Niebler, 2026).

[17] [P3826R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r5.html) - "Fix Sender Algorithm Customization" (Eric Niebler, 2026).

[18] [P3927R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3927r1.html) - "task_scheduler Support for Parallel Bulk Execution" (Eric Niebler, 2026).

[19] [P4154R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4154r0.html) - "Renaming various execution things" (Tim Song, Ruslan Arutyunyan, Arthur O'Dwyer, 2026).

[20] [cplusplus/papers #2448](https://github.com/cplusplus/papers/issues/2448) - WG21 public paper tracker issue for P3826, recording the adoption poll.

[21] [P3100R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r6.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026).

[22] [P3100R7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r7.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026).

[23] [cplusplus/papers #1901](https://github.com/cplusplus/papers/issues/1901) - WG21 public paper tracker issue for P3100, recording the Brno Evolution poll of 2026-06-10.
