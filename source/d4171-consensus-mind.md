---
title: "Info: Institutional-Theory Predictions About Standards Bodies"
document: P4171R0
date: 2026-03-30
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
audience: WG21
---

## Abstract

Six academic disciplines independently describe the same phenomenon: consensus bodies change how their members think.

Organizational sociology, social psychology, regulatory theory, political science, fisheries ecology, and diplomatic studies each name a force that acts on deliberative institutions. The forces are documented, the mechanisms are published, and the predictions are testable. This paper introduces the six forces, derives one prediction from each, and tests each prediction against WG21's published record. The paper takes no position on whether the observed effects are beneficial, harmful, or neutral. It provides a vocabulary.

---

## Revision History

### R0: April 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space: [P4003R0](https://wg21.link/p4003r0)<sup>[1]</sup>, [P4007R0](https://wg21.link/p4007r0)<sup>[2]</sup>, and [P4100R0](https://wg21.link/p4100r0)<sup>[3]</sup>. The author has attended WG21 meetings since 2018. The institutional-theory literature presented here applies to every consensus body, including bodies whose decisions the author agrees with.

The author asks for nothing.

---

## 2. Six Forces

The academic literature across six disciplines identifies forces that act on consensus-driven institutions. Each force is an observable phenomenon with a published research basis. This section introduces them without reference to WG21. The forces are presented as properties of institutions, not as criticisms of the people within them.

### 2.1 Goal Displacement

**Discipline:** Organizational sociology.

**Source:** Robert K. Merton, "Bureaucratic Structure and Personality," *Social Forces*, 18(4):560-568, 1940<sup>[4]</sup>. Republished in *Social Theory and Social Structure*, Free Press, 1957<sup>[5]</sup>.

Goal displacement occurs when the procedures designed to achieve an objective become more important than the objective itself. Merton observed that bureaucracies reward strict adherence to rules and formal procedures. Over time, participants optimize for procedural compliance because that is what the institution measures and rewards. The original goal - the reason the institution was created - recedes. The procedures remain.

Merton studied government agencies. He found that officials developed what he called "trained incapacity" - a condition where their training in procedural compliance made them less capable of responding to the substantive problems the procedures were designed to address. The officials were not incompetent. They were competent at the wrong thing.

The phenomenon is structural. It does not require bad intent. It requires only that the institution reward procedure more visibly than it rewards outcomes.

### 2.2 Professional Socialization

**Discipline:** Social psychology.

**Source:** Jean Lave and Etienne Wenger, *Situated Learning: Legitimate Peripheral Participation*, Cambridge University Press, 1991<sup>[6]</sup>.

Professional socialization is the process through which newcomers to a specialized community internalize the community's norms, vocabulary, and implicit hierarchy. Lave and Wenger studied five communities - midwives, tailors, quartermasters, butchers, and recovering alcoholics - and found a common trajectory. Newcomers begin at the periphery, participating in limited ways. Over time, they move toward full participation. Along the way, they adopt the community's assumptions about what constitutes competence, what constitutes a serious contribution, and what constitutes a naive question.

The process is not indoctrination. It is learning. The newcomer gains genuine expertise. The cost is that the expertise is defined by the community's existing norms. A newcomer who arrives with a different frame of reference - a different definition of what "good" looks like - gradually adopts the community's definition. The original frame does not survive full participation.

The literature does not characterize this as good or bad. It characterizes it as observable and predictable.

### 2.3 Representational Capture

**Discipline:** Regulatory theory.

**Source:** George Stigler, "The Theory of Economic Regulation," *The Bell Journal of Economics and Management Science*, 2(1):3-21, 1971<sup>[7]</sup>. Nobel Prize in Economics, 1982.

Stigler observed that regulatory bodies tend, over time, to reflect the priorities of the entities most actively represented in the regulatory process. The entities that attend hearings, file comments, build relationships with regulators, and participate most consistently shape the body's output. The broader constituency the body was created to serve participates less and shapes the output less.

Stigler's insight was not that regulators are corrupt. His insight was that participation costs create a structural asymmetry. Entities with concentrated interests - for whom the regulatory outcome affects a large share of their operations - invest heavily in participation. Entities with diffuse interests - for whom the regulatory outcome is one of many concerns - invest less. The body's output reflects the participants, not the constituency.

This is sometimes called regulatory capture. It operates through participation, not through corruption.

### 2.4 The Iron Law

**Discipline:** Political science.

**Sources:** Robert Michels, *Political Parties: A Sociological Study of the Oligarchical Tendencies of Modern Democracy*, 1911<sup>[8]</sup>. Jerry Pournelle, "The Iron Law of Bureaucracy," 2006<sup>[9]</sup>.

Michels studied European socialist parties - organizations explicitly committed to democratic governance - and found that they inevitably developed oligarchies. Large organizations require delegation. Delegation creates administrators. Administrators develop specialized knowledge about the organization's procedures. That procedural knowledge becomes a form of power that rank-and-file members cannot easily replicate or challenge. Michels summarized: "Who says organization, says oligarchy."

Pournelle restated the principle for modern bureaucracies: "In any bureaucracy, the people devoted to the benefit of the bureaucracy itself always get in control, and those dedicated to the goals the bureaucracy is supposed to accomplish have less and less influence, and sometimes are eliminated entirely." Pournelle identified the selection mechanism: people skilled at navigating the organization's internal procedures are better at accumulating influence within the organization than people skilled at the organization's stated mission. The institution selects for procedural competence.

Neither Michels nor Pournelle characterized the phenomenon as intentional. Both characterized it as structural.

### 2.5 Shifting Baseline Syndrome

**Discipline:** Fisheries ecology.

**Source:** Daniel Pauly, "Anecdotes and the Shifting Baseline Syndrome of Fisheries," *Trends in Ecology and Evolution*, 10(10):430, 1995<sup>[10]</sup>.

Pauly observed that each generation of fisheries scientists accepts the stock size and species composition at the beginning of their career as the baseline for evaluating change. As fish stocks decline, the next generation of scientists uses the depleted stock as their baseline. The decline is invisible because the reference point moves with each cohort. Pauly called this the shifting baseline syndrome.

The mechanism is perceptual, not political. The scientists are not lying about the stock. They are accurately measuring change relative to the baseline they inherited. The problem is that the baseline itself represents a decline from the previous generation's baseline. Over multiple generations, significant cumulative decline goes unrecognized because no single generation observed it.

Pauly's original domain was fisheries. The concept has since been applied to environmental policy, urban planning, and institutional governance. The mechanism is the same in each domain: participants inherit a reference point and measure change from that reference point rather than from an absolute standard.

### 2.6 Going Native

**Discipline:** Diplomatic studies.

**Source:** Jeffrey T. Checkel, "'Going Native' In Europe? Theorizing Social Interaction in European Institutions," *Comparative Political Studies*, 36(1-2), 2003<sup>[11]</sup>.

Checkel studied members of the Council of Europe's Committee of Experts on Nationality and asked whether their preferences changed as a result of participating in the institution. He found that the quality of social interaction - not merely the duration of contact - determined whether participants adopted institutional perspectives. Deliberation and sustained engagement with peers produced genuine preference change. Casual contact did not.

In diplomatic theory, "going native" describes an ambassador who begins to advocate for the host country's interests rather than their home country's interests. The mechanism is proximity: the ambassador's daily social environment is the host country. Approval and disapproval signals come from the local context, not from the distant principal. Over time, the local context becomes the primary reference frame.

Checkel's contribution was to specify the mechanism. It is not mere exposure. It is the quality and depth of social engagement that produces the shift. Participants who deliberate - who engage in sustained, substantive discussion with institutional peers - are the ones whose preferences change.

---

## 3. Predictions

If the six forces described in Section 2 act on consensus-driven standards bodies, they should produce observable effects. This section derives one prediction from each force. Each prediction names the force it derives from, states the expected observation, and describes what evidence would confirm or disconfirm it.

The predictions are stated for consensus-driven standards bodies in general. Section 4 tests them against a specific body's published record.

### 3.1 From Goal Displacement

**Prediction 1.** A consensus body will advance features to completion based on the strength of their procedural record - number of revisions, study group approvals, straw poll history - rather than on evidence of end-user adoption. Features that achieve consensus through a complete procedural path will ship without published evidence that independent end users have deployed them.

**Confirmation:** Multiple features in the body's published record reached final adoption without published independent deployment experience. **Disconfirmation:** Every feature that reached final adoption had published independent deployment experience from organizations unaffiliated with the proposal's authors.

### 3.2 From Professional Socialization

**Prediction 2.** Long-tenured participants will evaluate proposals primarily through procedural criteria - process compliance, design review history, subgroup progression - while newcomers and external participants will evaluate proposals primarily through outcome criteria - user adoption, deployment evidence, measured performance. The vocabularies of long-tenured and short-tenured participants will diverge.

**Confirmation:** Published statements from long-tenured participants emphasize procedural criteria; published statements from newcomers or external participants emphasize outcome criteria. **Disconfirmation:** No vocabulary divergence is observable between long-tenured and short-tenured participants.

### 3.3 From Representational Capture

**Prediction 3.** The composition of the body's active participants will overrepresent entities with concentrated institutional interests - compiler vendors, platform owners, organizations that employ professional committee participants - relative to the broader user population the body serves. End users who write production code but do not participate in the standards process will be underrepresented.

**Confirmation:** Published attendance records show that compiler vendors and platform owners constitute a larger share of active participants than their share of the user population. **Disconfirmation:** The body's active participants are proportionally representative of the broader user population.

### 3.4 From the Iron Law

**Prediction 4.** Proposals with strong procedural navigation - experienced authors, coalition support, chair relationships, many revisions - will advance faster than proposals with strong deployment evidence but weak procedural navigation. Procedural skill will predict advancement speed more reliably than deployment evidence.

**Confirmation:** Proposals backed by well-resourced organizations with experienced committee participants advance faster than proposals from less-resourced authors, independent of deployment maturity. **Disconfirmation:** Advancement speed correlates with deployment evidence rather than with the resources and procedural experience of the proposing organization.

### 3.5 From Shifting Baseline Syndrome

**Prediction 5.** Long-tenured participants will describe the body's current pace and process as normal, while participants outside the institution will describe the same pace as slow. Each cohort of participants will calibrate its expectations to the conditions it inherited rather than to an external standard.

**Confirmation:** Published statements from long-tenured participants characterize multi-year timelines as careful or appropriate; published statements from external participants characterize the same timelines as excessive. **Disconfirmation:** Long-tenured and external participants describe the body's pace in similar terms.

### 3.6 From Going Native

**Prediction 6.** Participants whose professional reputation and career advancement depend on the body's internal approval will adopt the body's institutional priorities as their own. The body's priorities will become the participant's priorities, independent of whether those priorities align with the broader user community's priorities.

**Confirmation:** Participants who were initially critical of institutional norms adopt those norms after sustained engagement. The body's internal priorities - consensus, procedural completion, schedule adherence - are reflected in participants' public statements as personal priorities. **Disconfirmation:** Participants maintain their original priorities unchanged after years of sustained institutional engagement.

---

## 4. Observations

This section tests each prediction from Section 3 against WG21's published record. The data sources are WG21 papers, committee meeting minutes, and public statements by committee participants. Every quotation is attributed with date and source.

The observations report what the record contains. Where the record confirms a prediction, the confirmation is stated. Where the record is silent or ambiguous, that is stated. Where the record contradicts a prediction, the contradiction is stated.

### 4.1 Observation 1: Procedural Completion Without Deployment Evidence

Prediction 1 stated that features would advance based on procedural record rather than end-user adoption evidence.

[P2274R0](https://wg21.link/p2274r0)<sup>[12]</sup> (Aaron Ballman, 2020), a document describing WG21's procedures to WG14 members, states: "WG21 finds implementation experience with a proposal to be incredibly valuable but does not have any requirement on implementation experience to adopt a proposal."

C++20 Contracts ([P0542R5](https://wg21.link/p0542r5)<sup>[13]</sup>) were adopted at Cologne in 2019 and removed at Prague in 2020. No production deployment was reported before adoption.

C++26 Contracts ([P2900R14](https://wg21.link/p2900r14)<sup>[14]</sup>) were adopted into the working draft at Hagenberg in February 2025. [P4020R0](https://wg21.link/p4020r0)<sup>[15]</sup> (Andrzej Krzemie&nacute;ski - a P2900 co-author) states that the committee's experience is limited to assertion statements in function bodies, not the novel declaration annotations that are the feature's primary contribution. Two controlled experiments by Contracts proponents - replacing existing assertion macros in LLVM and libc++ - constitute the reported deployment evidence.

The Graph Library ([P3126R0](https://wg21.link/p3126r0)<sup>[16]</sup>) was proposed for standardization in 2024. Section 10 states: "There is no current use of the library." Section 11 states: "There is no current deployment experience."

Howard Hinnant wrote on the library reflector in July 2016<sup>[17]</sup>: "I should quit asking: 'Has it been implemented?' The correct question is: What has been the field experience? Is there positive feedback from anyone outside your immediate family or people who could have a perceived conflict of interest (such as employees of your company)?"

The record confirms Prediction 1. The body's procedures permit advancement without deployment evidence, and multiple features have advanced through the full procedural path without published independent deployment experience.

### 4.2 Observation 2: Vocabulary Divergence

Prediction 2 stated that long-tenured and short-tenured participants would use different vocabularies when evaluating proposals.

[P3962R0](https://wg21.link/p3962r0)<sup>[18]</sup> (Nina Ranns and 17 implementer co-authors, 2026) reports: "Implementation feedback is often introduced late, treated as adversarial, or framed primarily as an obstacle to progress rather than as essential design input." The implementers - participants whose daily work is shipping code to users - describe a reception pattern in which outcome-oriented feedback is reframed as procedural obstruction.

The same paper states: "Full conformance to recent standards remains difficult in practice, with some implementations still working toward C++20 conformance with limited capacity to adopt newer standards." This is an outcome measurement - a statement about what users can and cannot access. The response to implementer concerns, as the implementers describe it, is procedural: the concern is "framed primarily as an obstacle to progress."

[P2138R4](https://wg21.link/p2138r4)<sup>[19]</sup> (Ville Voutilainen, 2021) proposed a "Tentatively Plenary" state requiring implementation and deployment experience review before plenary votes. The LEWG poll to adopt the proposal failed to reach consensus<sup>[20]</sup>:

| SF | WF | N  | WA | SA |
| -: | -: | -: | -: | -: |
|  5 | 14 |  2 |  6 |  6 |

Nineteen delegates favored adoption. Twelve opposed. The objections centered on gatekeeping, discouraging participation, and slowing the process - procedural concerns. The proposal itself was an outcome-oriented measure: require evidence that the feature works before making it permanent.

The record is consistent with Prediction 2. Outcome-oriented vocabulary (deployment, implementation, field experience) and process-oriented vocabulary (progress, consensus, schedule) are observably present in different participant populations.

### 4.3 Observation 3: Participation Composition

Prediction 3 stated that entities with concentrated institutional interests would be overrepresented relative to the broader user population.

WG21 does not publish delegate affiliation data in its public minutes. [N5007](https://wg21.link/n5007)<sup>[21]</sup> (Hagenberg 2025 minutes) records attendance by national body but not by employer or organizational affiliation. A quantitative test of Prediction 3 against published data is not possible with the available record.

Qualitative evidence is available. The five largest C++ compiler toolchains are maintained by five organizations: GCC (Red Hat and community), Clang/LLVM (Apple, Google, and community), MSVC (Microsoft), Intel C++ (Intel), and EDG (Edison Design Group). Representatives of these organizations are consistently present in WG21 proceedings. The broader C++ user population - estimated at approximately five million developers<sup>[22]</sup> - participates primarily through the standard library and language features the committee produces, not through committee attendance.

[P3962R0](https://wg21.link/p3962r0)<sup>[18]</sup> documents the structural position of implementers: "Adding new features to an implementation can displace other work, including bug fixes and performance tuning." The implementers who signed the paper represent a small fraction of the organizations that ship C++ code. The users who consume the standard's output are not signatories.

The record is consistent with Prediction 3 in qualitative terms. Quantitative confirmation would require affiliation data that WG21 does not publish.

### 4.4 Observation 4: Procedural Skill and Advancement Speed

Prediction 4 stated that procedural skill would predict advancement speed more reliably than deployment evidence.

Stackless coroutines were proposed by Gor Nishanov at Microsoft. Microsoft provided experimental Visual Studio support in 2013, before formal committee approval. The proposal progressed from initial paper to C++20 standardization in approximately six years<sup>[23]</sup>.

Stackful coroutines were proposed by Oliver Kowalke and Nat Goodspeed, community developers. P0876 reached 19 revisions over twelve years and remains in a "needs-revision" state. Stackful coroutines are not in the C++26 working draft<sup>[23]</sup>. Stackful coroutines have multiple production implementations and decades of deployment experience across languages and platforms.

The Networking TS was based on Boost.Asio - the most deployed asynchronous library in C++, with decades of field experience<sup>[24]</sup>. `std::execution` ([P2300R10](https://wg21.link/p2300r10)<sup>[25]</sup>) was authored primarily by delegates from NVIDIA, Meta, and other organizations with significant committee presence. At Kona in November 2023, SG4 polled that networking should use a sender/receiver model. The Networking TS, despite its deployment record, was set aside.

Both cases show the same pattern: the proposal with stronger institutional backing advanced faster than the proposal with stronger deployment evidence. The record is consistent with Prediction 4.

### 4.5 Observation 5: Pace Perception

Prediction 5 stated that long-tenured participants would describe the body's pace as normal while external participants would describe it as slow.

[P3962R0](https://wg21.link/p3962r0)<sup>[18]</sup> (18 implementer co-authors) states: "We would like the committee to consider ways of slowing down the addition of features into the standard to allow implementers to catch up." The implementers describe the pace as too fast for features and too slow for implementation quality. Their baseline is the rate at which compilers can absorb new features.

The train model ([P1000R2](https://wg21.link/p1000r2)<sup>[26]</sup> through [P1000R7](https://wg21.link/p1000r7)<sup>[27]</sup>) establishes a three-year cadence. The model has been in effect since C++11. Participants who entered the committee after the train model was adopted have never experienced a different cadence. For them, a three-year cycle and a multi-meeting progression from study group to plenary is the baseline.

The networking and executor arc spans twenty-one years, from the first networking proposals in 2005 through the present day. [P4094R0](https://wg21.link/p4094r0)<sup>[28]</sup> through [P4098R0](https://wg21.link/p4098r0)<sup>[29]</sup> document this timeline. Within the committee, the timeline is described as a consequence of the problem's difficulty. Outside the committee, the timeline is described differently. Boost.Asio has been serving users since 2003.

The record is consistent with Prediction 5. Long-tenured participants and external participants describe the same timelines using different reference frames.

### 4.6 Observation 6: Priority Adoption

Prediction 6 stated that participants whose careers depend on institutional approval would adopt the body's priorities as their own.

Profiles were endorsed by the Direction Group unanimously in [P2759R1](https://wg21.link/p2759r1)<sup>[30]</sup> (2023). The resulting vote at Issaquah was 47-2<sup>[31]</sup>. SG23 at Wroclaw gave 18-1 consensus to the initialization profile and forwarded [P3081R0](https://wg21.link/p3081r0)<sup>[32]</sup> to EWG for C++26. In January 2026, six senior committee members co-signed [P3970R0](https://wg21.link/p3970r0)<sup>[33]</sup>, a call to action urging the committee to build on the profiles framework. Profiles are not in C++26.

The record shows a sequence: the body endorsed a direction by supermajority, reaffirmed it by near-unanimity, reaffirmed it again by white paper, and did not execute it. The body's stated priority (profiles) and the body's revealed priority (the features that actually shipped) diverged. A participant who adopted the body's stated priorities as their own would have expected profiles to ship. A participant who adopted the body's revealed priorities would have expected the features that had stronger procedural momentum to ship instead.

Checkel's framework predicts that sustained institutional engagement produces genuine preference change. The profiles record does not directly test this prediction - it tests whether the body's own stated preferences predict its outputs. The divergence between stated and revealed preference is observable. Whether that divergence reflects goal displacement (Section 2.1), the iron law (Section 2.4), or some other force is a question the record does not resolve.

---

## 5. Summary of Observations

| Prediction | Force                        | Record              |
| ---------: | ---------------------------- | ------------------- |
|          1 | Goal Displacement            | Confirmed           |
|          2 | Professional Socialization   | Consistent          |
|          3 | Representational Capture     | Consistent (qual.)  |
|          4 | Iron Law                     | Consistent          |
|          5 | Shifting Baseline Syndrome   | Consistent          |
|          6 | Going Native                 | Partially testable  |

Four predictions are consistent with the published record. One is confirmed by the body's own documentation of its procedures. One is partially testable - the divergence between stated and revealed preference is observable, but the causal mechanism is not isolable from the available evidence.

No prediction was contradicted by the published record.

---

## 6. Conclusion

Six forces from six disciplines describe the same phenomenon from different angles. The forces are documented in published research spanning 1911 to 2003. The predictions they generate are testable. The tests against one standards body's published record produced no contradictions.

This paper places a vocabulary in the permanent record. The vocabulary is not new - the terms have been in the academic literature for decades. What is new is the application to a specific consensus body's published artifacts.

The next time the committee observes a pattern it cannot easily name - a proposal advancing without deployment evidence, a newcomer's concerns reframed as procedural obstruction, a supermajority endorsement that does not produce action - the vocabulary in Section 2 may be useful. Goal displacement, professional socialization, representational capture, the iron law, shifting baseline syndrome, going native. Each names a specific, documented mechanism. Each points to a specific body of published research. Each is falsifiable.

The vocabulary is in the record. It will wait there until someone needs it.

---

## Acknowledgements

Robert K. Merton, for identifying goal displacement. Jean Lave and Etienne Wenger, for the communities of practice framework. George Stigler, for the theory of economic regulation. Robert Michels, for the iron law of oligarchy. Jerry Pournelle, for the modern restatement. Daniel Pauly, for shifting baseline syndrome. Jeffrey Checkel, for specifying the going-native mechanism. Nina Ranns and the 17 co-authors of P3962R0, for documenting the implementer perspective. Ville Voutilainen, for P2138R4. Howard Hinnant, for the field experience principle. Aaron Ballman, for documenting WG21's procedures in P2274R0.

---

## References

1. [P4003R0](https://wg21.link/p4003r0) - "Coroutines for I/O" (Vinnie Falco, Mungo Gill, Steve Gerbino, 2026). https://wg21.link/p4003r0

2. [P4007R0](https://wg21.link/p4007r0) - "Senders and Coroutines" (Vinnie Falco, Mungo Gill, 2026). https://wg21.link/p4007r0

3. P4100R0 - "The Network Endeavor" (Vinnie Falco, Mungo Gill, 2026). Post-Croydon mailing.

4. Robert K. Merton. "Bureaucratic Structure and Personality." *Social Forces*, 18(4):560-568, 1940. https://www.csun.edu/~snk1966/Robert%20K%20Merton%20-%20Bureaucratic%20Structure%20and%20Personality.pdf

5. Robert K. Merton. *Social Theory and Social Structure*. Free Press, 1957.

6. Jean Lave and Etienne Wenger. *Situated Learning: Legitimate Peripheral Participation*. Cambridge University Press, 1991.

7. George Stigler. "The Theory of Economic Regulation." *The Bell Journal of Economics and Management Science*, 2(1):3-21, 1971. https://rasmusen.org/zg601/readings/Stigler.1971.pdf

8. Robert Michels. *Political Parties: A Sociological Study of the Oligarchical Tendencies of Modern Democracy*. 1911. English translation: Eden Paul and Cedar Paul, Hearst's International Library Co., 1915.

9. Jerry Pournelle. "The Iron Law of Bureaucracy." 2006. https://jerrypournelle.com/archives2/archives2view/view408.html

10. Daniel Pauly. "Anecdotes and the Shifting Baseline Syndrome of Fisheries." *Trends in Ecology and Evolution*, 10(10):430, 1995. https://doi.org/10.1016/S0169-5347(00)89171-5

11. Jeffrey T. Checkel. "'Going Native' In Europe? Theorizing Social Interaction in European Institutions." *Comparative Political Studies*, 36(1-2), 2003. https://journals.sagepub.com/doi/10.1177/0010414002239377

12. [P2274R0](https://wg21.link/p2274r0) - "C and C++ Compatibility Study Group" (Aaron Ballman, 2020). https://wg21.link/p2274r0

13. [P0542R5](https://wg21.link/p0542r5) - "Support for contract based programming in C++" (G. Dos Reis, J. D. Garcia, J. Lakos, A. Meredith, N. Myers, B. Stroustrup, 2018). https://wg21.link/p0542r5. Adopted at Cologne 2019, removed at Prague 2020.

14. [P2900R14](https://wg21.link/p2900r14) - "Contracts for C++" (Joshua Berne, Timur Doumler, Andrzej Krzemie&nacute;ski, 2025). https://wg21.link/p2900r14

15. [P4020R0](https://wg21.link/p4020r0) - "Concerns about contract assertions" (Andrzej Krzemie&nacute;ski, 2026). https://wg21.link/p4020r0

16. [P3126R0](https://wg21.link/p3126r0) - "Graph Library: Overview" (Phil Ratzloff, Andrew Lumsdaine, 2024). https://wg21.link/p3126r0

17. Howard Hinnant. Library reflector posts, July 2016. Quoted with permission in P4046R0<sup>[34]</sup>.

18. [P3962R0](https://wg21.link/p3962r0) - "Implementation reality of WG21 standardization" (Nina Ranns et al., 2026). https://wg21.link/p3962r0

19. [P2138R4](https://wg21.link/p2138r4) - "Rules of Design<=>Specification engagement" (Ville Voutilainen, 2021). https://wg21.link/p2138r4

20. [P2435R0](https://wg21.link/p2435r0) - "2021 Summer Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2021). https://wg21.link/p2435r0

21. [N5007](https://wg21.link/n5007) - "WG21 February 2025 Hagenberg Minutes of Meeting" (Nina Ranns, 2025). https://wg21.link/n5007

22. JetBrains. "The State of Developer Ecosystem 2024." https://www.jetbrains.com/lp/devecosystem-2024/

23. Vinnie Falco. "Stackful Coroutines in WG21: A Case Study in Institutional Dynamics." 2025. https://www.vinniefalco.com/p/stackful-coroutines-in-wg21-a-case

24. [P2469R0](https://wg21.link/p2469r0) - "Response to P2464: The Networking TS is baked, P2300 Sender/Receiver is not" (Christopher Kohlhoff, Jamie Allsop, Vinnie Falco, Richard Hodges, Klemens Morgenstern, 2021). https://wg21.link/p2469r0

25. [P2300R10](https://wg21.link/p2300r10) - "std::execution" (Micha&lstrok; Dominiak et al., 2024). https://wg21.link/p2300r10

26. [P1000R2](https://wg21.link/p1000r2) - "C++ IS Schedule" (Herb Sutter, 2018). https://wg21.link/p1000r2

27. [P1000R7](https://wg21.link/p1000r7) - "C++ IS Schedule (proposed)" (Herb Sutter, 2026). https://wg21.link/p1000r7

28. [P4094R0](https://wg21.link/p4094r0) - "Retrospective: Networking, Executors, and Senders/Receivers in WG21" (Vinnie Falco, 2026). https://wg21.link/p4094r0

29. [P4098R0](https://wg21.link/p4098r0) - "Retrospective: The Kona 2023 Sender-Only Decision" (Vinnie Falco, 2026). https://wg21.link/p4098r0

30. [P2759R1](https://wg21.link/p2759r1) - "DG Opinion on Safety for ISO C++" (Michael Wong, Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, 2023). https://wg21.link/p2759r1

31. [P3984R0](https://wg21.link/p3984r0) - "A type-safety profile" (Bjarne Stroustrup, 2026). https://wg21.link/p3984r0

32. [P3081R0](https://wg21.link/p3081r0) - "Core safety Profiles: Specification, adoptability, and impact" (2024). https://wg21.link/p3081r0

33. [P3970R0](https://wg21.link/p3970r0) - "Profiles and Safety: a call to action" (Daveed Vandevoorde, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, Michael Wong, 2026). https://wg21.link/p3970r0

34. P4046R0 - "SAGE: Saving All Gathered Expertise" (Vinnie Falco, 2026). Post-Croydon mailing.
