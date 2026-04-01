---
title: "What Civilizations Remember"
document: P4163R0
date: 2026-03-27
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
audience: WG21
---

## Abstract

The committee endorsed profiles by 47 to 2. Then by 18 to 1. Then by white paper. Profiles are not in C++26.

This paper examines the gap between consensus and action through a lens that predates C++ by several millennia. The historical record on institutions that honor their foundational knowledge - and institutions that do not - is clear, documented, and not encouraging. The paper presents the committee's own voting record, places it alongside that historical record, and proposes a single poll: WG21 honors its own votes.

---

## Revision History

### R0: March 2026 (post-Croydon mailing)

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and the author of [P4137R0](https://wg21.link/p4137r0)<sup>[1]</sup>, "PAVE: Profile Analysis and Verification Evidence." [P3984R0](https://wg21.link/p3984r0)<sup>[2]</sup> cross-references PAVE. The author has a stake in the profiles effort succeeding. The author is telling you this so you can calibrate everything that follows.

The author is not a historian, anthropologist, or governance scholar. The civilizational evidence in this paper is drawn from published research in evolutionary biology, anthropology, and comparative history. It stands or falls on the sources, not on who assembled them. But the reader should know that one person chose which sources to assemble and in what order. That choice is itself a framing.

---

## 2. The Record

In 2023, the WG21 Direction Group - Wong, Hinnant, Orr, Stroustrup, and Vandevoorde - unanimously endorsed profiles as the mechanism for C++ to address safety concerns. They wrote in [P2759R1](https://wg21.link/p2759r1)<sup>[3]</sup>: "We now support the idea that the changes for safety need to be not just in tooling, but visible in the language/compiler and library."

In February 2023, Stroustrup presented the profiles direction to SG23 and EWG at Issaquah ([P2816R0](https://wg21.link/p2816r0)<sup>[4]</sup>). The resulting vote was 47 for and 2 against<sup>[2]</sup>.

In November 2024, SG23 at Wroclaw gave strong consensus (18-1-0) to the initialization profile and forwarded [P3081R0](https://wg21.link/p3081r0)<sup>[5]</sup> to EWG for C++26<sup>[2, 6]</sup>.

In November 2024, Microsoft stated in [P3498R0](https://wg21.link/p3498r0)<sup>[7]</sup>: "We consider that the proposals along the lines of C++ Profiles are promising."

In February 2025, EWG at Hagenberg voted to "pursue a language safety white paper in the C++26 timeframe containing systematic treatment of core language Undefined Behavior in C++, covering Erroneous Behavior, Profiles, and Contracts"<sup>[8]</sup>. The minutes note: "Many people felt that what profiles are trying to address (security, safety) is hugely critical"<sup>[8]</sup>.

In January 2026, six senior committee members - Vandevoorde, Garland, McKenney, Orr, Stroustrup, and Wong - co-signed [P3970R0](https://wg21.link/p3970r0)<sup>[9]</sup>, a call to action urging the committee to build on the profiles framework. They wrote: "SG23 and EWG have repeatedly (by massive votes) pointed to 'Profiles' as the direction for addressing these urgent needs."

Profiles are not in C++26.

---

## 3. What Civilizations Remember

The committee's voting record raises a question about institutional coherence. The historical record has an answer.

### 3.1 The Evolutionary Foundation

Human beings are the only primates whose females outlive their reproductive years by decades. In 2012, a computer simulation at the University of Utah demonstrated why: introducing menopause and grandmothering into a hypothetical primate species model produced evolution toward human-like lifespans over 60,000 years<sup>[10]</sup>. Grandmothers caring for grandchildren enabled mothers to have more offspring at shorter intervals. Extended longevity correlates with extended brain development, enabling the larger brains characteristic of humans<sup>[11]</sup>.

The traits that make civilization possible - longer lifespans, larger brains, pair bonding, cooperative behavior - are downstream of elder care<sup>[10, 11]</sup>. The evolutionary argument is simple. Elder care is not charity. It is the mechanism that produced the species.

### 3.2 The Longest Civilizations

Chinese civilization is the longest continuously existing civilization in the historical record. It is also the civilization with the most deeply codified system of elder respect. Filial piety was systematic thought by the Warring States period, a governing principle by the Han dynasty, and embedded in law by the Tang dynasty<sup>[12]</sup>. Historian Hugh D.R. Baker identifies respect for the family as "the one element common to almost all Chinese people"<sup>[13]</sup>. The principle outlasted every dynasty. It survived invasions, revolutions, and the Cultural Revolution.

Ancient Egypt venerated its elders for three thousand years. The Instruction of Ani prescribes: "Never remain seated if a man older than yourself is standing"<sup>[14]</sup>. Reaching old age was seen as evidence of divine favor<sup>[14]</sup>. The ideal lifespan in Egyptian culture was 110 years.

These are the two longest-lived civilizations in the historical record. Both structurally embedded respect for accumulated knowledge into their institutions.

### 3.3 Governance Through Elder Councils

Sub-Saharan Africa before colonial rule was governed by gerontocracies - elder councils operating through consensus rather than coercion<sup>[15]</sup>. The Giriama kambi system in Kenya functioned from approximately 1700 through the nineteenth century without centralized authority<sup>[16]</sup>. The Igbo village councils in Nigeria combined elders, age grades, and deliberative bodies<sup>[17]</sup>. Authority was horizontal. No hereditary rulers emerged.

The mechanism worked because every younger member knew they would eventually become an elder. The system's stability was built on that inevitability<sup>[15]</sup>.

### 3.4 What Happens When It Erodes

Modernization theory documents the pattern when elder status erodes. As societies transition from agrarian to industrial economies, the extended family fragments into nuclear families. Accumulated knowledge becomes less relevant. Social roles diminish. The theory's proposition - that familial support for older people declines with industrialization - has been "the principal and most common framework" for explaining this shift, in both the industrialized and the developing worlds<sup>[18]</sup>.

Three-quarters of 71 surveyed hunter-gatherer tribes venerated their elders<sup>[19]</sup>. The respect was near-universal when institutional survival depended on accumulated knowledge. It declined when the institution stopped depending on what the elders carried.

### 3.5 The Structural Principle

These systems worked because respect for elders was respect for principles, not for individuals. The elder embodied the accumulated knowledge. Honoring the elder meant honoring the continuity of the institution itself.

The civilizations that remembered this persisted. The institutions that forgot it fragmented.

---

## 4. The Founding Vision

Stroustrup writes in [P3984R0](https://wg21.link/p3984r0)<sup>[2]</sup>:

> My initial motivation to develop C++ was to combine the best of C and Simula:
>
> - C's ability to access hardware and manipulate data without overhead.
> - Simula's ability to organize programs and guarantee type safety.

Type safety was the founding aspiration. Compatibility concerns and the zero-overhead principle prevented its enforcement<sup>[2]</sup>. Forty years later, profiles are the mechanism to deliver that enforcement without abandoning either constraint.

The question is whether C++ can evolve toward its own founding aspirations - type safety, resource safety, compatibility, and zero overhead - or whether the committee's process has become structurally incapable of executing on principles it has repeatedly endorsed.

Stroustrup first responded to the safety crisis in 2022 with [P2739R0](https://wg21.link/p2739r0)<sup>[20]</sup>: "A call to action: Think seriously about 'safety'; then do something sensible about it." The committee did think seriously. It voted. It endorsed. It directed. It co-signed.

It has not shipped.

---

## 5. The Clock

Beginning in November 2022, a series of government actions created an external timeline that operates independently of the committee's internal process<sup>[2]</sup>:

- **November 2022**: The NSA published "Software Memory Safety," recommending that organizations shift to memory-safe languages<sup>[21]</sup>.
- **December 2023**: CISA, NSA, FBI, and Five Eyes allies published "The Case for Memory Safe Roadmaps," urging software manufacturers to create transition plans away from C and C++<sup>[22]</sup>.
- **February 2024**: The White House ONCD published "Back to the Building Blocks," explicitly naming C and C++ as memory-unsafe<sup>[23]</sup>.
- **October 2024**: CISA's "Product Security Bad Practices" guidance set a January 1, 2026 deadline for manufacturers to publish memory-safety roadmaps<sup>[24]</sup>.

Executive Order 14028 remains in force<sup>[25]</sup>. The underlying policy documents remain published. The enforcement mechanism was rescinded in January 2026; the direction was not. A future administration can reinstate or strengthen the mandate overnight.

The committee's deliberative process is designed for careful, considered language evolution. The regulatory threat operates on a political calendar. Without the profiles framework, every future safety response requires a new multi-year standardization effort. With it, the committee has a standing instrument: new safety guarantees can be defined, named, and enforced without further language changes<sup>[2]</sup>.

The committee has voted for the instrument. The instrument has not been built.

---

## 6. The Ask

The committee has endorsed profiles by supermajority at Issaquah. By near-unanimity at Wroclaw. By white paper at Hagenberg. By Direction Group consensus. By corporate endorsement from Microsoft. By a co-signed call to action from six of its most senior members.

The evidence in Sections 2 through 5 is public. The conclusions are the reader's.

**Proposed poll:**

> WG21 honors its own votes.

---

## 7. Conclusion

Civilizations that honor their foundational knowledge persist. Institutions that endorse principles and then fail to execute them lose coherence - first externally, then internally.

WG21 has endorsed profiles at every opportunity for three years. The regulatory clock runs whether the committee acts or not. The founding vision of C++ - type safety, resource safety, compatibility, and zero overhead - is precisely what profiles deliver.

**The committee's own record is the evidence. The committee's own votes are the precedent.**

---

## Acknowledgements

Thanks to Bjarne Stroustrup for the profiles vision and forty years of C++. Thanks to Gabriel Dos Reis for [P3589R2](https://wg21.link/p3589r2) and the framework specification. Thanks to the Direction Group - Michael Wong, Howard Hinnant, Roger Orr, Bjarne Stroustrup, and Daveed Vandevoorde - for endorsing the direction unanimously. Thanks to Daveed Vandevoorde, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, and Michael Wong for co-signing [P3970R0](https://wg21.link/p3970r0). Thanks to Kristen Hawkes for the grandmother hypothesis research that informed the evolutionary argument in Section 3.

---

## References

1. [P4137R0](https://wg21.link/p4137r0) - "PAVE: Profile Analysis and Verification Evidence" (Vinnie Falco, 2026). https://wg21.link/p4137r0

2. [P3984R0](https://wg21.link/p3984r0) - "A type-safety profile" (Bjarne Stroustrup, 2026). https://wg21.link/p3984r0

3. [P2759R1](https://wg21.link/p2759r1) - "DG Opinion on Safety for ISO C++" (Michael Wong, Howard Hinnant, Roger Orr, Bjarne Stroustrup, Daveed Vandevoorde, 2023). https://wg21.link/p2759r1

4. [P2816R0](https://wg21.link/p2816r0) - "Safety Profiles: Type-and-resource Safe programming in ISO Standard C++" (Bjarne Stroustrup, Gabriel Dos Reis, 2023). https://wg21.link/p2816r0

5. [P3081R0](https://wg21.link/p3081r0) - "Core safety Profiles: Specification, adoptability, and impact" (2024). https://wg21.link/p3081r0

6. [N5000](https://wg21.link/n5000) - "WG21 November 2024 Wroclaw Minutes of Meeting" (Nina Ranns, 2024). https://wg21.link/n5000

7. [P3498R0](https://wg21.link/p3498r0) - "Stop the Bleeding but, First, Do No Harm" (Gabriel Dos Reis, Thomas Wise, Zachary Henkel, 2024). https://wg21.link/p3498r0

8. [N5007](https://wg21.link/n5007) - "WG21 February 2025 Hagenberg Minutes of Meeting" (Nina Ranns, 2025). https://wg21.link/n5007

9. [P3970R0](https://wg21.link/p3970r0) - "Profiles and Safety: a call to action" (Daveed Vandevoorde, Jeff Garland, Paul E. McKenney, Roger Orr, Bjarne Stroustrup, Michael Wong, 2026). https://wg21.link/p3970r0

10. P. S. Kim, J. E. Coxworth, K. Hawkes. "Increased longevity evolves from grandmothering." Proceedings of the Royal Society B, 279(1749), 2012. https://royalsocietypublishing.org/doi/10.1098/rspb.2012.1751

11. Smithsonian Magazine. "New Evidence That Grandmothers Were Crucial for Human Evolution." October 2012. https://www.smithsonianmag.com/science-nature/new-evidence-that-grandmothers-were-crucial-for-human-evolution-88972191/

12. Britannica. "Confucianism: Filial Piety." https://www.britannica.com/topic/Confucianism/Filial-piety

13. H. D. R. Baker. "Chinese Family and Kinship." Columbia University Press, 1979.

14. TourEgypt. "Old Age in Ancient Egypt." https://www.touregypt.net/featurestories/oldage.htm

15. H. Ahmanson Jr. "The Gerontocratic Democracy of Old Africa, and Gerontocracy in Our Own Time." 2020. https://howardahmansonjr.com/2020/05/the-gerontocratic-democracy-of-old-africa-and-gerontocracy-in-our-own-time/

16. "Gerontocratic Government: Age-Sets in Pre-Colonial Giriama." Africa (Cambridge University Press). https://www.cambridge.org/core/journals/africa/article/abs/gerontocratic-government-agesets-in-precolonial-giriama/D4CE5CF481C15AFA6813C48EF579D60E

17. "The Pre-Colonial Traditional Political Institution." Journal of Humanities and Social Science Practice. Vol. 10, No. 4, 2024. https://iiardjournals.org/get/JHSP/VOL.%2010%20NO.%204%202024/THE%20PRE-COLONIAL%20TRADITIONAL%2050-57.pdf

18. "Status of Older People: Modernization." Encyclopedia.com. https://www.encyclopedia.com/education/encyclopedias-almanacs-transcripts-and-maps/status-older-people-modernization

19. J. Simmons. "The Role of the Aged in Primitive Society." Yale University Press, 1945. Cited via Harvard DASH. https://dash.harvard.edu/bitstreams/f447e015-3f01-4469-91e4-de39cc43980b/download

20. [P2739R0](https://wg21.link/p2739r0) - "A call to action: Think seriously about 'safety'; then do something sensible about it" (Bjarne Stroustrup, 2022). https://wg21.link/p2739r0

21. NSA. "Software Memory Safety." Cybersecurity Information Sheet. November 2022. https://media.defense.gov/2022/Nov/10/2003112742/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF

22. CISA, NSA, FBI, and international partners. "The Case for Memory Safe Roadmaps." December 2023. https://www.cisa.gov/case-memory-safe-roadmaps

23. White House ONCD. "Back to the Building Blocks: A Path Toward Secure and Measurable Software." February 2024. https://bidenwhitehouse.archives.gov/oncd/briefing-room/2024/02/26/press-release-technical-report/

24. CISA. "Product Security Bad Practices." October 2024. https://www.cisa.gov/resources-tools/resources/product-security-bad-practices

25. Executive Order 14028. "Improving the Nation's Cybersecurity." May 2021. https://nist.gov/itl/executive-order-14028-improving-nations-cybersecurity
