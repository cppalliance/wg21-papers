---
title: "Do Remove Contracts From C++26"
document: P4420R0
date: 2026-10-23
intent: ask
audience: EWG, WG21
reply-to:
 - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper asks WG21 not to commit in advance to shipping the C++26 DIS unchanged. The no-change position asks WG21 to confirm by poll that it will entertain no language design change to the DIS. That position was written before the national body comments were known, and the poll would be taken before WG21 has reviewed those comments at a meeting, while clause 2.6.4 of the ISO/IEC Directives puts that review first. This paper asks WG21 to hold the review and, if the objections to contract assertions survive it, to recommend a revised C++26 draft without contract assertions.

The case rests on process and risk. The ballot is a review outside the working group. Removal costs a delay; a defect in a published standard is effectively permanent. The one concession made to the objectors was reversed before the ballot closed. The record shows the objections were heard, which is not the same as answered. The disputes over undefined behavior, mixed translation units, safety, static analysis, teachability, and incompleteness are left to other papers.

## Revision History

### R0: October 2026

- Initial version.

## 1. What This Paper Does Not Dispute

The no-change position is right on several points, and nothing below depends on the contrary. WG21 has polled in favor of keeping contracts since February 2025: the Hagenberg EWG poll to remove them from C++26 and find a different ship vehicle failed at 9/8/3/19/41 (SF/F/N/A/SA),<sup>[1]</sup> and the Croydon poll to remove them failed at 11/3/7/24/35.<sup>[2]</sup> Contracts on virtual functions, which [P4334R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4334r0.pdf)<sup>[3]</sup> calls an inheritance model, were postponed to C++29, so the position's bullet about a "completely untried inheritance model" misdescribes the draft. P4334R0 cites P3878R0 on hardening, which [P3878R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r1.html)<sup>[4]</sup> superseded. Contract assertions are implemented, and GCC 16.1 ships them.<sup>[5]</sup> [P4324R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4324r0.html)<sup>[6]</sup> calls itself an exploration and is not a ready replacement. None of the polls below turns on any of this.

## 2. The Review Comes First

The no-change position holds that technical work backed by strong consensus in WG21 cannot be undone at the DIS ballot by a small group of individuals whose position did not prevail in WG21. The DIS ballot exists so that national bodies can challenge exactly that. It is the review outside the working group, and the approval rules let a minority block the draft.<sup>[7]</sup>

That position was formulated before the comments were known, and it asks WG21 to rule out language design changes before reviewing them at a meeting. Clause 2.6.4 of the Directives says an appropriate group of the committee "will, at a meeting, address any comments received."<sup>[7]</sup> A poll that rules out change on those terms replaces the review with a fixed answer, and leaves the ballot as the rubber stamp P4238R1 warned about.<sup>[1]</sup>

Clause 2.6.4 lays out several courses of action. The position endorses two: publish if the ballot passed, and run another eight-week ballot without altering contract assertions if it failed. It never asks the committee to address the comments at a meeting first, though the clause requires exactly that. The ask in this paper is the same whether the ballot passed or failed, because the clause puts the review first in either case.<sup>[7]</sup>

The position adds that sustained opposition confers no veto. That is a statement about consensus inside WG21. Clause 2.5.7 says the concept of sustained opposition "is not applicable in the context of National Body votes on enquiry or approval ballots since these are subject to the applicable voting rules."<sup>[7]</sup> Under clause 2.6.3, negative votes with technical comments above one quarter of the votes cast are enough to fail the draft.<sup>[7]</sup> A national body vote is cast by a national body, not by an individual, and by the position's own account some national bodies have voted against a DIS for the first time in the history of C++. That is evidence of breadth, not of a faction.

## 3. A Delay Against a Permanent Defect

The no-change position supplies the case for removal. It says what contracts lack will be added in C++29 and beyond, and that the planned extensions are purely additive. If that is true, removal sends contract assertions to C++29, where they can arrive together with the pieces they lack. P2695R1 allowed for this: Contracts "will miss the train and we will have to wait three more years."<sup>[8]</sup> If it is false, C++26 freezes a base design that cannot take those pieces at all. The position needs the first to be true, and asserts that it is.

The two costs are not alike. Removal costs a delay, not a failure: wording review, an eight-week revised ballot,<sup>[7]</sup> and whatever comment resolution follows. P4238R1 puts it at months, not years.<sup>[1]</sup> A locked-in defect costs effectively forever. Field experience after publication can add pieces on top of the base, but changing the base is the slow and rare route described below. Everything else in C++26 continues unchanged apart from the standard library hardening wording, which P3471R4 section 8.1 says could easily be reworded without contracts, subject to the project editors' review.<sup>[9]</sup>

Withdrawing a feature from a published standard is slow and rare, and the clean reversals have all come before publication: Concepts in 2009,<sup>[10]</sup> Contracts in 2019, and trivial relocation in 2025, which C++26 lost at Kona at the committee draft stage after national body comments and a recorded statement that the major implementers could not support that version.<sup>[1]</sup><sup>[11]</sup> The reasoning of the 2019 removal paper applies now: "if there is not consensus that a feature is in acceptable form when the train is about to depart that the feature must be taken off the train."<sup>[12]</sup> It added: "We have removed features before (such as Concepts for C++11) and came back with better approaches."<sup>[12]</sup> The position's account of that history does not mention the 2019 removal of contracts from the C++20 draft, though P2899R1 records it.<sup>[12]</sup><sup>[13]</sup>

## 4. The Concession That Expired

The no-change position points to one concrete change as an answer to the objections: contracts on virtual functions were removed from C++26 and postponed until C++29 to address the sustained objections. The removal is real, it is dated, it is in the record, and the objections that prompted it are in P3573R0.<sup>[14]</sup> The position cites it as an example of the process changing in response to sustained objections. It shows something narrower.

**The concession was reversed before the ballot it was meant to influence.** EWG voted contracts on virtual functions out of C++26 in February 2025.<sup>[13]</sup> P3097R3, which re-proposes them for C++29,<sup>[15]</sup> was approved for the C++29 working draft at Brno in June 2026,<sup>[16]</sup> sixteen months later, after WG21 voted to send C++26 to DIS ballot<sup>[2]</sup> and before that ballot closed. Remove the piece, send the core to ballot, restore the piece to the C++29 draft. Nothing was conceded to the objectors that their objection could still test.

**The position uses the deferral twice.** It cites the removal as the process responding to the objections, and it cites the Brno adoption to rebut the claim that the pieces ordinary use needs are still being designed. Both statements can be true. As arguments they pull against each other: a deferral restored sixteen months later was a small accommodation, and it is hard to cite it both as evidence that the process bent to the objectors and as evidence that the missing pieces are already arriving.

**The "purely additive" claim turns the deferral into a dismissal.** The position says the C++29 extensions are purely additive and fully backwards compatible. If that is true, pulling the piece out of C++26 cost the design nothing and it returns unchanged in C++29, and a change that costs nothing and is restored on schedule is no accommodation at all. If it is false, the C++26 base cannot take those pieces without change, and the deferral is not a plan.

**The ratchet.** A ratchet turns one way: each step forward is held in place, and no step back is allowed. The record shows the same mechanism at three gates. At the first, the plan agreed in P2695R1 was later used to close complaints about pace (section 6). At the second, the piece was removed in response to the objections and restored once the core had gone to ballot. At the last, the position argues that work carried by consensus in WG21 cannot be undone at the DIS ballot. Each gate treats the one before it as settled.

**What the ratchet leaves.** After publication contract assertions are effectively permanent (section 3), while the removed piece returns as an extension on a frozen base. The one change made for the objectors is undone. The decisions that went against them are not. If EWG believes the deferral improved the design, it can prove that by letting the deferral complete before the base is frozen. Shipping the pruned version now is what makes the belief untestable.

## 5. Heard Is Not Answered

The no-change position answers the procedural objection with meeting time: by its own count, six meetings with dedicated EWG time, and an assertion that each concern was weighed and decided. The question P4238R1 raises is narrower, whether the minutes record a finding that each objection was answered.<sup>[1]</sup> Hearing is not accommodation, and volume of process is not yield of process. Across the P2900 revision history and the papers after it, the changes this paper can tie to the objections are one library function deleted (`evaluation_exception()`)<sup>[17]</sup> and one sub-feature cycled out and back (section 4).

The position also says the objectors offered no alternative design. They asked for field experience first, through a Technical Specification, and SG21 recommended against it in May 2024 (1/3/3/12/10).<sup>[1]</sup> They did propose design changes, such as John Spicer's P3281R0,<sup>[18]</sup> which failed in SG21 the same month (8/4/0/4/3 and 4/2/1/4/10).<sup>[13]</sup>

The position answers that predicates are C++ expressions and can have undefined behavior, that behavior across translation units follows the existing linkage model, and that incompleteness is deliberate. On those three points the answer is "this was considered and judged acceptable," not "this is wrong." Section 1 concedes the points where the position is right. That is a legitimate basis for a majority decision, but not a refutation of the objection, and a ballot outside the working group is where a majority decision is tested.

## 6. The Record on Pace

The no-change position denies that the design was hasty. The record says otherwise.

SG21 adopted a roadmap targeting C++26 in November 2022, and the plan, in its authors' words, "can be derived more or less directly from" the release deadlines.<sup>[8]</sup> P3443R0 reports that complaints about the pace were "considered but rejected based on the plan agreed in P2695R1."<sup>[19]</sup> The rationale paper, P2899R1, says SG21 "meticulously followed" the plan:<sup>[13]</sup> fifteen revisions, P2900R0 to P2900R14, in 16.6 months.<sup>[20]</sup><sup>[21]</sup> Wording arrived in R5, in February 2024,<sup>[20]</sup> and SG21 forwarded the paper to EWG and LEWG two weeks later.<sup>[13]</sup> By P3443R0's data, 23 of the 41 Contracts poll items between January and October 2024 came a week or less after the paper appeared.<sup>[19]</sup>

The design was still changing in the last week. EWG merged contracts on virtual functions in June 2024 and, in response to objections, voted them out on 11 February 2025 (20/24/13/14/2).<sup>[13]</sup> CWG approved the next day and LWG the day after,<sup>[22]</sup> and the plenary adopted P2900R14 that week at 100/14/12.<sup>[23]</sup> John Spicer, who chaired SG21 and co-wrote the plan, now says "the schedule itself became part of the next failure mode."<sup>[24]</sup>

A late addition was removed after adoption. The function `evaluation_exception()` was added in November 2024.<sup>[20]</sup> Its authors later found that on some platforms it required copying the exception object, which may pose a security risk, and it was removed in November 2025 in response to national body comments.<sup>[17]</sup><sup>[11]</sup>

Field experience came late. The implementers' report met EWG's Tokyo request for "some usage experience" in a standard library implementation (16/30/12/3/0),<sup>[13]</sup> but said that the libc++ experience was "limited to contract_assert, as no new pre and post conditions were added."<sup>[25]</sup> GCC first shipped C++26 contract assertions on 30 April 2026, a month after WG21 voted to send the draft to DIS ballot.<sup>[5]</sup><sup>[2]</sup>

## 7. Suggested Polls

Two polls could read:

1. WG21 will review the national body comments on the C++26 DIS under ISO/IEC Directives Part 1, clause 2.6.4, before it recommends any course of action to the SC22 chair.
2. After that review, if the national body objections to contract assertions remain unresolved, WG21 recommends to the SC22 chair a revised C++26 draft without contract assertions.

Poll 2 is taken only after the review in poll 1 is complete. If the poll the no-change position asks for is also put to WG21, this paper asks that poll 1 be taken first. A revised draft would respecify standard library hardening without contract assertions (section 3). Four Kona comments and RU-016 disagree on whether hardening should rely on contracts at all.<sup>[11]</sup> Like the no-change position, this paper was written before the comments were known. Unlike it, this paper asks for the review first.

## Disclosure

The author provides information and serves at the pleasure of the committee.

Vinnie Falco is president of the C++ Alliance, a co-author of P4334R0 and P4238R1, and the lead signatory of the petition "C++26 Needs To Go Back." The C++ Alliance has published the position that national bodies should vote No on the C++26 DIS. Readers should weigh the argument with that interest in mind.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

## References

[1] [P4238R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r1.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, José Daniel García Sánchez, John Spicer, 2026).

[2] [N5040](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5040.pdf) - "WG21 2026-03 Croydon Hybrid Meeting Minutes" (Braden Ganetsky, 2026).

[3] [P4334R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4334r0.pdf) - "P2900 Contracts' fundamental flaws" (Bjarne Stroustrup, J-Daniel Garcia, Vinnie Falco, John Spicer, Ville Voutilainen, 2026).

[4] [P3878R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r1.html) - "Standard library hardening should not use the 'observe' semantic" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[5] [GCC 16.1 release announcement](https://www.mail-archive.com/gcc@gcc.gnu.org/msg107232.html) - "GCC 16.1 Released" (Richard Biener, 2026). Posted to the gcc mailing list on 30 April 2026.

[6] [P4324R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4324r0.html) - "Exploration of a more library-oriented approach to contracts" (Ville Voutilainen, 2026).

[7] [ISO/IEC Directives, Part 1](https://www.iso.org/sites/directives/current/consolidated/index.html) - 21st edition (2026), clauses 2.5.7, 2.6.3 and 2.6.4. The 2024 text numbers the sustained-opposition clause 2.5.6 and says "member body votes" where the 2026 text says "National Body votes". The argument does not depend on the difference.

[8] [P2695R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2695r1.pdf) - "A proposed plan for Contracts in C++" (Timur Doumler, John Spicer, 2023).

[9] [P3471R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3471r4.html) - "Standard library hardening" (Konstantin Varlamov, Louis Dionne, 2025).

[10] [N2920](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2009/n2920.html) - "Minutes of WG21 Meeting, July 13, 2009" (Robert Klarer, 2009).

[11] [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf) - "WG21 2025-11 Kona Minutes of Meeting" (Nina Dinka Ranns, 2025).

[12] [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf) - "Remove Contracts from C++20" (Nicolai Josuttis, Ville Voutilainen, Roger Orr, Daveed Vandevoorde, John Spicer, Christopher Di Bella, 2019).

[13] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Joshua Berne, Timur Doumler, Rostislav Khlebnikov, Andrzej Krzemieński, 2025).

[14] [P3573R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3573r0.pdf) - "Contract concerns" (Michael Hava, J. Daniel Garcia Sanchez, Ran Regev, Gabriel Dos Reis, John Spicer, Bjarne Stroustrup, J.C. van Winkel, David Vandevoorde, Ville Voutilainen, 2025).

[15] [P3097R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3097r3.pdf) - "Contracts for C++: Virtual functions" (Timur Doumler, Joshua Berne, Gašper Ažman, 2026).

[16] [cplusplus/papers #1822](https://github.com/cplusplus/papers/issues/1822) - WG21 public paper tracker issue for P3097, recording the CWG approval of P3097R3 at Brno on 2026-06-12, the plenary-approved label, and the merged working draft change for 2026-06 CWG Motion 16.

[17] [P3819R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3819r0.pdf) - "Remove evaluation_exception() from contract-violation handling for C++26" (Peter Bindels, Timur Doumler, Joshua Berne, Eric Fiselier, Iain Sandoe, 2025).

[18] [P3281R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3281r0.pdf) - "Contract Checks Should Be Regular C++" (John Spicer, 2024).

[19] [P3443R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3443r0.pdf) - "Reflection on SG21's 2024 Process" (Ran Regev, 2024).

[20] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemieński, 2025).

[21] [P2900R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2900r0.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemieński, 2023).

[22] [cplusplus/papers #1648](https://github.com/cplusplus/papers/issues/1648) - WG21 public paper tracker issue for P2900, recording the EWG, LEWG, CWG, and LWG polls.

[23] [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf) - "WG21 02/2025 Hagenberg Minutes of Meeting" (Nina Dinka Ranns, 2025).

[24] [P4381R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4381r0.html) - "Chairing SG21 and then objecting to Contracts" (John Spicer, 2026).

[25] [P3460R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3460r0.pdf) - "C++ Contracts Implementers Report" (Eric Fiselier, Nina Dinka Ranns, Iain Sandoe, 2024).
