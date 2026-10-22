---
title: "Do Remove Contracts From C++26"
document: P4420R0
date: 2026-10-22
intent: ask
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper asks WG21 to decline the poll proposed in P4419R0 and to recommend a revised C++26 draft without contract assertions.

[P4419R0](https://isocpp.org/files/papers/P4419R0.pdf)<sup>[1]</sup> asks WG21 to rule out any language design change to the DIS, whatever the national body comments say. It was written before those comments were known. It corrects several real errors in [P4334R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4334r0.pdf)<sup>[2]</sup> and this paper concedes them. It answers the procedural objection with a list of meeting dates and an assertion of consensus.

## Revision History

### R0: October 2026

- Initial version.

## 1. What P4419R0 Gets Right

1. P4419R0 is right that WG21 polls since February 2025 favored keeping contracts. The Hagenberg EWG poll to remove them failed at 9/8/3/19/41 (SF/F/N/A/SA).<sup>[3]</sup>
2. Contract inheritance was postponed to C++29, so the P4334R0 bullet "Includes a completely untried inheritance model" misdescribes the draft.
3. P4334R0 cites P3878R0 on hardening. [P3878R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r1.html)<sup>[4]</sup> superseded it, and, as P4419R0 reports, the wording fix it kept was applied in Kona.
4. Contract assertions are implemented. GCC 16.1 ships them, and Clang and EDG branches exist. "Unimplemented" was wrong.
5. GCC marks every C++26 feature experimental, so the label applies to contracts like any other feature.
6. As P4419R0 explains, the "56 pages" includes existing wording reproduced for context. P4334R0 should have cited net new words, which P4419R0 reports as 4,946.
7. [P4324R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4324r0.html)<sup>[5]</sup> calls itself an exploration and keeps the C++26 pre, post, and contract_assert keywords. It is not a ready replacement.

## 2. What P4419R0 Dodges or Overstates

1. It asserts "strong, sustained" consensus. The recorded tallies show a standing minority: twelve Strongly Against when EWG forwarded P2900R11 at Wroc&lstrok;aw,<sup>[3]</sup> and fourteen opposed when the plenary adopted P2900R14, the largest opposition to any motion at that meeting.<sup>[6]</sup>
2. It answers the procedural objection with meeting time. Footnote 15 lists the sessions where concerns were heard, and the text asserts that each concern was weighed and decided. The question in P4238R1 is whether the minutes record a finding that each objection was answered.
3. It lists "controversial in WG21" among claims that "are not true." It then documents sustained opposition, a "well-known" Microsoft objection, six meetings where EWG took up the concerns, and the removal of virtual function support to answer them.
4. It says sustained opposition "does not confer a veto." That sentence is about consensus inside WG21. The ballot rules it quotes in footnote 1 let a minority fail the draft, since negative votes with technical comments above one quarter of the votes cast are enough. A No vote is a national body's position.
5. Its history of the feature skips the 2019 removal of contracts from the C++20 draft.<sup>[7]</sup> C++26 also lost trivial relocation after national body objections.<sup>[3]</sup>
6. It asks whether contracts are "less tried" than lambdas, constexpr, and reflection. The only release it names is GCC 16.1, from April 2026, a month after WG21 approved the DIS draft in March.<sup>[1]</sup>
7. It says the objectors offered no alternative design. They asked for field experience first, through a Technical Specification, and SG21 voted that down in May 2024 (1/3/3/12/10).<sup>[3]</sup>

## 3. The Design Was Hasty

P4419R0 lists "the design is hasty" among the claims it says "are not true."<sup>[1]</sup> The record says otherwise.

SG21 locked in the C++26 deadline with a roadmap poll in November 2022 (10/10/5/1/1), and the plan was "derived more or less directly from" the release deadlines.<sup>[8]</sup> The rationale paper, P2899R1, says SG21 "meticulously followed" the plan:<sup>[9]</sup> fifteen revisions, P2900R0 to P2900R14, in 16.6 months.<sup>[10]</sup> The first revision carried twelve TODO notes, among them the syntax, virtual functions, and coroutines, and promised wording "after all TODO items above have been resolved in SG21."<sup>[11]</sup> Wording arrived in R5, in February 2024,<sup>[10]</sup> and SG21 forwarded the paper to EWG and LEWG two weeks later.<sup>[9]</sup> P3443R0's data show that 23 of the 41 Contracts poll items between January and October 2024 came a week or less after the paper appeared. The 17 between 29 February and 16 May averaged 4.5 days from publication to poll.<sup>[12]</sup>

The design was still changing in the last week. EWG merged virtual functions in June 2024 and voted them out on 11 February 2025 (20/24/13/14/2).<sup>[9]</sup> CWG approved the next day, LWG the day after,<sup>[13]</sup> and the plenary adopted P2900R14 that week at 100/14/12 with no discussion.<sup>[6]</sup> The former SG21 co-chair who co-wrote the plan now says "the schedule itself became part of the next failure mode."<sup>[14]</sup>

Changes continued after adoption. The function evaluation_exception() was added in November 2024.<sup>[10]</sup> Its authors later found that on some platforms it required copying the exception object, which may pose a security risk, and it was removed in November 2025.<sup>[15]</sup><sup>[16]</sup>

Field experience came late. The implementers' report said its standard library deployment was "limited to contract_assert,"<sup>[17]</sup> and GCC first shipped Contracts, experimentally, on 30 April 2026, a month after WG21 voted to send the draft to DIS ballot.<sup>[18]</sup><sup>[19]</sup>

## 4. Why the Argument Fails

P4419R0 argues that technical work carried by strong consensus "cannot be undone at the DIS ballot by a small group of individuals whose position did not prevail in WG21." The DIS ballot exists to do exactly that. It is the review outside the working group, and the approval rules give a blocking minority by design.<sup>[20]</sup> P4419R0 says that, for the first time, some national bodies voted against the DIS. Its authors wrote before the result or the comments were known, yet they ask WG21 to rule out language design changes whatever the comments say. Clause 2.6.4 of the Directives, which the paper quotes, says an appropriate group of the committee "will, at a meeting, address any comments received." A poll that rules out change on those terms replaces that review with a fixed answer, and turns the ballot into the rubber stamp P4238R1 warned about.<sup>[3]</sup>

P4419R0 also supplies the case for removal. It says what contracts lack will be added in C++29 and beyond, and that the planned extensions are "purely additive." If that is true, removal costs C++26 one more ballot and delays contract assertions to C++29, where they can arrive together with the pieces they lack. If it is false, C++26 locks in a base design that cannot take those pieces. P4419R0 needs the first to be true and asserts it. What it shows is one compiler release from April 2026, two trial reports from 2024, and decades of experience with a subset, assertion macros. The cost of removal is a bounded delay. The cost of a locked-in defect is permanent. WG21 made this call in 2019, when contracts left C++20, and the removal paper's reasoning applies now: "if there is not consensus that a feature is in acceptable form when the train is about to depart that the feature must be taken off the train."<sup>[7]</sup> Reflection, execution, and the rest of C++26 continue unchanged, and the draft ships a few months later without one feature.

## 5. Suggested Polls

Two polls could read:

1. WG21 will review the national body comments on the C++26 DIS under ISO/IEC Directives Part 1, clause 2.6.4, before it recommends any course of action to the SC22 chair.
2. After that review, WG21 recommends to the SC22 chair a revised C++26 draft without contract assertions.

## Disclosure

The author provides information and serves at the pleasure of the committee.

Vinnie Falco is president of the C++ Alliance, a co-author of P4334R0 and P4238R1, and a signatory of the petition "C++26 Needs To Go Back," which P4419R0 criticizes. The C++ Alliance has published the position that national bodies should vote No on the C++26 DIS. Readers should weigh the argument with that interest in mind.

This paper asks WG21 to take the two polls in section 5.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

## References

[1] [P4419R0](https://isocpp.org/files/papers/P4419R0.pdf) - "Do not remove Contracts from C++26" (Timur Doumler, Joshua Berne, Ga&scaron;per A&zcaron;man, 2026).

[2] [P4334R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4334r0.pdf) - "P2900 Contracts' fundamental flaws" (Bjarne Stroustrup, J-Daniel Garcia, Vinnie Falco, John Spicer, Ville Voutilainen, 2026).

[3] [P4238R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r1.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[4] [P3878R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r1.html) - "Standard library hardening should not use the 'observe' semantic" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[5] [P4324R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4324r0.html) - "Exploration of a more library-oriented approach to contracts" (Ville Voutilainen, 2026).

[6] [N5007](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5007.pdf) - "WG21 02/2025 Hagenberg Minutes of Meeting" (Nina Ranns, 2025).

[7] [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf) - "Remove Contracts from C++20" (Nicolai Josuttis, Ville Voutilainen, Roger Orr, Daveed Vandevoorde, John Spicer, Christopher Di Bella, 2019).

[8] [P2695R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2695r1.pdf) - "A proposed plan for Contracts in C++" (Timur Doumler, John Spicer, 2023).

[9] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Joshua Berne, Timur Doumler, Rostislav Khlebnikov, Andrzej Krzemie&nacute;ski, 2025).

[10] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2900r14.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025).

[11] [P2900R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2900r0.pdf) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2023).

[12] [P3443R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3443r0.pdf) - "Reflection on SG21's 2024 Process" (Ran Regev, 2024).

[13] [cplusplus/papers #1648](https://github.com/cplusplus/papers/issues/1648) - WG21 public paper tracker issue for P2900, recording the EWG, LEWG, CWG, and LWG polls.

[14] [P4381R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4381r0.html) - "Chairing SG21 and then objecting to Contracts" (John Spicer, 2026).

[15] [P3819R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3819r0.pdf) - "Remove evaluation_exception() from contract-violation handling for C++26" (Peter Bindels, Timur Doumler, Joshua Berne, Eric Fiselier, Iain Sandoe, 2025).

[16] [N5031](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5031.pdf) - "WG21 2025-11 Kona Minutes of Meeting" (Nina Dinka Ranns, 2025).

[17] [P3460R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3460r0.pdf) - "C++ Contracts Implementers Report" (Eric Fiselier, Nina Dinka Ranns, Iain Sandoe, 2024).

[18] [GCC 16.1 release announcement](https://www.mail-archive.com/gcc@gcc.gnu.org/msg107232.html) - "GCC 16.1 Released" (Richard Biener, 2026). Posted to the gcc mailing list on 30 April 2026.

[19] [N5040](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5040.pdf) - "WG21 2026-03 Croydon Hybrid Meeting Minutes" (Braden Ganetsky, 2026).

[20] [ISO/IEC Directives, Part 1](https://www.iso.org/sites/directives/current/consolidated/index.html) - Consolidated ISO Supplement (2024), clauses 2.6.3 and 2.6.4.
