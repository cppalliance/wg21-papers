---
title: "The Capacity to Self-Correct"
document: D4264R0
date: 2026-06-11
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

This paper is an instrument that measures the committee's capacity to self-correct.

It takes the significant claims of P4263R0 and pairs each with two observable responses: the response a disclosed behavioral framework expects, and the response that would contradict it. Exactly one branch of each pair will occur. The paper therefore cannot be wrong, asserts nothing that either branch would prove, promises no follow-up, and asks for nothing. Which branches fire is the measurement.

---

## Revision History

### R0: July 2026

- Initial revision.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author developed and maintains [Capy](https://github.com/cppalliance/capy) and [Corosio](https://github.com/cppalliance/corosio) and believes coroutine-native I/O is a practical foundation for networking in C++.

This paper states, for each significant claim of P4263R0, the response the author's behavioral framework expects and the response that would contradict it.

The author maintains composite behavioral models of three structural segments of the committee's ecosystem: appointees, delegates, and the public. The models are constructed from public sources - procedural documents, published papers, attendance records, trip reports, poll outcomes, recorded talks, and political science research. This paper discloses the models in outline and the binaries they generate in full.

The models describe aggregate tendencies of structural roles. Their resolution is the role.

This paper is drafted with AI.

This paper asks for nothing.

---

## 2. The Instrument

[P4263R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4263r0.pdf)<sup>[1]</sup> answers the committee's question "why do you write so many papers?" with a structural analysis: a thin evidentiary record, a tournament incentive that produces the thinness, a self-authored rulebook that permits change at will, and a program of information-only papers addressed to the permanent record. Those are claims. Claims about an institution generate responses from the institution, and responses are observable.

This paper treats the responses as data before any of them exist. For each significant claim, two columns are stated in advance: the expected column - what the author's behavioral framework anticipates - and the disconfirming column - the observable behavior that would contradict the framework. Each pair is exhaustive. One branch must occur.

An instrument built this way is unfalsifiable by construction, and this paper says so plainly. An instrument is not a hypothesis. It does not bet; it partitions.

[P4047R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4047r0.pdf)<sup>[2]</sup> scores predictions after outcomes are known. This paper defines its binaries before any outcome exists and assigns no scores. The relationship is methodological ancestry. The difference is the genre: A scorecard judges; an instrument reads.

The framework behind the expected column is a set of three composite behavioral models. A composite model describes the aggregate personality of a structural role - the tendencies the role produces in whoever occupies it. The framework holds that structural incentives produce predictable aggregate behavior regardless of individual occupants. The three roles follow.

### 2.1. Appointees

Appointees are the committee's officers: the convener and the subgroup chairs, appointed without fixed terms under [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)<sup>[3]</sup>, exercising discretion over scheduling, polling, and consensus determination. The role achieves something real. The neutrality norm it enforces is what makes consensus sessions of two hundred participants workable, and the procedural fairness instinct it selects for is genuine.

The framework holds that long tenure without term limits merges the occupant's identity with the role, and that the merger produces a binary switch. Communications about technical substance - a design choice, an API shape, a measurement - receive collegial, proportionate engagement. Communications about governance, process, or institutional structure shift the register: Criticism of the institution arrives as criticism of the self, because the distance between the two has closed. The framework expects every claim of P4263R0 to land in the governance register, and it expects the response pattern to be a challenge to standing - "is this appropriate?" - in place of a challenge to correctness - "is this correct?"

### 2.2. Delegates

Delegates are the working membership: sent by employers and national bodies, expert within their own working group's domain, the electorate whose votes determine consensus. Their attention pattern is rational. A delegate cannot evaluate hundreds of papers a year, and selective depth plus social inference is the correct allocation of finite attention - the pattern political science names rational ignorance, declining to acquire information whose cost exceeds the value of the single vote it informs ([An Economic Theory of Democracy](https://archive.org/details/economictheoryof0000down)<sup>[4]</sup>). The consensus model was built to leverage exactly that allocation.

The framework holds that most communications never reach a delegate at all, that social inference substitutes for independent evaluation outside the home domain, and that the first framing a delegate encounters locks the default disposition. P4263R0 is a process paper outside every working group's domain. The framework expects most of its claims to reach delegates only as framed by others, when they reach them at all.

### 2.3. The Public

The public is everyone who writes C++ and cannot vote. The framework models it as roughly sixteen million working developers with a politically engaged core in the tens of thousands, reading trip reports, forums, and conference talks. Its pattern recognition is earned: The templates it applies encode a decade of shipped features and broken promises, and they are right often enough to function as the ecosystem's distributed early-warning system.

The framework holds that the public slots every communication into a pre-existing template before evaluating substance, that process papers draw little engagement unless they confirm an existing template, and that the one-sentence compression of a paper is what survives in collective memory. The framework expects P4263R0 to be received as confirmation of grievances already held rather than as novel analysis.

---

## 3. The Headline Binary

P4263R0 is an information paper. It requests no floor time, no polls, and no scheduling, so by default nothing happens. The headline binary concerns initiative, and it is the instrument's primary reading.

The four working groups - Library Evolution (LEWG), Evolution (EWG), Core (CWG), and Library (LWG) - administer the process that P4263R0's claims examine. A body with the capacity to self-correct, on discovering a documented analysis of its own potential failure modes, examines the analysis on its own initiative.

**B0 - expected:** No working group chair initiates examination of any claim in P4263R0.

**B0 - disconfirmer:** Any of the four working groups proactively opens discussion of any claim - whether the evidence behind the networking decision is in fact thin, whether the tournament incentive is in fact operative, or any other.

One branch follows from the framework's model of the governance register. The other demonstrates a capacity outside the framework's model. The paper assigns no meaning beyond the definitions.

**One branch will occur. The record will show which.**

---

## 4. The Eight Claims

Each subsection states one claim from P4263R0 and the columns for each cohort the claim reaches. Cohorts a claim does not reach are omitted.

### 4.1. The Thin Record

P4263R0 Section 3 asserts that the published evidence behind the networking claim in `std::execution` is empty: The unification of executors rests on one hypothetical code snippet, and the cells pairing twenty years of asynchronous claims with networking evidence are blank.

**Appointees - expected:** Procedural challenge ("this is relitigating settled decisions") or silence. The missing evidence is not produced. No specific factual error is identified.

**Appointees - disconfirmer:** The networking evidence the record lacks is produced in any public venue, or a specific factual error in the claim is identified. Either response fills a gap the record holds today.

**The public - expected:** Template match: committee dysfunction. The sentence "the networking cells are empty" circulates detached from its context.

**The public - disconfirmer:** Discussion engages the evidence question itself - what was polled, what was published - rather than the template.

### 4.2. The Tournament

P4263R0 Section 4 asserts that papers compete in a zero-sum tournament whose dominant strategy - the move that wins regardless of what others play - is to claim the largest domain on the least evidence. Thinness wins polls.

**Appointees - expected:** Dismissal as caricature ("papers are evaluated on their merits"), with the accuracy of the incentive analysis left unexamined.

**Appointees - disconfirmer:** The structural argument is engaged in a public venue: where the incentive analysis fails, or where it holds.

**The public - expected:** The vocal minority adopts "claim maximally, evidence minimally" as a slogan confirming what it already believes.

**The public - disconfirmer:** Discussion tests the incentive model against cases instead of repeating it.

### 4.3. The Chosen Game

P4263R0 Section 5 asserts that the tournament structure is self-authored: The ISO/IEC Directives impose nothing at the working group's interior, so the structure is a local construction, renewable and changeable by local authority with no ISO process.

**Appointees - expected:** Silence on the Directives analysis specifically. Redirection to practical constraints. The structure described as documentation of long-standing practice.

**Appointees - disconfirmer:** The Directives analysis is engaged on its merits: a demonstrated misreading, or public acknowledgment that the structure is locally authored and locally changeable.

**The public - expected:** The committee-serves-itself template activates. The sentence "a pathology chosen freely and renewable at will is a decision" circulates.

**The public - disconfirmer:** Pushback that the analysis over-reads the Directives' silence.

### 4.4. Three Rational Responses

P4263R0 Section 6 asserts that game theory predicts three responses to evidence supplied from outside the tournament - attack the volume, attack the provenance, go silent - and reports all three as already observed.

**Appointees - expected:** The analysis is characterized as unfalsifiable - a construction in which any response confirms the model - and the documented response patterns continue.

**Appointees - disconfirmer:** A specific claim from the corpus is engaged on its substance: the one response the analysis says the structure does not reward.

This paper is itself unfalsifiable by construction and states the property openly in Section 7. The concession removes the trap. The definitions are the paper's entire claim.

**The public - expected:** The analysis is shared as spectacle.

**The public - disconfirmer:** The game-theoretic argument is critiqued on its merits - the dominant-strategy claim tested, not enjoyed.

### 4.5. A Dead Player

P4263R0 Section 7 asserts, borrowing the vocabulary of Samo Burja's [Great Founder Theory](https://samoburja.com/gft/)<sup>[5]</sup> - in which a live player reasons from first principles while a dead player executes inherited scripts - that the committee performs the ceremonies of evidence without the principles that generated them.

**Appointees - expected:** A vitality defense anchored to numbers - standards shipped on schedule, attendance counts - delivered in the indignation register. The underlying question, whether the institution can examine itself, goes unengaged.

**Appointees - disconfirmer:** Any officer publicly engages the question of whether the ceremonies still serve their generating principles. The engagement is the disconfirmer regardless of the conclusion reached.

**The public - expected:** The strongest template available: The committee is fundamentally broken. Reception splits by career stage, with early-career readers validated and established readers threatened.

**The public - disconfirmer:** The dead-player frame is evaluated as a model rather than adopted as a verdict or dismissed as an insult.

### 4.6. Ask For Nothing As Strategy

P4263R0 Section 9 asserts that information-only papers that ask for nothing are the one move the tournament cannot process: They request nothing that can be denied, compete for nothing that can be lost, and sit in the permanent record either way.

**Appointees - expected:** The strategy disclosure is cited as evidence of adversarial intent - a campaign, not scholarship - and discussion centers on the author rather than the claims.

**Appointees - disconfirmer:** The claims are evaluated independently of the strategy that delivered them.

**Delegates - expected:** Disposition follows the first framing encountered, and the structure positions appointees to set it.

**Delegates - disconfirmer:** A delegate forms a position traceable to the paper's content: a public comment or paper referencing specific sections.

**The public - expected:** The platform sets the register. One venue reads the disclosure as honesty and gamesmanship; another debates its legitimacy.

**The public - disconfirmer:** The venues converge on reading the disclosure as manipulation.

### 4.7. The Wager

P4263R0 Section 11 declares its program's term: C++29 is when the committee's answer on networking comes due, against a published record of benchmarks, working implementations, and dated decisions. If the shipped answer matches or exceeds the working implementations, the author's predictions are scored wrong in public by the same method the corpus applies to everyone else.

**Appointees - expected:** The falsification criteria are read as presumption - who sets terms for the committee? - and the incumbent model is defended on precedent, labeled alternatives, and the shipped artifact.

**Appointees - disconfirmer:** The wager's discipline - dated predictions with stated criteria - is acknowledged as legitimate accountability, with or without agreement on the outcome.

**Delegates - expected:** Position follows the expert signal. Absent one, no position forms.

**Delegates - disconfirmer:** The wager's terms are evaluated independently in public.

**The public - expected:** The accountability framing resonates, then attention decays well before resolution.

**The public - disconfirmer:** The wager is tracked beyond one news cycle.

### 4.8. What the Author Wants

P4263R0 Section 13 states four conditions under which its corpus would stop being necessary - a symmetric evidence bar, examinable decision records, output bounded by absorption, reconciliation as the operating mode - and notes that every one is already permitted.

**Appointees - expected:** The conditions are read as demands ("he says he asks for nothing, but this is clearly an ask") and converted into committee homework ("bring a proposal we can poll").

**Appointees - disconfirmer:** A condition is examined as a condition: what a symmetric evidence bar would require, discussed without routing the question back to the author as an ask.

**The public - expected:** Instinctive agreement with all four conditions.

**The public - disconfirmer:** Substantive critique of any condition - that absorption-bounded output starves urgent domains, for example.

---

## 5. Rhetorical Approaches

A political assertion dressed as a claim is a sentence with the surface grammar of an evaluation - truth conditions, checkable content - whose working function is positional: It defends standing, shifts burden, or converts substance into procedure. "It works today" sounds like evidence and functions as burden-shift. "Not a single person I have spoken with agrees" sounds like data and is unverifiable by construction, because the conversations are private. The framework catalogs these grammars as named verbal moves. Each move has a trigger, a sentence-level structure, and a function the surface conceals.

The catalog below is extracted from the public communications record of senior committee members: eighteen years of trip reports, recorded conference sessions, community question-and-answer sessions, and blog posts. It is presented as a structural model of senior-member rhetoric. The expectation is conditional: If a senior member responds publicly to a claim, the framework expects the response to instantiate the paired move. Silence is measured by the headline binary and Claim 4, never by this catalog.

Every utterance below is synthetic - expected speech, modeled on the documented register. The utterances retain contractions because they depict speech.

**praise-then-pivot** - [genuine compliment] + ["at the same time"] + [criterion shift onto ground where the speaker's position wins]. Target: Claim 6.

- "Vinnie is one of the most productive library authors this community has - nobody doubts the work ethic. At the same time, it's really important to talk about what moves the committee forward, and that's proposals the room can act on."
- "There's real energy in these papers and real research behind them. And the question that matters is adoptability and impact: What here can a working group actually use?"

**concession-reframe** - [quote the concern precisely] + [validate it] + [show it does not change the conclusion]. Target: Claim 8.

- "Better decision records are a good idea - I'm all for them. But they're not the answer to how we ship C++29 on schedule."
- "A symmetric evidence bar sounds right in principle, and we should always ask for evidence. That doesn't change the fact that the committee evaluated what was before it and reached consensus."

**administrative-framing** - [describe structural power as housekeeping] + [relocate agency to the room]. Target: Claim 3.

- "The convener's job is to convene meetings - say when and where we meet - and to determine consensus. It's administrative. The room makes the decisions."
- "SD-4 isn't a rulebook anyone imposed. It just writes down how the committee has always worked, so newcomers don't have to learn it by osmosis."

**disclaimer-then-claim** - [perfunctory hedge, weight inversely proportional to the claim] + [substantive intervention]. Target: Claim 5.

- "It's not really my place to respond to this - I'm just one retired chair - but the institution described in this paper is not one I recognize, and I was in the room for twenty years."
- "I don't usually engage with process meta-commentary, and this isn't the most important thing, but: A committee that ships on schedule for fifteen years is performing its function."

**number-anchored-thesis** - [declarative thesis anchored to a specific number] + [trailing hedge]. Target: Claim 5.

- "Five standards in fifteen years, every one on time. That is not what a dead institution looks like, I think."
- "Two hundred attendees from thirty-one nations at the last meeting. The committee has never been more alive, as far as I can see."

**tripartite-scaffold** - [historical precedent with timeline] + [labeled alternatives, one obviously superior] + [shipped artifact]. Target: Claim 7.

- "We've been here before: The Networking TS spent a decade in flight and never converged. For C++29 there are three paths: a second async model that fragments the ecosystem, no networking again, or networking on the model we already shipped - which runs in production today."
- "Python took twelve years to recover from a compatibility break. Our choices: two competing async foundations in one standard, another decade of nothing, or building on std::execution, which works today."

**demand-concrete-alternative** - [acknowledge the critique] + [require a proposal before discussion]. Target: Claim 2.

- "If the incentive structure is wrong, what's the concrete alternative? We can only evaluate proposals that are before us."
- "'The tournament rewards over-claiming' - okay. Until that becomes a tad more concrete - a specific process change in a paper we can poll - we are going to proceed with the process we have."

**existence-proof** - [assert the artifact works today] + [shift the burden to whoever lacks a demo]. Target: Claim 1.

- "std::execution is in the working draft, it has a reference implementation, and it runs in production at a major trading firm today. The evidence question answers itself."
- "The model ships. It works today. If someone believes it cannot do networking, the burden is on them to show the failure, not on the committee to re-prove the success."

**pragmatic-close** - [specific next action, never a summary] + [register shift to personal]. Target: Claim 8.

- "Would it be possible for the author to bring the evidence-bar idea as a concrete proposal to the next telecon? I'd love to see it polled properly. Let's dig in."
- "I think the right next step is simple: Pick the one condition that matters most, write the two-page paper, and let the room decide. Does that help?"
- Function: converts conditions into committee homework, routing them back into the tournament whose rules the conditions decline to play by.

**bikeshed-shutdown** - [reframe the discussion as time cost] + [user-trust appeal]. Target: Claim 6.

- "Every hour we spend debating who may file papers and why is an hour not spent on C++29. If we can't handle this gracefully, why should our users trust us with their language?"
- "The list has spent two weeks on the ethics of info papers. Our users are waiting for networking. Can we get back to work?"

**style-over-substance** - [aesthetic condemnation of the work as a category] + [zero engagement with any specific finding]. Target: Claim 1.

- "These retrospectives don't read like engineering papers; they read like legal briefs. That's not how this community communicates."
- "I skimmed a few. The tone is prosecutorial and the framing is conspiratorial. I didn't find them a productive use of my time."
- Signature: No specific factual error appears in either utterance. The absence is the diagnostic.

**consensus-manufacture** - [unverifiable collective attribution]. Target: Claim 4.

- "I've spoken with a lot of members about this, and not a single person reads those events the way the paper does."
- "The only discussion among the chairs has been concern for the author, not hostility. Everyone wants the same thing here."
- Function: The claimed consensus can be neither verified nor refuted, because the conversations are private and the minutes are sealed.

**sheep-dipping** - [private channel] + [warmth and concern for the target's reputation] + [directive whose outcome serves the speaker]. Target: Claim 4.

- Private email: "I'm writing as a friend, not in any official capacity. The papers are becoming the story instead of the work, and people I respect are starting to tune you out. I'd hate to see that happen to someone with your talent."
- Hallway: "You know I want the networking work to succeed. That's exactly why I'd slow down on the process papers - they make it easier for people to dismiss the technical contribution."

**channel-convergence** - [the same recommended outcome across multiple channels and audiences, each message individually warm]. Target: Claim 4.

- A public reply praising the author's energy while suggesting consolidation; a private email recommending fewer, deeper papers; the same advice relayed through a third party in the hallway. Three channels, one outcome: reduce.
- A trip report noting that paper volume is straining review capacity, naming no one, paired with a private note to the author: "you'd have more impact with two papers than twenty."

**correction-then-teaching** - [curt correction] + [warmth, access, and teaching arriving only after compliance]. Target: Claim 8.

- "No. That's not how consensus works here." Then, after the author softens: "This version is much better. Happy to walk you through how to get networking onto the schedule."
- "Now that the papers are focused, let me introduce you to the people who can actually move this. You've earned the room's attention back."
- Signature: The teaching is the reward for submission. It arrives after compliance, and arrives nowhere else.

**dismissal-with-humor** - [joke that reframes the claim as ammunition for an out-group]. Target: Claim 5.

- "'WG21 is a dead player' - that's a perfect pull quote for a Rust poster."
- "Maybe we can get 'the ceremonies survived the principles' on a T-shirt for the next conference. The competition will love it."

**parable-prescription** - [story of a dissenter who lost, complied, did the work, and was vindicated] + [prescription: wait for history]. Target: Claim 6.

- "The model for dissent here is the engineer who opposed export templates, lost the vote, implemented the feature anyway, and was vindicated when it was removed years later. Dissent, accept the outcome, do the work, and let history judge."
- "If the coroutine model is right, time will prove it the way it proved the export skeptics right - through implementation experience, not through papers about the committee."

**institutional-language-shift** - [frustration expressed as institutional embarrassment in place of personal attack]. Target: Claim 6.

- "This thread is exactly what people parody when they talk about 'design by committee.'"
- "We are becoming the story. A standards body that spends its energy on meta-debate is not one our users can take seriously."
- Signature: The shift from technical register to institutional embarrassment marks the point where the speaker has stopped arguing and started managing.

---

## 6. What This Paper Claims

This paper claims exactly three things.

1. Each binary is exhaustive: One branch must occur.
2. Each branch is observable in public venues.
3. The framework that generates the expected column is disclosed above.

Everything else belongs to the reader: the framework's correctness, the meaning of any outcome, and what any branch says about any person. The binaries describe aggregate behavior in structural roles. Non-response is one branch of a binary - a defined, measured outcome. Engagement prompted by this paper is engagement; the disconfirming column registers prompted self-correction at full value. The record is complete as published.

---

## 7. Reading the Instrument

**Exhaustiveness.** Each binary in this paper is exhaustive: Exactly one branch will occur. The paper is therefore unfalsifiable by construction, and says so here. An instrument is not a hypothesis. It does not bet; it partitions.

**Observability.** Every branch is defined against public venues: mailing papers, trip reports, conference talks, public forums, published meeting records. Sealed venues - the reflectors, wikis, and minutes that may not be quoted publicly under [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)<sup>[3]</sup> - sit outside every binary. Every branch can be read without quoting sealed material.

**Hierarchy.** Silence is measured by the headline binary and by Claim 4. Public speech is measured by the claim binaries and by the move catalog: A response either instantiates the paired move or it does not. Silence, response-with-move, and response-without-move cover the outcome space.

**No scorekeeper.** The public record and the tables below are sufficient for any reader at any time.

### "The disconfirmers are unreachable."

The strongest objection to this instrument is that its disconfirming column is constructed to never fire. The column's contents say otherwise: producing evidence, identifying a factual error, writing a response paper, discussing a topic in session, evaluating a claim on its merits. Each is ordinary committee behavior, performed daily on technical questions. The disconfirming column asks for nothing the committee does not already do in the technical domain. The instrument measures whether the same behavior crosses into the governance domain - which is precisely the binary switch the framework describes.

### The Binary Table

Branch labels below are compressed; the governing definitions are in Sections 3 and 4.

| ID  | Claim            | Cohort     | Expected                             | Disconfirmer                     |
| :-- | :--------------- | :--------- | :----------------------------------- | :------------------------------- |
| B0  | All (initiative) | Appointees | No WG opens examination              | Any WG opens it                  |
| B1a | Thin record      | Appointees | Challenge or silence                 | Evidence produced or error named |
| B1b | Thin record      | Public     | Template match                       | Evidence question engaged        |
| B2a | Tournament       | Appointees | Dismissed as caricature              | Structural engagement            |
| B2b | Tournament       | Public     | Slogan adoption                      | Model tested against cases       |
| B3a | Chosen game      | Appointees | Silence on the analysis              | Directives engaged on merits     |
| B3b | Chosen game      | Public     | Template confirmation                | Over-reading pushback            |
| B4a | Three responses  | Appointees | Unfalsifiable charge, patterns hold  | A claim engaged on substance     |
| B4b | Three responses  | Public     | Shared as spectacle                  | Argument critiqued on merits     |
| B5a | Dead player      | Appointees | Vitality numbers, question unengaged | The question engaged             |
| B5b | Dead player      | Public     | Strongest template match             | Frame evaluated as model         |
| B6a | Strategy         | Appointees | Disclosure cited as intent           | Claims evaluated independently   |
| B6b | Strategy         | Delegates  | First framing holds                  | Independent position surfaces    |
| B6c | Strategy         | Public     | Honesty and gamesmanship             | Read as manipulation             |
| B7a | Wager            | Appointees | Presumption framing                  | Discipline acknowledged          |
| B7b | Wager            | Delegates  | Expert signal or nothing             | Terms evaluated independently    |
| B7c | Wager            | Public     | Resonance, then decay                | Sustained tracking               |
| B8a | Conditions       | Appointees | Read as demands                      | Examined as conditions           |
| B8b | Conditions       | Public     | Instinctive agreement                | A condition critiqued            |

### The Move Index

If a public response to a claim arrives, it either instantiates the paired move or it does not. Both are observable.

| Move                         | Target  |
| :--------------------------- | :------ |
| praise-then-pivot            | Claim 6 |
| concession-reframe           | Claim 8 |
| administrative-framing       | Claim 3 |
| disclaimer-then-claim        | Claim 5 |
| number-anchored-thesis       | Claim 5 |
| tripartite-scaffold          | Claim 7 |
| demand-concrete-alternative  | Claim 2 |
| existence-proof              | Claim 1 |
| pragmatic-close              | Claim 8 |
| bikeshed-shutdown            | Claim 6 |
| style-over-substance         | Claim 1 |
| consensus-manufacture        | Claim 4 |
| sheep-dipping                | Claim 4 |
| channel-convergence          | Claim 4 |
| correction-then-teaching     | Claim 8 |
| dismissal-with-humor         | Claim 5 |
| parable-prescription         | Claim 6 |
| institutional-language-shift | Claim 6 |

---

## 8. The Invitation

The reader is invited to observe. The committee's capacity to self-correct is measured by what happens next, and what happens next belongs entirely to the committee. The instrument is now part of the record it measures.

**The disconfirming column is a door. It opens from the inside.**

---

## Acknowledgments

Thanks to Samo Burja for the *Great Founder Theory* framework, whose live-player and dead-player vocabulary Claim 5 summarizes.

---

## References

[1] [P4263R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4263r0.pdf) - "Why I Write" (Vinnie Falco, 2026).

[2] [P4047R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4047r0.pdf) - "CRYSTAL BALL: Checking Predictions Against the Record" (Vinnie Falco, 2026).

[3] [SD-4: WG21 Practices and Procedures](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) (Standing Document, isocpp.org).

[4] [An Economic Theory of Democracy](https://archive.org/details/economictheoryof0000down) - Anthony Downs, 1957.

[5] [Great Founder Theory](https://samoburja.com/gft/) - Samo Burja, 2020.
