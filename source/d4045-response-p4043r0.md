---
title: "Response to P4043R0"
document: P4045R0
date: 2026-03-09
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
audience: EWG
---

## Abstract

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> ("Are C++ Contracts Ready to Ship in C++26?") asks EWG to reconsider the shipping vehicle for C++ Contracts. The paper cites 15 prior papers, raises no concern the committee has not already deliberated on, and proposes deferral as a remedy whose precondition - deployment experience - deferral itself prevents. Every argument in [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> was before the committee when it adopted [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> with strong consensus and when it subsequently rejected every proposal to reverse that decision.

---

## Revision History

### R0: March 2026 (pre-Croydon)

- Initial version.

---

## 1. Introduction

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> proposes three polls asking EWG to reconsider, defer, or change the shipping vehicle for C++ Contracts. The paper was posted on 2026-03-07, two weeks before Croydon, outside any official WG21 mailing.

The question this paper addresses is narrow: does [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> present information or analysis that the committee has not already considered?

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> advances five claims:

1. The Contracts design continues to evolve ("design churn").
2. Papers raising concerns about Contracts have not reached consensus.
3. NB comments remain unresolved.
4. Deferral would allow implementation and deployment experience.
5. The committee should reconsider the shipping vehicle.

Claims 1 through 4 are offered as evidence for claim 5. Sections 2 through 6 examine each claim in order. Section 7 addresses procedural concerns.

The author has no involvement in the C++ Contracts facility and holds no position on its design.

---

## 2. Design Changes Since Adoption

**Claim 1: The Contracts design continues to evolve.**

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> characterizes post-adoption activity as evidence that "the design continues to evolve." The changes since adoption fall into three categories.

### 2.1 Routine NB Comment Resolutions

Two changes have been applied to the Working Draft since [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> was adopted:

- [P3819R0](https://wg21.link/p3819r0)<sup>[4]</sup> removed `evaluation_exception()`. Three identical NB comments (NL 17.10, US 69-125, GB 04-124) identified the function as syntactic sugar that turned out to be unimplementable without significant complexity. EWG applied the fix at Kona 2025.
- [P3886R0](https://wg21.link/p3886r0)<sup>[5]</sup> added a feature-test macro that was missed. EWG applied the fix at Kona 2025.

Both are exactly the kind of fix the NB comment process exists to produce. Neither changes the design.

### 2.2 The Romanian NB Comment (RO 2-056)

NB comment RO 2-056 proposed new design for enforcement semantics. Seven of the 15 papers [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> cites are entirely about this one comment:

| Paper                                                | Title                                                |
| ---------------------------------------------------- | ---------------------------------------------------- |
| [P3911R2](https://wg21.link/p3911r2)<sup>[6]</sup>  | Make Contracts Reliably Non-Ignorable                |
| [P3912R0](https://wg21.link/p3912r0)<sup>[7]</sup>  | Design considerations for always-enforced assertions |
| [P3919R0](https://wg21.link/p3919r0)<sup>[8]</sup>  | Guaranteed-(quick-)enforced contracts                |
| [P3946R0](https://wg21.link/p3946r0)<sup>[9]</sup>  | Designing enforced assertions                        |
| [P4005R0](https://wg21.link/p4005r0)<sup>[10]</sup> | A proposal for guaranteed-(quick-)enforced contracts |
| [P4009R0](https://wg21.link/p4009r0)<sup>[11]</sup> | A proposal for solving all of the contracts concerns |
| [P4015R0](https://wg21.link/p4015r0)<sup>[12]</sup> | Enforcing Contract Conditions with Statements        |

The discussion was extensive. No design change resulted. The committee rejected each specific proposal; it did not poll against guaranteed enforcement as a goal. The outcome reinforced consensus for the adopted design.

### 2.3 Core Design

Unchanged. [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> (published 2025-02-13) remains the latest revision. Zero design changes have been applied since adoption.

### 2.4 Assessment

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> conflates two routine NB fixes and one NB comment that generated extensive discussion but no design change with design instability. Two small fixes and a resolved NB comment are not churn. They are the NB comment process working as intended.

---

## 3. Prior Deliberation on Each Concern

**Claim 2: Papers raising concerns about Contracts have not reached consensus.**

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> cites 15 papers. Every one was published before [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup>. The arguments they contain were before the committee in EWG telecons and at the Kona 2025 and Hagenberg 2025 meetings. The paper does not cite any new implementation result, deployment observation, or design analysis.

The following table maps each claim to the prior papers that raised it and the committee action that disposed of it:

| Claim                              | Raised by                                                                                                                                      | Disposition                                                                                                    |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1. Design continues to evolve      | [P3573R0](https://wg21.link/p3573r0)<sup>[13]</sup>, [P3829R0](https://wg21.link/p3829r0)<sup>[14]</sup>, [P3835R0](https://wg21.link/p3835r0)<sup>[15]</sup> | See Section 2. Zero design changes since adoption.                                                             |
| 2. Concern papers lack consensus   | [P3851R0](https://wg21.link/p3851r0)<sup>[16]</sup>, [P3853R0](https://wg21.link/p3853r0)<sup>[17]</sup>, [P3909R0](https://wg21.link/p3909r0)<sup>[18]</sup> | Each proposal to modify or remove Contracts was rejected ([P3846R0](https://wg21.link/p3846r0)<sup>[3]</sup>). |
| 3. NB comments remain unresolved   | [P3911R2](https://wg21.link/p3911r2)<sup>[6]</sup>, [P3912R0](https://wg21.link/p3912r0)<sup>[7]</sup>, [P3919R0](https://wg21.link/p3919r0)<sup>[8]</sup>, et al. | RO 2-056 is the one outstanding comment. [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> proposes no solution. |
| 4. Deferral enables deployment     | [P3909R0](https://wg21.link/p3909r0)<sup>[18]</sup>                                                                                           | See Section 5. Deferral prevents the deployment it claims to enable.                                           |
| 5. Reconsider the shipping vehicle | EWG poll, 2025-02-11                                                                                                                           | Consensus against removal ([P2899R1](https://wg21.link/p2899r1)<sup>[19]</sup>).                              |

[P4020R0](https://wg21.link/p4020r0)<sup>[20]</sup> ("Concerns about contract assertions") appeared in the 2026-02 pre-Croydon mailing and has not yet been discussed. It recommends no specific action beyond observing that "there are just 2 coherent actions" - keep Contracts or remove them. [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> cites it but does not engage with its analysis.

A note on terminology: a committee poll produces one of three outcomes - consensus for, consensus against, or no consensus - and these are not interchangeable. Consensus against a proposal is an affirmative decision; no consensus means the committee did not reach a decision in either direction. [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> states that proposals "have not yet achieved consensus" and that "none has yet reached consensus." The EWG poll on removing Contracts from C++26 was not "no consensus." It was consensus against removal. The proposals to modify the adopted design were not merely unsuccessful - they were rejected. Characterizing consensus against as the absence of consensus erases the committee's decision.

---

## 4. Outstanding NB Comments

**Claim 3: NB comments remain unresolved.**

Of the NB comments related to Contracts, all have been resolved except RO 2-056. Section 2.2 documents the seven papers written in response to that comment and the outcome: extensive discussion, no design change, consensus for the current design reinforced.

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> cites the outstanding status of RO 2-056 as evidence of instability but proposes no solution to it. The paper recommends deferral or a White Paper - neither of which addresses the technical question RO 2-056 raises.

---

## 5. Deferral and Deployment Experience

**Claim 4: Deferral would allow implementation and deployment experience.**

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> recommends deferral to allow "implementation and deployment experience." Language features do not receive widespread deployment outside standards. The Concepts TS (ISO/IEC TS 19217:2015<sup>[21]</sup>) demonstrated this: the TS was withdrawn, and Concepts were redesigned and shipped directly in C++20. Deferral does not produce deployment experience. Deferral prevents it.

The question of whether to ship Contracts as a TS rather than in the IS has been litigated. [P3265R3](https://wg21.link/p3265r3)<sup>[22]</sup> ("Ship Contracts in a TS") proposed exactly this. [P3276R0](https://wg21.link/p3276r0)<sup>[23]</sup> ("P2900 Is Superior to a Contracts TS") responded that no evidence supports the claim that a TS would resolve open questions, and that the established process for a TS requires listing specific goals, exit criteria, and a viable path through which answers will be acquired. The Direction Group addressed the same question in [P4000R0](https://wg21.link/p4000r0)<sup>[24]</sup> ("To TS or not to TS: that is the question"). SG21 polled on the question and reached consensus against shipping Contracts as a TS ([P2899R1](https://wg21.link/p2899r1)<sup>[19]</sup>).

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> suggests a White Paper as an alternative vehicle. A White Paper carries the same structural requirement as a TS: it must answer a clear set of questions through a viable process. [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> identifies no such questions and proposes no such process.

`constexpr` shipped as a minimal language feature in C++11 ([N2235](https://open-std.org/jtc1/sc22/wg21/docs/papers/2007/n2235.pdf)<sup>[25]</sup>). C++14 relaxed its constraints dramatically ([N3652](https://open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3652.html)<sup>[26]</sup>). The MVP model - ship a minimal feature, expand it in the next standard - is established WG21 practice.

---

## 6. The Committee Record

**Claim 5: The committee should reconsider the shipping vehicle.**

On 2025-02-11, EWG polled on whether to remove [P2900](https://wg21.link/p2900r14)<sup>[2]</sup> ("Contracts for C++") from consideration for C++26 and find a different shipping vehicle. The result was consensus against removal ([P2899R1](https://wg21.link/p2899r1)<sup>[19]</sup>).

On 2025-02-13, LWG forwarded [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> to plenary with consensus ([P2899R1](https://wg21.link/p2899r1)<sup>[19]</sup>).

On 2025-02-16, plenary adopted [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> into the C++26 Working Paper with strong consensus ([P2899R1](https://wg21.link/p2899r1)<sup>[19]</sup>).

Since adoption, multiple proposals to modify the design have been presented; each was rejected ([P3846R0](https://wg21.link/p3846r0)<sup>[3]</sup>). The burden of proof lies with the paper proposing to reverse a decision taken with strong consensus. [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> does not meet that burden.

---

## 7. Procedural Concerns

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> (dated 2026-03-07) does not appear in any official WG21 mailing. The 2026-02 pre-Croydon mailing (released 2026-02-23) contains papers through [P4032R0](https://wg21.link/p4032r0)<sup>[27]</sup>. The paper was simultaneously posted to Reddit. The paper presents no proposed solution to the one outstanding NB comment (RO 2-056).

---

## 8. Conclusion

[P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> presents no new implementation result, no new deployment observation, and no new design analysis. The two post-adoption changes to the Working Draft are routine NB comment resolutions. The extensive discussion around RO 2-056 produced no design change and reinforced consensus for the adopted design. The alternative vehicles the paper suggests - C++29, a TS, a White Paper - have been considered and rejected, and [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> provides no new basis for revisiting those decisions. The committee adopted [P2900R14](https://wg21.link/p2900r14)<sup>[2]</sup> with strong consensus. Nothing in [P4043R0](https://wg21.link/p4043r0)<sup>[1]</sup> warrants reversing that decision.

---

## Acknowledgements

The author thanks Joshua Berne for detailed feedback on the structure and content of this paper, and Darius Nea&#355;u for factual corrections on the reflector.

---

## References

1. [P4043R0](https://wg21.link/p4043r0) - "Are C++ Contracts Ready to Ship in C++26?" (Darius Nea&#355;u, 2026). https://wg21.link/p4043r0
2. [P2900R14](https://wg21.link/p2900r14) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&#324;ski, et al., 2025). https://wg21.link/p2900r14
3. [P3846R0](https://wg21.link/p3846r0) - "C++26 Contracts, reasserted" (Timur Doumler, Joshua Berne, 2025). https://wg21.link/p3846r0
4. [P3819R0](https://wg21.link/p3819r0) - "Remove evaluation_exception from Contracts" (Timur Doumler, Joshua Berne, 2025). https://wg21.link/p3819r0
5. [P3886R0](https://wg21.link/p3886r0) - "Contract violation handler replaceability" (Timur Doumler, Joshua Berne, 2025). https://wg21.link/p3886r0
6. [P3911R2](https://wg21.link/p3911r2) - "Make Contracts Reliably Non-Ignorable" (Darius Nea&#355;u, Andrei Alexandrescu, et al., 2026). https://wg21.link/p3911r2
7. [P3912R0](https://wg21.link/p3912r0) - "Design considerations for always-enforced contract assertions" (Timur Doumler, et al., 2025). https://wg21.link/p3912r0
8. [P3919R0](https://wg21.link/p3919r0) - "Guaranteed-(quick-)enforced contracts" (Ville Voutilainen, 2025). https://wg21.link/p3919r0
9. [P3946R0](https://wg21.link/p3946r0) - "Designing enforced assertions" (Andrzej Krzemie&#324;ski, 2025). https://wg21.link/p3946r0
10. [P4005R0](https://wg21.link/p4005r0) - "A proposal for guaranteed-(quick-)enforced contracts" (Ville Voutilainen, 2026). https://wg21.link/p4005r0
11. [P4009R0](https://wg21.link/p4009r0) - "A proposal for solving all of the contracts concerns" (Ville Voutilainen, 2026). https://wg21.link/p4009r0
12. [P4015R0](https://wg21.link/p4015r0) - "Enforcing Contract Conditions with Statements" (Lisa Lippincott, 2026). https://wg21.link/p4015r0
13. [P3573R0](https://wg21.link/p3573r0) - "Contract concerns" (Michael Hava, J. Daniel Garcia Sanchez, et al., 2025). https://wg21.link/p3573r0
14. [P3829R0](https://wg21.link/p3829r0) - "Contracts do not belong in the language" (David Chisnall, John Spicer, et al., 2025). https://wg21.link/p3829r0
15. [P3835R0](https://wg21.link/p3835r0) - "Contracts make C++ less safe - full stop!" (John Spicer, Ville Voutilainen, Jose Daniel Garcia Sanchez, 2025). https://wg21.link/p3835r0
16. [P3851R0](https://wg21.link/p3851r0) - "Position on contract assertions for C++26" (J. Daniel Garcia, et al., 2025). https://wg21.link/p3851r0
17. [P3853R0](https://wg21.link/p3853r0) - "A thesis+antithesis=synthesis rumination on Contracts" (Ville Voutilainen, 2025). https://wg21.link/p3853r0
18. [P3909R0](https://wg21.link/p3909r0) - "Contracts should go into a White Paper" (Ville Voutilainen, 2025). https://wg21.link/p3909r0
19. [P2899R1](https://wg21.link/p2899r1) - "Contracts for C++ - Rationale" (Timur Doumler, Joshua Berne, Andrzej Krzemie&#324;ski, Rostislav Khlebnikov, 2025). https://wg21.link/p2899r1
20. [P4020R0](https://wg21.link/p4020r0) - "Concerns about contract assertions" (Andrzej Krzemie&#324;ski, 2026). https://wg21.link/p4020r0
21. ISO/IEC TS 19217:2015 - "C++ Extensions for Concepts" (ISO, 2015). Withdrawn.
22. [P3265R3](https://wg21.link/p3265r3) - "Ship Contracts in a TS" (Ville Voutilainen, 2024). https://wg21.link/p3265r3
23. [P3276R0](https://wg21.link/p3276r0) - "P2900 Is Superior to a Contracts TS" (Joshua Berne, Steve Downey, Jake Fevold, Mungo Gill, Rostislav Khlebnikov, John Lakos, Alisdair Meredith, 2024). https://wg21.link/p3276r0
24. [P4000R0](https://wg21.link/p4000r0) - "To TS or not to TS: that is the question" (Michael Wong, H. Hinnant, R. Orr, B. Stroustrup, D. Vandevoorde, 2024). https://wg21.link/p4000r0
25. [N2235](https://open-std.org/jtc1/sc22/wg21/docs/papers/2007/n2235.pdf) - "Generalized Constant Expressions" (Gabriel Dos Reis, Bjarne Stroustrup, Jens Maurer, 2007). https://open-std.org/jtc1/sc22/wg21/docs/papers/2007/n2235.pdf
26. [N3652](https://open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3652.html) - "Relaxing constraints on constexpr functions" (Richard Smith, 2013). https://open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3652.html
27. [P4032R0](https://wg21.link/p4032r0) - last paper in the 2026-02 pre-Croydon mailing.
