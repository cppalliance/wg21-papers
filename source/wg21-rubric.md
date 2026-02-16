# WG21 Paper Evaluation Rubric

A rubric for evaluating WG21 papers, distilled from patterns of critique applied across technical, polemical, and priority papers targeting `std::execution` and C++ networking.

## 1. Claims Match Evidence

Does every factual claim have a citation, benchmark, or verifiable source? Does the paper distinguish between demonstrated facts and plausible-but-unsubstantiated assertions?

- **Strong**: Primary sources, benchmarks, poll records, code excerpts from specifications
- **Weak**: Back-of-envelope estimates presented as conclusions, plausible assertions without measurement, theoretical performance arguments with no profiling data
- **Red flag**: "X becomes the bottleneck" without showing it became the bottleneck

## 2. Terminology Precision

Does the paper use terms that match the severity of the thing being described? Overstatement invites dismissal even when the underlying concern is real.

- **Strong**: "Silent performance degradation under load" when describing suboptimal-but-correct behavior
- **Weak**: "Silent failure" for something that works correctly but slowly
- **Red flag**: Emotionally loaded framing that the opposition can trivially deflect by pointing out the term is inaccurate

## 3. Problem Decomposition

Does the paper separate problems that have different causes, even when they co-occur? Bundling distinct problems into a single label overstates the scope of what is uniquely wrong with the target.

- **Strong**: Problem A is structural to the protocol; Problem B is structural to the language. They need different solutions
- **Weak**: Treating co-occurring problems as a single issue ("the allocator sequencing gap" when two separable gaps exist)
- **Red flag**: A recommendation that addresses both problems when the paper has only demonstrated one

## 4. Remedy Proportionality

Is the recommendation proportionate to the demonstrated problem? A defect in one use case does not justify deferring an entire framework that serves multiple use cases.

- **Strong**: Remedy scoped to the part of the design that has the defect (e.g. "ship without `task`")
- **Weak**: Recommending deferral of the whole framework for a gap that affects one use case
- **Red flag**: The paper acknowledges other use cases work well, then recommends a remedy that blocks them too

## 5. Engagement with Obvious Compromises

Does the paper address the most obvious middle-ground options, even if only to explain why they are insufficient?

- **Strong**: Considers "ship without the contested component, iterate for C++29" and explains why it does or does not work
- **Weak**: Jumps from problem identification to maximalist recommendation without discussing incremental alternatives
- **Red flag**: Silence on the compromise the committee will obviously ask about

## 6. Engagement with Counterarguments

Does the paper address the strongest version of the opposing position? Does it acknowledge when a problem is inherent to the domain rather than specific to the target?

- **Strong**: "This problem would exist in any coroutine framework, including the author's own alternative" - acknowledged and reckoned with
- **Weak**: Criticizes the target for a problem that is intrinsic to the language (e.g. allocator propagation difficulty predates sender/receiver)
- **Red flag**: Citing the target's limitations without disclosing that the proposed alternative shares them

## 7. Historical Analogies

Does the paper use historical comparisons where the structural parallels are tight, or does it reach for superficially similar but structurally different cases?

- **Strong**: CORBA vs. `std::execution` - standards-consortium-designed universal middleware with bundled concerns, competing against narrow pragmatic alternatives, primary use case deferred. Structural parallel is tight on multiple independent axes
- **Weak**: OSI vs. TCP/IP as a one-line aside without developing the structural comparison
- **Red flag**: Grand historical analogies (OSI, architecture astronauts) used as rhetorical weight rather than analytical tools

## 8. Scope Alignment Between Evidence and Recommendations

Does the evidence support the specific recommendation, or does it support a weaker conclusion that the paper escalates into a stronger one?

- **Strong**: Evidence shows networking should not be gated on `std::execution`; recommendation says don't gate networking on `std::execution`
- **Weak**: Evidence shows networking should not be gated; recommendation says remove `std::execution` from C++26 entirely
- **Red flag**: The paper's own evidence more naturally supports a conclusion it presents as secondary

## 9. Constructive Direction

Does the paper provide enough constructive content that the committee can act on it, or does it stop at critique?

- **Strong**: Identifies the problem, sketches a solution direction, provides code showing what the alternative looks like, and explains why it is feasible
- **Weak**: Convincingly demonstrates a gap exists but offers no sketch of what a fix requires or how long it would take
- **Red flag**: "This is broken" with no indication of whether fixing it is a one-cycle change or a five-cycle language redesign

## 10. Completeness of Technical Analysis

Does the paper address known solutions, workarounds, and partial mitigations, even if only to explain their insufficiency?

- **Strong**: Discusses PMR as a partial solution, thread-local allocator registries, coroutine-local storage, and explains why each is or is not adequate
- **Weak**: Identifies a gap but does not engage with the ecosystem of workarounds that practitioners already use
- **Red flag**: The opposition can respond "did you consider X?" and the paper has no answer

## 11. Comparison Fairness

When comparing the target to alternatives, does the paper hold them to the same standard?

- **Strong**: "The proposed alternative also has this limitation, and here is how it handles it differently" or "here is why the limitation matters less in the alternative's design"
- **Weak**: Cataloguing limitations of the target without disclosing whether the proposed alternative shares them
- **Red flag**: The alternative is presented only in its best light while the target is presented only in its worst

## 12. Political Feasibility Awareness

Does the paper distinguish between what the evidence supports and what the committee is likely to do? Does it separate asks of different political difficulty so the committee can act on the achievable one even if it rejects the ambitious one?

- **Strong**: Primary recommendation (achievable, well-supported) explicitly separated from secondary recommendation (ambitious, justified but politically harder). The committee can adopt either independently
- **Weak**: A single all-or-nothing recommendation with no fallback
- **Red flag**: The paper's strongest evidence supports the modest ask, but the paper leads with the maximalist one

## 13. Defect Contextualization

When citing defects, instability, or design churn as evidence, does the paper provide a baseline? Every newly standardized feature has defects. The question is whether the rate or severity is abnormal.

- **Strong**: Compares defect rate to `<ranges>`, `<format>`, or other features at the same lifecycle stage
- **Weak**: Lists defects without context, implying the mere existence of defects is damning
- **Red flag**: "Priority 1 LWG defects exist" without noting that every major feature has them

## Using This Rubric

No paper will score perfectly on all dimensions. The rubric is diagnostic, not prescriptive. A polemical paper can legitimately lean on rhetoric (dimension 7) as long as the structural parallels are tight. A technical paper can omit political feasibility (dimension 12) if it is addressing a design group rather than plenary. A priority paper can omit benchmarks (dimension 1) if its argument is about committee resource allocation rather than runtime performance.

The rubric's value is in identifying where a paper is vulnerable to the opposition's strongest response. For each dimension that scores weak or red-flag, ask: can the opposition dismiss the paper by pointing at this gap? If yes, the paper needs revision on that dimension before it goes to committee.
