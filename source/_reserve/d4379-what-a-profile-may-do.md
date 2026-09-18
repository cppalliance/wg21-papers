---
title: "Does a Profile Need to Define Behavior? A Scope Rule for Profiles and Undefined Behavior"
document: D4379R0
date: 2026-09-18
intent: ask
audience: SG23, EWG
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper proposes a three-clause rule for profiles and core-language undefined behavior: a profile may reject a program, may terminate it at undefined behavior a runtime check detects, and never selects a defined continuation.

The published profiles papers disagree on whether a profile may give undefined behavior a meaning: one grants a profile authority to give signed overflow a defined result, while others hold that any defined replacement is a change to the base language that cannot be gated on a switch. Scoring every response a profile could give to undefined behavior against criteria drawn from those papers shows that selecting a value fails four of them - it gives a construct a defined result it did not have, gates that result on the active profile, breaks code copied out from under the profile, and lets two profiles conflict on one construct - while rejection and termination fail none, because termination produces no result a program can depend on. The cost is the wrap and saturate profiles, which C++26 already supplies as `std::add_sat` and unsigned arithmetic with the meaning stated in the source. Under the rule no profile creates a dialect in any form of the question, and SG23 is asked to adopt the rule as guidance for profile papers in two polls that separate the uncontested clauses from the contested one.

---

## Revision History

### R0: September 2026

- Initial version.

---

## Introduction

This paper proposes a three-clause scope rule for what a profile may do about undefined behavior, and shows that under the rule no profile creates a dialect of C++.

1. A profile may reject a program: it may make ill-formed a program that is well-formed without it.
2. A profile may terminate a program: at an instance of undefined behavior that a runtime check detects, it may specify that execution ends.
3. A profile never selects: it does not choose among defined continuations for behavior the base language leaves undefined, unspecified, or implementation-defined. Where a program wants a particular continuation, the source states it.

The rule covers profiles and core-language undefined behavior, and extends to erroneous behavior where Section 4 says so. Contract assertions, their evaluation semantics, and the contract-violation handler are a separate facility and are out of scope; nothing here changes them or depends on them.

### Related work

P3589R3<sup>[1]</sup> defines the profiles framework, including the transparency rule that a profile does not change the meaning of a well-formed program with no undefined behavior, and the rule that a profile's static effects apply as-if after translation phase 7. P4314R0<sup>[2]</sup> enumerates five tools a profile employs, defines "dialect" in its glossary, and holds that any behavior a profile defines for erroneous or undefined behavior is a change to the base language rather than an effect of activation. P3984R0<sup>[3]</sup> states the subset-of-a-superset technique and grants a profile authority to define the meaning of undefined behavior, naming signed overflow as its example. P3100R8<sup>[4]</sup> classifies core-language undefined behavior, proposes erroneous behavior for the cases with a replacement value, and states that refined behavior must be unconditional to avoid dialects. P4317R1<sup>[5]</sup>, by this author, specifies a profile over the runtime-checkable core-language cases and adopts defined replacement values for 15 of them; the rule here is stricter than P4317R1, and Section 8 announces the revision that brings that paper into line.

### Contributions

1. A scored option space for what a profile could do at an instance of undefined behavior, evaluated against criteria drawn from P3589R3, P4314R0, and P3100R8.
2. The three-clause rule as the option that survives every criterion.
3. A point-by-point answer to the dialect question in each of its forms, including a set-theoretic form.
4. A proposed replacement paragraph for P4314R0's fifth tool.
5. A statement of what the rule forbids that current papers permit, and the revision to P4317R1 that follows.

### Assumptions

The framework in P3589R3 is the baseline: profiles are activated per translation unit, their static effects apply after phase 7, and standard profiles compose. The word "dialect" is taken in the sense P4314R0's glossary gives it, sharpened in Section 2. The standard's vocabulary is N5054.<sup>[6]</sup>

## 1. The dialect question has four forms

This section collects the forms in which the question "do profiles create dialects?" has been put, so that Section 5 can answer each one. Two forms are on the public record, in a glossary and on a conference floor; two are stated here, as a portability argument and as a set-theoretic formulation.

The first form is definitional. P4314R0's glossary reads: "Dialect - A language that is not strictly a subset of the base language, typically by redefining the meaning of a well-defined construct."<sup>[2]</sup> The same paper's fifth tool draws a consequence: "If a profile proposes to define behavior for an erroneous or undefined behavior, that change in behavior is not contingent on the profile being active. It is a proposed change to the base language. Two profiles proposing to change the meaning of an erroneous or undefined behavior in incompatible ways conflict and cannot be merged into the standard without prior resolution."<sup>[2]</sup> Under this form, the question is whether a profile that gives undefined behavior a meaning has redefined a construct.

The second form is the forking argument, put to Bjarne Stroustrup from the floor at CppCon 2026 by John Lakos.<sup>[7]</sup> The scenario has two guarantees and a later standard: "How about two profiles defining integer overflow? ... we have wraparound which is what we do now by default. And then there's this other one called saturation which is incredibly useful but they can't both exist at the same time. So one company goes saturation the other company goes wraparound. Okay. And then the standard finally decides it's going to be wraparound, defined, done, end of story. Now what?" The consequence named is copyability: "how are we going to deal with the automatic forking that goes on when you redefine undefined behavior as an actual guarantee and then somebody copy paste it out from under whatever profile is governing and now it's a bug." The question closed with an offer: "I want to work with you as engineers using a principle." Stroustrup deferred: "I haven't worked out the details of overflow ... With a bit of luck I'll have a good answer next year."<sup>[7]</sup> Section 4 states a principle.

The third form is portability, stated here. A profile is a per-translation-unit choice, and a compiler that does not implement profiles compiles the same source. If a profile gave a construct a meaning, code written against that meaning would depend on the profile, and the dependence would be invisible on a compiler without it. Under this form, the question is whether code that is correct under a profile stays correct when the profile is absent.

The fourth form is set-theoretic, stated here. Take a well-formed program and let S be the set of behaviors the standard permits for it. Let profiles P1 and P2, applied separately, restrict S to S1 and S2. The questions are: must S1 and S2 be the same set; may they differ; may neither be a subset of the other; may they be disjoint and non-empty; does the answer depend on whether S was bounded (no undefined behavior) or unbounded (undefined behavior present); and what is the permitted set when P1 and P2 are both active. Under this form, a dialect exists when two profiles can each yield a result the other excludes.

The four forms are one question: can a profile give a construct a result that another profile, a build without the profile, or a later standard could contradict.

## 2. Definitions fix what a dialect would require

This section fixes the vocabulary the rule is stated in, using the standard's own definitions and P4314R0's glossary, so that the rule can be checked against them rather than against intuition.

Undefined behavior is "behavior for which this document imposes no requirements" (N5054 [defns.undefined]).<sup>[6]</sup> The accompanying note gives the range: "Permissible undefined behavior ranges from ignoring the situation completely with unpredictable results, to behaving during translation or program execution in a documented manner characteristic of the environment ... to terminating a translation or execution (with the issuance of a diagnostic message)." Termination is inside that range, and so is wraparound; an implementation that does either at an instance of undefined behavior is conforming today. The difference between them is not conformance but dependence: a program can depend on wraparound for a result, and no program can depend on termination for one.

Erroneous behavior is "well-defined behavior that the implementation is recommended to diagnose" ([defns.erroneous]).<sup>[6]</sup> Unspecified behavior and implementation-defined behavior are behavior "for a well-formed program construct and correct data, that depends on the implementation", the latter documented ([defns.unspecified], [defns.impl.defined]).<sup>[6]</sup> A well-formed program is one "constructed according to the syntax and semantic rules" ([defns.well.formed]).<sup>[6]</sup>

The standard assigns a program a set of behaviors, not one behavior. [intro.abstract]/3 reads: "Where possible, this document defines a set of allowable behaviors. These define the nondeterministic aspects of the abstract machine. An instance of the abstract machine can thus have more than one possible execution for a given program and a given input."<sup>[6]</sup> [intro.abstract]/6 adds that if an execution "contains an undefined operation, the implementation executing that program with that input may produce arbitrary additional observable behavior afterwards", and that where an operation has erroneous behavior "the implementation is permitted to issue a diagnostic and is permitted to terminate the execution of the program."<sup>[6]</sup> For a program with undefined behavior, the permitted set S is unbounded. The framework's author put the same point on the SG23 reflector: "The C++ standards assign a set of permitted behaviors to a well-formed input source file. In general, that set is not a singleton. ... A profile is intended to restrict further that set of permitted behaviors that non-profile enabled semantics would be associated with."<sup>[8]</sup>

P3589R3 gives the two framework rules Sections 3 through 5 rely on. Transparency: a profile's rules "are not to change the meaning (i.e. set of permitted observable behaviors) of a well-formed program with no undefined behavior."<sup>[1]</sup> Phase 7: "A profile may have an effect on the runtime behavior of a program such as enabling runtime instrumentation (e.g. bound checking in array indexing). However, its static semantic effects are as-if applied only after translation phase 7. It is not possible for a profile to change the outcome of overload resolution or template instantiation, nor is it possible to "SFINAE out" failure of a program to satisfy a profile requirement."<sup>[1]</sup> On the reflector the author restated the static half: profile rules "don't retroactively make a program well-formed when it would have been ill-formed without profiles. They can reject programs that [are] well-formed under C++-sans-profiles."<sup>[9]</sup>

P4314R0 states the principle behind its glossary entry: "Profiles cannot change the meaning of anything that is currently well-defined."<sup>[2]</sup> P3100R8, writing about the base language, states the same principle in its discussion of refined behavior: "To avoid creating language dialects, refined behaviour needs to be unconditional. ... We also cannot have two different language dialects where the same expression means two different things (overflow or wraparound)."<sup>[4]</sup>

The glossary's literal condition, redefining a well-defined construct, is not met by any profile that acts only where behavior is undefined, whether the profile traps or wraps; neither redefines anything well-defined. The condition P3100R8 states is stricter and is the one adopted here: a dialect exists when two translations of the same source give the same construct different defined results. Under that condition, undefined behavior has no result to redefine, and termination selects none.

## 3. Six responses to undefined behavior, scored against six criteria

This section enumerates every response a profile could give at an instance of undefined behavior and scores each against criteria drawn from the papers in Section 2. Each disagreement with the rule in Section 4 maps to one cell of Table 1.

The responses partition what a translation can do when a construct's behavior is undefined and a profile is active. Statically, the translation can accept or reject the program. At runtime, on reaching the construct, it can do nothing, stop, continue with a defined result, continue with an unspecified flagged result, or continue through a hook. That gives six responses:

- R1 Leave it undefined. The profile says nothing; S stays unbounded.
- R2 Reject. The profile makes the program ill-formed when it can decide statically that the construct is reached.
- R3 Terminate. The profile inserts a runtime check and specifies that execution ends when the check fails: a trap, a diagnostic followed by `abort()`, or a handler that does not return by any path.
- R4 Continue with a defined result. The profile specifies wraparound, saturation, zero, or a thrown exception.
- R5 Continue with an erroneous value. The profile specifies that the operation yields an unspecified value and that the behavior is erroneous.
- R6 Continue through a handler. The profile inserts a runtime check, invokes a handler on failure, and execution proceeds past the construct.

The criteria, each with its source:

- C1 Transparency. Among the programs a profile accepts, a program with no undefined behavior has the same permitted set with and without the profile (P3589R3).<sup>[1]</sup> Rejection of programs with no undefined behavior is expected and is what "strictly a subset" means.
- C2 No new defined result. No construct acquires a defined result it lacks in the base language. This criterion is this paper's, derived in Section 2 from P3100R8's condition; a delegate who rejects it can score Table 1 on C3 through C6 alone, and the outcome is unchanged.
- C3 Unconditional refinement. A refined value, if introduced, is introduced for all programs, not under a switch (P3100R8 Section 4.3.2; P4314R0 tool 5).<sup>[4]</sup><sup>[2]</sup>
- C4 Removal safety. Removing the profile from a translation unit leaves a program whose correct behaviors are unchanged and introduces no dependence the source did not state (Section 1, forms two and three).
- C5 Composition. Two active profiles combine by intersection of permitted sets, ill-formed when the intersection is empty (P4314R0 tool 3; the framework author's statement on the SG23 reflector).<sup>[2]</sup><sup>[10]</sup>
- C6 Guarantee. The profile prevents execution from proceeding past the undefined operation (the stated aim of P3984R0: "insert run-time checks to ensure that an error action is triggered rather than reaching the point of UB").<sup>[3]</sup>

Table 1. Each response scored against each criterion. "Pass" means the criterion holds for every instance of undefined behavior; "fail" means a case exists where it does not; "n/a" means the criterion does not bear on the response. For C5, all terminating responses are treated as one element of the permitted set, for the reason given in Section 5.

| Response | C1 Transparency | C2 No new result | C3 Unconditional | C4 Removal safety | C5 Composition | C6 Guarantee |
|---|---|---|---|---|---|---|
| R1 Leave undefined | pass | pass | n/a | pass | pass | fail |
| R2 Reject | pass | pass | n/a | pass | pass | pass |
| R3 Terminate | pass | pass | n/a | pass | pass | pass |
| R4 Defined result | pass | fail | fail | fail | fail | pass |
| R5 Erroneous value | pass | fail | fail | fail | pass | fail |
| R6 Continue via handler | pass | pass | n/a | pass | pass | fail |

Every response passes C1, because every response acts only where the base language imposes no requirement; among accepted programs, one with no undefined behavior never reaches any of them. The columns that separate the rows are C2 through C6.

R4 fails C2 because the construct `a + b` on signed operands acquires a defined result it did not have. It fails C3 because the result depends on which profile is active. It fails C4 because code written against the result loses it when the profile is removed. It fails C5 because a wraparound profile and a saturation profile have an empty intersection on the same construct, and P4314R0 records this case: two profiles "proposing to change the meaning of an erroneous or undefined behavior in incompatible ways conflict".<sup>[2]</sup>

R5 fails C2 and C3 for the same reason as R4 with one qualification. The value is unspecified, so no program can depend on a particular result, but the program does continue with a result where it had none, and two builds can differ on whether they continue. It fails C4 because a program that relied on continuing past the construct stops relying on it when the profile is removed. It passes C5 because two erroneous-value profiles agree on the construct's status. It fails C6 because execution proceeds past the undefined operation. P3100R8 chose this response for the base language and did so unconditionally, for the reason its Section 4.3.2 gives; a profile that chose it conditionally would be the case that section rules out.

R6 fails C6 by construction. Continuation past the undefined operation is the property the response exists to provide. Whether that property is wanted for contract assertions is a question for the contracts facility and is out of scope here; for core-language undefined behavior it is the property the guarantee excludes.

R1 fails only C6, and R2 and R3 fail nothing. Every response that survives the criteria either removes a program or removes a continuation; none adds a result.

## 4. The rule: reject, terminate, never select

This section states the rule as the survivor of Table 1, gives one example per clause, and shows where each clause sits inside the framework already published.

### Clause 1: a profile may reject

A profile may make a program ill-formed. Its static effect is as-if applied after translation phase 7, so it can only remove programs from the well-formed set; it cannot add any (P3589R3).<sup>[1]</sup> This is P4314R0's second tool, "Features removed from the language or library are removed only when the profile is active",<sup>[2]</sup> generalized from features to any statically decidable violation of the profile's guarantee. Rejection does not require that the construct have undefined behavior; a profile may reject a well-formed, well-defined construct its guarantee excludes, and that is the ordinary subsetting P3984R0 describes.<sup>[3]</sup>

```cpp
// status: hypothetical profile, illustrative syntax
[[profiles::enforce(pointers)]];
int f() {
    int* p = nullptr;
    return *p;      // ill-formed under the profile: the dereference of a
                    // null pointer is decidable statically on every path
}
```

### Clause 2: a profile may terminate

At an instance of undefined behavior that a runtime check detects, a profile may specify that execution ends. The response is one of trap, diagnostic then `abort()`, or a handler that does not return by any path, including by exception or `longjmp`; these are the three candidates P4317R1 Section 3 lists, all of which terminate.<sup>[5]</sup> A terminating execution is one the base language already permits at an undefined operation,<sup>[6]</sup> so a build with the profile and a build without it are both conforming executions of the same program. The profile narrows the set S from unbounded to a single element at that point; it adds nothing to S, and it produces no result a program can depend on. The same clause applies to erroneous behavior: [intro.abstract]/6 already permits an implementation to terminate there,<sup>[6]</sup> so a profile that terminates at an erroneous operation selects an execution the base language allows.

```cpp
// status: hypothetical profile, illustrative syntax
[[profiles::enforce(bounds)]];
int g(int (&a)[8], std::size_t i) {
    return a[i];    // under the profile: if i >= 8, execution ends;
                    // without the profile: undefined behavior, as today
}
```

### Clause 3: a profile never selects

A profile does not choose among defined continuations for behavior the base language leaves undefined, unspecified, or implementation-defined. Where a program wants a particular continuation, the source states it, and the meaning is in the source.

```cpp
// status: existing C++26 library, [numerics.sat.func]
int h(int a, int b) {
    return std::add_sat(a, b);   // saturates on every compiler, under
                                 // every profile, and under none
}
int k(unsigned a, unsigned b) {
    return static_cast<int>(a + b);  // wraps, by the base language
}
```

The clause is the separation of mechanism from policy applied to profiles. What a construct computes is the source's meaning; a profile is a mechanism that removes programs or removes continuations, and it does not move a semantic decision out of the code and into a build switch. P3100R8 states the corresponding rule for the base language: a refined value is introduced unconditionally or not at all.<sup>[4]</sup> Clause 3 is the profile-side counterpart. A profile introduces no refined value, so there is nothing for it to introduce conditionally.

The clause reaches unspecified and implementation-defined behavior for one reason. A profile that fixed, say, left-to-right evaluation of function arguments would narrow the permitted set of a program with no undefined behavior, which P3589R3's transparency rule forbids;<sup>[1]</sup> a profile that selected a documented alternative for implementation-defined behavior would do the same. Table 1 scores responses to undefined behavior, and the extension rests on the transparency rule alone.

### Corollary: transparency follows

A profile does not change the meaning of any well-formed program it accepts that has no undefined behavior. This is P3589R3's transparency rule,<sup>[1]</sup> and it follows from the three clauses. Rejection and termination act only where the base language imposes no requirement, and clause 3 forbids the one action that could act elsewhere.

### The rule inside the framework

Each clause is already present in the published framework. Rejection is P3589R3's phase-7 rule and P4314R0's second tool. Termination is P3589R3's "runtime instrumentation",<sup>[1]</sup> with the response fixed. Clause 3 is P4314R0's principle that profiles cannot change well-defined meaning,<sup>[2]</sup> extended to say that a profile also does not give a well-defined result to what is currently undefined. The one published grant the rule narrows is P3984R0's, taken up in Section 8.

## 5. Each form of the question has the answer "no"

This section takes the four forms from Section 1 in turn and shows that under the rule each has the answer "no". The forms are answered in the order they were raised, with a note on inline functions at the end.

### The glossary test: strictly a subset

P4314R0's dialect is "a language that is not strictly a subset of the base language, typically by redefining the meaning of a well-defined construct."<sup>[2]</sup> Under the rule a profile removes programs (clause 1) and removes continuations (clause 2). The set of programs it accepts is a subset of the base language's; the set of behaviors it permits for each program is a subset of the base language's. No well-formed construct is redefined, because clause 3 forbids the profile from giving any construct a result. The language under the profile is strictly a subset of the base language.

The glossary's literal condition is also met by a wrapping profile, which is why the glossary form of the question does not by itself rule out value selection; Section 2's stricter condition and criteria C3 through C5 do. The point was made on the SG23 reflector for the terminating case: "UB is not well-defined. A profile that replaces UB with a trap is not redefining a well-defined construct. It is giving defined behavior to something that had none. The set of well-defined programs grows. No existing well-defined program changes meaning."<sup>[11]</sup> The stricter condition adds that the something it gives is termination, which is no result at all.

### The forking test: no consequence arises

The forking scenario from Section 1 has four consequences. Each is impossible under the rule.

Removing a profile cannot change the semantics of well-defined code. Under clause 1, removing the profile turns an ill-formed program into a well-formed one whose behavior is what it always was. Under clause 2, removing the profile turns a terminating execution back into the undefined behavior the base language already assigned. In neither case does any well-formed construct compute a different result; the only semantics that change are the ones the base language never defined.

Code copied out from under a profile cannot fail for want of the profile. Code that compiled under clause 1 contains no construct the profile rejects, so it compiles anywhere. Code that ran under clause 2 either never reached the undefined operation, in which case it behaves identically, or reached it and terminated, in which case it had a bug the profile exposed, and the base language's behavior for that bug is undefined as it always was. Under clause 3 the copied code's arithmetic meaning was in the source: `std::add_sat` saturates in every translation unit of every program.

Two profiles cannot choose incompatible resolutions. Under clause 3 no profile chooses a resolution, so there is nothing for two profiles to disagree about. A profile that terminates on overflow and a profile that terminates on out-of-bounds access compose by intersection: both checks are active, both terminate, and the intersection is non-empty. Two profiles that both terminate on overflow may differ in how (a trap against a diagnostic), and the next subsection says why that difference is not a dialect.

A later standard cannot strand a profile. If a future standard gives signed overflow a defined result, the construct no longer has undefined behavior, and clause 2's authority at that construct lapses with it: the profile's check is dropped, or, where the overflow is statically decidable, becomes a clause-1 rejection, which clause 1 always permits. No code written under the profile breaks, because no code depended on termination for a result. No profile chose wraparound or saturation, so no profile is stranded. Under the rule a later standard is unconstrained by any profile.

The reason the four consequences cannot arise is the same in every case. Undefined behavior carries no guarantee that a profile could break, and termination adds no guarantee that a later change could contradict.

### The portability test: correct with and without

A compiler without profiles compiles the same source. Under clause 1 that source contains none of the constructs the profile forbids, so it is the same program on both compilers. Under clause 2 the source has the same permitted set on both compilers up to the undefined operation, and past it the profile-less compiler's behavior is undefined, as the standard permits. There is no meaning the profile-aware build relied on that the other build lacks, because clause 3 forbade the profile from supplying one. Code that is correct under the profile is correct without it.

### The set-theoretic questions: no disjoint pair

Take a well-formed program with permitted set S, and profiles P1 and P2 yielding S1 and S2. For this analysis all terminating responses count as one element of S, because a trap, a diagnostic followed by `abort()`, and a non-returning handler differ in what the environment observes and agree in what the program observes: nothing, since no result is produced and no statement after the construct executes. The dialect condition in Section 2 concerns results the program computes, so that is the right granularity. The answers under the rule:

1. Must S1 and S2 be the same set? No. A bounds profile and an initialization profile restrict different constructs.
2. May S1 and S2 differ? Yes, by which constructs they reject or terminate on.
3. Is one required to be a subset of the other? No. Each is a subset of S; neither need be a subset of the other.
4. May S1 and S2 be disjoint and non-empty? No. For a construct with undefined behavior, each profile's contribution is either S (the profile says nothing), the single element "terminate" (clause 2), or rejection of the program (clause 1). Two profiles that both act at the construct both yield "terminate" or at least one rejects; two profiles of which one acts and one does not yield "terminate" and S, and "terminate" is in S. A disjoint non-empty pair would require two different selected results, which clause 3 forbids.
5. Does the answer depend on whether S was bounded? Yes. If the program has no undefined behavior, S is bounded and, by the corollary, either the program is rejected or S1 = S2 = S; a bounded S is never narrowed. If the program has undefined behavior, S is unbounded and each profile may cut it to "terminate" or reject the program.
6. What if P1 and P2 are both active? The permitted set is the intersection of S1 and S2, and the program is ill-formed if the intersection is empty. This is the framework author's own answer on the SG23 reflector: "the set of permitted behaviors of the resulting program is the intersection of the sets that each profile would have independently given. If the intersection is nonempty you get a behavior from that intersection, otherwise, the program is ill-formed from the profiles perspective."<sup>[10]</sup> Under the rule the intersection is empty only when at least one profile rejects, and a rejected program has no behaviors to intersect.

The dialect condition in this form is a pair of results b1 in S1 only and b2 in S2 only for the same construct. Item 4 shows the pair cannot exist.

### Inline functions: a removal-safety consequence

Per-translation-unit choices interact with inline functions. [basic.def.odr]/16 requires that definitions of an inline function in different translation units "consist of the same sequence of tokens",<sup>[6]</sup> and an implementation picks one definition for the program. Under any per-unit choice, including a profile, the picked definition's behavior at an undefined operation is the behavior every unit gets. If one unit selected wraparound and the picked definition came from a unit that did not, code in the selecting unit that depended on the result would silently lose it; that is criterion C4 at the program level. Under clause 3 no unit selected a result, so no unit depended on one. Under clause 2 the picked definition either terminates or proceeds undefined, and no code in any unit depended on either; the status is that of per-unit sanitizer instrumentation today, which the framework author's description of a profile's runtime part invokes: "not unlike ubsan".<sup>[12]</sup> One consequence follows and is stated plainly: the clause-2 guarantee is program-wide only when every unit that defines a checked inline function enables the profile.

No form of the question has a "yes" answer under the rule.

## 6. The rule gives up the wrap profile and the saturate profile, and three smaller things

This section states what the rule forbids that current papers permit, what a programmer who wanted the forbidden thing gets instead, and the costs that remain after the substitution.

The rule forbids a profile from defining signed overflow as wraparound, as saturation, or as a thrown exception. P3984R0 permits all three: "signed arithmetic overflow is UB so a profile can define it to be wraparound like unsigned arithmetic (though I wouldn't do that), to be saturated arithmetic, or to throw an exception."<sup>[3]</sup> P4317R1 exercised the permission for 15 cases.<sup>[5]</sup> Under clause 3 none of the three is available; a profile that meets an overflow terminates or says nothing.

What the programmer gets instead is already in the standard. C++26 provides `std::add_sat`, `std::sub_sat`, `std::mul_sat`, and `std::div_sat` in [numerics.sat.func] and `std::saturate_cast` in [numerics.sat.cast], from P0543R3: "simple free functions for basic saturating operations on all signed and unsigned integer types."<sup>[13]</sup> Wraparound is unsigned arithmetic, well-defined since C. A program that wants saturation writes `std::add_sat(a, b)`; a program that wants wraparound writes the addition on unsigned operands. Both choices are visible at the construct, survive copying into any translation unit, and mean the same thing on every compiler.

What the programmer wanted from an overflow profile is the guarantee that the program does not continue past an overflow it did not ask for. That guarantee is clause 2. A terminating overflow profile provides it; a wrapping profile does not, because a wrapping profile continues. P3984R0 states the aim of a profile as triggering an error action "rather than reaching the point of UB",<sup>[3]</sup> and termination is the error action that reaches no further.

Three costs remain after the substitution, and each is a scoping decision rather than an oversight. First, a wrapping profile's value is to existing code without edits, which is why P3100R8 frames its discussion around `-fwrapv`;<sup>[4]</sup> `std::add_sat` requires the arithmetic to be rewritten, and under the rule existing code that relies on wraparound is made explicit or is left to the base language. Second, a terminate-only response excludes deployments that cannot end a process in production; under the rule such a deployment activates the profile in testing and continuous integration and does not activate it in the build it cannot afford to stop, which is the removal-safe choice clause 2 was designed to permit. Third, runtime checks have costs of their own, and for cases such as an uninitialized read the check requires instrumentation the size of a sanitizer's; where a check is too expensive, clause 1 rejection where decidable and R1 where not are the remaining options, and the rule leaves that choice to each profile.

The cost of the rule is two profiles that C++26 already provides as library calls, plus the three items above stated in the open; the benefit is a portable answer to the dialect question.

## 7. Expected objections

This section states the objections a delegate is likely to raise, each as a heading in its strongest form, and answers each from evidence already in the paper.

### "A wrapping profile and a trapping profile are both useful; a rule that forbids one of them is wrong."

Both are useful, and one of them is a dialect under the condition Section 2 adopts. Table 1 row R4 fails C2, C3, C4, and C5; the wrapping profile is the case P3100R8 Section 4.3.2 names when it says the same expression cannot mean "overflow or wraparound" in two dialects.<sup>[4]</sup> The trapping profile is row R3 and fails nothing. The rule keeps the useful response that creates no dialect and leaves the other to the source, where `std::add_sat` and unsigned arithmetic already provide it (Section 6).

### "Terminate is itself a selected behavior; the profile has chosen it over the others."

Termination and wraparound are both inside the range the standard names for undefined behavior, so conformance does not separate them (Section 2). What separates them is that no program can depend on termination for a result, because termination produces none. The dialect condition requires two translations computing different defined results for the same construct; a translation that terminates computes no result. Clause 2 narrows S; it does not extend it.

### "The rule forbids the initialization profile from reading an uninitialized variable as zero."

It does. Reading zero is a defined result (row R4) and fails C3 and C4: code that came to depend on the zero would lose it when the profile is removed. The initialization profile's guarantee is delivered by clause 1 where the read is decidable statically and by clause 2 where it is not, and Section 6 states the cost of the runtime check. A program that wants zero writes `= 0` or `{}`, and the meaning is in the source.

### "This is subsetting-only under another name."

Clause 2 is a runtime effect. A profile that inserts a bounds check and terminates on failure changes code generation and changes the executions the program can exhibit; a subsetting-only model, in which a profile is a compile-time pass/fail with no runtime part, excludes it. The rule keeps the runtime part P3589R3 names<sup>[1]</sup> and fixes its response.

### "A terminating profile check is a contract assertion with a restricted semantic, so profiles are a configuration of contracts."

The rule is stated so that it holds under either answer to that question. Whichever specification carries the check, the observable response under the rule is fixed: the program does not continue past the construct, and no result is produced. Which specification carries the check is a coupling question left open here; the rule constrains what the check does, wherever it is written down.

### "The paper quotes two participants from a members-only list and no one else."

Five quotations from that list are used. Four are the framework's author stating what the framework specifies; one is the terminating-case argument that Section 5 sharpens. The positions not quoted from that list are answered through their public forms: P4314R0's glossary and fifth tool, P3100R8's Section 4.3.2, and the CppCon 2026 exchange. Table 1 and the answers in Section 5 cite the published papers and the standard; the reflector quotations corroborate them.

Each objection either concedes a case the rule already handles or asks the profile to select a result.

## 8. The rule is consistent with the framework, amends one tool, and narrows one grant

This section checks the rule against the four published papers it touches and states the changes it implies. Two need no text change; one needs a paragraph; the author's own paper needs a revision.

### P3589R3: no change

The rule is expressible entirely in the framework's terms. Clause 1 is the phase-7 rule. Clause 2 is the runtime instrumentation the framework permits, with its response fixed to termination. Clause 3 is transparency extended from "no change to well-defined meaning" to "no new well-defined result". The framework's compatibility rule is declared rather than derived, "Two profiles are compatible if they are the same or proclaimed as such by the implementation. All standard profiles are compatible with each other",<sup>[1]</sup> and the rule makes the declaration easy to honor: standard profiles that never select results cannot conflict on a result.

### P4314R0: a replacement paragraph for tool 5

The fifth tool's logic is correct for value-selecting definitions: a defined replacement, if the committee wants one, is a base-language change and is not gated on activation. That is P3100R8's "refined behaviour needs to be unconditional" in P4314R0's vocabulary. What the tool does not yet say is that a profile's own response to undefined behavior is termination, and that termination is gated on activation like the second tool's removals. The proposed text:

> 5. A profile does not define a replacement result for erroneous, undefined, unspecified, or implementation-defined behavior. A paper that proposes such a result proposes a change to the base language, and the change is not contingent on any profile being active. A profile may specify that an instance of undefined or erroneous behavior detected by a runtime check terminates the program; that specification takes effect only when the profile is active, and two profiles that both specify termination at the same construct both terminate, so that the program has no result at that construct under either.

With this paragraph the "In short" section's third bullet, which says activation "has zero impact on ... any newly defined behavior",<sup>[2]</sup> stays true, because under the rule a profile defines no new behavior. The first bullet says an active profile means "the runtime checks it affects are restricted in their evaluation modes";<sup>[2]</sup> the termination clause is such a restriction, with the permitted executions at the construct narrowed to one.

### P3984R0: the grant is wider than its aim requires

P3984R0 provides three things the rule retains: the subset-of-a-superset technique, the transparency statement that "a program without UB will behave identically when compiled with or without a profile enforced",<sup>[3]</sup> and the aim of inserting "run-time checks to ensure that an error action is triggered rather than reaching the point of UB".<sup>[3]</sup> In the same paragraph as the aim it grants a profile authority to define overflow as wraparound, saturation, or a thrown exception. The aim is satisfied by termination alone. The grant's author added "(though I wouldn't do that)" to the wraparound option and, asked at CppCon 2026 how two overflow profiles avoid forking, answered that the details were not worked out.<sup>[7]</sup> The rule keeps the part of the grant the aim requires and leaves the rest to the source.

At CppCon 2026 Stroustrup also said: "I'm not a fan of erroneous behavior. It does a very good thing of removing UB but it leaves you with something that is implementation defined and can be a source of errors. ... I don't need erroneous behavior if you're using the initialization profile."<sup>[7]</sup> That remark concerns base-language erroneous behavior and the initialization profile; it is reported here because row R5 of Table 1 is the profile-side analogue and fails the criteria R4 fails. The consequence drawn here is the author's own.

### P4317R1: revision announced

P4317R1 Section 2 states that for 15 cases "the profile defines the meaning directly, fixed for every conforming implementation ... Signed overflow is wraparound, out-of-range conversion is erroneous value",<sup>[5]</sup> while its Appendix A.4 lists signed overflow as "Coerce to erroneous value".<sup>[5]</sup> The two statements disagree with each other, and both are row R4 or R5 of Table 1. P4317R2 will move all 15 cases to termination, with static rejection where a check is decidable at translation time. The profile then terminates on all 77 of the runtime-checkable cases it guards and defines no result. P4317R2 also closes the question P4310R1 left open for the defined-replacement class,<sup>[14]</sup> in the direction of termination.

The rule is stricter than the author's prior paper, and the prior paper changes to match.

## Conclusion

Three clauses settle what a profile may do about undefined behavior. A profile may reject a program. A profile may terminate a program at an instance of undefined behavior a check detects. A profile never selects among defined continuations for behavior the base language leaves undefined, unspecified, or implementation-defined; that choice stays in the source. Table 1 shows the three clauses are the only responses that pass every criterion the published papers supply, and Section 5 shows that under them the dialect question has the answer "no" in each of its four forms: no well-formed construct is redefined, no forking consequence can arise, no profile-dependent result travels with copied code, and no two profiles can yield disjoint non-empty behavior sets. A profile that only rejects or terminates is a restriction of C++, and a restriction is not a dialect.

If SG23 adopts the rule, C++ gains a portable answer to the question that has delayed the profiles discussion, a criterion against which every future profile paper can be checked in one table, and a P4314R1 fifth tool that is consistent with P3100R8's own anti-dialect principle. If it does not, each profile paper re-argues the dialect question from the start, and the forking scenario put at CppCon 2026 stays unanswered. What the rule gives up is stated in Section 6: two profiles that C++26 already supplies as `std::add_sat` and unsigned arithmetic, edits to existing code that relied on wraparound, and a terminate-only response in the builds that activate the profile.

The rule is falsifiable. It is wrong if there exists a case of core-language undefined behavior with exactly one reasonable defined continuation that termination cannot serve and that the source cannot state. The author has not found one among the 80 cases enumerated in P3100R8 Appendix A;<sup>[4]</sup> a delegate who finds one names the case, and the rule gains a fourth clause or loses.

Who builds next: authors of profile papers, who check their runtime responses against Table 1; the author of P4314R0, who is offered the paragraph in Section 8; and this author, who revises P4317R1.

### Proposed polls

The two polls separate the clauses that the published framework already contains from the clause that narrows a published grant, so that a delegate who accepts the first and rejects the second has a vote to cast.

> Poll 1. SG23 adopts the following as guidance for profile papers: a profile may make a program ill-formed, and a profile may specify that an instance of undefined or erroneous behavior detected by a runtime check terminates the program.

> Poll 2. SG23 adopts the following as guidance for profile papers: a profile does not define a replacement result for undefined, erroneous, unspecified, or implementation-defined behavior.

### Summary for forwarding

> D4379R0 proposes a three-clause scope rule for profiles and undefined behavior: reject, terminate, never select a result. It scores six possible responses against criteria taken from P3589R3, P4314R0, and P3100R8 and shows the three clauses are the only responses that pass every criterion. Under the rule no profile creates a dialect in any of the four forms the question has taken, including a set-theoretic form. The cost is the wrap and saturate profiles, which C++26 already provides as library calls. The paper offers replacement text for P4314R0's fifth tool, two polls, and announces P4317R2, which moves that profile's 15 defined-replacement cases to termination.

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author is president of the C++ Alliance and maintains coroutine-native I/O libraries under it.

This paper asks SG23 to adopt the rule in Section 4 as guidance for profile papers, in the two polls stated in the Conclusion, and to consider the replacement paragraph in Section 8 for P4314R1.

The author is the author of P4317R1, which this paper finds inconsistent with the rule and announces a revision to; a co-author of P4310R1,<sup>[14]</sup> which left open the question this paper closes; and a co-author of P4238R0,<sup>[15]</sup> which asks the National Bodies to return the C++26 draft over Contracts. Each is a stake in how the profiles and contracts facilities are related, and this paper's rule is stated so that it holds under either answer to that question (Section 7).

One limitation bounds the method. The rule is derived from the standard's definitions and from published papers, not from deployment experience with a profile that follows it; the terminating responses in Section 4 have shipping precedent in library hardening and bounds-safety tooling, but no shipping profile has yet been specified under this rule.

This paper is one of a series with P4297R1,<sup>[16]</sup> P4306R1,<sup>[17]</sup> P4308R1,<sup>[18]</sup> P4310R1, P4317R1, and P4318R1<sup>[19]</sup> on the relation between profiles and implicit contract assertions.

Quotations from the CppCon 2026 session are taken from the published recording's caption track; the author will confirm each against the audio before this paper is mailed, and the timestamp is approximate. Five quotations are taken from the SG23 reflector, four from the framework's author and one from this author; Table 1 and Section 5 do not depend on them.

This paper was prepared with the assistance of generative tools. The author is responsible for its content.

## References

[1] [P3589R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3589r3.pdf) - "C++ Profiles: The Framework" (Gabriel Dos Reis, 2025).

[2] [P4314R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4314r0.html) - "On activating a profile" (Peter Bindels, 2026).

[3] [P3984R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3984r0.pdf) - "A type-safety profile" (Bjarne Stroustrup, 2026).

[4] [P3100R8](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3100r8.pdf) - "A framework for systematically addressing undefined behaviour in the C++ Standard" (Timur Doumler, Joshua Berne, 2026).

[5] [P4317R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4317r1.pdf) - "A Profile for Runtime-Checkable Core-Language Undefined Behavior: std::core_ub" (Vinnie Falco, 2026).

[6] [N5054](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/n5054.pdf) - "Working Draft, Programming Languages - C++" (Thomas K&ouml;ppe, editor, 2026).

[7] [CppCon 2026 recording](https://www.youtube.com/watch?v=41USGJaGsAo) - "Profiles for Simplicity and Guarantees, audience question and answer at approximately 1:15:00" (Bjarne Stroustrup, John Lakos, 2026).

[8] SG23 reflector - "P4314R0 'On activating a profile': two items that create unnecessary coupling" (Gabriel Dos Reis, 2026-09-15, 9:55 AM).

[9] SG23 reflector - "P4314R0 'On activating a profile': two items that create unnecessary coupling" (Gabriel Dos Reis, 2026-09-15, 3:18 PM).

[10] SG23 reflector - "P4314R0 'On activating a profile': two items that create unnecessary coupling" (Gabriel Dos Reis, 2026-09-18, 7:01 AM).

[11] SG23 reflector - "P4314R0 'On activating a profile': two items that create unnecessary coupling" (Vinnie Falco, 2026-08-31, 7:33 PM).

[12] SG23 reflector - "P4314R0 'On activating a profile': two items that create unnecessary coupling" (Gabriel Dos Reis, 2026-09-16, 3:55 PM).

[13] [P0543R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p0543r3.html) - "Saturation arithmetic" (Jens Maurer, 2023).

[14] [P4310R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4310r1.pdf) - "Hasta la Vista, Undefined Behavior: Why std::core_ub Should Terminate by Default" (Vinnie Falco, Ville Voutilainen, 2026).

[15] [P4238R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4238r0.pdf) - "Returning C++26 for the Evaluation It Skipped" (Vinnie Falco, Ville Voutilainen, Jos&eacute; Daniel Garc&iacute;a S&aacute;nchez, John Spicer, 2026).

[16] [P4297R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4297r1.pdf) - "Severing P3100's Profiles Claim from Its Case-by-Case Review" (Vinnie Falco, 2026).

[17] [P4306R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4306r1.pdf) - "Configuring Runtime Checking: Profiles and Implicit Contract Assertions" (Vinnie Falco, 2026).

[18] [P4308R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4308r1.pdf) - "Eight Responses to a Throwing Implicit Contract Assertion" (Vinnie Falco, 2026).

[19] [P4318R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4318r1.pdf) - "Transient Benefit, Perpetual Cost: Implicit Core-Language Assertions" (Vinnie Falco, 2026).
