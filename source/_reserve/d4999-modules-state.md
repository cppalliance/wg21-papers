---
title: "C++ Modules in 2026: Compiler, Tooling, and Adoption Status Six Years After C++20"
document: D4999R0
date: 2026-07-08
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

C++20 modules have full compiler support from one vendor, partial support from two, one production build system, and an adoption rate of 4.1%.

Since C++20 was published in December 2020, the three major compilers have all implemented named modules, but they differ in completeness, in how modules are enabled, and in whether they ship pre-built standard-library artifacts. MSVC is production-ready; Clang and GCC require manual bootstrapping for `import std;`. CMake 3.28 with Ninja is the most-deployed build-system combination for modules; vcpkg and Conan cannot distribute BMIs. Of 2,587 tracked projects, 107 have module support. The committee has refined the specification through C++23 and C++26. This paper documents what the record shows.

---

## Revision History

### R0: July 2026

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains proposals in the `std::execution` space. The author does not maintain competing proposals related to modules. This paper documents the implementation, tooling, and adoption status of C++ modules as of July 2026.

This paper was produced with machine assistance.

This paper provides four contributions:

1. A compiler-by-compiler status table for named modules, header units, module partitions, and `import std;` across MSVC, Clang, and GCC.
2. A survey of build-system, IDE, and package-manager support for modules.
3. Quantitative and qualitative adoption evidence from tracking data, experience reports, and developer surveys.
4. A record of committee activity on modules since C++20: CWG issues, C++26 papers, and SG15 ecosystem work.

This paper assumes the reader is familiar with the C++20 modules language as specified in [P1103R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1103r3.pdf)<sup>[1]</sup> and with the `import std;` facility added by [P2465R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2465r3.pdf)<sup>[2]</sup>.

This paper asks for nothing.

---

## 2. One Compiler Ships Production Modules

C++20 modules were adopted via [P1103R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1103r3.pdf)<sup>[1]</sup> at Kona in February 2019. This section documents what each major compiler ships as of July 2026. The three implementations differ in completeness, in how modules are enabled, and in whether they ship pre-built standard-library module artifacts.

### 2.1 MSVC

MSVC provides the most complete C++20 modules implementation. Named modules reached feature completeness in Visual Studio 2019 version 16.10, and modules are enabled automatically with `/std:c++20` since version 16.11<sup>[3]</sup><sup>[4]</sup>. Header units are production-ready since version 16.11<sup>[5]</sup>. Module partitions are fully supported. `import std;` shipped in Visual Studio 2022 version 17.5 and is available in C++20 mode since version 17.8<sup>[5]</sup>.

The Visual Studio installer ships standard-library module interface source files (`std.ixx`, `std.compat.ixx`) at `%VCToolsInstallDir%\modules\`<sup>[4]</sup>. IntelliSense support for modules uses a separate frontend (EDG) and can produce false errors in the editor on valid module code<sup>[5]</sup>. Module-related internal compiler errors remain a recurring subject of MSVC Build Tools Preview patches in 2026.

MSVC is the only compiler where a developer can write `import std;`, compile with a standard flag, and link without manual bootstrapping.

### 2.2 Clang

Clang supports named modules since version 16 (March 2023), enabled automatically with `-std=c++20`<sup>[6]</sup>. Module partitions are supported from the same version. Header units are explicitly experimental; the documentation states that "the details described here may change in the future"<sup>[6]</sup>. `import std;` is available since Clang 18.1 with libc++, but users must manually compile the module interface to produce a pre-compiled module (PCM) file and pass `-fmodule-file=std=std.pcm` to every consuming translation unit<sup>[7]</sup>.

No Linux distribution ships pre-compiled PCM files for libc++ as of July 2026<sup>[8]</sup>. Every consumer must be told where every Binary Module Interface (BMI) lives via explicit `-fmodule-file` flags; Clang has no auto-discovery mechanism<sup>[6]</sup>. Work on native Clang driver support for `import std;` without a build system is under active development as of June 2026.

Clang's named-module support is production-grade for projects that use CMake or another P1689-aware build system. Header units and the standard-library module require manual intervention that build-system integration has not yet automated.

### 2.3 GCC

GCC has supported named modules in experimental form since GCC 11, but modules require the `-fmodules` flag and are not enabled by `-std=c++20` alone<sup>[9]</sup><sup>[10]</sup>. The GCC documentation states: "C++20 modules support is still experimental and needs to be enabled by `-fmodules` command-line flag"<sup>[10]</sup>. GCC 16 announced that C++20 is stable but explicitly excluded modules from that announcement.

Three documented gaps remain in the GCC 16.1 implementation<sup>[9]</sup>: private module fragments emit an error rather than compiling; module partition visibility rules are not enforced, allowing definitions to leak outside the module; and textual merging of reachable global-module entities is incomplete. `import std;` works since GCC 15 with libstdc++, but the standard-library module must be manually compiled from `bits/std.cc` before use, and no distribution ships pre-compiled `.gcm` files<sup>[9]</sup>.

GCC treats modules as experimental more than five years after C++20 was published. The separate opt-in flag means that a developer writing standard C++20 code does not get modules unless they know to ask.

### 2.4 Summary

*Table 1: C++20 modules compiler support as of July 2026. "Production" means the vendor documents the feature as ready for use; "experimental" means the vendor warns of instability or incompleteness.*

| Feature | MSVC | Clang | GCC |
|---------|------|-------|-----|
| Named modules | Production (VS 2019 16.8+) | Production (Clang 16+) | Experimental (GCC 11+, requires `-fmodules`) |
| Header units | Production (VS 2019 16.11+) | Experimental | Supported, no pre-built stdlib units |
| Module partitions | Full | Full (Clang 16+) | Partial (visibility rules not enforced) |
| `import std;` | Production (VS 2022 17.5+) | Manual bootstrap (Clang 18.1+) | Manual bootstrap (GCC 15+) |
| Enabled by `-std=c++20` | Yes | Yes | No |
| Pre-built stdlib modules shipped | Yes | No | No |

MSVC provides the most complete implementation with production-ready named modules, header units, and `import std;`. Clang supports named modules for production use but requires manual intervention for header units and standard-library modules. GCC keeps modules behind a separate flag, reflecting the implementation's self-assessed experimental status.

## 3. One Build System Integrates Modules

Build systems must solve a problem that traditional compilation does not present: C++20 modules introduce inter-file dependencies that cannot be determined before scanning source files. A translation unit that writes `import foo;` cannot compile until the build system has located and compiled `foo`'s module interface unit. This section surveys how each build system addresses that ordering problem and what gaps remain.

### 3.1 CMake and Ninja

CMake has the largest user base among build systems with C++20 module support. Named modules exited experimental status in CMake 3.28 (December 2023)<sup>[11]</sup>. CMake uses [P1689R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p1689r5.html)<sup>[12]</sup> dependency scanning: The compiler outputs a JSON file describing which modules each source provides and requires, and CMake generates Ninja `dyndep` files to update the build graph dynamically. This requires Ninja 1.11 or later; Makefile generators are not supported because they lack the dynamic dependency mechanism<sup>[11]</sup>.

`import std;` support is experimental since CMake 3.30<sup>[11]</sup>. Header units are not supported. CMake can install module interface source files via `FILE_SET CXX_MODULES` for the Ninja generator, but the Visual Studio generator has no support for exporting or installing module information<sup>[11]</sup>.

### 3.2 Other Build Systems

*Table 2: Build-system support for C++20 modules as of July 2026.*

| Build system | Named modules | `import std;` | Header units | Notes |
|-------------|---------------|---------------|-------------|-------|
| build2 0.17.0 | Yes | Yes (Clang, MSVC) | GCC only | Uses GCC module mapper protocol<sup>[13]</sup> |
| xmake | Yes | Yes | Yes | Broadest feature coverage<sup>[14]</sup> |
| Meson | Partial | Experimental (1.10.0) | No | Tracking issue open since 2019<sup>[15]</sup> |
| Bazel 9.0.0 | Experimental | In progress | No | Clang only<sup>[16]</sup> |
| MSBuild | Yes | Yes | No | MSVC only |

build2 takes a different approach from CMake: It uses GCC's module mapper protocol for direct build-system-to-compiler communication, falling back to P1689R5 scanning for Clang and MSVC<sup>[13]</sup>. xmake provides the broadest feature coverage, including header units across all three compilers<sup>[14]</sup>. Meson's tracking issue for module support has been open since March 2019; `import std;` support landed in version 1.10.0 (December 2025) behind an experimental flag<sup>[15]</sup>. Bazel 9.0.0 introduced module support limited to Clang, with active development continuing as of June 2026<sup>[16]</sup>.

### 3.3 Package Managers

Neither vcpkg nor Conan has a native workflow for distributing modularized libraries. vcpkg's tracking discussion for C++20 module support has been open since 2021. Conan published an analysis of the packaging problem in October 2023<sup>[17]</sup>, identifying the fundamental constraint: BMIs are compiler-version-specific and cannot be portably distributed.

The Conan team<sup>[17]</sup> and CMake documentation<sup>[11]</sup> both describe the same workaround: Ship module interface source files and compile BMIs locally. This approach works but adds compilation overhead for consumers and contradicts the pre-built binary model that package managers are designed to provide.

### 3.4 IDE Support

CLion provides the most mature IDE support for modules, with auto-import added in CLion 2026.1. Visual Studio's IntelliSense uses a separate frontend and can report false errors on valid module code. clangd supports modules experimentally behind `--experimental-modules-support`. The VS Code cpptools extension depends on EDG for module support, which remains incomplete.

CMake 3.28 with Ninja 1.11 is the most-deployed build-system combination for C++20 modules. build2 and xmake provide working alternatives with different design trade-offs. No package manager distributes binary module interfaces, and no cross-compiler BMI format exists.

## 4. import std Shipped in C++23 but Deploys on One Platform

`import std;` replaces all standard-library `#include` directives with a single import statement. This section traces how standard-library modules reached C++23 and documents where each implementation stands.

### 4.1 From P0581 to P2465

The first proposal for modularizing the standard library was [P0581R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0581r0.pdf)<sup>[18]</sup> (Gabriel Dos Reis, Billy O'Neal, Stephan T. Lavavej, Jonathan Wakely, 2017), which proposed a hierarchical decomposition into partitions such as `std.fundamental`, `std.core`, `std.io`, and `std.threading`. In July 2021, Bjarne Stroustrup argued in [P2412R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2412r0.pdf)<sup>[19]</sup> that the committee could "spend years discussing" fine-grained decomposition and proposed getting a minimal `import std;` into C++23 without further delay.

[P2465R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2465r3.pdf)<sup>[2]</sup> (Stephan T. Lavavej, Gabriel Dos Reis, Bjarne Stroustrup, Jonathan Wakely, 2022) implemented that strategy. It specifies two modules: `import std;` exports all declarations in namespace `std` from the C++ library headers plus global `operator new` and `operator delete`; `import std.compat;` adds the global-namespace C library names such as `::fopen` and `::printf`. Macros are not exported. LEWG approved the design in October 2021; LWG approved the wording in February 2022; CWG approved in March 2022; plenary adopted the paper for C++23 in July 2022<sup>[2]</sup>.

### 4.2 Implementation Status

*Table 3: Standard-library module implementation status as of July 2026.*

| | MSVC STL | libc++ (Clang) | libstdc++ (GCC) |
|---|---|---|---|
| Status | Production | Experimental | Experimental |
| First available | VS 2022 17.5 (Feb 2023) | libc++ 17 (partial) | GCC 15 |
| C++20 mode | Yes (since 17.8) | Yes (extension) | Yes (extension) |
| Pre-built artifacts | Source files (`.ixx`) | Source files (`.cppm`) | Source files (`.cc`) |
| `#include` coexistence | Include-before-import (17.10+) | Include-after-import may fail | Experimental |

MSVC ships standard-library module interface source files with the Visual Studio installer and documents `import std;` as production-ready since VS 2022 17.5<sup>[5]</sup>. The libc++ documentation states that modules are "not considered stable nor complete"<sup>[7]</sup>; the source files must be explicitly installed with `-DLIBCXX_INSTALL_MODULES=ON`, and no Linux distribution ships pre-compiled PCM files. libstdc++ ships source files since GCC 15, and GCC 16 added module initialization functions to `libstdc++.so` in March 2026, but the full pipeline remains experimental<sup>[9]</sup>.

All three implementations support `import std;` in C++20 mode as an extension, per an informal agreement between implementers<sup>[5]</sup>. This agreement reflects a practical consensus that users should not be required to switch to C++23 solely to use library modules.

MSVC is the only implementation where `import std;` is documented as production-ready. libc++ and libstdc++ provide the source files but require manual compilation, and no Linux distribution ships pre-compiled module artifacts.

## 5. Tracked Adoption Stands at 4.1%

This section measures adoption through published experience reports, aggregate tracking data, and developer surveys. Absences are evidence: When a major library does not ship module interfaces, that is a data point about the state of adoption.

### 5.1 Experience Reports

The most detailed published migration account is Wolfgang Bangerth's report on converting deal.II, an 800,000-line finite-element library, to C++20 modules<sup>[20]</sup>. The conversion required six weeks of full-time work and nearly 200 pull requests. Bangerth's assessment: "An only slightly simplified answer to the question 'Does it actually work?' is 'No, not for downstream projects, and at least not automatically.'" He concluded: "There is currently no easy or uniform way to export a project's modules to downstream users"<sup>[20]</sup>.

A 2026 analysis of the tooling landscape observed: "Every successful module adoption I've seen had the same thing: one person who understood P1689R5... That person is the module adoption. When they go on vacation, the build breaks and nobody knows why"<sup>[8]</sup>.

Modules-related talks at CppCon 2024 and CppCon 2025 focused on build-system integration, compiler status, and practical considerations rather than reporting completed production migrations.

### 5.2 Library Adoption

The community tracking site arewemodulesyet.org reports that 107 of 2,587 tracked C++ projects have module support, a rate of 4.1%<sup>[21]</sup>.

The fmt formatting library ships a module interface (`import fmt;`), the only tracked library to do so, and it works reliably only with Clang<sup>[21]</sup>. No other major library ships module interfaces:

*Table 4: Module adoption status of major C++ libraries as of July 2026.*

| Library | Module support | Notes |
|---------|---------------|-------|
| Boost | No | Experimental analysis published January 2025; not production-ready |
| Qt | No | Blocked by Qt moc (Meta-Object Compiler) lacking module awareness |
| LLVM/Clang | No | Does not use modules internally |
| Abseil | No | Header-only, described as C++17 compliant |
| range-v3 | No | No module interfaces in repository |
| folly | No | Header-based |

### 5.3 Survey Data

The ISO C++ Developer Survey 2024 found that 29.25% of respondents planned to allow module usage in the next 12 months, the lowest rate among the three major C++20 features (concepts, coroutines, and modules)<sup>[22]</sup>. The 2025 survey ranked modules third in "most anticipated features," behind reflection and memory safety, confirming that modules are anticipated rather than adopted<sup>[23]</sup>.

The quantitative evidence is consistent across sources. Production adoption of C++20 modules is confined to single-compiler environments and greenfield projects. The gap between the specification and deployment is not the language - it is the ecosystem infrastructure that surrounds it: build systems, package managers, distribution tooling, and cross-compiler BMI portability.

## 6. The Committee Refined the Specification; the Ecosystem Gap Persists

This section records the committee's post-C++20 work on modules: core-language refinements, standard-library additions, and ecosystem tooling efforts.

### 6.1 Core Language

[P1103R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1103r3.pdf)<sup>[1]</sup> specified the modules language for C++20. [P1857R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1857r3.html)<sup>[24]</sup> (Michael Spencer, 2020) was adopted at Prague to resolve 11 national body comments related to the inability to perform fast dependency scanning without full preprocessing. [P1502R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1502r1.html)<sup>[25]</sup> (Richard Smith, 2019) guaranteed that standard-library headers can be imported as header units, providing the minimal library-side modules support for C++20.

Three modules papers were adopted for C++26:

*Table 5: Modules papers adopted for C++26.*

| Paper | Title | Effect |
|-------|-------|--------|
| [P3034R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3034r1.html)<sup>[26]</sup> | Module Declarations Shouldn't be Macros | Prohibits macro expansion in module names (DR against C++20) |
| [P3618R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3618r0.html)<sup>[27]</sup> | Allow attaching main to the global module | Allows `main` in a module unit |
| [P3868R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3868r1.html)<sup>[28]</sup> | Allow #line before module declarations | Fixes P1857R3 strictness (DR against C++20) |

The CWG issues list contains 22 module-related entries, of which 15 have been resolved across C++23 and C++26 and 7 remain active.

### 6.2 Standard Library

[P2465R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2465r3.pdf)<sup>[2]</sup> added `import std;` and `import std.compat;` to C++23. The implementation status of each standard library is documented in Section 4.

### 6.3 Ecosystem

[P1689R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p1689r5.html)<sup>[12]</sup> (Ben Boeckel, Brad King, 2022) defines the JSON format that compilers use to report module dependencies to build systems. All three major compilers implement it. The paper is not part of the C++ International Standard; it is intended for inclusion in the proposed C++ Ecosystem International Standard.

SG15 (Tooling) evolved from a Modules Ecosystem Technical Report effort ([P1688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1688r0.html)<sup>[29]</sup>, Bryce Adelstein Lelbach, 2019) to a broader C++ Ecosystem IS proposal ([P2656R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2656r3.html)<sup>[30]</sup>, Ren&eacute; Ferdinand Rivera Morell, 2024). The Ecosystem IS covers tool interoperation formats including but not limited to modules.

The committee has refined the modules specification through two standard cycles, added `import std;` to C++23, and continued to address defects through C++26. The ecosystem tooling that P1689 and SG15 address - dependency formats, module metadata, build-system interoperability - remains outside the International Standard.

## 7. What the Record Shows

The record as of July 2026 is summarized below.

MSVC provides production-ready named modules, header units, and `import std;` without manual bootstrapping. On Windows, MSVC with MSBuild or CMake and the Visual Studio installer constitute a complete, working modules toolchain. Clang supports named modules for production use but requires manual intervention for the standard-library module and header units. GCC keeps modules behind a separate `-fmodules` flag and documents three implementation gaps.

CMake 3.28 with Ninja 1.11 is the most-deployed build-system combination for modules. build2 0.17.0 and xmake offer alternative paths with different trade-offs; xmake supports header units across all three compilers. Meson and Bazel remain experimental. vcpkg and Conan cannot distribute BMIs; the Conan team and CMake documentation both describe shipping module interface sources and compiling BMIs locally as the current practice<sup>[17]</sup><sup>[11]</sup>. No Linux distribution ships pre-compiled standard-library module artifacts.

Of 2,587 tracked C++ projects, 107 (4.1%) have module support<sup>[21]</sup>. The tracking data does not report a trend, so whether this figure is rising, flat, or declining is not known. No major library ecosystem - Boost, Qt, Abseil, folly, range-v3 - ships module interfaces. The ISO C++ Developer Survey 2024 found that 29.25% of respondents planned to allow modules in the next 12 months, the lowest rate among the three major C++20 features<sup>[22]</sup>.

The committee has resolved 15 CWG issues on modules, adopted three papers for C++26, and added `import std;` to C++23 via [P2465R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2465r3.pdf)<sup>[2]</sup>. The ecosystem tooling work - P1689R5, P2656R3, module metadata formats - proceeds through SG15 but remains outside the International Standard.

The specification is stable. Compiler support ranges from production-ready (MSVC) to experimental (GCC). The build-system, packaging, and distribution infrastructure that connects the specification to working deployments varies by platform and toolchain.

---

## Acknowledgments

The arewemodulesyet.org project provided the aggregate library-adoption data. Wolfgang Bangerth's deal.II migration report provided the most detailed published evidence of a large-scale modules conversion. The compiler and build-system teams at Microsoft, LLVM, GCC, Kitware, and build2 produced the documentation from which this paper draws its findings.

## References

[1] [P1103R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1103r3.pdf) - "Merging Modules" (Richard Smith, 2019).

[2] [P2465R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2465r3.pdf) - "Standard Library Modules std and std.compat" (Stephan T. Lavavej, Gabriel Dos Reis, Bjarne Stroustrup, Jonathan Wakely, 2022).

[3] [cppreference](https://en.cppreference.com/w/cpp/compiler_support/20) - "C++ compiler support: C++20" (cppreference.com, 2026).

[4] [Microsoft Learn](https://learn.microsoft.com/en-us/cpp/cpp/modules-cpp?view=msvc-170) - "Overview of modules in C++" (Microsoft, 2026).

[5] [microsoft/STL#1694](https://github.com/microsoft/STL/issues/1694) - "Tracking issue for C++20/23 Modules" (Microsoft STL, 2021).

[6] [Clang docs](https://clang.llvm.org/docs/StandardCPlusPlusModules.html) - "Standard C++ Modules" (LLVM Project, 2026).

[7] [libc++ Modules](https://libcxx.llvm.org/Modules.html) (LLVM Project, 2026).

[8] [moderncpp.dev](https://moderncpp.dev/articles/c20-modules-the-tooling-gap/) - "C++20 Modules: The Tooling Gap" (2026).

[9] [GCC 16.1 docs](https://gcc.gnu.org/onlinedocs/gcc-16.1.0/gcc/C_002b_002b-Modules.html) - "C++ Modules" (GCC, 2026).

[10] [GCC](https://gcc.gnu.org/projects/cxx-status.html) - "C++ Standards Support in GCC" (GCC, 2026).

[11] [cmake-cxxmodules(7)](https://cmake.org/cmake/help/latest/manual/cmake-cxxmodules.7.html) (Kitware, 2026).

[12] [P1689R5](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p1689r5.html) - "Format for describing dependencies of source files" (Ben Boeckel, Brad King, 2022).

[13] [build2 0.17.0](https://build2.org/release/0.17.0.xhtml) (build2, 2026).

[14] [xmake](https://xmake.io/examples/cpp/cxx-modules.html) - "C++ Modules" (xmake, 2026).

[15] [Meson #5024](https://github.com/mesonbuild/meson/issues/5024) - "C++20 modules are in: discussing a sane (experimental) design for Meson" (Meson, 2019).

[16] [Bazel 9.0.0](https://github.com/bazelbuild/bazel/releases/tag/9.0.0) (Bazel, 2026).

[17] [Conan Blog](https://blog.conan.io/2023/10/17/modules-the-packaging-story.html) - "C++ Modules: The Packaging Story" (Conan, 2023).

[18] [P0581R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0581r0.pdf) - "Standard Library Modules" (Gabriel Dos Reis, Billy O'Neal, Stephan T. Lavavej, Jonathan Wakely, 2017).

[19] [P2412R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2412r0.pdf) - "Minimal module support for the standard library" (Bjarne Stroustrup, 2021).

[20] [arXiv:2506.21654](https://arxiv.org/abs/2506.21654) - "Experience converting a large mathematical software package written in C++ to C++20 modules" (Wolfgang Bangerth, 2025).

[21] [arewemodulesyet.org](https://arewemodulesyet.org/) (2026).

[22] [ISO C++ Developer Survey 2024](https://isocpp.org/files/papers/CppDevSurvey-2024-summary.pdf) (ISO C++ Foundation, 2024).

[23] [ISO C++ Developer Survey 2025](https://isocpp.org/files/papers/CppDevSurvey-2025-summary.pdf) (ISO C++ Foundation, 2025).

[24] [P1857R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p1857r3.html) - "Modules Dependency Discovery" (Michael Spencer, 2020).

[25] [P1502R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1502r1.html) - "Standard Library Header Units for C++20" (Richard Smith, 2019).

[26] [P3034R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3034r1.html) - "Module Declarations Shouldn't be Macros" (Michael Spencer, 2024).

[27] [P3618R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3618r0.html) - "Allow attaching main to the global module" (Michael Spencer, 2025).

[28] [P3868R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3868r1.html) - "Allow #line before module declarations" (Michael Spencer, 2025).

[29] [P1688R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1688r0.html) - "Towards a C++ Ecosystem Technical Report" (Bryce Adelstein Lelbach, 2019).

[30] [P2656R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2656r3.html) - "C++ Ecosystem International Standard" (Ren&eacute; Ferdinand Rivera Morell, 2024).
