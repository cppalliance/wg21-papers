| Document | D0000 |
|----------|-------|
| Date | 2026-01-02 |
| Reply-to | Vinnie Falco \<vinnie.falco@gmail.com\> |
| Audience | WG21 |

# Measuring Success: Evaluating WG21

## Abstract

WG21 produces metrics: papers published, meetings held, standards shipped on schedule. But are these measures of success, or merely measures of activity? This paper examines how WG21 evaluates its own performance, identifies what it measures and what it avoids measuring, and asks the question no standing document answers: who is WG21 accountable to, and what happens when it fails?

We find that WG21's success metrics are largely unfalsifiable—they measure process completion rather than user outcomes. The committee tracks papers but not adoption, attendance but not mentorship, features shipped but not features used. Most critically, it has no mechanism to measure whether it is passing on the knowledge and judgment that made the committee functional in the first place.

These are not criticisms of individuals. Great Founder Theory observes that functional institutions are rare—most organizations exhibit exactly these patterns. WG21 is not uniquely dysfunctional; it is typically dysfunctional, in ways that follow predictably from its structure. The question is whether the committee can recognize these patterns and address them before the founding generation's knowledge is lost.

---

## 1. The Measurement Gap

A business reports to shareholders. A government reports to voters. A standards body reports to... whom?

WG21 publishes convener's reports and direction papers citing impressive numbers: developer population growth (31M→47M from 2022-2025), TIOBE rankings (#2 language), three-year release cadence maintained. The narrative is one of success.

But these metrics measure C++'s installed base, not committee effectiveness. C++ would have millions of developers regardless of WG21's performance—momentum from decades of deployment ensures that. The relevant question isn't whether C++ is popular. It's whether WG21's decisions make it better.

That question goes unanswered. Not because the answer is negative, but because no one is asking.

---

## 2. What WG21 Counts

The committee's self-assessment emphasizes activity metrics:

| Metric | What It Measures | What It Doesn't Measure |
|--------|------------------|------------------------|
| Standards shipped | Process completion | Whether content is good |
| Three-year cadence | Schedule adherence | Whether rushing helps |
| Paper count | Activity volume | Whether activity adds value |
| Attendance | Participation quantity | Participation quality |
| Feature additions | Scope expansion | Whether features are used |

These metrics answer: "Is WG21 busy?" They don't answer: "Is WG21 effective?"

The committee's success narrative relies on appeals that cannot fail: scale (C++ has many developers), schedule (we ship on time), activity (many papers), scope (many features). These are unfalsifiable—they cannot distinguish a functional process from a dysfunctional one that ships on schedule.

---

## 3. What WG21 Doesn't Count

### 3.1 Outcome Metrics

No standing document tracks:

| Missing Metric | What It Would Reveal |
|----------------|---------------------|
| Feature adoption rates | `std::regex` is avoided; `std::optional` is embraced |
| Time-to-usability | Coroutines took 3 years to become usable |
| Workaround prevalence | Abseil, Folly, BDE replace standard components |
| Survey responsiveness | Networking: top request for a decade, still missing |

The committee cannot learn from outcomes it doesn't measure.

### 3.2 Knowledge Transmission Metrics

Here is the deepest gap: **WG21 doesn't measure whether it is passing on its knowledge.**

| Knowledge Metric | Status |
|------------------|--------|
| Formal mentorship programs | None exist |
| Mentor-mentee pairings | Not recorded |
| Progress reports on newcomers | Not produced |
| Competency evaluation | Not performed |

Consider what a functioning tradition would track: How many newcomers received structured mentorship? How many can articulate why certain features belong in the standard and others don't? Which senior members are actively mentoring?

WG21 tracks none of this. The committee has grown from dozens to hundreds of participants, but there is no mechanism to ensure new participants understand the principles that guided early decisions.

> "Traditional master-apprentice relationships are the gold standard for these training relationships... Otherwise, the knowledge simply isn't transferred, and with many crafts, is lost forever."

The Sunday orientation tells newcomers where the rooms are. It doesn't teach them what WG21 values.

### 3.3 The Falsifiability Problem

A meaningful success metric must be falsifiable—it must be possible to fail.

WG21's current metrics cannot indicate failure. Compare to falsifiable alternatives:

| Current Metric | Falsifiable Alternative |
|----------------|------------------------|
| Papers published | >80% of features adopted within one cycle |
| Attendance growing | >50% of newcomers complete mentorship |
| Standards shipped | <10 LWG issues per 100 pages of specification |

An institution that cannot fail cannot learn.

---

## 4. The Accountability Void

### 4.1 Who Is WG21 Accountable To?

| Stakeholder | Accountability Mechanism |
|-------------|-------------------------|
| ISO | Administrative compliance only |
| National bodies | Representation, not oversight |
| Users | None—no representatives with power |
| Implementers | Implicit veto only (can ignore the standard) |

The structure creates a void. ISO provides administrative framework but doesn't evaluate whether C++ is improving. National bodies ensure countries are represented but don't assess effectiveness. Users have no formal representation—their only power is the exit option.

**WG21 is accountable to no one for outcomes.** It is accountable only for process compliance.

### 4.2 What Happens When It Fails?

When a business fails, shareholders intervene. When a government fails, it loses elections. What happens when WG21 fails?

- **Contracts (2019)**: Years of work, "most impactful feature of C++20" (Sutter), then removed. *No accountability review, no process changes.*
- **Ranges (2020)**: Less capable than `std::find`. *No regression analysis, shipped permanently.*
- **Networking (2017-2026)**: Top user request for a decade, repeatedly deferred. *No explanation required.*

There is no mechanism to recognize failure, no procedure to correct it, no accountability to anyone who would demand correction. No standing document defines what committee failure looks like.

This is not unusual. Great Founder Theory observes:

> "Functional institutions are the exception, not the rule."

Most institutions exhibit exactly this pattern: formal trappings of rigor while lacking mechanisms to assess whether their evaluations predict success. WG21 is typical, not aberrant.

---

## 5. Why This Happens

### 5.1 The Incentive Structure

Great Founder Theory examines why rational individuals in institutions produce irrational outcomes. The answer lies in incentives:

**Paper authors** benefit from shipping regardless of adoption—publication is the reward.

**Corporate sponsors** advance strategic interests, not user satisfaction metrics.

**Committee chairs** are evaluated by process management—smooth meetings, predictable schedules.

**Senior members** have no incentive to formalize mentorship—informal influence is power.

The structure rewards activity, not impact. Measuring impact would reveal that much activity has negative value. Measuring knowledge transfer would reveal that expertise isn't transferring. No one's career benefits from documenting these facts.

### 5.2 The Dead Player Pattern

Great Founder Theory defines a "dead player" as one working off script, incapable of doing new things:

- Papers follow standard format ✓
- Revisions address committee feedback ✓
- Process continues on schedule ✓
- But no external validation occurs ✗
- No retrospectives evaluate success ✗
- No mechanism to learn from failure ✗

The committee maintains formal trappings of rigor while lacking mechanisms to assess whether evaluations predict success. This is the signature of institutional decay—process continues, outcomes degrade, and no one measures the difference.

Again, this pattern is common. Most long-lived institutions exhibit it. The question is whether WG21 can recognize the pattern and break it.

---

## 6. The Evidence

Three patterns illustrate the measurement gap:

**Priority inversion**: Freestanding has consumed 14+ years of effort for a "tiny" community that "cannot provide timely feedback" (Macieira, 2023). Networking—top user request for a decade, 20 years of Boost.Asio validation—has been repeatedly deferred. If WG21 measured demand vs. resource allocation, this inversion would be visible.

**Capability regression**: `std::ranges::find` fails where `std::find` succeeds (over-constrained concepts). If WG21 measured capability regression, this would be flagged before shipping.

**Framework-first pattern**: C++20 shipped coroutines without `std::generator`; C++26 ships `std::execution` without usable types. P2300 authors cite coroutines as precedent. If WG21 measured time-to-usability, this pattern would show as recurring failure.

---

## 7. What We're Losing

WG21 has perhaps ten years before the founding generation is largely gone. Stroustrup is approximately 75. Sutter is approximately 60. The implicit knowledge they carry—why decisions were made, what was considered and rejected—is not documented and not being systematically transferred.

> "A living tradition of knowledge is a tradition whose body of knowledge has been successfully transferred, i.e., passed on to people who comprehend it."

New participants learn to navigate process: how to write papers, present proposals, respond to feedback. This is procedural knowledge. It is not the same as understanding what belongs in the standard and what doesn't.

> "Students of a tradition can appear to possess understanding of a tradition's body of knowledge despite actually lacking it. This is counterfeit understanding."

A committee that doesn't measure knowledge transmission cannot detect counterfeit understanding. Every year, the ratio shifts—more people who know the forms, fewer who know the substance.

Without accountability, no mechanism recognizes degradation. Features regress in capability. Decades pass without shipping high-demand features. Frameworks ship without usable types. The founding generation ages out. And no metric captures any of it.

---

## 8. What Must Change

These recommendations address the process, not individuals. The problem is structural.

### 8.1 Create Accountability Structure

- **Define success criteria** in writing—feature adoption, user satisfaction, knowledge transfer. Make them falsifiable.
- **Establish oversight** mechanisms for stakeholders to evaluate performance. Not advisory—evaluative.
- **Publish retrospectives** after each standard. What worked? What failed? Create institutional memory.

### 8.2 Measure Outcomes

- **Track adoption** one cycle after standardization. What problems emerged? What workarounds exist?
- **Track responsiveness** to user surveys. If networking is #1 for a decade, why isn't it shipping?

### 8.3 Measure Knowledge Transmission

- **Establish formal mentorship**. Pair newcomers with experienced members. Track outcomes.
- **Evaluate understanding** before voting privileges. Not procedures—principles.
- **Verify knowledge transfer**. Can newcomers articulate the generating principles of C++ standardization?

### 8.4 Make Failure Visible

- **Define failure criteria** explicitly. What would committee failure look like?
- **Report against criteria** in convener's reports. If criteria aren't met, acknowledge it.
- **Create correction procedures**. When failure is recognized, what happens?

---

## 9. The Choice

WG21 faces a choice: **measure what matters, or measure what's easy.**

Measuring what's easy means counting papers, attendance, features shipped. It means success by cheerleading, no retrospectives, no knowledge transfer verification. It means the founding generation's knowledge dies with them.

Measuring what matters means tracking adoption, defects, mentorship outcomes. It means defining failure and reporting against it. It means creating accountability to someone who cares whether C++ improves.

This is not a criticism of individuals. The people contributing to WG21 are talented and well-intentioned. But talent and good intentions, operating within a structure that measures activity rather than outcomes, cannot ensure good results. The structure must change.

Great Founder Theory observes that most institutions fail to make this transition. They continue until external pressure forces change or the institution becomes irrelevant. WG21 has an opportunity to be the exception—to recognize the pattern and break it while the founding generation can still help.

The clock is running.

---

## Acknowledgements

This analysis draws on Samo Burja's Great Founder Theory for the framework of institutional health, accountability, and knowledge transmission. The case studies emerge from publicly available WG21 papers, mailing list discussions, and community feedback.

This paper critiques WG21's process and structure, not the individuals who contribute their time and expertise to C++ standardization.

---

## References

### Great Founder Theory

- Burja, Samo. [Great Founder Theory](https://www.samoburja.com/gft/). 2020.

### WG21 Papers and Documents

- P1823R0, P2899: Contracts removal and rationale
- P2300: std::execution proposal
- [SD-4: WG21 Practices and Procedures](https://isocpp.org/std/standing-documents/sd-4-wg21-practices-and-procedures)
- [P2000: Direction for ISO C++](https://wg21.link/P2000)
- [N4990: WG21 2023-2024 Convener's Report](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/n4990.pdf)

### Community Sources

- Sutter, Herb. Year-end blog posts (2024, 2025)
- Macieira, Thiago. ISO C++ mailing list discussions

---

## Notes

Unattributed block quotes are from *Great Founder Theory* by Samo Burja.

---

## Revision History

- R0 (2026-01-01): Initial version
