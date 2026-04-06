---
title: "Failure Modes in Large-Scale Standardization"
document: P4050R0
date: 2026-03-16
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
  - "C++ Alliance Proposal Team"
audience: WG21
---

## Abstract

WG21 produces poll numbers. It does not produce decision records.

This paper extracts fourteen failure modes from the executor and networking arc, generalizes them, and proposes proportional deliberation - a framework of decision sizing, missing artifacts, domain coverage, and tooling that gives the chair structured tools for running sessions where the process scales with the consequence. The executor arc is the case study. The failure modes and the framework are general.

---

## Revision History

### R0: March 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

This paper is independent of the Network Endeavor ([P4100R0](https://wg21.link/p4100r0)<sup>[26]</sup>). It draws its case study from the executor and networking arc documented in five companion retrospectives ([P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> through [P4098R0](https://wg21.link/p4098r0)<sup>[5]</sup>), but its findings are general. The failure modes apply to any multi-year, multi-author standardization effort - contracts, reflection, modules, or whatever comes next.

The author developed and maintains [Corosio](https://github.com/cppalliance/corosio)<sup>[6]</sup> and [Capy](https://github.com/cppalliance/capy)<sup>[7]</sup> and is a co-author of [P2469R0](https://wg21.link/p2469r0)<sup>[8]</sup>. The failure modes are presented as general patterns, not as criticisms of individuals. Every decision in the arc was made by experienced practitioners under real constraints. The intent is to give the committee - and especially its chairs - better tools, not a verdict.

---

## 2. The Problem

The chair walks into a session with a paper, a room full of people, and a time slot. The chair may not be a domain expert in the paper being discussed. The chair has no structured way to know how consequential the decision is, whether the affected domains have practitioners present, or what artifacts should exist before the poll is taken. The chair calls the poll. The result is recorded: SF:24 / WF:16 / N:3 / WA:6 / SA:3. The reasoning behind the result is not recorded. The alternatives considered are not recorded. The dissenting views are not recorded. The conditions for revisiting the decision are not recorded.

A decision that sets aside years of work gets the same process as a decision to add `[[nodiscard]]` to a function. The consequence varies by orders of magnitude. The process does not scale. The chair has no tools to scale it.

The executor and networking arc is the case study. Over a decade, four locally reasonable decisions - each made by experienced practitioners under real constraints - produced twenty-one years without networking in the C++ standard, counting from [N1925](https://wg21.link/n1925)<sup>[15]</sup> (2005). The failure modes extracted from that arc are general. The proposals in this paper are tools for the chair.

---

## 3. The Case Study

Five retrospective papers ([P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup>, [P4095R0](https://wg21.link/p4095r0)<sup>[2]</sup>, [P4096R0](https://wg21.link/p4096r0)<sup>[3]</sup>, [P4097R0](https://wg21.link/p4097r0)<sup>[4]</sup>, [P4098R0](https://wg21.link/p4098r0)<sup>[5]</sup>) examined four decision points in the executor and networking arc. This section presents the fourteen failure modes they identified, organized into five categories.

| Category           | What goes wrong                                                             |
| ------------------ | --------------------------------------------------------------------------- |
| Evidence           | Assertions shape decisions without prototypes, surveys, or measurements     |
| Knowledge transfer | Design rationale drops out when papers change hands                         |
| Scope management   | Coupling blocks independent delivery; iteration costs compound              |
| Analytical framing | Analysis under one framing misses conclusions visible under another         |
| Governance         | Decisions proceed without consensus or without evaluating cost to all domains |

### Category A: Evidence

**A1. Unification without prototype.** Three deployed executor models were unified into [P0443R0](https://wg21.link/p0443r0)<sup>[9]</sup> (2016) with no prototype demonstrating the unified model working across all three domains. The unified model was never deployed as unified. It was replaced by [P2300R10](https://wg21.link/p2300r10)<sup>[10]</sup>. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 4; Section 5.5.

**A2. Assertions supported by hypothetical code only.** Six rationale assertions for unification were supported by one hypothetical code snippet as the only code-level evidence in the entire published record. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 4.

**A3. Consensus poll on a claim without domain-specific evidence.** The October 2021 poll "including networking" achieved consensus ([P2453R0](https://wg21.link/p2453r0)<sup>[25]</sup>). At the time, the published record contained no sender-based networking deployment, no prototype, and one hypothetical example. Published voter comments included "can't judge its suitability for networking" from voters who voted Weakly Favor. [P2430R0](https://wg21.link/p2430r0)<sup>[11]</sup>, documenting that compound I/O results cannot use `set_error` without information loss, was published two months before the poll. *Source:* [P4097R0](https://wg21.link/p4097r0)<sup>[4]</sup> Sections 2-3.

**A4. Predictions without follow-up.** [P2464R0](https://wg21.link/p2464r0)<sup>[12]</sup> stated "I don't know" whether Networking TS compositions scale. Five years later, no sender-based networking has shipped either. The constraint applied to one model was not applied symmetrically to the replacement. *Source:* [P4096R0](https://wg21.link/p4096r0)<sup>[3]</sup> Section 9.1.

### Category B: Knowledge Transfer

**B1. Design rationale lost across paper boundaries.** The continuation framing was established in [P0113R0](https://wg21.link/p0113r0)<sup>[13]</sup> (2015). It was carried by institutional knowledge rather than by the API surface or the type system. When the property hint was removed in 2019 by authors who inherited the API surface but not the conceptual model, the framing dropped out. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 6.3.

**B2. Terminology drift erasing a conceptual model.** `dispatch`/`post`/`defer` became `execute(F&&)` across seven papers over five years. Each rename was locally reasonable. The cumulative effect was that the continuation framing was no longer visible on the API surface. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 6.1.

### Category C: Scope Management

**C1. Coupling that blocks independent delivery.** [P1256R0](https://wg21.link/p1256r0)<sup>[14]</sup> (2018): "SG1 has decided that the Networking TS should not be merged into the C++ working paper before executors go in." Executors went through fourteen revisions and were replaced. Networking waited. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 5.1.

**C2. Iteration cost of an ill-posed problem.** [P0443](https://wg21.link/p0443)<sup>[9]</sup> went through fourteen revisions. More than 100 papers were produced. A property system was built and then discarded entirely. The unified model was never deployed. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 5.2.

### Category D: Analytical Framing

**D1. Pivotal analysis under one framing only.** [P1525R0](https://wg21.link/p1525r0)<sup>[16]</sup> identified four deficiencies in `execute(F&&)`. The analysis was under the work framing only. Under the continuation framing, three deficiencies do not arise and the fourth addresses a different question. *Source:* [P4095R0](https://wg21.link/p4095r0)<sup>[2]</sup> Section 4.

**D2. Pivoting without evaluating cost to the blocked domain.** The Cologne pivot (July 2019), driven by [P1658R0](https://wg21.link/p1658r0)<sup>[17]</sup> and [P1660R0](https://wg21.link/p1660r0)<sup>[18]</sup>, eliminated all interface-changing properties. No paper at Cologne analyzed the diagnosis under the continuation framing. No paper asked what networking loses. *Source:* [P4095R0](https://wg21.link/p4095r0)<sup>[2]</sup> Section 5.2.

**D3. Absence of the blocked domain's use cases from the pivotal analysis.** [P1525R0](https://wg21.link/p1525r0)<sup>[16]</sup>'s examples are thread pools, deadline executors, GPU contexts, and `when_all`. No example involves an I/O reactor or sockets. *Source:* [P4095R0](https://wg21.link/p4095r0)<sup>[2]</sup> Section 3.3.

**D4. Treating properties of the API surface as inherent properties of the domain.** The three deficiencies [P2464R0](https://wg21.link/p2464r0)<sup>[12]</sup> identified are properties of the `execute(F&&)` signature, not inherent to executor-based async. The coroutine executor constrains the argument type and eliminates those deficiencies. *Source:* [P4096R0](https://wg21.link/p4096r0)<sup>[3]</sup> Section 3.

### Category E: Governance

**E1. Proceeding without consensus on the foundational premise.** The "one grand unified model" poll achieved SF:4/WF:9/N:5/WA:5/SA:1 - no consensus, leaning in favor. The committee proceeded with a decade-long design commitment. *Source:* [P4094R0](https://wg21.link/p4094r0)<sup>[1]</sup> Section 5.6.

**E2. Evidence bar applied non-uniformly across claims.** The GPU and infrastructure evidence is real. The networking evidence column is empty for most claims. Both categories shaped committee decisions. *Source:* [P4098R0](https://wg21.link/p4098r0)<sup>[5]</sup> Section 3.

---

## 4. Generalizing the Failure Modes

The failure modes in Section 3 are specific to the executor arc. This section extracts the general pattern from each.

### 4.1 Already General

Eight of the fourteen failure modes need no transformation. They apply as stated to any multi-year standardization effort:

- **A2.** Assertions without deployed evidence
- **A4.** Predictions without follow-up
- **B1.** Design rationale lost across paper boundaries
- **B2.** Terminology drift erasing a conceptual model
- **C1.** Coupling that blocks independent delivery
- **C2.** Iteration without deployment
- **E1.** Proceeding without consensus on the foundational premise
- **E2.** Evidence bar applied non-uniformly across claims

### 4.2 Transformation

Six of the fourteen failure modes are specific to the executor arc. The following table extracts the general pattern.

| #  | Executor-Arc Instance                         | General Form                                                            | Why the Step                                                                                                                  |
| -- | --------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| A1 | Unification without prototype                 | Architecture chosen without working demonstration                       | The arc is about unification; the general mode is choosing any architecture without building it first                         |
| A3 | Bundled-domain consensus                      | Poll where evidence covers some domains but not others                  | The arc bundled networking with GPU/parallelism; the general mode is any poll with uneven evidence                            |
| D1 | Pivotal analysis under one framing            | Direction set by analysis examining only one interpretation             | The arc had work vs. continuation; the general mode is any unexamined alternative interpretation                              |
| D2 | Pivot without domain-cost evaluation          | Direction change evaluated for domains it helps, not domains it affects | The arc affected networking; the general mode is any pivot where cost falls on unrepresented stakeholders                     |
| D3 | Blocked domain absent from analysis           | Affected stakeholders absent from the driving analysis                  | The arc had networking absent from P1525R0; the general mode is any decision where those who pay the cost are not represented |
| D4 | API properties mistaken for domain properties | Design limitations attributed to the problem domain                     | The arc attributed `execute(F&&)` deficiencies to the domain; the general mode is any diagnosis that forecloses alternatives  |

---

## 5. Proportional Deliberation

The fourteen failure modes share a root cause. WG21 has no proportional-deliberation requirement. A decision that sets aside years of work gets the same process as a decision to rename a function. This section proposes a framework that scales the process with the consequence.

### 5.1 Decision Sizing

The documentation requirement must scale with the consequence. Scaling requires a shared measure. The sizing system is based on observable properties of the decision - things you can count, not things you argue about.

| Criterion                   | What to count                                                         | Why it matters                                |
| --------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| Prior work affected         | Years from first proposal to present                                  | More years = more sunk cost at risk           |
| Paper chain depth           | Number of published papers in the dependency chain                    | More papers = more institutional investment   |
| Deployed codebases affected | Number of production deployments that depend on the current direction | More deployments = more real-world disruption |
| Reversibility               | Can the decision be undone in a future standard?                      | Irreversible decisions need more scrutiny     |
| Domain breadth              | Number of distinct domains affected                                   | More domains = more stakeholders to consult   |

These criteria combine into four tiers, each with its own documentation requirement.

| Tier | Name        | Criteria                                                                                    | Required artifacts                                                                                                                 | Example                                              |
| ---- | ----------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1    | Routine     | One paper, no deployed code, reversible, single domain                                      | The paper itself                                                                                                                   | Adding `[[nodiscard]]` to a function                 |
| 2    | Significant | Multiple papers or one deployed codebase, single domain                                     | Stakeholder brief + evidence summary + reflector discussion                                                                        | Adopting a new library feature with deployment history |
| 3    | Major       | Years of prior work, multiple deployed codebases, or multiple domains; partially reversible | Full artifact set (5.3); domain coverage report (Section 6)                                                                        | Adopting `std::execution` for C++26 ([N4985](https://wg21.link/n4985)<sup>[27]</sup>) |
| 4    | Structural  | Sets aside or replaces years of prior work; multiple domains; effectively irreversible      | Full artifact set + mandatory stakeholder presence or written position + decision rationale + follow-up criteria with revisit date | Setting aside the Networking TS; the Cologne pivot   |

Four design choices keep the sizing system from becoming a political instrument.

| Design choice                     | How it works                                                                                                                                  | Why                                                                                                          |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Observable criteria, not judgment | Tier determined by countable properties (years, papers, deployments, domains)                                                                 | If the tier depends on opinion, the sizing is political. If it depends on counts, the sizing is factual.     |
| Highest criterion governs         | A decision that meets Tier 4 on any single criterion is Tier 4                                                                                | Prevents undersizing by averaging. 20 years of deployed code is Tier 4 even if only one domain is affected.  |
| Author proposes, chair decides    | Paper author includes `decision-tier: N` in the paper. Chair can override. Disagreement resolved by a quick poll before the substantive poll. | The author knows the domain. The chair knows the process. Quick poll resolves edge cases.                    |
| Four tiers, not continuous        | Coarse enough that most decisions fall obviously into one tier                                                                                 | A 1-10 scale invites argument over whether something is a 6 or a 7. Four tiers have clear boundaries.        |

### 5.2 The Chair's Brief

The chair may not be a domain expert. The chair needs a one-page summary before the session that answers: What tier is this decision? What artifacts exist? What artifacts are missing? Which stakeholders are registered? Which are present? Which submitted written positions?

The chair's brief is produced from the stakeholder registry (Section 6) and the artifact checklist. For Tier 1, the brief is trivial - the paper itself is the brief. For Tier 4, the brief is a structured document that tells the chair what the room has and what it lacks before the first speaker stands up.

By the time the meeting starts, the chair already knows the decision's size, the stakeholder coverage, and the artifact gaps. The session is the closing argument. The deliberation happened before.

### 5.3 The Missing Artifacts

**F1. Missing artifacts disproportionate to the decision.** A Tier 4 decision proceeds with the same documentation as a Tier 1 decision. The artifacts that would have surfaced objections, alternatives, or gaps in evidence do not exist because nobody was required to produce them.

Eight artifacts WG21 does not systematically produce. The table maps each artifact to the tier at which it becomes required.

| Artifact                         | What it contains                                                                         | When produced            | Who produces it                                | WG21 today                                          | Required at tier |
| -------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------ | ---------------------------------------------- | --------------------------------------------------- | ---------------- |
| Stakeholder brief                | Affected parties' analysis of impact on their domain                                     | Before the meeting       | Each affected stakeholder                      | Nothing structured                                  | 2+               |
| Evidence summary                 | Deployments, prototypes, surveys, measurements for and against                           | Before the meeting       | Paper author + stakeholders                    | Inconsistent; some papers have data, some have none | 2+               |
| Pre-meeting reflector discussion | Structured exchange testing the analysis and raising objections                           | Weeks before the meeting | All interested parties                         | Informal and inconsistent                           | 2+               |
| Counteranalysis                  | Structured response examining the proposal under alternative framings                    | Before the meeting       | Affected stakeholders or independent reviewers | Reactive response papers, unstructured              | 3+               |
| Decision rationale               | Why the committee voted as it did - reasoning, alternatives considered, dissenting views | After the vote           | Chair or designated recorder                   | Poll numbers only                                   | 3+               |
| Dissent record                   | Specific objections of those who voted against, in their own words                       | After the vote           | The dissenters                                 | Nothing structured                                  | 3+               |
| Follow-up criteria               | Conditions under which the committee will revisit the decision                           | At the time of the vote  | Chair or paper author                          | Nothing; no decision has a built-in revisit trigger | 4                |
| Impact assessment                | What existing work, deployed code, or in-progress proposals are affected                 | Before the vote          | Paper author or chair                          | Nothing structured                                  | 3+               |

### 5.4 Hypothetical: P2464R0 (Networking TS Removal)

Decision sizing: 13 years of prior work (Tier 4). 100+ papers in the chain (Tier 4). Boost.Asio deployed for 15+ years (Tier 4). Effectively irreversible (Tier 4). Multiple domains (Tier 4). **Tier 4 on every criterion.**

| Artifact                         | What existed in 2021                                                    | What Tier 4 requires                                                                                  |
| -------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Stakeholder brief                | None. Kohlhoff was credited in acknowledgments but no structured brief. | Written briefs from Kohlhoff, the Networking TS authors, and affected national bodies.                |
| Evidence summary                 | P2464R0 itself. No deployment data for sender-based networking.         | Published evidence for and against, from both sides.                                                  |
| Pre-meeting reflector discussion | Not documented in the published record.                                 | Structured reflector exchange completed weeks before the session.                                      |
| Counteranalysis                  | P2469R0 (reactive, published after P2464R0).                            | Structured response examining P2464R0 under the continuation framing.                                 |
| Decision rationale               | Poll numbers only.                                                      | Why the committee agreed. What alternatives were considered. What the dissenting views were.           |
| Dissent record                   | None.                                                                   | SA voters' specific objections, in their own words.                                                   |
| Follow-up criteria               | None.                                                                   | "Revisit in 3 years if no sender-based networking prototype has been published."                      |
| Impact assessment                | None.                                                                   | Networking TS (ISO TS, 2018). Boost.Asio (15+ years). Boost.Beast (2017). Affected national bodies.  |

### 5.5 Hypothetical: Sofia Task Adoption (P3552R3)

Decision sizing: [P3552R3](https://wg21.link/p3552r3)<sup>[28]</sup> is new (Tier 1-2 on prior work). But it affects `std::execution` (years of prior work, Tier 3). Multiple domains (Tier 3). Partially reversible via NB comments (Tier 2-3). **Tier 3 by highest criterion.**

Jonathan M&uuml;ller's [P3801R0](https://wg21.link/p3801r0)<sup>[24]</sup> arrived after the Sofia vote. Under Tier 3 requirements, his concerns would have been a stakeholder brief before the vote. The 29 abstentions might have been fewer - people who abstained because they did not understand the issues would have had written briefs to read. The plenary vote passed 77-11. The record does not document why 29 members abstained.

---

## 6. Domain Coverage

### 6.1 The Problem

A poll records how many people voted each way. It does not record whether the affected domains had practitioners present. One hundred generalists voting on a networking question and five networking practitioners voting on a networking question produce the same output format. The information content is not the same.

Howard Hinnant described the consequence on the WG21 reflector: a key stakeholder was absent from the session where `std::variant` was discussed, and the decision's trajectory changed. Christopher Kohlhoff - the person whose domain is most affected by networking decisions - was not always present when networking-adjacent decisions were made. The committee proceeded.

### 6.2 Two Failure Modes

**G1. Decision without domain coverage.** Before a consequential vote, does the record show which domains are represented among the voters and which are not?

**G2. Absent stakeholder on a consequential decision.** Before a consequential vote, has the committee verified that identified stakeholders are present or have submitted their position in writing?

### 6.3 The Stakeholder Registry

Six design choices make the registry lightweight enough to use and resistant to gaming.

| Design choice                             | How it works                                                                                                                                                                                                                                                                                                                                                  | Why                                                                                                                                                                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Self-registration, not credentialing      | Stakeholders declare their own relationship to the domain. Nobody certifies anyone.                                                                                                                                                                                                                                                                           | The committee has no credentialing body and should not create one. Self-declaration avoids the "who decides who is qualified" problem. Social accountability does the work - the community knows who has built what.              |
| Attached to the paper, not to the person  | Domain relevance is per-decision. A networking expert may have no stake in a contracts decision. Registration is scoped to the paper.                                                                                                                                                                                                                         | Avoids permanent labels. Domain relevance is contextual.                                                                                                                                                                         |
| Open issue or reflector thread per paper  | Stakeholders self-register by posting: name and domain relationship ("I have deployed in this domain" / "I have authored papers in this domain" / "I am evaluating from outside this domain").                                                                                                                                                                | Uses existing infrastructure. No new tools needed for the minimum viable version.                                                                                                                                                |
| Chair's pre-meeting report                | For each affected domain: how many registered stakeholders are present? How many submitted written positions? This is metadata on the agenda item.                                                                                                                                                                                                            | The chair already prepares the agenda. The report adds one artifact.                                                                                                                                                             |
| Domain coverage attached to the poll record | "SF:24/WF:16/N:3/WA:6/SA:3; of 3 self-registered networking practitioners, distribution was F:1/SA:2."                                                                                                                                                                                                                                                      | The poll result plus the coverage distribution is more informative than the poll result alone. The committee interprets the coverage. The record preserves it.                                                                    |
| Continuous scaling                        | For trivial decisions, the registry is empty and nobody registers - that is the correct outcome. For consequential decisions, the affected stakeholders register and the coverage is visible.                                                                                                                                                                  | No threshold. The system scales by social pressure, not by rule.                                                                                                                                                                 |

### 6.4 What This Would Have Changed

The October 2021 networking poll achieved consensus (SF:24/WF:16/N:3/WA:6/SA:3). Published voter comments included "can't judge its suitability for networking" from voters who voted Weakly Favor. Under domain coverage, the chair's report would have shown the networking-practitioner distribution before the vote. The committee would have known what it was deciding with and without.

---

## 7. Tooling

The artifacts, the registry, and the chair's brief are labor. The committee should explore tooling to reduce the labor. This paper does not propose specific tools. It proposes that the committee explore automated assistance to make proportional deliberation practical. The artifacts described in Sections 5 and 6 are the requirements. The tooling is the implementation.

| Task                         | What tooling could do                                                                                                                           | Why                                                                                                                               |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Decision sizing              | Given a paper number, look up the dependency chain depth, years of prior work, and known deployments from the published record. Propose a tier. | The observable criteria are countable. Counting is what tools do well. The chair reviews and overrides; the tool does the lookup. |
| Stakeholder registry         | Structured form attached to each paper. Collects self-registrations. Produces the chair's pre-meeting report automatically.                     | Replaces an unstructured reflector thread with a queryable record.                                                                |
| Chair's brief generation     | Generated from the registry and the artifact checklist. One page. Shows tier, coverage, artifact gaps.                                          | The chair should not have to assemble this by hand. The tool reads the registry and the mailing, produces the brief.              |
| Decision rationale capture   | After the poll, a structured template for the chair or recorder: reasoning, alternatives considered, dissenting views.                          | A template is faster than a blank page. The structure ensures nothing is omitted.                                                 |
| Domain coverage report       | From the registry: for each affected domain, how many registered stakeholders voted, and how. Attached to the poll record.                      | The report is a query over the registry. The tool runs the query.                                                                 |

Automated assistance can reduce the labor of producing these artifacts to minutes rather than hours. The committee's institutional knowledge is already in the published record. Structured templates with automated lookup make it accessible.

---

## 8. Relieving the Chair's Burden

The artifacts in Sections 5 and 6 are aspirational without enforcement. This section answers: who makes people follow this? The answer: the chair, using powers the chair already has.

The chair currently makes subjective judgments about whether a session is ready, with no framework. Under proportional deliberation, the chair has a checklist. The checklist does the judgment. The chair applies it. That is less work, not more.

| Power                                | How it applies                                                                                                                                                                              | Why it reduces burden                                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Scheduling priority                  | Tier 4 decision with missing artifacts: scheduled last, or deferred until artifacts arrive. Tier 4 with complete artifacts: priority.                                                       | The chair no longer decides subjectively whether a paper is "ready." The artifact checklist decides. The chair applies it.           |
| Pre-meeting requirements             | Chair tells the author: "This is Tier 3. Before I schedule this, I need a stakeholder brief and an evidence summary. Reflector discussion should be complete two weeks before the meeting." | The author does the work. The chair checks the box. The chair is not doing the analysis - the chair is requiring that it exist.      |
| Compelling stakeholder participation | Chair contacts identified stakeholders: "Your domain is affected. Have you registered? Have you submitted a written position?"                                                              | Not new power. Chairs already invite people to sessions. This structures the invitation.                                             |
| Deferring without blocking           | Artifacts incomplete: defer the poll to the next meeting. Paper stays on the agenda. Author has time.                                                                                       | Not blocking - "come back when you're ready." The chair is not saying no. The chair is saying not yet.                               |
| The brief as shield                  | When someone objects to a deferral, the chair points to the brief: "Tier 4. Artifact checklist requires X, Y, Z. X and Z are missing."                                                    | The brief makes the deferral defensible. The chair is not exercising personal judgment. The chair is applying a published framework. |

This is the same principle as code review. A reviewer does not decide subjectively whether code is ready to merge. The CI pipeline decides. The reviewer applies judgment on top of a passing build. The chair applies judgment on top of a complete artifact set.

---

## 9. The Checklist

The fourteen failure modes from Section 3, plus the two governance modes from Section 6 and the artifact mode from Section 5, reduce to seventeen yes-or-no questions. A chair or paper author can run through the table in minutes. Each row names the failure mode, states the test question, and says when to ask it.

| #  | Failure Mode                                                    | Test Question                                                                                     | When to Ask                        |
| -- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------- |
| A1 | Architecture chosen without working demonstration               | Does a working demonstration exist for the proposed architecture?                                 | Before choosing an architecture    |
| A2 | Assertions without deployed evidence                            | Does at least one piece of evidence come from a deployed codebase?                                | Before acting on an assertion      |
| A3 | Poll where evidence covers some domains but not others          | Does the evidence support each domain in the poll independently?                                  | Before polling on bundled claims   |
| A4 | Predictions without follow-up                                   | Has the committee revisited the diagnosis after N years?                                          | At defined intervals after a pivot |
| B1 | Design rationale lost across paper boundaries                   | Does the new paper restate the prior paper's design rationale?                                    | At every paper handoff             |
| B2 | Terminology drift erasing a conceptual model                    | Does each simplification step document what conceptual model is preserved and what is removed?    | At every API rename                |
| C1 | Coupling that blocks independent delivery                       | Can the blocked feature ship independently with a narrower dependency?                            | Before coupling features           |
| C2 | Iteration without deployment                                    | After N revisions without deployment, has the committee asked whether the problem is ill-posed?   | At defined revision thresholds     |
| D1 | Direction set by analysis examining only one interpretation     | Has the analysis been performed under every interpretation that applies to the affected domains?  | Before acting on a pivotal paper   |
| D2 | Direction change evaluated for domains it helps, not domains it affects | Has the cost to each affected domain been evaluated?                                      | Before acting on a direction change |
| D3 | Affected stakeholders absent from the driving analysis          | Does the driving analysis contain examples from every affected domain?                            | Before acting on a pivotal paper   |
| D4 | Design limitations attributed to the problem domain             | Does the paper distinguish between properties of the current design and properties of the domain? | When evaluating a diagnosis        |
| E1 | Proceeding without consensus on the foundational premise        | Is the dissent documented and the premise revisited at defined intervals?                         | After every "no consensus" poll    |
| E2 | Evidence bar applied non-uniformly across claims                | Is the same evidence bar applied to each claim that drives the direction?                         | When bundled claims drive a direction |
| F1 | Missing artifacts disproportionate to the decision              | Are the artifacts proportional to the decision's tier?                                            | Before every poll (via the brief)  |
| G1 | Decision without domain coverage                                | Does the poll record include the domain coverage distribution?                                    | At every consequential poll        |
| G2 | Absent stakeholder on a consequential decision                  | Are identified stakeholders present or heard in writing?                                          | Before every Tier 3+ poll          |

---

## 10. Applying the Checklist: One Example

[P4048R0](https://wg21.link/p4048r0)<sup>[20]</sup>, "Networking for C++29: A Call to Action," proposes a production pipeline for networking. It is one example of how a large effort could be structured to address the failure modes above. Other efforts could use different safeguards for the same failure modes.

| #  | Failure Mode                                                    | Safeguard in P4048R0                                                                                                                |
| -- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| A1 | Architecture chosen without working demonstration               | No unification proposed. Two models, each for its domain. Working code ships before standardization.                                |
| A2 | Assertions without deployed evidence                            | Capy and Corosio are deployed with three independent adopters. Every claim is backed by running code.                               |
| A3 | Poll where evidence covers some domains but not others          | The endeavor targets one domain (networking). No bundled claims.                                                                    |
| A4 | Predictions without follow-up                                   | The pipeline produces visible artifacts at every stage. Progress is measurable.                                                     |
| B1 | Design rationale lost across paper boundaries                   | WG21 SAGE captures the reasoning behind every decision. Rationale is a first-class deliverable.                                     |
| B2 | Terminology drift erasing a conceptual model                    | The Vision Integrity Team reviews every artifact for architectural coherence.                                                        |
| C1 | Coupling that blocks independent delivery                       | The endeavor does not depend on `std::execution` changes. Bridges are additive.                                                     |
| C2 | Iteration without deployment                                    | The libraries are deployed before standardization begins. The pipeline starts from working code.                                    |
| D1 | Direction set by analysis examining only one interpretation     | The `std::execution` Compatibility Team reviews every artifact. Both framings are represented.                                       |
| D2 | Direction change evaluated for domains it helps, not domains it affects | The Design Team includes domain experts from networking, senders, allocators, and error handling.                             |
| D3 | Affected stakeholders absent from the driving analysis          | The endeavor is the affected domain's analysis. Every paper contains networking examples.                                           |
| D4 | Design limitations attributed to the problem domain             | [P4088R0](https://wg21.link/p4088r0)<sup>[21]</sup> distinguishes the design fork (API choice) from domain requirements.           |
| E1 | Proceeding without consensus on the foundational premise        | The endeavor asks for exploration, not commitment. "Let's explore both" is the lowest-cost consensus position.                      |
| E2 | Evidence bar applied non-uniformly across claims                | Every paper applies the same evidence bar: working code, constructed comparisons, published deployments.                            |
| F1 | Missing artifacts disproportionate to the decision              | SAGE captures rationale. The pipeline produces continuous artifacts. Cross-cutting review teams provide counteranalysis.             |
| G1 | Decision without domain coverage                                | The Compatibility Team is the stakeholder registry made structural. The Design Team includes domain experts from every affected area. |
| G2 | Absent stakeholder on a consequential decision                  | The pipeline's team structure ensures affected stakeholders are participants, not observers.                                         |

---

## 11. Anticipated Objections

**Q: This is hindsight bias.**

A: Some failure modes could have been identified at the time (A1, A2, C1, E1). Others required capabilities that did not exist (D1 under the coroutine framing, which required C++20). The checklist distinguishes between the two by specifying when to ask each question.

**Q: The committee already knows how to run large efforts.**

A: Contracts, reflection, and `std::execution` each consumed years. Each grew with every revision. Each generated controversy. The checklist is offered as a tool, not a criticism.

**Q: These failure modes are specific to the executor arc.**

A: Section 4 generalizes each failure mode. The categories - evidence, knowledge transfer, scope management, analytical framing, governance, proportional deliberation, domain coverage - apply to any multi-year, multi-author standardization effort.

**Q: Proportional deliberation adds bureaucracy.**

A: The artifacts already exist informally for trivial decisions - the paper itself is the stakeholder brief, the evidence summary, and the impact assessment. The proposal is to produce them formally for consequential decisions. The cost of not producing them is documented in Sections 3 and 5. Tier 1 decisions require only the paper. The bureaucracy scales with the consequence.

**Q: Self-registration is gameable.**

A: So is the current system - anyone can walk into a room and vote. Self-registration adds information to the record. It does not restrict voting. The committee still decides. The record is richer. Social accountability corrects false claims - the community knows who has built what.

**Q: Domain coverage implies some votes count more than others.**

A: It does not. Every vote counts equally in the poll. Domain coverage is metadata on the record, not a weighting function. The committee interprets the metadata. A future committee reviewing the decision can see whether the affected domains were represented.

**Q: This puts more work on the chair.**

A: It puts less. The chair currently makes subjective readiness judgments with no framework. Under proportional deliberation, the chair has a brief and a checklist. The framework does the judgment. The chair applies it. The author does the artifact work. The tooling does the lookup. The chair reviews a one-page brief instead of reading every paper cold.

**Q: You are arguing for your own library.**

A: Section 1 discloses this. The failure modes are extracted from the published record. The proportional-deliberation framework applies to any large effort. They stand or fall on the sources, not on who assembled them.

---

## Acknowledgments

The author thanks Christopher Kohlhoff for the executor model, [N3747](https://wg21.link/n3747)<sup>[19]</sup>, and the candid retrospective in [P1791R0](https://wg21.link/p1791r0)<sup>[22]</sup>; Eric Niebler, Kirk Shoop, Lewis Baker, and Lee Howes for [P1525R0](https://wg21.link/p1525r0)<sup>[16]</sup> and [P2300R10](https://wg21.link/p2300r10)<sup>[10]</sup>; Ville Voutilainen for [P2464R0](https://wg21.link/p2464r0)<sup>[12]</sup>; Jared Hoberock, Michael Garland, and Chris Mysen for [P0443](https://wg21.link/p0443)<sup>[9]</sup>; Bryce Adelstein Lelbach for the published poll outcomes; Dietmar K&uuml;hl for [P2762R2](https://wg21.link/p2762r2)<sup>[23]</sup>; Jonathan M&uuml;ller for [P3801R0](https://wg21.link/p3801r0)<sup>[24]</sup>; Howard Hinnant for the variant anecdote that motivated Section 6; and Steve Gerbino for feedback.

---

## References

1. [P4094R0](https://wg21.link/p4094r0) - "Retrospective: The Unification of Executors and P0443" (Vinnie Falco, 2026). https://wg21.link/p4094r0

2. [P4095R0](https://wg21.link/p4095r0) - "Retrospective: The Basis Operation and P1525" (Vinnie Falco, 2026). https://wg21.link/p4095r0

3. [P4096R0](https://wg21.link/p4096r0) - "Retrospective: Coroutine Executors and P2464R0" (Vinnie Falco, 2026). https://wg21.link/p4096r0

4. [P4097R0](https://wg21.link/p4097r0) - "Retrospective: The Networking Claim and P2453R0" (Vinnie Falco, 2026). https://wg21.link/p4097r0

5. [P4098R0](https://wg21.link/p4098r0) - "Retrospective: Async Claims and Evidence" (Vinnie Falco, 2026). https://wg21.link/p4098r0

6. [cppalliance/corosio](https://github.com/cppalliance/corosio) - Coroutine-native networking library. https://github.com/cppalliance/corosio

7. [cppalliance/capy](https://github.com/cppalliance/capy) - Coroutine I/O primitives library. https://github.com/cppalliance/capy

8. [P2469R0](https://wg21.link/p2469r0) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not" (Christopher Kohlhoff, Jamie Allsop, Vinnie Falco, Richard Hodges, Klemens Morgenstern, 2021). https://wg21.link/p2469r0

9. [P0443R0](https://wg21.link/p0443r0) - "A Unified Executors Proposal for C++" (Jared Hoberock, Michael Garland, Chris Kohlhoff, Chris Mysen, Carter Edwards, 2016). https://wg21.link/p0443r0

10. [P2300R10](https://wg21.link/p2300r10) - "std::execution" (Micha&lstrok; Dominiak et al., 2024). https://wg21.link/p2300r10

11. [P2430R0](https://wg21.link/p2430r0) - "Partial success scenarios with P2300" (Christopher Kohlhoff, 2021). https://wg21.link/p2430r0

12. [P2464R0](https://wg21.link/p2464r0) - "Ruminations on networking and executors" (Ville Voutilainen, 2021). https://wg21.link/p2464r0

13. [P0113R0](https://wg21.link/p0113r0) - "Executors and Asynchronous Operations, Revision 2" (Christopher Kohlhoff, 2015). https://wg21.link/p0113r0

14. [P1256R0](https://wg21.link/p1256r0) - "Executors Should Go To A TS" (Detlef Vollmann, 2018). https://wg21.link/p1256r0

15. [N1925](https://wg21.link/n1925) - "A Proposal to Add Networking Utilities to the C++ Standard Library" (Chris Kohlhoff, 2005). https://wg21.link/n1925

16. [P1525R0](https://wg21.link/p1525r0) - "One-Way execute is a Poor Basis Operation" (Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, 2019). https://wg21.link/p1525r0

17. [P1658R0](https://wg21.link/p1658r0) - "Suggestions for Consensus on Executors" (Jared Hoberock, Bryce Adelstein Lelbach, 2019). https://wg21.link/p1658r0

18. [P1660R0](https://wg21.link/p1660r0) - "A Compromise Executor Design Sketch" (Jared Hoberock, Michael Garland, Bryce Adelstein Lelbach, Micha&lstrok; Dominiak, Eric Niebler, Kirk Shoop, Lewis Baker, Lee Howes, David S. Hollman, Gordon Brown, 2019). https://wg21.link/p1660r0

19. [N3747](https://wg21.link/n3747) - "A Universal Model for Asynchronous Operations" (Christopher Kohlhoff, 2013). https://wg21.link/n3747

20. [P4048R0](https://wg21.link/p4048r0) - "Networking for C++29: A Call to Action" (Vinnie Falco, 2026). https://wg21.link/p4048r0

21. [P4088R0](https://wg21.link/p4088r0) - "What C++20 Coroutines Already Buy The Standard" (Vinnie Falco, 2026). https://wg21.link/p4088r0

22. [P1791R0](https://wg21.link/p1791r0) - "Evolution of the P0443 Unified Executors Proposal to accommodate new requirements" (Christopher Kohlhoff, Jamie Allsop, 2019). https://wg21.link/p1791r0

23. [P2762R2](https://wg21.link/p2762r2) - "Sender/Receiver Interface For Networking" (Dietmar K&uuml;hl, 2023). https://wg21.link/p2762r2

24. [P3801R0](https://wg21.link/p3801r0) - "Concerns about the design of std::execution::task" (Jonathan M&uuml;ller, 2025). https://wg21.link/p3801r0

25. [P2453R0](https://wg21.link/p2453r0) - "2021 October Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022). https://wg21.link/p2453r0

26. [P4100R0](https://wg21.link/p4100r0) - "The Network Endeavor: Coroutine-Native I/O for C++29" (Vinnie Falco, Steve Gerbino, Michael Vandeberg, Mungo Gill, Mohammad Nejati, 2026). https://wg21.link/p4100r0

27. [N4985](https://wg21.link/n4985) - "WG21 2024-06 St Louis Minutes of Meeting" (Nina Ranns, 2024). https://wg21.link/n4985

28. [P3552R3](https://wg21.link/p3552r3) - "task - An Asynchronous Coroutine Task Type" (Lewis Baker, 2025). https://wg21.link/p3552r3
