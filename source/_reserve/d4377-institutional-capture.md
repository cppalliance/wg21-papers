---
title: "Institutional Capture of the C++ Coroutine Task Type"
document: P4377R0
date: 2026-09-10
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

"WG21 is where great designs go to become good designs." - Vinnie Falco

The standard coroutine task type is the product of institutional capture, and the record is the committee's own.

The committee's founding documents state a preference for existing practice, recorded by its Direction Group as having little effect; no admission rule has ever policed the door. The sender model was created inside the committee in 2019, and the October 2021 polls redirected networking toward it over a deployed alternative - the warnings published before the vote, the model's published production use confined to its authors' own organizations, none of it networking. Five years later, no sender-based networking has shipped; the correction record accumulated before any vendor shipped the design and grows in the current mailing; and the adopted task type carries a second template parameter as a structural requirement of that model, against an ecosystem whose independent task types converged on one, at costs the specification mandates, four of which cannot be repaired after shipment. On that record - every element of it visible to the institution in its own documents at the time of the decision - the C++ Alliance states that it does not have confidence that WG21, with its current delegate population and ruleset, can deliver coroutine-only I/O to the standard without alterations that materially harm users, or networking based on senders and receivers in a form that will resonate with ordinary users, and concludes that users are best served by library components that compete fairly in the marketplace rather than components designed in place by committee.

---

## Revision History

### R0: September 2026

* Initial version.

---

## 1. Introduction

This paper examines the standard coroutine task type, `std::execution::task`, and the process that produced it: the existing-practice rule the committee wrote for itself, the October 2021 polls that set networking's direction, the correction record since adoption, and the constraint that makes the task type a sender.

Related work. The author's prior papers examine parts of this record: [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> (the Environment parameter and task-type diversity), [P4097R1](https://isocpp.org/files/papers/P4097R1.pdf)<sup>[2]</sup> (the October 2021 polls), [P4096R1](https://isocpp.org/files/papers/P4096R1.pdf)<sup>[3]</sup> (the 2021 analysis and its framings), [P4099R1](https://isocpp.org/files/papers/P4099R1.pdf)<sup>[4]</sup> (the twenty-one-year networking arc), [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup> (the spec-mandated costs), [P4041R0](https://isocpp.org/files/papers/P4041R0.pdf)<sup>[6]</sup> (the post-adoption correction ledger), and [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> (admission criteria and the Standardization Penalty). This paper assembles the record they document and states the conclusion the C++ Alliance draws from it.

The contributions:

1. A documentary history of the sender model, from the existing-practice record (Section 3) through the October 2021 polls (Section 4.3) to the current mailing (Section 4.5).
2. An analysis of the task type's constraint and its spec-mandated costs (Section 5).
3. A comparison of the two architectures' home domains and the bridges between them (Section 6).
4. The expected objections in their strongest form, answered from the record (Section 8).
5. The conditions under which confidence would be restored, with a falsification condition (Section 9).

Assumptions. The public record is the record: published papers, published poll outcomes, public repositories. Polls and advisories are cited as the historical record of what a body resolved, never as evidence of technical merit. The author's stake is disclosed in Section 2.

---

## 2. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++. The C++ Alliance develops both libraries and competes in the marketplace the conclusion recommends.

The author is a co-author of [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[8]</sup>, "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not," which argued in October 2021 that the Networking TS was more mature than [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[9]</sup>. The reader should be aware that the author had a prior published position on the relationship between the Networking TS and the sender/receiver model.

The author's prior analyses are cited where their evidence is used; each is identified as the author's own work where it is introduced.

---

## 3. The Founding Rule

This section covers the committee's own stated criteria for admitting library components, because every later section measures the sender model's admission against them. The criteria were stated repeatedly, in public documents, across twenty-five years.

The TR2 call for proposals in 2005 stated the principle together with its rationale ([N1810](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1810.html)<sup>[10]</sup>):

> "The committee prefers proposals that are based on existing practice. Existing practice isn't an absolute rule, but it is an important guideline that the committee can use to judge the risk of a proposal. First, a proposal must be implementable, and the best evidence that something is implementable is that it has been implemented. Second, if a proposal is based on existing practice, the committee can have more confidence that the proposal solves a real problem and that its interface serves the needs of real users."

The standing call for library proposals restated the principle in 2012 and added a delivery rule ([N3370](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3370.html)<sup>[11]</sup>): "the clear preference is for new library components to go into TRs, while modifications go into the standard."

In 2018 the Direction Group assessed the founding criteria on the record ([P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[12]</sup>):

> "During the early stages of the development of the first standard, we articulated some principle for what to include in the standard library, including Language support; Facilities that everybody needs; Facilities needed for communicating among separately developed libraries. We think these are reasonable criteria, but in practice they didn't have much effect."

The same paper named the cost side: "No feature is cost free, there is always the implementation cost, the cost of producing teaching material, the time needed to learn, the opportunities for confusion, and the inevitable distraction from overselling."

In 2020, a document describing WG21's procedures to WG14 members stated the evidentiary situation plainly ([P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2274r0.pdf)<sup>[13]</sup>): "WG21 finds implementation experience with a proposal to be incredibly valuable but does not have any requirement on implementation experience to adopt a proposal."

In 2022 the Direction Group was still asking for the discussion to start ([P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.pdf)<sup>[14]</sup>, Section 5.3): "We encourage a discussion of criteria of what should be in the standard library and what should not. The aim is to be able to discuss proposed new standard-library components in the context of articulated criteria."

The nearest modern criteria statement appears in a paper written to argue against one admission ([P3001R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p3001r0.html)<sup>[15]</sup>, 2023): "Elements of the standard library ideally fall into one of the following categories: 3.1 Types and functions requiring compiler intrinsics ... 3.2 Core vocabulary types ... 3.3 Cross-platform OS abstractions ... 3.4 Fundamental algorithms and data structures."

The field-experience standard has an elder's formulation. Howard Hinnant, writing in July 2016 during the `std::variant` debate (originally posted to the library reflector; republished with permission in [P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf)<sup>[16]</sup>):

> "I should quit asking: 'Has it been implemented?' The correct question is: What has been the field experience? Is there positive feedback from anyone outside your immediate family or people who could have a perceived conflict of interest (such as employees of your company)? Having your Mom and your direct reports say the proposal is wonderful is nice, but not sufficient."

And on the design risk of standardizing ahead of that experience:

> "It is now my understanding that we (the committee) have made significant design changes with respect to all existing variants in the field (most notably boost::variant). We /think/ these are good changes, and I /hope/ that we are right. We won't /know/ if these are good design changes until we have field experience with an implementation that implements these design changes."

The author's own [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> traced this record in full and summarized it: "The committee checks whether a proposal is well-made. Nothing on record checks whether the standard needs it."

The criteria the committee wrote for itself were quality filters: they ask whether a proposal is well-made, implementable, and welcome. By the Direction Group's own assessment they had little effect, and nothing on record enforces them.

---

## 4. A History of the Sender Model

This section traces the sender model from its origins to the present mailing, in five steps: the practice that preceded it (4.1), its invention (4.2), the October 2021 polls that made it the direction for networking (4.3), what followed for networking (4.4), and the correction record since adoption (4.5). Every quotation is from the public record.

### 4.1 Forty Years of Practice

Asynchronous I/O completion predates the committee's networking effort by decades: BSD sockets arrived in 1983, Windows I/O completion ports in 1994, `kqueue` in 2000, and `epoll` in 2002. Boost.Asio began in 2003 and has been in production use ever since. Its authors described the model in October 2021 ([P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[8]</sup>):

> "The asynchronous model of Asio/Net.TS has also evolved to support new use cases while also being careful not to leave existing use cases behind, and the strength of the composition model is testament to that. The model is the result of growth and adaptation from use in the real world, and is one reason it is so widely deployed."

The Networking TS followed, published as an ISO Technical Specification in 2018. The author's [P4088R1](https://isocpp.org/files/papers/P4088R1.pdf)<sup>[17]</sup> summarizes the durability of the completion contract: "The contract has survived POSIX, BSD sockets, IOCP, Asio, the Networking TS, io_uring, and every transport from TCP to QUIC."

The committee's own networking effort is nearly as old as the TR2 call. The first networking proposal is [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf)<sup>[18]</sup>, "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, December 2005), posted seven months after [N1810](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1810.html)<sup>[10]</sup> listed networking among the welcomed proposal areas. The twenty-one-year arc from N1925 to the present is traced in the author's [P4099R1](https://isocpp.org/files/papers/P4099R1.pdf)<sup>[4]</sup>.

The practice base for asynchronous I/O was four decades deep, deployed, and public.

### 4.2 The Invention

The sender model did not come from that practice base. The author's [P4094R1](https://isocpp.org/files/papers/P4094R1.pdf)<sup>[19]</sup> records the arc:

> "In 2014, three deployed executor models - networking, GPU dispatch, and thread pools - were unified into P0443R0, which went through fourteen revisions, was never deployed as unified, and was replaced by P2300R10."

[P1791R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1791r0.html)<sup>[20]</sup> records the scale of the unification effort: "more than 100 papers and revisions have been produced that either directly or indirectly have significantly impacted the consensus position represented by P0443."

In 2019, [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf)<sup>[21]</sup> argued that the unified executor's basis operation could not support generic error handling:

> "Any errors that happen, whether during task submission, after submission and prior to execution, or during task execution, are handled in an implementation-defined manner, which can vary from executor to executor. The implication is that no generic code can respond to asynchronous errors in a portable way."

At Cologne in 2019 the committee adopted the redesign. The author's [P4095R1](https://isocpp.org/files/papers/P4095R1.pdf)<sup>[22]</sup> records what changed: "Sender, Receiver, and Scheduler concepts were introduced. The executor concept was reduced to a single `execute` function." And where the redesign came from: "The sender/receiver model that replaced the executor concept traces its committee lineage to this paper."

The author's [P4014R2](https://isocpp.org/files/papers/P4014R2.pdf)<sup>[23]</sup> documents the design's intellectual pedigree: continuation-passing style (Steele and Sussman, 1975-1980), monads (Moggi, 1991), delimited continuations and algebraic effects (Danvy and Filinski, 1990). It describes the result as "continuation-passing style expressed as composable value types, drawing on techniques refined across four decades of programming language research." The theory was four decades old. The application as the general asynchronous substrate for C++ was new, and it was developed inside the committee rather than adopted from the field.

The author's [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> names what the design provides: "`std::execution` provides a composable asynchronous model with structured cancellation, compile-time work-graph construction, and deployed GPU-domain prototypes."

The deployment record at the time of adoption is also on the record. [P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf)<sup>[24]</sup>, the P2300R2 presentation slides, documented the production use:

> "Sender/receiver as specified in P2300R2 is currently being used in the following shipping Facebook products: Facebook Messenger on iOS, Android, Windows, and macOS; Instagram on iOS and Android; Facebook on iOS and Android; Portal; An internal Facebook product that runs on Linux."

The author's [P4097R1](https://isocpp.org/files/papers/P4097R1.pdf)<sup>[2]</sup> tabulates the full deployment evidence at the time of the vote: "Sender deployments (non-networking): [P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf)<sup>[24]</sup>: Facebook (mobile apps), NVIDIA (GPU dispatch), Bloomberg (experimentation)." The production deployments were at the design authors' own employers; the third entry was experimentation. None was networking.

The sender basis was created inside the committee in 2019. At the time of the October 2021 vote, its published production use was at its authors' own organizations, and none of it was networking.

### 4.3 The Polls

This section presents the October 2021 votes that set the direction, from the published poll outcomes ([P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[25]</sup>, "2021 October Library Evolution and Concurrency Networking and Executors Poll Outcomes"). The polls are quoted as the historical record of what the body resolved. No poll is evidence of technical merit, in either direction, and this paper applies that rule to every poll it cites, including the ones it agrees with.

Fifty-six committee members participated in five polls taken October 4-8, 2021 by electronic ballot.

Poll 1 asked about the deployed model:

> "The Networking TS/Asio async model (P2444) is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs."
>
> SF:5 / WF:10 / N:6 / WA:14 / SA:18 - Weak consensus against.

Poll 2 asked about the sender model:

> "The sender/receiver model (P2300) is a good basis for most asynchronous use cases, including networking, parallelism, and GPUs."
>
> SF:24 / WF:16 / N:3 / WA:6 / SA:3 - Consensus in favor.

[P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[25]</sup> publishes 45 voter comments on Poll 2, spanning every position from Strongly Favor to Strongly Against. The four below are this paper's selection, all from Weakly Favor voters:

> "I think this is a good basis for parallelism/GPUs but can't judge its suitability for networking."

> "My vote is weakly in favor as I am not familiar enough with the networking requirements to be sure that it satisfies those, but for the other domains I am confident it does. If this were only for the parallelism and GPUs use case I would vote strongly in favour."

> "P2300R2 has not been around as long as Asio and hasn't been 'tried by fire' in the networking domain. I'm pretty familiar with special cases of networking for parallel computing, but not generally familiar with 'doing networking in C++,' so I'm voting WF instead of SF."

> "I think the general direction of sender/receiver more closely matches the semantics of the language and normal functions with regards to its handling of separate value/error channels... However, I do not think that sender/receiver is sufficiently well-baked to be included in C++23, and could do with some more refinement to address issues raised and more implementation experience."

These votes counted toward the consensus in favor that included networking.

Poll 3 asked whether to stop pursuing the Networking TS:

> "Stop pursuing the Networking TS/Asio design as the C++ Standard Library's answer for networking."
>
> SF:13 / WF:13 / N:8 / WA:6 / SA:10 - No consensus.

The chair's interpretation:

> "What this doesn't mean: The Networking TS is not "dead"."
>
> "What this means: The C++ Committee will still work on networking in this general form, but the authors need to do a lot in order to build up consensus to get something like the TS merged into the standard. The bulk of this work should be done in Networking Study Group. Many of the people in favor of stopping work on the TS would like networking to be built on top of Senders and Receivers. Others were opposed to the lack of security through Transport Layer Security (TLS). It is highly unlikely that design changes to the Networking TS can be made fast enough, and consensus gained fast enough, for networking to make C++23."

Poll 4 asked the networking-specific question:

> "Networking in the C++ Standard Library should be based on the sender/receiver model (P2300)."
>
> SF:17 / WF:11 / N:10 / WA:4 / SA:6 - Weak consensus.

The chair's interpretation:

> "What this doesn't mean: Work on networking using other models will still be reviewed and considered on its own merits. WG21 doesn't pause work on a concrete paper based off of the wish for another paper. Note that there are a high number of neutrals on this vote. Many of the neutrals (and some of the abstentions) would like to see a paper before picking a side here."
>
> "What this means: In the short term, this poll result doesn't mean much. We don't have a paper in hand that proposes networking based on the [P2300R2] model. For paper authors though, this poll is encouragement to do work in the area of networking based on senders and receivers, or to be prepared with compelling new information on why networking should use a different model."

A selected voter comment on Poll 4, from a Neutral voter:

> "Maybe it should, but there is no concrete proposal to evaluate, let alone one that has been field-tested. We've tried inventing networking before pursuing ASIO, and that effort didn't succeed."

Poll 5 asked whether socket-based networking without TLS could ship; it reached no consensus.

A sixth poll, taken at the September 28, 2021 telecon and reproduced in [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[25]</sup> Section 3, tested the premise behind all of the above:

> "We believe we need one grand unified model for asynchronous execution in the C++ Standard Library, that covers structured concurrency, event based programming, active patterns, etc."
>
> SF:4 / WF:9 / N:5 / WA:5 / SA:1 - No consensus (leaning in favor).

The premise of a single unified model was tested by poll and did not achieve consensus. The guidance that followed proceeded as if it had. [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[25]</sup> Section 3 states: "The combination of this 'grand unified model' poll and Poll 4 heavily encourages the networking study group to produce a paper based on Senders and Receivers." The guidance to the Networking Study Group:

> "Before bringing networking papers back to Library Evolution, two major areas need to be thoroughly addressed: Security, and the Senders and Receivers async model."

The guidance further states that a non-sender/receiver paper would need "compelling new information in order to convince the 'grand unified model' contingent that S&R can't get the job done suitably." [P2400R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2400r3.html)<sup>[26]</sup>, the Library Evolution status report for the period ending January 2022, confirmed that networking remained listed as "Under Networking Study Group review" and restated the compelling-new-information burden.

The warnings were on the record before the vote. [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf)<sup>[27]</sup> (Kohlhoff, August 2021), two months before the polls, documented that compound I/O results - an error code and a byte count - cannot be routed onto the sender's three completion channels without information loss:

> "Due to the limitations of the set_error channel (which has a single 'error' argument) and set_done channel (which takes no arguments), partial results must be communicated down the set_value channel."

And [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[8]</sup>, published the week the polls opened, warned:

> "Conversely, the proposed solution in P2300 forces a single composition mechanism, one for which we have limited field experience, on every user."

The author's [P4097R1](https://isocpp.org/files/papers/P4097R1.pdf)<sup>[2]</sup> summarizes the sequence: "The committee asked the architect of the Networking TS to adopt a model he had already published evidence was structurally incompatible with networking I/O."

The October 2021 polls redirected networking toward a model for which no networking proposal existed, over a deployed alternative, with the warnings on the record.

### 4.4 The Aftermath

This section covers what followed for networking under the guidance.

The first published paper proposing sender-based networking APIs arrived fifteen months after the polls: [P2762R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r0.pdf)<sup>[28]</sup> (K&uuml;hl, January 2023), "Sender/Receiver Interface For Networking." It mentioned a coroutine task for networking in one paragraph:

> "It may be useful to have a coroutine task (`io_task`) injecting a scheduler into asynchronous networking operations used within a coroutine... The corresponding task class probably needs to be templatized on the relevant scheduler type."

The author's [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup> records where that line of work stands: "[P2762R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r2.pdf)<sup>[29]</sup> stopped at R2 (October 2023). No revision in over two years. No published paper defines what `IoEnv` looks like inside `std::execution::task`."

In November 2023, [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup> records, SG4 polled at Kona that networking must use the sender model. The public trip report for that meeting corroborates the substance: the group had "a consensus in favor of supporting only the Senders/Receivers model for asynchronous operations and dropping the executors model from the Networking TS" ([r/cpp Kona 2023 trip report](https://www.reddit.com/r/cpp/comments/17vnfqq/)<sup>[30]</sup>). The SG4 minutes are not publicly accessible, so the poll text and tally cannot be reproduced from the primary record.

The author's [P4099R1](https://isocpp.org/files/papers/P4099R1.pdf)<sup>[4]</sup> records the prototypes that exist - K&uuml;hl's P2762 work and experimental library, and a Qt integration - and notes that no production networking deployment on senders has been published. The one published production evaluation is [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf)<sup>[31]</sup> (Mungo Gill, C++ Alliance), a derivatives exchange's port from Asio to coroutine-native I/O (the engineers are anonymized and the paper discloses that the study design and reporting are not independent). It records the partner's evaluation of the sender model:

> "The partner evaluated sender/receivers and concluded that the model of computation was not aligned with their workload or their workflow. No further assessment was undertaken."

The author's [P4097R1](https://isocpp.org/files/papers/P4097R1.pdf)<sup>[2]</sup> states the timeline's end point: "2026: no sender-based networking has shipped. Networking is not in the C++ standard. Twenty-one years from N1925."

Five years after the polls, no sender-based networking has shipped, and the twenty-one-year networking arc continues.

### 4.5 Designed In Place

This section covers the correction record since the design's adoption: what was removed before the merge, what has been repaired since, and what the current mailing adds.

Before the working-draft merge, [P3187R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3187r1.pdf)<sup>[32]</sup> removed three operations - `ensure_started`, `start_detached`, and `execute` - from the approved design. The stated reason: "the current design of these facilities would introduce major footguns in the standard library as they are deceptively enticing yet difficult to use correctly, making it much harder to guarantee code safely cleans up resources used by the eagerly launched operations."

[P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[9]</sup> was adopted into the C++26 working draft at the St. Louis plenary in June 2024. Jonathan M&uuml;ller's [trip report](https://www.think-cell.com/en/career/devblog/trip-report-summer-iso-cpp-meeting-in-st-louis-usa)<sup>[33]</sup> records the margin: "it was a very narrow vote with 1/3 voting against adoption."

The author's [P4041R0](https://isocpp.org/files/papers/P4041R0.pdf)<sup>[6]</sup> attempts a complete enumeration of the post-adoption changes, compiled from published WG21 mailings, the Library Working Group (LWG) issues list, and the C++26 national-body (NB) ballot repository. Its category table counts 2 removals, 1 rewrite, 2 architectural fixes, 1 wording omnibus, 7 post-adoption additions, 5 LWG defects, and 4 national-body comment groups. Its direction-of-change table, which counts differently, states: "Twenty-four post-adoption items modified the sender sub-language or its integration. Zero modified coroutines."

In January 2026 the design's architect wrote in [P3826R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r3.html)<sup>[34]</sup>:

> "That change has some ripple effects, the biggest of which is that the receiver is not known during early customization. Therefore, early customization is irreparably broken and must be removed."
>
> "There are risks with trying to fix the problem now. It is a design change happening uncomfortably close to the release of C++26. One mitigating factor is that the major Standard Library vendors seem to be in no rush to implement std::execution. If there are lingering problems, they could be fixed with the usual DR process."

The vendor observation is borne out by the record. The author's [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> compiles the vendor status pages: as of July 2026, no mainstream standard library ships `std::execution` - libstdc++, libc++, and MSVC STL all record "none." The Execution control clause enters the working draft at 91 pages, larger than the filesystem or regular expressions clauses, with zero shipping mainstream implementations.

The task type followed the same pattern at smaller scale. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[35]</sup> was plenary-approved for C++26 at Sofia in 2025; the author's [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> records that six motions at Croydon in 2026 modified `task` after plenary approval.

The pattern continues in the current mailing. [P4373R0](https://isocpp.org/files/papers/P4373R0.pdf)<sup>[36]</sup> (Leahy, this mailing) observes that the standard permits a consumer to observe whether an operation emits a stopped completion but not why, and proposes to legislate the distinction through undefined behavior: an operation that advertises a stopped completion only when its environment carries a stop token is undefined if "it invokes `set_stopped(rcvr)` when `get_stop_token(get_env(rcvr)).stop_requested()` is false." Two years after adoption, the meaning of the stopped channel is still being specified.

Every repair in this section predates the first shipping implementation of the design it repairs.

---

## 5. The Centerpiece: The Task Type

This section covers the standard coroutine task type: the demand for it, the constraint it carries, and what the constraint costs. The task type is where the sender model's requirements meet every coroutine user.

A standard task type has been requested since C++20 shipped the coroutine machinery with no library. The discussion notes of SG1, the concurrency study group, record the expectation of diversity (reproduced in [P3552R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r0.pdf)<sup>[37]</sup>): "There can be more than one task type for different needs." The adopted design acknowledges the same limit in its own objectives section ([P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[35]</sup>): "The task coroutine provided by the standard library may not always fit user's needs although they may need/want various of the facilities."

The adopted `task` is not only a coroutine task type. It is a sender: it carries the full sender protocol, including completion signatures computed as a function of an environment, and therefore it takes a second template parameter, `Environment`. The author's [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> states the consequence plainly: "The Environment parameter is a structural requirement imposed by P2300."

The environment protocol bottoms out at one concept. [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[9]</sup> defines `queryable` in [exec.queryable.concept] as follows:

```cpp
template<class T>
  concept queryable = destructible<T>; // exposition only
```

`scheduler` refines it directly; `sender` and `receiver` require their associated environments to model it. [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> tabulates the relationship between the clause and its foundation:

| [exec]       | [exec.queryable.concept] |
| ------------ | ------------------------ |
| 6,607 lines  | 2 lines                  |

*Table: the Execution control clause and the concept at its foundation, from [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup>.*

And its finding: "`queryable` is `destructible`. It cannot be narrowed after C++26 ships. N libraries with N different environments produce N incompatible task types with no general conversion path."

The ecosystem's library authors have already decided this shape. [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> surveys nine coroutine task types:

| Library       | Declaration                                                           | Params |
| ------------- | --------------------------------------------------------------------- | :----: |
| asyncpp       | `template<class T> class task`                                        |   1    |
| Boost.Cobalt  | `template<class T> class task`                                        |   1    |
| Capy          | `template<class T = void> struct task`                                |   1    |
| cppcoro       | `template<typename T> class task`                                     |   1    |
| aiopp         | `template<typename Result> class Task`                                |   1    |
| libcoro       | `template<typename return_type> class task`                           |   1    |
| folly::coro   | `template<typename T> class Task`                                     |   1    |
| Boost.Asio    | `template<class T, class Executor = any_io_executor> class awaitable` | **2**  |
| P3552R3 (std) | `template<class T, class Environment> class task`                     | **2**  |

*Table: nine coroutine task types and their template parameter counts, from [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup>; declarations from each library's public repository.*

The convergence argument is not about counting libraries - it is about independent design decisions. Five teams, plus the author's Capy and Morgenstern's Cobalt, arrived at one parameter. Two of the five carry affiliations with the sender model's own authors - cppcoro is Lewis Baker's library, and folly is Meta's - and both designs predate P2300's 2021 publication. The two libraries that added a second parameter both needed an escape hatch: Asio provides `any_io_executor`; [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[35]</sup> does not.

The layering was the design intent of the coroutine machinery. Gor Nishanov wrote in [P0975R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0975r0.html)<sup>[38]</sup>: "Unlike most other languages that support coroutines, C++ coroutines are open and not tied to any particular runtime or generator type and allow libraries to imbue coroutines with meaning." His layering model ([P1362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1362r0.pdf)<sup>[39]</sup> Section 4.4) assigns environment customization to the awaitable tier: power users define new awaitables for their environment using existing coroutine types; the coroutine type stays fixed. [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> states the inversion: "What Nishanov assigned to the awaitable tier, `task<T, Environment>` moves into the expert tier and exposes in the return type."

Adaptation between environments exists but is manual. [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> traces `write_env`, the mechanism [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[9]</sup> provides: "The caller must know every custom query from every library, by name, and inject them all manually. There is no discovery mechanism - no way to ask an environment 'what queries do you need?'" Custom queries are not hypothetical. NVIDIA's reference implementation defines `get_stream_provider_t`, a custom forwarding query whose `stream_provider` carries a CUDA stream and, via its `context_` member, pinned and managed memory resources, a stream pool, a task hub, and a priority level ([nvexec/stream/common.cuh](https://github.com/NVIDIA/stdexec/blob/main/include/nvexec/stream/common.cuh)<sup>[40]</sup>). As [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf)<sup>[1]</sup> records: "This is not hypothetical. This is deployed code in the `std::execution` reference implementation."

The costs are analyzed in the author's [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup>, which grants every engineering fix that has been proposed and compares against the best possible conforming implementation - one that eliminates every cost not mandated by [exec.task]:

| Property                                     | Coroutine-native `task<T>`  | Best `task<T, IoEnv>` Case A                     | Best `task<T, IoEnv>` Case B                     |
| -------------------------------------------- | --------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Template parameters                          | 1                           | 2                                                | 2                                                |
| Sender concept instantiation per task        | 0                           | 1 per task type in chain                         | 1 per task type in chain                         |
| Task-to-task `co_await` suspend              | 2 pointer stores            | `state<Rcvr>` construction + scheduler extraction | `state<Rcvr>` construction + scheduler extraction |
| I/O `co_await` suspend                       | 2 pointer stores            | 2 pointer stores                                 | `state<Rcvr>` construction + scheduler extraction |
| I/O `co_await` `affine` wrapping          | 0                           | 0                                                | 1 per I/O operation                              |
| I/O `co_await` symmetric transfer            | Yes                         | Yes                                              | No (void-returning `set_value`)                  |
| Type-erased stream I/O allocation            | 0                           | 0                                                | 1 heap allocation per I/O operation              |

*Table: spec-mandated costs of `task<T, IoEnv>` that do not exist in the coroutine-native model, from [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup>. Case A assumes I/O operations return awaitables; Case B assumes I/O operations return senders, the stated direction for networking.*

The costs are normative, not implementation quality: "The `state<Rcvr>` construction and scheduler extraction are spec-mandated and remain in any conforming implementation." [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf)<sup>[5]</sup> is careful about what the table claims: the operation counts are theoretical, the wall-clock cost of each operation is an empirical question, and "That it exists is a normative one."

Some of the costs cannot be repaired after shipment. The author's [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf)<sup>[41]</sup> classifies the open issues by whether shipping forecloses the fix. Four are foreclosed or partly foreclosed: allocator timing (the frame is allocated before `connect`/`start` runs, so the receiver's environment is unavailable to `operator new`), allocator propagation (no automatic frame-allocator propagation through the coroutine call tree), error return (`task` requires `co_yield with_error(e)`; `co_return` cannot carry an error value), and symmetric transfer (the completion functions return `void`, providing no channel to propagate a `coroutine_handle<>`). Jonathan M&uuml;ller's [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[42]</sup> states the consequence of the last: "Having iterative code that is actually recursive is a potential security vulnerability." In April 2026 a user [reported](https://github.com/NVIDIA/stdexec/issues/2047)<sup>[43]</sup> a production crash in stdexec - "Destroying the spawn state destroys the task operation, which destroys the currently executing task coroutine frame, including the sender awaiter whose `await_suspend()` has not returned yet" - a single report, reproducible on MSVC only.

The implementation record closes the section. [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[35]</sup>'s implementation section states: "This implementation hasn't received much use, yet, as it is fairly new."

The Environment parameter makes the standard task type carry the sender model's requirements. The ecosystem's independent task types converged on one parameter. And the remaining costs are spec-mandated, not accidents of implementation.

---

## 6. Two Architectures

This section covers the shape of each model and the domain each serves, because the capture claim does not require the sender model to be wrong everywhere - only imposed where it does not serve.

The sender model's strengths are real and named in the record. The author's [P4088R1](https://isocpp.org/files/papers/P4088R1.pdf)<sup>[17]</sup> states the design fork: the receiver-parameterized operation state gives the optimizer full pipeline visibility across a compile-time work graph - the property that serves GPU kernel fusion and heterogeneous pipelines. The same paper documents what the fork costs at the I/O boundary, in a benchmark of 100,000,000 `read_some` calls:

| Stream type  | capy IoAwaitable    |       | P2300 sender        |       |
| ------------ | ------------------: | ----: | ------------------: | ----: |
|              | ns/op               | al/op | ns/op               | al/op |
| Native       | 31.4                | 0     | 30.0                | 0     |
| Abstract     | 32.1                | 0     | 53.5                | 1     |
| Type-erased  | 36.4                | 0     | 53.4                | 1     |

*Table: per-operation cost under type erasure, from [P4088R1](https://isocpp.org/files/papers/P4088R1.pdf)<sup>[17]</sup>. At the native level the models are equivalent; under type erasure, awaitables add +5 ns and zero allocations, senders add +23 ns and one allocation per operation.*

The composition algebra has its own boundary. The author's [P4090R1](https://isocpp.org/files/papers/P4090R1.pdf)<sup>[44]</sup> constructs the comparison and concludes: "The cost of engaging the composition algebra for compound I/O results is nonzero. The benefit over `if (ec)` is zero." The author's [P4091R1](https://isocpp.org/files/papers/P4091R1.pdf)<sup>[45]</sup> names the mechanism: "The coroutine floor is `throw`. The sender floor is `set_error`. Both destroy compound data when crossed. The difference is where the floor sits relative to composition. In coroutines, the floor is opt-in. In senders, the composition algebra lives above it."

The two models need no capture to coexist, and the record shows it. The author's bridge papers - [P4092R1](https://isocpp.org/files/papers/P4092R1.pdf)<sup>[46]</sup> (consuming senders from coroutine-native code) and [P4093R1](https://isocpp.org/files/papers/P4093R1.pdf)<sup>[47]</sup> (producing senders from coroutine-native code) - demonstrate interoperation in both directions, implemented in Capy.

The practitioner study group has recorded its position. SG14, the study group for low-latency systems, states in its priority list ([P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[48]</sup>): "SG14 advise that Networking (SG4) should not be built on top of P2300. The allocation patterns required by P2300 are incompatible with low-latency networking requirements." That advisory is cited as the historical record of a study group's position, under the same rule applied in Section 4.3: no poll or advisory is evidence of technical merit, in either direction.

Each model has a home domain, and the bridges demonstrate that coexistence does not require capture.

---

## 7. The Self-Inflicted Wound

This section covers why the failure was avoidable: every element of it was visible to the institution at the time of the decision, in its own documents.

The institution's own principles stated the rule. Section 3 presents them: the existing-practice preference ([N1810](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1810.html)<sup>[10]</sup>, [N3370](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3370.html)<sup>[11]</sup>), the Direction Group's assessment that the founding criteria "didn't have much effect" ([P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[12]</sup>), and the absence of any implementation-experience requirement ([P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2274r0.pdf)<sup>[13]</sup>).

The alternative was in the room. The architect of the Networking TS championed it at the October 2021 telecon ([P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[8]</sup>). A Neutral voter on Poll 4 stated the historical lesson in the published record: "We've tried inventing networking before pursuing ASIO, and that effort didn't succeed."

The warnings were in writing, before the vote. [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf)<sup>[27]</sup> documented the compound-results problem two months before the polls; [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf)<sup>[8]</sup> warned of limited field experience the week the polls opened.

The repair bill is paid from the institution's own scarcest resource. [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> documents the review-bandwidth collapse from public sources. The years 2019 and 2024 each produced more than 900 paper documents, approaching the paper output of the entire eight-year C++98 cycle. LEWG's own accounting in [P2400R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r2.html)<sup>[49]</sup> records 74 telecons and 107 papers reviewed in roughly seventeen months against a standing backlog of 41 active papers. [P3443R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3443r0.pdf)<sup>[50]</sup> measured one study group's docket: of the 41 papers that received binding polls, 56.10 percent were published less than one week before they were discussed and polled. [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> states the finding: "The standard does not ship late. It ships less-reviewed." The correction ledger of Section 4.5 consumes exactly that bandwidth.

The wound is also re-inflicted. [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> records `std::linalg`, adopted on the strongest existing-practice pedigree available, accumulating fix papers against its own facility before any vendor ships it, with LWG deleting one function entirely: "If somebody cares sufficiently, they can propose it back for C++29 ..."

The principles, the alternative, the warnings, and the repair costs are each in the institution's own documents, dated at or before the decision.

---

## 8. Objections

This section states the expected objections in their strongest form and answers each from the evidence already presented.

**"The sender model had production deployment before the vote."** It did, and Section 4.2 presents it: Facebook products in production, NVIDIA GPU dispatch, Bloomberg experimentation ([P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf)<sup>[24]</sup>). None of it was networking, and the production deployments were at the design authors' own employers - the configuration the field-experience principle names as insufficient ([P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf)<sup>[16]</sup>). The Poll 2 comment record includes voters who supported the direction while declining to judge networking (Section 4.3).

**"The coroutine executor concept did not exist in 2021."** It did not, and the author's [P4096R1](https://isocpp.org/files/papers/P4096R1.pdf)<sup>[3]</sup> says so: "The coroutine executor concept did not exist in 2021. [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html)<sup>[51]</sup> could not have evaluated it." The finding is not that the 2021 analysis was wrong about `execute(F&&)`. The finding is that the process "had no mechanism to verify that the analysis examined every applicable framing, and no mechanism to revisit the outcome against evidence." The concept now exists, is implemented on three platforms ([P4003R3](https://isocpp.org/files/papers/P4003R3.pdf)<sup>[52]</sup>), and the guidance has not been revisited.

**"The marketplace pipeline works - std::format came from {fmt}."** It did, and [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> presents `std::format` as the strongest admission of the modern era: adopted after six and a half years of field deployment, with the author driving. The same record shows the best case still pays the Penalty - `std::print` arrived nine years after `{fmt}` had it, named arguments remain absent - and concludes: "That shortfall is the floor of the Penalty rather than its ceiling." Adopting a marketplace verdict is the pipeline working. The October 2021 decision was the other kind: a contemporaneous choice against a deployed alternative.

**"The Alliance competes with the standard library and profits from this finding."** The stake is real and is disclosed in Section 2. Every load-bearing claim in this paper rests on a primary public source: the poll outcomes, the published papers, the vendor status pages, the public repositories. Where the author's own analytical frameworks appear - the Standardization Penalty in Sections 7 and 9 - they are named as the author's own, and the conclusion rests on the record if the frameworks are rejected entirely.

**"The guidance left the door open to other models."** The Poll 4 chair comment says so: "Work on networking using other models will still be reviewed and considered on its own merits." The same guidance required "compelling new information" to convince the "grand unified model" contingent - the burden of proof sat on the challenger of the adopted model, not on the model. The five years since are the evidence of how that burden worked in practice.

Each objection, stated at its strongest, is answered by the record already presented.

---

## 9. What Would Restore Confidence

This section states the conditions under which the finding of this paper would no longer hold. They are procedural, they are falsifiable, and they are stated as information, not as requests.

The first condition is a revisit mechanism for direction-setting decisions. [P4096R1](https://isocpp.org/files/papers/P4096R1.pdf)<sup>[3]</sup> records that the 2021 guidance was set with "no mechanism to revisit the outcome against evidence." A published trigger - a date, a shipping criterion, a deployment threshold at which the guidance is re-examined against the record - is the mechanism whose absence the record documents.

The second condition is an admission gate that prices the freeze. [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf)<sup>[7]</sup> proposes the instruments: the GitHub Test (what does standardization deliver that downloading the library does not), the Standardization Penalty (the immediate loss of evolutionary capacity on entry), and a requirement that a proposal price both before admission. [P3001R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p3001r0.html)<sup>[15]</sup> already states the freeze to proposal authors: "as soon as something is standardized, it is essentially done."

The third condition is a field-evidence requirement with teeth: positive feedback from users outside the proposing organization, per the principle formulated in [P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf)<sup>[16]</sup>.

The falsification condition is plain. If sender-based networking ships and independent users adopt it over the deployed alternatives, the finding of this paper fails.

The conditions are procedural, falsifiable, and cost the committee nothing its own documents do not already promise.

---

## 10. Conclusion

The record assembled here is the committee's own. The founding documents stated the existing-practice principle, and the Direction Group recorded that it had little effect. The October 2021 polls redirected networking toward a model for which no networking proposal existed, over a deployed alternative, with the warnings published before the vote. The correction ledger accumulated before any vendor shipped the design - twenty-four post-adoption items modified the sender sub-language or its integration, and zero modified coroutines - and the ledger grows in the current mailing. The standard coroutine task type carries a second template parameter that the ecosystem's independent task types do not, imposed by a model whose home domain is elsewhere.

The C++ Alliance does not have confidence that WG21, with its current delegate population and ruleset, can deliver coroutine-only I/O to the standard without alterations that materially harm users. The churn documented in Section 4.5 is what standardizing an invented novelty costs. The Alliance does not have confidence that the committee can deliver networking based on senders and receivers in a form that will resonate with ordinary users of C++.

The Alliance concludes that users are best served by library components that compete fairly in the marketplace, without being designed in place by committee. The Alliance will continue to develop Capy and Corosio, to publish field reports, and to provide information to the committee. The conditions under which confidence would be restored appear in Section 9.

What is built next is built by the delegates who read the record and by the users who choose their libraries.

---

## Disclosure

The author provides information and serves at the pleasure of the committee.

The author maintains [Boost.Beast](https://github.com/boostorg/beast) and founded the [C++ Alliance](https://cppalliance.org/), which develops [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio). The Alliance's libraries compete in the marketplace this paper examines. When this paper compares standard library components with marketplace alternatives, the author's stake is direct. The reader should weigh every claim in this paper with that bias in mind. Every quotation is attributed.

This paper documents the public record on the sender model's development, adoption, and correction history, and states the Alliance's confidence finding. It proposes no changes to any working paper.

One genuine limitation: the paper's absence claims - no published sender-based networking deployment, no published `IoEnv` design - are bounded by the public record. Committee discussions occur in rooms, hallways, and private channels that leave no public trace. Evidence may exist that the author's search did not reach. A reader aware of a published document, deployment, or prototype that this paper's research did not reach is welcomed to send the correction, and the record will be updated in a future revision.

This paper is a companion to the Network Endeavor series ([P4100R1](https://isocpp.org/files/papers/P4100R1.pdf)<sup>[53]</sup>) and draws on the author's prior analyses, each identified as the author's own work where it is introduced.

Methodology: every quotation was verified character-for-character against its source, and every absence claim carries its search method. Quotations are transcribed with straight quotation marks and apostrophes; obvious typographical errors in sources are corrected. Research notes with per-quote provenance are available on request.

This paper was prepared with AI assistance for research, drafting, and verification. The author reviewed and stands behind every word.

This paper asks for nothing.

---

## Acknowledgements

**Gor Nishanov** - the C++20 coroutine machinery and its explicit layering model, which this paper cites as the design intent for task-type diversity.

**Christopher Kohlhoff** - Boost.Asio, the Networking TS, and [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf)<sup>[27]</sup>, which documented the compound-results problem before the October 2021 polls.

**The authors of [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html)<sup>[9]</sup>** - the design this paper examines. The structured concurrency guarantees and the completion channel model defined the vocabulary the coroutine-native work builds on.

**Dietmar K&uuml;hl** - [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html)<sup>[35]</sup>, [P2762R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r2.pdf)<sup>[29]</sup>, and `beman::execution`, and for collecting the task issues himself in [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html)<sup>[54]</sup>.

**Jonathan M&uuml;ller** - [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html)<sup>[42]</sup>, documenting the symmetric transfer gap, and the St. Louis trip report recording the adoption margin.

**Eric Niebler** - [P3826R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r3.html)<sup>[34]</sup>, whose candor about the state of the design is on the public record.

**Bryce Adelstein Lelbach, Fabio Fracassi, and Ben Craig** - the published poll outcomes in [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html)<sup>[25]</sup>, without which Section 4.3 could not exist.

**Robert Leahy** - [P4373R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4373r0.pdf)<sup>[36]</sup> in the current mailing.

**Michael Wong** - [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf)<sup>[48]</sup>, the SG14 priority list.

**Steve Gerbino and Mungo Gill** - co-development of Capy and Corosio, and co-authorship of the bridge papers.

---

## References

[1] [P4089R1](https://isocpp.org/files/papers/P4089R1.pdf) - "On the Diversity of Coroutine Task Types" (Vinnie Falco, 2026).

[2] [P4097R1](https://isocpp.org/files/papers/P4097R1.pdf) - "The Networking Claim and P2453R0" (Vinnie Falco, 2026).

[3] [P4096R1](https://isocpp.org/files/papers/P4096R1.pdf) - "Coroutine Executors and P2464R0" (Vinnie Falco, 2026).

[4] [P4099R1](https://isocpp.org/files/papers/P4099R1.pdf) - "The Twenty-One Year Networking Arc" (Vinnie Falco, 2026).

[5] [P4123R0](https://isocpp.org/files/papers/P4123R0.pdf) - "The Cost of Senders for Coroutine I/O" (Vinnie Falco, 2026).

[6] [P4041R0](https://isocpp.org/files/papers/P4041R0.pdf) - "Is `std::execution` a Universal Async Model?" (Vinnie Falco, 2026).

[7] [P4133R0](https://isocpp.org/files/papers/P4133R0.pdf) - "Should WG21 Even See This Paper? Admission Gates for Library and Language Proposals" (Vinnie Falco, 2026).

[8] [P2469R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2469r0.pdf) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not." (Jamie Allsop, Vinnie Falco, Richard Hodges, Christopher Kohlhoff, Klemens Morgenstern, 2021).

[9] [P2300R10](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p2300r10.html) - "std::execution" (Micha&lstrok; Dominiak, Georgy Evtushenko, Lewis Baker, Lucian Radu Teodorescu, Lee Howes, Kirk Shoop, Michael Garland, Eric Niebler, Bryce Adelstein Lelbach, 2024).

[10] [N1810](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1810.html) - "Library Extension TR2 Call for Proposals" (Howard Hinnant, Beman Dawes, Matt Austern, 2005).

[11] [N3370](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3370.html) - "Call for Library Proposals" (Alisdair Meredith, 2012).

[12] [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf) - "Direction for ISO C++" (Beman Dawes, Howard Hinnant, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2018).

[13] [P2274R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2274r0.pdf) - "C and C++ Compatibility Study Group" (Aaron Ballman, 2020).

[14] [P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.pdf) - "Direction for ISO C++" (Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2022).

[15] [P3001R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p3001r0.html) - "std::hive and containers like it are not a good fit for the standard library" (Jonathan M&uuml;ller, Zach Laine, Bryce Adelstein Lelbach, David Sankel, 2023).

[16] [P4046R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4046r0.pdf) - "SAGE: Saving All Gathered Expertise" (Vinnie Falco, 2026).

[17] [P4088R1](https://isocpp.org/files/papers/P4088R1.pdf) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026).

[18] [N1925](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2005/n1925.pdf) - "Networking proposal for TR2 (rev. 1)" (Gerhard Wesp, 2005).

[19] [P4094R1](https://isocpp.org/files/papers/P4094R1.pdf) - "The Unification of Executors and P0443" (Vinnie Falco, 2026).

[20] [P1791R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1791r0.html) - "Evolution of the P0443 Unified Executors Proposal to accommodate new requirements" (Christopher Kohlhoff, Jamie Allsop, 2019).

[21] [P1525R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1525r0.pdf) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019).

[22] [P4095R1](https://isocpp.org/files/papers/P4095R1.pdf) - "The Basis Operation and P1525" (Vinnie Falco, 2026).

[23] [P4014R2](https://isocpp.org/files/papers/P4014R2.pdf) - "The Sender Sub-Language For Beginners" (Vinnie Falco, Mungo Gill, 2026).

[24] [P2470R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2470r0.pdf) - "Slides for presentation of P2300R2: std::execution (sender/receiver)" (Eric Niebler, 2021).

[25] [P2453R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2453r0.html) - "2021 October Library Evolution and Concurrency Networking and Executors Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[26] [P2400R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2400r3.html) - "Library Evolution Report: 2021-09-28 to 2022-01-25" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[27] [P2430R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2430r0.pdf) - "Partial success scenarios with P2300" (Christopher Kohlhoff, 2021).

[28] [P2762R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r0.pdf) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023).

[29] [P2762R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2762r2.pdf) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023).

[30] [r/cpp Kona 2023 trip report](https://www.reddit.com/r/cpp/comments/17vnfqq/) - "2023-11 Kona ISO C++ Committee Trip Report" (2023).

[31] [P4125R1](https://isocpp.org/files/papers/P4125R1.pdf) - "Coroutine-Native I/O at a Derivatives Exchange" (Mungo Gill, 2026).

[32] [P3187R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3187r1.pdf) - "remove ensure_started and start_detached from P2300" (Kirk Shoop, Lewis Baker, 2024).

[33] [Trip Report: Summer ISO C++ Meeting in St. Louis, USA](https://www.think-cell.com/en/career/devblog/trip-report-summer-iso-cpp-meeting-in-st-louis-usa) (Jonathan M&uuml;ller, 2024).

[34] [P3826R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p3826r3.html) - "Fix Sender Algorithm Customization" (Eric Niebler, 2026).

[35] [P3552R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r3.html) - "Add a Coroutine Task Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[36] [P4373R0](https://isocpp.org/files/papers/P4373R0.pdf) - "Why Did You Stop?" (Robert Leahy, 2026).

[37] [P3552R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3552r0.pdf) - "Add a Coroutine Lazy Type" (Dietmar K&uuml;hl, Maikel Nadolski, 2025).

[38] [P0975R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0975r0.html) - "Impact of coroutines on current and upcoming library facilities" (Gor Nishanov, 2018).

[39] [P1362R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1362r0.pdf) - "Incremental Approach: Coroutine TS + Core Coroutines" (Gor Nishanov, 2018).

[40] [nvexec/stream/common.cuh](https://github.com/NVIDIA/stdexec/blob/main/include/nvexec/stream/common.cuh) - NVIDIA stdexec GPU stream environment queries (2026).

[41] [P4007R3](https://isocpp.org/files/papers/P4007R3.pdf) - "Open Issues in `std::execution::task`" (Vinnie Falco, Mungo Gill, 2026).

[42] [P3801R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3801r0.html) - "Concerns about the design of `std::execution::task`" (Jonathan M&uuml;ller, 2025).

[43] [NVIDIA/stdexec issue 2047](https://github.com/NVIDIA/stdexec/issues/2047) - "Another crash with stdexec::task (again probably premature coro destruction)" (2026).

[44] [P4090R1](https://isocpp.org/files/papers/P4090R1.pdf) - "Sender I/O: A Constructed Comparison" (Vinnie Falco, Steve Gerbino, 2026).

[45] [P4091R1](https://isocpp.org/files/papers/P4091R1.pdf) - "Error Models of Regular C++ and the Sender Sub-Language" (Vinnie Falco, 2026).

[46] [P4092R1](https://isocpp.org/files/papers/P4092R1.pdf) - "Consuming Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[47] [P4093R1](https://isocpp.org/files/papers/P4093R1.pdf) - "Producing Senders from Coroutine-Native Code" (Vinnie Falco, Steve Gerbino, 2026).

[48] [P4029R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4029r0.pdf) - "The SG14 Priority List for C++29/32" (Michael Wong, 2026).

[49] [P2400R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r2.html) - "Library Evolution Report: 2021-06-01 to 2021-09-20" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, et al., 2021).

[50] [P3443R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3443r0.pdf) - "Reflection on SG21's 2024 Process" (Ran Regev, 2024).

[51] [P2464R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2464r0.html) - "Ruminations on networking and executors" (Ville Voutilainen, 2021).

[52] [P4003R3](https://isocpp.org/files/papers/P4003R3.pdf) - "A Minimal Coroutine Execution Model" (Vinnie Falco, Steve Gerbino, Mungo Gill, 2026).

[53] [P4100R1](https://isocpp.org/files/papers/P4100R1.pdf) - "Coroutine-Native I/O for C++29 (The Network Endeavor)" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026).

[54] [P3796R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3796r1.html) - "Coroutine Task Issues" (Dietmar K&uuml;hl, 2025).
