---
title: "Each Standard Takes Longer"
document: P4193R0
date: 2026-08-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

Each successive C++ standard takes longer for compilers to implement, and C++20 - published over five years ago - remains incomplete on two of three major compilers.

C++14 achieved near-complete conformance within months. C++20 has not achieved it after 64. What changed between those two standards, and what institutional forces produce the pattern? This paper measures the interval between ISO publication and compiler conformance across five standards, three compilers, and fifteen years.

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Boost.Beast](https://github.com/boostorg/beast), [Capy](https://github.com/cppalliance/capy), and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++. This paper does not address networking, coroutines, or senders. It documents the implementation gap across standards.

[P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup>, signed by eighteen implementer co-authors across all three major compilers, reports that implementation feedback is "framed primarily as an obstacle to progress." [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> observes that WG21 "does not have any requirement on implementation experience to adopt a proposal." This paper examines both observations against the conformance data.

The author is not a compiler implementer. All conformance data derives from vendor self-reported status pages and official release announcements.

This paper asks for nothing.

---

## 2. Methodology

This paper tracks the interval between ISO publication of each C++ standard and the date each major implementation (GCC/libstdc++, Clang/libc++, MSVC/MSVC STL) claimed conformance. Dates derive from official release announcements and vendor conformance tracking pages<sup>[[3]](#ref-3)</sup><sup>[[4]](#ref-4)</sup><sup>[[5]](#ref-5)</sup>. "Conformance" means the vendor's own claim of complete feature support, not independent verification. Where no claim was made, the implementation is treated as incomplete. Language and library are tracked separately because they follow different timelines and face different constraints. Gap is measured in months from ISO publication; negative values indicate conformance before publication.

---

## 3. The Timeline

| Standard | ISO Date | GCC Lang | GCC Lib | Clang Lang | Clang Lib | MSVC Lang | MSVC Lib |
|----------|----------|----------|---------|------------|-----------|-----------|----------|
| C++11 | Sep 2011 | +21 | +43 | +21 | ~0 | +80 | ~46-66 |
| C++14 | Dec 2014 | +4 | +4 | -11 | ~-3 | +27 | +7 |
| C++17 | Dec 2017 | -7 | +53 | -3 | >100 | +5 | +9 |
| C++20 | Dec 2020 | >64 | >64 | >64 | >64 | +8 | +17 |
| C++23 | Oct 2024 | >18 | >18 | >18 | >18 | >18 | >18 |

Positive values: months after publication. Negative values: months before publication. Values with > prefix: incomplete implementations, months elapsed as of April 2026.

---

## 4. Per-Standard Analysis

### 4.1 C++11

ISO publication: September 1, 2011.

| Compiler | Language | Library |
|----------|----------|---------|
| GCC | 4.8.1, May 2013 (+21) | 5.1, Apr 2015 (+43) |
| Clang | 3.3, Jun 2013 (+21) | Designed for C++11 (~0) |
| MSVC | VS2017 15.7, May 2018 (+80) | ~VS2015-VS2017 (~46-66) |

C++11 was the largest single expansion of the C++ language: rvalue references, variadic templates, lambdas, constexpr, auto, decltype, range-for, nullptr, strongly-typed enums, static_assert, and a memory model with threading primitives. GCC and Clang achieved language conformance within 21 months. MSVC took 80 months - nearly seven years. The bottleneck was architectural. MSVC's parser descended from a 1982 YACC grammar and stored code as a token stream rather than an AST. Two-phase name lookup and expression SFINAE were impossible without a fundamental rewrite. Microsoft began that rewrite in 2012; it would not complete until VS2017 15.7 in May 2018. Jim Springfield described the source: "Our compiler is old. There are comments in the source from 1982."<sup>[[6]](#ref-6)</sup>

Library conformance lagged language in every implementation. libstdc++ reached C++11 conformance in GCC 5.1 (April 2015, +43 months), delayed by the dual ABI mechanism for std::string and std::list needed to preserve backward compatibility. libc++ was designed as a C++11 standard library from inception and had substantial conformance near publication. MSVC's standard library completed C++11 support incrementally across the VS2015 and VS2017 release cycles.

### 4.2 C++14

ISO publication: December 15, 2014.

| Compiler | Language | Library |
|----------|----------|---------|
| GCC | 5.1, Apr 2015 (+4) | 5, Apr 2015 (+4) |
| Clang | 3.4, Jan 2014 (-11) | 3.4-3.5, Jan-Sep 2014 (~-3) |
| MSVC | VS2017 15.0, Mar 2017 (+27) | VS2015 RTM, Jul 2015 (+7) |

C++14 was deliberately small: variable templates, generic lambdas, relaxed constexpr restrictions, return type deduction, and std::make_unique. The limited scope enabled rapid implementation. Clang shipped full language support 11 months before publication, implementing features as they were voted into the draft. GCC followed 4 months after publication with language and library conformance in the same release. MSVC's +27 month language gap reflects residual C++11 parser debt, not C++14 difficulty.

**C++14 is the only standard where every major compiler achieved both language and library conformance within 27 months.**

### 4.3 C++17

ISO publication: December 2017.

| Compiler | Language | Library |
|----------|----------|---------|
| GCC | 7.1, May 2017 (-7) | 12, May 2022 (+53) |
| Clang | 5.0, Sep 2017 (-3) | Never complete (>100) |
| MSVC | VS2017 15.7, May 2018 (+5) | VS2017 15.8, ~Sep 2018 (+9) |

C++17 language features - structured bindings, if constexpr, fold expressions, class template argument deduction - were implemented quickly by all three compilers. GCC and Clang shipped language conformance before publication. MSVC completed language support five months after, with the finished parser rewrite enabling rapid adoption.

The library split open. Three features proved disproportionately costly. std::to_chars and std::from_chars for floating-point types required implementing novel algorithms (Ryu, fast_float) with exact round-trip guarantees - the MSVC STL team described charconv as "C++17's final boss," consuming over a developer-year of effort<sup>[[7]](#ref-7)</sup>. The special mathematical functions demanded numerical analysis expertise rarely found on compiler teams. Parallel algorithms required a parallelism runtime. MSVC completed all three, finishing library conformance in roughly 9 months. libstdc++ completed charconv in GCC 12 (May 2022, +53 months). libc++ has never completed C++17: Parallel algorithms and special mathematical functions remain unimplemented as of April 2026, and floating-point from_chars shipped seven years late in October 2024.

**C++17 is the first standard where a major implementation has no prospect of completing its library.**

### 4.4 C++20

ISO publication: December 15, 2020.

| Compiler | Language | Library |
|----------|----------|---------|
| GCC | Never claimed (>64) | Never claimed (>64) |
| Clang | Never claimed (>64) | Never claimed (>64) |
| MSVC | VS2019 16.11, Aug 2021 (+8) | VS2022 17.2, May 2022 (+17) |

C++20 introduced four features that each represent a new subsystem rather than an incremental extension: modules (replacing textual inclusion with a new compilation model), coroutines (stackless coroutine framework with ABI implications), concepts (constrained generic programming), and ranges (a redesigned algorithms library with lazy composition). std::format added Python-style text formatting. The three-way comparison operator changed overload resolution rules.

MSVC is the only compiler to claim full C++20 conformance: language in August 2021 (+8 months), library in May 2022 (+17 months)<sup>[[8]](#ref-8)</sup>. Microsoft delayed the /std:c++20 mode switch because the committee kept modifying std::format and std::ranges semantics through post-publication defect reports, requiring the backport of over 100 commits.

GCC and Clang have never claimed C++20 conformance. 64 months after publication, both remain officially incomplete. GCC's module implementation carries ~48 FIXMEs and remains labeled experimental. Coroutines have 84+ open bugs against GCC. libstdc++ shipped std::format in GCC 13 (April 2023), 28 months after publication. Clang lists C++20 language support as "Partial." Clang's coroutine implementation has an unfixable ABI bug on 32-bit Windows (Issue #59382): The x86 calling convention requires non-trivially-copyable arguments in a stack slot, but coroutine suspension can destroy that slot between argument evaluation and the call. Three theoretical fixes exist; all are either non-conforming or reject coroutines on 32-bit Windows entirely.

**C++20 is the first standard where two of three major compilers have not achieved conformance and show no trajectory toward it.**

### 4.5 C++23

ISO publication: October 19, 2024.

| Compiler | Language | Library |
|----------|----------|---------|
| GCC | Incomplete (GCC 15, >18) | Incomplete (>18) |
| Clang | Incomplete (Clang 20, >18) | Incomplete (>18) |
| MSVC | Incomplete (MSVC 14.50, >18) | Incomplete, leads (>18) |

C++23 was published 18 months ago. No compiler claims conformance for language or library. Major features include deducing this, std::print, std::expected, std::mdspan, std::generator, and std::flat_map. MSVC leads on library implementation. [P1787R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1787r6.html)<sup>[[9]](#ref-9)</sup> ("Declarations and where to find them") - a massive wording overhaul to scope and name lookup - has not been implemented by any compiler; the LLVM Discourse thread is titled "How to tackle P1787," and GCC Bugzilla shows it assigned with no target milestone.

With C++20 still incomplete on two of three compilers and C++17 library still incomplete on Clang, the implementation backlog is cumulative.

---

## 5. Per-Vendor Profiles

### 5.1 GCC

GCC's language conformance accelerated steadily through C++17 - from +21 months (C++11) to +4 months (C++14) to -7 months (C++17, shipping before publication). This trajectory broke at C++20. Modules remain experimental after five years, carrying ~48 FIXMEs in the implementation source. Coroutines have 84+ open bugs. GCC has never claimed full C++20 language conformance.

The library is the persistent bottleneck. libstdc++ is largely volunteer-maintained and faces expanding API surface with each standard. The dual ABI (introduced for C++11 std::string compatibility) imposed +43 months on C++11 library conformance. C++17 library took +53 months, gated by charconv. std::format arrived 28 months after C++20 publication in GCC 13. The pattern is consistent across every standard: Language ships on time, library slips.

Architectural constraints reinforce the gap. ABI stability is treated as inviolable - libstdc++ routes ABI-unstable features through libstdc++exp.a rather than risk binary compatibility breakage. The constexpr evaluator is fast (10-50x faster than Clang's for heavy workloads) but tightly coupled to compiler internals. The module implementation's FIXME density suggests deep architectural obstacles rather than merely incomplete feature work.

### 5.2 Clang

Clang's language conformance peaked at C++14 (-11 months, shipping nearly a year before publication), then degraded: -3 months for C++17, then "Partial" for C++20 with no completion date 64 months later. The clean-slate AST architecture that enabled early language conformance provides no corresponding advantage for the library.

libc++ is Clang's structural gap. Parallel algorithms have never been implemented. Special mathematical functions have never been implemented. Floating-point from_chars shipped in October 2024 - seven years after C++17 publication. libc++ is largely volunteer-maintained. The unimplemented C++17 features, now over 100 months old, suggest no path to completion. ABI sensitivity has caused collateral damage: Sized deallocation was disabled by default for nine years; std::format was marked experimental for years after initial implementation.

Apple Clang compounds the problem. Apple ships a Clang fork with version numbers unrelated to upstream, omitting clang-scan-deps (breaking CMake module workflows) and OpenMP. Developers who check their compiler version frequently discover they are 1-2 major versions behind upstream. Clang's coroutine implementation has an unfixable ABI bug on 32-bit Windows.

### 5.3 MSVC

MSVC went from worst to first. C++11 language conformance took 80 months - the longest gap of any compiler for any standard - because the parser descended from a 1982 YACC grammar and could not implement two-phase name lookup or expression SFINAE. Microsoft launched a multi-year rejuvenation rewrite in 2012, replacing the 35-year-old token-stream parser with a modern recursive-descent architecture<sup>[[6]](#ref-6)</sup>.

The rewrite was transformative. Post-rewrite conformance gaps: C++17 language +5 months, C++20 language +8 months. MSVC is the only compiler to claim full C++20 conformance for both language and library. The library team shipped charconv ("C++17's final boss") in VS2017 15.8, completing C++17 library in roughly 9 months<sup>[[7]](#ref-7)</sup>. C++20 library followed in VS2022 17.2 (+17 months)<sup>[[8]](#ref-8)</sup>. Microsoft delayed the /std:c++20 compiler switch because the committee kept changing std::format and std::ranges through post-publication defect reports.

MSVC has maintained ABI stability since VS 2015 across five major Visual Studio releases, using /std:c++latest as a staging area for features not yet ABI-stable. IntelliSense, which uses the EDG frontend rather than MSVC's own parser, still labels modules "experimental" in VS 2026.

---

## 6. Secondary Compilers

### 6.1 Intel C++

Intel transitioned from its own frontend (ICC, EDG-based) to the Clang-based ICX compiler in 2021. ICC was deprecated and discontinued in oneAPI 2024.0. Intel cited 14% build time reduction and 41-48% SPEC performance improvement with ICX. The deeper fact: Maintaining a standalone C++ frontend is no longer economically viable, even for Intel. ICX inherits Clang's conformance status - and its gaps.

### 6.2 EDG

EDG sells a C++ frontend to 183+ licensees including Intel (ICC), Nvidia (nvcc), Comeau, Cray, TI, IAR, and Green Hills. EDG reports zero failures on Perennial/Plum Hall conformance test suites and functions as an unofficial reference implementation. Intel's decision to abandon the EDG-based ICC for Clang-based ICX signals that conformance quality alone no longer justifies the cost of a separate frontend. EDG remains critical infrastructure for embedded and specialized compilers where Clang/LLVM integration is impractical.

### 6.3 Apple Clang

Apple ships a Clang fork with its own version numbering scheme unrelated to upstream. The fork omits clang-scan-deps (breaking CMake module workflows) and OpenMP support. Developers who run `clang --version` see Apple's version number and must cross-reference documentation to determine the actual upstream Clang version, which is typically 1-2 major releases behind. This version gap means Apple platform developers may lack access to C++ features that upstream Clang already supports.

### 6.4 Nvidia nvcc

nvcc is a compiler driver that splits source into host and device code. Host code delegates to the system compiler (GCC, Clang, or MSVC). Device code uses the EDG frontend. CUDA 12 supports C++20 language features for device code but excludes coroutines and modules. Library feature availability depends entirely on the host compiler's standard library. This architecture means nvcc's conformance ceiling is bounded by both EDG's device-code support and the host compiler's library gaps.

---

## 7. What Users Say

The adoption data tells a consistent story: Users trail the standard by half a decade or more, and the gap is structural.

C++17 is the lingua franca of production C++ in 2025. JetBrains surveys from 2022 through 2025 place it at 43-45% usage, dominant across every measured period<sup>[[10]](#ref-10)</sup>. It reached this position roughly five years after publication - not because users were slow, but because it took that long for compilers and build systems to make it safe to deploy. Even now, 10.30% of workplaces prohibit C++17. Projects like Apache Arrow and PowerDNS remain on C++17 not by choice but because Apple Clang lags behind upstream LLVM, and their users ship on macOS.

C++11 adoption tells the bleakest version of this story. Enterprise migration took three to seven years. In 2024 - thirteen years after publication - JetBrains still measured 26% usage<sup>[[10]](#ref-10)</sup>. The ISO survey showed 90.69% of respondents were allowed to use C++11 at work by 2023<sup>[[11]](#ref-11)</sup>, meaning nearly one in ten workplaces still restricted a twelve-year-old standard. MSVC's C++11 support was described as "beyond abysmal" in 2013, and that single compiler's deficiency held back the entire Windows ecosystem for years.

C++14 barely registers as a standard in user perception. An LLVM contributor called it "worth moving to mainly for C++11 bug fixes." JetBrains 2024 data shows it at 19% and falling fastest of any standard<sup>[[10]](#ref-10)</sup>. Users did not adopt C++14 - they passed through it on the way to C++17.

C++20 is where the gap becomes most visible to users. Usage reached 34% in JetBrains 2025 data<sup>[[10]](#ref-10)</sup>, but the ISO survey from 2023 showed 42.50% of workplaces prohibiting it outright<sup>[[11]](#ref-11)</sup>. Modules do not work: CMake does not officially support `import std`, build system integration remains experimental, and no cross-compiler module story exists. Coroutines are described as "just barely starting to become usable" in 2023 developer commentary. When QPDF used concepts in its public headers, it broke every C++17 downstream consumer and had to revert the change. Users who adopt C++20 do so partially, cherry-picking constexpr expansions and std::format while avoiding modules and treating coroutines as expert-only territory.

C++23 is the fastest-growing standard at 21% (JetBrains 2025)<sup>[[10]](#ref-10)</sup>, but no compiler has full conformance. Projects like Ceph upgraded specifically for std::expected, flat_map, and stacktrace - targeted features with clear value. Users are not adopting C++23 as a standard. They are adopting individual C++23 features that happen to compile on their toolchain.

**The pattern across every standard is the same.** Users do not adopt standards. They adopt features, one at a time, when every compiler they target implements the feature correctly and their build system supports it. The "portable C++ standard" is not what the committee published most recently. It is the intersection of what GCC, Clang, and MSVC all implement, minus whatever their build systems cannot handle, minus whatever breaks downstream consumers. That intersection has never matched the published standard within three years of publication. For C++20, it has not matched after five.

---

## 8. Pattern Analysis

**The gap is growing.** C++14 achieved near-complete conformance across all three compilers within months of publication. C++17 language features shipped on time or early, but library conformance lagged by 53 months on GCC and exceeded 100 months on Clang. C++20 language conformance remains incomplete on GCC and Clang after 64 months; only MSVC achieved language conformance at +8 months. C++23 shows all six columns at >18 months with no compiler close to complete. The trajectory is unambiguous: Each successive standard takes longer to implement than the last, and the deficit is compounding. C++23 implementation began before C++20 was finished on two of three compilers.

**Library features cause the gap more than language features.** In C++11, GCC's language conformance arrived at +21 months; its library took +43 months. In C++17, GCC and Clang shipped language features before or near publication, but libstdc++ took +53 months for library and libc++ exceeded +100 months. The library gap in C++17 was an order of magnitude worse than the language gap. This holds across standards. Language features require compiler engineering. Library features require correct language support underneath, stable ABI decisions, and algorithms that sometimes do not exist yet when the standard ships.

**Four categories of features drive implementation difficulty.**

*New compilation models* produce the largest delays. Two-phase lookup cost MSVC 80 months because it required replacing a parser architecture dating to the 1980s. Modules represent the same class of problem: GCC's implementation is 25,000 lines, still experimental after five years, and only MSVC claims production readiness. These features demand architectural changes to the compiler, not incremental additions.

*ABI-sensitive features* produce the longest-lived gaps. GCC's dual ABI decision delayed C++11 library conformance by four years. Clang's sized deallocation remained disabled by default for nine years. ABI stability is the single largest cause of library lag, and it is a constraint that cannot be solved by additional engineering effort within a release cycle.

*Features that outrun their algorithms* ship broken by design. The committee standardized charconv before the Ryu algorithm (2018) and fast_float (2021) existed. libc++ shipped from_chars for floating-point seven years after the standard. The standard specified an interface whose efficient implementation had not been invented yet.

*Large API surfaces with post-publication instability* create a distinct problem. Ranges and std::format received committee DRs after C++20 publication. MSVC delayed its /std:c++20 switch specifically to avoid shipping an API the committee was still changing, then backported over 100 commits. libstdc++ std::format arrived 28 months late. When the committee revises a feature after publication, it resets the implementation clock for every vendor.

**The three-year cadence outpaces implementation capacity.** C++20 was published in December 2020. As of April 2026 - 64 months later - GCC and Clang have not completed it. C++23 was published in late 2024. Implementation is underway on all three compilers with none close to complete. The committee is publishing standards faster than two of three major compilers can implement the previous one.

**Both factors are real: The standard is getting harder and compiler resources are not scaling.** C++14 was deliberately small and conformance was fast. C++20 was the largest single standard since C++11, introducing three new compilation models plus two large library surfaces plus continuous constexpr expansion. The difficulty per standard is increasing nonlinearly. Compiler teams have not grown proportionally. GCC and Clang are open-source projects with finite contributor pools. MSVC has a dedicated team but still carries architectural debt - [P2564R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2564r3.html)<sup>[[12]](#ref-12)</sup> constexpr support is still missing.

**Intel's abandonment of ICC's frontend is a signal about barrier to entry.** A company with thousands of engineers, deep x86 expertise, and direct financial interest in C++ performance decided that maintaining an independent C++ frontend was no longer viable. Intel now ships a Clang-based compiler. The complexity of modern C++ has reduced the number of viable frontend implementations. Three remain.

---

## 9. The Situation

As of April 2026, portable C++ - defined as features that compile correctly on current releases of GCC, Clang, and MSVC - is a subset of C++20. It is not C++20 itself.

Developers can portably use: concepts, constexpr improvements through C++20 (with gaps), coroutines (with known bugs on every compiler), std::format (with recent-enough library versions), and most of the C++20 language surface. They cannot portably use modules. They cannot rely on HALO optimization for coroutines. They cannot assume charconv floating-point support on all platforms. They cannot use C++23 features and expect them to work everywhere.

C++20 modules are not portable. GCC and Clang implementations are experimental. Build system support is incomplete. Only MSVC claims production readiness, and that claim is platform-specific. Any project targeting more than one compiler cannot use modules. Five years after publication, this remains true.

C++23 is partially available on all compilers. std::expected works. std::generator works on compilers that support it. But no compiler has full C++23 conformance, and the features users want most have uneven support. Teams adopting C++23 are doing so feature-by-feature, testing each one against their specific compiler matrix.

The committee is now two standards ahead of what the open-source compilers have delivered. MSVC is closer, but carries its own gaps. The gap between what the committee publishes and what the ecosystem delivers is not closing. It is widening.

---

## 10. Structural Diagnosis

Six diagnostic lenses from institutional analysis, applied to the implementation data.

**Functionality (North 1990).** The test asks whether an institution produces what it claims to produce.

> "Institutions are the humanly devised constraints that structure political, economic and social interaction."<sup>[[13]](#ref-13)</sup>

ISO/IEC JTC1/SC22/WG21 claims to produce a usable programming language standard. If so, the prediction is that compiler conformance should follow publication within a release cycle - roughly 12 to 18 months. The data refutes this. C++20 language features remain incomplete in GCC and Clang more than 64 months after publication. Modules are production-ready in one of three major compilers after five years. Coroutines carry 84+ open GCC bugs and an unfixable Clang ABI defect on 32-bit Windows. C++17 usage stands at 43%; 42.50% of workplaces prohibit C++20<sup>[[11]](#ref-11)</sup>. The committee's actual output is aspirational specification. The standard describes a language that does not yet exist in deployable form. Confirmed.

**Self-Correction (Ashby 1956).** The test asks whether the institution has independent feedback mechanisms to detect when its output rate exceeds implementation capacity.

> "Only variety in [the regulator] can force down the variety due to [disturbance]; only variety can destroy variety."<sup>[[14]](#ref-14)</sup>

The prediction is that a functioning feedback loop would slow feature adoption when compilers fall behind. No such mechanism operates. [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> states the consequence directly: WG21 "does not have any requirement on implementation experience to adopt a proposal." [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup> finds that implementer feedback is "framed primarily as an obstacle to progress." The committee that votes features in is the same body that evaluates whether those features were implementable. Charconv shipped in the C++17 standard before the Ryu algorithm it needed existed (Ryu published 2018; libc++ from_chars arrived seven years late). Ranges and format required post-publication DRs that forced MSVC to delay /std:c++20 to avoid shipping unstable API. The feedback loop is a ceremony. Confirmed.

**Principal-Agent Misalignment (Jensen & Meckling 1976).** The test asks whether the agents (committee members who design features) bear the costs that fall on the principals (compiler teams who implement, users who wait).

> "If both parties to the relationship are utility maximizers, there is good reason to believe that the agent will not always act in the best interests of the principal."<sup>[[15]](#ref-15)</sup>

The prediction is that cost externalization produces overproduction. The evidence is direct. The committee shipped coroutines without a standard library type until C++23 and with HALO optimization unreliable in practice. MSVC carried a 1982-era parser incapable of two-phase lookup; Jim Springfield noted comments in the source from 1982<sup>[[6]](#ref-6)</sup>, and the rewrite took six years. GCC's module implementation spans 25,000 lines with approximately 48 FIXMEs. Intel abandoned its own frontend entirely (2021), choosing to absorb Clang rather than continue tracking the standard independently. The committee bears no cost for features that take half a decade to implement. The principals - compiler engineers and the users blocked on their work - bear all of it. Confirmed.

**Goodhart's Law (Goodhart 1984).** The test asks whether a proxy metric has displaced the quantity it was meant to measure.

> "When a measure becomes a target, it ceases to be a good measure."<sup>[[16]](#ref-16)</sup>

The prediction is that "features shipped per standard" becomes the target, displacing "useful, implementable improvements delivered to users." C++20 supports this. It added modules, coroutines, concepts, ranges, format, and constexpr allocation in a single revision. None shipped complete across all three compilers within 64 months. MSVC required a complete rewrite of its constexpr evaluator (announced 2018); [P2564R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2564r3.html)<sup>[[12]](#ref-12)</sup> remains unimplemented as of April 2026. The standard that added the most features produced the largest implementation gap. Feature count and user value have diverged. Confirmed.

**Capacity Constraints (Laffont & Tirole 1993).** The test asks whether demand on a supply-constrained system produces quality shading - degraded output from providers who cannot refuse work.

> "When a regulated firm faces demand it cannot decline, the predicted response is quality shading - reduced output quality rather than reduced output quantity."<sup>[[17]](#ref-17)</sup>

The prediction is that compiler teams, unable to decline mandates from a standard they must track, will ship partial or defective implementations. GCC modules carry approximately 48 FIXMEs after five years. Clang modules remain "Partial." Clang's sized deallocation was disabled by default for nine years due to ABI concerns. GCC's dual ABI delayed C++11 library conformance by four years. Coroutines shipped across compilers with known, persistent defects rather than complete implementations. The 183 EDG licensees face the same constraint; the market is consolidating as Intel's frontend abandonment demonstrates. Compiler teams cannot expand capacity to match committee output. They ship what they can. Quality shades. Confirmed.

**Lock-in and Switching Costs (Klemperer 1987).** The test asks whether the absence of exit options removes the market pressure that would force a producer to match output to ecosystem capacity.

> "Switching costs make the products of the firms, which were ex ante homogeneous, ex post differentiated."<sup>[[18]](#ref-18)</sup>

The prediction is that a captive user base tolerates gaps a competitive market would not permit. C++ users cannot switch to a competing standard for the same language. The ISO survey (2023) shows C++20 at 34% adoption and C++17 at 43%<sup>[[11]](#ref-11)</sup> - users cluster on older standards not by preference but because newer ones are not fully available. Titus Winters estimates ABI break costs at "engineer-millennia," making even partial migration prohibitive. No user can credibly threaten to leave. The committee faces no demand-side penalty for shipping standards that take years to become real. The corrective mechanism that markets provide is absent. Confirmed.

---

## 11. Behavioral Diagnosis ("The Room")

The structural diagnosis in Section 10 showed what happens: Features enter the standard faster than compilers can absorb them, the gap widens with each cycle, and users adopt slowly. This section asks why. Six behavioral forces, each documented in institutional analysis, predict the pattern. Each is tested against the implementation data.

**Goal displacement.** When an organization's procedures become ends in themselves, the original objective recedes.

> "Adherence to the rules, originally conceived as a means, becomes transformed into an end-in-itself; there occurs the familiar process of displacement of goals whereby 'an instrumental value becomes a terminal value.'"<sup>[[19]](#ref-19)</sup>

WG21's objective is a standard that ships in compilers. Its procedures - revisions, straw polls, study group rotations, committee approvals - measure paper progress, not deployment. [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> states the consequence directly: WG21 "does not have any requirement on implementation experience to adopt a proposal." Coroutines entered C++20 with no standard library type; std::generator arrived four years later in C++23. The charconv specification shipped in C++17 referencing algorithms that did not exist in the literature until 2018-2021. In both cases the procedural record was complete. The implementation record was not. The metric the room optimizes is paper maturity, and papers can mature entirely within the room.

**Shifting baseline syndrome.** When degradation is gradual, each generation accepts the current state as normal because it lacks memory of the prior baseline.

> "Each generation of fisheries scientists accepts as a baseline the stock size and species composition that occurred at the beginning of their careers, and uses this to evaluate changes. The result obviously is a gradual shift of the baseline, and inappropriate reference points."<sup>[[20]](#ref-20)</sup>

C++14 is the counterfactual. Clang shipped full language conformance eleven months before ISO publication. GCC followed four months after. By C++20, all three compilers remain incomplete more than five years after publication. The room does not compare against the C++14 baseline because nobody frames C++14 as the standard to beat. Instead, the C++20 gap becomes the new normal, and C++23 inherits it without alarm. JetBrains (2025) reports C++17 at 43% adoption and C++20 at 34%, with 42.5% of respondents prohibited from using C++20 at work<sup>[[10]](#ref-10)</sup><sup>[[11]](#ref-11)</sup>. These numbers would have been crisis-level against C++14 expectations. Against the shifted baseline, they register as ordinary.

**Implementer feedback suppression.** [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup>, signed by eighteen implementer co-authors across all three major compilers, reports that implementation feedback is "framed primarily as an obstacle to progress." This is a structural damping mechanism. When the corrective signal - the signal that says "this will take longer than you think" - is treated as obstruction, the room loses its only empirical check on complexity. Modules were voted in during 2019. Five years later, support remains experimental on two of three compilers and build system integration is incomplete. The room had access to implementer estimates before the vote. The estimates were not wrong. They were discounted.

**Procedural momentum.** A paper at revision R3 or R4 has accumulated years of author labor, multiple rounds of committee feedback, and a trail of straw polls. Opposing such a paper requires a delegate to assert that the accumulated process was insufficient - a socially expensive claim. The result is a "paid its dues" heuristic that operates independently of implementation cost. C++20 consolidated modules, coroutines, concepts, ranges, format, and constexpr allocation into a single release. Each had extensive revision histories. Each cleared every procedural gate. The combined implementation burden produced the largest gap since C++11, with GCC and Clang both exceeding 64 months of incomplete conformance. Procedural completion and implementation feasibility are orthogonal, but the room treats the first as evidence of the second.

**The train model.** [P1000](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1000r4.pdf)<sup>[[21]](#ref-21)</sup> established a fixed three-year release cadence. A feature that misses the train waits three more years. This creates deadline pressure that compresses the final stages of standardization. The pressure runs in one direction: toward inclusion. A feature author facing a three-year delay has strong incentive to push for adoption now. An implementer facing a three-year delay in shipping has no corresponding lever. The asymmetry is visible in C++20, where the volume of features adopted into a single release exceeded anything the implementers could absorb within the subsequent cycle. Ranges and format required committee DRs after publication, forcing MSVC to delay /std:c++20 conformance mode and backport over one hundred commits. The train departs on schedule. Whether the cargo is deliverable is evaluated after departure.

**Loss aversion asymmetry.** A delegate who votes for a feature that proves difficult to implement bears no individual cost. The vote is one among two hundred on a ballot. A delegate who votes against bears visible cost: The paper author knows, the study group knows, and the vote is recorded against a specific person blocking a specific proposal.

> "The response to losses is stronger than the response to corresponding gains."<sup>[[22]](#ref-22)</sup>

This asymmetry biases the room toward adoption. The bias compounds with procedural momentum. Intel's 2021 decision to abandon its standalone C++ frontend - concluding that maintaining one was no longer economically viable - demonstrates the downstream cost of accumulated complexity. But that cost is borne outside the room, by organizations that never cast a vote.

**Synthesis.** These six forces do not operate independently. Goal displacement defines what the room measures. Shifting baselines suppress the alarm that the measurements have diverged from outcomes. Implementer feedback suppression removes the corrective signal. Procedural momentum makes late-stage rejection socially prohibitive. The train model adds deadline pressure toward inclusion. Loss aversion asymmetry ensures that when the vote comes, the path of least individual resistance is yes. The result is a system that reliably produces standards faster than they can be implemented - not because any participant intends that outcome, but because the incentive structure makes it the equilibrium. The data confirm the prediction: Each standard from C++17 onward ships with a larger implementation gap than its predecessor, and each is adopted more slowly by the users the standard exists to serve.

---

## 12. C++26 Predictions

C++26 will be the first standard where every headline feature carries a history of implementation failure, design reversal, or zero production deployment at the time of adoption. Contracts were voted into C++20 and removed before publication. Reflection has been in committee since SG7 formed in 2013 with no upstream compiler implementation. std::execution accumulated 24 revisions across two paper lineages over ten years with no production deployment before the vote. Each demands new compiler infrastructure, new library surface, or both.

The trend data is unambiguous. C++14 achieved near-complete conformance within 27 months across all compilers. C++17 split: Language shipped on time, library exceeded 53 months on GCC and 100 months on Clang. C++20 remains incomplete on two of three compilers after 64 months. C++23 is incomplete on all three after 18. The deficit compounds - C++23 implementation began before C++20 was finished. The compilers that will implement C++26 have not finished C++20.

The features voted into C++26 sit at the intersection of every difficulty category identified in Section 8. Reflection expands the constexpr surface area (compounding evaluator burden), introduces compile-time metaprogramming over AST data, and depends on library surface that does not yet exist. Contracts introduce a new evaluation model with multiple semantics the committee has not resolved - the Tokyo 2024 poll on enforce-only showed 24 Strongly Against versus 6 Strongly Favor. std::execution ships without thread pool, without coroutine task type, and without standardized networking - after killing the Networking TS that had 20 years of production deployment.

1. **No compiler will claim full C++26 language and library conformance within 36 months of publication.** C++14 is the only standard where all three compilers achieved conformance within 27 months, and it was deliberately small. C++20 - the nearest comparable in scope - produced a 64+ month gap on two of three compilers. C++26 introduces three features (contracts, reflection, std::execution) each comparable in implementation cost to C++20 modules or coroutines individually, with no production implementation of any of the three at the time of the vote.

2. **Reflection will take 4-6 years post-publication for complete implementation across all three compilers.** It is the largest new compile-time surface since constexpr itself, requiring the compiler to expose AST-level data to constexpr evaluation. The only existing implementation is Bloomberg's experimental Clang fork - not upstream, not production. The constexpr evaluator burden compounds: Each prior expansion added surface the evaluator must support, and MSVC has still not completed [P2564R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2564r3.html)<sup>[[12]](#ref-12)</sup> from C++23. Sutter called reflection "more transformational than any 10 other major features we've ever voted into the standard combined." That describes the implementation burden as precisely as the capability.

3. **Contracts will undergo post-publication design revision within 24 months of publication.** The precedent is exact: Contracts were voted into C++20 ([P0542R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0542r5.html)<sup>[[23]](#ref-23)</sup>, Rapperswil 2018) and removed before publication ([P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf)<sup>[[24]](#ref-24)</sup>) because EWG kept approving design changes after adoption. The current design ([P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2900r14.html)<sup>[[25]](#ref-25)</sup>) carries four evaluation semantics (ignore/observe/enforce/quick-enforce). The Tokyo 2024 poll revealed deep disagreement on whether enforce-only was sufficient. [P4020R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4020r0.pdf)<sup>[[26]](#ref-26)</sup> raises reliability concerns for security-critical code before any compiler has shipped an implementation. A feature with four modes, unresolved committee disagreement on the correct default, and zero deployment is the archetype of a specification that changes after publication.

4. **C++20 will still be incomplete on at least one major compiler when C++26 publishes.** GCC's module implementation carries approximately 48 FIXMEs after five years and remains experimental. Clang lists C++20 language conformance as "Partial" with no projected completion date. The C++17 libc++ precedent is instructive: Parallel algorithms were never implemented and show no path to completion after 100+ months. Features requiring architectural changes to the compiler do not converge with time. They persist as permanent gaps.

5. **std::execution will not produce a portable async networking facility within the C++26 cycle.** The Networking TS - backed by 20 years of Boost.Asio production deployment, the most implementation evidence of any feature in committee history - was declared "no longer relevant" in February 2025. [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[[27]](#ref-27)</sup> ships without thread pool or coroutine task type. No sender/receiver-based networking has shipped in production. The executor model that displaced Asio's has 24 revisions and zero deployment. Networking has been in committee for 23 years with zero standardized result.

6. **At least one major compiler vendor will de-prioritize full ISO conformance in favor of selective C++26 implementation, creating a de facto dialect.** The cumulative backlog is three standards deep: unfinished C++20, incomplete C++23, and C++26 arriving on top. Compiler teams are not growing - Intel abandoned its standalone frontend in 2021. [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup>, signed by 18 implementer co-authors, constitutes the largest implementer intervention in committee history, a signal that implementation capacity has been exceeded. When the backlog exceeds capacity, prioritization replaces conformance.

7. **Library conformance for C++26 will lag language conformance by 3 or more years on open-source compilers.** This pattern held for every non-trivial standard: C++11 GCC language +21 months, library +43; C++17 GCC language -7 months, library +53; C++17 Clang library 100+ months and never completed. std::execution alone represents a library surface comparable to ranges. Reflection's library component adds a second major surface. libstdc++ and libc++ are volunteer-maintained with expanding API obligations. The structural conditions that produced every prior library lag - constrained maintainer pools, ABI decisions, algorithms that may not exist at publication time - apply to C++26 with greater force.

---

## 13. How This Paper Will Read

The data in this paper will land differently depending on where the reader sits. A working group chair will see a compiler problem. A feature champion will feel attacked by category. An engineer whose paper was rejected on procedural grounds will feel validated. A delegate who votes on papers he has not read will feel discomfort. A newcomer who left will feel nothing new. An expelled insider will see ammunition. A developer who writes C++ daily and has never attended a meeting will see confirmation of what they already know.

The sections that follow examine these reactions. They are structural predictions derived from the same institutional analysis that produced the findings above. Each describes a composite - a structural position within or outside the committee, not a specific individual. The reader is invited to notice which reaction matches their own.

| # | Reader | Structural Position | Predicted Reaction |
|---|--------|--------------------|--------------------|
| 14 | Chair | Working group chair, 6+ years, controls agenda and poll framing | Sees a compiler problem, not a committee problem |
| 15 | Architect | Feature champion, R6, co-authors from two vendors | Feels attacked by category - his feature IS good |
| 16 | Author | Mid-career engineer, correct paper, no standing | Validation - the data confirms his experience |
| 17 | Delegate | One of eighty, votes on papers he has not read | Discomfort without agency |
| 18 | Newcomer | Young engineer, presented to six people, left | Nothing new - she already exited |
| 19 | Patron | Expelled insider, mentors from the margins | Ammunition - knows what to do with this |
| 20 | Public | Five million developers, no vote, no voice | "I knew it" - confirmation before exit |

These characters are composites drawn from structural analysis of WG21's published record. No character represents a single individual. The dynamics are structural.

---

## 14. The Chair

> "Voters face a take-it-or-leave-it choice between the setter's proposal and a reversion option."<sup>[[28]](#ref-28)</sup>

The Chair is a composite figure representing the structural position of a long-serving working group chair within WG21. He has held the role for years, appointed by the convener with no fixed term, no formal recall mechanism, and no ex-post performance review. He controls the agenda, frames the polls, and delivers the summary before the vote. He is courteous, organized, and by every procedural measure, fair. His professional identity is inseparable from the claim that the room he runs produces good outcomes through good process. He is a structural position with unconstrained discretion and no feedback loop.

The Chair will reject this paper's central thesis - that WG21's procedures systematically produce features the ecosystem cannot absorb - while accepting nearly all of its data. He will do so out of structural necessity: Accepting the thesis would require him to conclude that the process he has optimized for decades is itself a cause of failure. This is not a conclusion his position permits. He will instead read the paper as a collection of compiler engineering problems misattributed to committee governance, and he will defend that reading with procedurally correct, structurally irrelevant rebuttals.

The timeline data showing GCC and Clang implementation gaps exceeding 64 months for C++20 features will register as a compiler resourcing problem. The Chair knows that GCC and Clang are volunteer-heavy projects with finite engineering bandwidth. He will note, correctly, that the committee cannot compel compiler vendors to hire more engineers. He will point out that MSVC shipped C++20 modules before GCC did, which proves the specification was implementable. He will not engage with the structural question the data poses: whether a process that routinely produces specifications requiring five to seven years of post-vote implementation effort is functioning as intended. Romer and Rosenthal's (1978) framework for monopoly agenda-setters is precise here<sup>[[28]](#ref-28)</sup> - the Chair does not need to consciously extract concessions. He need only control the sequence of business, the framing of polls, and the interpretive summary that precedes them. The concession is extracted by the structure, not the person.

[P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup>'s observation that the committee "does not have any requirement on implementation experience to adopt a proposal" will provoke a specific and practiced rebuttal: Implementation experience is encouraged, frequently provided, and weighed when available. The Chair will cite cases where implementation feedback changed outcomes. He will not address the structural point - that encouragement without requirement is not a constraint. Merton's (1940) analysis of goal displacement describes the mechanism exactly<sup>[[19]](#ref-19)</sup>: the procedure of soliciting feedback has become the goal, displacing the original purpose of ensuring that voted-in features are implementable at production quality. The committee can point to process steps labeled "implementation feedback" while adopting features that no compiler has shipped in a conforming mode. The label satisfies the procedure. The procedure satisfies the Chair.

[P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup>'s finding that implementer feedback is "framed primarily as an obstacle to progress" will strike the Chair as editorializing. He has seen implementers raise objections that were heard, discussed, and voted on. The process worked. What he cannot see is the selection effect: Implementers who raised concerns that were heard and then outvoted eventually stop raising concerns. The feedback mechanism exists. The feedback loop does not. Ashby's (1956) law of requisite variety requires that a self-correcting system have independent channels of negative feedback<sup>[[14]](#ref-14)</sup>. WG21's feedback channels run through the same agenda-setting and poll-framing structures that produced the outcome being evaluated. The Chair is the feedback loop's bottleneck and its judge.

The multi-decade feature histories will be the hardest data for the Chair to reframe. Contracts consumed 22 years of committee time, were voted into C++20, and then removed before publication. Reflection has been under active development for 12 years with no production implementation. Networking was declared unsuitable for standardization after 23 years despite Boost.Asio's two decades of deployment across millions of lines of production code. Intel abandoned its own C++ frontend entirely. The Chair will address each one individually - Contracts had a design flaw, Reflection is technically ambitious, Networking faced legitimate design questions, Intel made a business decision. Each individual explanation is defensible. The pattern they form is not addressable within the Chair's framework because the framework evaluates process, not outcomes. North's (1990) institutional analysis asks a single question: Does the institution produce what it claims to produce?<sup>[[13]](#ref-13)</sup> The Chair's framework cannot ask this question because the answer might implicate the process he embodies.

The moment the Chair cannot name is the gap between two facts he holds simultaneously: that his process is fair, and that his process produced Contracts, Reflection, and Networking. Fair procedures produced outcomes no one defends. The discomfort is not intellectual - the Chair is intelligent enough to see the pattern. It is structural. His role has no mechanism for acknowledging that procedural fairness and institutional functionality are different properties. To name the gap would be to admit that he has spent years optimizing for the wrong variable.

The Chair will not change. He will not change because his position offers no incentive to change, no mechanism to evaluate whether change is needed, and no accountability for the outcomes his process produces. He will retire from the role eventually, and his successor - appointed by the same convener, with the same unconstrained discretion, the same absent term limits, the same missing feedback loops - will inherit the same structural position and optimize for the same variable. The process will continue to be fair. The features will continue to take seven years to compile.

---

## 15. The Architect

> "If both parties to the relationship are utility maximizers, there is good reason to believe that the agent will not always act in the best interests of the principal."<sup>[[15]](#ref-15)</sup>

The Architect is a composite. He represents the committee member whose career is measured in papers advanced: fifteen years of attendance, six revisions of a single feature, co-authors from two compiler vendors whose release schedules name his proposal. His feature is in the working draft or has shipped in at least one toolchain. His standing in the committee - his place in what members informally recognize as a peerage of influence - rests on that record of procedural success. He is a skilled agent operating inside a system that rewards the wrong output.

He reads this paper and feels attacked by category. Not by name - his name does not appear - but by structural position. The paper argues that the committee produces standards faster than compilers can implement them, that "features per revision" has become a metric decoupled from "useful improvements delivered to programmers," and that the incentive structure rewards paper authors for advancing proposals through votes rather than through deployment. The Architect's entire career is a case study in that incentive structure. He won. The paper says the game measures the wrong thing.

His first response is to distinguish his feature from the failures. Modules required 25,000 lines in GCC and remain experimental after five years. Coroutines shipped without a standard library type. Charconv was standardized before the algorithms it specified had been invented. His feature is not like those. His feature works - or will work, once the remaining compiler catches up. This distinction is real but irrelevant to the structural argument. The paper does not claim every feature is broken. It claims the process that advanced his feature is the same process that advanced modules and coroutines, and that nothing in that process distinguishes "ready to ship" from "ready to vote." [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> confirms there is no requirement for implementation experience before a feature enters the working draft. His feature survived the pipeline not because the pipeline filters for quality but because he is talented enough to produce something that works despite a pipeline that does not check.

The principal-agent framework (Jensen and Meckling, 1976) is the one that stings<sup>[[15]](#ref-15)</sup>. The paper observes that paper authors do not bear the cost of implementation. The Architect bore enormous cost - years of drafting, revision, negotiation, straw polls, wording reviews - but in committee currency, not in compiler-engineering currency. The mass of the iceberg sits in the compiler: the register allocation, the ABI constraints, the interaction with every other feature shipped in the same revision. Someone else pays that bill. His co-authors from the compiler vendors were in the room, and they supported the design - but the paper documents what happens when vendor representatives agree to schedules they cannot keep. MSVC announced in 2018 that it was "completely rewriting our constexpr evaluator." [P2564R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2564r3.html)<sup>[[12]](#ref-12)</sup>, a constexpr feature voted into C++23, remains unimplemented. The vendor co-author's presence in the room is not the same as the vendor's capacity to deliver.

Goodhart's Law (1984) frames his career metric as a symptom<sup>[[16]](#ref-16)</sup>. When "papers advanced" becomes the measure of a committee member's contribution, it ceases to be a good measure of whether the standard is improving. The Architect advanced papers. He won polls. He completed revisions. By every metric the committee tracks, he succeeded. The paper argues that those metrics diverge from the outcome that matters - code that compiles, runs correctly, and is available to programmers on the toolchains they actually use. C++20 added modules, coroutines, concepts, ranges, format, and constexpr allocation in a single revision. None were fully implemented on all major compilers within 64 months of ratification. The committee measured throughput. The field experienced a backlog.

Merton's (1940) concept of goal displacement describes the mechanism precisely<sup>[[19]](#ref-19)</sup>. The original goal - improve the language for its users - has been displaced by the procedural goal of advancing papers through the committee's stages. The Architect's sixth revision is evidence of extraordinary procedural stamina, not necessarily of deployment readiness. He heard implementer feedback. He may even have incorporated some of it. But the process does not require him to wait for implementation before advancing, and [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup> frames implementer objections as obstacles to be managed rather than signals to be heeded. The capacity constraints that Laffont and Tirole (1993) describe<sup>[[17]](#ref-17)</sup> - finite compiler-engineering bandwidth allocated across too many simultaneous features - are visible in the data but absent from the committee's decision framework. No stage gate asks "can the implementers absorb this alongside everything else we voted in this cycle?"

The Architect will not absorb the paper's thesis because absorbing it requires him to reclassify his achievement. His feature is good. The work was real. The cost was significant. But the paper says the currency was wrong - that procedural success inside a misaligned system is not the same as contribution to the language's users. Accepting that reframing means accepting that fifteen years of effort optimized for the wrong objective function. The psychological cost of that reclassification exceeds the cost of dismissing the paper. So he does what skilled agents in misaligned systems always do: He defends the metric that validates his record, attributes the implementation failures to other people's features, and continues advancing his next paper through a process that still does not ask whether the compilers can keep up.

---

## 16. The Author

> "If a satisfactory answer to a hard question is not found quickly, System 1 will find a related question that is easier and will answer it."<sup>[[29]](#ref-29)</sup>

The Author is a mid-career engineer at a company that ships C++ in production. He holds no committee office. He has no co-authorship history with major compiler vendors. His employer sends him to one meeting per year. He wrote a paper proposing an alternative to an established proposal at R6 - a proposal with six revisions, three study group rotations, and co-authors from two compiler vendors. His alternative disclosed tradeoffs the incumbent did not. It reported 18 months of deployment data from production systems. He presented to a working group at 3:45 PM on the final day of a plenary week. The room had thinned by a third. He lost 22-34. The first questioner did not ask about his deployment data. The first question was why his design deviated from what "already exists." He returned six months later with a co-author from a second organization and a second independent implementation. He narrowed the margin to 18-22. The paper was technically correct both times.

He reads this paper and feels relief before anything else. The data confirms that the system which evaluated his paper on procedural standing rather than deployment evidence is the same system that produces standards compilers cannot implement within five years. Section 10 confirmed all six structural lenses. Section 11 documented the behavioral forces. The problem is not that his paper was bad. The problem is that the room's evaluation function substitutes procedural maturity for technical merit, and that substitution operates on every paper, not just his.

The goal displacement Merton (1940) described operates directly on his case<sup>[[19]](#ref-19)</sup>. His paper was R0. The incumbent was R6. The room's implicit weighting treated revision count as evidence of quality - a paper that has survived six rounds of committee feedback must be more mature than one at its first appearance. This weighting ignores the content of the revisions. His R0 carried 18 months of deployment data. The R6 carried six revisions of committee feedback and zero months of deployment data. [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> confirms that WG21 has no requirement for implementation experience to adopt a proposal. The room measured what it measures - procedural progress - and his paper scored zero on that axis regardless of what it contained.

The first questioner's framing is the attribute substitution Kahneman (2011) described<sup>[[29]](#ref-29)</sup>: the hard question ("which design has better deployment evidence?") is replaced by an easier one ("which design matches what the committee has already invested in?"). Framing his paper as a deviation from what "already exists" converted a technical comparison into a legitimacy contest. The incumbent existed in the committee's procedural record. His paper existed in production systems the questioner had never seen. The substitution is not conscious. It operates through the availability of information. Committee members have read the R6. They have not used either implementation.

His paper was a corrective signal in the sense Ashby (1956) described<sup>[[14]](#ref-14)</sup> - it carried empirical data about tradeoffs the incumbent design had not addressed. The system damped that signal through the same mechanism Section 11 documented for implementer feedback: Corrective information is "framed primarily as an obstacle to progress"<sup>[[1]](#ref-1)</sup>. The burden of proof ran in one direction. The alternative must justify its departure from the established proposal. The established proposal need not justify its lack of deployment evidence. This asymmetry is structural.

The paper's case studies confirm the pattern at scale. Networking had 23 years of committee history and more production deployment evidence than any other feature in WG21's record. It was declared "no longer relevant" in February 2025. Contracts have 22 years of procedural churn, were voted in once and removed before publication, and carry unresolved design disagreements visible in the Tokyo 2024 polls. His experience - deployment evidence discounted, procedural standing weighted - is a specific instance of the general case.

What he does with the validation defines his next move. Grievance is the path of least resistance - the data confirms he was treated unfairly, and unfairness is a stable resting point. Strategy requires a harder recognition: The system's dysfunction is not aimed at him. It is structural. He can return with a co-author from a third organization, a third implementation, and a paper at R2 that has absorbed the committee's stated objections. Or he can conclude that the evaluation function cannot be satisfied and redirect his effort. Both are rational responses. Only one requires continued engagement with the system that produced the gap this paper measures.

---

## 17. The Delegate

> "It is irrational to be politically well-informed because the low returns from data simply do not justify their cost in time and other resources."<sup>[[30]](#ref-30)</sup>

He is one of eighty who vote in plenary. He represents his employer competently. He votes on fifteen to thirty polls per session and has read the papers for three. His hand goes up when the room's hand goes up. He is not a chair, not an architect, not a champion. He is the median voter (Black 1948)<sup>[[31]](#ref-31)</sup>, and in a consensus body his default state - mild agreement with whatever sounds reasonable - is the most powerful political force in the room.

This paper describes him with clinical precision, and he knows it. Section 11's loss aversion asymmetry is his voting behavior stated as a theorem. He votes yes because voting yes is invisible and voting no is not. He votes on papers he has not read because the cost of reading four hundred papers per cycle exceeds any benefit his single vote could capture<sup>[[30]](#ref-30)</sup>. He is rationally ignorant about ninety percent of the committee's work, and the rationality of that ignorance is what makes the pattern durable.

The bandwidth gap is not a personal failing. It is a structural property of the role. Eighty delegates voting on thirty polls cannot all have read all thirty papers. The room knows this. The chairs know this. The system depends on it. Consensus-as-silence treats his default state - not objecting - as affirmative agreement. When the chair asks for objections and none arise, the room has not reached consensus. It has counted his silence. He did not consent. He simply did not object, and the institution recorded those as the same thing.

> "Self-censorship of deviations from the apparent group consensus, reflecting each member's inclination to minimize to himself the importance of his doubts and counterarguments."<sup>[[32]](#ref-32)</sup>

Janis (1972) identified the mechanism: Self-censorship combined with an illusion of unanimity produces outcomes that no individual member would have chosen independently<sup>[[32]](#ref-32)</sup>. Lorenz et al. (2011) demonstrated that social influence in sequential decisions degrades the accuracy of group judgment<sup>[[33]](#ref-33)</sup>:

> "Although groups are initially 'wise,' knowledge about estimates of others narrows the diversity of opinions to such an extent that it undermines the wisdom of crowd effect."<sup>[[33]](#ref-33)</sup>

The room's straw polls run sequentially. His hand follows the room's hand.

He voted for modules. They remain experimental on two of three compilers five years later. He voted for coroutines. They carry 84 open bugs in GCC and an unfixable ABI defect in Clang. He ratified outcomes that 42.50% of workplaces now prohibit<sup>[[11]](#ref-11)</sup>. These facts do not embarrass him individually because no individual vote is traceable to a specific outcome. The vote was two hundred to twelve, or it was consensus by silence, and either way his hand was one among many. Newham and Midjord's (2018) analysis of FDA advisory committees found that 46% of members consider previous votes and 17% change their own vote in response<sup>[[34]](#ref-34)</sup> - herding behavior in a body designed to aggregate independent judgment. WG21's consensus model amplifies the effect. There is no recorded vote. There is no dissent on the record. There is a room temperature, and he reads it.

The discomfort this paper produces is real. He recognizes the mechanism. He can see that his rational ignorance, multiplied across eighty delegates, is the substrate on which procedural momentum, loss aversion, and consensus-as-silence operate. He is collectively the most powerful political force in the room and individually powerless to change the outcome. The structural position that makes his conformity rational also makes his dissent costly. Voting against the room's mood risks visibility - the paper author notices, the study group chair notices. The expected benefit of a single dissenting vote on a thirty-item ballot is near zero. The expected cost - social exposure in a body where belonging is the primary asset - is immediate and personal.

What he does with this paper is nothing. Not from apathy, not from agreement, not from ignorance of the problem. From calculation. The incentive gradient points toward conformity and has always pointed toward conformity. He will attend the next plenary. He will vote on twenty-five polls. He will have read the papers for four. His hand will follow the room's hand. The implementation gap will widen. His calculation will remain correct.

---

## 18. The Newcomer

> "Learning viewed as situated activity has as its central defining characteristic a process that we call legitimate peripheral participation."<sup>[[35]](#ref-35)</sup>

She is thirty, an engineer at a company with forty developers in a country that sends one delegate to WG21. She wrote a paper that solved a real problem - a library deficiency her team had worked around for three years. She submitted it through the proper channels, secured a presentation slot, and flew to the meeting on her own budget. She presented to six people in a half-empty room at 4:30 on the last day of the plenary week. Two asked questions. One was checking email. The chair thanked her and moved to the next agenda item. She did not return.

She reads this paper and feels nothing new. The data confirms a cost-benefit calculation she already completed. She is not angry. She is not vindicated. She exited the system eighteen months ago and built the feature she proposed as an internal library at her company, where it ships in production. Every finding - the growing implementation gap, the suppression of implementer feedback, the procedural filters that select for persistence over correctness - matches what she observed firsthand. She does not need the institutional analysis. She lived it.

Lave and Wenger (1991) describe professional socialization as a process of legitimate peripheral participation<sup>[[35]](#ref-35)</sup>: newcomers enter a community of practice, learn its norms through supervised engagement, and either internalize those norms or leave. Her experience follows the prediction exactly. She entered WG21 through the documented path. She wrote a paper. She attended a meeting. She presented. The community's response was structurally indistinguishable from rejection: a slot at the end of an exhausted schedule, an audience too small to constitute quorum, no follow-up, no mentor, no indication that a path forward existed. She internalized the norm - that the committee selects for institutional backing and procedural endurance, not for deployment evidence - and acted on it by leaving.

The selection mechanism is visible in the data. [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> establishes that WG21 has no requirement for implementation experience to adopt a proposal. But procedural maturity - revision count, study group history, co-authors from major vendors - determines reception. A paper at R0 from an engineer without committee history faces a filtration system that is formally neutral and structurally exclusionary. The committee selects for delegates who can attend six meetings over three years, who have employers willing to fund travel and lost productivity, who can navigate the study group topology, and who can absorb rejection without exit. Michels (1911) identified this pattern<sup>[[36]](#ref-36)</sup>:

> "Who says organization, says oligarchy."<sup>[[36]](#ref-36)</sup>

Organizations that select for procedural skill over substantive contribution develop an oligarchic structure where advancement correlates with institutional fluency.

She is Pauly's (1995) shifted baseline made visible<sup>[[20]](#ref-20)</sup>. Those who find the current pace abnormal - who compare the committee's output against the C++14 baseline where Clang shipped conformance eleven months before publication - do not acclimate. They leave. The delegates who remain are those for whom the current gap is normal. Her departure is not an anomaly. It is the selection mechanism operating as designed: The system retains those who tolerate the gap and ejects those who do not. The talent pipeline narrows with each cycle not because talent is scarce but because the system's filtration rate exceeds its absorption rate. Laffont and Tirole (1993) predict this for capacity-constrained systems<sup>[[17]](#ref-17)</sup> - when a system cannot process its inputs, it sheds load. She is shed load.

The structural cost of her departure is not her paper. It is the information her paper carried. She had deployment evidence. She had identified a gap the committee had not addressed. The committee's inability to absorb her contribution is the same capacity constraint that produces the implementation gap itself. If Asio's twenty years of production deployment did not prevent networking from being declared dead after twenty-three years in committee, her two years of deployment evidence were never going to matter. She builds outside the committee's walls now. Her library ships. Her users use it. She is the talent pipeline's output, and the evidence that the pipeline is broken.

---

## 19. The Patron

> "In any bureaucracy, the people devoted to the benefit of the bureaucracy itself always get in control, and those dedicated to the goals the bureaucracy is supposed to accomplish have less and less influence, and sometimes are eliminated entirely."<sup>[[37]](#ref-37)</sup>

The Patron is a composite representing a class of former insiders - long-serving committee participants who contributed substantively over years or decades but held no formal office. They were not expelled by vote or censure. They were expelled by accumulation: procedural friction, social cost, the quiet withdrawal of collaboration from those who challenge consensus. They now operate from the margins - mentoring newer participants, publishing outside committee channels, building tooling and processes that route around the dysfunction they could not reform from within. They are the committee's most dangerous critics because they understand both the process and its consequences. They have been making the argument this paper formalizes - that the committee serves itself rather than its users - for years, informally, to anyone who will listen.

The Patron does not read this paper as a diagnosis. He reads it as ammunition. Not for vindication - he passed that threshold years ago. The paper supplies what his informal arguments have always lacked: formalized structural analysis, quantitative baselines, and cross-validated evidence from multiple independent lenses. Where he previously told colleagues "the room protects itself," the paper provides the institutional economics term (goal displacement<sup>[[19]](#ref-19)</sup>), the measurement (C++20 conformance at 64+ months and counting against a C++14 baseline of months), and the confirmation across six structural and six behavioral dimensions. He now has a citable artifact. He will use it.

The implementation gap data lands first because it is the hardest to dismiss. The Patron has watched the conformance timeline stretch across standard after standard, but the specific quantification - C++14 in months, C++20 still incomplete after 64+ months, Intel abandoning its own frontend entirely - converts anecdote into evidence. He has argued for years that the committee adds features faster than implementations can absorb them. The capacity constraint lens<sup>[[17]](#ref-17)</sup> and the shifting baselines<sup>[[20]](#ref-20)</sup> formalize exactly this dynamic: Each standard redefines "current" before implementers finish the previous one, and no institutional mechanism tracks or corrects the growing delta. The JetBrains survey data showing 42.50% of users prohibited from adopting C++20<sup>[[10]](#ref-10)</sup><sup>[[11]](#ref-11)</sup> confirms his long-standing claim that committee output and user reality have diverged.

The case studies in networking, contracts, and executors supply the granular evidence the Patron has described in fragments across conference hallways and mailing list posts. Networking's 23-year arc - the most deployment evidence of any proposed feature, killed not by technical failure but by procedural attrition - is the case he cites most often. Contracts' 22-year trajectory ending in adoption and then removal demonstrates that even successful navigation of the process guarantees nothing. [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup>, authored by 18 implementers, is particularly significant to the Patron because it represents the formal emergence of the critique he has made informally. The paper's finding that implementer feedback was "framed primarily as an obstacle to progress" is the institutional mechanism he has described as "the room decides what counts as feedback."

The six structural lenses and six behavioral forces give the Patron something he has never had: a taxonomy. His informal critique has always been directionally correct but structurally ad hoc. The paper separates the mechanisms, which means they can be addressed independently. Unbundled and formalized, each mechanism demands its own institutional response.

The Patron's response to this paper is operational. He publishes commentary linking the paper's findings to specific committee decisions his audience has witnessed. He uses the structural lenses in mentoring conversations with younger participants who are encountering the dynamics for the first time and lack the vocabulary to describe what they are experiencing. He incorporates the implementation gap data into arguments for alternative processes - smaller, implementation-first working groups that require conformance evidence before feature adoption. He does not expect the committee to reform itself; the paper's own analysis of absent self-correction explains why. He expects the paper to accelerate the construction of alternatives by giving the growing population of dissatisfied participants a shared analytical framework. The paper is a tool, and the Patron is the character who knows how to use one.

---

## 20. The Public

> "Some customers stop buying the firm's products or some members leave the organization: this is the exit option. The firm's customers or the organization's members express their dissatisfaction directly to management or to some other authority to which the management is subordinate: this is the voice option."<sup>[[38]](#ref-38)</sup>

This section addresses the mass public: the estimated five million C++ developers worldwide who ship production code but hold no vote in WG21, belong to no national body, attend no standards meeting, and possess no formal mechanism for organized voice. They experience the committee's output as accomplished facts - delivered through compiler release notes, migration guides, and Stack Overflow answers written by others. They adopt features one at a time, testing each against a compiler matrix that may span three vendors across two or three major versions. They have the emotional investment of stakeholders and the structural powerlessness of spectators. The 2024 JetBrains survey places their center of mass: C++17 at 43%, C++20 at 34%, C++23 at 21%<sup>[[10]](#ref-10)</sup>. Fully 42.50% report being prohibited from using C++20 at work<sup>[[11]](#ref-11)</sup>. The median C++ developer is not on the reflector, not in a national body, not at CppCon, and 37% do not write unit tests. This is the constituency. It is enormous, diffuse, and silent.

The public will not read the structural diagnosis or the behavioral analysis. They will read the table. And they will say, "I knew it." This reaction - confirmation rather than surprise - is the most important datum in the paper's reception. The practitioner who has waited five years for portable modules, who freezes a codebase on C++17 because the migration cost exceeds the feature benefit, who tells a junior colleague "just use Rust for the new service" - that practitioner already holds an intuitive version of every finding in this paper. What this paper provides is vocabulary. It gives names to dynamics the practitioner has felt but could not articulate: why features arrive broken, why the timeline keeps stretching, why the committee appears unresponsive to deployment reality.

The theoretical framework for this constituency is well established. Hirschman (1970) identified three responses available to members of a declining organization: exit, voice, and loyalty<sup>[[38]](#ref-38)</sup>. The trajectory of the C++ public maps cleanly. C++11 was a loyalty event - the language modernized dramatically, and the community responded with genuine enthusiasm. C++14 and C++17 sustained that loyalty through incremental, reliable delivery. C++20 introduced voice: Modules did not work, coroutines required expert-level boilerplate, and ranges produced error messages that filled terminal windows. By C++26, exit enters the frame. Rust gave them somewhere to go. The 71% who consider their current standard sufficient are not expressing satisfaction - they are expressing the rational calculus of a user who has stopped expecting the next version to help.

Olson (1965) explains why this constituency cannot organize<sup>[[39]](#ref-39)</sup>:

> "Unless the number of individuals in a group is quite small, or unless there is coercion or some other special device to make individuals act in their common interest, rational, self-interested individuals will not act to achieve their common or group interests."<sup>[[39]](#ref-39)</sup>

The benefits of improved C++ standardization are diffuse - spread across five million developers - while the costs of organizing are concentrated on whoever attempts it. The result is a collective action failure so complete that the committee can operate for decades without systematic feedback from its largest constituency. Putnam's (1988) two-level game framework sharpens the point<sup>[[40]](#ref-40)</sup>: WG21 conducts an elaborate internal negotiation among delegations, but unlike trade negotiations, there is no domestic ratification step. The public receives the result. It does not vote on it.

Klemperer (1987) completes the picture<sup>[[18]](#ref-18)</sup>. Switching costs in C++ are measured in billions of lines of code, decades of accumulated expertise, and toolchain ecosystems that have no equivalent elsewhere. The captive user cannot exit quickly even when exit is rational. What exit looks like in practice is not a single dramatic departure but a slow portfolio reallocation: Rust for greenfield projects, frozen C++17 for brownfield maintenance, selective adoption of individual C++20 or C++23 features where compiler support is confirmed. This is not a migration. It is a hedge. And hedging, once it begins, compounds - each new project started in Rust is a project that will never generate demand for the next C++ standard's features.

The critical distinction is between anger and confirmation. Anger is an engagement signal. The developer who writes a furious blog post about modules is still invested in the outcome - still expecting the committee to fix the problem. Confirmation is a disengagement signal. The developer who reads this paper's timeline data and says "I knew it" has already completed the emotional transition. The institution has lost the argument not because the critic won but because the audience stopped listening. "Still waiting for modules to work" and "just use Rust" are not arguments. They are shibboleths - markers of group membership among the frustrated practitioner class, repeated not to persuade but to signal shared experience. When a constituency's discourse collapses from argument to shibboleth, the institution's window for responsive action is closing.

The committee's central demand from this constituency - ship features that work on Monday morning - is the simplest critique in this paper and the most devastating. It requires no knowledge of process, no theory of institutional design, no familiarity with the paper numbering system. It asks only that the features the committee standardizes can be used, portably, in production code, within a reasonable time after publication.

---

## 21. Conclusion

C++14 shipped in compilers before it shipped as a standard. C++20 has not shipped in compilers five years after it shipped as a standard. The distance between those two facts is the finding.

The committee publishes the standard it votes for. The ecosystem ships the standard it can implement. The interval between those two events is measured in months. It is growing. The institutional forces that produce the interval are documented, named, and falsifiable. The predictions are on the record.

---

## Acknowledgments

The eighteen implementer co-authors of [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf)<sup>[[1]](#ref-1)</sup> created the largest implementer intervention in committee history and placed the phrase "framed primarily as an obstacle to progress" into the public record. Aaron Ballman's [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html)<sup>[[2]](#ref-2)</sup> documented the absence of an implementation requirement with the precision needed to cite it. Stephan T. Lavavej named charconv "C++17's final boss" and made the implementation cost visible. Jim Springfield described the 1982 parser and made the architectural debt legible. Casey Carter documented the /std:c++20 completion. The compiler teams at GCC, Clang, and MSVC maintain public conformance tracking pages that make this analysis possible.

---

## References

<a id="ref-1"></a>
[1] [P3962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3962r0.pdf) - "Implementation Feedback on the C++ Standard" (Lisa Lippincott, Michael Wong, et al., 2026).

<a id="ref-2"></a>
[2] [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2274r0.html) - "C++ Standard Library Ready Issues to be Moved in Virtual Plenary" (Aaron Ballman, 2020).

<a id="ref-3"></a>
[3] [GCC C++ Standards Support](https://gcc.gnu.org/projects/cxx-status.html) - GCC conformance tracking page (GCC Project).

<a id="ref-4"></a>
[4] [Clang C++ Status](https://clang.llvm.org/cxx_status.html) - Clang conformance tracking page (LLVM Project).

<a id="ref-5"></a>
[5] [Microsoft C++ Language Conformance](https://learn.microsoft.com/cpp/overview/visual-cpp-language-conformance) - MSVC conformance table (Microsoft).

<a id="ref-6"></a>
[6] Jim Springfield - ["Rejuvenating the Microsoft C/C++ Compiler"](https://devblogs.microsoft.com/cppblog/rejuvenating-the-microsoft-cc-compiler/) (MSVC C++ Team Blog, September 2015).

<a id="ref-7"></a>
[7] Stephan T. Lavavej - "floating-point &lt;charconv&gt;: Making Your Code 10x Faster With C++17's Final Boss" (CppCon, 2019).

<a id="ref-8"></a>
[8] Casey Carter - ["MSVC's STL Completes /std:c++20"](https://devblogs.microsoft.com/cppblog/msvcs-stl-completes-stdc20/) (MSVC C++ Team Blog, May 2022).

<a id="ref-9"></a>
[9] [P1787R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1787r6.html) - "Declarations and where to find them" (Richard Smith, 2020).

<a id="ref-10"></a>
[10] [JetBrains C++ Developer Ecosystem Survey](https://www.jetbrains.com/lp/devecosystem-2024/cpp/) - C++ usage and adoption data (JetBrains, 2022-2025).

<a id="ref-11"></a>
[11] [ISO C++ Annual Developer Survey](https://isocpp.org/blog/2024/04/results-summary-2024-annual-cpp-developer-survey-lite) - C++ standard adoption by workplace (ISO C++, 2023).

<a id="ref-12"></a>
[12] [P2564R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2564r3.html) - "consteval needs to propagate up" (Barry Revzin, 2023).

<a id="ref-13"></a>
[13] Douglass C. North - [*Institutions, Institutional Change and Economic Performance*](<https://doi.org/10.1017/CBO9780511808678>) (Cambridge University Press, 1990).

<a id="ref-14"></a>
[14] W. Ross Ashby - [*An Introduction to Cybernetics*](https://archive.org/details/introductiontocy00ashb) (Chapman & Hall, 1956).

<a id="ref-15"></a>
[15] Michael C. Jensen and William H. Meckling - ["Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure"](https://www.sfu.ca/~wainwrig/Econ400/jensen-meckling.pdf) (*Journal of Financial Economics* 3(4):305-360, 1976).

<a id="ref-16"></a>
[16] Charles A.E. Goodhart - [*Monetary Theory and Practice: The UK Experience*](https://en.wikipedia.org/wiki/Goodhart%27s_law) (Macmillan, 1984). Marilyn Strathern restated the law: "When a measure becomes a target, it ceases to be a good measure."

<a id="ref-17"></a>
[17] Jean-Jacques Laffont and Jean Tirole - [*A Theory of Incentives in Procurement and Regulation*](https://mitpress.mit.edu/9780262121743/a-theory-of-incentives-in-procurement-and-regulation/) (MIT Press, 1993).

<a id="ref-18"></a>
[18] Paul Klemperer - ["Markets with Consumer Switching Costs"](https://www.jstor.org/stable/1885068) (*Quarterly Journal of Economics* 102(2):375-394, 1987).

<a id="ref-19"></a>
[19] Robert K. Merton - ["Bureaucratic Structure and Personality"](https://www.csun.edu/~snk1966/Robert%20K%20Merton%20-%20Bureaucratic%20Structure%20and%20Personality.pdf) (*Social Forces* 18(4):560-568, 1940).

<a id="ref-20"></a>
[20] Daniel Pauly - ["Anecdotes and the Shifting Baseline Syndrome of Fisheries"](https://www.cell.com/trends/ecology-evolution/abstract/S0169-5347(00)89171-5) (*Trends in Ecology and Evolution* 10(10):430, 1995).

<a id="ref-21"></a>
[21] [P1000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1000r4.pdf) - "C++ IS Schedule" (Herb Sutter, 2018).

<a id="ref-22"></a>
[22] Daniel Kahneman and Amos Tversky - ["Prospect Theory: An Analysis of Decision under Risk"](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Behavioral_Decision_Theory/Kahneman_Tversky_1979_Prospect_theory.pdf) (*Econometrica* 47(2):263-291, 1979).

<a id="ref-23"></a>
[23] [P0542R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0542r5.html) - "Support for contract based programming in C++" (G. Dos Reis, J.D. Garcia, J. Lakos, A. Meredith, N. Myers, B. Stroustrup, 2018).

<a id="ref-24"></a>
[24] [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf) - "Remove Contracts from C++20" (Ville Voutilainen, 2019).

<a id="ref-25"></a>
[25] [P2900R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p2900r14.html) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2026).

<a id="ref-26"></a>
[26] [P4020R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4020r0.pdf) - "Concern about Contract Assertions" (2026).

<a id="ref-27"></a>
[27] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "`std::execution`" (Micha&lstrok; Dominiak, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

<a id="ref-28"></a>
[28] Thomas Romer and Howard Rosenthal - ["Political Resource Allocation, Controlled Agendas, and the Status Quo"](https://link.springer.com/article/10.1007/BF03187594) (*Public Choice* 33(4):27-43, 1978).

<a id="ref-29"></a>
[29] Daniel Kahneman - [*Thinking, Fast and Slow*](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow) (Farrar, Straus and Giroux, 2011).

<a id="ref-30"></a>
[30] Anthony Downs - [*An Economic Theory of Democracy*](https://archive.org/details/economictheoryof00down) (Harper & Row, 1957).

<a id="ref-31"></a>
[31] Duncan Black - ["On the Rationale of Group Decision-Making"](https://www.jstor.org/stable/1825026) (*Journal of Political Economy* 56(1):23-34, 1948).

<a id="ref-32"></a>
[32] Irving L. Janis - [*Victims of Groupthink*](https://en.wikipedia.org/wiki/Groupthink) (Houghton Mifflin, 1972).

<a id="ref-33"></a>
[33] Jan Lorenz, Heiko Rauhut, Frank Schweitzer, and Dirk Helbing - ["How Social Influence Can Undermine the Wisdom of Crowd Effect"](https://www.pnas.org/doi/10.1073/pnas.1008636108) (*PNAS* 108(22):9020-9025, 2011).

<a id="ref-34"></a>
[34] Melissa Newham and Rune Midjord - ["Herd Behavior in FDA Committees: A Structural Approach"](https://www.diw.de/de/diw_01.c.593214.de/publikationen/diskussionspapiere/2018_1744/herd_behavior_in_fda_committees__a_structural_approach.html) (DIW Berlin Discussion Paper 1744, 2018).

<a id="ref-35"></a>
[35] Jean Lave and Etienne Wenger - [*Situated Learning: Legitimate Peripheral Participation*](https://www.cambridge.org/highereducation/books/situated-learning/6915ABD21C8E4619F750A4D4ACA616CD) (Cambridge University Press, 1991).

<a id="ref-36"></a>
[36] Robert Michels - [*Political Parties: A Sociological Study of the Oligarchical Tendencies of Modern Democracy*](https://socialsciences.mcmaster.ca/econ/ugcm/3ll3/michels/polipart.pdf) (1911; English trans. 1915).

<a id="ref-37"></a>
[37] Jerry Pournelle - ["The Iron Law of Bureaucracy"](http://jerrypournelle.com/reports/jerryp/iron.html) (2006).

<a id="ref-38"></a>
[38] Albert O. Hirschman - [*Exit, Voice, and Loyalty: Responses to Decline in Firms, Organizations, and States*](https://www.hup.harvard.edu/books/9780674276604) (Harvard University Press, 1970).

<a id="ref-39"></a>
[39] Mancur Olson - [*The Logic of Collective Action: Public Goods and the Theory of Groups*](https://archive.org/details/logicofcollectiv00olso) (Harvard University Press, 1965).

<a id="ref-40"></a>
[40] Robert D. Putnam - ["Diplomacy and Domestic Politics: The Logic of Two-Level Games"](<https://doi.org/10.1017/S0020818300027697>) (*International Organization* 42(3):427-460, 1988).
