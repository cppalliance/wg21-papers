---
title: "Who Needs P3400?"
document: P4240R0
date: 2026-09-10
intent: info
audience: EWG, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

P3400R4<sup>[1]</sup> describes its assertion-control labels as "essential to the unhindered and widespread adoption of Contracts across the many domains in which C++ is used." This paper examines the public record behind that claim. One company has stated, in its own WG21 papers, that contracts are "business-critical," that it funds the compiler prototypes P3400R4 cites as implementation experience, and that it has appointed personnel to verify that ISO proposals satisfy its published business requirements. The public record shows that the prototypes behind P3400R4's Section 6 are not independent implementations but corporate-sponsored branches in the paper author's own repositories, committed from his employer's address.

This paper then generalizes from the public record and the author's observations of committee proceedings into eight falsifiable behavioral predictions. If the committee record does not match them, they are wrong.

---

## Revision History

### R0: September 2026

- Initial version.

---

## The Implementer Gate

This paper offers seven items from the public record, in chronological order. Each is a verbatim quotation from a public source - a published WG21 paper, a corporate website, or a public code repository - followed by its implication for P3400R4's readiness claims. Two categories of material are excluded by rule: committee minutes and reflector posts. Nothing in this paper quotes them.

### 2017: "Business Requirements"

P0678R0<sup>[2]</sup> is titled "Business Requirements for Modules." The paper frames the deployment needs of established codebases (Bloomberg's named as the primary example) as requirements the international standard must satisfy:

> "if the agreed-upon implementation of modules does not take into account established code bases, such as Bloomberg's, they will surely fall far short of wide-spread adoption by industry."<sup>[2]</sup>

The title is the finding. An ISO standard is not a requirements document for any single company's codebase.

### 2019: Management appoints verification personnel

P1487R0<sup>[3]</sup> discloses corporate management directing the standardization effort. The paper's internal timeline dates the first appointment to September 2017 and the second to August 2018; the paper itself is published in 2019:

> "Bloomberg's senior management realizing, among other features, the importance of a proper language-based contract-checking facility in C++, made the multi-year commitment to engage the services of Dr. Andrew Sutton to create a prototype version of the GCC and clang compilers consistent with the needs of even the most demanding large-scale software development companies (e.g., Google)."<sup>[3]</sup>

The same paper discloses a second appointment:

> "Management, acknowledging the importance of modules as an architectural feature (as well as an organization [sic] one), agree to appoint Nate as Bloomberg's 'goto person' for modules within the Standardization process. Nate is responsible for reviewing all module-related functionality proposed for incorporation into the C++ language and, in particular, verifying that it satisfies p0678r0, 'Business Requirements for Modules' (Lakos)."<sup>[3]</sup>

Corporate management appoints personnel to verify that ISO proposals satisfy the company's published business requirements. The verification target is not a technical specification; it is P0678R0, the paper titled "Business Requirements."

### 2020: A CTO-backed deployment plan

A footnote in P2035R0<sup>[4]</sup>, a paper on allocator-aware software, discloses a corporate initiative to deploy ISO features before standardization:

> "Conceived by John Lakos in early 2018, Bloomberg's 2020 Vision (BB20V) initiative is jointly supported by Bloomberg's Chief Technology Officer and its engineering services. BB20V includes a focused effort to bring C++23-like compiler technology (e.g., via GCC and Clang) to Bloomberg well before some features are part of the official C++ Standard through proactive development and deployment (at scale) of four specifically targeted business-critical features, namely concepts, contracts, modules, and allocators."<sup>[4]</sup>

Four features are named "business-critical." The stated goal is deployment before ISO ratification. Early deployment at scale would create institutional pressure on the standard to converge on what has already been shipped.

### 2024: Investment thesis and compiler funding

P3276R0<sup>[5]</sup>, co-authored by seven Bloomberg-affiliated engineers, states the corporate investment thesis:

> "[Bloomberg] has made this investment because it believes that a contract-checking facility is the single most powerful tool that can be added to the language to improve the correctness &mdash; and, therefore, safety &mdash; of both existing and future C++ code."<sup>[5]</sup>

The same paper discloses compiler-implementation funding:

> "Bloomberg is in the process of continuing those efforts to implement the Contracts MVP in GCC and is beginning efforts to see a clang implementation made available."<sup>[5]</sup>

P3270R0<sup>[6]</sup>, published five days later, names who pays. Its stated plan for the facility is to

> "implement [P2900R7] on GCC, Clang, and perhaps on one other platform (e.g., EDG) before the end of 2024 at the very latest (which Bloomberg intends to fund itself)"<sup>[6]</sup>

The parenthesis is the disclosure. A GCC and Clang implementation of the Contracts MVP is to be paid for by one company, stated by that company's engineers in a WG21 paper.

### 2025: Bloomberg's website

Bloomberg's corporate website lists "implementation experience for Contracts" as a major standardization contribution alongside allocators, reflection, and modules.<sup>[7]</sup> The standardization work is presented as corporate thought leadership, not as independent volunteer activity.

### 2026: P3400R4 - "essential"

The Abstract of P3400R4<sup>[1]</sup> states:

> "The functionality enabled by this proposal is essential to the unhindered and widespread adoption of Contracts across the many domains in which C++ is used."<sup>[1]</sup>

Section 6 cites GCC and Clang prototypes on Compiler Explorer behind the `-fcontracts-p3400` flag as implementation experience. It gives five links. All five resolve to the same two builds and to no others: `gcc_notadragon_contracts_p3850` and `clang_notadragon_contracts_p3850`, shown to the reader as "x86-64 gcc (P3850 contracts)" and "x86-64 clang (P3850 contracts)".

Compiler Explorer's build configuration records where those two builds are compiled from:<sup>[8]</sup>

```
- { image: gcc, name: gcc_notadragon_contracts_p3850,
    args: notadragon-contracts-p3850,
    repos: ["https://github.com/notadragon/gnu_gcc/tree/contracts-p3850"] }
- { image: clang, name: clang_notadragon_contracts_p3850,
    args: notadragon-contracts-p3850,
    repos: ["https://github.com/notadragon/llvm-project/tree/contracts-p3850"] }
```

The account holding both repositories belongs to the author of P3400R4. P3204R0<sup>[9]</sup>, an earlier paper of his, gives his reply-to address as `berne@notadragon.com`.

Of the most recent 300 commits on the GCC branch, 151 are authored by `jberne4@bloomberg.net`<sup>[10]</sup>; on the Clang branch, 153 of 300<sup>[11]</sup>. In each case that is more than twelve times the next most frequent author, whose commits, like the rest of the remainder, come from the upstream GCC and LLVM histories these forks track. `jberne4@bloomberg.net` is the reply-to address P3400R4 itself carries.

P3400R4 discloses none of this. The string "notadragon" appears nowhere in the paper, and neither repository is named. A reader who wants to know whose implementation experience is on offer has to resolve the build identifiers to find out.

### The implementer test

P3173R0<sup>[12]</sup>, a broader critique of P2900R6 covering safety, undefined behavior, and dynamic dispatch, argues among other points for "field experience" with the actual design. P3506R0<sup>[13]</sup>, which also raises concerns about UB in predicates and exception handling, argues for "deployment experience." P3878R0<sup>[14]</sup> argues that contract violations used for hardening must guarantee termination, not permit continuation.

Prototypes in compiler branches are not themselves the objection. P3276R0 says so, in the same passage that discloses the funding:

> "... compiler branches of all open-source compilers for experimental papers are frequently made available through Compiler Explorer (https://godbolt.org) and readily locally buildable for experimentation."<sup>[5]</sup>

The configuration cited above bears that out. Personal and organizational forks from many contributors sit alongside one another there, including one published by the C++ Alliance, of which this paper's author is president.

The objection is disclosure. P3400R4 names the assistance it received in producing the prototypes, recording in its acknowledgments that Claude "was used for editorial assistance during the preparation of this paper, as well as significant parts of the prototype implementations."<sup>[1]</sup> It does not name whose branches those prototypes are on.

Section 6 of P3400R4 cites prototypes written by the paper author, in his own repositories, from his employer's address, behind experimental flags, in forks of GCC and Clang. No shipping compiler implements P3400. No production codebase deploys it. The implementation experience is a corporate sponsor verifying its own requirements on branches its own employee writes.

The implementation status is checkable. As of 2026-09-18, a search of the GCC C++ status page, the GCC 16 release notes, the Clang C++ status page, the cppreference C++26 compiler support table, the microsoft/STL C++26 contracts tracking issue, and EDG's published feature list found no reference to P3400 or to assertion-control labels; the cppreference table tracks four contracts papers, P2900R14, P3598R0, P3819R0 and P3886R0, and P3400 is not among them.<sup>[19]</sup><sup>[20]</sup><sup>[21]</sup><sup>[22]</sup><sup>[23]</sup> No feature-test macro for P3400 appears on any of those pages, and the papers tracker records P3400R4 as an EWG-direction-approved paper targeting C++29 rather than an adopted feature.<sup>[24]</sup> This establishes absence from those pages on that date, not absence from every implementation under every name.

The implementers describe the state of the work in the same terms. [P3595R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3595r0.pdf)<sup>[25]</sup> reports that the configuration system "has been partially implemented in branches of GCC and Clang that are available on compiler explorer", and links a Compiler Explorer build for "control of evaluation semantic based on group labels (as provided by [P3400R4])". One qualification belongs with that citation and cuts against this paper's own argument: P3595R0's co-author Iain Sandoe is the GCC contracts implementer and is not a Bloomberg employee, so that implementation is not one the sponsor's own employee wrote.

## Predictions

The following predictions generalize from the author's observations of committee proceedings on contracts, partially corroborated by the public record cited in the preceding section. Each identifies a behavioral pattern that the structural position of an entity requiring P3400 would produce. They are falsifiable: if the committee record does not match them, they are wrong.

**Prediction 1.** An entity that needs P3400 will characterize the C++26 Contracts MVP as unusable without it, framing the extension as urgent rather than optional.

**Prediction 2.** An entity that needs P3400 will treat its own deployment constraints as non-negotiable requirements on the international standard's design, rather than as one stakeholder's preference among alternatives.

**Prediction 3.** An entity that needs P3400 will present the adoption of its preferred design as the default path and frame alternatives as schedule risks to be managed rather than as designs to be compared.

**Prediction 4.** An entity that needs P3400 will argue that continuation past undefined behavior serves its customers, positioning a business-value judgment as a language-design principle.

The record already carries instances. [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf)<sup>[16]</sup> gives the production rationale directly: the observe semantic "provides the opportunity to install a logging handler to instrument an existing codebase - one that is known to run successfully in production - with contract assertions to find defects in that codebase without bringing down the entire production system upon contract violation", and elsewhere licenses continuing past undefined behavior on the ground that in such a codebase "any undefined behavior it exhibits is most likely 'benign'". [P3400R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3400r3.pdf)<sup>[17]</sup> makes the argument in its own motivation section, that a marked assertion can be "more easily deployed to production environments", and P1487R0's 2010 entry calls a returning violation handler "an absolute requirement for incorporating new contract checks into older programs".<sup>[3]</sup>

Two things in the same record cut the other way and belong here. P2899R1 states the safety caveat in the same passage: "In many situations, this strategy is not advisable because continuing past a contract violation is likely to execute incorrect code and cause undefined behavior."<sup>[16]</sup> And P1487R0 records a 2015 outage at the same company caused by a violation handler that returned, after which management ruled that a check proved correct "is to be changed to never return ... and must never be allowed to continue again".<sup>[3]</sup> The prediction concerns how the extension is argued for. It is not a claim that the company favors continuation uniformly, and its own published record shows that it does not.

**Prediction 5.** An entity that needs P3400 will describe the choice of violation response in the vocabulary of business risk and operational policy, rather than in the vocabulary of language safety guarantees.

**Prediction 6.** An entity that needs P3400 will characterize sustained technical opposition as an obstacle to industry adoption, casting delay as harm to users rather than as unresolved design disagreement.

The record already carries instances here too. P3276R0 frames delay as a signal to regulators - shipping as a TS "would only delay delivery of a feature that is essential for correctness and safety to C++ users around the world", and "such a delay would imply to governments, regulatory bodies, and users that we do not actually take language safety issues seriously" - and characterizes the opposing position as a "myopic mindset" that "does not serve our users, our business, or our long-term need for a qualitatively safer programming language".<sup>[5]</sup> [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf)<sup>[18]</sup> states that "delaying standardisation to add features blocks adoption, deployment in real-world codebases, and evolution", and that "removing P2900 from C++26 entirely would not benefit any constituency". P3400R3's abstract applies the same frame to this extension, calling the functionality "essential to the unhindered and widespread adoption of Contracts".<sup>[17]</sup>

**Prediction 7.** An entity that needs P3400 will cite its own internal deployment history as authoritative evidence, but the room cannot independently corroborate it.

**Prediction 8.** An entity that needs P3400 will present the migration constraints of its own installed base as constraints on the standard's defaults for every user.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author is president of the C++ Alliance and maintains coroutine-native I/O libraries under it.

The C++ Alliance has published a position, in [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf)<sup>[15]</sup>, that the National Bodies vote No on the C++26 DIS ballot and return the draft over Contracts. The author is a co-author of P4238R0, and this paper's findings support that position. That co-authorship is a material stake in the question under assessment.

Two limitations bound the method. Sponsorship is established from the public record - the employer's own published statements that it funds a GCC and Clang implementation, its claim of that implementation experience as a corporate contribution, and the address its employee commits from - and not from any accounting document, which no party outside the company can see. The predictions in the preceding section generalize partly from the author's own observations of committee proceedings, which is evidence no reader can independently check.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

This paper asks for nothing.

## References

[1] [P3400R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3400r4.pdf) - "Controlling Contract-Assertion Properties" (Joshua Berne, 2026).

[2] [P0678R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0678r0.pdf) - "Business Requirements for Modules" (John Lakos, 2017).

[3] [P1487R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1487r0.pdf) - "User Experience with Contracts That Work" (John Lakos, 2019).

[4] [P2035R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2035r0.pdf) - "Value Proposition: Allocator-Aware (AA) Software" (Pablo Halpern, John Lakos, 2020).

[5] [P3276R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3276r0.pdf) - "P2900 Is Superior to a Contracts TS" (Joshua Berne, Steve Downey, Jake Fevold, Mungo Gill, Rostislav Khlebnikov, John Lakos, Alisdair Meredith, 2024).

[6] [P3270R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3270r0.pdf) - "Repetition, Elision, and const-ification With Regard to contract_assert: A Principled Analysis" (Joshua Berne, John Lakos, 2024).

[7] [Bloomberg C++ page](https://www.bloomberg.com/company/values/tech-at-bloomberg/c-plus-plus/) - "Bloomberg's thought leadership in C++" (Bloomberg L.P., accessed 2026-08-14).

[8] [compiler-explorer/compiler-workflows](https://github.com/compiler-explorer/compiler-workflows/blob/main/compilers.yaml) - "compilers.yaml, mapping each Compiler Explorer build identifier to its source repository and branch" (Compiler Explorer, accessed 2026-09-10).

[9] [P3204R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3204r0.pdf) - "Why Contracts?" (Joshua Berne, 2024).

[10] [notadragon/gnu_gcc](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850) - "Branch contracts-p3850" (GitHub, accessed 2026-09-10).

[11] [notadragon/llvm-project](https://github.com/notadragon/llvm-project/tree/contracts-p3850) - "Branch contracts-p3850" (GitHub, accessed 2026-09-10).

[12] [P3173R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3173r0.pdf) - "P2900R6 May Be Minimal, but It Is Not Viable" (Gabriel Dos Reis, 2024).

[13] [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf) - "P2900 Is Still Not Ready for C++26" (Gabriel Dos Reis, 2025).

[14] [P3878R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r0.pdf) - "C++26 Contracts are not a good fit for standard library hardening" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).

[15] [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[16] [P2899R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2899r1.pdf) - "Contracts for C++ - Rationale" (Timur Doumler, Joshua Berne, Andrzej Krzemie&nacute;ski, Rostislav Khlebnikov, 2025).

[17] [P3400R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3400r3.pdf) - "Controlling Contract-Assertion Properties" (Joshua Berne, 2026).

[18] [P3846R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3846r1.pdf) - "C++26 Contract Assertions, Reasserted" (Timur Doumler, Joshua Berne, 2026).

[19] [C++ Standards Support in GCC](https://gcc.gnu.org/projects/cxx-status.html) - GCC C++ status page (GNU Project, accessed 2026-09-18).

[20] [GCC 16 Release Series Changes](https://gcc.gnu.org/gcc-16/changes.html) - GCC 16 release notes (GNU Project, accessed 2026-09-18).

[21] [C++ Support in Clang](https://clang.llvm.org/cxx_status.html) - Clang C++ status page (LLVM Project, accessed 2026-09-18).

[22] [Compiler support for C++26](https://en.cppreference.com/w/cpp/compiler_support/26) - cppreference C++26 compiler support table (accessed 2026-09-18).

[23] [microsoft/STL issue 5286](https://github.com/microsoft/STL/issues/5286) - "P2900R14 `<contracts>`" tracking issue (Microsoft, accessed 2026-09-18).

[24] [cplusplus/papers issue 2184](https://github.com/cplusplus/papers/issues/2184) - "P3400 R4 Controlling Contract-Assertion Properties" tracker issue, labelled C++29 (accessed 2026-09-18).

[25] [P3595R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3595r0.pdf) - "Configuration of Contract Evaluation Semantics" (Joshua Berne, Iain Sandoe, 2026).
