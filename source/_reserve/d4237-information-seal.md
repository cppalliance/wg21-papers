---
title: "The Information Seal: Game-Theory Analysis of SD-4's Quoting Restriction"
document: P4237R0
date: 2026-07-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

SD-4 offers a consent-based exception to its quoting restriction, but game theory predicts the exception is never exercised.

This paper models the incentive structure that SD-4's quoting restriction creates. Five games are analyzed using standard Nash equilibrium concepts: the consent request, the paraphrase challenge, the candor-accountability design space, the multi-participant coordination problem, and the information asymmetry between insiders and outsiders. Each game produces a stable equilibrium. Each equilibrium imposes costs on the Institution that the individual players do not bear, producing a social dilemma. Together they produce a system in which committee deliberation cannot be quoted, cannot be paraphrased reliably, and cannot be verified by anyone who was not present.

---

## Revision History

### R0

* Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

This paper examines a governance document (SD-4<sup>[1]</sup>), not a technical proposal. The author has no competing governance proposal and no stake in any particular disclosure regime. The analysis uses standard game-theoretical concepts (Nash equilibrium, dominant strategy, Pareto dominance, prisoner's dilemma, externality, social dilemma) applied to the incentive structure that SD-4's quoting restriction creates.

This paper asks for nothing.

---

## 2. The Rule

SD-4<sup>[1]</sup> defines the following materials as protected:

> Meeting records of subgroup discussion, meeting wikis, and non-public committee email lists (aka reflectors), which often include personal positions and discussion. It is not allowed to quote from these publicly (e.g., in papers and blog posts) except that the following are allowed: (a) quoting straw poll questions and numeric results; and (b) quoting words or positions attributed to a specific person with that person's prior consent.

WG21's committee email lists (reflectors) are subscription-restricted mailing lists accessible to committee participants. Subgroup discussion records and meeting wikis are similarly restricted. The restriction covers both in-meeting deliberation and between-meeting correspondence on reflectors.

Exception (a) permits citing poll questions and numeric results. Exception (b) permits quoting a specific person's words with that person's prior consent.

This paper analyzes exception (b).

---

## 3. What The Rule Protects

The restriction protects real interests. Before analyzing its structural properties, those interests deserve recognition.

First, the restriction enables candid position-taking. A delegate who believes a popular proposal has a fatal flaw can say so on the reflector without the statement appearing in a blog post the next morning. The distance between a reflector post and a public record creates space for honest technical disagreement.

Second, the restriction allows delegates to explore positions they might not defend publicly. A delegate can ask "what if we removed this feature entirely?" on the reflector as a thought experiment. Without the restriction, that question becomes a headline: "Delegate X wants to remove feature Y." The restriction protects the difference between exploring an idea and endorsing it.

Third, the restriction protects preliminary technical analysis from being quoted out of context. A delegate who posts an early analysis with errors can correct it in the next message. Without the restriction, the erroneous analysis can be quoted in a paper while the correction remains on the restricted reflector.

These are genuine benefits. The same mechanism also protects effects that are not benefits - strategic coordination of opposition among in-group members, dismissive characterization of inconvenient positions, ad hominem framing that would not survive public scrutiny, explicit coordination of plenary tactics. The restriction does not selectively protect substantive candor; it protects all private speech indiscriminately. The question is not whether candor deserves protection, but whether SD-4's specific mechanism - a blanket prohibition with a consent-based exception - distinguishes the private speech that serves the institution from the private speech that protects insider interests against it.

---

## 4. The Consent Request

Does exception (b) function as a usable mechanism?

A game-theoretical model requires three elements: players, strategies, and payoffs. A Nash equilibrium is a set of strategies where no player can improve their outcome by changing strategy alone - it is the stable state the game settles into.

The games in this paper are two-player. But the equilibria they produce have consequences beyond the players. The Institution - WG21 as a body - bears costs it did not choose to incur. Its legitimacy, its accountability to national bodies, and the quality of evidence available for its own decisions all depend on which equilibria the individual games reach. The Institution is not a player. It is the entity that absorbs the externality.

Two players: the Author (a paper writer who wants to cite reflector content) and the Participant (a committee member whose words the Author wants to quote).

The Author moves first: ask for consent, or do not ask. If the Author asks, the Participant chooses: grant or deny.

| | Participant grants | Participant denies |
|---|---|---|
| **Author's payoff** | Strong evidence for paper | No evidence, social capital spent |
| **Participant's payoff** | Words enter public record, constrain future positions | Protection preserved, no cost |

If the Author does not ask, the Author paraphrases (weaker evidence, no social capital spent) and the Participant is unaffected.

Granting consent has a concrete cost: The Participant's words become part of the public record, available to critics, to national bodies, to future papers that may use the words in arguments the Participant disagrees with. Denying consent has no cost. A strategy that is always at least as good as the alternative, regardless of what the other player does, is called a dominant strategy.

The Participant has a dominant strategy: deny.

The Author, knowing the Participant will deny, compares asking (which spends social capital for no evidence) to not asking (which preserves social capital and produces a paraphrase). Not asking dominates.

**Nash equilibrium: The Author does not ask, the Participant would deny.** The Author paraphrases. Exception (b) is never exercised.

**The permission exists in the text of SD-4. It does not exist in the practice of the committee.**

The consent mechanism is the Institution's stated accountability tool. Its equilibrium inertness makes it a dead letter. The structure is a prisoner's dilemma: Each individual is rational to deny, but all participants - including the deniers - would be better off if all granted, because their own positions would be defended by accurate quotation rather than corrupted paraphrase.

The mechanism also lacks enforcement. SD-4 states no procedure for requesting consent, maintains no registry of grants or denials, and describes no enforcement process. When a reflector post was leaked to the web in 2025, the author's only recourse was to publish it himself as a formal paper<sup>[10]</sup>. No enforcement action is documented. The enforcement asymmetry is telling: The committee spent enforcement resources making GitHub repositories private during the Kona 2025 meeting to prevent live leaks through pull requests applying decisions in real time. Confidentiality is actively enforced through technical controls. The consent exception is not enforced at all.

**The Institution protects the restriction but not the exception.**

---

## 5. The Paraphrase-Challenge

After the consent game reaches its equilibrium, the Author paraphrases. A second game begins.

The original text lives on a restricted reflector. The paper's audience falls into two groups: insiders who have read the reflector and can verify accuracy, and outsiders who have not and cannot. For most readers - including national body experts who did not attend, and the public - the paraphrase is the only version they will ever see.

Two players: the Author (who paraphrases) and the Participant (whose words were paraphrased).

| | Participant accepts | Participant challenges |
|---|---|---|
| **Author paraphrases accurately** | Paper stands | Author's credibility questioned despite accuracy |
| **Author paraphrases favorably** | Paper stands with stronger framing | Dispute that outsiders cannot adjudicate |

The Participant's decision to challenge depends on whether the paraphrase is favorable to them, not on whether it is accurate. An accurate paraphrase that makes the Participant look bad will be challenged. An inaccurate paraphrase that makes the Participant look good will be accepted. The correlation between accuracy and acceptance is negative in adversarial contexts.

The restriction does not merely prevent direct quotation. It removes the verification mechanism that keeps paraphrasing honest. In a world where the original text is accessible, an inaccurate paraphrase can be caught. In a world where the original text is restricted, neither the paraphrase nor the challenge to it can be verified by outsiders.

**The restriction corrupts the only alternative it permits.**

A paper claims a delegate said X. The delegate says the paper misrepresents their position. Both are speaking publicly. The original text is on a restricted reflector. The Institution has no way to adjudicate the dispute.

**The Institution's own records are inadmissible in its own proceedings.**

---

## 6. The Candor-Accountability Design Space

The standard justification for reflector restrictions is that they enable candid discussion. This is a real benefit (Section 3). The question is whether SD-4's specific design achieves the best available trade-off.

A design that is Pareto-dominated provides less of one good (or the same amount) and less of another good than an available alternative. A dominated design can be improved without making anyone worse off.

Six disclosure regimes, ordered by candor:

| Regime | Candor | Accountability | Verification | Speech protected |
|---|---|---|---|---|
| Full restriction (no quoting, no paraphrasing) | Highest | None | None | All |
| SD-4 as practiced (no quoting, paraphrasing allowed, consent exception structurally inert) | High | Nominal | None | All |
| Attributed paraphrase (paraphrasing with attribution, no direct quotes) | Medium | Medium | Partial | All (but attributed) |
| Selective transparency (substantive deliberation protected, strategic coordination exposed) | Medium | Medium-High | Partial | Substantive deliberation only |
| Quotation with functioning consent (the regime SD-4 claims to implement) | Medium | Medium | Full for quoted material | All for deniers; quoted material for granters |
| Full transparency (reflector is public record) | Lowest | Highest | Full | None |

The "Speech protected" column reveals what the other columns obscure. Most regimes protect all private speech or none. The selective transparency regime - protecting substantive deliberation while exposing strategic coordination - protects only the speech that serves the institution. The transparency literature distinguishes transparency of outcomes (desirable, auditable) from transparency of process (which can degrade deliberative quality)<sup>[11]</sup>. The selective transparency regime maps to this: transparent outcomes, protected process.

SD-4 as practiced provides less candor than a full restriction. Participants already know their positions may be described publicly through paraphrasing. The restriction does not prevent characterization of positions - it prevents verification of characterizations.

SD-4 as practiced provides less accountability than any transparency regime. The consent mechanism is structurally inert (Section 4). The paraphrase mechanism is structurally corrupted (Section 5).

The regime that SD-4 claims to implement (quotation with functioning consent) would provide the same candor protection for those who deny consent, plus a functioning accountability mechanism for those who grant it. But Section 4 shows this regime is unreachable. The consent mechanism's equilibrium collapses it back to the current regime.

The current regime is dominated not just by full transparency but by selectively-transparent regimes that protect substantive deliberation while exposing strategic coordination. The Pareto-improving direction is not "more transparency" in the abstract. It is a design that distinguishes the private speech that serves the institution from the private speech that protects insider interests against it - the distinction SD-4 does not make (Section 3).

**The current regime occupies neither extreme. It provides partial candor protection and near-zero accountability.**

---

## 7. The Multi-Participant Problem

Reflector exchanges involve multiple participants. The Author typically wants to characterize an exchange, not quote a single person. This creates a coordination game.

Suppose N participants in a reflector exchange. The Author asks all N for consent. Each Participant independently chooses to grant or deny. The Author can only quote the exchange coherently if all relevant Participants grant consent - a partial quotation that includes some voices but not others distorts the exchange.

This is a weakest-link coordination game. The probability of all N participants granting consent is p raised to the N, where p is the individual probability of granting.

| Participants | P(all grant) at p=0.7 | P(all grant) at p=0.5 | P(all grant) at p=0.3 |
|---|---|---|---|
| 2 | 0.49 | 0.25 | 0.09 |
| 3 | 0.34 | 0.13 | 0.03 |
| 5 | 0.17 | 0.03 | 0.002 |
| 8 | 0.06 | 0.004 | 0.0001 |

Even at p=0.7 - an unrealistically generous assumption given the dominant-strategy analysis in Section 4 - a six-person exchange has a twelve percent chance of unanimous consent. At a more realistic p=0.3, it is less than one tenth of one percent.

The discussions most worth citing for accountability - the ones with the most participants and the highest stakes - are the discussions the consent mechanism makes hardest to quote.

**The mechanism filters inversely by importance.**

This is a stag hunt. Each participant would benefit from a regime of mutual consent - accurate public records that defend everyone's positions - but only if all others cooperate. A single defection (one denial) collapses the outcome for everyone. A two-person exchange about a minor editorial fix has a reasonable chance of unanimous consent. A twelve-person exchange about a contested design decision - the kind that shapes a language for decades - has none.

**The mechanism makes accountability hardest precisely where it matters most.**

---

## 8. The Information Asymmetry

SD-4's quoting restriction is enforced against paper authors who want to cite reflector content. But the reflector content itself - the positions taken, the arguments made, the reasoning behind decisions - is available to every insider who reads the reflector.

| Capability | Insider | Outsider |
|---|---|---|
| Knows what was said | Yes | No |
| Can use knowledge in meetings and corridor conversations | Yes | No |
| Can cite knowledge in papers | Paraphrase only | Cannot paraphrase (no source access) |
| Can challenge a paraphrase with authority | Yes (has read the original) | No |
| Can verify claims about reflector content | Yes | No |

The restriction does not restrict the information. Anyone subscribed to the reflector can read it. The restriction controls the credible public use of the information. Insiders can use reflector knowledge in every operational context - meetings, hallway conversations, political calculations, their own papers through paraphrase. Outsiders cannot use it at all.

Committee decisions cannot be audited by anyone who was not in the room or on the reflector. National body experts who did not attend a meeting cannot verify what positions their delegation took. Papers analyzing committee process must rely on the weakest evidence standard (unverifiable paraphrase) for the most important evidence (what was actually said in deliberation).

**The restriction creates an information monopoly - not on the information itself, but on its credible public use.**

A national body whose delegation voted for a feature cannot verify, after the meeting, what arguments carried the room. A compiler vendor implementing a new feature cannot check whether the committee considered the implementation concern they raised on the reflector.

**The Institution's own constituents cannot hold it accountable for the quality of its reasoning.**

---

## 9. The Meta-Equilibrium

The five games produce a single stable state:

1. **Exception (b) is structurally inert.** The consent mechanism's equilibrium ensures it is never exercised. (Section 4)

2. **Paraphrasing is corrupted.** The alternative to quotation produces unreliable evidence because the verification mechanism is absent. (Section 5)

3. **The regime is Pareto-dominated.** The current position provides less candor than full restriction and less accountability than any transparency regime. (Section 6)

4. **Multi-participant consent is combinatorially impossible.** The mechanism filters inversely by importance. (Section 7)

5. **Information asymmetry favors insiders.** The restriction creates a monopoly on credible public use of reflector content. (Section 8)

The equilibrium is stable because no individual player can improve their payoff by changing strategy alone. No individual Participant benefits from granting consent. No individual Author benefits from violating SD-4 (enforcement costs exceed citation benefits). Each individual member benefits from the restriction. But the Institution's payoff is uniformly negative across all five games: It loses legitimacy, accountability, evidence quality, and verification while gaining only partial candor protection. This is a social dilemma - the canonical structure in which individually rational choices produce collectively irrational outcomes.

The trap is deepened by SD-4's procedural status. Standing documents are maintained by the Convenor and updated without plenary polls<sup>[12]</sup>. For over a decade, SD-4 bore Herb Sutter's name as Convenor and maintainer. The current attribution to Guy Davidson reflects the procedural transfer that accompanies a change in Convenor - standing documents pass to the new Convenor as part of the role. A new Convenor who inherits a portfolio of standing documents, an active committee calendar, and the accumulated expectations of a large working group has limited bandwidth to revisit each inherited document from first principles. The quoting restriction predates the current Convenor's tenure and was not collectively adopted by the committee through consensus. Reform would require collective action to change a document the members never collectively voted on - a document that individually benefits each of them. The Institution cannot change the mechanism because it is not a unitary actor. The members who would need to act are the same members who individually benefit from inaction.

---

## 10. Comparative Practice

WG21's quoting restriction is not inherited from ISO. It is an SD-4 invention. Other standards bodies - including sibling working groups within the same subcommittee (SC 22) - operate under different disclosure regimes.

The Chatham House Rule, established by the Royal Institute of International Affairs in 1927 and last revised in 2002, provides that participants may use information received at a meeting but may not reveal the identity or affiliation of any speaker<sup>[2]</sup>. It has been criticized as "designed to protect elite discussions from transparency and accountability"<sup>[3]</sup>. SD-4's restriction is stricter: It prohibits not only attribution but quotation of the content itself.

| Body | Domain | Meeting records | Quotation policy | Verification |
|---|---|---|---|---|
| WG14 (C) | SC 22 | Minutes published as N-documents<sup>[9]</sup> | On the record | Full |
| WG5 (Fortran) | SC 22 | Minutes published on official site<sup>[20]</sup> | On the record | Full |
| WG9 (Ada) | SC 22 | Minutes in public document log<sup>[21]</sup> | On the record | Full |
| SC 29/MPEG | JTC 1 | Public meeting reports<sup>[22]</sup> | No restriction found | Full |
| TC39 | JavaScript (Ecma) | Verbatim notes published on GitHub<sup>[8]</sup> | On the record | Full |
| W3C | Web standards | Minutes published publicly<sup>[7]</sup>; transcripts attendee-restricted<sup>[13]</sup> | On the record (off-the-record option) | Partial |
| WHATWG | HTML | Discussions in public GitHub issues<sup>[23]</sup> | On the record | Full |
| IETF | Internet standards | Meetings recorded and published<sup>[6]</sup>; mailing lists public | On the record | Full |
| Rust | Language governance | Council minutes on GitHub<sup>[24]</sup>; private carve-outs for moderation | Default transparent | Full |
| Python | Language governance | Steering Council updates on GitHub<sup>[25]</sup>; PEP discussions public | On the record | Full |
| WG21 (C++) | SC 22 | Plenary minutes only; subgroup records restricted | Prohibited except by consent | None for outsiders |

Ten of eleven bodies publish meeting records. Nine do so as a matter of course. WG21's three sibling working groups in SC 22 - the C, Fortran, and Ada committees - all publish their minutes without restriction.

IETF counts Cisco, Huawei, Google, Meta, Netflix, Oracle, Cloudflare, Akamai, Ericsson, Juniper, Nokia, and Comcast among its major corporate participants, all operating under full transparency with no attribution restrictions<sup>[14]</sup>. IETF's transparency is codified as a core process requirement<sup>[14]</sup>. The corporate-constituency argument does not distinguish WG21 from bodies that function under transparency.

ISO's own framework for meeting records is SF.10<sup>[4]</sup>, a consent-based system that balances transparency with participant comfort. Under SF.10, meetings may be recorded with participant consent, participants may opt out on a per-intervention basis, recordings are held by the secretary, and minutes are approved through a defined process. In March 2025, ISO published guidance explicitly permitting the use of AI tools for meeting transcription under SF.10<sup>[26]</sup>.

WG21's meeting guidelines operate outside this framework:

> Meetings are not public, we want everyone to be able to speak freely. Please refrain from live tweeting, blogging, taking photos or videos.<sup>[5]</sup>

| Body | Recording practice |
|---|---|
| IETF | Meetings recorded via Meetecho; recordings published on YouTube and Datatracker |
| W3C | Recording optional per working group with announced consent process |
| TC39 | Collaborative notes drafted during meetings, published to GitHub |
| Rust | Default no recording; design meetings may be recorded with unanimous agreement |
| Python | Internal meetings not recorded; PyCon panels recorded and published |
| WG21 | Recording prohibited |

WG21 does not adopt SF.10. It prohibits recording.

WG21's relationship to ISO confidentiality is selective. Strict ISO compliance would require making GitHub repositories private, forbidding conference talks about committee papers, and removing the wg21.link redirect service<sup>[15]</sup>. The committee ignores these rules but enforces the quoting restriction. The restriction is not an ISO inheritance; it is a choice.

---

## 11. Objections

### "The restriction protects candor."

Section 3 acknowledges this benefit. Section 6 shows the current regime provides less candor than a full restriction on both quoting and paraphrasing. Participants already know their positions may be described publicly through paraphrase. The restriction does not prevent characterization - it prevents verification of characterizations. The candor rationale supports a different design, not this one.

### "Game theory assumes rational self-interested actors. The committee operates on trust."

The analysis does not require cynicism. Trust-based actors may face a different payoff structure: A delegate who trusts their colleagues and prioritizes the institution may grant consent for reasons that do not appear in the individual-rationality matrix. But:

The dominant-strategy analysis applies whenever the cost asymmetry exceeds the trust premium. It typically does, because the future costs of granting consent are unbounded - the words enter the public record permanently, available to critics and future papers in arguments the granter cannot foresee. The trust premium is bounded by the relationship.

The multi-participant coordination problem (Section 7) is not solved by trust between any two participants. Trust between A and B does not produce trust between A and C. The N-way coordination remains a stag hunt regardless of bilateral trust levels.

Even if some participants grant consent out of trust, the overall equilibrium is still dominated by the asymmetric-cost regime. A mechanism that functions only when enough participants override their dominant strategy on trust is not a functioning mechanism. The trust defense survives partially - some individuals may grant - but it does not rescue the mechanism.

### "Iterated play sustains cooperation through reputation effects."

The committee is a repeated game. Participants interact over years. The standard game-theory response to "Nash predicts defection" is that iterated play can sustain cooperation through reputation: Participants who consistently deny consent build a reputation as opaque actors, which has costs in future interactions.

Reputation effects are too weak in this context. The population is small enough that denial is the unremarkable default, not a visible deviation that builds a reputation. The cost of granting consent is concrete and immediate (words in the public record); the reputation cost of denying is diffuse and delayed. The committee's culture of restraint discourages exactly the kind of public reputation-tracking that would make denial costly. A norm of not pressuring colleagues to grant consent is simultaneously a norm that makes denial costless.

### "The restriction has worked for decades."

The restriction's equilibrium is stable regardless of whether it works well. A Nash equilibrium is a state from which no individual can improve by unilateral change. Stability and optimality are different properties. A mechanism can be stable, widely accepted, and Pareto-dominated simultaneously.

### "Newcomers do not understand why the restriction exists."

The analysis does not depend on the author's tenure. The payoff matrices, the probability table, and the asymmetry structure are structural properties of the mechanism. They hold regardless of who describes them. A bridge does not become load-bearing because an experienced engineer inspects it. It is load-bearing, or it is not, before the inspector arrives.

### "The restriction lets delegates speak against their employers' interests."

This is the strongest folk rationale. A delegate employed by a compiler vendor might want to oppose a feature their employer is championing. The restriction, on this account, protects them from retaliation.

Two observations:

SD-4's stated rationale does not say this. The full justification in SD-4 is:

> ...which often include personal positions and discussion.

The meeting guidelines state:

> Meetings are not public, we want everyone to be able to speak freely.<sup>[5]</sup>

Neither document mentions employer pressure, corporate independence, or dissent protection. The folk rationale is an inference, not a stated policy.

The structural incentive runs the other way. Face-to-face meeting attendance is employer-funded. The delegates in the room are overwhelmingly there because their employer sent them. The structural incentive is for employers to send more delegates to amplify their position, not for employees to dissent against the employer who paid for their travel. The restriction protects speech that is already employer-aligned. The dissent it purports to enable is not structurally incentivized.

### "Transparency produces theatrical speech-making rather than honest exchange."

This objection has real empirical support. When the Federal Reserve began publishing verbatim FOMC transcripts, members shifted toward prepared remarks on popular topics and reduced spontaneous opinion-sharing<sup>[16]</sup>. When EU Council deliberations became transparent, delegates shifted to rigid position-taking for domestic audiences rather than genuine negotiation<sup>[17]</sup>. As formal EU Council sessions became more transparent, use of informal lunch breaks with no recorded minutes increased substantially for controversial issues<sup>[18]</sup>. A comparative study of Norwegian and Danish municipal meetings found that Norway's open meetings pushed substantive deliberation into informal, unrecorded channels<sup>[19]</sup>.

The evidence is real. But the FOMC study itself demonstrates the key point: Theatrical speech is auditable. Computational linguistics can detect the shift from candid to scripted in the textual record. Private coordination cannot be detected at all. The comparison is not candor versus theater. It is auditable dysfunction versus unauditable dysfunction. A body whose public proceedings become theatrical has a problem that can be diagnosed and corrected. A body whose private proceedings cannot be verified has a problem that cannot be diagnosed at all.

The migration studies (EU lunch breaks, Norwegian municipalities) show that transparency does not create private negotiation. It reveals existing private negotiation by contrast with the now-theatrical public record. The private negotiation was always there. Transparency made it visible.

### "Comparison bodies have other dysfunctions that may be byproducts of their transparency."

IETF has a reputation for protracted debates. TC39 has its own dynamics. A defender will argue that WG21's restriction prevents analogous dysfunctions.

Those dysfunctions are visible and correctable. IETF's protracted debates are observable in public mailing list archives. TC39's dynamics play out in published meeting notes. A dysfunction you can see is a dysfunction you can fix. WG21's dysfunctions - if they exist - cannot be observed, diagnosed, or corrected by anyone outside the reflector.

### "WG21's corporate constituency needs the restriction more than the comparison bodies."

Section 10 documents that IETF operates under full transparency with corporate participation at least as concentrated as WG21's. The corporate-constituency argument does not distinguish WG21 from bodies that function under transparency.

---

## 12. Conclusion

SD-4 says you may quote a committee member's words with that person's prior consent. In practice, no one consents. Denying is free. Granting puts your words in the public record, available to critics and future papers, with no offsetting benefit. The consent mechanism exists in the text. It does not exist in the committee.

The fallback is paraphrasing. But the original text lives on a restricted mailing list. A paraphrase cannot be checked. The person paraphrased can say "that is not what I meant" and no outsider can verify either claim. The restriction does not merely block quotation. It corrupts the only alternative.

Committee decisions are reached in discussions that cannot be quoted, cannot be paraphrased reliably, and cannot be verified by anyone who was not present. National body experts who did not attend cannot confirm what their delegation agreed to. The public cannot evaluate whether consensus was genuine.

The costs do not fall only on outsiders. Each equilibrium in this analysis imposes costs on the Institution that the individual players do not bear: a dead-letter accountability mechanism, corrupted evidence, inverse importance filtering, an information monopoly that insulates decisions from validation. Participants whose positions are defended by corrupted paraphrase rather than accurate quotation are worse off too. The bill arrives as diffuse institutional costs - eroded legitimacy, degraded evidence quality, diminished external credibility - rather than as concrete individual costs. The restriction is not a zero-sum transfer from outsiders to insiders. It is negative-sum. The Institution absorbs the externality of every game, and it is negative in every case.

What the rule protects is consequence-free speech for people who are present. What it costs is accountability to people who are not. What it costs the Institution is both.

---

## Acknowledgments

*To be completed.*

---

## References

[1] [SD-4](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures) - "WG21 Practices and Procedures" (Guy Davidson, 2026).

[2] [Chatham House Rule](https://www.chathamhouse.org/about-us/chatham-house-rule) - "Chatham House Rule" (Royal Institute of International Affairs, 2002).

[3] [Chatham House Rule - Powerbase](https://powerbase.info/index.php/Chatham_House_Rule) - "Chatham House Rule" (David Miller, Powerbase).

[4] [ISO SF.10](https://www.iso.org/publication/PUB100382.html) - "ISO Policy on Communication of Committee Work" (ISO, 2024).

[5] [N4916](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/n4916.html) - "WG21 Meeting Guidelines" (WG21, 2021).

[6] [RFC 8718](https://www.rfc-editor.org/rfc/rfc8718) - "IETF Plenary Meeting Venue Selection Process" (IETF, 2020).

[7] [W3C Process Document](https://www.w3.org/Consortium/Process/) - "W3C Process Document" (W3C, 2023).

[8] [TC39 Meeting Notes](https://github.com/tc39/notes) - "TC39 Meeting Notes" (Ecma TC39).

[9] [WG14 Meeting Minutes](https://www.open-std.org/jtc1/sc22/wg14/www/wg14_document_log.htm) - "WG14 Document Log" (WG14).

[10] [P3651R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3651r0.pdf) - "Profiles for C++26" (Bjarne Stroustrup, 2025).

[11] Quill, "Sunshine's Chill: Overboard American Open Meetings Laws and the Limits of Disclosure" (SSRN, 2015).

[12] [Standing Documents](https://isocpp.org/std/standing-documents) - "WG21 Standing Documents" (isocpp.org).

[13] [W3C Automated Transcripts Policy](https://www.w3.org/guide/meetings/transcripts.html) - "Automated Transcripts at W3C Meetings" (W3C).

[14] [RFC 9501](https://datatracker.ietf.org/doc/html/rfc9501) - "Open Participation Principle" (IETF, 2022).

[15] Rivera Morell, [std-proposals mailing list](https://lists.isocpp.org/std-proposals/2025/02/12422.php) (February 2025).

[16] Meade & Stasavage, "Transparency and Deliberation Within the FOMC: A Computational Linguistics Approach," *Quarterly Journal of Economics* 133(2), 2018, 801-870.

[17] Stasavage, "Striking a Pose: Transparency and Position Taking in the Council of the European Union," *European Journal of Political Research* 43(1), 2004.

[18] Cross & Hedgehammer, "Negotiating with Your Mouth Full: Intergovernmental Negotiations Between Transparency and Confidentiality," *Review of International Organizations*, 2024.

[19] Gimmingsrud et al., "Do Open Meetings Affect Deliberation?" *Journal of Deliberative Democracy*.

[20] [WG5 Documents](https://wg5-fortran.org/documents.html) (WG5 Fortran).

[21] [WG9 Electronic Documents Log](https://open-std.org/JTC1/SC22/WG9/documents.htm) (WG9 Ada).

[22] [MPEG Meeting Reports](https://www.mpeg.org/) (SC 29/MPEG).

[23] [WHATWG HTML](https://github.com/whatwg/html) (WHATWG).

[24] [Rust Leadership Council Minutes](https://github.com/rust-lang/leadership-council/tree/main/minutes) (Rust Leadership Council).

[25] [Python Steering Council](https://github.com/python/steering-council) (Python Steering Council).

[26] [AI Guidance](https://www.iso.org/files/live/sites/isoorg/files/developing_standards/who_develops_standards/docs/use%20of%20AI.pdf) - "Guidance on use of artificial intelligence (AI) for ISO committees" (ISO, 2025).
