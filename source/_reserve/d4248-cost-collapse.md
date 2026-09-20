---
title: "The Cost Collapse"
document: P4248R0
date: 2026-07-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

SD-4's first-mover rule was designed when papers cost months of expert effort. AI reduces that cost by an order of magnitude. Seven predictions follow from the game-theoretical structure. Three independent data sources - two public, one non-public - confirm all seven. What happens to a consensus body's procedural architecture when the cost assumption underneath it disappears?

---

## Revision History

### R0

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains proposals in the `std::execution` space: P4003, P4007, and P4100. The author uses AI-assisted drafting. The author's papers have been categorically dismissed on provenance grounds. The structural analysis applies regardless of the author's personal experience. The same mechanisms operate on every consensus body where paper production costs have dropped, including bodies whose decisions the author agrees with.

This paper is a companion to P4201<sup>[1]</sup> (SD-4 and ISO governance), P4237<sup>[2]</sup> (the information seal), and P4241<sup>[3]</sup> (dopaminergic effects of consensus participation).

This paper asks for nothing.

---

## 2. What The Rules Achieve

SD-4's paper-related provisions serve real functions.

The paper-existence rule - "if a proposal doesn't have a paper, it doesn't exist"<sup>[4]</sup> - filters noise. It ensures that committee time is spent on proposals that someone cared enough to write down, with examples, with alternatives considered, with principles articulated. The committee processes 300-500 papers per year. Without this filter, the number would be higher and the quality lower.

The first-mover rule - "if a competing alternative does not have a paper, it does not exist and will not block progress of a proposal that we do have before us"<sup>[4]</sup> - prevents indefinite delay. A concrete proposal advances. A hypothetical alternative does not block it. The chair "may elect to delay the progress of the active proposal by one meeting"<sup>[4]</sup> to give the objector time to produce a paper. One meeting. Then the concrete proposal moves.

The quality bar - papers should be "example-based," "principle-based," and "show design alternatives considered"<sup>[4]</sup> - produces better proposals. The committee explicitly distinguishes "someone's cool idea" from "a real proposal"<sup>[4]</sup> on these criteria.

The prepared-presenter requirement - the proposal must have "one of its authors, or another qualified and prepared presenter"<sup>[4]</sup> physically present - ensures that someone who understands the domain is in the room to answer questions and receive feedback.

Each provision purchases something real. The question is what happens to the purchase when the price changes.

---

## 3. The Cost Assumption

Every provision in Section 2 rests on an unstated assumption: Papers are expensive to produce.

The paper-existence rule filters for commitment because writing a paper costs months of expert effort. The first-mover rule protects incumbents because a challenger cannot produce a competing paper in one meeting cycle. The quality bar (example-based, principle-based, alternatives considered) filters for depth because meeting all three criteria requires sustained analytical work. The one-meeting delay is sufficient because no one can produce a high-quality competing paper in four weeks.

These assumptions were correct for thirty years. A paper that meets SD-4's quality bar required domain expertise, familiarity with the committee's prior art, the ability to write fluent technical prose, and weeks to months of concentrated effort. The production cost was the filter. The filter worked because the cost was real.

---

## 4. The Collapse

AI reduces paper production cost by an order of magnitude.

A competing paper - example-based, principle-based, with design alternatives considered - can be produced before the next mailing deadline. SD-4's quality bar describes properties that current generative tools produce reliably: motivating examples, articulated design principles, enumerated alternatives with concrete discussion of tradeoffs.

The binding constraint shifts. Under the old cost structure, the constraint was "can you write a paper?" Under the new cost structure, the constraint is "will the chair schedule it?"

**The cost assumption was load-bearing. It has collapsed.**

---

## 5. The First-Mover Vulnerability

The first-mover game has two players: the Incumbent (has a paper, has meeting time, has revision history) and the Challenger (believes a different approach is better).

Under the old cost structure:

| | Challenger writes competing paper | Challenger does not write |
|---|---|---|
| **Challenger's cost** | Months of expert effort | Zero |
| **Challenger's benefit** | Uncertain scheduling; one-meeting delay at best | None, but no cost either |

The Challenger's dominant strategy was not to challenge. The cost exceeded the expected benefit. The Incumbent advanced unchallenged.

Under the new cost structure:

| | Challenger writes competing paper | Challenger does not write |
|---|---|---|
| **Challenger's cost** | Days of AI-assisted effort | Zero |
| **Challenger's benefit** | Paper "exists" under SD-4; one-meeting delay triggered | None |

The Challenger's production cost has dropped. The one-meeting delay is still available. The paper still "exists" under SD-4's own rules. The first-mover advantage weakens on the paper-production axis.

At scale: Every proposal can be challenged by any actor with AI access and a mailing deadline. The scheduling game - controlled by chairs appointed by the Convenor<sup>[1]</sup> - becomes the sole remaining filter.

IETF explicitly allows multiple competing drafts simultaneously: "The document is always subject to change by the working group, up to and including full replacement"<sup>[5]</sup>. TC39 allows competing proposals to coexist at any stage<sup>[6]</sup>. W3C's incubation model is designed to surface rival proposals before standardization<sup>[7]</sup>. SD-4's bird-in-hand doctrine is structurally unique among major standards bodies.

---

## 6. The Provenance Dismissal Game

AI creates a new game that did not exist when all papers were human-written.

Two players: the Reader (encounters an AI-assisted paper) and the Author (published it).

| | Reader engages with content | Reader dismisses on provenance |
|---|---|---|
| **Paper is correct** | Reader must address conclusions | No cost; conclusions ignored |
| **Paper is wrong** | Reader finds the flaw | No cost; same outcome |

Dismissing on provenance is a dominant strategy. It is weakly better in every cell. The Reader never needs to read the paper.

The quality concern is real and frequently correct. AI produces bad output. Readers who have been burned by low-quality AI-generated text are right to be skeptical. The structural observation is narrower: The dominant response is categorical dismissal on provenance, not specific identification of quality defects. If the objection were purely about quality, the response would cite a specific error in a specific paper. Instead the response asserts that AI authorship precludes new information "by definition." The magnitude of the objection exceeds what the quality concern alone can explain.

A quality-based filter produces heterogeneous response: "P4129 has a point about voting dynamics but P4208 is thin." A provenance-based filter produces homogeneous response: every paper dismissed on the same basis, the label applied to the corpus, no discrimination between papers. Fifty papers were published between March and August 2026. A search of the public record returns zero instances of a participant citing a specific claim from a specific paper as worth examining despite its provenance. The uniformity is the tell.

**The committee's only defense is a social norm that has no procedural basis.**

---

## 7. The Exposure Gradient

P4241<sup>[3]</sup> documents the reward architecture of consensus-body participation: dopaminergic reinforcement from poll victories, hedonic adaptation that drives escalation, and a selection mechanism that retains the most susceptible participants across decades. The same framework predicts who will exhibit the sharpest provenance-dismissal response.

Three independent proxies measure cumulative exposure to the reward architecture:

**Tenure.** Years of participation. Each year adds meeting cycles, poll outcomes, wins and losses. P4241 Section 11 documents the selection mechanism: Participants who stayed longest are those whose neurochemistry responded most intensely to the initial reward. Those who habituated fully or refused to escalate left. The committee's composition is the residue of this filter.

**Paper volume.** Successfully adopted papers. Each adoption is a dopamine event whose prediction error decays toward zero with repetition (Schultz 1997<sup>[8]</sup>). A participant with twenty adopted papers has experienced twenty reward events whose signal has attenuated. AI-produced papers threaten the currency these events represent.

**Chair status.** P4241 Section 12 documents the chair's unique reward: ambient deference, singular authority over consensus determination, continuous (not intermittent) reinforcement during meetings. AI threatens the chair's authority over scheduling by flooding the queue, and threatens the scarcity that makes chair decisions consequential.

The prediction: Participants with longer tenure, more adopted papers, and current or former chair status will exhibit sharper provenance-dismissal responses. Participants with shorter tenure or external status will engage with content.

Not every long-tenured, high-volume, chair-holding participant will exhibit provenance dismissal. Some participants are immune to the reward architecture or have developed compensating mechanisms. They can hold chair positions, adopt many papers, and serve for decades without the reward circuit dominating their response to novelty. Their existence confirms the model describes a tendency shaped by neurochemistry, not a deterministic rule. The immune participant's long tenure proves that long service is possible without the effect. Both populations coexist. They are distinguishable by their response to AI-assisted papers - because AI threatens the reward architecture but not the work itself.

Published research supports the mechanism. Sarkar (2025)<sup>[9]</sup> argues that "AI shaming" - disparaging work as AI-generated - is boundary work by knowledge workers protecting class identity whose value depends on exclusivity. Empirical studies demonstrate a social evaluation penalty for AI use: Observers discount competence when effort appears bypassed, and workers reduce AI reliance by approximately 14% when usage becomes visible to evaluators<sup>[10]</sup>. The Princeton "Making Talk Cheap" study<sup>[11]</sup> formalizes the dynamic: When LLMs collapse Spencian costly signals, top-quintile workers are hired 19% less often. The signal that effort provided is destroyed.

At the neurochemical level, perceived social devaluation activates an evolved shame defense system that tracks devaluation magnitude with correlation coefficients of .67-.79 across cultures (Sznycer et al. 2016<sup>[12]</sup>). Social-evaluative threat produces cortisol increases correlated specifically with shame, not general anxiety (Gruenewald et al. 2004<sup>[13]</sup>). Status loss activates anti-reward circuits via negative reward prediction error in the lateral habenula (Fan et al. 2023<sup>[14]</sup>). Exposure to generative AI's capabilities elicits negative emotions that mediate perceived threat to identity, uniqueness, and social value - emotional-first, threat-appraisal-second (Gabbiadini et al. 2023<sup>[15]</sup>).

**The gap between how concerned you should be about AI-assisted papers and how concerned you actually are is the size of the threat the reward architecture perceives.**

---

## 8. Two Patterns

Two behavioral patterns emerge from the analysis. Pattern A describes the response of a participant whose engagement is not dominated by the reward architecture. Pattern B describes the response of a participant whose reward circuit has been remodeled by years of consensus-body participation.

| Stimulus | Pattern A | Pattern B |
|---|---|---|
| "Papers used to be expensive. Are they still?" | Evaluates the observation | Perceives a threat. Language protects scarcity: "Write it yourself." "Leave the LLM out." |
| The first-mover vulnerability | Evaluates the argument. May disagree on specifics. | Dismisses without examining. Acknowledging would retroactively devalue institutional capital. |
| An AI-assisted paper with checkable claims | Asks "is this claim true?" Skepticism produces specific objections. | Attacks the author, not the content. The intensity is disproportionate to the stated concern. |
| The trilemma | Evaluates the three options. May prefer one. | Rejects the framing. The trilemma itself is a threat. |

---

## 9. Seven Predictions

If the provenance dismissal game operates as modeled and P4241's selection mechanism operates as documented, seven behaviors should be observable wherever AI-assisted papers are discussed:

1. **Categorical dismissal on provenance.** A participant asserts that AI authorship precludes new information by definition, without engaging any specific claim in any specific paper.

2. **Blanket labeling.** A single term is applied to the entire corpus, collapsing the question "is this specific paper useful?" into "is this class of papers legitimate?"

3. **Advice to restore the cost barrier.** A well-intentioned participant suggests removing the tool and writing manually - structurally honest advice whose function is to re-impose the production cost that protects the first-mover equilibrium.

4. **No engagement with checkable claims.** A falsifiable claim is present in the discussion and is not checked.

5. **Social pressure to stop publishing.** The request is framed as concern for the author's reputation, not as procedural authority - because no procedural authority to restrict publication exists.

6. **Tenure correlation.** Participants with longer tenure exhibit Pattern B responses. Participants with shorter tenure or external status exhibit Pattern A responses.

7. **Uniform rejection.** The rejection is applied uniformly across the corpus. No individual paper is singled out as having a valid finding despite its provenance.

**Disconfirmation:** If participants engage with specific claims before evaluating provenance, the model is wrong.

---

## 10. Observation A: r/cpp, beast2 Thread

The following exchanges occurred on r/cpp in May 2026, in a thread about beast2 and std::execution.

**Prediction 1.**

Khalil Estell (WG21 member, US NB, ~3 years) writes on r/cpp (May 2026):

> Given you tend to use LLM to generate a lot to stuff, before I read this, did you fully read and review this paper. If so, then I'll consider reading it. If not, then I'll pass.

Jonathan Wakely (LWG chair, libstdc++ maintainer, ~20 years) writes on r/cpp (May 2026):

> But have you read it and fact checked it yourself? It's a simple question.

**Prediction 2.**

James20k (paper author, ~3 years) writes on r/cpp (May 2026):

> Its because the vast majority of AI produced content is slop, and authors generating content with LLMs have a tendency to push the burden of reviewing and authenticating its quality onto their peers.

**Prediction 5.**

The provenance question receives 20 upvotes. The response "the claims stand on their own" receives -5.

**Counter-evidence.**

not_a_novel_account (non-committee member) writes on r/cpp (May 2026):

> I don't think the designs presented in your existing papers on the topic are bad, quite the opposite, they're probably the best exploration of the problem which currently exists.

Daveed Vandevoorde (Direction Group member, EDG, ~30 years) engages substantively on reflection history, reaching agreement on process questions. dr-mrl (non-committee member) reads the paper, identifies a typo, and it is corrected.

**Prediction 6.** Wakely (~20 years, LWG chair) exhibits Pattern B. Vandevoorde (~30 years, Direction Group) exhibits Pattern A. The tenure correlation predicts tendency, not rule. Vandevoorde is counter-evidence.

---

## 11. Observation B: r/cpp, Benchmark Thread

In a separate r/cpp thread the same week, a colleague posted benchmark results comparing sender-based I/O against coroutine-based I/O. The post contained benchmark tables, methodology, five independent runs, and a public repository with source code.

**Prediction 1.**

slithering3897 writes on r/cpp (May 2026):

> How much of this is written yourself?

34 upvotes.

Abbat0r writes on r/cpp (May 2026):

> The primary thing this post means is that its author couldn't be bothered to do more than copy-paste LLM output to produce this analysis. Determining what that means for the quality of the benchmarks themselves should probably be an exercise for us all.

15 upvotes.

throw_cpp_account writes on r/cpp (May 2026):

> I have no idea if the work is valid or not, but your behavior makes me highly distrusting of it.

14 upvotes.

**Prediction 2.**

ald_loop writes on r/cpp (May 2026):

> man you and Vinnie Falco really need to learn that no one wants to read paragraphs of AI slop

30 upvotes.

**Prediction 5.**

Stephan T. Lavavej (MSVC STL Dev, r/cpp moderator, ~20 years) writes on r/cpp (May 2026):

> Moderator warning: The subreddit rules prohibit AI-generated content. Write in your own words here, or don't write at all. You clearly think you're being good about editing an AI-generated first draft, but as multiple people are telling you, anyone who can tell the difference is strongly put off by what you're doing, and you need to stop.

24 upvotes. The trilemma's second leg - formalize anti-AI restrictions - already operating through platform moderation rules.

**Quantitative social cost.** The benchmark author's substantive defense receives -10 votes. Provenance questions receive 30-34.

**Counter-evidence.**

Remarkable-Test7487 (non-committee member, university professor) writes on r/cpp (May 2026):

> the benchmark and all the code are publicly available, and the folks at the C++ Alliance are putting in a lot of hours on this project... we should also include a discussion of technical issues

19 upvotes.

---

## 12. Observation C: WG21 Mattermost

The following exchanges occurred on a non-public WG21 communication platform in May 2026. Quotes are anonymized by role and tenure. Participants with access to the platform can verify each quote.

**Prediction 1.**

A subgroup chair (~15 years) writes (May 2026):

> It looks like that paper, P4208R0, was written by an LLM in which case, by definition, it does not contain new information unless you personally added such information.

One additional committee member (~10 years) endorsed this statement.

**Prediction 2.**

A committee member (~10 years) writes (May 2026), endorsed by six additional members (all 10+ years, including two subgroup chairs):

> Sure, that doesn't mean we can't come to conclusions when an author continuously sends us heaps of AI slop. We initially assume in good faith, we are not required to pretend we are stupid.

A subgroup chair (~15 years) writes (May 2026):

> Please stop publishing these papers as they are nothing but noise. We all have access to LLMs that we can ask to do an analysis if we like. We don't need you to do that for us, especially when we didn't ask you to.

**Prediction 3.**

A subgroup chair (~15 years) writes (May 2026):

> Great, make the arguments. Leave the LLM out of it so that you can create trust with your readers. You don't have that trust right now.

**Prediction 4.**

In the same thread, the claim "in no revision of P2300 does the term 'symmetric transfer' appear" was stated. The claim is falsifiable in thirty seconds. It was not checked.

**Prediction 5.**

A subgroup chair (~15 years) writes (May 2026):

> I suggest you reconsider whether doing so is worth your time given the reception your papers have received so far.

A specification subgroup chair (~20 years) writes (May 2026):

> Write a blog

**Prediction 6.**

Every Pattern B response in the thread comes from a participant with 10+ years of committee tenure and/or a chair position. No Pattern B response comes from a participant with fewer than 10 years.

In a separate thread three weeks earlier, the label appears as a casual aside in a conversation about paper numbering:

A long-tenured member (~20+ years) writes (May 2026):

> I don't consider AI slop papers to be good

In the same thread, a committee member describes the vulnerability this paper documents as a joke:

A committee member writes (May 2026):

> Unless somebody hooks up an AI and makes it output papers at an absolutely impossible rate

**The equilibrium under self-awareness.**

The author stated: "dismissing the papers because of their provenance is the game-theoretical best move." Six committee members endorsed this statement, including two subgroup chairs. All six had 10+ years of tenure. The same participants continued to dismiss papers on provenance in the same thread.

**They see the game. They play it anyway. That is what an equilibrium is.**

---

## 13. The Endorsement Pattern

Across two threads on the non-public platform, thirteen distinct participants endorsed or authored provenance-dismissal statements via emoji reactions. The endorsement pattern:

| Statement | Endorsements | Tenure range of endorsers |
|---|---|---|
| "AI slop" characterization | 6 endorsements + author | All 10+ years; includes 2 subgroup chairs |
| Resistance to external scrutiny | 7 endorsements | All 10+ years; includes 1 subgroup chair |
| "Copypastaed tokens" | 2 endorsements (laughing) | Both 10+ years |
| "Provenance dismissal is the game-theoretical best move" | 6 endorsements | All 10+ years; includes 2 subgroup chairs |
| "Slow down" / "Write it yourself" | 2 endorsements each | Both 10+ years |
| "By definition no new information" | 1 endorsement + author | Both 10+ years; author is subgroup chair |
| Information seal defense | 6 endorsements + author | All 10+ years |

Two participants endorsed five or more of the seven statements tracked. Both hold structural positions (one specification subgroup chair, one long-tenured member). Every endorser with known tenure is 10+ years. Zero endorsements from anyone under 10 years.

---

## 14. Cross-Source Summary

| Prediction | r/cpp beast2 thread | r/cpp benchmark thread | Non-public platform |
|---|---|---|---|
| 1. Categorical provenance dismissal | Estell, Wakely | slithering3897, Abbat0r, throw_cpp_account | Subgroup chair ("by definition") |
| 2. Blanket labeling | James20k ("slop") | ald_loop ("AI slop") | "AI slop" (6 endorsements), "noise" |
| 3. Advice to restore cost barrier | - | - | "Leave the LLM out" |
| 4. No engagement with checkable claims | - | Benchmarks not evaluated | "symmetric transfer" not checked |
| 5. Social pressure to stop | Voting pattern (-5) | Lavavej (mod warning), voting (-10) | "Write a blog" (two chairs) |
| 6. Tenure correlation | Wakely (B), Vandevoorde (A) | Lavavej (B) | All Pattern B responses 10+ years |
| 7. Uniform rejection | No paper singled out | No benchmark data examined | Corpus-level dismissal |

Three independent observation points. Partially overlapping participants. Same seven behaviors. Counter-evidence present in all three sources. The model predicts the dominant strategy, not universal behavior.

---

## 15. The Trilemma

The committee faces three responses. Each has consequences.

| Response | Provides | Costs |
|---|---|---|
| Reform the first-mover rule | Structural adaptation to cheap papers | Opens SD-4 to governance reform; the standing document lock (P4201<sup>[1]</sup>) makes this difficult |
| Formalize anti-AI restrictions | Clear bright line for reviewers | Unenforceable (how to distinguish AI-assisted from human-written?); conflicts with ISO's own position permitting AI for research<sup>[16]</sup>; faces an authority gap: "Our P-papers very intentionally do not adhere to ISO copyright rules" (former EWG chair, ~20 years)<sup>[17]</sup> |
| Accept the vulnerability | No procedural change required | Bird-in-hand advantage nullified; scheduling game becomes sole filter; chair discretion increases |

The second leg is already being attempted. ArXiv announced a one-year submission ban for unchecked AI output (May 2026)<sup>[18]</sup>. ICML 2026 desk-rejected 497 papers for LLM policy violations<sup>[19]</sup>. P3702R1<sup>[20]</sup> proposes to ban AI-generated content in WG21 submissions. P4023R0<sup>[21]</sup> (Direction Group) adopts ISO's AI guidance. W3C's Advisory Board takes a different approach: AI is permitted with disclosure, labeling, and human responsibility<sup>[22]</sup>. IETF requires disclosure of substantial AI content but permits editorial use<sup>[23]</sup>. TC39 has no AI policy as of May 2026.

The enforcement problem is unsolved everywhere. No organization has demonstrated reliable detection of AI-assisted text. Formalization without enforcement is a rule that binds the honest and releases the strategic.

All three legs weaken SD-4's current equilibrium. The trilemma cannot be avoided because the cost collapse has already happened.

---

## 16. The Remaining Filter

After the cost collapse, one SD-4 filter still binds: the prepared-presenter requirement.

AI can write the paper. AI cannot attend the meeting. The "qualified and prepared presenter"<sup>[4]</sup> must be physically in the room. This shifts the barrier from writing capacity to travel funding. The employer-dependency that P4201<sup>[1]</sup> documents becomes more central, not less. The paper-production barrier was partially meritocratic - it rewarded effort and expertise. The travel barrier is purely economic - it rewards employer willingness to fund attendance.

**AI does not democratize outcomes. It shifts the bottleneck from the filter that rewarded effort to the filter that rewards patronage.**

---

## 17. Objections

### "AI papers are low quality."

The quality concern is real and frequently correct. The structural observation is narrower: The dominant response is categorical dismissal on provenance, not specific identification of quality defects. If the objection were about quality, the response would cite a specific error. Instead the response asserts that AI authorship precludes new information "by definition." The magnitude exceeds what the quality concern alone explains. The residual is the subject of this paper.

### "The committee can simply ignore obstructive papers."

This requires chair discretion, which concentrates more power in the appointment chain that P4201<sup>[1]</sup> documents. The defense against the exploit is more chair discretion, which is the structural problem the exploit exposes.

### "Nobody would actually do this."

The vulnerability exists regardless of whether it is exploited. Making it common knowledge changes the game. A committee member described the vulnerability as a joke three weeks before the provenance dismissal thread. The joke was not followed by structural analysis.

### "This paper is self-serving."

The structural vulnerability affects every proposal, including proposals the author opposes.

### "The author's volume of papers IS the flooding attack."

The author's papers are inform-papers. They carry `intent: info`. They do not compete with any proposal. They do not trigger the one-meeting delay. They do not require scheduling. They do not consume meeting time unless a chair elects to schedule them. Of the author's entire corpus, one paper carries an ask. SD-4's first-mover rule applies to proposals, not to the mailing archive. The delegates have been aware of this distinction for months.

### "ISO rules prohibit AI-generated content in papers."

ISO's AI guidance states: "Do not use images or text created by generative AI in any ISO content"<sup>[16]</sup>. P3702R1<sup>[20]</sup> proposes to align SD-7 with this guidance. However, a former EWG chair (~20 years) states on a non-public WG21 platform: "Our P-papers very intentionally do not adhere to ISO copyright rules for their prose content. ISO has no ownership of them and can't dictate where they can and cannot go"<sup>[17]</sup>. If P-papers are not ISO content, ISO's AI guidance has no jurisdiction over them. The proposed ban faces an authority gap: The rules it invokes do not apply to the documents it targets.

---

## 18. Conclusion

A rule that filters for commitment works when commitment is expensive. When the cost drops, the filter passes everything. What remains is whatever other filters the system provides. In SD-4's case, what remains is chair discretion over scheduling - a filter that operates through the appointment chain, not through merit.

The committee's defense against this structural change is a social norm: Dismiss AI-assisted papers on provenance. The norm has no procedural basis. It is enforced through social cost, not through rules. It works today because the committee's social cohesion is strong enough to sustain it. It stops working the moment any respected insider uses AI for a competing paper - because the norm cannot distinguish the insider's AI paper from the outsider's.

The author cannot assess whether the provenance dismissal is entirely strategic or partially justified. Some AI-assisted papers may genuinely be lower quality. The structural observation holds regardless: The dominant strategy is dismissal on provenance whether the papers are good or bad. The magnitude of the response exceeds what quality concern alone explains. The uniformity of the response across fifty papers, with zero instances of selective engagement, exceeds what quality filtering predicts. The tenure correlation of the response matches what P4241's reward architecture predicts. Three independent data sources confirm seven predictions.

The cost assumption was load-bearing. It has collapsed. What the committee builds on the ground where it stood is the committee's decision.

---

## Acknowledgments

*To be completed.*

---

## References

[1] Falco, V. [P4201R0](https://wg21.link/p4201r0) - "Two Systems, One Committee: A Game-Theoretical Analysis of ISO Governance vs. SD-4." 2026.

[2] Falco, V. [P4237R0](https://wg21.link/p4237r0) - "The Information Seal: Game-Theory Analysis of SD-4's Quoting Restriction." 2026.

[3] Falco, V. [P4241R0](https://wg21.link/p4241r0) - "Long-Term Dopaminergic Effects of Consensus Body Participation." 2026.

[4] Davidson, G. [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures." 2026-05-11.

[5] Farrel, A. [RFC 7221](https://www.rfc-editor.org/rfc/rfc7221) - "Handling of Internet-Drafts by IETF Working Groups." 2014.

[6] [TC39 Process Document](https://tc39.es/process-document/) - Ecma TC39.

[7] [W3C Recommendation Track](https://www.w3.org/guide/standards-track/) - W3C.

[8] Schultz, W. "A neural substrate of prediction and reward." *Science* 275(5306), 1997.

[9] Sarkar, A. "AI Could Have Written This: Birth of a Classist Slur in Knowledge Work." CHI 2025.

[10] "AI Shaming in Organizations: When Technology Adoption Threatens Professional Identity." 2026.

[11] "Making Talk Cheap: Generative AI and Labor Market Signaling." Princeton, 2025.

[12] Sznycer, D. et al. "Shame Closely Tracks the Threat of Devaluation by Others, Even Across Cultures." *PNAS* 113(10), 2016.

[13] Gruenewald, T.L. et al. "Acute Threat to the Social Self: Shame, Social Self-Esteem, and Cortisol Activity." *Psychosomatic Medicine* 66(6), 2004.

[14] Fan, Z. et al. "Neural Mechanism Underlying Depressive-Like State Associated with Social Status Loss." *Cell* 186(3), 2023.

[15] Gabbiadini, A. et al. "The Emotional Impact of Generative AI: Negative Emotions and Perception of Threat." 2023.

[16] ISO. "Guidance on use of artificial intelligence (AI) for ISO committees." Version 1.1, March 2025.

[17] Former EWG chair. Non-public WG21 communication platform, May 2026.

[18] "ArXiv Introduces One-Year Ban for Researchers Who Submit Papers with Unchecked AI-Generated Content." Ars Technica, May 2026.

[19] ICML 2026 Peer Review Ethics.

[20] Schultke, J. [P3702R1](https://wg21.link/p3702r1) - "Stricter requirements for document submissions (SD-7)." 2025.

[21] [P4023R0](https://wg21.link/p4023r0) - "Strategic Direction for AI in C++: Governance, and Ecosystem." 2026.

[22] W3C Advisory Board. [Use of Large Language Models in Standards Work](https://www.w3.org/TR/llms-standards/). March 2026.

[23] [RFC 9775](https://www.rfc-editor.org/rfc/rfc9775.html) - "IRTF Code of Conduct." IETF.

[24] Simcoe, T. "Standard Setting Committees: Consensus Governance for Shared Technology Platforms." *American Economic Review* 102(1), 2012.

[25] "Close Enough for Government Work: The Committee Rulemaking Game." *Virginia Law Review*.

[26] Inzlicht, M. et al. "The Effort Paradox: Effort Is Both Costly and Valued." *Trends in Cognitive Sciences* 22(4), 2018.

[27] "Evidence of a social evaluation penalty for using AI." *PMC*, 2026.
