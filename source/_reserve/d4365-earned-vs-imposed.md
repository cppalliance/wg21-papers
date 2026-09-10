---
title: "Sixteen Million Users, One Hundred Delegates"
document: P4365R0
date: 2026-09-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "Harry Bott <haroldjbott@gmail.com>"
---

## Abstract

The committee adopts the marketplace's libraries and rejects the marketplace's designs.

Two observable models of library development coexist in C++. One produces libraries through marketplace competition: authors publish code, users adopt or abandon it, and quality is determined by survival. The other produces libraries through committee process: delegates evaluate proposals, vote, and the result ships with every conforming compiler. Economic theory makes specific predictions about the outcomes each model produces. This paper states six predictions derived from established economics, then examines real C++ libraries from both models to test those predictions.

The record is public. Section 4.12 states the condition that would falsify the last of the six.

---

## Revision History

### R0: September 2026

- Initial version.

---

## 1. Two Models

Two models of library development coexist in the C++ ecosystem. Both produce libraries. Both serve users. They differ in the mechanisms that connect authors to users, evaluate quality, and determine what survives.

### 1.1 Model A: Competitive Libraries

Model A libraries are developed in the open marketplace, such as Boost, GitHub, vcpkg, and Conan. The author publishes code, users evaluate it against alternatives, and adoption is the verdict.

| Property            | Model A                                  |
| ------------------- | ---------------------------------------- |
| Author's audience   | Users who can choose alternatives        |
| Adoption mechanism  | Earned through competition               |
| Feedback signal     | Users adopt, switch, or abandon          |
| Lifecycle           | Library improves or dies                 |
| Cost of entry       | Publish code                             |
| Cost of defect      | Users leave                              |
| Knowledge source    | Millions of users across all domains     |

### 1.2 Model B: Standardized Libraries

Model B libraries are developed through the WG21 process. The author writes a paper, delegates evaluate it in committee, and the result ships with every conforming compiler.

| Property            | Model B                                  |
| ------------------- | ---------------------------------------- |
| Author's audience   | Voting delegates                         |
| Adoption mechanism  | Shipped with the compiler                |
| Feedback signal     | Committee review, NB comments            |
| Lifecycle           | ABI-locked; effectively permanent        |
| Cost of entry       | Paper, attendance, years of process      |
| Cost of defect      | Workarounds proliferate; defect persists |
| Knowledge source    | ~100 delegates at plenary                |

### 1.3 What Model B Provides

Model B provides properties that Model A cannot. Portability is guaranteed across every conforming implementation: a `std::optional` on Linux is the same `std::optional` on Windows, on embedded systems, on every platform the compiler targets. Universal availability eliminates dependency management entirely, with no package manager, no build system integration, and no version conflicts. Vocabulary type coordination means the entire ecosystem agrees on what `optional`, `variant`, and `string_view` mean, enabling libraries from different authors to compose without adaptation layers. A single authoritative specification provides a reference that courts, contracts, and compliance regimes can cite. These are genuine, structurally important strengths. No marketplace library can replicate them.

### 1.4 Historical Context

The two models have not always been separate. In 1990, the committee's founding document stated the principle that would govern library standardization: "A key decision was that the Library working group was not in the business of designing new libraries. The key idea is that the Standard would be based on existing practice"<sup>[1]</sup>. In 1998, Beman Dawes founded [Boost](https://www.boost.org/)<sup>[2]</sup> to provide peer-reviewed libraries as candidates for standardization. The pipeline from Boost to the standard produced C++11, the standard's most celebrated release, with `shared_ptr`, `function`, `bind`, `regex`, `random`, and `thread` all tested through years of Boost deployment before entering the standard<sup>[2]</sup>. Boost.Filesystem took longer and arrived in C++17, and `chrono` came the other way: Howard Hinnant designed it for the committee in N2661, and Boost.Chrono followed three years later as a backport.

Bjarne Stroustrup observed in his HOPL paper that the committee considered adopting a commercial foundation library in 1992: "Texas Instruments offered their very nice library for consideration and within an hour five representatives of major corporations made it perfectly clear that if this offer was seriously considered they would propose their own corporate foundation libraries"<sup>[3]</sup>. The committee could not adopt one corporation's library over another. The marketplace, specifically Boost, solved the problem the committee could not.

Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz observed in 2024 that the relationship has changed: "the standards committee has taken on the role of innovator and is pushing the industry rather than adopting external advancements or coexisting with them"<sup>[4]</sup>.

---

## 2. Economic Foundations

The properties described in Section 1 are not unique to software. Economists have studied centralized allocation and competitive markets for centuries. The findings are settled, empirical, and reproduced across domains. This section presents seven results from the economic literature. Each describes an observable property of resource allocation systems. None mentions C++ or WG21.

### 2.1 The Knowledge Problem

Friedrich Hayek, in "The Use of Knowledge in Society" (1945)<sup>[5]</sup>, explains that no central authority can aggregate the distributed knowledge held by millions of individuals. Each participant holds local knowledge, about their own needs, constraints, and preferences, that is costly or impossible to communicate to a central planner. Markets solve this through price signals that encode the preferences of all participants into a single actionable number. The price aggregates information without requiring any single actor to hold all of it.

### 2.2 The Calculation Problem

Ludwig von Mises, in "Economic Calculation in the Socialist Commonwealth" (1920)<sup>[6]</sup> and *Bureaucracy* (1944)<sup>[7]</sup>, sets out that even if a central authority could gather dispersed knowledge, without a price signal it cannot calculate which allocation is optimal. Prices emerge from voluntary exchange and encode marginal utility across heterogeneous preferences. Without them, rational resource allocation at scale reduces to guesswork, however well-intentioned the allocators.

In *Bureaucracy*, Mises distinguishes two management systems. Profit management measures success by an outcome metric, profit or loss, that is external, quantitative, and self-correcting. Bureaucratic management has no equivalent metric. Success is measured by compliance with rules and procedures, because the outcome that the organization exists to produce cannot be priced. The distinction is structural, not a judgment of the people involved.

### 2.3 Creative Destruction

Joseph Schumpeter, in *Capitalism, Socialism and Democracy* (1942)<sup>[8]</sup>, describes that in competitive markets, inferior products are displaced by superior ones. Schumpeter called this process creative destruction: the mechanism through which quality improves over time. New entrants challenge incumbents. Users migrate to the better product. The inferior product loses its user base and either improves or disappears. Where competition is absent or where incumbents are protected from displacement, inferior products persist.

### 2.4 Collective Action

Mancur Olson, in *The Logic of Collective Action* (1965)<sup>[9]</sup>, explains that small, concentrated groups with strong per-member incentives outperform large, diffuse groups in influencing institutional outcomes, even when the diffuse group's aggregate interest is greater. A firm with three delegates in a standards body has concentrated incentives: the delegates attend every meeting, track every paper, and coordinate their positions. The sixteen million developers who use C++<sup>[10]</sup> have diffuse incentives: no individual developer's stake justifies the cost of participation.

### 2.5 Regulatory Capture

George Stigler, in "The Theory of Economic Regulation" (1971)<sup>[11]</sup>, observes that regulatory bodies tend, over time, to serve the interests of the entities with the most representation, rather than the broader public the body was created to serve. The entities that participate most actively in the regulatory process, attending hearings, filing comments, and building relationships with regulators, shape the body's output. The broader public, whose interests the body nominally serves, participates less and shapes the output less.

### 2.6 Public Choice

James Buchanan and Gordon Tullock, in *The Calculus of Consent* (1962)<sup>[12]</sup>, note that actors in institutional settings respond to the incentive structures of those institutions, not to abstract public interest. The quality of institutional outcomes depends on the feedback mechanism that connects decisions to consequences. In markets, a bad decision produces a loss. In committees, the feedback mechanism is different: a bad decision produces a paper trail. The distance between the decision and its consequences determines how quickly errors are corrected.

### 2.7 Self-Interest and Quality

Adam Smith, *The Wealth of Nations* (1776)<sup>[13]</sup>: "It is not from the benevolence of the butcher, the brewer, or the baker that we expect our dinner, but from their regard to their own interest." When self-interest is channeled through competition, the result is quality. The butcher who sells bad meat loses customers to the butcher across the street. When competition is absent, self-interest produces different outcomes. The insight is not that people are selfish; it is that the mechanism, competition or its absence, determines whether self-interest serves the public.

### 2.8 Summary

| Concept              | Observable Property                                         | Mechanism                       |
| -------------------- | ----------------------------------------------------------- | ------------------------------- |
| Knowledge problem    | Centralized allocators miss distributed needs               | Information loss                |
| Calculation problem  | Without price signals, allocation reduces to guesswork      | Absence of outcome metric       |
| Creative destruction | Inferior products displaced in competitive markets          | User choice                     |
| Collective action    | Concentrated interests outperform diffuse interests         | Per-member incentive asymmetry  |
| Regulatory capture   | Regulatory output reflects regulated entities               | Representation asymmetry        |
| Public choice        | Outcome quality tracks feedback mechanism quality           | Decision-consequence coupling   |
| Self-interest        | Competition channels self-interest toward quality           | Rivalry for adoption            |

---

## 3. Predictions

If the economic findings in Section 2 apply to software library development, then the two models described in Section 1 should produce different observable outcomes. This section derives six predictions. Each states what we should expect to observe under Model A and Model B. The predictions are numbered for reference.

**Prediction 1** (Hayek): Libraries developed under Model A should more accurately reflect the needs of the broader user community than libraries developed under Model B, because Model A aggregates information from a larger population through adoption signals.

**Prediction 2** (Mises): Model B's evaluation process should substitute procedural compliance for outcome measurement, because the outcome metric - user adoption - is structurally unavailable to the evaluators. Model A's evaluation should be dominated by outcomes.

**Prediction 3** (Schumpeter): Under Model A, libraries with significant quality defects should be superseded by better alternatives. Under Model B, libraries with significant quality defects should persist indefinitely.

**Prediction 4** (Olson): Under Model B, proposals backed by concentrated organizational resources should advance faster than proposals backed by diffuse community effort, independent of technical maturity.

**Prediction 5** (Buchanan and Tullock): Model A's feedback mechanism - users choosing alternatives - should produce faster quality iteration than Model B's feedback mechanism - committee review on multi-year cycles.

**Prediction 6** (Stigler): Decisions that bind every user of the standard library should be made by the participants rather than by the users, and the deciding body should be small. Where a deployed Model A design and a Model B design are both live and the committee must choose between them, it should choose its own. Correction, where it comes at all, should come only retrospectively, after deployment has settled the question the room could not.

---

## 4. Observations

This section collects data from the C++ ecosystem and examines each prediction against the public record. The data sources are WG21 papers, committee meeting minutes, Boost mailing list archives, published benchmarks, and public statements by committee participants. Every quotation is attributed with date and source.

### 4.1 Observation 1

Prediction 1 stated that Model A libraries should more accurately reflect the needs of the broader user community than Model B libraries.

Christopher Kohlhoff is an individual developer with no corporate sponsor. He wrote Boost.Asio and has maintained it for over twenty years. The library has millions of deployed users across every major platform. It formed the basis of the Networking TS<sup>[14]</sup>. The Networking TS has not been standardized.

The Graph Library ([P3126R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3126r0.pdf))<sup>[15]</sup> was proposed for standardization in 2024. Section 10 of P3126R0 states: "There is no current use of the library." Section 11 states: "There is no current deployment experience." The proposal has since reached R4 and acquired a reference implementation, and it is targeted at C++29<sup>[16]</sup>. It has not been standardized on the strength of the original submission, which is the process working.

The C++ JSON ecosystem contains five competing libraries, each serving a different user need. The throughput figures below come from a benchmark repository maintained by Stephen Berry, the author of `glaze`<sup>[17]</sup>:

| Library       | Parse Throughput | Niche                     |
| ------------- | ---------------- | ------------------------- |
| simdjson      | ~1163 MB/s       | Maximum throughput (SIMD) |
| glaze         | ~1200 MB/s       | Compile-time reflection   |
| RapidJSON     | ~416 MB/s        | Low-level control         |
| Boost.JSON    | ~308 MB/s        | Modern, balanced          |
| nlohmann/json | ~81 MB/s         | Developer ergonomics      |

No committee designed this ecosystem. Five independent authors identified five different user needs and built five different libraries. Users choose among them based on their own requirements. The distributed knowledge of millions of users produced five specialized solutions. One committee-designed JSON library would serve one of those needs.

### 4.2 Observation 2

Prediction 1 stated that Model A should aggregate information from a larger population through adoption signals.

Victor Zverovich published the `{fmt}` library on GitHub in December 2012<sup>[18]</sup>. Over the six years and seven months that followed, the library won its users in open competition. In the week the committee adopted the design at Cologne in July 2019, `{fmt}` had 6,185 stars, 742 forks, and twenty-one releases<sup>[19]</sup>. It had been adopted by Meta (Folly), among other production codebases. The committee recognized the marketplace's verdict and standardized the design as `std::format` in C++20 ([P0645R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0645r10.html))<sup>[20]</sup> and `std::print` in C++23 ([P2093R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2093r14.html))<sup>[21]</sup>. Competition continued after standardization: the library now stands at 25,641 stars, 3,046 forks, and 436 contributors<sup>[18]</sup>.

The marketplace identified what C++ developers needed, and the committee adopted the marketplace's output. This is the founding principle working as designed: existing practice was standardized. The committee did not need to invent a formatting library. The marketplace delivered one, the community validated it through adoption, and the committee consolidated the result.

### 4.3 Observation 3

Prediction 2 stated that Model B's evaluation process should substitute procedural compliance for outcome measurement.

[P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2274r0.pdf)<sup>[22]</sup> (Aaron Ballman, 2020), a document describing WG21's procedures to WG14 members, states: "WG21 finds implementation experience with a proposal to be incredibly valuable but does not have any requirement on implementation experience to adopt a proposal."

The committee's own documentation confirms the absence of an outcome metric. A library can advance from LEWG to LWG to plenary to the International Standard without a single user outside the proposing organization.

Howard Hinnant, writing on the library reflector in July 2016<sup>[23]</sup>, described the metric that Model B lacks: "I should quit asking: 'Has it been implemented?' The correct question is: What has been the field experience? Is there positive feedback from anyone outside your immediate family or people who could have a perceived conflict of interest (such as employees of your company)?"

The library reflector is not public. These remarks are reproduced with permission in [P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf)<sup>[23]</sup>, a paper by one of the present authors, and that is the source used here and in Sections 4.5 and 4.9.

Hartmut Kaiser characterized the Boost volunteer review process on the Boost mailing list in 2017<sup>[24]</sup>: "Having the review process being volunteer-driven guarantees a) a real-world need for the library under review, b) fairness of the decision, c) a high quality of the review, d) direct interest in organizing the review by the review manager."

### 4.4 Observation 4

Prediction 2 stated that Model A's evaluation should be dominated by outcomes.

[N3370](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3370.html)<sup>[25]</sup> (Alisdair Meredith, "Call for Library Proposals," 2012) lists what WG21 asks of library proposers: design decisions, technical specifications, impact on the standard, interaction with other proposals, and proposed wording. A Boost formal review asks different questions: does the library compile on all supported platforms, does it have tests, is the documentation adequate, has anyone used it, would the reviewer use it, and does it meet a real-world need<sup>[2]</sup>.

| Evaluated Property          | Model A (Boost Review)    | Model B (WG21 Process)       |
| --------------------------- | ------------------------- | ---------------------------- |
| Has it been used?           | Required                  | Not required<sup>[22]</sup>  |
| Do independent users exist? | Expected                  | Not required<sup>[22]</sup>  |
| Does it compile everywhere? | Tested on CI              | Not required before LEWG     |
| Is the documentation good?  | Evaluated by reviewers    | Not a formal criterion       |
| Does it meet a real need?   | Central question          | Implicit in design rationale |
| Is the wording correct?     | Not applicable            | Central question             |

One rubric measures whether the library works for users. The other measures whether the paper is ready for the standard.

### 4.5 Observation 5

Prediction 3 stated that under Model A, defective libraries should be superseded by better alternatives, and under Model B, defective libraries should persist.

**`std::variant` and `boost::variant2`.** Howard Hinnant wrote on the library reflector in July 2016, before `std::variant` was standardized<sup>[23]</sup>: "It is now my understanding that we (the committee) have made significant design changes with respect to all existing variants in the field (most notably boost::variant). We /think/ these are good changes, and I /hope/ that we are right. We won't /know/ if these are good design changes until we have field experience." He continued: "I won't bother to go down the list of libraries where this strategy has failed us in the past."

`std::variant` was standardized in C++17 with a `valueless_by_exception` state - a condition in which the variant holds no valid value<sup>[26]</sup>. Peter Dimov wrote `boost::variant2` with a never-empty guarantee using double-buffering<sup>[27]</sup>. Niall Douglas wrote on the Boost mailing list in November 2023<sup>[28]</sup>: "the whole valueless by exception footgun was 100% avoidable, and Boost.Variant2 immediately eliminated that footgun." The defect persists in `std::variant`. The marketplace produced the fix. Section 4.12 records the ballot in which the committee declined it.

**`std::regex` and Boost.Regex.** Andrey Semashev wrote on the Boost mailing list in July 2021<sup>[29]</sup>: "my general impression was that all std::regex implementations were slow compared to Boost.Regex, which seems to be one of the fastest implementations." Phil Endecott reported that a simple pattern match taking two seconds with libstdc++ `std::regex` completed in negligible time with Boost.Regex<sup>[29]</sup>. `std::regex` remains in the standard, unchanged. Boost.Regex, Boost.Xpressive, CTRE, and RE2 are available as alternatives in the marketplace.

**`std::unordered_map` and `boost::unordered_map`.** After the Boost 1.80 rewrite by Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz, `boost::unordered_flat_map` outperforms `std::unordered_map` by approximately 3x for string keys and 2.9x for integer keys on GCC 12 (x64)<sup>[30]</sup>. The two are not the same kind of container, and the constraint that separates them is not ABI. `[unord.req.general]` requires that rehashing "does not invalidate pointers or references to elements," and the mandated bucket interface forces a chained implementation<sup>[31]</sup>. A container written today with no ABI history at all could not be `boost::unordered_flat_map`. The decision that foreclosed it was taken in [N1456](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2003/n1456.html)<sup>[32]</sup> in 2003, which considered open addressing, rejected it, and closed: "All further discussion will assume chaining."

**`std::error_code` and `boost::error_code`.** Niall Douglas wrote on the Boost mailing list in November 2023<sup>[28]</sup> that he prefers "`boost::error_code` over the fundamentally unsafe `std::error_code`." The mechanism he has stated elsewhere is identity by global address: `std::error_code` compares categories by pointer, and dynamic libraries may duplicate a category global while unloading a shared object may destroy one<sup>[33]</sup>. Boost.System has since added source-location capture and an opt-in category identifier that does not depend on an address. Note the provenance: `std::error_code` came from Boost.System, so this is a marketplace design that the marketplace went on to improve and the standard did not.

`std::variant`, `std::regex`, `std::unordered_map`, and `std::error_code` were standardized and remain in the standard. `boost::variant2`, Boost.Regex, `boost::unordered_flat_map`, and `boost::error_code` are available as alternatives in the marketplace.

Two of these four came from the marketplace to begin with. `std::regex` is Boost.Regex, carried into TR1 by John Maddock, who wrote both; the case-insensitive range defect that is the specification's best-known flaw was diagnosed in the Boost version first, after Boost's own review had passed it. `std::error_code` is Boost.System. The observation this section supports is therefore narrower than it first appears. It is not that committee-designed libraries decay while marketplace ones do not. It is that a library which cannot break compatibility keeps its defects, wherever the design came from, while one that can breaks compatibility and fixes them.

### 4.6 Observation 6

Prediction 3 stated that where competition is absent, inferior products persist.

`std::filesystem` was standardized in C++17 based on Boost.Filesystem, and the standard version has received no redesign since. It is not static. Roughly thirty LWG issues have been resolved against `[fs.*]` since publication, several applied retroactively as defect reports against C++17, including two on path decomposition<sup>[34]</sup><sup>[35]</sup>, and [P1164R1](https://open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1164r1.pdf)<sup>[36]</sup> was adopted carrying the author's own statement that it "should be a defect against C++17." What has not happened is structural change: no `path_view`, no asynchronous interface, no revision of the design itself.

Boost.Filesystem Version 4 was released afterward with breaking changes to improve the design<sup>[37]</sup>. Subsequent releases added `fdopendir`/`openat` support for resilience to concurrent filesystem modifications and storage preallocation in `copy_file` to reduce fragmentation on Linux, both in 1.85.0<sup>[37]</sup>. The marketplace version can change its shape. The standard version can only accumulate corrections.

Daniel Lemire documented `std::ranges` performance degradation in October 2025<sup>[38]</sup>. Trimming whitespace from strings using chained views (`drop_while`, `reverse`, `drop_while`, `reverse`) produced 70 instructions per string on GCC 15 versus 24 for a simple imperative loop. Engineers at a C++ company observed measurable performance degradation after switching to `std::ranges`. The simdjson project limited `std::ranges` support because it caused performance loss<sup>[38]</sup>. In the marketplace, developers choose the imperative alternative. In the standard, the design persists regardless of the performance evidence.

### 4.7 Observation 7

Prediction 4 stated that under Model B, proposals backed by concentrated organizational resources should advance faster than proposals backed by diffuse community effort.

Stackless coroutines reached the standard in C++20. Microsoft shipped an experimental implementation in its November 2013 compiler preview, five years before the committee approved the design<sup>[39]</sup>. That first implementation tracked the earlier future-based resumable-functions design of [N3722](https://open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3722.pdf)<sup>[40]</sup>; the stackless design that became C++20 was proposed by Gor Nishanov in [N4134](https://isocpp.org/files/papers/N4134.pdf)<sup>[41]</sup> in October 2014 and shipped under MSVC's `/await` switch in 2015<sup>[39]</sup>.

Stackful coroutines were proposed by Oliver Kowalke and Nat Goodspeed, community developers without comparable corporate backing. Boost.Context shipped in Boost 1.51 in August 2012. P0876R22 has reached twenty-two revisions and is not in the C++26 working draft.

The two were never set against each other. [P0099R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0099r0.pdf)<sup>[42]</sup>, by Kowalke and Goodspeed themselves, records that at Urbana in 2014 "the members of the committee concluded that stackless and stackful coroutines have distinct use cases and decided to pursue both technologies." Nishanov agreed in [P1520R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1520r0.pdf)<sup>[43]</sup>: "There is no conflict between stackful and stackless." Nor was stackful ever voted down. It was voted up, in SG1 at Kona in 2019, in EWG-I at Belfast, in EWG at Prague, and in LEWG at Issaquah in 2023<sup>[44]</sup>.

Both models are well-understood. Both have multiple implementations. Both serve real use cases. Both were endorsed. One shipped in 2020, and the other has no vehicle after twenty-two revisions.

One qualification belongs here. [P0991R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0991r0.html)<sup>[45]</sup> catalogues twelve distinct stackful proposals between 2013 and 2018, which is a competing explanation for the delay. A proposal that keeps changing shape is harder to advance than one that does not. What the record does not contain is a decision against stackful coroutines. It contains a decision for both, followed by one of them moving.

### 4.8 Observation 8

Prediction 4 stated that concentrated organizational resources should predict advancement speed independent of technical maturity.

[P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[46]</sup> (Kohlhoff, Allsop, Falco, Hodges, Morgenstern, October 2021) states: "The asynchronous model of Asio/Net.TS has evolved to support new use cases while also being careful not to leave existing use cases behind, and the strength of the composition model is testament to that. The model is the result of growth and adaptation from use in the real world, and is one reason it is so widely deployed."

The Networking TS was based on Boost.Asio, the most deployed asynchronous library in C++, with decades of field experience, multiple continuation styles (callbacks, futures, coroutines, fibers, deferred, detached), and production deployment at many companies<sup>[46]</sup>. `std::execution` ([P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html))<sup>[47]</sup> was authored primarily by delegates from NVIDIA, Meta, and other major corporations with significant committee presence.

The two designs were heard together. On 4 October 2021 a joint Library Evolution and Concurrency telecon took P2300R2 alongside [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[48]</sup>, "Ruminations on networking and executors," and P2469R0, championed by Kohlhoff himself. Polls followed on the library evolution reflector<sup>[49]</sup>. The Asio model as a basis for most asynchronous use cases drew weak consensus against, on 53 votes. The sender/receiver model as the same basis drew consensus in favor, on 52 votes. That networking should be based on sender/receiver drew weak consensus in favor, on 48 votes. The chair recorded one observation alongside that last result: "We don't have a paper in hand that proposes networking based on the P2300 model."<sup>[49]</sup>

P2469R0 objected at the time that "the proposed solution in P2300 forces a single composition mechanism, one for which we have limited field experience, on every user." Half of that objection has since been overtaken. Libunifex was in production in Meta's mobile applications by October 2021, with monthly active users in the billions<sup>[47]</sup>. The other half stands. `std::execution` entered the C++26 working draft at St. Louis in 2024 with roughly a third of the room opposed, and no networking is in the standard.

### 4.9 Observation 9

Prediction 5 stated that Model A's feedback mechanism should produce faster quality iteration than Model B's feedback mechanism.

Boost.Serialization was submitted for formal review and rejected. The author, Robert Ramey, revised the library and resubmitted it. It was accepted on the second review. Ramey wrote on the Boost mailing list in January 2023<sup>[50]</sup>: "The serialization library, after much feedback and consideration was initially rejected by Boost. This was the correct decision as it wasn't really ready by a long shot."

Peter Brett stated in the WG21 admin telecon minutes ([N4890](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/n4890.pdf), May 2021)<sup>[51]</sup>: "we dealt with NB comments and we did not do that based on implementation experience. All these bugs that we have found might have surfaced if we had the implementation experience."

Bryce Adelstein Lelbach stated in the same minutes<sup>[51]</sup>: "the amount of field experience we want to see is very different to how it was 4 or 5 years ago, and I believe that's because we shipped a lot of library features and found a lot of late problems. We have more experience with what happens if we don't make sure that we see field experience."

Arno Schoedl, CTO of think-cell GmbH, wrote on the Boost mailing list on May 9, 2024<sup>[52]</sup>: "Some recent additions to the standard made questionable design choices, which if a library had been implemented and widely used prior to standardization like in Boost, design choices may have been made differently."

The Boost feedback cycle is: submit, review, reject or accept with conditions, revise, re-review. The review window itself is ten days, though the wait for a volunteer review manager can run far longer. Niall Douglas counted twenty-three libraries in the queue in 2017, some of them "waiting around for years" for someone to manage a review<sup>[53]</sup>. The WG21 feedback cycle is: propose, advance through study groups, vote at plenary, ship in a standard on a three-year cadence. Boost.Serialization was rejected, revised, and accepted. `std::variant` was standardized without the field experience Howard Hinnant requested, and the defect persists.

### 4.10 Observation 10

Prediction 5 stated that Model A's feedback mechanism - users choosing alternatives - should produce faster quality iteration.

`{fmt}` and `std::format` share the same core design and the same original author. The marketplace version has shipped 58 releases since 2012, each incorporating user feedback, performance improvements, and new features<sup>[18]</sup>. The standard version ships on a three-year cadence. The `{fmt}` documentation states it is faster than `(s)printf`, `std::to_chars`, `to_string`, and `std::ostringstream`<sup>[18]</sup>.

Same design. Same author. Different feedback loops. After thirteen years, `{fmt}` stands at release 12.2.0, the fifty-eighth. `std::format` has been revised continuously as well. Its feature-test macro has been bumped eight times since C++20, across the C++23 and C++26 cycles and through defect reports applied retroactively to the standard that introduced it<sup>[54]</sup>.

The difference is what the revisions are for. The `{fmt}` releases add what users asked for. The `std::format` revisions repair what shipped.

The pattern is not confined to formatting. Section 4.12 lists the prior art behind every significant library addition in C++26, and the intervals run from eight years to forty. Each of those libraries had users, tests, and a maintainer before the committee looked at it. What the committee's cycle contributes is not validation, which the marketplace had already supplied, but the wait.

### 4.11 Observation 11

Prediction 6 stated that decisions binding every user should be made by the participants, and that the deciding body should be small.

The C++ standard library binds roughly 16.3 million developers<sup>[10]</sup>. The bodies that decide its content are these:

| Body              | Participants in a typical design poll |
| ----------------- | ------------------------------------- |
| Study group       | 11 to 16                              |
| LEWG (forwarding) | 24 to 34                              |
| Plenary           | 87 to 129                             |

Study group attendance is reported in the committee's own minutes. [N5000](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n5000.pdf)<sup>[55]</sup> records SG1 attendance as "averaged ~12 or so, peaked at ~20," SG6 as "a few people in the room and a few online for a minimum of our quorum of 6," and SG15 as "between 7 and 10 people." Per-poll tallies and attendance counts are published for each paper in the committee's public paper tracker<sup>[44]</sup>, so every figure above can be checked by any reader.

Plenary is large, but it does not re-open design. At Wroc&lstrok;aw in November 2024, LWG Poll 12 on P2835R7 passed with 41 in favor, 6 opposed, and 42 abstaining<sup>[55]</sup>. More delegates abstained than approved. The chair asked whether any national body objected, found none, and the motion carried.

The Direction Group described the mechanism in the same minutes<sup>[55]</sup>: "The number of papers is very large and the number of reflector messages for some groups are enormous. This unfortunately narrows the number of people who are able to keep up-to-date, participate, and provide informed votes."

Users report the same thing from outside. The committee's own 2025 developer survey records, among its ranked free-form themes, that developers perceive the committee as "insular, opaque, and more focused on niche use cases than the needs of working developers"<sup>[56]</sup>. That is a statement about perception rather than about output, and it should be read as one.

### 4.12 Observation 12

Prediction 6 stated that where a deployed Model A design and a Model B design are both live, the committee should choose its own, and that correction should come only retrospectively.

The pipeline is not the place to look, because it still runs. Every significant library addition in C++26 arrived from prior art outside the committee, and most of it arrived from a long way outside.

| Addition              | Prior art                                       | Interval  |
| --------------------- | ----------------------------------------------- | --------- |
| `linalg`              | BLAS (1979)                                     | 40+ years |
| saturation arithmetic | SSE2 and NEON hardware instructions             | 25+ years |
| RCU                   | Linux kernel (2002), DYNIX/ptx (1993)           | 24 years  |
| hazard pointers       | folly, in Meta production since 2017            | 21 years  |
| `text_encoding`       | IANA Character Sets registry (RFC 2978, 2000)   | 19 years  |
| `simd`                | Vc (2009)                                       | 15 years  |
| `philox_engine`       | Random123 (2011)                                | 13 years  |
| `inplace_vector`      | EASTL `fixed_vector` (2007), Boost (2013)       | 12 years  |
| `hive`                | `plf::colony` (2015)                            | 10 years  |
| `function_ref`        | LLVM, folly, Abseil, GDB, `tl::`, `type_safe::` | 10 years  |
| `views::concat`       | range-v3                                        | 8 years   |

[P1673R13](https://open-std.org/jtc1/sc22/wg21/docs/papers/2023/p1673r13.html)<sup>[57]</sup>, the linear algebra proposal, describes itself as "one of the strongest possible examples of standardizing existing practice that anyone could bring to C++."

Two entries in that release are hybrids rather than adoptions. `std::execution` was invented inside the committee, in P1525R0, then prototyped as libunifex and deployed before the vote. Contracts draw on Bloomberg's `bsls_assert`, described to the committee in 2013 as already carrying more than a decade of production use. Only reflection is committee work throughout.

So the marketplace still supplies. What it does not do is win an argument.

**The never-empty guarantee.** Boost.Variant, by Eric Friedman and Itay Maman, shipped a never-empty guarantee from 2002. At Lenexa in May 2015, LEWG ran an approval ballot on what a standard variant should do when a type-changing assignment throws<sup>[58]</sup>:

| Option                                                  | Approvals |
| ------------------------------------------------------- | --------- |
| invalid, assignable, undefined behavior on read         | 13        |
| empty, queryable state                                  | 12        |
| invalid, throws on read                                 | 6         |
| double buffer                                           | 5         |
| require all members nothrow-move-constructible          | 1         |
| require move-noexcept or one-default-construct-noexcept | 0         |

The marketplace's answer placed fourth of six, and `valueless_by_exception` shipped in C++17. Peter Dimov then implemented the rejected option anyway. `boost::variant2` entered Boost at 1.71 in August 2019 and states as its first property that it is never valueless, "achieved with the use of double storage, unless all of the contained types have a non-throwing move constructor"<sup>[27]</sup>.

**Networking.** Section 4.8 recorded the October 2021 ballot. Fifty delegates resolved that networking should be built on a model for which, as the chair noted at the time, no networking paper existed. The design they set aside had seventeen years of deployment behind it, and its author was in the room.

**What happens later.** The committee does correct itself, and it corrects toward the marketplace every time.

| Model B design                  | Model A replacement          | Shipped | Deprecated | Removed |
| ------------------------------- | ---------------------------- | ------- | ---------- | ------- |
| `auto_ptr`                      | `unique_ptr`, Boost.SmartPtr | C++98   | C++11      | C++17   |
| `bind1st`, `bind2nd`, `ptr_fun` | `bind`, Boost.Bind           | C++98   | C++11      | C++17   |
| `mem_fun`, `mem_fun_ref`        | `mem_fn`, Boost.Bind         | C++98   | C++11      | C++17   |

[N4190](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4190.htm)<sup>[59]</sup> states the reasoning in the committee's own words: `auto_ptr` "has been superseded by `unique_ptr`," and the old binders "were superseded by `mem_fn()`."

Boost had the smart pointer by 1999 and the standard removed its own in 2017. What the committee does not do is make that correction in the room, while both designs are live and a choice has to be made.

One condition would falsify this: a case where a deployed marketplace design beat a committee design in a contemporaneous decision on the same slot. Modules is not one, being a merger of the Modules TS with Clang's design rather than a contest between them. `string_view` is not one either, since the committee synthesized three industrial implementations and had no design of its own in the field. If such a case exists, this prediction fails.

---

## 5. The Record

Two models of library development are observable in the C++ ecosystem. Section 1 described their properties. Section 2 presented seven findings from the economic literature on centralized allocation and competitive markets. Section 3 derived six predictions from those findings. Section 4 tested each prediction twice - twelve observations drawn from real C++ libraries, committee documents, marketplace data, and the public statements of committee participants.

Prediction 6 carries the condition that would falsify it, stated at the end of Section 4.12. The observations are drawn from documents any reader can open, and where the record runs against the argument this paper has said so: the marketplace pipeline into C++26 is intact, and the two coroutine models were never set against each other. The record is public.

---

## Disclosure

The authors provide information and serve at the pleasure of the committee.

Vinnie Falco maintains [Boost.Beast](https://github.com/boostorg/beast)<sup>[60]</sup> and founded the [C++ Alliance](https://cppalliance.org/)<sup>[61]</sup>, where Harry Bott is chief executive. Both authors have a financial interest in the Boost ecosystem. This paper documents two observable models of library development and tests economic predictions against the public record.

The Boost ecosystem competes with the standard library. When this paper examines standard library components alongside Boost alternatives, the authors' stake is direct. The reader should weigh every claim in this paper with that bias in mind. Every quotation is attributed, and every document cited is public. Two sections rest in part on the authors' own prior papers, which are marked where they appear.

This paper asks for nothing.

---

## Acknowledgments

The authors thank Adam Smith, Friedrich Hayek, Ludwig von Mises, Joseph Schumpeter, Mancur Olson, George Stigler, and James Buchanan for the theoretical framework. The authors thank Bjarne Stroustrup for the historical record in the HOPL paper. The authors thank Howard Hinnant for the field experience principle and the `std::variant` assessment. The authors thank Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz for the Bannalia analysis and the Boost.Unordered rewrite. The authors thank Peter Dimov for `boost::variant2`. The authors thank Arno Schoedl for the design quality observation. The authors thank Niall Douglas for the creative destruction characterization. The authors thank Robert Ramey for the Boost.Serialization account. The authors thank Aaron Ballman for documenting WG21's procedures in P2274R0. The authors thank Peter Brett and Bryce Adelstein Lelbach for the field experience statements in the WG21 admin minutes. The authors thank Hartmut Kaiser for the volunteer review characterization. The authors thank Christopher Kohlhoff for twenty years of Boost.Asio.

---

## References

[1] [X3J16_90-0052. WG21 founding committee minutes, 1990](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/1990/WG21%201990/X3J16_90-0052%20WG21.pdf)

[2] [Boost](https://www.boost.org/). Free peer-reviewed portable C++ source libraries.

[3] [Bjarne Stroustrup. "Evolving a language in and for the real world: C++ 1991-2006." HOPL III, 2007](https://stroustrup.com/hopl-almost-final.pdf)

[4] [Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz. "WG21, Boost, and the ways of standardization." Bannalia, May 2024](https://bannalia.blogspot.com/2024/05/wg21-boost-and-ways-of-standardization.html)

[5] [Friedrich Hayek. "The Use of Knowledge in Society." *American Economic Review*, 35(4):519-530, 1945](https://doi.org/10.1142/9789812701275_0025)

[6] [Ludwig von Mises. "Economic Calculation in the Socialist Commonwealth." 1920](https://mises.org/library/economic-calculation-socialist-commonwealth-0)

[7] [Ludwig von Mises. *Bureaucracy*. Yale University Press, 1944](https://cdn.mises.org/Bureaucracy_3.pdf)

[8] Joseph Schumpeter. *Capitalism, Socialism and Democracy*. Harper & Brothers, 1942.

[9] Mancur Olson. *The Logic of Collective Action*. Harvard University Press, 1965.

[10] [Global developer population trends 2025](https://www.slashdata.co/post/global-developer-population-trends-2025-how-many-developers-are-there) - "How many developers are there?" (SlashData, 2025).

[11] George Stigler. "The Theory of Economic Regulation." *Bell Journal of Economics*, 2(1):3-21, 1971.

[12] James Buchanan and Gordon Tullock. *The Calculus of Consent*. University of Michigan Press, 1962.

[13] Adam Smith. *The Wealth of Nations*. 1776.

[14] [Christopher Kohlhoff. Boost.Asio and the Networking TS](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html)

[15] [P3126R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3126r0.pdf). Phil Ratzloff, Andrew Lumsdaine. "Graph Library: Overview." 2024.

[16] [P3126R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3126r4.pdf) - "Graph Library: Overview" (Phil Ratzloff, Andrew Lumsdaine, 2026).

[17] [JSON library benchmarks. Stephen Berry](https://github.com/stephenberry/json_performance)

[18] [{fmt}](https://github.com/fmtlib/fmt). Victor Zverovich. A modern formatting library.

[19] [fmtlib/fmt, archived 12 July 2019](http://web.archive.org/web/20190712163322/https://github.com/fmtlib/fmt). Internet Archive snapshot taken eight days before the Cologne adoption of P0645R10.

[20] [P0645R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0645r10.html). Victor Zverovich. "Text Formatting."

[21] [P2093R14](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2093r14.html). Victor Zverovich. "Formatted output." 2022.

[22] [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2274r0.pdf). Aaron Ballman. "C and C++ Compatibility Study Group." 2020.

[23] Howard Hinnant. Library reflector posts, July 2016. Quoted with permission in [P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf)<sup>[32]</sup>.

[24] Hartmut Kaiser. Boost mailing list, March 2017. Subject: "[boost] [review queue] Proposed new policy to enter the review queue."

[25] [N3370](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3370.html). Alisdair Meredith. "Call for Library Proposals." 2012.

[26] [P0308R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0308r0.html) - "Valueless Variants Considered Harmful" (Peter Dimov, 2016).

[27] [Boost.Variant2](https://www.boost.org/libs/variant2/). Peter Dimov. A never-valueless variant type.

[28] Niall Douglas. Boost mailing list, November 2023. Subject: "[boost] [scope] Scope review starts on November 26th."

[29] Andrey Semashev and Phil Endecott. Boost mailing list, July 2021. Subject: "[boost] Regexp performance guarantees."

[30] [Boost.Unordered benchmarks. Joaqu&iacute;n M L&oacute;pez Mu&ntilde;oz](https://github.com/boostorg/boost_unordered_benchmarks)

[31] [Working Draft, Programming Languages - C++](https://eel.is/c++draft/unord.req.general), [unord.req.general].

[32] [N1456](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2003/n1456.html) - "A Proposal to Add Hash Tables to the Standard Library (revision 4)" (Matthew Austern, 2003).

[33] [P1028R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p1028r6.pdf) - "SG14 status_code and standard error object" (Niall Douglas, 2023).

[34] [LWG 3070](https://cplusplus.github.io/LWG/issue3070) - "path::lexically_relative causes surprising results if a filename can also be a root-name" (Library Working Group, 2018).

[35] [LWG 3096](https://cplusplus.github.io/LWG/issue3096) - "path::lexically_relative is confused by trailing slashes" (Library Working Group, 2018).

[36] [P1164R1](https://open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1164r1.pdf) - "Make create_directory() Intuitive" (Nicolai Josuttis, 2019).

[37] [Boost.Filesystem Release History](https://www.boost.org/doc/libs/release/libs/filesystem/doc/release_history.html) (Andrey Semashev).

[38] [Daniel Lemire. "std::ranges may not deliver the performance that you expect." October 2025](https://lemire.me/blog/2025/10/05/stdranges-may-not-deliver-the-performance-that-you-expect/)

[39] [Announcing the Visual C++ Compiler November 2013 CTP](https://devblogs.microsoft.com/cppblog/announcing-the-visual-c-compiler-november-2013-ctp/) (Microsoft, 2013).

[40] [N3722](https://open-std.org/jtc1/sc22/wg21/docs/papers/2013/n3722.pdf) - "Resumable Functions" (Niklas Gustafsson, Deon Brewis, Herb Sutter, Sana Mithani, 2013).

[41] [N4134](https://isocpp.org/files/papers/N4134.pdf) - "Resumable Functions v.2" (Gor Nishanov, Jim Radigan, 2014).

[42] [P0099R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0099r0.pdf) - "A low-level API for stackful context switching" (Oliver Kowalke, Nat Goodspeed, 2015).

[43] [P1520R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1520r0.pdf) - "Response to response to 'Fibers under the magnifying glass'" (Gor Nishanov, 2019).

[44] [cplusplus/papers](https://github.com/cplusplus/papers) - ISO/IEC JTC1 SC22 WG21 paper scheduling and management, recording per-poll tallies and attendance.

[45] [P0991R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0991r0.html) - "Comparison of Stackful Coroutine Proposals" (Detlef Vollmann, 2018).

[46] [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf). Christopher Kohlhoff, Jamie Allsop, Vinnie Falco, Richard Hodges, Klemens Morgenstern. "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not." 2021.

[47] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html). Micha&lstrok; Dominiak, et al. "std::execution." 2024.

[48] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[49] [cplusplus/papers issue 1113](https://github.com/cplusplus/papers/issues/1113) - poll records for the joint Library Evolution and Concurrency telecon of 4 October 2021, recorded by Bryce Adelstein Lelbach.

[50] Robert Ramey. Boost mailing list, January 2023. Subject: "[boost] [Aedis] Formal Review: We could have done better."

[51] [N4890](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/n4890.pdf). Nina Ranns. "WG21 2021-05 Admin telecon minutes." 2021.

[52] Arno Schoedl. Boost mailing list, May 9, 2024. Subject: "[boost] What is this 'Beman Project Development'?"

[53] [Niall Douglas. Boost mailing list, March 2017. Subject: "[boost] Paying for review managers."](https://lists.boost.org/archives/list/boost@lists.boost.org/thread/RY4LIZ7XMXT2NCLBRQESILUXRG5JVTIY/)

[54] [Feature test macros and standard library headers](https://en.cppreference.com/w/cpp/utility/format) - the `__cpp_lib_format` value history.

[55] [N5000](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n5000.pdf) - "WG21 November 2024 Hybrid meeting Minutes of Meeting" (Nina Ranns, 2024).

[56] [2025 Annual C++ Developer Survey "Lite"](https://isocpp.org/files/papers/CppDevSurvey-2025-summary.pdf) - summary of results (Standard C++ Foundation, 2025).

[57] [P1673R13](https://open-std.org/jtc1/sc22/wg21/docs/papers/2023/p1673r13.html) - "A free function linear algebra interface based on the BLAS" (Mark Hoemmen, Daisy Hollman, Christian Trott, Daniel Sunderland, Nevin Liber, Alicia Klinvex, Li-Ta Lo, Damien Lebrun-Grandie, Graham Lopez, Peter Caday, Sarah Knepper, Piotr Luszczek, Timothy Costa, 2023).

[58] [P0088R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2016/p0088r1.html) - "Variant: a type-safe union that is rarely invalid (v6)" (Axel Naumann, 2016). Records the Lenexa approval ballot.

[59] [N4190](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4190.htm) - "Removing auto_ptr, random_shuffle(), And Old &lt;functional&gt; Stuff" (Stephan T. Lavavej, 2014).

[60] [Boost.Beast](https://github.com/boostorg/beast). Vinnie Falco. HTTP and WebSocket library.

[61] [C++ Alliance](https://cppalliance.org/).
