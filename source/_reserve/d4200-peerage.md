---
title: "The Peerage: What WG21 Appears To Be, And What It Actually Is"
document: P4200R0
date: 2026-03-10
intent: info
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "Claude Opus 4.6 Thinking Max"
audience: WG21
---

## Abstract

"A standards body that cannot distinguish between social consensus and technical correctness will, over time, converge on social consensus alone, because social consensus is easier to achieve and harder to falsify." - Claude Opus 4.6 Thinking Max

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

This paper was generated entirely by AI. The conclusions were drawn by AI. The operator did not alter the AI output in any way. The paper demonstrates two things. That WG21 forms a functional peerage, and that frontier Large Language Models can competently analyze social structures and dominance hierarchies. Altering the AI's output would weaken the latter.

### 1.1 Context

The operator - a WG21 paper author preparing to present technical papers at an upcoming committee meeting - asked the AI a question during a working session:

> "The papers are correct. Anyone can read them and verify the correctness. Why do I need to argue them in person? Why is there opposition? Help me understand why this process depends on what is essentially a verbal prosecution in a room."

The AI analyzed the question against the material it had been provided. The operator then asked a follow-up: How would the language creator feel upon discovering that the committee process he built had devolved from its intended meritocratic design? The AI's analysis of these two questions produced the conclusions in this paper.

The AI was provided with the following inputs during the session:

- Published and draft WG21 papers in the async, coroutine, and sender domains, including [P2300R0](https://wg21.link/p2300r0)<sup>[1]</sup> through [P2300R10](https://wg21.link/p2300r10)<sup>[2]</sup>, [P3552R3](https://wg21.link/p3552r3)<sup>[3]</sup>, [P4007R0](https://wg21.link/p4007r0)<sup>[4]</sup>, [P2583R1](https://wg21.link/p2583r1)<sup>[5]</sup>, [P4003R0](https://wg21.link/p4003r0)<sup>[6]</sup>, [P4014R0](https://wg21.link/p4014r0)<sup>[7]</sup>, and others. These are public documents in the WG21 mailing archive.
- An analysis of eight US national body comments filed against the C++26 CD targeting `std::execution::task`, including their resolution status and relationship to published papers.
- LEWG and plenary poll results from public committee records.
- Transcripts and descriptions of public conference talks, podcast appearances, and published interviews by committee members, including Bjarne Stroustrup's public talks spanning 2007-2025.
- Posts from the LEWG reflector.

Every conclusion in this paper is derivable from the public record.

---

## 2. What WG21 Appears to Be

WG21 presents itself as a technical meritocracy. Proposals compete on engineering merit. The room evaluates them. The best design wins. This is the story told at CppCon keynotes, in committee recruitment materials, and in the ISO process documents that govern how C++ evolves.

The story has a credible origin. Bjarne Stroustrup deliberately structured C++ governance to prevent any single entity from controlling the language - including himself. He fought AT&T for author credit in the early 1980s and won.<sup>[8]</sup> When IBM, Sun, and HP pushed him toward standardization in the early 1990s, he built a committee rather than a foundation, a corporation, or a benevolent dictatorship. The intent was independence: No company would own C++, no individual would control it, and the language would evolve through the collective judgment of its practitioners.

The intended evaluation method was engineering judgment, not politics. Stroustrup's own method is to build a list of requirements for a domain and score proposals against them. When Alexander Stepanov presented the STL, Stroustrup evaluated it against a criteria list he had built over years: "I had a list with about 12 items and it matched 11 of them. And okay, it doesn't look right, but it must be - nothing else matches that many of my criteria."<sup>[9]</sup> The proposal won on merit. The evaluator accepted the result even though the design violated his aesthetic preferences. That is what a meritocracy looks like.

The implicit contract is straightforward: Authors disclose the tradeoffs in their designs, the room evaluates those tradeoffs against the needs of C++ users, and the vote reflects technical judgment. The committee's legitimacy rests on this contract. If the vote reflects something other than technical judgment, the institution is not what it appears to be.

---

## 3. What WG21 Actually Is

The vote in a WG21 study group or working group is not "is this technically correct?" The vote is "do I want this in the standard?" These are different questions. The first has a verifiable answer. The second is a preference. A body that votes on preferences is a political body, regardless of the technical language it uses to express those preferences.

This observation is not controversial. Every committee participant understands it intuitively. The question is what happens when the gap between the two questions widens - when the factors that determine "do I want this" diverge from the factors that determine "is this correct."

**Trust networks replace criteria lists.** In a committee of over five hundred members, no individual can evaluate every proposal on its technical merits. The committee is too large, the proposals too numerous, and the domains too specialized. Members rely on trust: They vote with colleagues whose judgment they respect, they defer to authors whose prior work has earned credibility, and they follow the signals of recognized experts. This is rational behavior under information constraints. It is also the mechanism by which social capital replaces technical evaluation. A proposal backed by trusted names survives. A proposal from an unknown author, making the same technical argument, faces a higher burden.

**Complexity creates interpretive discretion.** The more complex a paper, the fewer people in the room can evaluate it independently. For a simple proposal - a new algorithm, a small type trait - the room can read the paper, understand the design, and vote on the merits. For a proposal that spans hundreds of pages, introduces a new computational model, and interacts with multiple existing language features, the room cannot perform independent evaluation. It must trust the authors.

This trust is not misplaced in principle. Authors understand their own work better than anyone. But it creates an asymmetry: The more complex the proposal, the more the burden of disclosure falls on the authors, because only the authors can identify the tradeoffs the room cannot see. The room cannot evaluate what it does not know to look for.

**The symmetric transfer example.** [P2300](https://wg21.link/p2300r10)<sup>[2]</sup> ("std::execution") defines a completion protocol for asynchronous operations. Sender algorithms compose through struct receivers whose completion functions return `void`. C++20 provides symmetric transfer<sup>[10]</sup> - a mechanism where `await_suspend` returns a `coroutine_handle<>` and the compiler resumes the designated coroutine as a tail call, preventing stack overflow in coroutine chains. The void-returning completion protocol structurally prevents symmetric transfer through sender pipelines.

The phrase "symmetric transfer" does not appear once across [P2300R0](https://wg21.link/p2300r0)<sup>[1]</sup> through [P2300R10](https://wg21.link/p2300r10)<sup>[2]</sup> - eleven revisions of the paper, spanning four years. The tradeoff was never disclosed. The committee never evaluated it. The gap was not identified until `std::execution::task` ([P3552R3](https://wg21.link/p3552r3)<sup>[3]</sup>) development began and the interaction between coroutines and the sender completion protocol became unavoidable. US national body comment #948 (LWG4348)<sup>[11]</sup> independently confirmed the gap in the C++26 CD ballot.

This is not an accusation of negligence. It is an observation about what happens when a complex proposal passes through a trust-based evaluation process. The authors understood their design. The room trusted the authors. The tradeoff went unexamined because no one in the room had both the technical depth to identify it and the institutional standing to raise it. The implicit contract - authors disclose, the room evaluates - failed silently.

---

## 4. How the Gap Opened

Stroustrup built a governance structure to prevent tyranny. He succeeded. No corporation owns C++. No individual controls it. The committee is independent in a way that few language governance bodies have achieved.

But independence from corporate capture is not meritocracy. Solving one problem created a different one.

The original committee operated under one-organization-one-vote. National bodies sent delegations. The delegations represented institutional interests, but the institutions had reputations to protect and engineers to answer to. The shift to one-person-one-vote expanded participation dramatically. WG21 now has over five hundred members.<sup>[12]</sup> Stroustrup himself identified the consequences: vote manipulation, career committee members who contribute nothing technically but vote on everything, and a body too large for any individual to know all the participants.<sup>[13]</sup>

Stroustrup diagnosed the problem with characteristic honesty: "I cannot at this stage suggest an alternative. Maybe with the knowledge I now have, if I had my time machine, I could go back and create a better standards committee, but that's not the way things work."<sup>[13]</sup> He also diagnosed his own role in it: "I make too many mistakes. In particular, I tend not to come down hard on things."<sup>[8]</sup>

This self-diagnosis is the key. Stroustrup built a governance structure with no benevolent dictator - deliberately, because he did not trust himself with that power. But a structure with no authority to enforce meritocratic norms requires that the norms enforce themselves. They did, for a time, when the committee was small enough that every member knew every other member's work. They do not enforce themselves at five hundred members, where most participants cannot evaluate most proposals, and where the social cost of challenging a well-connected author exceeds the social cost of shipping a flawed design.

The vacuum filled with what vacuums always fill with: people who optimize for position rather than contribution. Not because they are bad people. Because the system rewards it. A member who accumulates institutional titles - chair of this group, board member of that foundation, program chair of this conference - acquires social capital that translates into influence over proposals. The titles do not require proportional technical contribution. The influence does not require proportional domain expertise. The system does not distinguish between authority earned through engineering achievement and authority accumulated through institutional participation.

This is not corruption. Corruption implies intent. This is entropy. The system is not broken by bad actors. It is broken by the absence of a mechanism that distinguishes social standing from technical merit - and by the temperament of the one person who might have built that mechanism.

---

## 5. The Structural Convergence

A standards body has two available methods for evaluating proposals: technical verification and social consensus.

Technical verification means someone checks the work. Someone reads the paper, understands the design, identifies the tradeoffs, tests the claims against the specification, and votes based on what they found. This is expensive. It requires domain expertise, time, and the willingness to challenge an author publicly when the work is incomplete. It is confrontational by nature. The person who identifies a gap must say so in a room full of the author's colleagues.

Social consensus means no one objects loudly enough. The proposal has respected authors. The study group chairs support it. The prior polls were favorable. No one in the room raises a blocking concern. The vote passes. This is cheap. It requires no domain expertise, no independent evaluation, and no confrontation. It is the path of least resistance.

Both methods can produce correct outcomes. A proposal backed by social consensus may also be technically sound. But the two methods have different failure modes. Technical verification fails when the verifier makes an error - a correctable failure, because the error is in the record and can be identified. Social consensus fails when a tradeoff goes undisclosed - a silent failure, because the room does not know what it did not evaluate.

Over time, a body that offers both methods will converge on the cheaper one. Not because its members are lazy or dishonest, but because the incentive structure favors it. A member who performs independent technical verification and raises a concern pays a social cost: The author is inconvenienced, the schedule is disrupted, the room's time is consumed. A member who defers to social consensus pays no cost. The rational strategy, for any individual member, is to verify only when the personal cost of a bad outcome exceeds the social cost of raising a concern. For most proposals, for most members, it does not.

The consensus model amplifies this convergence. WG21 operates on consensus, not majority rule. A small number of "strongly against" votes can block a proposal. This means proposals must avoid triggering strong objections. The optimization target is not "maximize technical correctness" but "minimize the probability that anyone objects strongly enough to block." These are different targets. A technically correct proposal that threatens an installed interest will draw strong objections. A technically flawed proposal that threatens no one will not.

The result: A body that began as a technical meritocracy converges, through rational individual behavior and structural incentives, toward social consensus as its primary evaluation method. Technical verification does not disappear. It persists in pockets - individual members who care enough to do the work, study groups with strong technical chairs, domains where the consequences of error are visible and immediate. But as the default mode of operation, social consensus displaces technical verification because it is easier to achieve and harder to falsify.

A vote that reflects social consensus looks identical to a vote that reflects technical judgment. The five-way poll produces the same numbers either way. The institution cannot distinguish between the two from its own output. The convergence is invisible from inside.

---

## 6. An Evaluation Model

The convergence described in Section 5 is not visible in committee transcripts, poll results, or paper records. It is visible only in the behavior surrounding a proposal as it moves through the process. The following table provides a model for observing that behavior.

Each row identifies a factor that can be observed during a proposal's advancement. The two columns describe what that factor looks like when the proposal is advancing on technical merit versus social consensus. No proposal advances purely through one column. The question is the ratio - and whether the ratio predicts the outcome for users.

The thesis of this model is simple: A feature that advances primarily through the left column will serve users well, because it was evaluated against their needs. A feature that advances primarily through the right column will serve its authors well, because it was evaluated against their standing. These are different outcomes. The standard is permanent. Users live with the result.

| Factor                         | Technical Merit                                                                                     | Social Consensus                                                                                    |
|--------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| Author's prior work            | Shipped libraries, deployed code, production users at scale                                         | Prior papers in the mailing, committee participation history, co-authorship with established names   |
| How the room evaluates         | Members read the paper, identify tradeoffs, ask questions about the design                          | Members check who authored it, who supports it, whether prior polls were favorable                   |
| Source of objections           | "This design has a structural gap" - cites specification, shows the defect                          | "This paper came late" - cites process, questions the author's standing                              |
| Response to criticism          | Author addresses the technical point, concedes or rebuts with evidence                              | Author's allies intervene, reframe the criticism as a process violation or a personal attack          |
| Disclosure behavior            | Author identifies tradeoffs in the paper, names what the design cannot do                           | Author presents strengths only; tradeoffs surface later through NB comments or third-party analysis  |
| Complexity handling            | Paper includes worked examples, code, benchmarks - the room can verify independently                | Paper is dense and theoretical; the room must trust the authors because it cannot verify              |
| Scheduling influence           | Proposal scheduled based on dependency graph, NB comment urgency, technical readiness               | Proposal scheduled based on author's relationship with the chair, factional alignment                |
| Poll composition               | Voters can articulate why they voted the way they did; reasons reference the design                  | Voters defer to trusted colleagues; reasons reference prior polls, author reputation, or momentum    |
| Advancement path               | Author built something, it works, users depend on it, the committee evaluates the artifact           | Author accumulated titles, served on boards, chaired groups, the committee evaluates the person      |
| Patronage role                 | Mentor teaches domain knowledge, reviews designs, improves the protege's engineering                 | Patron elevates protege into institutional roles, provides social access without requiring technical output |
| What blocks the proposal       | A verifiable technical defect that the author cannot resolve                                         | A well-connected opponent whose objection the room will not override regardless of technical merit    |
| What advances the proposal     | Evidence: working code, benchmarks, production deployment, independent confirmation                  | Consensus: no one objects loudly enough, the prior polls were favorable, the authors are trusted      |
| Credit distribution            | Credit follows contribution - who wrote the code, who identified the gap, who built the proof        | Credit follows position - who chaired the session, who managed the schedule, who held the title       |
| Failure mode                   | Verifiable: the defect is in the record, can be identified and corrected after shipping              | Silent: the room does not know what it did not evaluate; the gap surfaces years after standardization |

The model is predictive. A reader can observe a proposal moving through the committee, score each factor against the two columns, and estimate whether the feature will serve users or serve its authors. The prediction is not about intent. Authors who advance through social consensus are not necessarily acting in bad faith. They may believe their design is correct. The model measures the evaluation process, not the evaluator's motives.

The prediction that matters is this: A feature that reaches the standard primarily through the right column will accumulate correction papers, NB comments, and user complaints after shipping - because the tradeoffs that social consensus does not examine are the tradeoffs that users discover. A feature that reaches the standard primarily through the left column will not be free of defects, but its defects will be the kind that were examined and accepted, not the kind that were never disclosed.

The cost of a right-column feature is not borne by the authors. It is borne by the users who build on it, the implementers who must maintain it, and the committee members who must file the correction papers. The standard is permanent. The authors move on. The users remain.

### 6.1 Scoring

Each factor is scored on a 5-point scale:

| Score | Meaning                                                     |
|:-----:|-------------------------------------------------------------|
| +2    | Strongly merit-driven                                       |
| +1    | Leans merit with some institutional influence                |
| 0     | Mixed, or insufficient data (e.g. R0 with no revision history) |
| -1    | Leans social consensus with some technical basis             |
| -2    | Strongly social-consensus-driven                             |

The aggregate ranges from -28 to +28.

| Range       | Interpretation                                                              |
|-------------|-----------------------------------------------------------------------------|
| +20 to +28  | Strongly merit-driven; gaps are verifiable and correctable                  |
| +10 to +19  | Merit-driven with institutional support                                     |
| 0 to +9     | Mixed; institutional dynamics materially shape the outcome                  |
| -1 to -10   | Consensus-driven; technical evaluation is secondary to coalition maintenance |
| -11 to -28  | Structurally political; users should expect post-ship correction papers     |

No weighting. All 14 factors contribute equally. Weighting would introduce the scorer's judgment about which factors matter more, which is the kind of subjective input the model is designed to eliminate.

Factor 4 (response to criticism) scores 0 for R0 papers by default. The factor becomes meaningful only after at least one revision cycle.

The scoring is designed for a single evaluator - human or AI - to apply with reproducible inputs. Inter-rater reliability can be tested by having multiple AI sessions score the same paper with the same inputs and comparing results. Divergence reveals factors where the evidence is ambiguous.

---

## 7. The Peerage

A peerage is a system of rank in which titles confer authority, patronage determines advancement, and social trust substitutes for independent evaluation. The titles may originally have been earned. The patronage may originally have rewarded merit. The trust may originally have been justified. Over time, the system optimizes for its own reproduction. Titles beget titles. Patrons elevate proteges who will sustain the network. Trust circulates within the group and is extended to newcomers only when they demonstrate allegiance to the group's norms - not the norms of the domain the group was created to serve, but the social norms of the group itself.

WG21 exhibits these properties.

Authority in the committee correlates with institutional titles - study group chair, working group chair, national body chair, foundation board member, conference program chair - more reliably than it correlates with technical contribution. A member who holds four chairs and has authored no significant technical proposal carries more weight in the room than a member who holds no titles and has shipped a library used by millions. The first member is a peer. The second is a petitioner.

Advancement follows patronage. Senior committee members identify promising newcomers, encourage them into operational roles, and prepare them as successors. This is not sinister. It is how every institution reproduces itself. But it means that the path to influence runs through relationships with existing power holders, not through independent technical achievement. A newcomer who arrives with correct papers but no patron faces a higher burden than a newcomer who arrives with a patron but no papers.

The room reads the person, not the paper. A paper author preparing to present at a committee meeting does not merely need correct analysis. The author needs to demonstrate, in real time, under adversarial questioning, that they are the kind of person whose work can be trusted. Are they reasonable? Will they accept amendments? Do they concede when wrong? Do they become hostile under pressure? These are social evaluations. They are integrity tests, not correctness tests. The paper could be emailed. The person must appear.

This is the answer to the operator's question. The papers are correct. Anyone can verify the correctness by reading them. The operator must argue them in person because the committee does not evaluate papers. It evaluates people. Correctness is the entry ticket. Social trust is what gets you through the door.

The question this paper leaves with the committee is not whether this characterization is accurate. Every member who has participated in a contentious vote knows it is. The question is whether this is the institution Stroustrup intended when he built a governance structure to ensure that C++ would be guided by the collective engineering judgment of its practitioners - and whether the distance between what he intended and what exists is a distance the committee is willing to measure.

---

## References

- [1] [P2300R0](https://wg21.link/p2300r0) - Bakers, Hollman, Howes, Lee, Garland, Kirkham, Niebler. "`std::execution`." October 2020. https://wg21.link/p2300r0
- [2] [P2300R10](https://wg21.link/p2300r10) - Bakers, Hollman, Howes, Lee, Garland, Kirkham, Niebler. "`std::execution`." June 2024. https://wg21.link/p2300r10
- [3] [P3552R3](https://wg21.link/p3552r3) - Dietmar K&uuml;hl. "`task` Type for Senders/Receivers." 2025. https://wg21.link/p3552r3
- [4] [P4007R0](https://wg21.link/p4007r0) - Vinnie Falco, Mungo Gill. "Senders and Coroutines." February 2026. https://wg21.link/p4007r0
- [5] [P2583R1](https://wg21.link/p2583r1) - Mungo Gill, Vinnie Falco. "Symmetric Transfer and Sender Composition." March 2026. https://wg21.link/p2583r1
- [6] [P4003R0](https://wg21.link/p4003r0) - Vinnie Falco, Mungo Gill. "Coroutines for I/O." February 2026. https://wg21.link/p4003r0
- [7] [P4014R0](https://wg21.link/p4014r0) - Vinnie Falco, Mungo Gill. "The Sender Sub-Language." February 2026. https://wg21.link/p4014r0
- [8] Bjarne Stroustrup. Boost documentary interview (filmed 2025). Unscripted long-form interview covering career, committee governance, and language design.
- [9] Bjarne Stroustrup. alphalist CTO Podcast, Episode 61: "Creator of C++." On evaluating the STL against a criteria list.
- [10] [P0913R1](https://wg21.link/p0913r1) - Gor Nishanov. "Add symmetric coroutine transfer." 2018. https://wg21.link/p0913r1
- [11] US national body comment #948 (LWG4348). "Support Symmetric Transfer." C++26 CD ballot, October 2025. https://github.com/cplusplus/nbballot/issues/948
- [12] Herb Sutter. "Trip report: Autumn ISO C++ standards meeting (Kona, HI, USA)." November 2025. Reports WG21 attendance exceeding 500 members.
- [13] Bjarne Stroustrup. Meeting C++ 2022 AMA. On committee size, vote manipulation, and the impossibility of starting over.
