---
title: "Require One Published Mailing Before Any Poll"
document: P4302R0
date: 2026-07-12
intent: ask
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The committee takes recorded polls on paper revisions that were never published in a mailing.

The pre-meeting mailing exists so that every national body can review what the committee will decide before it decides. When the revision that is polled never appeared in a mailing, the delegates who prepared from the mailing prepared against text that is not the text being decided, and the delegates who prepared most thoroughly lose the most. This paper documents the pattern at two consecutive meetings and proposes a single bright-line rule: no poll may be taken on a paper unless the polled revision appeared in a pre-meeting mailing, with one narrow exception for wording corrections at the final meeting before a release. Its purpose is to change what authors optimize for, not to block those revisions. When the mailed revision is the only revision that can be polled, authors make the mailed revision their best revision. Then the committee stops spending its scarcest resource, the prepared attention of its delegates, on text that will not survive to the vote.

---

## Revision History

### R0: July 2026 (post-Brno mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space: [P4003R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r3.pdf)<sup>[1]</sup>, [P4007R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4007r3.pdf)<sup>[2]</sup>, [P2583R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2583r4.pdf)<sup>[3]</sup>, and [P4100R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r1.pdf)<sup>[4]</sup>, a coroutine-native model for byte-oriented I/O. This paper proposes a process rule that would apply to every paper in every feature area, including the author's own. His preferred asynchronous model competes with `std::execution`. Accordingly, the reader should calibrate everything that follows.

If it had been in effect, the proposed rule would also have prevented the author from seeking a poll on any last-minute normative revision to his own papers. The author accepts that constraint.

This paper is one of a series by the author on committee process. Companion papers on the train model, on voting dynamics, and on appointment as policy are in preparation. This paper examines the mailing and the poll.

This paper was prepared with the assistance of generative tools. The author is responsible for its content, and every quotation and citation in it has been verified against a public source.

This paper asks for a change in SD-4, the document which describes WG21's operating procedures.

---

## 2. Why I Rise

I care about the standard more than I care about my position in the room. Two facts about my situation make that claim testable rather than sentimental.

### 2.1. The Conflict, Stated Plainly

I have competing papers, and the evidence in Section 6 draws heavily from `std::execution`, the feature area my own proposals compete with. It is the largest feature area in the C++26 cycle and generates more in-meeting revisions than any other, so the proposed rule would constrain it most. That conflict is disclosed in Section 1. What follows explains why it runs opposite to this paper's argument.

If I wanted `std::execution` to ship with defects, I would argue for the opposite of what I propose here. I would argue for an environment where last-minute changes go unreviewed, where wording written in a conference room on a Tuesday is voted on Saturday. That environment maximizes defect probability, and every defect that ships makes my competing proposals look better. I am arguing for the discipline that reduces that probability. I want C++ to win even when winning costs me the competitive advantage of a rival's mistake.

The authors of the in-meeting revisions in Section 6 did what was locally rational at every step. They invested years in `std::execution`. When specification review surfaced issues at the final meeting of the cycle, their choice was to fix the wording in the room or ship a known defect. That is not a real choice. The process left them no other. At each step, each author did what he believed was best for C++. The problem is structural, not personal: no amount of skill or good intention changes the risk of writing normative wording under deadline pressure and voting on it before the review chain has seen it. The authors were not given good choices.

### 2.2. What Preparation Cost Me

I prepared for the March 2026 Croydon meeting the way the process asks every delegate to prepare. I arrived with printed notes on nineteen papers in my areas: cross-referenced wording, specification-consistency checks, and questions for authors. During the meeting week, six of those nineteen changed under me. The notes I had prepared did not become partially outdated. They were structurally invalidated, because the wording and design had moved in ways that touched every point I had written down.

I watched design compromises get locked into the working draft under time pressure, in versions no national body expert outside the room could have reviewed. I was a new delegate, and I could see no way to object that would not mark me as the person who delayed the room. So I said nothing.

The effect on my own behavior was immediate and measurable. I came to Croydon with notes on nineteen papers. I came to the next meeting with notes on none. No one decided to prepare less. I learned what the structure rewards. That is a single delegate after a single meeting. The argument of this paper is that the same incentive acts on every delegate who prepares thoroughly, and that its cumulative effect is the slow erosion of the committee's review capacity.

---

## 3. The Rule: One Mailing Before Any Poll

The proposed rule is a single sentence. No poll may be taken on a paper unless the revision under consideration appeared in a pre-meeting mailing published before the meeting at which the poll is taken.

The trigger is the poll, not the presentation. Any document may be presented and discussed at any time: a draft on the committee wiki, a revision posted between mailings, a sketch on a whiteboard. Discussion is how the committee does its work, and nothing here restricts it. The rule engages only when the committee takes a poll, because a poll is the act that converts discussion into committee weight - a recorded position that later sessions treat as settled.

The bright line asks one question: did the polled revision appear in a pre-meeting mailing, yes or no. It requires no judgment about whether a change is large or small, design or wording, normative or editorial. SD-4<sup>[5]</sup> already defines the pre-meeting mailing deadline through SD-7<sup>[6]</sup> as the Monday four weeks before a meeting, and already states the purpose of that deadline: "Requiring papers to be received on time ensures that national body experts have sufficient time to consider the proposals in advance and arrive at the meeting prepared to participate in a productive discussion." The proposed rule extends that existing purpose from the agenda to the poll.

There is one exception. At the last meeting before a standard's publication deadline, polls on wording corrections that preserve the mailed design are permitted. A wording correction preserves the mailed design when it does not add, remove, or rename any public-facing interface, does not change observable behavior, and does not narrow or eliminate options presented in the mailed revision. This exception exists at exactly one meeting because that is the only meeting where deferring a fix costs a full release: at every earlier meeting, the next mailing is always available, so even a wording correction can wait for it. Section 10 explains why the exception has to live where the circular problem lives, and nowhere else.

SD-4<sup>[5]</sup> permits "followup papers to an on-time paper, such as late or in-meeting rebuttal/elaboration/update papers," and imposes no constraint on in-meeting revisions reaching a poll. This paper proposes adding that constraint, scoped to the poll alone.

---

## 4. The Incentive Inversion

The first-order effect of the rule is that a revision not ready by the mailing deadline waits one mailing cycle before it can be polled. Real as it is, that effect is not the reason to adopt the rule. The reason is the second-order effect: the rule changes what authors optimize for, and that change protects the committee's scarcest resource.

The committee's scarcest resource is the prepared attention of its delegates. A national body expert who reads a paper in the mailing, cross-references its wording, and arrives ready to engage has spent hours that do not scale and cannot be recovered. Multiply those hours across every delegate who prepares and every paper in a mailing, and preparation is the largest single investment the committee makes in the quality of the standard. It is also the investment the current structure quietly wastes.

Consider what the current structure rewards. An author who submits polished wording by the mailing deadline exposes that wording to weeks of national body scrutiny. At the deadline, an author whose wording is still moving can submit an incomplete revision, iterate in the room, and reach the same poll with far less review. The second author is not acting in bad faith. Waiting is what the structure rewards. In parallel, the delegate who prepared thoroughly against the mailed revision discovers in the room that the revision has changed, and that the preparation no longer applies. Over enough cycles, those incentives shape behavior.

The proposed rule is designed to invert both incentives, and the mechanism is a short causal chain. First, if the mailed revision is the only revision that can be polled, the mailing deadline becomes the moment that decides whether a paper can advance at the next meeting. Second, an author who wants the paper to advance then has reason to make the mailed revision the strongest one, rather than treating the mailing as a checkpoint to clear and the room as the place to finish. Third, because the polled revision is the mailed revision, the version a delegate studies is the version the committee votes, so preparation keeps its value. The delegate side of this chain is the one with evidence: the n=1 record in Section 2 is a delegate who stopped preparing once preparation stopped paying. The author side is a prediction, not a proof - authors respond to the deadline that governs the outcome, and this rule moves that deadline to the mailing.

The prediction that follows is that fewer papers end up waiting a cycle. Though the rule reads as a delay, it is an incentive to finish on time, and an incentive to finish on time tends to produce more finished-on-time work. A rule that only blocked late revisions would slow the committee. A rule that makes early preparation the paper's best path to a poll is intended to speed it up, by keeping the committee from spending its most expensive resource - delegate preparation - on text that will not survive to the vote. Whether the author-side incentive materializes as predicted is something the committee can observe after adopting the rule.

This is the whole argument. The evidence that follows shows the cost of the current incentive at two consecutive meetings, the mechanism sections show why the incentive persists, and the objections section shows that the alternatives leave the incentive in place.

---

## 5. Prior Art: A Committee Proposal, an Implementer Request, and a Sibling Committee

This paper is not the first to identify the problem or to propose a cooling period for normative wording. On the record it places three pieces of prior art: a committee proposal from 2021, an implementer request from 2026, and the standing practice of the sibling C committee. The three cover what they cover: the committee has proposed this discipline before, implementers have asked for it, and a peer body already operates a version of it.

### 5.1. The Committee Proposed a Cooling Period in 2021

In 2021, Ville Voutilainen proposed [P2138R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.html)<sup>[7]</sup>, "Rules of Design<=>Specification engagement." The paper addressed the same structural problem this paper addresses: normative wording reaching a plenary poll without adequate review. Its abstract proposes "a new Tentatively Plenary state between specification review and plenary poll" - a paper that finishes specification review waits, by default, until the next meeting for its plenary vote.

The Library Evolution poll to adopt P2138R4 as official process did not reach consensus. [P2435R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2435r0.html)<sup>[8]</sup>, "2021 Summer Library Evolution Poll Outcomes," records the tally on the question to make it "the official process of the C++ Evolution groups":

| SF | WF | N  | WA | SA |
| -: | -: | -: | -: | -: |
|  5 | 14 |  2 |  6 |  6 |

The columns are the WG21 poll scale: strongly favor, weakly favor, neutral, weakly against, strongly against. Nineteen delegates favored adoption and twelve opposed. The recorded outcome was "No consensus." The direction had majority support and fell short of the bar. Offered in good faith, the objections were substantive - concerns about gatekeeping, discouraging participation, and process weight. This paper treats P2138R4 as a direct ancestor and, in Section 9, argues that one contributing factor in its near-miss was the judgment-heavy mechanism it used, which the bright-line rule here avoids.

### 5.2. Eighteen Implementers Asked the Committee to Slow Down

In 2026, [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[9]</sup>, "Implementation reality of WG21 standardization," arrived from Nina Ranns and seventeen implementer co-authors. On the cost of the current pace, the paper reports that "full conformance to recent standards remains difficult in practice, with some implementations still working toward C++20 conformance with limited capacity to adopt newer standards." On how implementation feedback is received, it observes that "implementation feedback is often introduced late, treated as adversarial, or framed primarily as an obstacle to progress rather than as essential design input." And it states a direct request: "we would like the committee to consider ways of slowing down the addition of features into the standard to allow implementers to catch up."

The people who build the standard asked for the kind of discipline P2138R4 proposed in 2021. This paper proposes a narrower version of that discipline, scoped to the poll: one mailing before any vote.

### 5.3. The C Committee Already Operates a Version of This

The sibling C committee, ISO/IEC JTC1/SC22/WG14, operates a document deadline that a WG21 delegate would recognize. WG14 Standing Document 1<sup>[10]</sup> sets the deadline for documents in the pre-meeting collection at "four weeks prior to the meeting," and WG14's contributing guidance describes the resulting practice: "papers submitted before a meeting's mailing deadline will be discussed at the meeting. Others will be discussed at the subsequent meeting." The scheduling remains at the convener's discretion rather than an absolute prohibition, so this is a difference of degree rather than an exceptionless rule. The point stands that a peer ISO committee, producing a working standard, already treats the pre-meeting deadline as the gate for what a meeting takes up. WG21's own on-time-paper rule gates the agenda the same way, and the proposed rule extends the gate to the poll.

---

## 6. The Croydon Evidence

At the March 2026 Croydon meeting, `std::execution` papers were adopted in revisions that were first published only in the mailing that followed. This section documents that record from public sources, acknowledges the reasonable defense of each revision, and separates the design changes that concern this paper from the wording corrections that do not.

### 6.1. The Public Proof: the Mailing Date Column

The open-std.org annual papers index carries, for every paper, a "Mailing Date" column and a "Disposition" column. For each revision below, the adopted revision shows a Mailing Date of 2026-04 - the post-Croydon mailing - while its mailed predecessor shows 2026-01 or 2026-02, and the Disposition reads "Adopted 2026-03." Those two columns, read together, are the whole proof: a revision adopted at the March meeting whose first mailing was the following month was never in a pre-meeting mailing.

### 6.2. Design Changes Adopted in Unmailed Revisions

**Narrowing three options to one.** [P3980R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3980r0.html)<sup>[11]</sup>, "Task's Allocator Use" (Dietmar K&uuml;hl), appeared in the pre-Croydon 2026-02 mailing presenting three wording options, labeled A, B, and C, with the note that only one could be chosen. [P3980R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3980r1.html)<sup>[12]</sup> drops options B and C and was adopted at the meeting. Its Mailing Date is 2026-04. Perhaps the working group discussed all three and directed the author to produce a clean revision with option A - that is the normal output of design review. The national body experts who read the mailing saw a choice among three, yet the revision that was voted presented one. Narrowing a design from three options to one is a design decision, and the revision that recorded it was never mailed before the vote.

**Making public concepts exposition-only.** [P4159R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4159r0.html)<sup>[13]</sup>, "Make sender_to and receiver_of exposition-only" (Tim Song), has no previous revision and a Mailing Date of 2026-04: it was born at the meeting and adopted there. It removes two concepts from the public interface by making them exposition-only. A reasonable reader could classify this as interface simplification rather than a design change, since the underlying constraints remain and only the names become non-normative. What is not debatable is that the paper existed in no mailing at all, so it had zero days of national body review in any form before it was adopted.

**Revisions past the mailed version.** [P3941R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r2.html)<sup>[14]</sup>, "Scheduler Affinity" (Dietmar K&uuml;hl), was the last mailed revision, in 2026-02. The revision adopted at Croydon was [P3941R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3941r4.html)<sup>[15]</sup>, two revisions later, first mailed in 2026-04, carrying in-meeting rebasing tied to the sender-customization revisions discussed below. K&uuml;hl is among the most careful authors in the committee, and specification review examined the revision in the room. The structural fact is unchanged: the adopted revision was two revisions past anything a national body could have read in a mailing.

**Two revisions of unmailed iteration.** [P3826R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r3.html)<sup>[16]</sup>, "Fix Sender Algorithm Customization" (Eric Niebler), appeared in the 2026-01 mailing. The revision adopted at Croydon was [P3826R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r5.html)<sup>[17]</sup>, two revisions later, first mailed in 2026-04. Its revision history records removing "the two uses of the `write_env` algorithm" for consistency with the in-meeting revision of Scheduler Affinity, integrating feedback from a specification review dated the Wednesday of the meeting week. Rather than a new design choice in the paper itself, the removal may have been a mechanical consequence of that Scheduler Affinity decision, and every individual change may have been correct. The concern is that the adopted revision was two revisions past the last mailed one and depended on another in-meeting revision. This is not new to Croydon: the same paper's public title history shows the design space moving from [P3826R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3826r0.html)<sup>[18]</sup>, "Defer Sender Algorithm Customization to C++29," mailed before the November 2025 Kona meeting, to [P3826R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3826r1.html)<sup>[19]</sup>, "Fix or Remove Sender Algorithm Customization," dated the opening day of that meeting.

### 6.3. Revisions That Referenced Each Other

The in-meeting revisions cross-referenced each other, so no one of them could be reviewed in isolation. [P3927R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3927r1.html)<sup>[20]</sup> (Eric Niebler) rebases its wording on an unmailed revision of Scheduler Affinity. P3826R5 removes `write_env` for consistency with that same revision, and [P4154R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4154r0.html)<sup>[21]</sup>, "Renaming various execution things" (Tim Song, Ruslan Arutyunyan, Arthur O'Dwyer), depends on P3826R5 having been applied. Cross-references among related papers are normal, and `std::execution` is large enough that a fix in one paper naturally propagates to others. In consequence, a delegate seeking to understand what was being voted would have needed to read all of them together, in revisions that appeared only after the meeting. The public adoption poll for P3826R5, recorded on the public paper tracker, passed 9 for, 0 against, 0 neutral<sup>[22]</sup> - a unanimous vote on a revision the national body review chain had not seen.

### 6.4. Wording Corrections Are Not the Concern

Other in-meeting revisions at Croydon were wording corrections that preserved a mailed design, and they are not part of this concern. [P3373R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r3.pdf)<sup>[23]</sup>, [P3981R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3981r2.html)<sup>[24]</sup>, [P3795R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3795r2.html)<sup>[25]</sup>, and [P3978R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3978r3.pdf)<sup>[26]</sup> each refine wording for a design that was already mailed in an earlier revision, without adding, removing, or renaming a public interface. Section 10 explains why corrections of this kind have to be permitted, and Section 3 draws the line that separates them from the design changes above.

---

## 7. The Brno Evidence

One meeting later, at the June 2026 Brno meeting, the pattern recurred in a different feature area and in a form that sharpens the rule. A committee poll authorized an ongoing review keyed to a revision that has never appeared in any mailing, while the announcement that pointed members at the paper resolves to an older revision. From the public paper tracker, the open-std index, and live URL checks, the account below is built entirely.

### 7.1. A Poll That Names a Revision No Mailing Contains

The published paper is [P3100R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r6.pdf)<sup>[27]</sup>, "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne), which appeared in the 2026-05 mailing. On 2026-06-10, the public paper tracker records the poll taken in the Brno Evolution session, with columns for strongly favor, favor, neutral, against, and strongly against<sup>[28]</sup>:

> EWG Approves of the overall direction of P3100R7, agrees to attend/spend time reviewing every line item in Telecons, and re-consider this in B&uacute;zios.

| SF | F | N | A | SA |
| -: | -: | -: | -: | -: |
| 16 | 15 | 6 | 2 | 0 |

The tracker records the result as consensus.

The poll names P3100R7. Three independent public checks confirm that no P3100R7 exists in any mailing. The open-std.org 2026 papers index enumerates only P3100R5 and P3100R6. A direct request for the paper at its constructed open-std URL returns HTTP 404. And the short link `wg21.link/p3100r7` returns HTTP 404, because that resolver is generated from the official index, so a 404 there means the revision is not a published paper. Meanwhile `wg21.link/P3100`, the unversioned short link a member would follow from an announcement, redirects to `p3100r6.pdf` - the older revision. The only "R7" artifact available anywhere in public is a draft at `isocpp.org/files/papers/D3100R7.pdf`<sup>[29]</sup>, hosted outside the mailing system, marked D for draft rather than P for published, and internally dated 2026-07-12 - roughly a month after the June poll that referenced it. A member preparing from the mailing could not have read a P3100R7, because none was ever mailed. Following the announcement link, a member reads R6. The most charitable reading is that "R7" was a forward reference to a revision the authors intended to publish, not a claim that one already existed. Even on that reading, the poll recorded a committee position against a revision number no delegate outside the room could open, and the only draft that now carries that number is dated after the vote.

### 7.2. Why the Rule Covers Every Poll, Not Only Wording Polls

The Brno poll is the reason the rule triggers on any poll rather than on normative-wording polls alone. This poll changed no wording. By its own text it approved an overall direction, committed the group to review every line item in telecons, and reserved reconsideration for the next meeting. Under a rule that governed only normative-wording polls, it would be permitted. Yet it still records a committee position - a consensus direction, keyed to a named revision - and a recorded direction is a starting point that later sessions build from. Even with reconsideration reserved, the review now proceeds from an approved direction keyed to a revision the mailing chain never received.

A rule that distinguished direction polls from wording polls would therefore leave the loophole open: present an unmailed revision, take a direction poll on it, and let the accumulated weight carry the wording later. The distinction between kinds of poll is a taxonomy that a determined process can work around. What cannot be worked around is whether the revision appeared in a mailing. So the bright line is any poll on a paper, full stop.

### 7.3. The Same Gap at Two Meetings

The reasonable defense is that the revision was reachable to those in the room and that the authors believed adequate notice had been given. That defense measures the gap without closing it: a revision reachable to the delegates physically present, and to no one else, is a revision the national body review chain outside the room did not receive. Reaching every national body expert in every member country, including those who do not attend, is the mailing's purpose. A document that reaches only the room is the case the mailing was designed to prevent.

Read together with Section 6, the two meetings show the same gap in two forms. At Croydon, revisions were adopted in versions mailed only afterward. At Brno, a poll approved a direction and a review series keyed to a revision that remains unpublished, and the short link that members were pointed to resolves to a different revision. Within a single meeting, the first spends a delegate's preparation on the wrong text. The second sets an approved direction against a revision the review chain has not seen. Two meetings do not establish a trend, but they are the two most recent, and in neither did the process require the polled revision to have been mailed.

---

## 8. The Structural Incentive Problem

Section 4 stated the incentive the rule creates. This section examines why the current incentive persists without it, because the mechanism is not obvious and its most important part - a shift in who bears the consensus burden - is easy to miss.

### 8.1. The Asymmetry Nobody Designed

The current structure creates an asymmetry that no one intended and no one wants. Wording submitted by the mailing deadline is exposed to weeks of national body scrutiny. Wording that reaches its final form in the room is exposed to the review available during a busy meeting week. Both can reach the same poll. Therefore the most thoroughly prepared wording receives the most scrutiny, and wording finished in the room receives less, which is the opposite of what a review process would choose if it were designing the incentive deliberately. SD-4<sup>[5]</sup> states that "any design change made between the ballot and publication will be expected to have near-unanimous consent in subgroups and in plenary." Near-unanimous consent from delegates who could not review the final text in advance is a different thing from consent formed after weeks of mailing review, and the difference is invisible in the tally.

### 8.2. The Consensus Threshold Flips

The most consequential effect is a change in who must clear the consensus bar. Consider a design option that enters a paper through an in-meeting revision and is then forwarded. A stakeholder group that reviewed the mailed revision, saw no such option, and did not attend now has to assemble a two-thirds majority to remove the option at a later meeting, because the option is the status quo once it is in the working draft. Had the same option waited for the next mailing, the stakeholders would have seen it, attended, and those seeking the option would have needed the two-thirds majority to add it. Depending only on whether the change entered before or after a mailing, the same disagreement resolves in opposite directions. Entering through an in-meeting revision does more than skip review. It moves the burden of the supermajority from those who want the change to those who do not.

This is also why a "forward with the following changes" poll falls within the rule. A poll that forwards a paper together with a design modification not present in any mailed revision is a poll on unmailed normative wording, and it produces the same threshold flip. Without ever having appeared in a mailing, the modification becomes the status quo.

### 8.3. The Pattern Is Not Driven by the Shipping Deadline

A natural response is that this is a symptom of end-of-cycle pressure and will subside once a standard ships. The Brno evidence in Section 7 is the counterexample: Brno was the first meeting of the C++29 cycle, with no imminent publication deadline, and the pattern appeared anyway. At every meeting, the pressure to revise in the room and poll the result is the standing incentive that the current structure creates. A deadline intensifies it, but the deadline is not its source, which is why the remedy has to be a standing rule rather than a special measure for final meetings.

---

## 9. Why a Bright-Line Test Outperforms Chair Judgment

A rule that turns on a judgment call carries three costs that a rule with an objective test avoids. First, the outcome depends on the skill, knowledge, and disposition of whoever makes the call, so the same rule yields different results under different chairs - a single point of failure. Second, a judgment call is contestable: a delegate who disagrees with the assessment can challenge it, and the challenge has standing because the rule invited interpretation. Third, the volume of judgment calls is exhausting. A chair asked to evaluate whether each in-meeting revision crosses a design threshold, under time pressure, at the end of a cycle, carries a burden the process could avoid placing on any individual.

The proposed rule has an objective test: did the polled revision appear in a mailing, yes or no. That question is consistent across chairs, leaves nothing to interpret, and takes seconds to apply, so the general case cannot turn into a contest. Judgment survives in one place only - the final-meeting exception for wording corrections - and it is bounded there by the explicit definition in Section 3 and by the group boundary in Section 10, which route any genuine design question back to an evolution group. The discretion is confined to a single meeting rather than spread across every poll at every meeting.

P2138R4<sup>[7]</sup> is instructive here. Its cooling period was sound, and Section 5 records that it drew majority support. However, its bypass mechanism required an explicit, minuted decision by both the design group and the specification group - a judgment call at the moment the process is most rushed. A mechanism that depends on discretion at the hardest moment invites the objections that a bright-line test does not. The rule proposed here keeps P2138R4's insight and drops the discretion.

---

## 10. The Circular Problem, and How the Rule Resolves It

The rule has a circular problem that has to be stated plainly. The train model ([P1000R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1000r2.pdf)<sup>[30]</sup>, "C++ IS schedule," and its current revision [P1000R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p1000r8.pdf)<sup>[31]</sup>) provides that a feature not ready for a release is removed rather than delaying the release: in P1000R2's words, "ship what's ready." Removing a feature from the working draft requires normative wording - a paper with deletions and feature-test-macro changes - and a poll to adopt it. If that removal is discovered to be necessary at the final meeting, its wording was by definition not in a pre-meeting mailing. A rule forbidding a poll on any unmailed revision would forbid the removal poll, and so would disable the train model's safety valve at the meeting where it matters most.

The final-meeting exception in Section 3 exists to resolve this, and its scope is deliberate. At the last meeting before publication, polls on wording corrections that preserve the mailed design are permitted, and a removal that reverts the working draft to a known prior state is the cleanest such correction: it adds no new design, it withdraws one. The exception is confined to that meeting because that is the only meeting where waiting for the next mailing forfeits a release. At every earlier meeting the next mailing is available, so the circular problem does not arise and no exception is needed.

A second mechanism keeps the exception from being stretched. CWG and LWG are specification groups. Their task is to render an adopted design into wording. When specification review at a meeting determines that a design change is needed rather than a wording correction, the paper returns to EWG or LEWG, and a design change that returns to an evolution group appears in the next pre-meeting mailing with a new revision number before any further poll. The group boundary is itself a bright line: wording corrections stay, design changes go back to evolution and therefore back to the mailing. Between the narrow final-meeting exception and the group boundary, the rule permits the removals the train model depends on without opening a general path for unmailed design changes to reach a poll.

---

## 11. Objections, Answered

Below, each objection is stated in the strongest form the author can give it, then answered only from evidence already presented.

### "The author's own paper was presented without having been mailed"

This is true, and it is the clearest illustration of the rule's boundary. The author has presented material to a study group that was not in a pre-meeting mailing, and no poll was taken on it. Because it triggers on the poll (Section 3), the rule does not reach that presentation. Presenting an unmailed document, discussing it, and taking feedback are unrestricted. The constraint applies only when the committee converts discussion into committee weight through a poll. The author's presentation would remain permitted under the rule, and the author accepts that the rule would equally forbid him from seeking a poll on any unmailed revision of his own papers.

### "Iterating within a meeting is efficient, and the rule throws that away"

The rule throws none of it away. A group that is already engaged with a paper can present revisions, discuss them, and refine wording across the meeting week, just as today. Only the poll (Section 3) does the rule touch, not presentation or discussion. An author may iterate all week and bring the result to a poll at the next meeting, after the revision has been in a mailing. All that goes away is the ability to convert same-week iteration into a recorded committee position before the review chain has seen it.

### "Study groups rely on quick polls to steer early work, and the rule forbids them"

Study groups do take polls, and many are quick reads of the room that guide discussion without recording a position on a paper: a show of hands on whether a direction is worth exploring, or which of two sketches to pursue. The rule is aimed at the poll that records a committee position on a specific revision - a direction approved, a paper forwarded, an option adopted - because that is the poll later sessions build on, and the poll the Brno case turns on: a minuted result, keyed to a named revision. A read of the room that records no position on a paper is not a poll on a paper in that sense and is unaffected. Where a study group does want to record a position on a specific revision, the rule asks only that the revision have been in a mailing first, the same discipline it asks of every other group.

### "Chairs already weigh how much has changed and decide whether re-review is needed"

They do, and Section 9 is the response: chair discretion is a judgment call, and a judgment call is a single point of failure, is contestable, and is most burdensome at the moment the cycle is most rushed. The proposed rule does not remove the chair. It removes the burden, by replacing a judgment about the size of a change with an objective test about whether the revision was mailed.

### "Better stakeholder notification would solve this instead"

Notification helps with attendance, but it cannot solve the problem the evidence describes. At Brno (Section 7), the revision named in the poll existed in no mailing. Notifying a national body expert that a session is happening does not give that expert a mailed revision to have read beforehand. One cannot be notified into having reviewed a document that was never published. Notification and a mailed revision are different things, and only the second is what the review chain depends on.

### "Specification review examined the revision in the room"

Specification review is real review by careful readers, and nothing here diminishes it. But specification review is not the national body review chain. The mailing reaches every national body expert in every member country, including those who never attend. The room reaches those present. In Sections 6 and 7, the evidence turns on the versions the mailing chain did not receive.

### "The author's competing proposals explain the paper"

The conflict is real and is disclosed in Section 1 so every reader can weigh the argument knowing it. Section 2 gives the structural reason the conflict cuts the other way: a rushed `std::execution` that ships with defects would help the author's competing proposals, so proposing the discipline that reduces those defects is against his competitive interest. The rule is general, applies to every feature area including the author's own, and would have constrained his own ability to seek a poll on unmailed wording.

### "You are proposing to slow the committee down"

Section 4 is the answer: the mailing deadline becomes the checkpoint authors optimize for, and the predicted effect is that fewer papers wait. Section 5 records that eighteen implementers<sup>[9]</sup> separately asked the committee to slow the addition of features. The discipline proposed here is narrower than that request and aimed at review quality rather than pace.

### "The rule would have killed C++26"

For each affected paper in Section 6, the rule leaves two paths: poll the last mailed revision, or defer the delta one mailing. Neither removes the feature. If a delta was important enough to justify bypassing the review chain, it was important enough to survive one mailing cycle. If it could not survive one cycle, its importance did not justify the bypass.

### "Evaluate each in-meeting revision case by case"

A case-by-case exception reintroduces the judgment the rule removes (Section 9). Every author with an in-meeting revision has a reasonable argument for an exception, and a chair asked to weigh each one under time pressure is placed back in the position the bright-line test was designed to spare.

### "The rule can be used to filibuster a paper"

If every design change reset the clock, an objector might try to force design changes at each meeting to keep a paper from ever reaching a poll. Only if the room adopts it does a change reset the clock, so a failed motion is not a filibuster. Where a feature is large enough that real design findings surface at every meeting, the group boundary in Section 10 handles it: specification groups make wording corrections that preserve the design, and anything requiring a design decision returns to an evolution group and the next mailing.

### "The rule would gridlock national body comment resolution"

During the comment-resolution cycle, national bodies submit comments that the committee resolves under an external ISO deadline, and resolving a comment can require a design change. This is a genuine open question rather than a solved case. The group boundary in Section 10 should cover most of it - wording resolutions preserve the design, design resolutions go through an evolution group - but the interaction with the external deadline deserves the committee's consideration, and Section 12 records it as an open question rather than legislating an answer.

---

## 12. Proposed Amendment to SD-4

The following text is offered as an amendment to SD-4<sup>[5]</sup> for the committee to contemplate. It is drafted to sit alongside the existing on-time-paper rule, which already gates the agenda. This extends the same principle to the poll.

> **Mailing discipline for committee polls.** No poll may be taken on a paper unless the revision under consideration appeared in a pre-meeting mailing published before the meeting at which the poll is taken. This applies to every poll on a paper, whether the poll concerns direction, design, specification, or a request to forward, and regardless of the subgroup. Presentation and discussion of any document, including drafts and revisions not in a mailing, remain unrestricted; the constraint applies only to the taking of a poll.

> **Final-meeting exception.** At the last meeting before a standard's publication deadline, polls on wording corrections that preserve the mailed design are permitted, so that defects found in specification review can be repaired without deferring a feature a full release. A wording correction preserves the mailed design when it does not add, remove, or rename any public-facing interface; does not change observable behavior or semantics; and does not narrow or eliminate options presented in the mailed revision. A poll to remove a feature from the working draft is permitted under this exception, since removal reverts the draft to a known prior state. At every earlier meeting no exception applies, because the next pre-meeting mailing is available.

> **Group boundary.** CWG and LWG are specification groups. When specification review during a meeting determines that a design change - not a wording correction - is needed, the paper returns to EWG or LEWG. A paper that returns to an evolution group for a design change appears in the next pre-meeting mailing with a new revision number before any further poll is taken on it.

> **Open question.** The interaction between this rule and national body comment resolution during the CD/DIS cycle is left as an open question for committee discussion. A comment resolution can require a normative design change under an external ISO deadline. The committee is best placed to determine whether comment resolution needs a distinct exception or whether the group-boundary mechanism above provides sufficient flexibility.

For a champion who brings this forward, a poll could read: "Adopt the mailing-discipline amendment to SD-4 in P4302R0 - no poll on a paper unless the polled revision appeared in a pre-meeting mailing, with the final-meeting exception for wording corrections and the group-boundary provision." The amendment text above is the exact wording to be adopted.

---

## 13. Conclusion

The record at two consecutive meetings shows the committee polling revisions that its own review chain never received. At Croydon, design changes were adopted in revisions first mailed the month after the vote. At Brno, a poll authorized an ongoing review keyed to a revision that remains unpublished, while the link that members were pointed to resolved to an older one. In both cases the delegates who prepared from the mailing prepared against text that was not the text being decided.

The rule proposed here moves the checkpoint for a poll back to the mailing, where national body preparation already happens. Its value is the incentive it creates: when the mailed revision is the only revision that can be polled, the mailing deadline becomes the moment authors work toward, and the version the review chain studies becomes the version the committee votes. Because early preparation becomes the strategy the structure rewards, the predicted result is that fewer papers wait a cycle.

What the committee keeps by adopting the rule is the return on its own preparation: the hours national body experts spend reading the mailing are spent on the text that will be decided, and the consensus recorded in a poll is consensus about a document the whole review chain could see. What the committee keeps paying without the rule is an incentive that rewards waiting and penalizes preparation, and a distance between what is published and what is decided that was present at each of the last two meetings. The instrument is the short amendment to SD-4 in Section 12: no poll on a paper unless the polled revision was in a pre-meeting mailing, with the single final-meeting exception for wording corrections. This paper asks the committee to adopt it.

---

## Acknowledgements

Ville Voutilainen, whose P2138R4<sup>[7]</sup> identified the need for a cooling period between specification review and a plenary poll five years before this paper, and which this paper treats as its direct ancestor. Nina Ranns and the seventeen co-authors of P3962R0<sup>[9]</sup>, whose account of implementation reality documents the cost this paper's rule is meant to reduce. The author also thanks colleagues who, in correspondence, sharpened the argument: the consensus-threshold asymmetry in Section 8, the filibuster concern and its resolution through the group boundary in Section 10, and the observation that a bright-line test avoids the discretion that weighed on P2138R4. Any errors are the author's own.

---

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

[18] [P3826R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3826r0.html) - "Defer Sender Algorithm Customization to C++29" (Eric Niebler, 2025).

[19] [P3826R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3826r1.html) - "Fix or Remove Sender Algorithm Customization" (Eric Niebler, 2025).

[20] [P3927R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3927r1.html) - "task_scheduler Support for Parallel Bulk Execution" (Eric Niebler, 2026).

[21] [P4154R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4154r0.html) - "Renaming various execution things" (Tim Song, Ruslan Arutyunyan, Arthur O'Dwyer, 2026).

[22] [cplusplus/papers #2448](https://github.com/cplusplus/papers/issues/2448) - WG21 public paper tracker issue for P3826, recording the adoption poll.

[23] [P3373R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3373r3.pdf) - "Of Operation States and Their Lifetimes" (Robert Leahy, 2026).

[24] [P3981R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3981r2.html) - "Better return types in std::inplace_vector and std::exception_ptr_cast" (Barry Revzin, Jonathan Wakely, Tomasz Kami&#324;ski, 2026).

[25] [P3795R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3795r2.html) - "Miscellaneous Reflection Cleanup" (Barry Revzin, 2026).

[26] [P3978R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3978r3.pdf) - "constant_wrapper should unwrap on call and subscript" (Matthias Kretz, 2026).

[27] [P3100R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r6.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026).

[28] [cplusplus/papers #1901](https://github.com/cplusplus/papers/issues/1901) - WG21 public paper tracker issue for P3100, recording the Brno Evolution poll of 2026-06-10.

[29] [D3100R7](https://isocpp.org/files/papers/D3100R7.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026). Draft; not published in any mailing.

[30] [P1000R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1000r2.pdf) - "C++ IS schedule" (Herb Sutter, 2018).

[31] [P1000R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p1000r8.pdf) - "Proposed C++ IS schedule" (Guy Davidson, 2026).
