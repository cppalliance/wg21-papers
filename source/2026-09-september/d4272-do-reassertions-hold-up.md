---
title: "Do Reassertions Hold Up? Verifying P3846R1 Against Its Own Sources"
document: P4272R0
date: 2026-09-01
intent: info
audience: EWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Two of eighteen responses in P3846R1<sup>[1]</sup> are supported by independently verifiable evidence. The remaining sixteen rest on sources that contradict them, on assertions with no source, or on evidence that does not reach the stated conclusion.

---

## Revision History

### R0: September 2026

- Initial version.

---

## 1. Introduction

P3846R1<sup>[1]</sup> responds to 18 concerns raised by national bodies and individual papers about C++26 contract assertions as specified in P2900R14<sup>[2]</sup>. This paper examines whether the concerns were suitably addressed.

P3846R1 provides a consolidated response to all eighteen concerns in a single document. It cites a source for most of those responses, which is what makes the verification below possible at all. Its comparison of the GCC and Clang implementations is accurate, and two of its eighteen responses are fully supported by the evidence they cite.

---

## 2. The Scorecard

Each response in P3846R1 falls into one of four categories based on what the cited sources show.

| Rating | Concerns | Count | Share |
|---|---|---|---|
| Contradicted by own sources | 12, 15, 18 | 3 | 17% |
| Unverified assertion or procedural argument | 1, 5, 11, 13, 14, 16, 17 | 7 | 39% |
| Partial evidence; conclusion overreaches | 2, 3, 4, 6, 7, 9 | 6 | 33% |
| Answered with verifiable evidence | 8, 10 | 2 | 11% |

Eleven percent of P3846R1's responses are fully supported by the evidence they cite.

---

## 3. What the Sources Show

The concerns below are ordered from those whose responses are contradicted by the cited sources to those whose responses are supported. For each, one sentence states what P3846R1 claims, and one sentence states what the cited source shows.

### Contradicted by own sources

- **Concern 12 (static analysis).** P3846R1 states that CodeQL is "already actively pursuing support for P2900 contract assertions," citing the Martin25 CppCon talk. P3893R0<sup>[3]</sup>, authored by the same CodeQL engineer who copresented that talk, states that "the portions of this talk presented by GitHub are not an endorsement of P2900," and the prototype targets traditional assertions, not P2900 contract specifiers.

- **Concern 15 (future features).** P3846R1 states that "in more than four decades of C++ evolution, no proposal for deep const has ever been brought forward." P1974R0<sup>[4]</sup> (Snyder, Dionne, Vandevoorde, 2020) proposes `propconst`, a language-level deep-const qualifier.

- **Concern 18 (stdlib hardening).** P3846R1 states that "both the libc++ and libstdc++ implementation currently being planned" will implement hardening on top of P2900. Jonathan Wakely, the libstdc++ maintainer, co-authored P3878R0<sup>[5]</sup>, whose title is "C++26 Contracts are not a good fit for standard library hardening." P3846R1 cites RU-016 as support for keeping hardening on contracts but does not note that RU-016 was rejected (N5031<sup>[6]</sup>) or that four other NB comments argued for decoupling.

### Unverified assertion or procedural argument

- **Concern 14 (missing features).** P3846R1 states that "no proposals [for the requested features] gained consensus in EWG." P3097R0<sup>[7]</sup> (virtual function contracts) gained EWG consensus in St. Louis with SF 18, F 15, N 5, A 1, SA 2 and was adopted into the C++26 working draft before being removed at the next meeting in Hagenberg.

- **Concern 11 (exceptions as violations).** P3846R1 states that its approach is "the only known solution" satisfying both the no-escape and recovery constituencies. P3626R0<sup>[8]</sup> proposes unconditional propagation, and P3909R0<sup>[9]</sup> proposes a build-mode option, both documented alternatives. The EWG Hagenberg poll on this question was 30 for change vs. 22 against, which P3846R1 characterizes as both SG21 and EWG concluding the concern was "unsound."

- **Concern 1 (safety).** P3846R1 asserts that the ability to ignore assertions is "a prerequisite for widespread adoption" and cites "decades of successful use of C assert." It cites no study, survey, or usage data linking the NDEBUG mechanism to assert's adoption, and none appears in its reference list. Rust checks bounds by default and requires an explicit `unsafe` block to elide the check, which has not prevented adoption: Android now carries roughly five million lines of Rust<sup>[10]</sup>, and a survey of the 500 most-downloaded crates found unchecked indexing in 10 percent of them, with 76 percent of their benchmarks showing little or no performance gain from eliding the check<sup>[11]</sup>.

- **Concern 17 (deployment experience).** P3846R1 states that P2900 has been "fully implemented in two major compilers" and that "we do have substantial deployment experience with components of P2900." Every deployment claim traces to a closed loop: the P2900 authors implemented their own proposal in GCC and Clang, deployed it on codebases they control (BDE, LLVM), aligned the libc++ hardening infrastructure they maintain with P2900 semantics, then cited all this as independent validation. P3846R1 cites no deployment report authored outside its own signatory list. Its deployment evidence is P3460R0 (Fiselier, Ranns, and Sandoe, all three signatories), P3336R0 (Berne), P3268R0 (Bindels), P3276R0 (Berne, Gill, and Lakos among its authors), P3191R0 (Dionne, one of three authors), and the Boost.Build support added by its maintainer; each is authored or coauthored by a P3846R1 signatory.

- **Concern 5 (modules).** P3846R1 asserts that modules could carry contract-evaluation semantics in BMIs. Its own wording is conditional throughout, opening "In principle, inline functions in a BMI could carry additional information," and it cites no implementation.

- **Concern 13 (complexity).** P3846R1 states the feature is "orders of magnitude simpler to support than modules, concepts, reflection, or even lambdas." P3460R0<sup>[12]</sup>, the cited source, confirms the implementations were straightforward but contains no comparison to other features. P3846R1 cites P3460R0 for the implementation effort, then attributes the comparison itself to an unreferenced report: "The implementers reported that P2900 is orders of magnitude simpler to support."

- **Concern 16 (decomposition).** P3846R1 states that P1893R0's decomposition approach was "subsequently shown to be inadequate." P3846R1 cites no source for that showing, and P2899R1<sup>[13]</sup>, the rationale paper, does not mention P1893R0.

### Partial evidence; conclusion overreaches

- **Concern 4 (ODR).** P3846R1 states that "both Clang (LLVMPR26774) and GCC (GCCBug70018) disabled [interprocedural optimizations on inline functions] nearly a decade ago." GCCBug70018<sup>[14]</sup> was fixed in GCC 7 (2017), confirming the GCC claim. LLVM bug 27796<sup>[15]</sup> is a user complaint about lost optimization from the Clang fix, contradicting P3846R1's claim that "Clang made this tradeoff long ago without user complaints." The same class of bug resurfaced with contracts (GCCBug121936<sup>[16]</sup>), which P3846R1 characterizes as "unrelated to contract assertions" despite the contracts implementation carrying a dedicated workaround for it.

- **Concern 2 (cross-TU semantics).** P3846R1 lists five implementation strategies; three are evidenced (naive in GCC/Clang, link-time deferral prototyped in GCC, ABI proof of concept at efcs/contracts-abi). The stated conclusion that "the worst case is an assertion goes unchecked" is contradicted by P3846R1's own Concern 4, which documents a case where mixed mode triggered miscompilation worse than an unchecked assertion (GCCBug121936<sup>[16]</sup>).

- **Concern 9 (global handlers).** P3846R1's historical claims are evidenced: per-assertion handlers were explored and abandoned, and std::unexpected was removed as part of eliminating dynamic exception specs. The analogies to Qt and game engines are asserted without evidence of those facilities being "successful." The strongest available evidence for a global violation handler, Bloomberg BDE's 20-year deployment, goes uncited in this section.

- **Concern 3 (dependency management).** Boost.Build adding contracts support in under an hour is evidenced by a public commit, but the B2 maintainer is a P3846R1 coauthor (Ren&eacute; Ferdinand Rivera Morell). P3846R1 adds that a linker map for the ABI strategy "can be easily added to existing build systems such as CMake." Asked in May 2026 how CMake would handle contracts, a Kitware maintainer replied that "historically CMake does not add mechanisms for experimental compiler features" and that "it is unlikely `-fcontracts` will be treated differently"<sup>[17]</sup>.

- **Concern 7 (uncheckable guidelines).** P3499R1<sup>[18]</sup> demonstrates that enforcing side-effect-freedom would render most expressions ill-formed, and Sutter &amp; Alexandrescu Rule 68 says what P3846R1 claims. The assertion that side-effect bugs are "rarely an issue" in decades of practice has no empirical backing; CERT PRE31-C and static-analysis rules (SonarQube S3346, PVS-Studio V6055) exist to catch this bug class.

- **Concern 6 (implementation-defined).** P3846R1 states that "P2900 introduces exactly five implementation-defined properties." The C++ standard's own implementation-defined behavior index<sup>[19]</sup> lists seven contract-related entries; the paper omits the `comment` field contents, `location` field contents, and whether `contract_violation` has a virtual destructor. The GCC/Clang comparison table is largely accurate, and SG15 stating no tooling concerns is confirmed by three independent sources. The count error is the only defect in an otherwise partially supported response.

### Answered with verifiable evidence

- **Concern 8 (const-ification).** Const-ification applied to BDE found six assignment-vs-equality bugs (P3336R0<sup>[20]</sup>), and applied to LLVM found approximately 75 const-correctness defects (P3460R0<sup>[12]</sup>). The SG21 adoption poll was 16 in favor, 0 against (SF 6, F 10, N 3, A 0, SA 0).

- **Concern 10 (consecutive assertions).** The `&&` short-circuit idiom is a working mitigation for the canonical case. The launchMissiles counter-example is logically valid. SG21 rejected auto-skipping with SF 0, F 0, N 1, A 13, SA 7, including the author of the proposal.

---

## 4. Conclusion

P3846R1 addresses 18 objections. Verification against the paper's own cited sources finds two responses supported by independently verifiable evidence. The committee record does not support treating the remaining sixteen as settled.

---

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author is president of the C++ Alliance and maintains coroutine-native I/O libraries under it.

This paper reports what P3846R1's cited sources show when each response is checked against them. It proposes no wording and requests no poll.

The C++ Alliance has published a position, in P4238R1<sup>[21]</sup>, that the National Bodies should vote No on the C++26 DIS ballot and return the draft over Contracts. This paper's findings support that position, and the author is a co-author of P4238R1.

The four rating categories are the author's judgment rather than measurements. "Contradicted," "overreaches," and "unverified" apply a standard this paper sets, and a second reader applying the same standard could sort some entries differently.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

---

## References

[1] [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, et al., 2025).

[2] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025).

[3] [P3893R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3893r0.pdf) - "The CppCon 2025 Talk on Contracts and CodeQL in Context" (Mike Fairhurst, 2025).

[4] [P1974R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1974r0.pdf) - "Non-transient constexpr allocation using propconst" (Jeff Snyder, Louis Dionne, Daveed Vandevoorde, 2020).

[5] [P3878R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r0.pdf) - "C++26 Contracts are not a good fit for standard library hardening" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[6] [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5031.pdf) - NB comment disposition record (2026).

[7] [P3097R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3097r0.pdf) - "Contracts for C++: Support for virtual functions" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, 2024).

[8] [P3626R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3626r0.pdf) - "Contracts: unconditional exception propagation" (Bengt Gustafsson, 2025).

[9] [P3909R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3909r0.pdf) - "Contracts should go into a White Paper - even at this late point" (Ville Voutilainen, 2025).

[10] [Rust in Android: move fast and fix things](https://blog.google/security/rust-in-android-move-fast-fix-things/) - Google security blog (Jeff Vander Stoep, 2025).

[11] [Safer at Any Speed: Automatic Context-Aware Safety Enhancement for Rust](https://liberty.princeton.edu/Publications/oopsla21_nader.pdf) - Proceedings of the ACM on Programming Languages 5, OOPSLA, Article 103 (Natalie Popescu, Ziyang Xu, Sotiris Apostolakis, David I. August, Amit Levy, 2021).

[12] [P3460R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3460r0.pdf) - "Contracts Implementors Report" (Eric Fiselier, Nina Dinka Ranns, Iain Sandoe, 2024).

[13] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Timur Doumler, Joshua Berne, et al., 2025).

[14] [GCC Bug 70018](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=70018) - "IPA optimization across weak definitions" (reported 2016).

[15] [LLVM Bug 27796](https://github.com/llvm/llvm-project/issues/27796) - User complaint regarding lost optimization from LLVM PR 26774 (2016).

[16] [GCC Bug 121936](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=121936) - IPA miscompilation with mixed-mode contract assertions (reported 2025).

[17] [C++26 contracts](https://discourse.cmake.org/t/c-26-contracts/15644) - CMake Discourse thread (Vito Gamberini, 2026).

[18] [P3499R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3499r1.pdf) - "Exploring strict contract predicates" (Timur Doumler, Lisa Lippincott, Joshua Berne, 2025).

[19] [Implementation-defined behavior index](https://eel.is/c++draft/impldefindex) - C++ working draft, retrieved 2026-08-14.

[20] [P3336R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3336r0.pdf) - "Usage Experience for Contracts with BDE" (Joshua Berne, 2024).

[21] [P4238R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r1.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).
