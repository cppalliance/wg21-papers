| Document | D0000 |
|----------|-------|
| Date:       | 2026-01-01
| Reply-to:   | Vinnie Falco \<vinnie.falco@gmail.com\>
| Audience:   | WG21

---

# WG21: A Dying Tradition of Knowledge

## Abstract

WG21 began as a small group of homogeneous experts who shared implicit engineering knowledge—deep systems backgrounds, practical implementation experience, and familiarity with the standard's wording. This culture worked when the committee was small. But as WG21 expanded over thirty years, it failed to develop social technology for transmitting this knowledge to newcomers. Structural changes—splitting working groups into Evolution and Wording—institutionalized the separation of expertise from authority. And while WG21 has created documentation, that documentation transmits *conclusions* rather than *judgment*.

The result is a dying tradition of knowledge. This paper analyzes WG21's cultural transmission failure through the lens of Great Founder Theory and proposes mechanisms for preserving the committee's engineering principles before the founding generation is gone.

---

## 1. The Committee We Inherited

C++ is infrastructure. It runs your phone, your car, your bank, your hospital. The language that powers civilization's critical systems deserves a standards committee that can maintain it for generations.

For a time, WG21 was that committee.

### 1.1 How It Worked

When C++ standardization began in 1990-91, the committee comprised a small, tight-knit group organized into two working groups: the [Core Working Group (CWG)](https://isocpp.org/std/the-committee) for language features and the [Library Working Group (LWG)](https://isocpp.org/std/the-committee) for the standard library.

- **Shared background**: Deep systems programming experience, often from Bell Labs, AT&T, or similar environments
- **Shared knowledge**: Everyone understood templates, memory models, and low-level systems concerns
- **Small standard**: The entire document was manageable—participants could hold it in their heads
- **Unified expertise**: The same people who evaluated designs also crafted the wording

When Bjarne Stroustrup, Andrew Koenig, or Alex Stepanov made design decisions, the reasoning was understood by their peers without explicit justification. The committee functioned as what Great Founder Theory calls a **living tradition of knowledge**:

> *"A living tradition of knowledge is a tradition whose body of knowledge has been successfully transferred, i.e., passed on to people who comprehend it."*

### 1.2 What Changed

As the committee grew, WG21 reorganized. The original two groups became four:

| Original Structure | New Structure |
|-------------------|---------------|
| Core Working Group (CWG) | Evolution Working Group (EWG) → CWG |
| Library Working Group (LWG) | Library Evolution Working Group (LEWG) → LWG |

The [Evolution Working Group (EWG)](https://isocpp.org/std/the-committee) and [Library Evolution Working Group (LEWG)](https://isocpp.org/std/the-committee) now handle design decisions. The original CWG and LWG became "wording groups," translating approved designs into standardese.

This split created a critical problem: **designs freeze when they move from Evolution to Wording**. Once EWG or LEWG approves a design, CWG or LWG can only accept or reject it—they cannot modify it. If they identify a flaw, they must [send it back](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.html). They are [not permitted to fix it](https://isocpp.org/std/the-committee).

But the wording groups contain the experts who understand:
- How features interact with existing language mechanisms
- Which designs have caused problems historically
- The subtle implications of specification choices

Great Founder Theory identifies this as a fundamental error—**separating skill from power**:

> *"The succession problem has two components: power succession (handing off the reins of the institution, keeping it piloted) and skill succession (transferring the skill needed to pilot the institution well, keeping it a live player)."*

The split achieved power succession (new groups have authority) while breaking skill succession (authority moved away from expertise).

### 1.3 How the Split Accelerates Decay

**Evolution groups are more accessible.** You can participate in EWG or LEWG with ideas and enthusiasm. You don't need deep knowledge of the standard's wording or historical interactions. This **selects for** participants who lack the tacit knowledge that once guided design decisions:

> *"Bureaucracies ameliorate the problem of talent and alignment scarcity... Bureaucrats are expected to act according to a script, or a set of procedures—and that's it."*

**Expertise is bypassed, not consulted.** The experts in CWG and LWG see proposals only after design decisions are locked. When they identify problems, bureaucratic friction discourages correction. Sending a proposal back means restarting the process, so marginal designs advance because "the process has momentum."

**Natural mentorship is broken.** Originally, newcomers engaged with experts directly—the same people evaluating designs also knew the wording. The split broke this. Now newcomers can participate in Evolution without ever deeply engaging with standardese experts:

> *"Traditional master-apprentice relationships are the gold standard for these training relationships... Otherwise, the knowledge simply isn't transferred, and with many crafts, is lost forever."*

### 1.4 Growth Without Discernment

WG21 has grown from dozens to hundreds of active participants. This growth was not accompanied by mechanisms to ensure new participants understand the committee's engineering principles.

The organization actively solicits new volunteers with an inclusive "everyone welcome" policy. There are no skill checks, no evaluation of whether newcomers understand principles, no gatekeeping by masters. Anyone can attend meetings, submit papers, and vote on decisions that will affect millions of developers for decades.

The inclusive policy was well-intentioned—democratize standardization, bring fresh perspectives. But from a Great Founder Theory perspective, it inverts how living traditions preserve themselves:

> *"Standardized education is useful because, among other things, it is easily scalable, but standardized methods of education... tend to produce counterfeit understanding because education is too complex to be easily standardized."*

Living traditions require masters who evaluate understanding. Inclusive policies remove the evaluation mechanism. More participants means each one gets less mentorship. The committee optimized for *quantity* of participation when it should have optimized for *quality* of knowledge transmission.

Today, [WG21 comprises over 20 subgroups](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4999.html)—each with its own culture, participants, and implicit norms. The [2024 Convener's Report](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4990.pdf) describes this as enabling "each independent work item to progress at its own speed." But proliferation of subgroups makes coherent transmission of founding principles nearly impossible.

---

## 2. What WG21 Has Built

Before diagnosing failure, we must acknowledge what exists. WG21 has created substantial documentation. The question is what that documentation transmits.

### 2.1 The Documentation Inventory

**Procedural Documents** (how the committee operates):

| Document | Content | Knowledge Transmitted |
|----------|---------|----------------------|
| [SD-3: Study Group Organizational Information](https://isocpp.org/std/standing-documents/sd-3-study-group-organizational-information) | How to form SGs, reporting requirements | Procedure only |
| [SD-4: WG21 Practices and Procedures](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) | Code of conduct, consensus building, voting | Procedure only |
| [SD-5: Meeting Information](https://isocpp.org/std/standing-documents/sd-5-meeting-information) | Dates, locations, mailing deadlines | Logistics only |
| [SD-7: Mailing Procedures and How to Write Papers](https://isocpp.org/std/standing-documents/sd-7-mailing-procedures-and-how-to-write-papers) | Document numbers, formatting, submission | Formatting only |
| [How to Submit a Proposal](https://isocpp.org/std/submit-a-proposal) | Float idea, use template, iterate, present | Process steps only |
| [Meetings and Participation](https://isocpp.org/std/meetings-and-participation) | How to join, national bodies, email lists | Access only |

**Policy Documents** (design decisions the committee has made):

| Document | Content | Knowledge Transmitted |
|----------|---------|----------------------|
| [SD-8: Standard Library Compatibility](https://isocpp.org/std/standing-documents/sd-8-standard-library-compatibility) | What breaking changes WG21 reserves | Conclusions, not reasoning |
| [SD-9: Library Evolution Policies](https://isocpp.org/std/standing-documents/sd-9-library-evolution-policies) | Default positions on `[[nodiscard]]`, `noexcept`, `explicit` | Conclusions, not reasoning |
| [SD-10: Language Evolution Principles](https://isocpp.org/std/standing-documents/sd-10-language-evolution-principles) | References D&E, compatibility, zero-overhead | **Partial**: References principles but briefly |

**Direction Documents** (high-level philosophy):

| Document | Content | Knowledge Transmitted |
|----------|---------|----------------------|
| [P2000: Direction for ISO C++](https://wg21.link/P2000) | Philosophy, priorities, "buckets" | Vision, not evaluation skills |
| [P0592: Bold Overall Plan](https://wg21.link/P0592) | Feature roadmaps per standard | Planning, not principles |

**Onboarding**:

| Mechanism | Content | Knowledge Transmitted |
|-----------|---------|----------------------|
| Sunday evening orientation | Hotel lobby meetup, room navigation | Logistics only |
| std-proposals mailing list | Unstructured feedback from experienced members | Implicit, unverified |
| Study Group participation | Learning by observation | Implicit, unverified |

### 2.2 The Critical Gap

The documentation has a pattern: **WG21 transmits conclusions but not judgment**.

Consider SD-9, which says things like "use `[[nodiscard]]` for functions where ignoring the return value is always a bug." This is a *conclusion*—a design decision. It doesn't teach:
- How to recognize such functions
- How to make this judgment in ambiguous cases  
- The underlying principle (error handling philosophy, RAII patterns)

SD-10 comes closest to real knowledge transfer by referencing "Design and Evolution of C++" principles. But:
- The references are brief, not elaborated
- Newcomers may not have read D&E
- No explanation of how to apply principles to novel cases

P2000 articulates philosophy—valuable for understanding committee goals. But it doesn't teach *how to evaluate* whether a proposal meets those goals.

**What's completely missing:**

1. **"What Belongs in the Standard" Document** — No explicit criteria for evaluating whether a feature should be standardized. No guidance distinguishing "useful" from "belongs."

2. **Design Judgment Training** — SD-9 says "use nodiscard when..." but doesn't teach *how to think* about API design. No document explains *why* certain historical features failed.

3. **Formal Mentorship** — No pairing of newcomers with experienced members. No structured learning path. No evaluation of understanding.

4. **Verification** — Anyone can vote after navigating procedure. No demonstration of understanding required.

This is the signature of a dying tradition: **the external forms persist while the comprehension fades**.

---

## 3. The Diagnosis

Great Founder Theory distinguishes three states of knowledge traditions:

1. **Living tradition**: Knowledge successfully transferred with understanding
2. **Dead tradition**: External forms transferred, but not comprehension
3. **Lost tradition**: Not transferred at all

WG21 exhibits symptoms of a **dead tradition**:

> *"A dead tradition of knowledge is a tradition whose body of knowledge has been unsuccessfully transferred, i.e., its external forms, its trappings such as written texts have been transferred, but not the full understanding of how to carry out this tradition of knowledge as practiced."*

New participants can navigate the paper process, write proposals in the correct format, present at meetings. But many cannot distinguish what belongs in the standard library from what doesn't, apply the implicit engineering principles that guided early decisions, or recognize when a proposal violates foundational design philosophy.

This is **counterfeit understanding**:

> *"Students of a tradition can appear to possess understanding of a tradition's body of knowledge despite actually lacking it. This is counterfeit understanding. This can happen if students merely reproduce the teacher's statements without understanding the underlying knowledge."*

### 3.1 What Living Traditions Require

Great Founder Theory identifies mechanisms that keep traditions alive:

**Verification mechanisms** allow practitioners to check their work:

> *"Scholars and practitioners in a body of knowledge will often use discrete techniques or mechanisms to verify their work for accuracy."*

WG21 lacks this. There's no checklist asking: Does this solve a coordination failure? Can this be distributed without standardization? What's the perpetual maintenance cost?

**Generating principles** enable extension of the tradition:

> *"Someone who understands the generating principles of a tradition will be able to verify or check their knowledge, but, more importantly, they will also be able to extend it while remaining faithful to the original body of knowledge."*

The generating principles of C++ standardization—why certain things belong and others don't—are not documented anywhere. They exist only in the minds of founding-era participants.

**Error correction** addresses inevitable transmission mistakes:

> *"Errors in transmission from one generation to the next are almost guaranteed and thus require proactive measures to correct them and maintain the fidelity of a tradition."*

When newcomers misunderstand principles, there's no correction mechanism. They proceed, submit papers, and vote based on incorrect understanding.

### 3.2 The Succession Crisis

WG21 shows:

- **Power succession working**: Convener position has transitioned, chairs rotate, meetings happen
- **Skill succession failing**: The tacit knowledge of good standardization is not transferring

This produces characteristic dysfunction:

> *"If power succession is successful but skill succession is not, then the institution remains piloted, but not a live player. Someone is at the controls, but they don't really know how to use them."*

WG21 is piloted—meetings happen, papers progress, standards ship. But it is not a live player—it cannot adapt, cannot fix mistakes efficiently, cannot prevent poor decisions from accumulating.

---

## 4. What WG21 Must Do

The solution is to make implicit culture explicit. The founding generation still walks among us. Their knowledge can be captured—but not forever.

### 4.1 Document the Generating Principles

Write down what the founding generation understood implicitly:

**Library Inclusion Criteria**
- What coordination failures justify standardization?
- When is an external library sufficient?
- What perpetual costs does standardization impose?
- How do we evaluate vocabulary necessity vs utility convenience?

**Design Philosophy**
- What is the relationship between performance and interface standardization?
- When do we prioritize theoretical consistency vs practical utility?
- How do we balance backwards compatibility against fixing mistakes?

**Paper Evaluation**
- What questions should every paper answer?
- What evidence demonstrates genuine demand?
- How do we distinguish proposer-driven from user-driven proposals?

These principles exist implicitly. They must be written down—not as rules to be gamed, but as frameworks for discussion.

### 4.2 Establish Real Onboarding

The Sunday orientation tells newcomers where the rooms are. It should tell them what WG21 values.

New participants should receive:

1. **Philosophy materials** explaining the committee's purpose and principles
2. **Mentor assignment** from experienced participants who actively teach
3. **Orientation session** covering design principles, not just logistics
4. **Feedback on early participation** specifically addressing principle understanding

This creates the master-apprentice relationships that transfer tacit knowledge:

> *"Since it cannot be easily transferred via texts, tacit knowledge must be taught via direct practice and extensive interaction with a skilled practitioner."*

### 4.3 Create Verification Mechanisms

Every paper should be evaluated against explicit criteria:

**Before LEWG/EWG**
- What coordination failure does this solve?
- What's the perpetual maintenance burden?
- Why is standardization the right distribution mechanism?
- What production experience validates the design?

**Before Plenary**
- Has the paper been evaluated against engineering principles?
- Do opponents' concerns reflect genuine principle violations?
- Are we standardizing because the proposal is good, or because the process has momentum?

### 4.4 Reunify Expertise and Authority

The structural split should be reconsidered. At minimum:

- Experts from CWG/LWG should have formal roles in EWG/LEWG design discussions
- The "design freeze" rule should be relaxed to allow wording groups to propose design improvements
- Cross-pollination between groups should be actively encouraged

> *"Ensuring the institution acquires this new, skilled pilot is the succession problem... If neither part of the succession problem is handled, then the institution becomes unpiloted and a dead player."*

### 4.5 Build Oral Tradition

Some knowledge cannot be fully written. WG21 needs:

- **Stories** about past decisions and their rationale
- **Case studies** of proposals correctly rejected
- **Post-mortems** on standardized features that proved problematic
- **Regular discussion** of principles, not just proposals

### 4.6 Enable Course Correction

A live institution can fix mistakes. WG21's process makes this nearly impossible. The committee should:

- Create lightweight mechanisms for addressing recognized usability problems
- Establish retrospective processes that evaluate past decisions
- Accept that removing features demonstrates institutional health, not failure

---

## 5. The Stakes

WG21 has perhaps ten years before the founding generation is largely gone. Stroustrup, Koenig, Stepanov—the people who understood what C++ standardization was *for*—are not getting younger. Their implicit knowledge is the committee's most valuable asset, and it is depreciating daily.

Without action:

- **Knowledge loss accelerates** as founding-era participants retire
- **Counterfeit understanding spreads** among newer participants who know forms but not substance
- **Bad decisions compound** without correction mechanisms
- **Structural barriers** keep expertise from informing design

Great Founder Theory is clear:

> *"Over time, functional institutions decay. As the landscape of founders and institutions changes, so does the landscape of society."*

The fix is not mysterious. Write down your principles. Teach them to newcomers. Verify that learning has occurred. Reunify expertise with authority. Enable correction when mistakes are made.

C++ has earned this. The language that runs the world's infrastructure deserves a committee that can maintain it for generations. The founding generation built something remarkable. Whether it survives them depends on what WG21 does now.

Make the implicit explicit. Or watch the tradition die.

---

## Acknowledgements

This analysis draws on Samo Burja's Great Founder Theory, which provides the conceptual framework for understanding institutional decay and knowledge transmission. The structural analysis of WG21's Evolution/Wording split emerged from conversations with long-time committee participants who observed these changes firsthand.

---

## References

### Great Founder Theory

- Burja, Samo. [Great Founder Theory](https://www.samoburja.com/gft/). 2020.

### WG21 Structure and Participation

- ISO C++ Committee. [The Committee](https://isocpp.org/std/the-committee). Description of WG21 structure and subgroups.
- ISO C++ Committee. [Meetings and Participation](https://isocpp.org/std/meetings-and-participation). How to participate in WG21.
- ISO C++ Committee. [How to Submit a Proposal](https://isocpp.org/std/submit-a-proposal). Guide for newcomers.

### Standing Documents

- [SD-3: Study Group Organizational Information](https://isocpp.org/std/standing-documents/sd-3-study-group-organizational-information). Formation and operation of Study Groups.
- [SD-4: WG21 Practices and Procedures](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures). Operational practices, consensus, proposal handling.
- [SD-5: Meeting Information](https://isocpp.org/std/standing-documents/sd-5-meeting-information). Schedules, mailing deadlines, logistics.
- [SD-7: Mailing Procedures and How to Write Papers](https://isocpp.org/std/standing-documents/sd-7-mailing-procedures-and-how-to-write-papers). Document formatting and submission.
- [SD-8: Standard Library Compatibility](https://isocpp.org/std/standing-documents/sd-8-standard-library-compatibility). Breaking change policies.
- [SD-9: Library Evolution Policies](https://isocpp.org/std/standing-documents/sd-9-library-evolution-policies). Default design policies.
- [SD-10: Language Evolution Principles](https://isocpp.org/std/standing-documents/sd-10-language-evolution-principles). EWG design principles.

### Direction Papers

- Stroustrup, Hinnant, Orr, Vandevoorde, Wong. [P2000: Direction for ISO C++](https://wg21.link/P2000). Committee philosophy and priorities.
- Voutilainen, Ville. [P0592: Bold Overall Plan](https://wg21.link/P0592). Feature roadmaps.

### Committee Reports

- WG21. [N4990: WG21 2023-2024 Convener's Report](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4990.pdf). Committee structure and workflow.
- WG21. [N4999: WG21 Active Subgroups](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4999.html). Current study groups and working groups.

### Process Documentation

- Bastien, JF; Revzin, Barry. [P2138R4: Rules of Design \<=> Wording engagement](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.html). Defines the separation between Evolution and Wording group responsibilities.

---

## Notes

Unattributed quotes are from *Great Founder Theory* by Samo Burja.

---

## Revision History

- R0 (2025-01-01): Initial version
