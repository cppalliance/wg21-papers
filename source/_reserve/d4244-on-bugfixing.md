---
title: "Two Removals, Thirty Years"
document: P4244R0
date: 2026-08-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

An organisation that cannot correct its mistakes will become overwhelmed by them.

The process that governs WG21 is structurally asymmetric: Adding a feature requires one paper and one set of favourable polls; removing or replacing a feature requires deprecation, a migration path, ABI coordination across every major implementation, and the political will to say the committee was wrong. The language's designer recorded this asymmetry in 1994. The committee's record since then confirms it. This paper examines what the record shows.

---

## Revision History

### R0: August 2026

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space: [P4003R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r0.pdf)<sup>[1]</sup>, [P4007R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4007r0.pdf)<sup>[2]</sup>, and [P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf)<sup>[3]</sup>. This paper does not address networking, senders, or any specific feature. It documents a structural property of the committee's correction process. The author does not propose which defect to fix.

This paper asks for nothing.

---

## 2. The Premise

Software has bugs. Standards have bugs. Every revision of every standard in the history of computing has shipped known defects alongside intended features.

The question is not whether WG21 makes mistakes. It does. The question is whether WG21 can fix them.

## 3. The Asymmetry

Adding a feature to the standard requires one paper, one set of favourable polls, and one revision cycle. Removing or replacing a feature requires deprecation, a migration path, Application Binary Interface (ABI) coordination across every major implementation, and the political will to tell users that the committee was wrong.

The process is structurally asymmetric. Bjarne Stroustrup recorded the observation in *The Design and Evolution of C++*<sup>[4]</sup>, Section 6.4:

> "It is much easier to accept a proposal than to reject it."

This asymmetry is not a flaw in the process. It is the process. The committee is designed to add. It is not designed to subtract. The result is a ratchet: Each cycle turns one direction.

**One direction.**

## 4. The Record

The committee has acknowledged mistakes it has not corrected.

| Component | Status | Duration | Outcome |
|-----------|--------|----------|---------|
| `std::auto_ptr` | Deprecated C++11, removed C++17 | 6 years | Complete removal |
| `std::random_shuffle` | Deprecated C++14, removed C++17 | 3 years | Complete removal |
| `std::regex` | Standardised C++11 | 15 years | No replacement proposed |
| Networking TS | First proposed 2006<sup>[5]</sup> | 20 years | No standard networking shipped |
| `volatile` compound ops | Deprecated C++20<sup>[6]</sup> | 6 years | No removal proposed |

`std::auto_ptr` and `std::random_shuffle` were removed together in [N4190](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4190.htm)<sup>[7]</sup>. Both removals happened in a single paper, in a single cycle, for components whose replacements had shipped in C++11 and C++14 respectively. This is the committee's complete track record of removal: two components, one paper, one cycle, under conditions of near-zero migration cost.

`std::regex` was standardised in C++11. Its performance characteristics are widely understood to be unacceptable for production use. Fifteen years later, the interface is unchanged. No replacement has been proposed. No fix has been applied.

The Networking TS was first proposed for TR2 in 2006<sup>[5]</sup>. Twenty years later, C++ has no standard networking. The committee could not ship it. The committee could not cancel it. The committee could not replace it. The proposal exists in a state that is none of these.

`volatile` compound assignment and increment/decrement were deprecated in C++20 via [P1152R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1152r4.html)<sup>[6]</sup>. Six years later, the deprecation stands. No removal has been proposed.

The pattern: The committee can add. The committee can deprecate. The committee has completed two removals in its history, both in the same paper, both under ideal conditions.

**Two removals. One paper. Thirty years.**

## 5. The Consequence

Stroustrup recorded the constraint directly in *The Design and Evolution of C++*<sup>[4]</sup>, Chapter 4:

> "Often, it is not feasible to eliminate a feature or correct a mistake."

If the ratchet turns only one direction, the standard accumulates mistakes at the rate they are made minus the rate they are corrected. The rate of addition is measured in dozens of features per cycle. The rate of correction is measured in two removals across the committee's entire history.

Each cycle, the surface area grows. Each cycle, the ratio of known mistakes to total surface area either holds steady or increases. No mechanism in the current process reverses this. Deprecation is not reversal. Deprecation is a label. The feature remains. The ABI remains. The teaching burden remains. The interaction surface with every future feature remains.

**Deprecation without removal is a warning label on a load-bearing wall.**

## 6. The Test

This paper makes one claim: WG21 must demonstrate, concretely, that it can fix at least one significant mistake. Not deprecate. Fix. Remove, replace, or correct.

The specific mistake does not matter. The capability matters.

An organisation that has never reversed a significant decision has no evidence that it can. It is an observation about what the institution has demonstrated.

**Capacity that has never been exercised is indistinguishable from capacity that does not exist.**

## 7. The Cost of Waiting

ABI makes every unfixed mistake permanent on a timeline the committee does not control. Implementations ship. Users compile against shipped interfaces. The cost of correction increases monotonically with time.

Each standard that ships without a correction raises the cost of the next correction. The window does not stay open. It narrows. An organisation that defers correction indefinitely is an organisation that has chosen, by inaction, never to correct.

The committee has demonstrated that it can build. The question is whether it can also repair. The answer is not yet in evidence.

## References

[1] [P4003R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r0.pdf) - "Coroutines for I/O" (Vinnie Falco, 2026).

[2] [P4007R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4007r0.pdf) - "Senders and Coroutines" (Vinnie Falco, 2026).

[3] [P4100R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4100r0.pdf) - "The Network Endeavor" (Vinnie Falco, 2026).

[4] Bjarne Stroustrup - *The Design and Evolution of C++* (Addison-Wesley, 1994).

[5] [N2054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2006/n2054.pdf) - "Networking Library Proposal for TR2" (Christopher Kohlhoff, 2006).

[6] [P1152R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1152r4.html) - "Deprecating volatile" (JF Bastien, 2019).

[7] [N4190](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4190.htm) - "Removing auto_ptr, random_shuffle(), And Old <functional> Stuff" (Stephan T. Lavavej, 2014).
