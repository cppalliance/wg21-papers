---
title: "Fantastic Committee Members And Where To Find Them"
document: P4249R0
date: 2026-08-01
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The psychology literature predicts who stays in a consensus body, who leaves, and what happens to those who remain.

This paper tests those predictions against thirty years of WG21 papers. It identifies the personality profile the academic research associates with long-term consensus participation, derives falsifiable predictions from that profile, and checks each prediction against the committee's own published record - from a 1995 compromise paper through a 2025 pulse poll. The model is offered as a hypothesis. The evidence is offered as a test. The reader evaluates both.

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space. The author's first attended WG21 meeting was in 2018.

This paper is a companion to [P4241R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4241r0.html)<sup>[1]</sup>, which examines the dopaminergic reward structure of consensus body participation. That paper documents the neurochemistry. This paper documents the psychology - the personality traits, the selection dynamics, and the social effects that operate on a timescale of years, not meetings.

No personality inventory has been administered to WG21 members. Every prediction in this paper is triangulated from adjacent literatures - intentional communities, open-source governance, deliberative mini-publics, Quaker meetings, the IETF, and the published psychology of consensus decision-making. The WG21 paper archive provides the validation.

This paper uses AI. The literature search, the archive search, and the initial synthesis were produced with AI assistance. The evidence and the arrangement are the author's.

This paper asks for nothing.

---

## 2. What The System Produces

The consensus model works. The record says so.

C++14, C++17, C++20, and C++23 shipped on time. Four consecutive on-time releases. The three-year cadence established by [P1000R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p1000r6.html)<sup>[2]</sup> transformed C++ from a language that shipped once a decade to one that ships every three years. Voutilainen wrote in 2019, in [P0592R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0592r3.html)<sup>[3]</sup>:

> "C++ ships on time. C++11 shipped late, C++14 shipped on time, C++17 shipped on time, C++20 will ship on time, and C++23 will ship on time."

By C++17, major compilers were shipping conforming implementations within months of publication. Sutter wrote<sup>[4]</sup>:

> "After C++98 shipped, it took 5 years before we saw the first complete conforming compiler that implemented all language features; after C++11 shipped, it took 3 years; when C++14 shipped, it took months."

The consensus model also functions as a brake. The SA votes that blocked `std::execution` for C++23 gave the proposal two additional years of refinement. The contracts removal from C++20 - plenary vote 68/0/4 - demonstrated that the safety valve works when the evidence is clear. Josuttis, Voutilainen, Orr, Vandevoorde, Spicer, and Di Bella wrote in [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf)<sup>[5]</sup>:

> "Part of the train model must be an agreement that if there is not consensus that a feature is in acceptable form when the train is about to depart that the feature must be taken off the train and that it has to catch the next train."

Anyone can write a paper. Anyone can attend a meeting. Stroustrup stated at CppCon 2021<sup>[6]</sup>:

> "Having an ISO committee allows people from competing organizations to collaborate on important things for their organizations. We have been doing lots of things that couldn't have been done without the committee."

The system produces these results. The people who produce them do so because they care about the language. The question this paper investigates is not whether the system works. The question is what kind of person it selects, what it does to them, and whether the committee's own paper archive is consistent with what the psychology literature predicts.

---

## 3. The Profile

The psychology of consensus-based organizations has been studied in intentional communities, open-source governance bodies, Quaker meetings, citizen assemblies, and intergovernmental organizations. No study has directly profiled standards body members. The composite below is triangulated from adjacent literatures.

### 3.1 Agreeableness

The single most consistent finding across every domain studied is that consensus environments select for high agreeableness - cooperativeness, trust, altruism, compliance, and modesty. A 2023 study using both genetic algorithm modeling and real-world data found that agreeableness improves team performance specifically in tasks with uncertainty.<sup>[7]</sup> Apache open-source developers exhibiting higher agreeableness were more likely to become contributors.<sup>[8]</sup> The ICmatch intentional community resource describes agreeable types as "the reason that intentional community has any chance whatsoever of working out."<sup>[9]</sup>

The Direction Group characterized the committee's composition in [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[10]</sup>:

> "We are 'a bunch of volunteers.' Most are enthusiasts for some aspect of the language or other. Few have a global view. Most have a strong interest in only some subset of use, language, or library. Many are clever people attracted to clever solutions. Some are devoted to ideas of perfection."

Thirty years earlier, a 1995 compromise paper on class exceptions captured the agreeableness norm in a single sentence. Schwarz, Colvin, Clamage, and Myers wrote in [N0665R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/1995/N0665R1.ps)<sup>[11]</sup>:

> "None of us was completely satisfied with the result but we each felt that our concerns were well enough addressed that we could support this proposal."

The operating principles paper reinforced the behavioral expectation. Van Winkel, Garcia, Voutilainen, Orr, Wong, and Bonnal wrote in [P0559R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0559r0.pdf)<sup>[12]</sup>:

> "Listen more than talk."

At the 2024 St. Louis meeting, Ranns set the behavioral frame in [N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf)<sup>[13]</sup>:

> "Be aware of them and of your interaction with them. Understand that what one person considers friendly, another one might find intrusive. What one person finds short and to the point, another may find dismissive and offensive."

### 3.2 Emotional Stability

The literature predicts low neuroticism as the second most consistent trait. Neuroticism negatively predicts performance under social pressure and is positively associated with ambiguity aversion.<sup>[14]</sup><sup>[15]</sup> The Attraction-Selection-Attrition (ASA) model predicts that between-organization differentiation operates most strongly on neuroticism - low-neuroticism organizations shed high-neuroticism members most aggressively.<sup>[16]</sup>

The 2020 WG21 pulse poll documented in [P2260R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2260r0.pdf)<sup>[17]</sup> provides indirect evidence:

> "Over 60% participants responded that they often feel exhausted by meetings and demands from all sources, not just WG21 meetings."

Forty-six percent said the pace was unsustainable. A third reported disagreeable culture. The people who remain after that level of sustained pressure are, by definition, the ones whose emotional equilibrium survived it.

### 3.3 Openness

The literature predicts moderate-to-high openness to experience. Openness predicts democratic regime support, civic engagement, and organizational involvement.<sup>[18]</sup><sup>[19]</sup> It also negatively predicts ambiguity aversion.<sup>[15]</sup>

The Direction Group's self-description captures both the openness and its shadow. They wrote in [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[10]</sup>:

> "Many are clever people attracted to clever solutions. Some are devoted to ideas of perfection."

Stroustrup identified the cost of that openness in [P1962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf)<sup>[20]</sup>:

> "The committee process, 'design by committee' (or more accurately 'design by a federation of committees') in general tends to converge on designs that encompass the unions of all stated needs. For initial acceptance of a feature, that's bad. It's bloat."

### 3.4 Tolerance for Ambiguity

The literature identifies tolerance for ambiguity as perhaps the single most important non-Big-Five trait for consensus organization survival. Role ambiguity is the most damaging source of occupational stress across a 60-year meta-analysis of 515 studies.<sup>[21]</sup> Those who tolerate it persist. Those who do not, leave.

The WG21 process demands extraordinary ambiguity tolerance. Contracts were first proposed in 2014. They were removed from C++20 in 2019. As of 2026, they remain under active debate. Twelve years of ambiguity for a single feature. The Direction Group wrote across multiple revisions of [P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.html)<sup>[22]</sup>:

> "Many members are overwhelmed as their work (and life in general) is complicated. The WG21 mailing lists alone produce in total between 1,000 and 3,000 messages a month, which is a large volume of traffic to keep on top of."

### 3.5 The Stubborn Minority

A mathematical modeling study in *Scientific Reports* examined how heterogeneous groups converge to consensus. Gavrilets and colleagues found that "more stubborn and less agreeable" individuals bias group consensus toward their preferred value, and that a single individual who is "stubborn, persuasive, reputable, and central to the social network" can achieve consensus quickly - at the cost of the consensus being strongly biased toward their initial position.<sup>[23]</sup>

The model predicts an internal ecology: a cooperative majority providing the substrate, punctuated by a small number of lower-agreeableness members who provide boundary-setting. The committee's own leadership has described exactly this ecology.

The Direction Group wrote in [P2000R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2000r0.html)<sup>[24]</sup>:

> "A small vocal minority can stop any proposal at any stage of the process."

McDougall and co-authors characterized the dynamic more sharply in [P3297R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3297r0.pdf)<sup>[25]</sup>:

> "Conversations in meetings tend to be dominated by a minority of voices, sometimes those who have learned to raise the temperature in order to discourage participation."

Liber documented a specific instance in [P3581R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3581r0.html)<sup>[26]</sup>. During the Tokyo plenary, a single author objected to unanimous consent for `inplace_vector`. The paper was delayed by one meeting cycle. By St. Louis the objection was resolved and inplace_vector was approved with strong consensus - only one dissenting vote.

**The cooperative majority provides the substrate. The stubborn minority provides the brake. The literature predicts both. The archive documents both.**

### 3.6 Falsifiable Predictions: The Profile

**If this model is correct:** A personality inventory administered to WG21 regulars would show statistically significant elevation in agreeableness and emotional stability relative to the general software engineering population. The small number of participants known for persistent blocking would score lower in agreeableness but higher in conscientiousness and openness - the "stubborn minority" the model predicts. Quaker meeting attenders and IETF regulars would produce a similar profile.

**If this model is wrong:** WG21 regulars would be a personality-representative sample of senior C++ engineers. No trait clustering would emerge. Blocking behavior would be distributed randomly across personality types rather than concentrated in a low-agreeableness minority.

---

## 4. The Filter

The Attraction-Selection-Attrition (ASA) model explains why consensus organizations become personality-homogeneous over time. People with compatible traits are drawn to the organization (attraction). Formal and informal processes favor temperamental fit (selection). Misfits leave voluntarily (attrition). The result is progressive homogenization across iterations.<sup>[16]</sup>

The model predicts a multi-stage filter. Each stage removes a different population.

### 4.1 Stage One: Entry

The literature predicts that people who opt into consensus bodies are disproportionately high in extraversion and openness, have high internal locus of control, and possess time and institutional resources. A study of approximately 4,000 Swedes found these traits predict willingness to participate in deliberative mini-publics.<sup>[27]</sup> Austrian citizen assembly data confirmed participants had significantly higher locus of control than the general population.<sup>[28]</sup>

The IETF Community Survey 2024 found that regular participants spend a median of 9 hours per week on IETF work. The biggest participation hindrance is "time to read emails and documents."<sup>[29]</sup> The committee's own paper on remote participation acknowledged the structural filter. Adelstein Lelbach, Winters, Fracassi, and co-authors wrote in [P2145R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2145r1.html)<sup>[30]</sup>:

> "Historically, to participate in C++ standardization, individuals had to attend three week-long face-to-face meetings a year to remain engaged. While we have accomplished a great deal with this model, it does disenfranchise certain types of stakeholders and no longer reflects best practice in the industry."

McDougall and co-authors identified who the entry gate favors in [P3297R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3297r0.pdf)<sup>[25]</sup>:

> "These groups are volunteer based - and often the people busiest writing the code that puts rubber to the road are the ones least available to attend committee meetings. The end result is that conversations in meetings tend to be dominated by a minority of voices, sometimes those who have learned to raise the temperature in order to discourage participation. Some of the loudest voices come from finance or 'big tech' - and while those are important industries - they do not represent the best interests of automotive, aerospace, or robotics companies."

### 4.2 Stage Two: Early Attrition

The literature predicts that participants who leave after one or two meetings disproportionately cite confusion about process, frustration with pace, or desire for more direct impact. A trans activist collective documented this directly: Exit interviews revealed that volunteers left because "this whole thing is chaos, I've no idea what you actually want me to do and that makes it impossible to do anything."<sup>[31]</sup>

Voutilainen acknowledged the unwritten-rules problem in [P2138R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.pdf)<sup>[32]</sup>:

> "This proposal makes our pipeline stages officially-specified for everybody, both old and new committee members, and it gives new and old committee members a process specification that they can read, as opposed to relying on hearsay and never really knowing what to expect."

The 2023 admin telecon minutes recorded Sutter's proposed orientation program for newcomers, documented in [N4934](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4934.pdf)<sup>[33]</sup>:

> "Have a Sunday night 'welcome orientation' for all new attendees, that as many chairs as are available could attend. Topics: Wiki, Subgroup voting, Set expectations: want to speak freely, not give offense and also not take offense easily, assume good faith."

The existence of an orientation program is evidence that the problem is recognized. Its content - "not take offense easily, assume good faith" - is evidence that the process demands specific temperamental traits from the first day.

### 4.3 Stage Three: Mid-term Attrition

The literature predicts that mid-term departures (two to five years) disproportionately include people who carried significant invisible labor. Organizational research describes how "empathetic people see problems sooner than others," experience constant inner tension, and eventually "have to make a decision" to protect themselves. "Organizations lose the people who take on the most responsibility and are particularly essential for change."<sup>[34]</sup>

The committee has documented the exhaustion. The 2020 pulse poll in [P2260R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2260r0.pdf)<sup>[17]</sup> found:

> "Over 60% participants responded that they often feel exhausted by meetings and demands from all sources, not just WG21 meetings. 46% said that the current pace of virtual meetings is not sustainable."

The Direction Group documented attrition of key voices in [P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.html)<sup>[22]</sup>:

> "The attendance of virtual meetings is less consistent (several key voices are often missing) and we have heard many mentions of 'meeting fatigue.'"

At the 2025 Sofia meeting, Wong announced in [N5016](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5016.pdf)<sup>[35]</sup>:

> "In Hagenberg, I announced the retirement of long-time contributor Howard Hinnant from C++."

Beman Dawes. Sean Corfield. Steve Clamage. Howard Hinnant. Peter Brett. The committee keeps a formal record of retirements and emeritus appointments. The record exists because the departures are significant enough to record.

### 4.4 Stage Four: Long-term Convergence

The literature predicts that the ten-year cohort is measurably more homogeneous in personality, demographics, and process preference than the two-year cohort. An NBER working paper on FDA advisory committees found that "members with more advisory committee experience are more biased for the status quo."<sup>[36]</sup> Shaw and Hill's empirical study of 683 wikis confirmed Michels' prediction: "as voluntary movements and membership organizations become large and complex, a small group of early members consolidate and exercise a monopoly of power."<sup>[37]</sup>

The LEWG chair documented the institutional shift toward caution in [P2400R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r1.html)<sup>[38]</sup>:

> "Library Evolution has become more cautious in its use of Technical Specifications."

He elaborated on the mechanism:

> "The amount of field experience we want to see is very different to how it was 4 or 5 years ago, and I believe that's because we shipped a lot of library features and found a lot of late problems. We are in the process of improving and the bar is higher now."

The Direction Group operates as a "small by-invitation group of experienced participants." Their operating principle, repeated across every revision of [P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.html)<sup>[22]</sup>, is:

> "We only speak as 'The Direction Group' when we are in unanimous agreement on a topic."

The unanimity requirement means individual disagreements within the Direction Group are structurally invisible to the committee. The group presents a unified position or it presents nothing.

Stroustrup identified the cost of convergence in [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[10]</sup>:

> "We have no shared aims, no shared taste. This is a major problem, possibly the most dangerous problem we face as a committee."

**The entry gate selects for resources and temperament. Early attrition removes the action-oriented. Mid-term attrition removes the empathetic. What remains is the residue - and the residue converges.**

### 4.5 Falsifiable Predictions: The Filter

**If this model is correct:** The ten-year cohort is measurably more homogeneous than the two-year cohort. Status quo bias increases with tenure - senior members vote against novel proposals at higher rates than junior members on proposals of comparable technical merit. The committee's self-assessment of its own health is more optimistic than the assessment given by recent departures. WG21's demographic profile converges toward the IETF pattern: 5.4% women among regulars, predominantly older men from Europe and North America.

**If this model is wrong:** The long-term cohort is as diverse as the entry cohort. Tenure does not predict voting conservatism. Exit interviews match staying members' assessments.

---

## 5. What Changes

Long-term consensus participation produces measurable cognitive, behavioral, and - according to recent neuroscience - neural changes.

### 5.1 The Positive Changes

The literature documents real benefits. A ten-year follow-up study found that adults who received sustained deliberative dialogue training showed more complex thinking about citizenship, more communication about politics across differences, and greater "dialectical complexity" - the ability to both differentiate multiple approaches and integrate them into novel solutions.<sup>[39]</sup> Perspective-taking increases. Civic efficacy increases. Listening skills improve measurably.<sup>[40]</sup>

The committee contains people who have developed these capacities to a degree most professionals never achieve. The patience required to bring a feature from first paper to the International Standard - contracts has taken twelve years and counting - is itself a form of cognitive discipline the process develops in the people who persist.

### 5.2 Risk Aversion

The literature predicts that consensus-based groups choose mediocre options at significantly higher rates than individual decision-makers, because the requirement for agreement acts as a structural filter against boldness.<sup>[41]</sup> The literature also predicts that risk aversion increases with institutional tenure.<sup>[36]</sup>

The archive is consistent with both predictions.

Every "not ready for standardization" paper found in the WG21 archive was authored by members with ten or more years of committee service. In 1996, Ball wrote in [N0883](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/1996/N0883.asc)<sup>[42]</sup>:

> "We will not discover them until we have a number of implementations in use by a large number of customers. If we issue the standard with such a large and complex area untested, we will guarantee incompatible implementation, exactly the situation that the standard is trying to avoid."

In 2009, Vandevoorde observed at the WG21 meeting documented in [N2920](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2009/n2920.pdf)<sup>[43]</sup>:

> "Whenever someone implemented a feature, bugs that require changes to the standard would be found. He added that it never happened otherwise."

At the same meeting, Plauger added:

> "Nobody in programming had ever done anything non-trivial without having to massage and iterate. He claimed that one could not get it right the first time."

In 2015, eight senior members - Wakely, Kohlhoff, Williams, Orr, Allsop, Sawyer, Coe, and Partow - wrote in [P0158R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0158r0.html)<sup>[44]</sup>:

> "This is a position paper by a number of concerned authors who share a strong feeling that any coroutines proposal belongs in a TS and should not be rushed into C++17."

In 2019, Stroustrup wrote in [P1962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf)<sup>[20]</sup>:

> "Many 'perfect' languages have failed. If we are not careful, C++ can still fail. We need to be flexible and responsible."

In 2022, anonymous voters documented in [P2459R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2459r0.html)<sup>[45]</sup> wrote regarding `std::execution`:

> "This has seen way too few field experience in a lot of target domains to give any confidence that the design has really settled. If we standardize this now, some fundamental design flaws will surface only after it's too late to change this version."

In 2025, Dos Reis wrote in [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf)<sup>[46]</sup> regarding contracts:

> "Field deployment/experiments are needed."

Titus Winters documented his own trajectory toward caution in [P1863R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1863r0.pdf)<sup>[47]</sup>:

> "For the past few years, I've been advocating for WG21 to prioritize progress over backward compatibility. I'm losing faith in that position."

The LEWG chair named the institutional trend explicitly in [P2400R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r1.html)<sup>[38]</sup>:

> "Library Evolution has become more cautious."

The pattern spans thirty years. The vocabulary changes - "untested" in 1996, "rushed" in 2015, "field experience" in 2025 - but the structure is the same. Senior members recommend delay. The recommendations come from members with the longest tenure. The literature predicts this. The archive confirms it.

### 5.3 Shared Information Bias

The literature predicts that groups disproportionately discuss information everyone already knows rather than unique knowledge held by individual members. When the goal is consensus rather than finding the correct answer, this bias intensifies.<sup>[48]</sup>

Doumler and Berne documented the pattern explicitly in the contracts debate. They wrote in [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf)<sup>[49]</sup>:

> "These arguments were raised repeatedly in P3173R0, P3362R0, P3506R0, and P3573R0, responded to in P3376R0, P3500R1, P3578R1, and discussed in EWG on multiple occasions - most recently in Hagenberg - without producing new technical insight. The specific suggestion of changing the meaning of pre and post to always be checked was polled in EWG in Tokyo and rejected with strong consensus. No new information has been presented since."

Boehm titled a paper [P1217R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1217r2.pdf)<sup>[50]</sup> - "Out-of-thin-air, revisited, again." The title is the evidence.

On memory_order::consume, Boehm wrote in [P3475R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3475r1.html)<sup>[51]</sup>:

> "This problem has been recognized for around a decade. We have had much discussion around it and possible replacements. We have not agreed on a replacement."

Stroustrup identified the pattern at the meta-level in [P1962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf)<sup>[20]</sup>:

> "Hardly any paper contains extensive discussions of the proposed feature's effect in combination with other new features. Few present details of experience of use or teaching. Hardly any contain a serious discussion of objections raised."

The literature predicts that committees recycle familiar arguments. The archive shows a committee that recycles them for a decade.

### 5.4 The Abilene Paradox

The Abilene Paradox describes a failure mode where every member privately disagrees with a course of action but publicly supports it, mistakenly believing they are the only dissenter. The group ends up doing something nobody actually wanted.<sup>[52]</sup>

The Direction Group described the WG21 variant across seven revisions of their flagship paper. They wrote in [P0939R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r1.pdf)<sup>[53]</sup>:

> "Finally, after years of process, someone then stands up in full committee and raises issues that have been discussed for years stating 'lack of comfort' with the proposal, suggesting alternative approaches, and demanding more time to consider or rejection. At this point, everybody unhappy with compromises made along the way chirps in with counter-points made over the years and the proposal is either withdrawn or defeated by a 20% minority, many of whom did not take part in previous discussions."

Members sat silently through years of subgroup work. Their disagreement surfaced only at plenary. The Direction Group concluded:

> "We think that 'lack of comfort' is not sufficient to block a proposal."

An anonymous voter in the 2021 Library Evolution poll outcomes, documented in [P2451R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2451r0.html)<sup>[54]</sup>, wrote:

> "I want to participate in this poll, but I don't think I have the time/knowledge/experience with ranges to do so. I think it probably makes sense, but I'm not sure of all the ramifications. I would probably go with whatever Eric and Casey say."

The literature predicts that consensus environments produce deference voting - people voting based on social trust rather than independent technical judgment. The archive records a voter explaining, in their own words, that they vote based on deference.

### 5.5 Design by Committee

Stroustrup diagnosed the core problem in [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf)<sup>[10]</sup>:

> "We have no shared aims, no shared taste. This is a major problem, possibly the most dangerous problem we face as a committee. The alternative is a dysfunctional committee producing an incoherent language."

Voutilainen named it plainly in [P3909R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3909r0.html)<sup>[55]</sup>:

> "We have spent a whole lot of time discussing things in the abstract, and paper-designing The One True Alternative, and rejected other alternatives not by trying them out, but by discussing them. That's literally what Design By Committee means. And it ends up serving real practical users poorly."

Stroustrup elaborated the mechanism in [P1962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf)<sup>[20]</sup>:

> "'I think so' is not a technical argument. 'My company does it' is not a conclusive argument. 'I badly need it' is not a conclusive argument. 'All modern languages have it' is not a conclusive argument. 'We can implement it' is a necessary but not sufficient reason to accept a feature. 'Most people in the room liked it' is not a sufficient reason."

Sankel characterized the expected posture in [P3023R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p3023r0.html)<sup>[56]</sup>:

> "It is easy to fall into a trap thinking standard committee participation is primarily a personal opportunity for you to leave your mark on the world by getting a proposal accepted. There is nothing you have done to earn a role that can impact millions of people's lives. You cannot afford to be bullied."

**The literature predicts self-censorship, risk aversion, shared information recycling, and convergence on the least controversial option. The archive documents all four - in the committee's own words, by its own leadership, across three decades.**

### 5.6 Falsifiable Predictions: What Changes

**If this model is correct:** WG21 veterans display measurably higher risk aversion in poll voting than participants with one to three years of experience. Papers discussed in committee are more likely to converge on shared information than to surface novel technical concerns raised by a single expert. The "bring it back next meeting" outcome produces more revision effort than a clear rejection, even when the technical feedback is identical in substance.

**If this model is wrong:** Voting patterns show no correlation with tenure. Committee discussion surfaces unshared information at rates predicted by group size. Near-misses and clear rejections produce equivalent revision effort.

---

## 6. How It Socializes

The literature predicts that consensus participation changes social behavior both inside and outside the organization. Neural alignment research found that consensus-building conversations literally synchronize brain activity between participants - and this alignment persists when viewing novel content afterward.<sup>[57]</sup> The shared interpretive framework carries into situations the group never discussed together.

### 6.1 Diplomatic Indirectness

The committee's formal culture documents prescribe indirectness. The operating principles in [P0559R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0559r0.pdf)<sup>[12]</sup> state:

> "We are a diverse group of people with many backgrounds socially and culturally. Be aware of that. Be respectful of one another. Our basic starting point is that we are all seeking to make C++ better, even when we do not agree. Always use respectful language. Do not speak over other. Listen more than talk. Keep to only what you know and reduce speculation."

The Direction Group prescribed the disposition toward other proposals in [P0939R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0939r4.pdf)<sup>[58]</sup>:

> "Don't oppose a proposal just because: it is seen as competing with your favorite proposal, it is not relevant to your current job, you have not personally reviewed it, it is not perfect (according to your principles), it is not coming from your friends, it is coming from someone you have been at odds with on different subject."

The electronic straw polls paper acknowledged that in-room decisions are subject to social pressure. Adelstein Lelbach wrote in [P2195R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2195r0.html)<sup>[59]</sup>:

> "It removes the pressure and hastiness of trying to determine consensus before the end of a meeting, giving stakeholders more time to contemplate and decide their position."

He also documented that polls do not necessarily reflect genuine views:

> "Within evolution, study, and core groups, we do not make decisions using polls. We make decisions by consensus not by vote. Chairs often use polls as a mechanism to help them determine consensus. The chair's determination of consensus is authoritative, not the straw poll."

### 6.2 Identity Fusion

The committee maintains a formal emeritus process. The 2012 Portland minutes documented in [N3454](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3454.pdf)<sup>[60]</sup> recorded a nomination for emeritus status with explicit criteria:

> "Ten years or longer as a member. History of Contributions to the Committee. Retirement from the ICT Industry."

The criteria require a decade of membership and a career's worth of contributions. The emeritus designation maintains the identity connection after retirement - a formal mechanism for preserving institutional identity beyond active participation.

Clamage opened the 2014 Rapperswil meeting, documented in [N4053](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4053.pdf)<sup>[61]</sup>, with a personal announcement:

> "He's been a committee member for 25 years and the chair for 20 years. Clamage announced he's going to retire from active committee participation after Urbana."

Stroustrup chaired the Evolution Working Group for 25 years before stepping down. Sutter served as convener for 22 years and retained the title "convenor emeritus." These are not exceptional durations. They are the norm for the committee's most senior roles.

### 6.3 Falsifiable Predictions: How It Socializes

**If this model is correct:** WG21 veterans use more hedged, indirect language in reflector posts and papers than newcomers - testable by comparing linguistic markers across tenure cohorts. Social networks at meetings cluster by faction, not by technical interest. Partners or close colleagues of long-term participants would describe behavioral changes consistent with diplomatic indirectness and conflict avoidance. Former participants who left after five or more years would describe a period of social readjustment.

**If this model is wrong:** Language patterns show no correlation with tenure. Social clustering at meetings follows technical interest, not factional alignment. Partners report no behavioral spillover.

---

## 7. Evidence from the Paper Archive

The sections above interspersed academic predictions with WG21 evidence. This section examines one pattern in closer detail: the "send it to a TS" recommendation as a structural marker of the selection dynamics the model predicts.

### 7.1 The TS Scorecard

Technical Specifications published by WG21 have the following outcomes:

| TS | Published | Reached IS? | Via TS Path? |
|----|-----------|-------------|--------------|
| File System TS | 2015 | Yes (C++17) | Yes |
| Parallelism TS v1 | 2015 | Yes (C++17) | Yes |
| Coroutines TS | 2018 | Yes (C++20) | Partly |
| Concepts TS | 2017 | Yes (C++20) | Heavily redesigned |
| Ranges TS | 2017 | Yes (C++20) | Heavily redesigned |
| Modules TS | 2018 | Yes (C++20) | Heavily redesigned |
| Library Fundamentals TS v1 | 2015 | Piecemeal | Partly |
| Concurrency TS v1 | 2015 | Partly (C++20) | Partly |
| Networking TS | 2018 | No | Failed |
| Transactional Memory TS | 2015 | No | Failed |

Three TSes reached the IS in substantially the form envisioned. Four were redesigned beyond recognition before reaching the IS. Two died outright. One was picked apart.

The LEWG chair documented the institutional conclusion in [P2400R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r1.html)<sup>[38]</sup>:

> "Technical Specifications provide implementation experience, but they do not deliver the levels of usage and deployment experience, or user feedback, that we had wished for."

He continued:

> "Putting a facility into a TS uses about the same resources as it would take to put it into the International Standard."

The committee formally declared no future Library Fundamentals TSes in 2022. Poll comments documented in [P2649R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2649r0.html)<sup>[62]</sup> were blunt:

> "LFTSes fail to provide more feedbacks than regularly updated papers, and are generally a waste of time."

The Direction Group's own warning, repeated in every revision from 2018 through 2024, reads:

> "Never use a TS simply to delay; it doesn't simplify later decision making."

That the warning has been repeated for six years suggests it describes a behavior that persists.

### 7.2 Who Recommends a TS?

The "send to TS" recommendation comes almost exclusively from senior members.

The 2015 coroutines TS paper ([P0158R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0158r0.html)<sup>[44]</sup>) was signed by Wakely (committee since approximately 2003), Kohlhoff (since approximately 2005), Williams (since approximately 2004), and Orr (since the 1990s). They wrote:

> "We believe the feature would be better evolved into, and through, the Technical Specification vehicle, allowing it to be refined and tempered through experience, rather than being hurried into C++17 for later regrets and surprises."

The 2018 executors TS paper ([P1256R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1256r0.html)<sup>[63]</sup>) was authored by Vollmann, a longtime SG1 participant. He wrote:

> "Executors are way too important and usage experience is still too low to put executors forward now for C++20."

The 2024 contracts TS paper ([P3265R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3265r3.html)<sup>[64]</sup>) was authored by Voutilainen, who chaired EWG for many years. He wrote:

> "This paper suggests that Contracts should ship in a Technical Specification first, not in the C++26 IS."

Doumler and Spicer - the SG21 chairs - wrote the counter-paper. They wrote in [P3269R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3269r0.pdf)<sup>[65]</sup>:

> "Targeting a Contracts TS would be a mistake. A Contracts TS would not contribute anything meaningful toward resolving these questions and would unnecessarily delay progress."

They noted the procedural cost:

> "The TS process is slow and bureaucratic. A TS must be approved by WG21 plenary, go through a national ballot, go through NB comment resolution, be approved by WG21 plenary again, and then be published by ISO. This process takes about a year and consumes a significant amount of precious committee resources."

The model predicts that senior members exhibit higher status quo bias. "Send it to a TS" is a status quo preserving recommendation that uses the process itself as the mechanism of delay. The archive shows that every "send to TS" recommendation found in the search came from members with ten or more years of committee service.

---

## 8. The Literature Gap

No direct empirical study has administered personality inventories to long-term members of WG21, the IETF, the W3C, or IEEE. Everything in Sections 3 through 6 is triangulated from adjacent literatures. Section 7 provides the first WG21-specific evidence by testing the model's predictions against the committee's own paper archive.

A straightforward survey instrument - the Big Five Inventory (BFI-2), the Tolerance for Ambiguity Scale, and a brief demographic questionnaire - administered to WG21 regulars and compared against a matched sample of senior C++ engineers who do not participate in the committee, would test most of the predictions in this paper directly.

The falsifiable predictions in Sections 3.6, 4.5, 5.6, and 6.3 are offered as a research agenda. The predictions are specific enough to be tested. If they fail, the model is wrong.

---

## 9. Conclusion

A consensus body selects for agreeableness, emotional stability, openness, and tolerance for ambiguity. It filters out the action-oriented early, the empathetic in the middle, and converges on a residue of process-fluent, conflict-tolerant, well-resourced insiders. It develops their listening skills and their patience. It develops their risk aversion and their self-censorship. It synchronizes their brains. It becomes their identity.

The WG21 paper archive - from a 1995 compromise paper where "none of us was completely satisfied" through a 2025 paper where the EWG chair calls the process "literally what Design By Committee means" - is consistent with every major prediction the literature makes.

The model is offered as a hypothesis. The evidence is offered as a test. The reader evaluates both.

---

## References

[1] [P4241R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4241r0.html) - "Long-Term Dopaminergic Effects of Consensus Body Participation" (Vinnie Falco, 2026).

[2] [P1000R6](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p1000r6.html) - "C++ IS schedule" (Herb Sutter, 2024).

[3] [P0592R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0592r3.html) - "To boldly suggest an overall plan for C++23" (Ville Voutilainen, 2019).

[4] Herb Sutter, "Trip report: Fall ISO C++ standards meeting (Bellevue)" (2018).

[5] [P1823R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1823r0.pdf) - "Remove Contracts from C++20" (Nicolai Josuttis, Ville Voutilainen, Roger Orr, Daveed Vandevoorde, John Spicer, Vittorio Romeo, 2019).

[6] Bjarne Stroustrup, CppCon 2021 keynote.

[7] "Kill Chaos with Kindness: Agreeableness improves team performance under uncertainty" (*Sage Journals*, 2023).

[8] "Apache Developer Personality Profiles" (*arXiv*, 2019).

[9] ICmatch - "Personality Types and IC Team Member Roles."

[10] [P0939R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r0.pdf) - "Direction for ISO C++" (Beman Dawes, Howard Hinnant, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2018).

[11] [N0665R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/1995/N0665R1.ps) - "Compromise Proposal for class exception" (Jerry Schwarz, Gregory Colvin, Steve Clamage, Nathan Myers, 1995).

[12] [P0559R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/p0559r0.pdf) - "Operating principles for evolving C++" (J.C. van Winkel, J. Daniel Garcia, Ville Voutilainen, Roger Orr, Michael Wong, Pierre-Nicolas Bonnal, 2017).

[13] [N4985](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4985.pdf) - "WG21 2024-06 St Louis Minutes of Meeting" (Nina Ranns, 2024).

[14] "Who Chokes Under Pressure? The Big Five Personality Traits and Decision-Making Under Pressure" (*PMC*, 2017).

[15] "Big Five Personality Traits and Ambiguity Management in Career Decision-Making" (*Career Development Quarterly*, Wiley).

[16] "Do Birds of a Feather Flock Together? The ASA Model Revisited" (*Journal of Occupational Behavior*, Wiley, 2019).

[17] [P2260R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2260r0.pdf) - "WG21 2020-11 Virtual Meeting Record of Discussion" (Nina Ranns, 2020).

[18] "The Civic Personality" (*Political Studies*, Sage Journals).

[19] "Personality and Civic Engagement" (*American Political Science Review*, Cambridge).

[20] [P1962R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf) - "How can you be so certain?" (Bjarne Stroustrup, 2019).

[21] "Meta-analysis of Workplace Stress" (*Journal of Vocational Behaviour*, 2025).

[22] [P2000R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.html) - "Direction for ISO C++" (Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2022).

[23] "Convergence to Consensus in Heterogeneous Groups and the Emergence of Informal Leadership" (*Scientific Reports*, Gavrilets et al., 2016).

[24] [P2000R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2000r0.html) - "Direction for ISO C++" (Michael Wong, Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, 2020).

[25] [P3297R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3297r0.pdf) - "C++26 Needs Contract Checking" (Ryan McDougall et al., 2024).

[26] [P3581R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3581r0.html) - "No, inplace_vector shouldn't have an Allocator" (Nevin Liber, 2025).

[27] "Deliberative Participation and Personality" (*European Political Science Review*, Jennst&aring;l, 2018).

[28] "Representative Personalities" (IHS Working Paper, Bechtold, Gangl et al., 2024).

[29] "IETF Community Survey 2024" (IETF, 2024).

[30] [P2145R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2145r1.html) - "Evolving C++ Remotely" (Bryce Adelstein Lelbach, Titus Winters, Fabio Fracassi et al., 2020).

[31] GFSC - "Consensus Decision Making Sucks" (gfsc.community).

[32] [P2138R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2138r4.pdf) - "Rules of Design<=>Specification engagement" (Ville Voutilainen, 2021).

[33] [N4934](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4934.pdf) - "2023 WG21 admin telecon meetings" (Herb Sutter, 2023).

[34] Lorena Hoormann - "Organizations often lose the very people who could secure their future."

[35] [N5016](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/n5016.pdf) - "WG21 June 2025 Sofia Hybrid meeting Minutes of Meeting" (Nina Ranns, 2025).

[36] "Status Quo Bias in FDA Advisory Committees" (NBER Working Paper 32787, 2024).

[37] "Laboratories of Oligarchy: How the Iron Law Extends to Peer Production" (Aaron Shaw, Benjamin Mako Hill).

[38] [P2400R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2400r1.html) - "Library Evolution Report: 2021-02-23 to 2021-05-25" (Bryce Adelstein Lelbach, 2021).

[39] "Civic (Re)socialisation: The Educative Effects of Deliberative Participation" (*Politics*, 2014).

[40] "High-quality Listening Training Improves Listening Behaviors" (CentAUR, University of Reading).

[41] "Why Committees Make Worse Decisions Than Individuals" (*Medium/Illumination*, Kumar, 2026).

[42] [N0883](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/1996/N0883.asc) - "Observations on the Template Compilation Model" (Michael Ball, 1996).

[43] [N2920](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2009/n2920.pdf) - "Minutes of WG21 Meeting, July 13, 2009" (2009).

[44] [P0158R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0158r0.html) - "Coroutines belong in a TS" (Jamie Allsop, Jonathan Wakely, Christopher Kohlhoff, Anthony Williams, Roger Orr, Andy Sawyer, Jonathan Coe, Arash Partow, 2015).

[45] [P2459R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2459r0.html) - "2022 January Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, Fabio Fracassi, Ben Craig, 2022).

[46] [P3506R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3506r0.pdf) - "P2900 Is Still not Ready for C++26" (Gabriel Dos Reis, 2025).

[47] [P1863R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1863r0.pdf) - "ABI - Now or Never" (Titus Winters, 2019).

[48] "Pooling of Unshared Information in Group Decision Making" (Stasser and Titus, *Journal of Personality and Social Psychology*, 1985).

[49] [P3846R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3846r0.pdf) - "C++26 Contracts, reasserted" (Timur Doumler, Joshua Berne, 2025).

[50] [P1217R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1217r2.pdf) - "Out-of-thin-air, revisited, again" (Hans Boehm, 2019).

[51] [P3475R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3475r1.html) - "Defang and deprecate memory_order::consume" (Hans Boehm, 2025).

[52] Jerry Harvey - "The Abilene Paradox: The Management of Agreement" (1974).

[53] [P0939R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0939r1.pdf) - "Direction for ISO C++" (Beman Dawes, Howard Hinnant, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2018).

[54] [P2451R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2021/p2451r0.html) - "2021 September Library Evolution Poll Outcomes" (Bryce Adelstein Lelbach, 2021).

[55] [P3909R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3909r0.html) - "Contracts should go into a White Paper - even at this late point" (Ville Voutilainen, 2025).

[56] [P3023R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p3023r0.html) - "C++ Should Be C++" (David Sankel, 2023).

[57] "Consensus-building conversation leads to neural alignment" (*Nature Communications*, Nguyen et al., 2023).

[58] [P0939R4](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p0939r4.pdf) - "Direction for ISO C++" (Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, Michael Wong, 2019).

[59] [P2195R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/p2195r0.html) - "Electronic Straw Polls" (Bryce Adelstein Lelbach, 2020).

[60] [N3454](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2012/n3454.pdf) - "Portland 2012 Minutes" (2012).

[61] [N4053](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4053.pdf) - "WG21 2014-06 Rapperswil Minutes" (2014).

[62] [P2649R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2649r0.html) - "2022-10 Library Evolution Poll Outcomes" (2022).

[63] [P1256R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1256r0.html) - "Executors Should Go To A TS" (Detlef Vollmann, 2018).

[64] [P3265R3](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3265r3.html) - "Ship Contracts in a TS" (Ville Voutilainen, 2024).

[65] [P3269R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p3269r0.pdf) - "Do Not Ship Contracts as a TS" (Timur Doumler, John Spicer, 2024).
