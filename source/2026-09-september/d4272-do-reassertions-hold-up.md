---
title: "Addressed but Not Resolved: P3846R1's Eighteen Responses on C++26 Contract Assertions"
document: P4272R0
date: 2026-09-03
intent: info
audience: EWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Measured against the resolution standard the ISO/IEC Directives define, P3846R1's eighteen responses resolve two of the eighteen objections raised against C++26 contract assertions.

P3846R1, "C++26 Contract Assertions, Reasserted", answers eighteen concerns about the contract assertions facility adopted into the C++26 working draft, and its abstract asserts that the objections were addressed in subsequent responses and extensively discussed in EWG. This assessment tests the closure claim against the public record at two cutoff dates. It rates each response for its support on the record, then measures the response against the standard the Directives assign to the word the claim uses: resolution by draft change, by explanation whose evidence suffices for its conclusion, or by recorded decision with a stated rationale. On support, the record is in the authors' favor: two responses are Supported, six Substantially supported, ten Mixed, and none Not supported or Contradicted, though fifteen responses contain a material assertion the record does not support, four of them contradicted by it. On resolution, the record is in favor of the objecting position: two objections Answered, fifteen Partly answered, one Not resolved. The authors' own public statements show the distinction in operation: they direct live objections to P3846 and invoke prior votes, roadmap boundaries, timing, or future work as reasons to retain the C++26 design unchanged. The three forms of resolution are not theoretical. This dispute produced all three: twice by a response, once by a draft change whose authors record the commenters' confirmation. The distribution is therefore a finding about the responses rather than the rubric: substantive argument was produced, and closure was not. The assessment then states what a discharged reconciliation duty leaves on the record, drawn from practice in force in WG21's Library Evolution group, WG14, and ASTM, and finds that record absent from the adoption arc.

---

## Revision History

### R0: September 2026

- Initial version.

---

## 1. Introduction

P3846R1<sup>[1]</sup>, "C++26 Contract Assertions, Reasserted", answers eighteen concerns raised about P2900R14<sup>[2]</sup>, the contract assertions facility adopted into the C++26 working draft at the February 2025 Hagenberg meeting. Its abstract states that "Almost all objections are repetitions of those raised in earlier papers, addressed in subsequent responses, and extensively discussed in EWG" (p. 1). The same abstract qualifies the claim: "Some of the concerns are legitimate yet unavoidable with any viable assertion facility. Others reflect misunderstandings of the proposal, leading to inaccurate observations." (p. 1). The closure claim is tested twice: each of the eighteen responses is assessed against the public record, and each is then measured against the standard the ISO/IEC Directives assign to the word P3846R1 itself uses, whether the objection was resolved. The abstract's qualification is answered as an objection in Section 8.

P2900 provides contract assertions in declaration position - preconditions, postconditions, and `contract_assert` - with four evaluation semantics selectable per translation unit and a global contract-violation handler invoked when a checked assertion fails. P3846R1 is the consolidated response by twenty-two authors, including two of the three authors of P2900R14. The concerns it answers come from the objecting papers P3835R0<sup>[3]</sup>, P3829R0<sup>[4]</sup>, P3849R0<sup>[5]</sup>, P3506R0<sup>[6]</sup>, and P3878R0<sup>[7]</sup>, and from national body comments on the C++26 draft whose dispositions the Kona November 2025 minutes record<sup>[8]</sup>.

The assessment provides seven contributions:

1. The resolution standard of the ISO/IEC Directives, stated with its scope, applied to P3846R1's closure claim (Section 2).
2. A three-field assessment method at two cutoff dates, separating support for a response from defects in its subclaims from resolution of the objection (Section 3).
3. The eighteen-concern assessment (Sections 4 and 5): two responses Supported, six Substantially supported, ten Mixed, none Not supported or Contradicted; fifteen responses with a material unsupported subclaim; two objections Answered, fifteen Partly answered, one Not resolved.
4. A concern-level and thematic record of the P3846R1 authors' own words, showing prior responses, polls, roadmap boundaries, timing, and future work functioning as closure (Sections 5 and 7).
5. Four corrections to the public citation record. The 2016 lost-optimization report is LLVM issue 28170, renumbered from Bugzilla 27796 when the LLVM tracker migrated to GitHub<sup>[9]</sup>. The Kona minutes N5031 are a 2025 document<sup>[8]</sup>. P3626R0 is the alternative wording prepared by the lead author of P2900R14 and P3846R1 so that EWG could poll the alternative; it is not an independent rival proposal<sup>[10]</sup>. P3097R0 was merged into P2900R8<sup>[11]</sup>, a revision of the proposal, never into the C++26 working draft<sup>[12]</sup>.
6. A description of the record a discharged reconciliation duty produces, each element located in practice in force today, with a WG21 instance of the record being made (Section 9).
7. The assignment of the reconciliation duty to the convenership, and the record of its non-exercise during the adoption arc, read against that description (Section 10).

Three assumptions govern the assessment. First, a paper's printed date fixes what its authors could have known: a source dated after 2025-11-03 cannot retroactively falsify a sentence written by that day. Second, a committee vote establishes procedural disposition without settling a technical question. Third, public sources are the only admissible evidence; a claim resting on unpublished discussion is recorded as unsourced rather than as false.

---

## 2. Resolution, Not Response, Is the Standard P3846R1 Claims

The ISO/IEC Directives define consensus around resolution, not reply. The foreword principles state: "Consensus, which requires the resolution of substantial objections, is an essential procedural principle and a necessary condition for the preparation of International Standards that will be accepted and widely used. Although it is necessary for the technical work to progress speedily, sufficient time is required before the approval stage for the discussion, negotiation and resolution of significant technical disagreements."<sup>[13]</sup> Clause 2.5.6 adopts the ISO/IEC Guide 2 definition, which characterizes consensus as a process "seeking to take into account the views of all parties concerned and to reconcile any conflicting arguments", and adds: "If the leadership determines that there is a sustained opposition, it is required to try and resolve it in good faith."<sup>[13]</sup> Clause 2.6.5 places the two duties side by side: "Committees are required to respond to all comments received", and "Every attempt shall be made to resolve negative votes."<sup>[13]</sup> Response is the floor. Resolution is the stated obligation.

Disposition practice contains no middle state. WG21's own disposition of comments for the C++20 committee draft, N4858, records three technical outcomes - "Accepted", "Accepted with Modification" naming the adopted paper that resolves the comment, and "Rejected. There was no consensus to adopt this change" - plus an editorial variant, "Accepted - Editorial", for comments routed to the editor.<sup>[14]</sup> ISO/TC 211's good-practice guidance for the enquiry stage instructs editors to elaborate on "Accepted in principle" and "Not accepted" dispositions "to make sure you do not get the same comment the next ballot or even a No vote in the FDIS ballot."<sup>[15]</sup> No recognized category records that a comment was partly answered. For the current cycle, the SC 22 summary of voting for the C++26 committee draft instructs "review and resolution of the comments" and directs the Project Editor to prepare "an approved Disposition of Comments document and a revised text for further processing."<sup>[16]</sup> The deliverables the system expects are resolution and revised text.

The response-resolution distinction comes from the processes themselves. The IETF's consensus doctrine holds that "the existence of the unaddressed open issue, not the number of people" is determinative, and that a consensus finding owes the objector "a reasoned explanation to the person(s) raising the issue of why their concern is not going to be accommodated"<sup>[17]</sup>. ANSI's Essential Requirements define a resolved comment as one where "the negative commenter accepts the proposed resolution of his/her comment"<sup>[18]</sup>. W3C's process defines "formally addressed" as a public, substantive response whose adequacy "is measured against what a W3C reviewer would generally consider to be technically sound"<sup>[19]</sup>. Three peer processes impose an adequacy test on the response itself; none recognizes a reply that leaves the objection standing as a disposition. Each test is also stated from the objector's side: what the objector can read, accept, or contest.

These provisions bind the standards process at two levels, the national body ballot and the plenary. P3846R1 is a working group paper, and no directive obliges it to meet the ballot-stage standard as a document. The definition of resolution nonetheless supplies the test for its claim, for two reasons. The paper's own abstract asserts that the objections were addressed, and "addressed" must mean something; the Directives define what the standards process means by resolving an objection. And the objections P3846R1 answers include national body comments on the C++26 draft, the same objections now before the national bodies at the Draft International Standard (DIS) ballot, where the resolution standard governs outright.

Under that standard, a response to a formal objection resolves it in one of three ways:

1. **Resolution by change.** The draft text is modified, and the commenter confirms the change resolves the concern.
2. **Resolution by explanation.** The committee gives a substantive, reasoned response whose evidence suffices for its stated conclusion and engages the objection's central mechanism.
3. **Disposition by recorded decision.** The committee rejects the concern by a recorded consensus with a stated rationale, converting the objection into a voted outcome.

A response that explains a tradeoff while leaving a material technical issue open does none of the three. It is a reply, and the Directives' vocabulary already has a place for replies: the floor. The assessment below tests each of the eighteen responses against these three forms. Whether the authors' rationale paper, P2899R1<sup>[24]</sup>, itself satisfies the third form is taken up as an expected objection in Section 8.

---

## 3. Method: Three Independent Fields at Two Cutoffs

Two cutoff dates fix which public record each claim is tested against, and three fields score every concern; the fields answer different questions and are never combined. Public statements after both cutoffs enter only as later corroboration of how the response corpus continued to function, are identified as such where used, and change no score.

The audited artifact is the P3846R1 PDF published in the April 2026 WG21 mailing<sup>[1]</sup>: 494,439 bytes, SHA-256 `0cbbdc9c27987d5694b5d4f6d48d97c3244d8c40a547225ce79cf060bd46035c`. The artifact prints "Date: 2025-11-03" on its title page; its PDF metadata reads 2026-03-23, its tracking issue records "Authors provided updated version" that day<sup>[20]</sup>, and the official 2026 index dates it 2026-03-23<sup>[21]</sup>. The printed date is the substantive cutoff: sources dated on or before 2025-11-03 test whether the responses were accurate when written. The build date is the publication-state cutoff: sources dated between the two test whether the artifact was current when supplied. Evidence after 2026-03-23 enters no score. No public artifact establishes that text byte-identical to the audited PDF circulated on the printed date: the 2025 index lists no P3846R1<sup>[22]</sup>, and the Internet Archive holds no capture of any P3846R1 before June 2026. The dual-date treatment is a disclosed method and makes no claim about the authors' intent.

The quotation record has a different and narrower purpose from the scores. Statements by P3846R1 authors are selected when they show an objection acknowledged alongside a prior-response pointer, poll, consensus claim, roadmap boundary, timing rule, or future-work answer. They establish how the response corpus was used; they do not establish the authors' motives. A statement after 2026-03-23 may corroborate that later function or describe later work; it cannot supply missing support for P3846R1 or retroactively resolve an objection at either cutoff.

Overall support rates the complete response against the record at the cutoffs, on five values: Supported, Substantially supported, Mixed, Not supported, Contradicted, where Mixed means material support and material weakness both affect the central response. The unsupported-subclaim flag is a separate yes/no field, set when the response contains a specific material assertion - factual, causal, quantitative, or historical - that lacks support or is false, regardless of the complete response's rating. Resolution status answers a third question: whether the response meets the original objection on its own terms. "Answered" means the supported response meets the stated objection. "Partly answered" means the response explains a tradeoff or documents a procedure while leaving a material technical issue open. "Not resolved" means the response does not meet the objection's central mechanism or evidence. A committee vote establishes procedural disposition; it does not by itself convert a technical status from Not resolved to Answered. The fields are separate because combining them produces two characteristic errors: treating one incorrect sentence as the failure of an entire response, and treating a committee decision as proof of a technical proposition.

The evidence standard is symmetric and limits both sides alike. Expert testimony may support a qualitative judgment when public and attributed; it cannot support an unattributed quantitative comparison. A coding rule proves recognition of a risk, not frequency. Evidence made public after the build-date cutoff cannot retroactively support a printed sentence; it can support a future revision. Poll tallies come from the chair-posted threads on the public cplusplus/papers tracker, because no published minutes record subgroup straw-poll tallies. The Hagenberg minutes direct readers to the tracker<sup>[23]</sup>, and the rationale paper corroborates each tally where that paper records the same poll<sup>[24]</sup>. This standard is the author's own construction, and the author has a material stake in the question under assessment, as the Disclosure records. If the standard is rejected, the quoted sentences and cited artifacts stand independently of the rating scheme, and the resolution column rests on the Directives' definition rather than on the author's.

Three limitations bound what the counts can mean; Section 5 states concern-level caveats in place. No public artifact establishes the November text's byte identity with the March PDF. The search for one claimed compiler prototype has one stated recall gap: the gcc.gnu.org web archives sit behind an interactive bot filter, so a gcc-patches posting describing the prototype would not have been found. And the ratings are judgments rather than measurements; another reviewer applying the same standard could move a boundary case one category.

---

## 4. The Scorecard: Authors Favored on Support, the Objecting Position on Resolution

**Table 1. Assessment of the eighteen P3846R1 responses. Overall support rates the complete response against the public record at the cutoffs of Section 3. Unsupported subclaim records whether the response contains a material unsupported factual, causal, quantitative, or historical assertion. Resolution records whether the response meets the original objection on its own terms. The three fields are independent by construction.**

| Concern | Overall support | Unsupported subclaim | Resolution |
|---|---|---|---|
| 1. Safety and non-ignorable checks | Mixed | Yes | Partly answered |
| 2. Cross-translation-unit semantics | Mixed | Yes | Partly answered |
| 3. Dependency management | Mixed | Yes | Partly answered |
| 4. One Definition Rule | Substantially supported | Yes | Partly answered |
| 5. Modules | Supported | No | Partly answered |
| 6. Implementation-defined behavior | Mixed | Yes | Partly answered |
| 7. Uncheckable guidance | Substantially supported | Yes | Partly answered |
| 8. Constification | Substantially supported | No | Answered |
| 9. Global violation handler | Substantially supported | Yes | Partly answered |
| 10. Consecutive assertions | Supported | No | Answered |
| 11. Predicate exceptions | Mixed | Yes | Not resolved |
| 12. Static analysis | Mixed | Yes | Partly answered |
| 13. Complexity | Mixed | Yes | Partly answered |
| 14. Missing features | Substantially supported | Yes | Partly answered |
| 15. Future features | Mixed | Yes | Partly answered |
| 16. Decomposition | Mixed | Yes | Partly answered |
| 17. Deployment experience | Substantially supported | Yes | Partly answered |
| 18. Library hardening | Mixed | Yes | Partly answered |

The counts are two Supported, six Substantially supported, ten Mixed, zero Not supported, and zero Contradicted. Fifteen responses receive the unsupported-subclaim flag. The resolution counts are two Answered, fifteen Partly answered, and one Not resolved. Converting these counts into a percentage of objections settled would misstate them: the support column rates responses rather than objections, and the resolution column records an evaluative judgment against the stated criterion.

The two axes diverge. On overall support, the scores favor the authors of P3846R1: eight responses receive favorable ratings, ten are Mixed, and no complete response is Not supported or Contradicted. On resolution, the verdicts favor the objecting position: two objections are Answered, fifteen are Partly answered, and one is Not resolved.

---

## 5. The Eighteen Concerns

### 5.1 Two fully supported responses

**Concern 5: Modules.** The objection is that P2900 does not work well with modules; P3835R0 asks whether modules could address the configuration of contract-evaluation semantics<sup>[3]</sup>. P3846R1's response is bounded and stated in bounded terms: "In principle, inline functions in a BMI could carry additional information, such as contract-evaluation semantics" (p. 16), with the same paragraph limiting the claim to "only a partial solution to the broader problem" (p. 16). GCC's module serialization change implements the bounded information-carrying described, streaming references to the outlined precondition and postcondition helpers and appending a boolean to the built-module-interface dialect string; it was merged into GCC master on 2026-01-28<sup>[25]</sup>. No evaluation semantic is written to or read from a module interface anywhere in the change, so the practical question of who controls the semantic across module boundaries remains open. Supported, no unsupported subclaim. Partly answered: the architectural avenue exists at the level claimed, and the practical question remains.

"The interaction between P2900 and modules was previously raised in [P3573R0], responded to in [P3591R0], and further discussed in EWG in Hagenberg. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The Discussion Status closes through a previous response, prior discussion, and absence of new information while the response itself calls modules "only a partial solution." The quotation establishes the function of the status entry without changing the favorable support rating.

**Concern 10: Consecutive assertions.** The objection is that observing consecutive assertions is dangerous, because an earlier assertion may be a precondition for safely evaluating a later one. The response supplies a mechanism, a counterexample, and a committee record: "The idiomatic solution is to combine dependent predicates into a single assertion, thus avoiding the risk of evaluating the second condition after the first fails" (p. 23), with the residual risk stated in the same response. Short-circuit conjunction works for the canonical case. The Contracts Study Group (SG21) polled the proposed alternative, automatically skipping subsequent assertions, on 2025-02-06 and declined it: SF 0, F 0, N 1, A 13, SA 7, "Consensus against"<sup>[26]</sup>, corroborated by the rationale paper<sup>[24]</sup>. The proposal itself states that no general method distinguishes related predicates from unrelated ones<sup>[27]</sup>. Supported, no unsupported subclaim. Answered: a working mitigation for the canonical case, a counterexample against the alternative, and a recorded committee decision declining that alternative.

"The observe semantic is an indispensable tool when introducing new contract assertions into existing code, but continuing past a failed assertion always comes with a risk." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup> In the public discussion, the same issue drew a pointer back to the paper: 'See P3846R0, Concern 10 "Observing consecutive contract assertions is dangerous".' ([Timur Doumler](https://lists.isocpp.org/sg15/2025/10/2744.php))<sup>[28]</sup>

Here the reference back to P3846 accompanies a working mitigation and a recorded decision. This is the control case: process records closure because the response also meets the objection's mechanism.

### 5.2 Six supported central claims, each with a material limit, one resolved objection

**Concern 4: One Definition Rule.** The objection is that P2900 violates the spirit of the One Definition Rule. The response classifies the reported failure as a general compiler defect: "both Clang (LLVMPR26774) and GCC (GCCBug70018) disabled them nearly a decade ago" (p. 15), and the behavior reported in P3829R0 is "a regression of the same issue in GCC 14, entirely unrelated to contract assertions" (p. 15). The classification holds: Clang's fix was committed on 2016-04-08<sup>[29]</sup>, GCC's appeared in the GCC 7 series<sup>[30]</sup>, and the 2025 bug's reproducer contains no contract assertion and no contracts flags<sup>[31]</sup>. The performance dismissal does not hold: the response states that such concerns are "equally unfounded" and that "Clang made this tradeoff long ago without user complaints" (p. 15), yet the cited bug contains Jan Hubi&ccaron;ka's report that "these optimisations may have a large performance impact", with one workload where the optimization "improved jpeg-xl encoding speed by 47%"<sup>[31]</sup>. Thirty-nine days after the Clang fix, Warren Ristow filed the report now numbered LLVM issue 28170, resolved in 2018 without relaxing the conservatism<sup>[9]</sup>. The same bug's comment 9 enumerates "contract checking mode" among the defect's triggers, and the GCC contracts implementation includes a dedicated default-on workaround, merged with the note that it suffices "while a suitable general fix is evaluated"<sup>[31]</sup><sup>[32]</sup>. Contracts exposed the defect and required operational mitigation, which does not make the defect a contracts design issue. Substantially supported; "equally unfounded" is a material unsupported subclaim, contradicted by a source the response cites. Partly answered.

"EWG, in Hagenberg, considered the general concerns regarding mixed mode and rejected altering the ODR for contract assertions. The specific issue with interprocedural optimisation in GCC was discussed only on the reflector, where it was identified as a compiler bug unrelated to P2900." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The status pairs an EWG decision on general ODR policy with a reflector-side classification of the specific GCC mechanism. The authors' rationale paper describes the EWG decision in its own terms: "EWG took a deliberately vaguely worded poll to gauge the interest of the room to 'do something about it'; the result was consensus against" (P2900: add ODR to contracts, SF 6, F 5, N 10, A 25, SA 17). ([P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf), Section 3.5.11)<sup>[24]</sup> A poll its proposers describe as deliberately vague, taken to gauge interest, is the decision the status invokes.

**Concern 7: Uncheckable guidance.** The objection is that P2900 relies on guidelines the compiler cannot check. The response separates design from frequency: the constraint "is not specific to P2900's design" (p. 19), enforcing it would reject most useful expressions<sup>[33]</sup>, and "Decades of experience with these facilities have shown that destructive side effects from predicates are easily identified during development and testing and are rarely an issue" (p. 19). The cited analysis supports the design half<sup>[33]</sup>. The frequency half supplies no data, survey, or defect study, and the counter-evidence is equally bounded. CERT's PRE31-C rule recognizes the bug class while labeling its likelihood "Unlikely" in its own risk table<sup>[34]</sup>. The two static-analysis checks in this class target other languages: SonarQube S3346 is a C# rule and PVS-Studio V6055 is a Java diagnostic<sup>[35]</sup><sup>[36]</sup>. Substantially supported; "rarely an issue" is a material unsupported subclaim. Partly answered.

"The desire to produce rules that a compiler can enforce to restrict predicates to only those that are nonproblematic has been put forth in papers such as [P2680R1], [P3285R0], and [P3362R0]. These papers have been given ample committee time and not achieved consensus. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The status entry records committee time, failed consensus, and absence of new information. None supplies the frequency evidence on which the response's practical dismissal depends. The rationale paper records the committee time in its own words. Of the Wroc&lstrok;aw poll on strict predicates (SF 10, F 6, N 3, A 14, SA 16): "EWG had consensus against pursuing this direction, although sustained opposition to that decision remained," with the recorded result "Consensus against, but P2900 would be in danger of failure in plenary." Of the Hagenberg poll "P2900: reduce the amount of Undefined Behavior in contracts" (SF 9, F 7, N 9, A 22, SA 19): "The group took a poll to do 'something' about this concern." ([P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf), Section 3.6.1)<sup>[24]</sup>

**Concern 8: Constification.** The objection is that const-ification changes the meaning of predicates, complicates teaching, and obstructs automatic assertion insertion. The response reports that "No compelling real-world examples of correct assertions rendered incorrect by const-ification have been produced" (p. 20) and that const-ification "revealed genuine bugs in existing libraries" (p. 20). The migration record supports it: applied to BDE, the experiment found six assignment-versus-equality defects<sup>[37]</sup>; applied to LLVM, approximately seventy-five const-correctness defects before about 98.5 percent of assertions compiled<sup>[38]</sup>. EWG retained the feature through two removal polls, at Wroc&lstrok;aw in November 2024 and at Hagenberg in February 2025, with the wider margin against the stronger question<sup>[39]</sup><sup>[40]</sup>.

The rationale paper records the complete decision chain with its reasons: SG21 adopted the rule on 2023-12-14 (SF 6, F 10, N 3, A 0, SA 0). EWG at St. Louis polled removal at SF 9, F 5, N 4, A 10, SA 5, "No consensus for change but a strong divide". SG21 declined two removal proposals on 2024-05-16 and voted to retain on 2024-10-10 (SF 3, F 1, N 2, A 10, SA 8, consensus against removal) while extending the rule to all variables (SF 6, F 14, N 2, A 0, SA 3). EWG then voted against removal at Wroc&lstrok;aw (SF 10, F 4, N 9, A 19, SA 12) and at Hagenberg (SF 9, F 7, N 6, A 37, SA 14). The same section states both tradeoffs the objection names, non-const-correct APIs and overload resolution differing inside and outside predicates, records that the confusion concern was weighed as early as P2388R0, and records the migration studies<sup>[24]</sup>. The limits preserve part of the objection: the BDE result is attributable to const-ification and the restricted predicate grammar together<sup>[37]</sup>, and the teachability question is answered by analysis rather than demonstrated harmlessness. Substantially supported, no unsupported subclaim. Answered: a mechanism with a stated purpose, the objection's own tradeoffs weighed on the record, repeated recorded decisions declining the alternative, and migration evidence. This is the one concern besides Concern 10 where Section 2's second and third forms are both on the record.

"In Wroc&lstrok;aw, EWG reached consensus against removing const-ification, which was reaffirmed in Hagenberg. The concern in [CZ 4-058] that const-ification could increase the difficulty of automatic assertion insertion by tooling and that const-ification could be replaced with erroneous behaviour are new. Otherwise, no new information has been presented since Wroc&lstrok;aw." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The status entry acknowledges two new forms of the objection, then records the earlier retention decisions. Those decisions dispose of the objection as stated. The two new forms P3846R1 itself identifies, automatic insertion by tooling and replacement with erroneous behaviour, are recorded here as residual: they postdate the decisions and are not yet answered, and they do not reopen the question the decisions settled.

**Concern 9: Global violation handler.** The objection is that a global contract-violation handler is problematic. The response grounds its analogy in the standard library: "C++ already includes several global handlers for this purpose (e.g., std::set_new_handler, std::set_terminate, signal handlers), and similar mechanisms are widely and successfully used in major frameworks such as Qt and in game engines" (pp. 22-23). The standard-library half stands, and the production history sits inside the response's own cited sources: BDE deployed user-provided violation handlers in 2004 and continued using them<sup>[41]</sup>. The Qt and game-engine half names no deployments and no outcomes. Substantially supported; the Qt and game-engine success claim is a material unsupported subclaim. Partly answered.

"The global contract-violation handler was adopted into P2900 when SG21 approved [P2811R7], and it had consensus in EWG. Local violation handlers have been proposed in [P3400R1] as a post-C++26 extension. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The entry answers through adoption history and a future extension. The poll establishes the selected design, while the unsupported deployment claim and the case for local control remain outside that disposition.

**Concern 14: Missing features.** The objection is that P2900 lacks important features. The response is an incremental-delivery argument with one categorical sentence: "All the requested features have been discussed in various papers; no proposals that included them gained consensus in EWG" (p. 28). One page later, the same section records the exception that falsifies the sentence: "pre and post on virtual functions do have a proposal ([P3097R0]) that is fully specified, has been reviewed and approved with strong consensus in EWG, has been reviewed by CWG, has been implemented in GCC, and could be re-added to the C++ working draft any time EWG wishes to do so" (pp. 29-30). EWG at St. Louis in 2024 polled merging P3097R0 into P2900: SF 18, F 15, N 5, A 1, SA 2, recorded as consensus<sup>[42]</sup><sup>[24]</sup>. The feature entered P2900R8, a revision of the proposal, never the working draft, and was struck at Hagenberg before P2900R14 entered the draft<sup>[40]</sup>. The authors' own rationale records both events: "support for virtual functions was added to the Contracts proposal in revision [P2900R8]" after the St. Louis poll, and Hagenberg's "disallow pre/post contracts on virtual functions entirely" (SF 20, F 24, N 13, A 14, SA 2) "reversed EWG's previous decision in St. Louis" (Section 3.3.2)<sup>[24]</sup>. The incremental-delivery argument around the defective sentence is substantive, and it supports extensibility without giving users the capabilities in C++26. Substantially supported; the categorical consensus sentence is a material unsupported subclaim, and it is false. Partly answered.

"The lack of syntactic control for contract assertions is certainly a concern, but the ability to introduce such things is a layer of complexity that has been explicitly left to future proposals that build on top of [P2900R13]." ([Joshua Berne and Timur Doumler, P3591R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3591r0.pdf))<sup>[43]</sup> The same use case was later answered by pointing to P3400 and adding: "We've also spent a lot of time in SG21 and EWG polling what features to target as part of the initial MVP and what features should be left until later, and the Contracts feature in the working draft today is the result of that decision making." ([Joshua Berne](https://lists.isocpp.org/sg15/2025/10/2980.php))<sup>[44]</sup>

The first quotation acknowledges the gap and assigns it to future work; the second makes the feature-selection polls the reason the C++26 design remains unchanged.

**Concern 17: Deployment experience.** The objection is that P2900 has insufficient deployment experience. The response accepts the standard and states its strongest sentence: "Expecting a reasonable level of implementation experience before standardising a novel language feature is good engineering practice that we strongly support. P2900 has been fully implemented in two major compilers." (p. 33). Eight lines later, the same page qualifies both halves: the implementations are "nearly complete" with "upstreaming in progress" (p. 33). The cited implementers' report documents P2900R8, not P2900R14, records complementary gaps in the two compilers, and states that "The code has not been merged into any official branch" (p. 5)<sup>[45]</sup>. The Clang status page recorded P2900R14 as not implemented at both cutoffs<sup>[46]</sup>. Between the cutoffs, on 2026-01-28, the base implementation of P2900R14 was merged into GCC master<sup>[47]</sup>. The response's prediction had come true for GCC when the March artifact was supplied, and the artifact's "with upstreaming in progress" was out of date in its authors' disfavor. Both implementations were publicly available on Compiler Explorer at both cutoffs<sup>[48]</sup>, and the response states the remaining gap itself: "While it has not been deployed to production, neither has any other major language feature adopted by C++ in any previous or current Standard" (p. 33). Substantially supported; "fully implemented in two major compilers" is a material unsupported subclaim as applied to P2900R14. Partly answered.

"This concern repeats earlier objections ([P3173R0], [P3506R0], [P3573R0]) already considered repeatedly in EWG. No new information has been presented since." The same response states: "Deployment experience with the entire feature set of P2900 is admittedly still limited, in particular with pre and post." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup> In public discussion, such deployment was called valuable and then declined as a prerequisite: "I don't think that's a reasonable expectation for a new language feature, and I don't remember this high bar ever having been applied for any other language feature we have standardised in the past." ([Timur Doumler](https://lists.isocpp.org/sg15/2025/10/2909.php))<sup>[49]</sup>

The requested evidence is admitted to be limited, while repetition, novelty, and the reasonableness of the evidentiary bar perform the closing work.

### 5.3 Ten responses where support and weakness are both material

**Concern 1: Safety and non-ignorable checks.** The objection is that contract assertions make C++ less safe because they can be switched off. The response's strongest claim: "The ability to configure their evaluation semantics externally is a prerequisite for widespread adoption, not a defect" (p. 6), grounded in adoption history "as proven by decades of successful use of C assert" (p. 7). The narrower claim has documented support: production settings where observing or disabling assertions reduces outage risk<sup>[50]</sup>, and production, gaming, low-latency, server, and high-performance-computing environments with conflicting enforcement needs<sup>[51]</sup>. The categorical prerequisite claim has none: no study, survey, or usage data links the ignore mechanism to the adoption, and historical coexistence does not establish causation. The Rust comparison available to the objecting side is bounded in both directions: Rust checks a fixed class of operations and permits source-level bypass, and the 2021 study of restoring elided checks found little, no, or negative benefit in 76.4 percent of tested benchmarks and meaningful gains in 23.6 percent<sup>[52]</sup>. The November 2025 Android report describing checked-by-default Rust at scale<sup>[53]</sup> postdates the printed date and qualifies only the March artifact. Mixed; the prerequisite claim is a material unsupported subclaim. Partly answered.

"Ville is correct in pointing out that this is indeed a consequence of the proposal, and we should make sure that this is really what we want before we standardise it (or reverse course if it is not what we want)." The same message continues: "It would be amazing to get actual hard data on this that could inform our opinion." After describing the discussion as subjective, it assigns the burden by the prior vote: "Overturning such strong consensus should normally require some significant new information, which I am not seeing in the current discussion." ([Timur Doumler](https://lists.isocpp.org/sg15/2025/10/2786.php))<sup>[54]</sup> The companion paper assigns non-ignorable checks to a later cycle: "this extension is realistically too nontrivial to be approved in the C++26 timeframe and will have to target C++29." ([Doumler, A&zcaron;man, Berne, and McDougall, P3500R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3500r1.pdf))<sup>[51]</sup>

The first statement acknowledges the consequence and the missing data before making consensus the reason not to revisit it; the second answers the requested C++26 capability with future work.

**Concern 2: Cross-translation-unit semantics.** The objection is that P2900 provides no consistent semantics across translation units compiled with different evaluation semantics. The response is a five-item strategy list requiring no change to P2900's specification, with the naive strategy's worst case scoped and qualified: "The worst case (barring compiler bugs such as those described in Concern 4) is that a contract assertion intended to be checked is instead ignored, which is no worse than if contract assertions did not exist" (p. 10). The qualified sentence is accurate as written, and the naive strategy is implemented in both compilers<sup>[45]</sup><sup>[55]</sup>. The record contains no public artifact for the two claimed prototypes. The response reports deferred selection as "prototyped in GCC" with link-time optimization that "has been shown to work reliably in the GCC prototype" (p. 10). Yet GCC's complete contract option table contains no link-time, load-time, or runtime selection option at either cutoff<sup>[55]</sup><sup>[56]</sup>. A web and GitHub search for contracts-ABI implementations locates exactly one public repository, consisting of a README frozen since 2025-06-27<sup>[57]</sup>.

The authors' own rationale fixes the baseline. On 2025-03-14 it stated of both compilers: "Neither implementation currently does anything to influence the chosen version of an inline function with multiple definitions, so any non-inlined evaluation of such a function will have one of the possible behaviors (though which is unspecified and depends on the linker)" (Section 2.10), and: "At the moment, implementations of Contracts in both GCC and Clang support per-translation-unit configuration of contract semantics... Work is in progress to add support for choosing caller-side evaluation in GCC" (Section 3.5.5)<sup>[24]</sup>. Caller-side evaluation is not deferred selection. Any deferred-selection prototype therefore postdates March 2025, and none appears in the public record by either cutoff. The response states the residual gap itself: on the naive implementation, "users who do not fully control their build environment cannot reliably predict which evaluation semantic applies to non-inlined calls to f" (p. 10), and the strategy taxonomy records that mixed modes can reduce the minimum evaluation count to zero<sup>[58]</sup>. Mixed; the claimed prototypes are a material unsupported subclaim, an existence claim no located public record contains, per the search scope and stated recall gap of Section 3. Partly answered.

"I agree that the problem you highlighted exists. I don't think anybody dismisses the existence of the problem." The same message then introduces the P3846 option set with: "Now, as described in P3846, there are only three ways to address the problem:" and gives as its first option "Accept that the problem exists and standardise P2900 anyway because it provides value to users despite the existence of the problem" ([Timur Doumler](https://lists.isocpp.org/sg15/2025/10/2782.php))<sup>[59]</sup>.

The rationale paper records the same acceptance eight months before P3846R1's printed date, as a trilemma: "satisfying all three simultaneously turns out to be impossible in this specific case. A conforming implementation of [P2900R14] inevitably needs to give up on one of the following items" - deterministic behavior in mixed mode, zero overhead on ignored assertions, or compatibility with current linkers - and adds that the problem "is unrelated to Contracts, has existed before Contracts, and is not made worse by Contracts." ([P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf), Section 3.5.11)<sup>[24]</sup>

The proposed first disposition is acceptance of the problem rather than removal of its mechanism. The quotations are unusually direct evidence for the difference between acknowledging an objection and resolving it. P3846R1's five-strategy list does not say which leg of the authors' own trilemma each strategy gives up; by that analysis, the deferred-selection and link-time strategies give up linker compatibility or zero overhead.

**Concern 3: Dependency management.** The objection, raised by P3849R0, is that contracts "introduce several new build configurations, but we have not yet seen concrete examples of how they interact with real-world build systems or complex dependency graphs."<sup>[5]</sup> The response answers with a replacement argument - "P2900 introduces no new configuration dimension" (p. 11) - and an example: "Boost.Build already added such support on top of the available GCC and Clang implementations of P2900. Adding this support took less than an hour of implementation effort" (p. 12). The example is genuine: the commit contains 149 additions across 9 files with a correct flag mapping<sup>[60]</sup>, and its example repository demonstrates the per-translation-unit model across the ignore-and-enforce combinations for static linking, with the shared-library case commented out from file creation<sup>[61]</sup>. The elapsed-time figure is the author's own unwitnessed report about his own work; the commit author is both the B2 maintainer and a P3846R1 coauthor, a disclosure fact that does not invalidate a public commit.

The response does not establish that implementation freedom and the Boost.Build example address complex dependency graphs. The package-manager case depends on a mechanism the example does not exercise: the rationale paper lists as the first use case for implementation-defined selection "Package managers and other forms of packaged software, which should not be forced to distribute a different binary for each possible evaluation semantic," resting on "the requirement that a conforming Contracts implementation should be allowed to enable and disable contract checks without requiring a rebuild," and records in the same section that only per-translation-unit configuration existed in either compiler (Section 3.5.5)<sup>[24]</sup>. Per-translation-unit flag mapping is what the B2 commit demonstrates, and it is the one mechanism that does not deliver the package-manager benefit; the link-time, load-time, and run-time selection that would deliver it is the unimplemented mechanism of Concern 2. Mixed; the elapsed-time figure is a material unsupported subclaim. Partly answered.

The status is procedural: "These topics were explored in [P3321R0] and discussed by SG15 in Wroc&lstrok;aw, with no concerns raised by that group. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup> The earlier analysis states the mechanism directly: "A Contracts design that requires build-time decisions regarding whether contracts are evaluated and what the consequences of contract violation are creates a significant burden for package managers." ([Joshua Berne and Tom Honermann, P2877R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2877r0.pdf))<sup>[50]</sup>

The earlier paper argued for the per-translation-unit model to reduce that burden, and P3846R1 relies on that design plus the Boost.Build example. The reduction the earlier paper sought requires selection without a rebuild, which the authors' March 2025 rationale records as not yet implemented. The Discussion Status answers the broader request for complex dependency-graph evidence through subgroup silence and novelty.

**Concern 6: Implementation-defined behavior.** The objection is that too much of P2900 is implementation-defined. The response explains the platform-dependence rationale and enumerates: "P2900 introduces exactly five implementation-defined properties:" (p. 17). Four of the five map to entries in the incorporated working draft's own index of implementation-defined behavior, but that index lists seven contract-related entries, adding the virtual-destructor choice for `contract_violation`, the `comment()` contents, and the `location()` value, and it was public 233 days before the printed date<sup>[62]</sup>. The omission was not obscure: P3321R0, described in the same paragraph of P3846R1 as discussing "the full list of implementation-defined behaviours" (p. 17), contains a section on the omitted strings<sup>[63]</sup>. The authors' own rationale paper, dated 2025-03-14, lists six: the five P3846R1 names and "Whether the contract_violation object is polymorphic" (Section 2.10)<sup>[24]</sup>. Mixed; "exactly five" is a material unsupported subclaim, contradicted by the authors' own rationale and by the draft the response invokes. Partly answered.

After citing the prior response, EWG discussion, SG15 discussion, and the absence of new information, the response concludes: "None of these implementation-defined behaviours alter the way contract assertions are written nor do any represent an unresolved design gap." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The response declares no unresolved design gap after relying on an inventory its own rationale paper had already counted differently. The platform-dependence rationale remains substantive, and the inventory error does not by itself establish such a gap.

**Concern 11: Predicate exceptions.** The objection, recorded from FI-071, is that no implementation or deployment experience exists for non-Itanium ABIs and that Microsoft considers treating predicate exceptions as contract violations infeasible (p. 25). The response describes the two constituencies its design serves and states: "The approach in P2900 is the only known solution that satisfies both groups" (p. 25), with "The overwhelming majority of predicates are trivially non-throwing" (p. 25) grounded in "our experience" rather than a cited dataset. The mechanism is coherent on its own terms<sup>[43]</sup>. The two documented alternatives satisfy only one constituency each: P3626R0, the lead author's own wording diff prepared so EWG could poll the alternative<sup>[10]</sup><sup>[24]</sup>, and P3909R0, which notes non-Itanium translation costs without specifying a complete alternative<sup>[64]</sup>. On the platform the objection named, the response supplies no implementation or measurement, and none was located in the public record.

The procedural record shows division rather than resolution. SG21 adopted the design on 2023-05-18 (SF 8, F 7, N 2, A 0, SA 1), after two Issaquah polls three months earlier found no consensus either to treat predicate exceptions as violations (SF 7, F 7, N 3, A 3, SA 7) or to propagate them (SF 5, F 5, N 4, A 3, SA 10)<sup>[24]</sup>. That 2023 decision adopted a design; it could not supply evidence about a platform, and FI-071's 2025 objection is evidentiary: no implementation or deployment experience on non-Itanium ABIs, and a vendor report of infeasibility. EWG at Hagenberg then polled unconditional unwinding of predicate exceptions at SF 12, F 18, N 11, A 15, SA 7, "No consensus for change"<sup>[40]</sup><sup>[24]</sup>. Of sixty-three votes cast, thirty favored the change the objection sought, twenty-two opposed it, and eleven were neutral. The twenty-two sufficed to deny consensus for change, and the thirty are sustained opposition to the design as shipped under any reading of the Directives' consensus definition. The authors' own rationale applies that term to the same body of objection, describing the pre-Hagenberg concerns as "restatements of known, sustained opposition to the Contracts design" (Section 2.6)<sup>[24]</sup>. A poll records that division exists; it is not reconciliation, and the record contains no reconciliation attempt after the vote. Mixed; the trivially-non-throwing proportion is a material unsupported subclaim. Not resolved: the response supplies a coherent mechanism for its stated constituencies and no evidence on the interface where infeasibility was reported.

"The same position from Microsoft was raised previously in [P3506R0], addressed in [P3591R0], and given due consideration by EWG in Hagenberg. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

This is the sole Not resolved entry. Its status consists entirely of a prior author response, committee consideration, and novelty; the response reports no implementation or measurement on the ABI the objection names. The rationale paper shows the authors were aware of that ABI's callee-side parameter destruction when specifying where postconditions must be checked (Section 3.5.1), and says nothing about predicate exceptions on it (Section 3.5.6)<sup>[24]</sup>.

**Concern 12: Static analysis.** The objection is that P2900 does not support static analysis. The response argues that declaration-level syntax removes the macro limitations<sup>[65]</sup> and claims vendor activity: "Some static analysis providers (such as CodeQL) are already actively pursuing support for P2900 contract assertions in their tools" (p. 26), with the CppCon work combining "the CodeQL static analyser with the Z3 constraint solver to validate a wide range of contracts" (p. 27). The cited context paper, written by the talk's CodeQL copresenter, states that the prototype targets traditional assertions rather than P2900 contract specifiers, warns against using it to judge the overall feasibility of P2900 static analysis, and records that "the portions of this talk presented by GitHub are not an endorsement of P2900"<sup>[66]</sup>. The prototype repository supports only assertion macros annotated with a bespoke comment syntax and states the forward intent plainly: "In the future, we hope to support C++26 contract specifiers `pre(...)` and `post(...)`"<sup>[67]</sup>. The syntax-level advantages are acknowledged from both directions<sup>[65]</sup><sup>[66]</sup>. Mixed; "validate a wide range of contracts" is a material unsupported subclaim, outrunning the demonstrated prototype. Partly answered.

The status closes through a paper chain and EWG discussion: "These concerns were raised in [P3362R0] and responded to in [P3376R0] and [P3386R1]. All three papers were discussed by EWG in Wroc&lstrok;aw. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup> The temporal tradeoff was stated more directly in public discussion: "Not being able to check all contract assertions is a feature, not a bug, and a way for us to get runtime checks now and a wide range of ever-more-powerful tools in the future." ([Joshua Berne](https://lists.isocpp.org/sg15/2025/10/2991.php))<sup>[68]</sup>

The immediate mechanism is runtime checking and readable syntax; the broader tooling answer remains prospective.

**Concern 13: Complexity.** The objection is that P2900 is too complex. The response reports that complete implementations "were produced relatively quickly by a tiny team" and states: "The implementers reported that P2900 is orders of magnitude simpler to support than modules, concepts, reflection, or even lambdas" (p. 27). The tractability half is documented: the cited implementers' report calls the specification "clear and implementable"<sup>[45]</sup>, and a P2900R14 co-author's later assessment calls the minimal form "fairly simple to implement"<sup>[69]</sup>. The comparative magnitude is not documented: the cited report contains no comparison to the named features, and no measurement or attributed quotation exists<sup>[45]</sup>. Mixed; "orders of magnitude simpler" is a material unsupported subclaim. Partly answered.

"The concern regarding complexity in [P3829R0] mirrors that of [P3573R0], which was discussed by EWG in Hagenberg. No new information has been presented since." The response then offers the adoption result as evidence: "the strong plenary consensus in Hagenberg to include P2900 in the C++26 working draft is further evidence that its value is worth the cost." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The first statement closes through prior discussion and novelty; the second uses the vote as evidence of value while the claimed comparative magnitude remains undocumented.

**Concern 15: Future features.** The objection is that adopting P2900 now forecloses or complicates future features, principally deep const. The response quotes SD-4's rule against delaying concrete proposals for hypothetical alternatives<sup>[70]</sup> and states: "Yet in more than four decades of C++ evolution, no proposal for deep const has ever been brought forward, and it appears doubtful that one will ever materialise" (p. 31). The historical sentence is false: P1974R0 proposes `propconst`, a language-level deep-const qualifier<sup>[71]</sup>, and P2670R1 revises that design line<sup>[72]</sup>. The falsity is narrow: P1974R0 predates P2900 const-ification, and no concrete compatibility analysis between P2900 and a complete deep-const design was located on either side. Mixed; the four-decades claim is a material unsupported subclaim, and it is false. Partly answered.

"Integration with future features was discussed extensively during P2900's development. Requirements were analysed in [P2885R3]; the possibility of deep const was examined in [P3261R2] and rejected via poll in both SG21 and EWG. No new information has been presented since." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The cited polls retained P2900's constification design; they did not reject a complete deep-const proposal or establish compatibility with one. Discussion, polls on the present design, and novelty stand in for the requested compatibility analysis.

**Concern 16: Decomposition.** The objection is that contract assertions could be composed from more primitive features standardized individually. The response identifies concrete omissions in the proposed decomposition - a shared global handler, control over check injection, and the assertion marker tools consume - and states: "The idea to redesign contract assertions as a composition of more primitive features was first proposed in [P1893R0] and subsequently shown to be inadequate for the real-world use cases for contract assertions ([P1995R1])" (p. 32). The attached citation does not support the sentence: P1995R1 catalogs and polls use cases and does not mention or evaluate P1893R0<sup>[73]</sup><sup>[74]</sup>. The identified omissions in the sketch stand unanswered, and a P2900R14 co-author who did not sign P3846R1 argues separately that an atomic assertion marker supports tooling<sup>[75]</sup>. Mixed; "shown to be inadequate" is a material unsupported subclaim by citation mismatch. Partly answered.

"Similar decompositions were proposed to SG21 by [P1893R0] and/or suggested as ideas in EWG but achieved no consensus as the basis for a proposal that meets the use cases P2900 was pursuing. Relaxation of the ODR was polled by EWG in Hagenberg, with consensus against. The specific decomposition proposed in [P3829R0] has not been explicitly discussed in WG21; otherwise, no new information has been presented since Hagenberg." ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>

The actual decomposition is expressly recorded as not discussed. Its Discussion Status nevertheless rests on a poll on one component and the absence of other new information. The authors' own rationale describes that poll as "deliberately vaguely worded," taken "to gauge the interest of the room to 'do something about it'" (Section 3.5.11)<sup>[24]</sup>.

**Concern 18: Library hardening.** The objection is that standard-library hardening cannot depend on contract assertions. The response names the four national body comments seeking decoupling in its first sentence (p. 35), explains that hardening can be specified through the contract-violation model without the literal syntax (p. 36), and states that "Both the libc++ and libstdc++ implementation currently being planned once contracts are available are conforming implementations of C++26 standard-library hardening on top of P2900" (p. 35). Six of its co-authors record the conforming macro approach both libraries use<sup>[76]</sup>. The response also anticipated the committee's later direction, calling the restriction of hardening to the enforce and quick-enforce semantics "a sound decision that the committee could make" (p. 36). Between the cutoffs, the committee made it: P3878R1 was adopted at Kona in November 2025 by unanimous consent in a motion stating that the change "addresses ballot comments RU-016, FR-001-014, FR-010-113, US 3-015, and US 61-112"<sup>[8]</sup><sup>[77]</sup>. The March artifact did not report the compromise adopted more than four months before the artifact was built, and the phrase "on top of P2900" remains ambiguous between the literal syntax and the contract-violation model. The plan's existence is asserted rather than shown: the libc++ half of "currently being planned" is consistent with a co-author's first-person knowledge, but no public record of the claimed libstdc++ plan was located at either cutoff. The macro approach the response's own cited source records for both libraries is not an implementation on top of P2900<sup>[76]</sup>. Mixed; the claimed libstdc++ plan is a material unsupported subclaim, an existence claim no located public record contains. Partly answered.

The response concedes that "the specification of standard library hardening, as it stands now, cannot be implemented purely in terms of the basic feature set in C++26 Contracts," then says that implementation strategies above P2900 are sufficient ([P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf))<sup>[1]</sup>. The rationale states the missing mechanism more directly: "we do not yet have the tools to distinguish contract assertions that should be treated differently in code," and leaves the assertion form to library implementers ([P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf))<sup>[24]</sup>.

The response acknowledges that the needed control is absent from the C++26 facility. Its closure rests on implementation discretion; P3878R1 later restricted which semantics qualify as standard-library hardening.

### 5.4 The fifteen unsupported subclaims

Because overall support is rated separately, each defect changes only the flag: five of the fifteen responses remain Substantially supported and ten remain Mixed, and no flag by itself invalidates the complete response that contains it.

**Table 2. The fifteen material unsupported subclaims in P3846R1, in concern order. Each row quotes the subclaim with its page in P3846R1, states what the public record establishes, and classifies the defect. Concern 3 has two defects of different kinds.**

| Concern | Unsupported subclaim | What the record establishes | Defect kind |
|---|---|---|---|
| 1 | External configurability is "a prerequisite for widespread adoption, not a defect" (p. 6) | Configurability reduces adoption barriers in the environments that asked for it; no study, survey, or usage data links the mechanism to the adoption | Unsourced causal claim |
| 2 | Deferred selection "prototyped in GCC"; link-time optimization "shown to work reliably in the GCC prototype" (p. 10) | No public code, measurement, or build log located; GCC's contract option table contains no deferred-selection option at either cutoff; the authors' March 2025 rationale records per-translation-unit configuration only, with caller-side evaluation the work in progress; search scope and one recall gap stated in Section 3 | Unverifiable existence claim |
| 3 | "Adding this support took less than an hour of implementation effort"; support includes "documentation covering scenarios such as static and dynamic linking" (p. 12) | No public record establishes the duration; the runnable example covers static linking only | Unsourced self-report; claim outrunning its evidence |
| 4 | Performance concerns are "equally unfounded" (p. 15) | The cited bug contains the GCC maintainer's report of a 47 percent gain on one workload and "quite considerable" surrendered opportunity in the narrow case | False statement |
| 6 | "P2900 introduces exactly five implementation-defined properties" (p. 17) | The authors' own rationale paper lists six, adding the polymorphic `contract_violation` choice; the working draft's index lists seven contract-related entries, public 233 days before the printed date | False statement |
| 7 | Destructive side effects from predicates "are rarely an issue" (p. 19) | No frequency data, survey, or defect study; teaching history establishes that the rule is taught, not how often the bug occurs | Unsourced quantitative claim |
| 9 | Similar mechanisms are "widely and successfully used in major frameworks such as Qt and in game engines" (pp. 22-23) | No deployments and no outcomes named for either ecosystem | Unsourced empirical claim |
| 11 | "The overwhelming majority of predicates are trivially non-throwing" (p. 25) | Grounded in the authors' experience; no dataset cited | Unsourced quantitative claim |
| 12 | The CppCon work combined CodeQL with Z3 "to validate a wide range of contracts" (p. 27) | The prototype validates annotated assertion macros only; P2900 specifier support is stated as future hope | Claim outrunning its evidence |
| 13 | "The implementers reported that P2900 is orders of magnitude simpler to support than modules, concepts, reflection, or even lambdas" (p. 27) | The cited report contains no such comparison; no measurement or attributed quotation exists | Unsourced quantitative claim |
| 14 | "no proposals that included them gained consensus in EWG" (p. 28) | P3097R0 gained EWG consensus at St. Louis, a history the same section records one page later | False statement |
| 15 | "no proposal for deep const has ever been brought forward" (p. 31) | P1974R0 proposes `propconst`, a language-level deep-const qualifier, and P2670R1 revises that design line | False statement |
| 16 | The decomposition idea was "subsequently shown to be inadequate" (p. 32), citing P1995R1 | P1995R1 catalogs and polls use cases and does not mention or evaluate P1893R0 | Citation mismatch |
| 17 | "P2900 has been fully implemented in two major compilers" (p. 33) | The cited report documents P2900R8 with complementary gaps and code merged into no official branch; upstream Clang recorded P2900R14 as not implemented at both cutoffs | Claim outrunning its evidence |
| 18 | "the libc++ and libstdc++ implementation currently being planned once contracts are available" (p. 35) | No public record of the claimed libstdc++ plan located at either cutoff; the cited source records the macro approach both libraries use, which is not an implementation on top of P2900 | Unverifiable existence claim |

The defects fall into five kinds: four false statements (Concerns 4, 6, 14, 15), six unsourced claims of magnitude, frequency, cause, duration, or deployment success (Concerns 1, 3, 7, 9, 11, 13), two unverifiable existence claims (Concerns 2 and 18), one citation mismatch (Concern 16), and three claims that outrun their evidence (Concerns 3, 12, 17). The three responses without a flag - Concerns 5, 8, and 10 - were tested against the same standard, and no material unsupported subclaim was found.

---

## 6. What P3846R1's Own Text Records

The items below rest on P3846R1's own text and no external evidence; a delegate can check every one with P3846R1 alone.

The categorical sentence that its own section falsifies. Concern 14 states that "no proposals that included them gained consensus in EWG" (p. 28) and records one page later that preconditions and postconditions on virtual functions "have been reviewed and approved with strong consensus in EWG" (pp. 29-30). The St. Louis poll the second sentence describes is the proposal the first sentence says does not exist.

The strongest sentence that its own page qualifies. Concern 17 states that "P2900 has been fully implemented in two major compilers" (p. 33) and eight lines later describes the same implementations as "nearly complete" with "upstreaming in progress" (p. 33). The cited implementers' report documents an earlier revision with complementary gaps in the two compilers and code merged into no official branch<sup>[45]</sup>.

The gap the response names itself. Concern 2 states of an inline function in a shared header that on the naive implementation "users who do not fully control their build environment cannot reliably predict which evaluation semantic applies to non-inlined calls to f" (p. 10). The four strategies offered beyond the naive one rest on prototypes no public record contains.

The claim stated only conditionally. Concern 5 opens "In principle, inline functions in a BMI could carry additional information" (p. 16) and closes with modules as "only a partial solution" (p. 16). The response is accurate, and the conditionality is the reason the objection remains open.

The concern the revision history adds. P3846R0<sup>[78]</sup> did not address the national body comments asking to decouple library hardening from contracts; P3878R0 recorded that "P3846 doesn't even mention these NB comments, and doesn't address them."<sup>[7]</sup> P3846R1's revision history records the repair: "Added Concern 18 about standard-library hardening in response to [FR-001-014], [US 3-015], [US 61-112] [FR-010-113], and [P3878R0]." The March artifact then did not report the compromise the committee adopted at Kona four months before the artifact was built<sup>[8]</sup><sup>[77]</sup>.

The deferral pattern. Where the responses look forward, they point to work that does not yet exist: the labels proposal "currently being pursued for C++29"<sup>[76]</sup>, the re-addition path for virtual functions, the future linker support of Concern 2. The deliverables the ballot process expects are a disposition and revised text<sup>[16]</sup>, and a promise of future work is neither; a later, post-cutoff objecting paper states the same principle: "An objection answered by a promise of future work is answered only when that work arrives."<sup>[79]</sup>

All three of Section 2's forms occur inside this dispute, and two responses meet one. Concern 10 supplied a working mechanism and a recorded SG21 decision declining the alternative. Concern 8 supplied a mechanism with its tradeoffs weighed on the record and seven recorded decisions declining removal. The same dispute produced a resolution by change: P3878R1 modified the draft, and its authors record that "the submitters of NB comments about standard library hardening confirmed that this change resolves their concerns."<sup>[77]</sup> Fifteen of the eighteen responses stop at explanation, and P3846R1's own text records where each stops.

---

## 7. In Their Own Words

The concern-level quotations show the pattern locally. The statements below show its repeated form across the response corpus and the public discussion around it. They establish that the authors invoked P3846R1 and its predecessors as the place where objections had already been considered and answered. They also establish that the authors invoked repetition, absence of new information, roadmap choices, or a prior consensus as reasons to retain the C++26 design unchanged. They do not establish that any author consciously intended to substitute response for resolution.

### 7.1 P3846 as the Answer

P3846R1 defines its two relevant fields this way:

> "Discussion Status: Whether, when, and/or where this concern was previously considered, and whether we believe any new information has been presented that was not part of earlier consideration"
>
> "Response: A brief explanation of why the concern, when previously considered, did not prevent contract assertions from achieving consensus"<sup>[1]</sup>

The test asks whether the issue was considered, whether information is new, and why the issue did not prevent consensus. It does not ask whether the objection's mechanism was resolved. The introduction then states the result in the past tense: the paper describes "how they have been previously considered, analysed, and addressed" and "clarifies why they fail to justify removing contract assertions" from C++26.<sup>[1]</sup>

Doumler used that function directly in the public exchange over non-ignorable checks:

> "Josh and I did our best to explain this in P3846R0, Concern 1."<sup>[54]</sup>

Doumler routed the live objection to the paper as the existing answer. Cited only as later corroboration, the post-cutoff C++29 roadmap preserves the same bibliography, listing the C++26 objections under "concerns" and P3846R0 among the "responses."<sup>[80]</sup>

### 7.2 Acknowledgment Without Resolution

The clearest statement comes from Doumler's answer to the cross-translation-unit problem:

> "I agree that the problem you highlighted exists. I don't think anybody dismisses the existence of the problem."<sup>[59]</sup>

Doumler then attributes the problem to the C++ compilation model and argues that any feature whose semantics change at build time encounters it. He continues:

> "Now, as described in P3846, there are only three ways to address the problem:
>
> (1) Accept that the problem exists and standardise P2900 anyway because it provides value to users despite the existence of the problem,
>
> (2) Change P2900 to require deterministic semantics across TUs, which means the feature will not work with existing toolchains, which in turn means nobody will adopt it,
>
> (3) Not standardise P2900 or any other such feature at all."<sup>[59]</sup>

The problem is acknowledged without dispute. The first listed answer is to accept it and standardize the design unchanged. Berne described the same residual outcome and placed the controls outside the standard:

> "The *only* negative possibility is that you thought you (the person building the program) had built a function one way but it turns out that you (the person building the program) also built it a different way in a different TU and so you get the semantic from that TU. That's exactly what we can get with linker technology today, and in the future we can both educate people better about making bad assumptions that they are in control of things they are not in control of and we can provide more options (in tooling, outside the standard, and all fully conforming with C++26 Contracts) to give them the controls they want."<sup>[81]</sup>

The same post also points to linker technology available today, says vendors may reject or warn about mixed configurations, and says implementations need not support mixed mode. Those controls are permitted rather than required by the standard; the controls in the quoted sentence remain future education and tooling outside it. In P3846R1 itself, the resulting inability to predict which semantic applies remains stated as a fact, while the Discussion Status says the concern was addressed in a previous author response and presents no new information.<sup>[1]</sup>

### 7.3 Polls and Consensus as Disposition

P3591R0 described its purpose in terms stronger than response:

> "Readers of those papers might mistakenly conclude that these concerns are new and profound flaws in the proposed Contracts facility and have not been previously discussed and addressed. In this paper, we present the missing background and facts related to each of the concerns raised; we describe how all the concerns have been discussed, how consensus was reached on their solutions, and why [P2900R13] is more than ready to be included in the C++ Standard."<sup>[43]</sup>

The rationale later described the treatment of strict predicates:

> "At this point, the topic of 'strict contracts' was closed as far as SG21 was concerned. However, when the Contracts proposal was forwarded to EWG for the WG21 meeting in March 2024 in Tokyo, the author of [P2680R1] published [P3173R0], repeating the concerns and targeting EWG directly. EWG showed significant interest in pursuing the general concern raised."<sup>[24]</sup>

The first group considered the topic closed; the next group showed significant interest in the same concern. The same rationale names its own category for the papers that followed: "A comprehensive response to all these concerns was published in [P3591R0]."<sup>[24]</sup> In October 2025, Doumler made his proposed evidentiary rule explicit. After writing, "It would be amazing to get actual hard data on this that could inform our opinion," and describing the discussion as "entirely subjective," he continued:

> "It makes more sense to me to put that onus on the people who seek to overturn the very strong consensus (100 in favour, 14 against) that we had in Hagenberg for including contract assertions as designed in C++26. Overturning such strong consensus should normally require some significant new information, which I am not seeing in the current discussion."<sup>[54]</sup>

Doumler argues that the prior vote should shift the evidentiary burden. That is a defensible rule for reconsideration; it is not evidence that the acknowledged consequence was resolved.

### 7.4 Roadmap, Mandate, and Timing

For missing features, P3846R1 begins with the roadmap:

> "The lifetime of P2900 really began when SG21 agreed to follow the path in [P2695R1] to pursue a specific plan to gain consensus on a minimal viable product (MVP) for contracts in C++. Starting with an MVP enables us to provide an already-standardised foundation on which consensus can be built for higher-level features that come later."<sup>[1]</sup>

For interaction with future features, the paper invokes a procedural bar:

> "Procedurally, delaying the standardisation of P2900 due the concerns of [P3829R0] about interactions with hypothetical proposals would be against WG21 practice."<sup>[1]</sup>

Berne applied the same division between MVP and later work to source-level semantic control:

> "We've also spent a lot of time in SG21 and EWG polling what features to target as part of the initial MVP and what features should be left until later, and the Contracts feature in the working draft today is the result of that decision making."<sup>[44]</sup>

The roadmap and polls explain why the feature set has its present boundary. They do not supply the capabilities assigned to the later layer or the compatibility analysis assigned to a future design.

### 7.5 Future Work as Closure

P3846R1's conclusion places present and future addressing side by side. It says the paper contains "a description of how each concern is addressed in C++26" and "pointers to future (in-progress) proposals that will expand the use cases covered and further address any remaining concerns"<sup>[1]</sup>. It then concludes:

> "We hope that the detailed analysis provided herein demonstrates that the latest objections are neither new nor indications of fundamental flaws in the design of P2900. This design has already achieved strong consensus within WG21 and deserves to remain in C++26 as one of its cornerstone features."<sup>[1]</sup>

The same corpus records what the future work must provide. Non-ignorable checks were too late for C++26;<sup>[51]</sup> syntactic control was "explicitly left to future proposals";<sup>[43]</sup> local handlers were a post-C++26 extension;<sup>[1]</sup> and deployment with the complete feature was admitted to remain limited.<sup>[1]</sup> These statements can justify incremental delivery. They cannot also establish that the objections to the absent capabilities were resolved in C++26.

### 7.6 Later Confirmation

The authors' C++29 roadmap, published after both scoring cutoffs, cannot support or alter any rating in this paper. It corroborates the distinction between an existing response record and substantive work that remained:

> "For concerns raised during the C++26 standardisation phase, see [P3173R0], [P3478R0], [P3506R0], [P3573R0], [P3829R0], [P3835R0], [P3849R0], [P3851R0], [P3911R2], [P4044R0]; for responses, see [P3500R1], [P3591R0], [P3846R0], [P3912R0], [P3946R0]."<sup>[80]</sup>

The same paper states:

> "The feature set included in C++26 provides a solid foundation, but lacks a number of extensions needed to support additional use cases for which there is already a demonstrated need. In particular, further work is required to make contract assertions truly usable at scale: in very large codebases, across libraries developed and distributed independently, and in specialised environments such as safety-critical systems. This is by design."
>
> "Our other goal for C++29 is to address most, if not all, concerns that were raised repeatedly during the C++26 standardisation phase."<sup>[80]</sup>

P3850R1 categorizes P3846 as a response, while the repeated concerns and capabilities needed for use at scale remain assigned to C++29. The authors' later account therefore corroborates that distinction: the response record existed, and the work needed to meet the concerns continued.

---

## 8. Expected Objections

Three objections to this assessment deserve their own section, each stated in its strongest form. The first is structural. Almost any response to a design objection leaves a material technical issue open, so a distribution of fifteen partly answered out of eighteen is a property of the rubric rather than a finding about P3846R1. The rubric never states what "Answered" would require. Objections that express priorities rather than technical questions cannot be resolved technically by construction. The second is P3846R1's own hedge: its abstract qualifies the closure claim with "Some of the concerns are legitimate yet unavoidable with any viable assertion facility. Others reflect misunderstandings of the proposal, leading to inaccurate observations." (p. 1), so on this reading P3846R1 never claimed to resolve all eighteen, and measuring it against a resolution standard grades a claim it disclaimed. The third is the rationale paper: P2899R1<sup>[24]</sup> provides, for each section of P2900R14, "a summary of the motivation for the proposed design, a history - as complete as possible - for the design decisions in that section," together with "polls that were taken and their results as called by the chair at the time" (Section 1), so on this reading Section 2's third form, a recorded decision with a stated rationale, already exists for every design decision the objections attack, and this paper cites that document eight times for tallies while denying it the status it claims.

The standard is not the rubric's. Section 2's three forms come from the ISO/IEC Directives and from disposition practice rather than from the three fields of Section 3. A response resolves an objection by changing the draft with the commenter's confirmation, by an explanation whose evidence suffices for its conclusion, or by a recorded decision with a stated rationale. The rubric's definition of "Answered" - the supported response meets the stated objection on its own terms - is the same test stated for a single response.

The three forms are not theoretical, and this dispute produced all three. Concern 10 was answered by a mechanism plus a recorded decision. Concern 8 was answered by a mechanism whose tradeoffs were weighed on the record plus seven recorded decisions declining removal. The hardening concern was resolved by change: P3878R1 modified the draft, and its authors record the submitters' confirmation that the change resolves their concerns<sup>[77]</sup>. A property-of-the-rubric reading predicts that no response can qualify as Answered; the record contains two that are, and one draft change whose authors record resolution, against the same objections, in the same cycle.

The non-technical objections have a form built for them. Where an objection expresses a priority rather than a technical question, the third form - a recorded consensus decision with a stated rationale - is the disposition the Directives contemplate, and N4858's rejections supply examples<sup>[14]</sup>. What the record does not contain for the fifteen is either the decision or the resolution.

The rationale paper does not supply the missing form, for four reasons. Authorship: form 3 is a committee act. N4858 is a disposition document prepared for the committee<sup>[14]</sup>; P2899R1 is a paper by four authors, among them all three authors of P2900R14, that, in its own words, "will largely defer to that paper" whose changes were adopted and "summarize" the decisions "along with polls that were taken" (Section 1)<sup>[24]</sup>. WG21 records tallies; it does not record rationales. P2899R1 is the proposers' account of the committee's reasons, and the Directives' vocabulary has a name for a proposer's account: a response.

Timing: P2899R1 is dated 2025-03-14 and its poll record ends at Hagenberg. Of the five objecting papers P3846R1 answers, only P3506R0 predates it; P3835R0, P3829R0, P3849R0, P3878R0, and every national body comment on the committee draft came later. A rationale cannot dispose of objections that did not yet exist. P2899R1 itself describes the concerns it does cover as "restatements of known, sustained opposition to the Contracts design" (Section 2.6)<sup>[24]</sup>, which records that the opposition outlived the decisions it documents.

Scope: P2899R1 records decisions about the design. Form 3 requires a decision rejecting the objection. The two coincide only where a poll targeted the objection's own alternative, and where they coincide, at Concerns 8 and 10, the responses receive credit. Where no poll addressed the objection's mechanism, P2899R1 is rationale for the design, not disposition of the objection.

The polls themselves: P2899R1 characterizes two of the Hagenberg polls on which P3846R1's status entries rest. Of "P2900: add ODR to contracts," it says "EWG took a deliberately vaguely worded poll to gauge the interest of the room to 'do something about it'" (Section 3.5.11); of "P2900: reduce the amount of Undefined Behavior in contracts," it says "The group took a poll to do 'something' about this concern" (Section 3.6.1)<sup>[24]</sup>. Those are the decisions behind Concerns 4, 7, and 16. A poll the proposers describe as deliberately vague, taken to gauge interest, is not a recorded decision with a stated rationale on any objection.

The abstract's hedge does not exempt the closure claim either. Its two classes are unnamed: no concern is mapped to "legitimate yet unavoidable" or to "misunderstanding," and no recorded decision disposes of any concern on either ground, so the hedge reserves an exemption without claiming it for anything. "Unavoidable with any viable assertion facility" is a universal claim about every viable facility, and the record contains a polled candidate counterexample: P3626R0, the alternative wording the lead author prepared so that EWG could poll the choice<sup>[10]</sup>. The "misunderstandings" class has its own form under Section 2, resolution by explanation, and the fifteen flagged sentences of Table 2 are explanations whose evidence does not suffice for their conclusions; a misunderstanding is not corrected by an unsupported sentence. "Extensively discussed" names the floor clause 2.6.5 sets and does not name the resolution the same clause obliges.

Nor does the rubric punish candor. The columns answer different questions by construction: candor about limits is rewarded in the support column, where the bounded Concern 5 response is Supported with no flag. The resolution column records the objection's state, not the response's virtue; a candidly acknowledged open issue is still an open issue, and reclassifying it as closed would be the dishonesty the support column exists to catch.

The boundary cases do not decide the finding. If every contested boundary moved one category in the authors' favor - Concern 11 to Partly answered, and Concerns 5 and 18 to Answered - the distribution becomes four Answered and fourteen Partly answered. The conclusion survives the most favorable defensible reading: the responses produced substantive argument without closing the objections they answer.

The distribution is therefore a property of the responses rather than of the instrument.

---

## 9. What a Discharged Duty Looks Like

Section 8 asked whether the proposers' rationale supplies the third form of resolution. This section states what a record that supplies any of the three forms looks like, before Section 10 asks whose duty it was to produce one. Nothing below is proposed. Each element is in force today in a body operating under the same or stricter rules, and one of them is WG21's own.

The reconciliation duty is discharged when every sustained objector can find, on the record, the answer to their objection, and can either accept that answer or name what remains. That is ANSI's definition of a resolved comment, which turns on the commenter's acceptance of the resolution rather than on the outcome<sup>[18]</sup>; it is the IETF's rule that an issue may be dismissed with reasons but not ignored<sup>[17]</sup>; and it is Section 2's three forms stated for one objector at a time. Nothing in it entitles the objector to be accommodated. It entitles the objector to an answer that exists where they can read it.

The test has an empirical basis. In controlled dispute-resolution experiments, Thibaut and Walker found that participants judged a procedure fairer, and accepted an adverse decision more readily, when they controlled the presentation of their case, even where the decision itself rested with a third party; the effect was on acceptance of the outcome, not on the outcome<sup>[86]</sup>. The bodies that instrument reconciliation wrote the same finding into procedure: the objector is heard on the record, told the answer, and given a path forward. An objector who disagrees with the outcome can still accept that the process ran. An objector whose objection was never answered has no such option, and the record shows where such objectors go instead: the same objection returns at the next stage.

The record a discharged duty leaves behind has five parts. Table 3 names each and locates it in current practice.

**Table 3. The record a discharged reconciliation duty produces, and where each element is in force today.**

| The record shows | Where it exists today |
|---|---|
| Who sustained which objection, named per objection | ISO/IEC Directives 2.5.6: the leadership determines that opposition is sustained<sup>[13]</sup> |
| The chair's determination in words beside each tally | WG14 minutes label each straw poll a decision or an opinion and print the outcome in words<sup>[87]</sup>; WG21's Library Evolution poll-outcome papers print a finding under each tally and each voter's stated reasons beneath it<sup>[88]</sup> |
| Each author told one of three outcomes, with reasons | WG14's contributing page: after discussion "the committee will inform each author whether the committee has accepted the proposal as-is, requires a further revision of the paper, or rejects the proposal"<sup>[89]</sup>; WG14's issue procedure: "No issue should be resolved without some attempted form of communication with the original reporter"<sup>[90]</sup> |
| Each deferral with an owner and a date, then checked | RFC 2026: an Internet-Draft "that has remained unchanged in the Internet-Drafts directory for more than six months without being recommended by the IESG for publication as an RFC, is simply removed"<sup>[91]</sup>; an unowned promise lapses by default |
| An objection found unpersuasive only by recorded vote, with written reasons served on the objector | ASTM regulations 11.4.3.3 and 11.4.4.1: a motion to find a negative vote not persuasive "requires an affirmative vote of at least two thirds of the combined affirmative and negative votes cast", and "If the motion or ballot fails, the balloted item is removed from the ballot"; the reasons and the vote are recorded in the minutes and the negative voter is notified of the disposition and the right to appeal<sup>[92]</sup> |

The fifth row is where an adopted design comes back changed over its authors' objection, and WG21's own record shows it happening without any rule being added. In January 2022 the Library Evolution group polled forwarding P2300R4, `std::execution`, to the Library Working Group for C++23. The tally was SF 23, F 14, N 0, A 6, SA 11, a margin above two to one<sup>[88]</sup>. The recorded finding was no consensus. Its text names the operative objection, "sustained strong opposition against including such a large proposal into C++23 at such a late stage"; separates it from the design question, "The overall design still has strong support"; and records that the chair, a co-author of P2300, "asked Vice Chairs Fabio Fracassi and Ben Craig to determine consensus on this poll" and "fully supports their decision"<sup>[88]</sup>. Beneath the tally, the same document prints each voter's stated reasons, so the objection the finding names can be read in the objectors' own words. Four months later the group forwarded P2300R5 for C++26 at SF 12, F 6, N 2, A 2, SA 3, with the recusal repeated<sup>[93]</sup>. The Strongly Against count had fallen from eleven to three. The design was not overruled. The objection was found persuasive on the record, the finding told the authors what had lost consensus and what had not, and the proposal returned on terms the objectors accepted.

The finding was made for a large proposal, against a release deadline, over a numeric majority, with the chair holding a stake. Each of those conditions is present in the record Sections 5 through 8 assessed. The SG21 co-chair is the lead author of P2900R14 and P3846R1<sup>[1]</sup><sup>[2]</sup>. The Wroc&lstrok;aw forwarding poll carried twelve votes at maximum opposition and zero neutrals<sup>[40]</sup>. The objections now before the national bodies are the ones the proposers' own rationale called sustained<sup>[24]</sup>.

None of the five rows requires ISO approval or a change to the Directives. Two are WG21's own published practice in one subgroup. Two are the C committee's practice under the same secretariat. One is ASTM's, under ANSI accreditation, for decades. A record with these five parts lets a national body delegate answer, for each of the sixteen objections, not whether the objection was heard but where its answer is. Whose duty it was to produce that record, and what the adoption arc produced instead, is Section 10.

---

## 10. The Duty to Reconcile Sat With the Convenership

Read against Table 3, the adoption arc's record is short in every row. Row 1: the determination that opposition was sustained was made, four times, in the proposers' rationale, and no record names which objector sustained which objection<sup>[24]</sup>. Row 2: the polls of record are tallies on the papers tracker with no determination in words<sup>[26]</sup><sup>[39]</sup><sup>[40]</sup><sup>[42]</sup>, and the proposers describe two of the load-bearing ones as polls to do "something" about a concern, one of them "deliberately vaguely worded"<sup>[24]</sup>. Row 3: "No new information has been presented since" closes sixteen of P3846R1's eighteen Discussion Status fields, fourteen of them without qualification<sup>[1]</sup>. Row 4: the deferrals Section 6 lists carry no owner and no date. Row 5: of the twenty-three national body comments on contract assertions at Kona, all but two were rejected, and the record of the rejections is the vote<sup>[8]</sup>.

The sixteen open objections therefore raise a question of office rather than of authorship: whose duty was the reconciliation that Section 2 requires? SD-4, WG21's own practices document, answers the structural question: it provides that "Subgroup chairs are appointed by the convener, and are selected to match the current needs of the subgroup. They have no fixed term", that "The subgroup chair may take any polls they choose", and that plenary consensus is "as determined by the Convener"<sup>[70]</sup>. The ISO/IEC Directives assign the reconciliation duty to "the leadership": "If the leadership determines that there is a sustained opposition, it is required to try and resolve it in good faith."<sup>[13]</sup> The accountability provisions stop one level below the top of this chain: the term limits of clause 1.8.1 bind technical and subcommittee chairs, not working group convenors<sup>[13]</sup>. Within WG21 the duty and the discretion therefore meet in a single office.

Herb Sutter held that office from 2002 through the adoption arc assessed here and authored SD-4 itself; every chair who presided over the polls of record held office under his appointment<sup>[82]</sup>. What the chain produced is on the record. The SG21 consensus record documents the polls' tallies and no reconciliation process between them<sup>[83]</sup>. EWG's forwarding poll at Wroc&lstrok;aw carried a twelve-vote Strongly-Against bloc with no recorded finding that the opposition had been answered<sup>[40]</sup>. Of the twenty-three national body comments on contract assertions at Kona, all but two were rejected<sup>[8]</sup>.

The determination clause 2.5.6 requires is also on the record, in the proposers' own rationale, which uses the Directives' term four times: the pre-Hagenberg concerns were "restatements of known, sustained opposition to the Contracts design"; the safety claim was "another source of sustained opposition"; EWG polled "whether, given the sustained opposition, the Contracts proposal should be withdrawn from consideration for C++26" (SF 9, F 8, N 3, A 19, SA 41, consensus against); and after the Wroc&lstrok;aw strict-predicates poll, "EWG had consensus against pursuing this direction, although sustained opposition to that decision remained," under a recorded result reading "Consensus against, but P2900 would be in danger of failure in plenary" (Sections 2.6 and 3.6.1)<sup>[24]</sup>. The recorded answers to that determination were a removal poll, two gauge polls, one of which the same rationale calls "deliberately vaguely worded", and a response paper, P3591R0, which the rationale names as "a comprehensive response to all these concerns"<sup>[24]</sup>.

The concentration is not the defect; the non-exercise is. A strong executive is how a volunteer committee breaks deadlocks, and the Directives vest the reconciliation duty in the leadership because a room of two hundred cannot reconcile anything. The duty was nonetheless not discharged on the record anywhere in the adoption arc, and it does not expire with the officeholder. Guy Davidson holds the convenership now: ISO selected him in November 2025, effective 2026-01-01, and the current revision of SD-4 names him as its reply-to<sup>[82]</sup><sup>[70]</sup>. In February 2026, the Directions Group issued guidance on building consensus and converging proposals<sup>[84]</sup>. The sixteen open objections identified in this assessment are now before the national bodies, the level where the resolution standard governs outright.

---

## 11. Conclusion: Sixteen Objections Remain Open

The eighteen responses defending C++26 contract assertions resolve two of the eighteen objections. Assessed against the public record at two cutoff dates, the responses come out in their authors' favor on support - two Supported, six Substantially supported, ten Mixed, none Not supported or Contradicted - while fifteen contain a material assertion the record does not support and four contain one the record contradicts. Measured against the resolution standard the ISO/IEC Directives define for the objections P3846R1's abstract describes as addressed, fifteen objections are Partly answered and one is Not resolved; two are Answered. The gap between the two axes is the finding: the responses produced substantive argument without closing the objections they answer.

The authors' own record shows how P3846R1 was invoked as closure despite that gap. Its Discussion Status asks whether a concern had been considered and whether information was new; its Response asks why the concern did not prevent consensus. In public discussion, its lead authors directed live objections back to P3846, acknowledged the cross-translation-unit problem, and invoked acceptance of the problem, prior consensus, later tooling, roadmap boundaries, or future proposals as reasons to retain the C++26 design unchanged. The statements do not establish motive. They establish that the lead authors invoked the response corpus as a stopping rule even where its text recorded that the requested mechanism, evidence, or capability remained absent.

The record contains points in P3846R1's favor, and they are part of the same record. The Concern 2 worst-case sentence is scoped to the naive strategy and excludes the compiler-bug case by construction. The Concern 18 response names all four decoupling comments in its first sentence and anticipated the restriction the committee later adopted. Between the cutoffs, the base implementation of P2900R14 was merged into GCC master<sup>[47]</sup>, a prediction the March artifact did not report in its authors' own favor. The two Answered responses show the standard being met, and the hardening change shows the committee resolving an objection by draft change in the same dispute, on the change authors' record.

Four groups can build on this assessment. The convenership can set the record Section 9 describes beside the record Section 10 found, row by row; every element of the first is in force today in a body under the same rules, and one of them in WG21. Authors preparing a future response paper can work from Table 2, which names the fifteen sentences to source, qualify, or remove. The fields are independent by construction, so such a revision improves the responses without changing the resolution column. That column changes only when an objection is resolved in one of the three forms: changed draft text with commenter confirmation, evidence that suffices for the stated conclusion, or a recorded decision with a stated rationale. Authors evaluating contract designs can build on the supported mechanisms: the bounded modules claim, the consecutive-assertion idiom, the const-ification migration evidence. National body delegates weighing the C++26 draft can apply the Directives' resolution standard directly, because the objections assessed here include the comments before them. The standard the process sets is resolution, and on the public record sixteen of eighteen objections remain open. They are objections to the design the responses defend, not to its C++26 vehicle, and any future vehicle for the same design inherits them unless they are resolved in one of the three forms.

---

## Acknowledgments

The author thanks Mungo Gill for independent verification of the quotations and citations, and Ville Voutilainen for a correction to Concern 18's quotation. Acknowledged individuals have not necessarily reviewed this paper and do not endorse its content.

---

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author is president of the C++ Alliance and maintains coroutine-native I/O libraries under it.

This paper assesses P3846R1's eighteen responses against the public record at the two cutoffs stated in Section 3, a record broader than the sources P3846R1 itself cites. It proposes no wording and requests no poll. Section 9 describes practice in force in other bodies and in one WG21 subgroup, and requests none of it.

The C++ Alliance has published a position, in [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf)<sup>[85]</sup>, that the National Bodies vote No on the C++26 DIS ballot and return the draft over Contracts. This paper's findings support that position, and the author is a co-author of P4238R0. This co-authorship is a material stake in the question under assessment. The author is likewise a co-author of P4334R0, quoted in Section 6.

The ISO/IEC provisions cited in Section 2 bind the national body ballot and plenary level of the standards process, not working group papers; Section 2 states the two reasons the resolution definition nonetheless supplies the test for P3846R1's closure claim. One further limitation of the method is the author's own: the assessment tests the sentences the author selected as load-bearing in each response, and a different selection could produce a different distribution of subclaim flags even if every verdict here were upheld.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

---

## References

[1] [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, Peter Bindels, Peter Dimov, Louis Dionne, Eric Fiselier, Mungo Gill, Pablo Halpern, Tom Honermann, Corentin Jabot, John Lakos, Nevin Liber, Lisa Lippincott, Ryan McDougall, Jason Merrill, Roger Orr, Nina Dinka Ranns, Ren&eacute; Ferdinand Rivera Morell, Oliver Rosten, Iain Sandoe, Hui Xie, 2025).

[2] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025).

[3] [P3835R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3835r0.html) - "Contracts make C++ less safe - full stop" (John Spicer, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, 2025).

[4] [P3829R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3829r0.pdf) - "Contracts do not belong in the language" (David Chisnall, John Spicer, Ville Voutilainen, Gabriel Dos Reis, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, 2025).

[5] [P3849R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3849r0.pdf) - "SIS/TK611 considerations on Contract Assertions" (Harald Achitz, 2025).

[6] [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf) - "P2900 Is Still Not Ready for C++26" (Gabriel Dos Reis, 2025).

[7] [P3878R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r0.html) - "C++26 Contracts are not a good fit for standard library hardening" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[8] [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf) - "WG21 November 2025 Kona Hybrid meeting Minutes of Meeting" (Nina Dinka Ranns, 2025).

[9] [LLVM Issue 28170](https://github.com/llvm/llvm-project/issues/28170) - "Calls to empty variadic functions in comdat no longer optimized out" (Warren Ristow, 2016).

[10] [P3626R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3626r0.pdf) - "Make predicate exceptions propagate by default" (Timur Doumler, 2025).

[11] [P2900R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2900r8.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2024).

[12] [P3097R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3097r0.pdf) - "Contracts for C++: Support for Virtual Functions" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, 2024).

[13] [ISO/IEC Directives, Part 1 (consolidated)](https://www.iso.org/sites/directives/current/consolidated/) - Procedures for the technical work of ISO/IEC JTC 1, current consolidated edition; foreword principles and clauses 2.5.6 and 2.6.5, retrieved 2026-09-03.

[14] [N4858](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4858.pdf) - "Disposition of Comments for CD Ballot, ISO/IEC CD 14882" (Barry Hedquist, 2020).

[15] [ISO/TC 211 good practices, enquiry stage](https://committee.iso.org/sites/tc211/home/resolutions/isotc-211-good-practices/--enquiry-stage---draft-internat.html) - ISO/TC 211 committee guidance on disposition of comments, retrieved 2026-09-03.

[16] [N5028](https://open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5028.pdf) - "Summary of Voting and Collated Comments, ISO/IEC CD 14882" (SC 22, 2025).

[17] [RFC 7282](https://www.rfc-editor.org/rfc/rfc7282.txt) - "On Consensus and Humming" (Pete Resnick, 2014); IETF consensus doctrine, retrieved 2026-09-03.

[18] [ANSI Essential Requirements](https://www.pci.org/PCI_Docs/About/ANSI-Essential-Requirements.pdf) - "Essential Requirements: Due process requirements for American National Standards" (ANSI); definition of a resolved comment, retrieved 2026-09-03.

[19] [W3C Process Document](https://www.w3.org/policies/process/) - "W3C Process Document" (W3C); section 5.3, the formally-addressed adequacy test, retrieved 2026-09-03.

[20] [cplusplus/papers issue 2455](https://github.com/cplusplus/papers/issues/2455) - P3846 tracking issue, cplusplus/papers (2025).

[21] [WG21 2026 paper index](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/) - Official WG21 paper index, 2026 directory, retrieved 2026-09-02.

[22] [WG21 2025 paper index](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/) - Official WG21 paper index, 2025 directory, retrieved 2026-09-02.

[23] [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf) - "WG21 February 2025 Hybrid meeting Minutes of Meeting" (Nina Dinka Ranns, 2025).

[24] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Joshua Berne, Timur Doumler, Rostislav Khlebnikov, Andrzej Krzemie&nacute;ski, 2025).

[25] [GCC commit 64674a2](https://github.com/gcc-mirror/gcc/commit/64674a295b63f46ac9b6776348ae6bbda63fd1ef) - "c++, contracts: Allow contract checks as outlined functions." (Nina Ranns, Iain Sandoe, Ville Voutilainen, 2026).

[26] [cplusplus/papers issue 2225](https://github.com/cplusplus/papers/issues/2225#issuecomment-2641031934) - SG21 poll on forwarding P3582R0, posted by the SG21 chair (Timur Doumler, 2025).

[27] [P3582R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3582r0.html) - "Observed a contract violation? Skip subsequent assertions!" (Andrzej Krzemie&nacute;ski, 2025).

[28] [SG15 post 2744](https://lists.isocpp.org/sg15/2025/10/2744.php) - Public discussion of P3835 and P3846 Concern 10 (Timur Doumler, 2025).

[29] [LLVM commit 5ce3272](https://github.com/llvm/llvm-project/commit/5ce32728330fe7684f24d1b9c418c152db988830) - "Don't IPO over functions that can be de-refined" (Sanjoy Das, 2016).

[30] [GCC Bug 70018](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70018) - "[6 Regression] Possible issue around IPO and C++ comdats discovered as pure/const" (Sanjoy Das, 2016).

[31] [GCC Bug 121936](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=121936) - "[14/15/16/17 Regression] Invalid optimisation (at O3) based on bodies of vague linkage functions" (Iain Sandoe, 2025).

[32] [GCC commit cac7958](https://github.com/gcc-mirror/gcc/commit/cac79586e1ab11fdb5480d7d1d93a48181fb3973) - "c++, contracts: Work around GCC IPA bug, PR121936 by wrapping terminate." (Nina Ranns, Iain Sandoe, 2026).

[33] [P3499R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3499r1.pdf) - "Exploring strict contract predicates" (Timur Doumler, Lisa Lippincott, Joshua Berne, 2025).

[34] [PRE31-C. Avoid side effects in arguments to unsafe macros](https://wiki.sei.cmu.edu/confluence/display/c/PRE31-C.+Avoid+side+effects+in+arguments+to+unsafe+macros) - SEI CERT C Coding Standard (Carnegie Mellon University Software Engineering Institute).

[35] [SonarQube S3346](https://github.com/SonarSource/sonar-dotnet/releases/tag/5.11.0.1761) - "Expressions used in Debug.Assert should not produce side effects", SonarQube static-analysis rule for C#, introduced in sonar-dotnet 5.11 (SonarSource, 2017); retrieved 2026-09-02.

[36] [PVS-Studio V6055](https://pvs-studio.com/en/docs/warnings/v6055/) - PVS-Studio static-analysis diagnostic for Java, retrieved 2026-09-02.

[37] [P3336R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3336r0.pdf) - "Usage Experience for Contracts with BDE" (Joshua Berne, 2024).

[38] [P3261R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3261r2.pdf) - "Revisiting const-ification in Contract Assertions" (Joshua Berne, 2024).

[39] [cplusplus/papers issue 2062](https://github.com/cplusplus/papers/issues/2062#issuecomment-2485786122) - EWG Wroc&lstrok;aw poll on removing const-ification, posted by the EWG chair (JF Bastien, 2024).

[40] [cplusplus/papers issue 1648](https://github.com/cplusplus/papers/issues/1648#issuecomment-2651224887) - EWG Hagenberg contracts polls, posted by the EWG chair (JF Bastien, 2025).

[41] [P2811R7](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2811r7.pdf) - "Contract-Violation Handlers" (Joshua Berne, 2023).

[42] [cplusplus/papers issue 1822](https://github.com/cplusplus/papers/issues/1822#issuecomment-2197580410) - EWG St. Louis polls on P3097R0, posted by the EWG chair (JF Bastien, 2024).

[43] [P3591R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3591r0.pdf) - "Contextualizing Contracts Concerns" (Joshua Berne, Timur Doumler, 2025).

[44] [SG15 post 2980](https://lists.isocpp.org/sg15/2025/10/2980.php) - Public discussion of P3400, the Contracts MVP, and features left until later (Joshua Berne, 2025).

[45] [P3460R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3460r0.pdf) - "C++ Contracts Implementers Report" (Eric Fiselier, Nina Dinka Ranns, Iain Sandoe, 2024).

[46] [Clang C++ support status](https://github.com/llvm/llvm-project/blob/e65522e596522faca391eea0adb440542b9f8f15/clang/www/cxx_status.html) - Clang C++ support status page, version at the 2025-11-03 cutoff; the version at the 2026-03-23 cutoff records the same status.

[47] [GCC commit c928dc51](https://github.com/gcc-mirror/gcc/commit/c928dc51966d) - "c++, contracts: C++26 base implementation as per P2900R14." (Iain Sandoe, 2026).

[48] [Compiler Explorer C++ compiler configuration](https://github.com/compiler-explorer/compiler-explorer/blob/main/etc/config/c%2B%2B.amazon.properties) - compiler-explorer/compiler-explorer, `etc/config/c++.amazon.properties`; the contracts toolchains appear identically in the versions at both cutoffs.

[49] [SG15 post 2909](https://lists.isocpp.org/sg15/2025/10/2909.php) - Public discussion of the deployment-experience standard for Contracts (Timur Doumler, 2025).

[50] [P2877R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2877r0.pdf) - "Contract Build Modes, Semantics, and Implementation Strategies" (Joshua Berne, Tom Honermann, 2023).

[51] [P3500R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3500r1.pdf) - "Are Contracts 'safe'?" (Timur Doumler, Ga&scaron;per A&zcaron;man, Joshua Berne, Ryan McDougall, 2025).

[52] [Safer at Any Speed: Automatic Context-Aware Safety Enhancement for Rust](https://doi.org/10.1145/3485480) - Proceedings of the ACM on Programming Languages, Volume 5, Issue OOPSLA, Article 103 (Natalie Popescu, Ziyang Xu, Sotiris Apostolakis, David I. August, Amit Levy, 2021).

[53] [Rust in Android: move fast and fix things](https://blog.google/security/rust-in-android-move-fast-fix-things/) - Google Security Blog (Jeff Vander Stoep, 2025).

[54] [SG15 post 2786](https://lists.isocpp.org/sg15/2025/10/2786.php) - Public discussion invoking P3846R0, the Hagenberg vote, and the new-information threshold (Timur Doumler, 2025).

[55] [gcc/c-family/c.opt at 436aff90](https://raw.githubusercontent.com/villevoutilainen/gcc/436aff90fc62a9637f475c2ea34840b1e9bc1a79/gcc/c-family/c.opt) - GCC contracts development fork (villevoutilainen/gcc), compiler option table at the branch head of 2025-10-19.

[56] [gcc/c-family/c.opt at bd0dde45](https://raw.githubusercontent.com/gcc-mirror/gcc/bd0dde45a3d0cd9fbf88b4b20515d477c555c335/gcc/c-family/c.opt) - GCC master compiler option table at the last commit touching the file on or before the 2026-03-23 cutoff.

[57] [efcs/contracts-abi](https://github.com/efcs/contracts-abi) - Contract-violation entrypoint ABI design document (Eric Fiselier, 2025); README and .gitignore only, frozen since 2025-06-27.

[58] [P3267R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3267r1.html) - "C++ contracts implementation strategies" (Peter Bindels, Tom Honermann, 2024).

[59] [SG15 post 2782](https://lists.isocpp.org/sg15/2025/10/2782.php) - Public discussion acknowledging cross-translation-unit unpredictability and presenting three responses (Timur Doumler, 2025).

[60] [Boost.Build commit 3b20a4e](https://github.com/boostorg/build/commit/3b20a4e16594b19a38f006a7af051c775bf0e1c9) - "Add initial support for {CPP}-26 Contracts for GCC based toolsets (like clang)." (Ren&eacute; Ferdinand Rivera Morell, 2025).

[61] [grafikrobot/cpp_contracts_example](https://github.com/grafikrobot/cpp_contracts_example) - C++ Contracts example repository (Ren&eacute; Ferdinand Rivera Morell, 2025).

[62] [N5008](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5008.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, 2025).

[63] [P3321R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3321r0.pdf) - "Contracts Interaction With Tooling" (Joshua Berne, 2024).

[64] [P3909R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3909r0.html) - "Contracts should go into a White Paper - even at this late point" (Ville Voutilainen, 2025).

[65] [P3386R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3386r1.pdf) - "Static Analysis of Contracts with P2900" (Joshua Berne, 2024).

[66] [P3893R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3893r0.pdf) - "The CppCon 2025 Talk on Contracts and CodeQL in Context" (Mike Fairhurst, 2025).

[67] [advanced-security/codeql-contracts-smt-z3](https://github.com/advanced-security/codeql-contracts-smt-z3) - SMT constraint solving in CodeQL with Z3; frozen since 2025-09-19.

[68] [SG15 post 2991](https://lists.isocpp.org/sg15/2025/10/2991.php) - Public discussion of runtime checks and future static-analysis tooling (Joshua Berne, 2025).

[69] [P4020R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4020r0.html) - "Concerns about contract assertions" (Andrzej Krzemie&nacute;ski, 2026).

[70] [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Guy Davidson, 2026).

[71] [P1974R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1974r0.pdf) - "Non-transient constexpr allocation using propconst" (Jeff Snyder, Louis Dionne, Daveed Vandevoorde, 2020).

[72] [P2670R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2670r1.html) - "Non-transient constexpr allocation" (Barry Revzin, 2023).

[73] [P1995R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1995r1.html) - "Contracts - Use Cases" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, Ryan McDougall, Herb Sutter, 2020).

[74] [P1893R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1893r0.pdf) - "Proposal of Contract Primitives" (Andrew Tomazos, 2019).

[75] [P3859R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3859r0.html) - "Assertions are not necessarily for changing program behavior" (Andrzej Krzemie&nacute;ski, 2025).

[76] [P3912R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3912r0.pdf) - "Design considerations for always-enforced contract assertions" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, Oliver Rosten, Lisa Lippincott, Peter Bindels, 2025).

[77] [P3878R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r1.html) - "Standard library hardening should not use the 'observe' semantic" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[78] [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, et al., 2025).

[79] [P4334R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4334r0.pdf) - "P2900 Contracts' fundamental flaws" (Bjarne Stroustrup, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, Vinnie Falco, John Spicer, Ville Voutilainen, 2026).

[80] [P3850R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3850r1.pdf) - "A proposed plan for extending Contracts in C++29" (Timur Doumler, Joshua Berne, 2026); later corroboration only.

[81] [SG15 post 2805](https://lists.isocpp.org/sg15/2025/10/2805.php) - Public discussion of mixed-translation-unit semantics and future tooling outside the standard (Joshua Berne, 2025).

[82] [Trip report: November 2025 ISO C++ standards meeting (Kona, USA)](https://herbsutter.com/2025/11/10/trip-report-november-2025-iso-c-standards-meeting-kona-usa/) - Herb Sutter's blog, 2025; the convenership succession announcement.

[83] [P2521R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2521r4.html) - "Contract support - Record of SG21 consensus" (Andrzej Krzemie&nacute;ski, Ga&scaron;per A&zcaron;man, Joshua Berne, Bronek Kozicki, Ryan McDougall, Caleb Sunstrum, 2023).

[84] [P4024R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4024r0.pdf) - "Guidance on Building Consensus and Converging Proposals" (Michael Wong, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, 2026).

[85] [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[86] Thibaut, John W., and Laurens Walker - *Procedural Justice: A Psychological Analysis* (Hillsdale, NJ: Lawrence Erlbaum Associates, 1975). Experimental findings on process control and acceptance of adverse decisions.

[87] [N3227](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3227.htm) - "Draft Minutes for 22-26 January, 2024", WG14 meeting in Strasbourg (WG14, 2024); straw polls labelled "decision" or "opinion" with the outcome stated in words, retrieved 2026-09-03.

[88] [P2459R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2459r0.html) - "2022-01 Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2022); Poll 1 on P2300R4, the recorded finding, and the voters' stated reasons.

[89] [Contributing to WG14](https://www.open-std.org/jtc1/sc22/wg14/www/contributing.html) - WG14 contributing page; the three outcomes communicated to each author after discussion, retrieved 2026-09-03.

[90] [N3002](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3002.pdf) - "Issue Tracking Proposal for C" (Aaron Ballman, 2022); the reporter-communication requirement in Section 2.4.

[91] [RFC 2026](https://www.rfc-editor.org/rfc/rfc2026.txt) - "The Internet Standards Process - Revision 3" (Scott Bradner, 1996); Section 2.2, the six-month expiry of Internet-Drafts, retrieved 2026-09-03.

[92] [Regulations Governing ASTM Technical Committees](https://www.astm.org/membership-participation/technical-committees/key-documents/regulations-governing-astm-technical-committees) - ASTM International; sections 11.4.3.3, 11.4.4.1, and the main committee provisions on recording reasons and notifying negative voters, retrieved 2026-09-03.

[93] [P2575R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2575r0.html) - "2022-04 Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2022); Poll 2.1 on P2300R5.

