---
title: "SD-4: Five Correctives Inspired by ISO Directives"
document: P4130R0
date: 2026-08-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

[SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)<sup>[1]</sup> lets the convenor appoint every subgroup chair, set the meeting schedule, and declare consensus.

No chair serves a fixed term, no appointment returns to the committee for confirmation, and no chair must reconcile the objections raised against a proposal. The ISO/IEC Directives govern to the working-group level and provide a check for each, and for three further passages of SD-4 besides. This paper proposes five correctives, each replacing a single passage of SD-4 with text that aligns the practice with the Directives. The convenor can adopt all five immediately.

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author's position is that C++ should prioritize stability over feature velocity.

## 2. One Office Appoints, Schedules, and Declares Consensus

One office holds three powers, and nothing checks any of them. The convenor appoints every subgroup chair, sets the meeting schedule, and declares consensus. Chairs serve no fixed term, the committee confirms no appointment, and no rule requires a chair to reconcile the objections raised against a proposal.

SD-4 confirms that chairs "have no fixed term."<sup>[1]</sup> Study group chairs function identically.<sup>[2]</sup> The committee's own description states that the convenor "determines consensus, chairs the WG, sets the WG meeting schedule," and "appoints Study Groups," and that the subgroups operate "with the authority of the convenor."<sup>[3]</sup> The Directives govern to the working-group level and are silent on WG-internal structure<sup>[4]</sup>; SD-4 fills that silence.

SD-4's text concentrates that power, whoever holds the office and however they use it. The correctives in Section 3 address the office rather than its current holder; every provision quoted here predates the current convenor.

### 2.1 Five Provisions Make a Declaration Nearly Irreversible

Once a chair declares consensus, five provisions of SD-4 make that declaration nearly impossible to reverse:

1. A proposal "normally advances if there are more than twice as many in favor of a proposal as against"<sup>[1]</sup> - a vote ratio, with no requirement to reconcile the concerns of those against.
2. The minority, once heard, must "accept group decisions."<sup>[1]</sup>
3. A national body ballot comment that revisits a decided question is "out of harmony with the ISO Code of Conduct."<sup>[1]</sup>
4. A competing approach that lacks a paper "does not exist and will not block progress."<sup>[1]</sup>
5. Repeated escalation "erodes their credibility."<sup>[1]</sup>

The provisions create compounding effects, each amplified by the Bandwidth Gap: the median delegate cannot absorb the volume of papers and falls back on social signals to vote. SD-4 then treats silence as agreement, in the provision it calls unanimous consent - Silence as Consensus. In a room where most delegates did not read the paper, a decision reached on a bare two-to-one vote becomes a result the minority must accept, may not revisit at ballot, dare not escalate, and cannot displace with a later alternative. This is a ratchet: it turns once, and it locks.

---

## 3. Five Correctives, Each Replacing One Passage of SD-4

Each corrective below replaces a single passage of SD-4 with text drawn from the ISO/IEC Directives.

### 3.1 SD-4 Grants Chairs Indefinite Tenure; the Directives Require Fixed Terms

The Directives require fixed terms with confirmation for the offices they govern (Directive 1.12.1)<sup>[4]</sup>; SD-4 grants subgroup chairs indefinite tenure with neither.

:::wording

<del>Subgroup chairs are appointed by the convenor, and are selected to match the current needs of the subgroup. They have no fixed term.</del>

<ins>Subgroup chairs are appointed by the convenor for a term of three years, subject to confirmation by the committee. Chairs may be reappointed through the same process.</ins>

:::

### 3.2 The Two-to-One Rule Appears Nowhere in the Directives

The Directives define consensus as the reconciliation of conflicting arguments, not a vote ratio (Directive 2.5.6)<sup>[4]</sup>. The two-to-one rule appears nowhere in the Directives.

:::wording

<del>Subgroup polls, especially in design subgroups, should favor progress. A proposal normally advances if there are more than twice as many in favor of a proposal as against, after discussion of the concerns of those voting against and possibly a re-poll to see if opinions have improved. This is true even if a large number vote Neutral, though it can be concerning if a majority of all those voting vote Neutral.</del>

<ins>Subgroup polls should ensure all views are heard. The chair determines whether consensus exists after discussion of the concerns of those voting against and, where possible, reconciliation of conflicting arguments. The reconciliation shall be minuted and circulated within four weeks of the meeting end (Directive 1.9.2c).</ins>

:::

### 3.3 The Directives Place No Content Limit on Ballot Comments

The Directives place no content restriction on national body ballot comments (Directive 2.6.2) and require every comment to be addressed (Directive 2.6.5)<sup>[4]</sup>; SD-4 cannot override either obligation, and no internal practices document could.

:::wording

<del>A ballot comment that requests a change that was already considered and decided otherwise at a WG21 meeting, and comes from a national body that was present at the meeting and had an opportunity to have their objections be heard and considered, is out of harmony with the ISO Code of Conduct's commitment to 'accept group decisions.' Once the WG has consensus to send a document for ballot, to repeat as an NB comment an objection that previously failed to carry the day is actually making, not a new technical objection, but an objection to the consensus of the WG.</del>

<ins>National body ballot rights are governed by the ISO/IEC Directives (2.6.2, 2.6.5). All technical and editorial comments are in scope and all comments shall be addressed.</ins>

:::

### 3.4 SD-4 Penalizes a Right the Directives Protect

The Directives direct objectors to a formal appeal process and attach no penalty to its use (Directive 2.5.6, Clause 5.1)<sup>[4]</sup>. SD-4's credibility language penalizes a participant for using a right the Directives protect.

:::wording

<del>...or (b) when a participant or national body regularly uses the escalation process to express a pattern of strong disagreement on topic after topic, which erodes their credibility and is not the purpose of the escalation resolution process (like exception handling, escalation handling is for hard errors, and is not designed for expressing less serious conditions or for what should be ordinary control flow).</del>

<ins>...or (b) when escalation is used routinely for matters that could be resolved through normal discussion. The formal appeal process (ISO/IEC Directives, Clause 5.1) is available to any participant at any time without prejudice.</ins>

:::

### 3.5 SD-4 Treats an Absence of a View as Agreement

The Directives define consensus as "seeking to take into account the views of all parties concerned" (Directive 2.5.6)<sup>[4]</sup>; silence is the absence of a view, not its expression.

:::wording

<del>Unanimous consent, where if there are no objections then it is known that everyone is either in favor or neutral, without having to count hands. This is typically used to save time when there may already be broad agreement.</del>

<ins>Unanimous consent is appropriate only for editorial corrections, procedural motions, and matters previously decided by an explicit poll. For substantive design or specification questions, the chair takes an explicit poll. Silence is not agreement.</ins>

:::

---

## 4. Conclusion

These five correctives do not close every gap between SD-4 and the Directives. Each one closes a gap on its own, and each cites the Directive it restores. All five replace a single passage in a document the convenor maintains and revises between meetings, so adopting them requires no poll, no study group, and no national body ballot.

---

## References

[1] [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Guy Davidson, 2026). The provisions quoted here predate the current convenor.

[2] [SD-3](https://isocpp.org/std/standing-documents/sd-3-study-group-organizational-information) - "Study Group Organizational Information."

[3] [The Committee](https://isocpp.org/std/the-committee) - "The Committee."

[4] [ISO/IEC Directives, Part 1, Consolidated JTC 1 Supplement](https://jtc1info.org/wp-content/uploads/2023/11/ISO-IEC-Consolidated-JTC-1-Supplement-2023.pdf) (ISO/IEC, 2023).
