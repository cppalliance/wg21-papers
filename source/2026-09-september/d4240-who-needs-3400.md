---
title: "Who Needs P3400?"
document: P4240R0
date: 2026-09-01
intent: info
audience: EWG, LEWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

P3400R4<sup>[1]</sup> describes its assertion-control labels as "essential to the unhindered and widespread adoption of Contracts across the many domains in which C++ is used." This paper examines the published record behind that claim. One company has stated, in its own WG21 papers, that contracts are "business-critical," that it funds the compiler prototypes P3400R4 cites as implementation experience, and that it has appointed personnel to verify that ISO proposals satisfy its published business requirements. The published record suggests that the prototypes behind P3400R4's Section 6 are not independent implementations but corporate-sponsored branches by the paper author's employer.

This paper then extrapolates from the published pattern to produce eight falsifiable behavioral predictions. If the committee record does not match them, they are wrong.

---

## Revision History

### R0: September 2026

- Initial version.

---

## The Implementer Gate

Seven items from the published record, in chronological order. Each is a verbatim quotation from a published WG21 paper or a corporate website, followed by its implication for P3400R4's readiness claims.

### 2017: "Business Requirements"

P0678R0<sup>[2]</sup> is titled "Business Requirements for Modules." The paper frames the deployment needs of established codebases - Bloomberg's named as the primary example - as requirements the international standard must satisfy:

> "if the agreed-upon implementation of modules does not take into account established code bases, such as Bloomberg's, they will surely fall far short of wide-spread adoption by industry."<sup>[2]</sup>

The title is the finding. An ISO standard is not a requirements document for any single company's codebase.

### 2019: Management appoints verification personnel

P1487R0<sup>[3]</sup> discloses corporate management directing the standardization effort:

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

> "[Bloomberg] has made this investment because it believes that a contract-checking facility is the single most powerful tool that can be added to the language to improve the correctness - and, therefore, safety - of both existing and future C++ code."<sup>[5]</sup>

The same paper discloses compiler-implementation funding:

> "Bloomberg is in the process of continuing those efforts to implement the Contracts MVP in GCC and is beginning efforts to see a clang implementation made available."<sup>[5]</sup>

The authors infer that the compiler branches disclosed here are the same branches P3400R4 Section 6 later cites as implementation experience.

### 2025: Bloomberg's website

Bloomberg's corporate website lists "implementation experience for Contracts" as a major standardization contribution alongside allocators, reflection, and modules.<sup>[6]</sup> The standardization work is presented as corporate thought leadership, not as independent volunteer activity.

### 2026: P3400R4 - "essential"

The Abstract of P3400R4<sup>[1]</sup> states:

> "The functionality enabled by this proposal is essential to the unhindered and widespread adoption of Contracts across the many domains in which C++ is used."<sup>[1]</sup>

Section 6 cites GCC and Clang prototypes on Compiler Explorer behind the `-fcontracts-p3400` flag as implementation experience. These prototypes appear to run on the compiler branches P3276R0<sup>[5]</sup> disclosed Bloomberg funds.

### The implementer test

P3173R0<sup>[7]</sup>, a broader critique of P2900R6 covering safety, undefined behavior, and dynamic dispatch, argues among other points for "field experience" with the actual design. P3506R0<sup>[8]</sup>, which also raises concerns about UB in predicates and exception handling, argues for "deployment experience." P3878R0<sup>[9]</sup> argues that contract violations used for hardening must guarantee termination, not permit continuation.

P3400R4 Section 6 cites prototypes funded by the paper author's employer, behind experimental flags, in forks of GCC and Clang. No shipping compiler implements P3400. No production codebase deploys it. The implementation experience is a corporate sponsor verifying its own requirements on branches it pays for.

## Predictions

The following predictions extrapolate from the published evidence in the preceding section. Each identifies a behavioral pattern that the structural position of an entity requiring P3400 would produce. They are falsifiable: if the committee record does not match them, they are wrong.

**Prediction 1.** An entity that needs P3400 will characterize the C++26 Contracts MVP as unusable without it, framing the extension as urgent rather than optional.

**Prediction 2.** An entity that needs P3400 will treat its own deployment constraints as non-negotiable requirements on the international standard's design, rather than as one stakeholder's preference among alternatives.

**Prediction 3.** An entity that needs P3400 will present its adoption as inevitable, foreclosing design alternatives before the room has evaluated them.

**Prediction 4.** An entity that needs P3400 will argue that continuation past undefined behavior serves its customers, positioning a business-value judgment as a language-design principle.

**Prediction 5.** An entity that needs P3400 will frame language semantics as corporate policy choices, treating the contract-violation response as a business decision rather than a safety guarantee.

**Prediction 6.** An entity that needs P3400 will frame committee opposition to its preferred design as blocking industry adoption, implying that the standard exists to serve large deployers.

**Prediction 7.** An entity that needs P3400 will cite its own internal deployment history as authoritative evidence which the room cannot independently corroborate.

**Prediction 8.** An entity that needs P3400 will argue that its legacy codebase's migration constraints must shape the standard's default behavior for all users.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author co-authored P3276R0, cited in this paper.

This paper asks for nothing.

## References

[1] [P3400R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3400r4.pdf) - "Controlling Contract-Assertion Properties" (Joshua Berne, 2026).

[2] [P0678R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0678r0.pdf) - "Business Requirements for Modules" (John Lakos, 2017).

[3] [P1487R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1487r0.pdf) - "User Experience with Contracts That Work" (John Lakos, 2019).

[4] [P2035R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2035r0.pdf) - "Value Proposition: Allocator-Aware (AA) Software" (Pablo Halpern, John Lakos, 2020).

[5] [P3276R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3276r0.pdf) - "P2900 Is Superior to a Contracts TS" (Joshua Berne, Steve Downey, Jake Fevold, Mungo Gill, Rostislav Khlebnikov, John Lakos, Alisdair Meredith, 2024).

[6] [Bloomberg C++ page](https://www.bloomberg.com/company/values/tech-at-bloomberg/c-plus-plus/) - "Bloomberg's thought leadership in C++" (Bloomberg L.P., accessed 2026-08-14).

[7] [P3173R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3173r0.pdf) - "P2900R6 May Be Minimal, but It Is Not Viable" (Gabriel Dos Reis, 2024).

[8] [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf) - "P2900 Is Still Not Ready for C++26" (Gabriel Dos Reis, 2024).

[9] [P3878R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3878r0.pdf) - "C++26 Contracts are not a good fit for standard library hardening" (Ville Voutilainen, Jonathan Wakely, John Spicer, Stephan T. Lavavej, 2025).
