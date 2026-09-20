---
title: "The Pathos of P3776"
document: P4194R0
date: 2026-05-02
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

A zero-cost feature adopted by every modern language was blocked because the room did not like how it looked.

This paper uses [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup>, "More trailing commas," as a diagnostic specimen. Each committee objection is decomposed and placed adjacent to a verbatim quote from published academic literature that predicted the objection decades before the paper existed. The paper does not argue for trailing commas. The commas are the lens. The institution is the subject.

---

## Revision History

### R0

* Initial Version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author has no competing trailing-comma proposal and no stake in the outcome of [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup>.

Each committee objection in Section 4 is matched to published academic literature and to public statements from C++ users. The literature was published between 1911 and 2011. The user statements were published on r/cpp after the Kona 2025 vote. [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> was published in 2025.

This paper asks for nothing.

---

## 2. The Specimen

[P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> proposes trailing commas in function parameter lists, template parameter lists, lambda captures, and other comma-separated lists enclosed by `()`, `[]`, or `<>`. C++ already permits trailing commas in braced initializer lists and enumerator lists. The proposal extends this permission to the remaining list types.

The cost: approximately 40 lines of parser change in a Clang fork<sup>[1]</sup>. Zero runtime cost. Zero breaking changes. No alteration to the meaning of existing code.

The benefit: eight motivation sections covering text editing, version control, code generation, auto-formatter control, language consistency, macro simplification, and bug prevention. Implementation experience in a public Clang fork with a Compiler Explorer demo. An endorsement from Herb Sutter, who added trailing commas to cppfront after years of resistance<sup>[1]</sup>.

The existing practice:

| Language   | Trailing commas in parameter lists | Year added |
|------------|-----------------------------------|------------|
| Python     | Always supported                  | 1991       |
| Go         | Mandatory in multi-line           | 2009       |
| Rust       | Always supported, style guide recommends | 2015 |
| Kotlin     | Supported                         | 2020       |
| JavaScript | Supported                         | 2017       |
| TypeScript | Supported                         | 2017       |
| Swift      | Supported                         | 2025       |
| C++        | Blocked                           | -          |

The predecessor paper [P0562R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p0562r2.pdf)<sup>[3]</sup> passed EWG polls with strong consensus at Tokyo 2024:

> SF 18 / F 10 / N 2 / A 1 / SA 0

> SF 12 / F 11 / N 4 / A 3 / SA 0

Both were declared consensus. Then a parsing ambiguity in one specific case - trailing commas in a mem-initializer-list - was identified on the core reflector. The entire proposal died. [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> excludes that case, addresses every criticism raised against the predecessor, and proposes only the unambiguous contexts.

EWG polled P3776R0 at Kona 2025:

> SF 9 / F 8 / N 4 / A 8 / SA 9

**Eight languages. Forty lines of code. The committee said no.**

---

## 3. The Objections

[P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> Section 5 catalogs the objections raised by EWG. They are reproduced here without editorial.

1. **Aesthetic objections.** "It looks ugly." "This makes me deeply uncomfortable."
2. **Lack of motivation.** The paper was told it had insufficient motivation.
3. **C compatibility.** Only C++ but not C would support trailing commas.
4. **Macro semantic inconsistency.** `f(0,)` means trailing comma for functions but third-empty-argument for macros.
5. **Multiple ways to do the same thing.** Parameter lists can already be written without trailing commas.
6. **Claiming syntax space.** `f(0,)` could hypothetically mean "pass a default argument."
7. **The parsing ambiguity.** Inherited from [P0562R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p0562r2.pdf)<sup>[3]</sup>, carried forward as institutional memory despite [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> excluding the affected case.

The paper's author observed on r/cpp after the Kona 2025 vote: "People's minds were already made up before the discussion began."<sup>[[14]](#ref-14)</sup>

---

## 4. The Diagnosis

Each subsection places one committee objection adjacent to a verbatim quote from published research.

### 4.1 Goal Displacement

**The objection:** "Lack of motivation."

[P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> contains eight motivation sections. It documents implementation experience in a Clang fork. It surveys eight programming languages. It includes an endorsement from the architect of cppfront. The predecessor paper passed two EWG polls with consensus.

> "Adherence to the rules, originally conceived as a means, becomes transformed into an end-in-itself."<sup>[[4]](#ref-4)</sup>

Merton called this trained incapacity - competence at the wrong thing. The institution rewards procedural compliance because that is what it measures. The original goal recedes. In a standards body, this predicts that "motivation" is evaluated by procedural credential - revision count, study group time, the right sponsors - rather than by evidence of user need.

> "I'm a huge fan of trailing commas in programming, as it makes the physical act of writing code easier." - u/RoyAwesome<sup>[[16]](#ref-16)</sup>

> "I don't think technical problems killed the idea; I think people's minds were already made up before the discussion began. People felt that the paper lacks motivation, and it's hard to convince someone that a feature is useful when they haven't used it for 30 years." - u/eisenwave<sup>[[14]](#ref-14)</sup>

**The paper has eight motivation sections. The room found insufficient motivation.**

### 4.2 Rational Ignorance

**The objection:** "It looks ugly." "This makes me deeply uncomfortable."

Aesthetic preference has no technical basis. The objection is taste, not engineering. In a room of two hundred delegates, most have no informed opinion on the comma syntax of twenty-three grammar productions. The room voted on whether a punctuation mark was attractive.

> "It is irrational to be politically well-informed because the low returns from data simply do not justify their cost in time and other resources."<sup>[[5]](#ref-5)</sup>

When a delegate has no informed technical position, the cost of forming one exceeds the benefit of influencing one vote among two hundred. The rational response is to fall back on a heuristic. The available heuristic is taste.

> "Determining committee size always involves a quality-versus-quantity dilemma."<sup>[[6]](#ref-6)</sup>

Karotkin and Paroush show that beyond an optimal committee size, per-member competence falls with each addition. A plenary of two hundred is not the information-aggregation unit for trailing comma syntax.

> "The only reason it didn't land is because wg21 only represents a tiny slice of C++'s userbase, and it showed there." - u/James20k<sup>[[17]](#ref-17)</sup>

> "I don't get trailing commas at all. Seems like very artificial problems they're trying to solve with it... I definitely won't ever use it, it feels very wrong." - u/Jovibor_<sup>[[18]](#ref-18)</sup>

**Two hundred engineers voted on whether a comma was pretty.**

### 4.3 Informational Cascade

**The observable:** EWG polls use sequential hand-raising. Early votes are visible to later voters.

> "An informational cascade occurs when it is optimal for an individual, having observed the actions of those ahead of him, to follow the behavior of the preceding individual without regard to his own information."<sup>[[7]](#ref-7)</sup>

The cascade mechanism: Early "Against" votes on aesthetics are visible. A delegate with no strong opinion observes the early hands and follows. The room converges on a shared position that has no technical basis.

> "Although groups are initially 'wise,' knowledge about estimates of others narrows the diversity of opinions to such an extent that it undermines the wisdom of crowd effect."<sup>[[8]](#ref-8)</sup>

Social influence reduces opinion diversity without increasing accuracy. The aggregate mild aesthetic discomfort of a room that can see each other's hands is manufactured into institutional consensus.

> "P3776R1 'More trailing commas,' which I thought had had extremely strong consensus given its utility to diff-viewers and code-generators, apparently somehow received perfect non-consensus (9-8-4-8-9) in EWG. That's odd news." - Arthur O'Dwyer<sup>[[15]](#ref-15)</sup>

> "The discussion on the mailing list around this one was absolutely crazy. Lots of people saying who even reviews/works with diffs... Its one of those threads which I wish was public, because I suspect people would be pretty shocked at committee member logic." - u/James20k<sup>[[17]](#ref-17)</sup>

### 4.4 Shifting Baseline

**The objection:** "Multiple ways to do the same thing." "C compatibility."

C++ already permits trailing commas in braced initializer lists and enumerator lists. It prohibits them in parenthesized lists, angle-bracketed lists, and square-bracketed lists. This inconsistency is the anomaly. Every other language in the table above corrected it.

> "Each generation of fisheries scientists accepts as a baseline the stock size and species composition that occurred at the beginning of their careers, and uses this to evaluate changes. The result obviously is a gradual shift of the baseline, and inappropriate reference points."<sup>[[9]](#ref-9)</sup>

Delegates who entered C++ when trailing commas were inconsistent accept the inconsistency as the baseline. The correction is perceived as the novelty. The anomaly is perceived as the norm.

> "I love more trailing commas, it's a feature that feels so good when using kotlin." - u/LiAuTraver<sup>[[19]](#ref-19)</sup>

> "It makes C++ more self-consistent, as trailing commas are already supported in initializer lists, designated initializers, and enumerations. So adding it to function and template parameters harmonizes the family of lists more." - u/fdwr<sup>[[20]](#ref-20)</sup>

**The anomaly is the status quo. The correction is the proposal.**

### 4.5 Professional Socialization

**The objection vocabulary:** "Lack of motivation." "Claiming syntax space." Process language.

Users say: "I want trailing commas." The committee says: "Insufficient motivation." The word "motivation" has been redefined. In the user's vocabulary, motivation means a reason to want the feature. In the committee's vocabulary, motivation means a procedural justification that satisfies the room's evaluative framework.

> "Learning viewed as situated activity has as its central defining characteristic a process that we call legitimate peripheral participation."<sup>[[10]](#ref-10)</sup>

Newcomers to a community of practice progressively adopt the community's norms, vocabulary, and definition of competence through participation. The process is learning, not indoctrination. The cost is that the community's definition of "motivation" replaces the user's definition. The delegate who has attended fifteen meetings no longer hears "I want trailing commas" as motivation. They hear it as a user preference that has not yet been converted into the procedural form the institution recognizes.

> "The committee isn't made up of C++ users. It's made up of people who are capable of spending the thousands of dollars a year to take part. Every individual should probably recognize the bias that introduces into the decision making process." - u/RoyAwesome<sup>[[21]](#ref-21)</sup>

> "Its weird seeing committee members go 'well I don't have a use case for this feature, so I'm going to kill it!'" - u/James20k<sup>[[22]](#ref-22)</sup>

### 4.6 The Immune System

**The observable:** [P0562R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p0562r2.pdf)<sup>[3]</sup> passed EWG with consensus. One parsing ambiguity in one specific case killed the entire proposal. [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> excluded that case, addressed every criticism, implemented the change in 40 lines. The system generated new objections.

> "Who says organization, says oligarchy."<sup>[[11]](#ref-11)</sup>

> "In any bureaucracy, the people devoted to the benefit of the bureaucracy itself always get in control, and those dedicated to the goals the bureaucracy is supposed to accomplish have less and less influence, and sometimes are eliminated entirely."<sup>[[12]](#ref-12)</sup>

The parsing ambiguity was resolved. The aesthetic objections were addressed. The motivation sections were expanded. The implementation was provided. The objections changed. The outcome did not.

> "I wonder if that paper had gone through whether it would have shifted the tide for P3776R1... Well, there are other ways to progress past a mumpsimus crowd, like `#embed` which started in C++, then had to go all the way through C to finally reach C++ again." - u/fdwr<sup>[[23]](#ref-23)</sup>

> "I would really love to see this for member initializers, at least..." - u/johannes1971<sup>[[24]](#ref-24)</sup>

**The committee found consensus, then found a reason to lose it.**

### 4.7 The Dead Tradition

**The quote:** [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> Section 5.1 cites Bjarne Stroustrup's *Design and Evolution of C++*:

> "It is more important to allow a useful feature than to prevent every misuse."<sup>[[13]](#ref-13)</sup>

The committee blocked the feature on aesthetics. Stroustrup's design principle says useful features take precedence over preventing misuse. The room's aesthetic discomfort is a form of misuse prevention - the fear that someone might write `f(0,)` and it might look wrong. The principle and the outcome point in opposite directions.

The rules survive. The reasons are lost.

> "C++ is famous for its own users observing that 'all the defaults are wrong', and that's an indictment of this very process because WG21 picked those defaults." - u/tialaramex<sup>[[25]](#ref-25)</sup>

> "I'm a huge fan of trailing commas in programming, as it makes the physical act of writing code easier. There are times when you copy+paste some code from elsewhere in your project and make changes. Or you re-order things. Having trailing commas just makes the actual act of programming easier." - u/RoyAwesome<sup>[[16]](#ref-16)</sup>

**Stroustrup wrote the principle. The committee blocked the feature.**

---

## 5. The Control Group

Seven language committees faced the same question: Should trailing commas be permitted in function parameter lists? The table records their answers.

| Language   | Decision          | Year | Process duration  |
|------------|-------------------|------|-------------------|
| Python     | Always permitted  | 1991 | No proposal needed |
| Go         | Mandatory (multi-line) | 2009 | Language design decision |
| Rust       | Always permitted  | 2015 | No proposal needed |
| JavaScript | Permitted         | 2017 | One TC39 proposal cycle |
| TypeScript | Permitted         | 2017 | Followed JavaScript |
| Kotlin     | Permitted         | 2020 | One language update |
| Swift      | Permitted         | 2025 | One Swift Evolution proposal |
| C++        | Blocked           | -    | Two papers, multiple years |

---

## 6. Predictions

If the diagnosis in Section 4 is correct, the following predictions are falsifiable.

1. [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> will require three or more revisions to advance through EWG.

2. The objections raised against R2 and subsequent revisions will be structurally similar to the objections raised against R0 and R1. New objections will appear as old ones are addressed.

3. Trailing commas will ship in C (via WG14) before they ship in C++. WG14 is smaller and less susceptible to the committee-size effects described in Section 4.2.

4. No EWG member who voted SA or A on the Kona 2025 poll will cite deployment evidence, user survey data, or measured productivity impact in support of their position.

Each prediction has a defined verification date. Predictions 1 and 2 can be evaluated at each subsequent meeting where [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> appears. Prediction 3 can be evaluated when either WG14 or WG21 acts. Prediction 4 can be evaluated immediately from the public record.

---

## 7. Acknowledgments

Jan Schultke authored [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html)<sup>[1]</sup> and addressed every criticism with technical precision. The paper's quality makes the committee's response legible as an institutional phenomenon rather than a technical disagreement.

---

## References

<a id="ref-1"></a>
[1] [P3776R1](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3776r1.html) - "More trailing commas" (Jan Schultke, 2025).

<a id="ref-2"></a>
[2] [P4003R0](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4003r0.pdf) - "I/O Awaitables" (Vinnie Falco, 2026).

<a id="ref-3"></a>
[3] [P0562R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p0562r2.pdf) - "Trailing Commas in Base-clauses and Ctor-initializers" (Alan Talbot, 2024).

<a id="ref-4"></a>
[4] Robert K. Merton - ["Bureaucratic Structure and Personality"](https://www.csun.edu/~snk1966/Robert%20K%20Merton%20-%20Bureaucratic%20Structure%20and%20Personality.pdf) (*Social Forces*, Vol. 18, No. 4, pp. 560-568, 1940).

<a id="ref-5"></a>
[5] Anthony Downs - [*An Economic Theory of Democracy*](https://en.wikipedia.org/wiki/An_Economic_Theory_of_Democracy) (Harper & Row, 1957).

<a id="ref-6"></a>
[6] Drora Karotkin and Jacob Paroush - ["Optimum committee size: Quality-versus-quantity dilemma"](https://link.springer.com/article/10.1007/s003550200190) (*Social Choice and Welfare*, Vol. 20, pp. 429-441, 2003).

<a id="ref-7"></a>
[7] Sushil Bikhchandani, David Hirshleifer, and Ivo Welch - ["A Theory of Fads, Fashion, Custom, and Cultural Change as Informational Cascades"](https://www.journals.uchicago.edu/doi/abs/10.1086/261849) (*Journal of Political Economy*, Vol. 100, No. 5, 1992).

<a id="ref-8"></a>
[8] Jan Lorenz, Heiko Rauhut, Frank Schweitzer, and Dirk Helbing - ["How social influence can undermine the wisdom of crowd effect"](https://www.pnas.org/doi/full/10.1073/pnas.1008636108) (*PNAS*, Vol. 108, No. 22, pp. 9020-9025, 2011).

<a id="ref-9"></a>
[9] Daniel Pauly - ["Anecdotes and the shifting baseline syndrome of fisheries"](https://www.cell.com/trends/ecology-evolution/abstract/S0169-5347(00)89171-5) (*Trends in Ecology and Evolution*, Vol. 10, No. 10, p. 430, 1995).

<a id="ref-10"></a>
[10] Jean Lave and Etienne Wenger - [*Situated Learning: Legitimate Peripheral Participation*](https://www.cambridge.org/highereducation/books/situated-learning/6915ABD21C8E4619F750A4D4ACA616CD) (Cambridge University Press, 1991).

<a id="ref-11"></a>
[11] Robert Michels - [*Political Parties: A Sociological Study of the Oligarchical Tendencies of Modern Democracy*](https://socialsciences.mcmaster.ca/econ/ugcm/3ll3/michels/polipart.pdf) (1911).

<a id="ref-12"></a>
[12] Jerry Pournelle - ["The Iron Law of Bureaucracy"](http://jerrypournelle.com/reports/jerryp/iron.html) (2006).

<a id="ref-13"></a>
[13] Bjarne Stroustrup - [*The Design and Evolution of C++*](https://stroustrup.com/dne.html) (Addison-Wesley, 1994).

<a id="ref-14"></a>
[14] u/eisenwave - ["Progress report for my proposals at Kona 2025"](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/) (r/cpp, November 2025).

<a id="ref-15"></a>
[15] Arthur O'Dwyer - ["How my papers did at Kona"](https://quuxplusone.github.io/blog/2025/11/18/kona-trip-report/) (November 2025).

<a id="ref-16"></a>
[16] u/RoyAwesome - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np6kz9x/) (r/cpp, November 2025).

<a id="ref-17"></a>
[17] u/James20k - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np8hkn5/) (r/cpp, November 2025).

<a id="ref-18"></a>
[18] u/Jovibor_ - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np8axnz/) (r/cpp, November 2025).

<a id="ref-19"></a>
[19] u/LiAuTraver - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np6ahun/) (r/cpp, November 2025).

<a id="ref-20"></a>
[20] u/fdwr - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/npaj128/) (r/cpp, November 2025).

<a id="ref-21"></a>
[21] u/RoyAwesome - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np8icef/) (r/cpp, November 2025).

<a id="ref-22"></a>
[22] u/James20k - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np8jruy/) (r/cpp, November 2025).

<a id="ref-23"></a>
[23] u/fdwr - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/npake6m/) (r/cpp, November 2025).

<a id="ref-24"></a>
[24] u/johannes1971 - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np83cmx/) (r/cpp, November 2025).

<a id="ref-25"></a>
[25] u/tialaramex - [comment on P3776R1](https://old.reddit.com/r/cpp/comments/1oyltrq/progress_report_for_my_proposals_at_kona_2025/np7732j/) (r/cpp, November 2025).
