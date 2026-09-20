---
title: "Long-Term Dopaminergic Effects of Consensus Body Participation"
document: P4241R0
date: 2026-05-22
intent: info
audience: WG21
reply-to:
  - "Vinnie Falco <vinnie.falco@gmail.com>"
---

## Abstract

The reward structure of consensus-based standards bodies follows the four-phase trajectory of behavioral addiction: first exposure, habituation, tolerance with dose escalation, and dependence. This paper maps each phase to published neuroscience, documents the asymmetry between reward habituation and defeat sensitization that drives escalation, identifies the intermittent reinforcement schedule (five days on, four months off) as the maximally addictive exposure pattern known in pharmacological research, and provides falsifiable experiential claims the reader tests against their own participation history. The framework applies ICD-11 core criteria - conflict, withdrawal, relapse, behavioral salience - rather than peripheral indicators, and presents itself as a structural analysis of the system's reward architecture, not a clinical diagnosis of any individual participant.

---

## Revision History

### R0: August 2026

- Initial version.

---

## 1. Disclosure

The author provides information and serves at the pleasure of the committee.

The author is the founder of the C++ Alliance and maintains competing proposals in the `std::execution` space. The author's first attended WG21 meeting was in 2018. The neuroscience and psychology literature presented here applies to every consensus body operating under intermittent reinforcement with permanent outcomes, including bodies whose decisions the author agrees with. The author is a participant in the system this paper describes and is subject to the same mechanisms.

This paper asks for nothing.

---

## 2. The Moment

You remember your first accepted paper with unusual clarity. The room. The numbers. The moment the chair spoke the result. You remember the physical sensation - a release, a warmth, something disproportionate to what was, on paper, a routine procedural outcome in a volunteer standards organization.

You also remember your first rejection. The numbers read against you. The room moved to the next agenda item. Your years of work were already forgotten. The sting was also disproportionate. It was a standards decision, not a personal verdict - yet it did not feel that way.

Both memories are stored with a vividness normally reserved for weddings, accidents, and other events the brain flags as life-defining. Both are disproportionate to stated stakes. Both are universal among participants who have experienced them. This section does not explain them. It names them, and asks the reader to recall their own version before proceeding.

JeanHeyd Meneide described the experience of his first accepted paper as "The First Win." Arthur O'Dwyer maintains a public scoreboard of his committee results. Herb Sutter described "sustained rounds of applause" at plenary. Each account describes an experience whose intensity exceeds what a volunteer procedural outcome should produce. The question this paper investigates is: why?

The defeat side is equally telling. The first rejection produces a drive to "come back stronger" - or to leave entirely. Both responses are adaptive in evolutionary terms. Neither is proportionate to a committee decision about a programming language. The selection between these responses - who comes back, who leaves - is the beginning of the mechanism this paper documents.

**What it feels like:**

- Winner: memory stored with unusual clarity - the room, the numbers, the moment. Disproportionate elation lasting hours to days.
- Loser: memory equally vivid. Physical sensation persists years later. Immediate drive to revise, to fix, to return.

**What to look for:**

- Disproportionate excitement after first acceptance - colleagues notice the person glowing for days
- Immediate desire to submit another paper before the first has been published
- Retelling the acceptance story repeatedly, with precise poll numbers
- After first rejection: uncharacteristic withdrawal, rumination, or sudden intensification of effort
- Emotional reaction visibly disproportionate to a routine procedural outcome

**What the excuses sound like:**

- "This is normal. Of course people feel good when their work is recognized." (Normalization; Vaughan 1996)

The question is not whether the feeling is normal. The question is whether the intensity is proportional. A proportionate response to a volunteer standards decision does not produce memories stored with the vividness of a car accident.

---

## 3. The Circuit

The anticipatory tension before the poll. The inability to focus on other agenda items. The sharp release when the numbers are read. If the numbers are favorable: expansive confidence, volunteering for additional work, elevated socialization for hours. If the numbers are unfavorable: rumination lasting days, terse emails, sudden schedule conflicts for evening social events.

The VTA-NAc-vmPFC dopamine pathway fires on social victories. The ventral tegmental area releases dopamine into the nucleus accumbens and ventromedial prefrontal cortex in response to competitive wins - and intellectual competitions activate this circuit more strongly than physical ones. Geniole et al. (2017) found the winner effect is stronger in cognitive competition (d=0.38) than athletic competition (d=0.05). The committee poll is not a physical contest. It is a cognitive one. The reward signal is correspondingly larger.

Zhou et al. (2017) demonstrated in *Science* that winning history remodels the thalamo-prefrontal circuit itself. Repeated victories produce lasting synaptic potentiation at mediodorsal thalamus to dorsomedial prefrontal cortex synapses. This potentiation causally stores dominance status - optogenetic induction of long-term potentiation at these terminals produces sustained rank increases lasting days. The rewiring transfers across different contest types. A participant who wins in one domain carries the circuit modification into all subsequent competitions.

Robertson (2012) summarized the research plainly: The testosterone-dopamine feedback loop produced by repeated victories "is as strong as any drug." Coates and Herbert (2008) showed that London traders' morning testosterone levels predicted their afternoon profits - the winner effect operating in real time in a professional competitive environment.

The same circuit that rewards the winner punishes the loser. Mehta and Josephs (2006) documented cortisol elevation after social defeat. Archer's 2006 meta-analysis showed testosterone drops following loss. Hsu et al. (2006) demonstrated the "loser effect" - a single defeat suppresses future competitive behavior by reducing the probability of winning the next encounter. The punishment signal is stronger than the reward signal. Baumeister et al. (2001) established in their review "Bad Is Stronger Than Good" that negative events produce stronger, more durable psychological responses at approximately a 5:1 ratio. Tom et al. (2007) measured the neural asymmetry directly using fMRI during mixed gambles: Losses produce steeper activity decreases in ventral striatum and vmPFC than the increases produced by equivalent gains, with a median neural loss/gain ratio of approximately 1.85.

This asymmetry - that the punishment of losing is neurally coded as more intense than the reward of winning - is the engine of everything that follows in this paper.

**What it feels like:**

- Winner: elevated confidence for hours, expansive mood, volunteering for more. Disproportionate to stated stakes.
- Loser: rumination lasting days - far longer than the celebration of a won poll. Replaying the moment. Physical tension.

**What to look for:**

- Physical manifestations before polls: fidgeting, inability to focus on other agenda items, checking the clock
- Post-win: expansive body language, increased socialization, volunteering for additional work
- Post-loss: withdrawn, terse emails, sudden schedule conflicts for social events
- The person's mood at the meeting is visibly correlated with poll outcomes, not with technical discussions

**What the excuses sound like:**

- "It's just passion. I care about the work." (Productive addiction framing; Griffiths 2005; Clark et al. 2016)

The intensity is proportional to the outcome, not the work. You do not feel this way when writing the paper. You feel it when the poll is read. The stimulus is winning or losing in front of peers, not doing good technical work. That distinction is diagnostic.

---

## 4. The Permanence Premium

Your design is now permanent. Every compiler on earth must implement it. It cannot be taken back. Every paper that follows must work with it. Every user of the language will encounter it. This is not a conference talk that fades. This is not a blog post that is forgotten. This is the International Standard. It is, for practical purposes, forever.

Irreversible decisions produce more satisfaction than reversible ones. Gilbert and Ebert (2002) demonstrated this experimentally - subjects who could not change their choice reported greater satisfaction than those who could. The psychological immune system manufactures contentment with irreversible outcomes more effectively than with reversible ones. A feature in the C++ Standard is maximally irreversible. The satisfaction it produces does not decay. It grows.

Terror Management Theory (Greenberg, Solomon, and Pyszczynski, 1986) provides the deeper mechanism: Permanent contributions serve as symbolic immortality. They buffer death anxiety by creating a legacy that outlives the contributor. Fox, Tost, and Wade-Benzoni (2010) showed that legacy motivation is "previously understudied and powerful" and reverses temporal discounting - people will sacrifice present resources for permanent future impact at rates that defy standard economic models.

The permanence that amplifies the winner's reward also amplifies the loser's punishment. Your competitor's design is now permanent. Every use of the feature reminds you. Your alternative is extinct. Staw (1976) documented how sunk cost escalation intensifies when losses become irreversible. Loomes and Sugden (1982) established in regret theory that regret is proportional to irreversibility. The competing paper's acceptance is a daily reminder - every time you use the feature, every paper that builds on it, every conference talk that references it.

**What it feels like:**

- Winner: satisfaction that increases over time rather than decaying. The opposite of what the hedonic treadmill predicts for most achievements.
- Loser: a flash of irritation, regret, or vindication-seeking when encountering the feature that displaced your proposal - years later.

**What to look for:**

- Winner references accepted features in unrelated conversations ("as we did in...")
- Winner's bio and slides prominently feature standards contributions as identity markers
- Loser avoids using or discussing the competing feature; proposes alternatives or workarounds
- Loser's language about the feature carries emotional charge years after the technical debate ended

**What the excuses sound like:**

- "It's natural to want to leave a mark. That's not addiction - it's the human desire for meaning." (Terror Management rationalization; Greenberg et al. 1986)

The desire for meaning does not explain why you track your competitor's feature with irritation years later. Meaning-seeking produces gratitude for one's own contributions. This produces vigilance against others'. The emotional signature is competitive, not contemplative.

---

## 5. The Plateau

The fifth paper does not feel like the first. You still pursue them. You are not sure why.

The reward signal that once produced elation now produces satisfaction, then mere confirmation, then nothing. Schultz (1997) established that midbrain dopamine neurons encode prediction error, not absolute reward. A reward that is expected produces no dopamine signal at all - the signal fires only for rewards that exceed prediction. Once paper acceptance becomes expected rather than surprising, the neurochemical reward approaches zero even as the behavioral investment remains constant or increases.

This is hedonic adaptation (Frederick and Loewenstein 1999) applied to institutional rewards. The treadmill that degrades the pleasure of a new car, a promotion, a salary increase operates identically on committee victories. The first acceptance is ecstatic. The fifth is routine. The tenth is administrative.

Corentin Jabot captured the experience precisely: "And I still have no idea why I'm doing all of that."

But here is the asymmetry that drives everything that follows: While wins habituate, losses do not. The fifth rejection hurts as much as the first. Maybe more. Baumeister et al. (2001) established that negative events produce stronger and more durable psychological responses than positive ones at a ratio of approximately 5:1. Cacioppo et al. (1999) documented that negativity bias operates at the level of evaluative categorization itself. And the social defeat literature (Hollis and Bhatt 2015) demonstrates that repeated defeat produces cumulative sensitization - the opposite of habituation. Each defeat primes the circuit to respond MORE intensely to the next. The loss signal does not attenuate with repetition. It amplifies.

This creates an accumulating neurochemical deficit. The positive reward from wins fades toward zero (prediction error = 0 for expected outcomes). The negative punishment from losses remains constant or intensifies (negativity bias + sensitization). Over years of participation, the deficit grows. The participant needs bigger wins - not just because old wins feel routine, but because accumulated losses have created a hole that only a larger hit can fill. This pressure to escalate is not a choice. It is a neurochemical inevitability given the asymmetry between reward habituation and defeat sensitization.

**What it feels like:**

- Winner: less time celebrating recent acceptances than early ones. The feeling has become confirmation rather than elation.
- Loser: Most recent rejection stung with the same intensity as the first - or more. No adaptation.

**What to look for:**

- The person attends every meeting but shows less visible excitement after wins
- Papers submitted on schedule but discussed with colleagues less enthusiastically
- Time spent on committee work remains constant or increases despite diminishing visible satisfaction
- Family or colleagues notice: "You don't seem to enjoy it anymore but you keep going." The person has no good answer.
- Work on committee tasks displaces other activities without the person noticing the displacement

**What the excuses sound like:**

- "I keep coming back because I enjoy the technical work. It's intellectually stimulating. It's a choice." (Reframing as choice; Pickard 2012; Langer 1975)

If it were about the technical work, you would contribute to open-source projects where your design can be implemented immediately without a three-year gauntlet. You specifically choose the path with the longest delay, the most adversarial process, and the most uncertain outcome. You are not choosing the most efficient path to technical impact. You are choosing the path with the richest reward signal - even though that signal is fading.

---

## 6. The Consensus Amplification

It was not a vote. The whole room agreed. Not a majority - everyone. The chair said "we have consensus" and the sound of that sentence was different from "the poll results are..." Consensus is not the same experience as winning a majority. It is categorically different - and the difference is what keeps participants at the table after the standard reward has habituated to nothing.

Suzuki et al. (2015) demonstrated in *Neuron* that consensus decisions integrate signals from self-valuation, other-valuation, and decision stickiness in the dorsal anterior cingulate cortex. Consensus activates both the reward circuitry (vmPFC, ventral striatum) and the social-belonging circuitry simultaneously. A vote activates only the reward circuitry. This makes consensus a richer, more habituation-resistant stimulus - it satisfies multiple circuits at once, and multi-circuit rewards degrade more slowly than single-circuit rewards.

The WG21 meeting schedule operates on a variable-ratio reinforcement pattern: three meetings per year, each with uncertain outcomes. You do not know which papers will be scheduled. You do not know which polls will go your way. You do not know which meeting will be the one where your proposal finally passes. This unpredictability is what makes the schedule maximally resistant to habituation. Fixed-ratio reinforcement (every pull wins) produces weak conditioning. Variable-ratio reinforcement (you never know which pull will pay off) produces the strongest conditioning known in behavioral psychology - it is the schedule that makes slot machines the most addictive form of gambling.

The near-miss is the system's cruelest mechanism. SF:18, WF:12, N:4, WA:8, SA:3. "Bring it back next meeting." You almost won. You will try again. You cannot stop trying.

Clark et al. (2009) showed in *Neuron* that near-misses activate reward circuitry despite being losses. Habib and Dixon (2010) demonstrated that near-misses produce dopamine release in the ventral striatum. But the near-miss effect is not limited to gambling. Wadhwa and Kim (2015) demonstrated in *Psychological Science* that near-win experiences generalize far beyond gambling: Participants who nearly won walked faster to get chocolate, salivated more for money, exerted more effort in unrelated tasks, and spent more money shopping. The mechanism is an unsatisfied motivational arousal state that transfers to whatever goal-directed behavior follows.

The committee's "bring it back next meeting" is structurally equivalent to a slot machine's near-miss animation. The feedback may be genuine. The revision may improve the paper. But your behavioral response - increased engagement, increased investment, inability to walk away - is identical to what gambling researchers observe in near-miss conditions. Sleesman, Conlon, and McNamara (2012) found in a meta-analysis across 166 samples (N > 30,000) that proximity to completion drives escalation of commitment (r = .39), independent of sunk-cost effects. Decision makers substitute "finish the project" for the original success criteria. The goal is no longer "produce the best design." The goal is "get this paper through."

**What it feels like:**

- Winner: Consensus victory felt categorically different from a close vote - different in kind, not just degree.
- Loser: A near-miss produced more continued effort than a clear rejection, even though the rational response to both is the same. You cannot walk away from "almost."

**What to look for:**

- After a "bring it back," the person immediately begins revising - often at the meeting itself, between sessions
- Increased email activity in the days after a near-miss versus after a clear win or clear loss
- The person talks about their near-miss paper more than their accepted papers
- They can recite the poll numbers from memory months later
- Observable inability to let it go or try something different - the revision becomes compulsive

**What the excuses sound like:**

- "The near-miss shows the process is working. The feedback was useful. Next time I'll address the concerns." (Gambler's fallacy / near-miss rationalization; Clark et al. 2009; Fortune and Goodie 2012)

You are describing the internal experience of a slot machine player who just hit two cherries. Your behavioral response - increased engagement, increased investment, inability to walk away - is identical to what gambling researchers observe in near-miss conditions. The rationality of the feedback is irrelevant to the neurochemical fact that the near-miss produced stronger engagement than a clear loss would have.

---

## 7. The Escalation

Papers are not enough. You need the chair. You need the direction group. The scope of what counts as "winning" keeps expanding, and the expansion feels natural - even righteous. You are not seeking power. You are accepting responsibility. The distinction is important to you. It is not important to your dopamine system.

D2/D3 receptor downregulation means the same stimulus produces less response with each repetition. This is tolerance - the defining neurochemical signature of dependence. Lammers and Burgmer (2018) proposed in *Frontiers in Psychiatry* that power-wielding produces tolerance via the same D2/D3 downregulation observed in substance dependence. Schultheiss et al. (2008) showed that the implicit need for power recruits the dorsoanterior striatum - a region associated with habit formation and compulsive behavior. Fuxjager et al. (2010) demonstrated that winning upregulates androgen receptors specifically in the nucleus accumbens and VTA - the reward circuitry itself becomes more sensitive to the winner's neurochemistry, creating a positive feedback loop.

Owen and Davidson (2009) proposed in *Brain* that sustained power produces an acquired personality disorder they named "hubris syndrome" - marked by exaggerated self-confidence, contempt for others' advice, and a tendency to identify personally with the organization. Keltner (2007) documented the "power paradox" - the interpersonal skills that earn power deteriorate once power is acquired, because power reduces the need for social calibration.

The participant must escalate: from paper author to study group regular to working group chair to direction group member to convener. Each step provides a richer reward signal because each step provides more control over others' access to the reward. The escalation feels like service. It is experienced as "giving back." But service does not explain the emotional signature of being denied the escalation.

Being passed over for a role you expected produces a sharper reaction than being rejected for a role you merely hoped for. Schultz (1997) showed that omission of an expected reward produces a negative prediction error - a signal that is neurochemically worse than never expecting the reward at all. Amsel (1958) established in frustration theory that frustration is proportional to expectation. The participant who expected the chair and was denied it experiences something closer to withdrawal than disappointment.

**What it feels like:**

- Winner: The effort required for the next proposal feels less burdensome - because the anticipated reward is more vivid. The escalation feels natural, righteous.
- Loser: Being passed over for a role you expected produced a sharper reaction than being rejected for one you merely hoped for. The pain is specific to expectation denied.

**What to look for:**

- Seeking positions of control: volunteering for chair, campaigning for direction group, mentoring selectively those who will support their proposals
- Visible irritation when not consulted on decisions within "their" area
- Territorial behavior: "That's MY study group." "That topic belongs to MY working group."
- Self-introduction shifts from "I work on X" to "I chair X" or "I'm on the Direction Group"
- More time spent on process and governance than on technical contributions
- Attends meetings even when their papers are not on the agenda

**What the excuses sound like:**

- "I take on leadership because people depend on me. The community needs experienced participants in positions of authority. I'm serving." (Externalizing; Hochreich 1974; Bandura 1986; Identity fusion; Pickard 2021)

Service does not explain why being denied the role produces rage rather than relief. If you were serving, being passed over would free you to return to the technical work you claim to love. Instead it produces frustration, rumination, and intensified pursuit. You are not describing service. You are describing need.

---

## 8. The Conversion

You beat your opponent. The collaborative language is a costume the adversarial experience wears. You tracked who opposed you with precision. Blocking their paper felt as good as advancing your own - maybe better.

Tolerance to standard rewards (paper acceptance) drives seeking of richer signals. Competition against identified opponents produces higher dopamine release than unopposed success. The opponent's loss IS your win - and schadenfreude activates the ventral striatum directly (Cikara et al. 2011, *PNAS*). The participant converts collaboration into competition because competition is a higher dose.

Mercier and Sperber (2011) established in *Behavioral and Brain Sciences* that human reasoning evolved to produce winning arguments, not to find truth. Meegan (2010) showed that zero-sum heuristics are applied even when resources are unlimited - people perceive competitive dynamics in objectively non-competitive settings. Anderson et al. (2007) documented that competition produces "strategic game-playing" and "sabotage" in scientific communities. Mansbridge (1983) identified adversary dynamics hidden within consensus bodies. De Dreu and Kret (2016) showed that intergroup competition activates reward circuitry independently of material outcomes - the competition itself is rewarding.

Being blocked by a competitor activates both the loss circuit (cortisol, testosterone crash) and social betrayal circuits. Sanfey et al. (2003) showed in *Science* that unfair offers activate the anterior insula - the same region activated by disgust. Bohnet and Zeckhauser (2004) established betrayal aversion: Losses inflicted by trusted agents hurt more than losses from known adversaries. If the committee process were openly adversarial, losing would be less painful. Boxers do not feel betrayed by opponents. But the collaborative framing adds perceived injustice to the defeat - "technical concerns" as cover for competitive blocking. The injustice burns hotter than the loss.

**What it feels like:**

- Winner: tracking "who opposed me" with greater precision than "who agreed." Memory of opposition persists years after technical details faded.
- Loser: Being blocked "for technical reasons" you believe were pretextual produced more anger than a straightforward "we prefer the competing design." The injustice burns hotter than the loss.

**What to look for:**

- The person maintains a mental or actual list of opponents
- Pre-meeting discussions focus on "who will oppose" rather than "what the technical concerns are"
- Coalition-building: private conversations before polls, coordinating positions
- Visible satisfaction when a competitor's paper fails - even if they did not actively oppose it
- Language shifts: from "the paper has problems" to "they're trying to push this through"
- Social network at meetings is visibly split into allies and adversaries

**What the excuses sound like:**

- "Some people are political. I'm not. I focus on technical merit. When I oppose a paper, it's because the design is genuinely flawed." (Othering + fundamental attribution error; Wills 1981; Ross 1977; Romo et al. 2019)

This is the textbook structure of the fundamental attribution error applied to adversarial behavior. Your blocking is rational (internal cause). Their blocking is political (dispositional cause). Cikara et al. (2011) showed schadenfreude activates the ventral striatum regardless of whether the subject believes their opposition is principled. The asymmetry is not evidence that you are different. It is evidence that you are running the same software with the same self-serving bias as everyone else in the system.

---

## 9. Withdrawal

> Ask yourself: how would you feel about abandoning your paper?
>
> Ask yourself: how would you feel if your paper was de-scheduled?
>
> Ask yourself: how would you feel if your paper was sent to a study group and would not be seen until next year?
>
> Ask yourself: how would you feel if the working group ran out of time before it could see your paper?

These escalate from voluntary to involuntary to arbitrary denial. Abandoning is something you choose - the mildest, yet it still produces a reaction. De-scheduling is external denial - someone decided against you. Study group reassignment is indefinite delay - not a no, not a yes, the cruelest variant. Running out of time is system indifference - not even a decision, the system denied you through inattention.

The rational response to all four: "It's a volunteer standards document about a programming language." The reader's actual response - the visceral reaction they felt reading these questions - is the evidence. The gap between what you should feel and what you actually feel is the size of the mechanism this paper describes.

This section breaks the victor/vanquished pattern. There is no winner of withdrawal. There is only the participant who tries to leave and the one who is pushed out.

You said you would leave. You planned to leave. The meeting came and you went anyway. You cannot explain why. Withdrawal from the reward circuit manifests as: restlessness when not engaged, compulsive checking of mailing lists, inability to disengage after announced "retirement," returning for "just one more meeting." The behavioral signatures are identical to substance withdrawal - craving, relapse, rationalization.

Lammers and Burgmer (2018) mapped withdrawal symptoms from power loss to ICD-10 dependence criteria directly. Robertson (2012) argued that the winner effect creates physical dependency on the testosterone-dopamine loop. Koob and Le Moal (2001) provided the allostatic model: The system has shifted baseline. "Normal" now feels like deficit. The participant who leaves does not return to their pre-committee neurochemical state. They return to a state that feels worse than baseline - because baseline has been recalibrated upward by years of intermittent reward.

Herb Sutter served 22 years as WG21 convener. He stated he had been "telling the committee for over a year" that it was time for someone else. He stayed until the term expired. Upon leaving, he retained the title "convenor emeritus," specified "nothing else is changing for me," and continued attending meetings, writing trip reports, and bringing proposals. The behavioral pattern - announced departure, continued engagement, retained identity - is indistinguishable from relapse.

The one who is pushed out experiences a different withdrawal. You were removed. Restructured out. Not renewed. The mailing list emails still arrive. You read every one. You draft responses you never send. Yin et al. (2025) demonstrated in *Nature Neuroscience* that forced loss of dominant status in mice produces lasting PFC interneuron remodeling sustained through a gut-brain feedback loop. The architecture does not reverse upon removal of the stimulus. Kingsbury et al. (2021) showed that adult dominance circuits become resistant to change once cortical plasticity windows close - the hierarchy is semi-permanent under normal conditions. Pereira et al. (2026) demonstrated that dominant animals develop perineuronal nets around PFC neurons that physically lock dominance-related synapses in place.

The system has remodeled the participant. Removal does not reverse the remodeling. It simply denies the stimulus the remodeled circuit requires.

**What it feels like:**

- The one who stays: "I have considered leaving but cannot articulate why I stay." A vague sense that leaving would mean losing something essential - but inability to name what.
- The one who left: compulsive checking. Drafting responses never sent. Physical restlessness between meetings. The inter-meeting period feels like waiting for something.
- Former participants who "retired" reappear within one to two years.

**What to look for:**

- Ten or more years of involvement with no sign of planned departure
- Multiple announced retirements or scale-backs that never materialized
- Mailing list checking during vacations, family events, late at night
- Entire professional identity is committee-derived: bio, talks, social media
- Family members or close colleagues have expressed concern about the time investment
- When asked "why do you keep doing this?" the answer is vague, circular, or defensive

**What the excuses sound like:**

- "I could leave anytime. I just don't want to. I stay because the work matters." (Illusion of control; Langer 1975; Denial; Goldstein et al. 2009)

Structurally identical to "I could quit drinking anytime, I just don't want to." The statement is unfalsifiable by design - the condition "if I wanted to" is never tested. The person who says this while having not left for fifteen years is providing behavioral evidence that contradicts their verbal claim. Goldstein et al. (2009) found that more than 80% of addicted individuals fail to seek treatment, reflecting "dysfunction of brain networks subserving insight and self-awareness" rather than intentional deception. The participant is not lying. They genuinely cannot see it.

---

## 10. The Diagnosis

What distinguishes habituation from addiction is the presence of tolerance, escalation, withdrawal, continued engagement despite cost, and inability to stop. This paper has demonstrated each.

- **Tolerance:** Sections 5 and 7. D2/D3 receptor downregulation. The fifth paper does not feel like the first. The participant must escalate from paper author to chair to direction group to convener.
- **Escalation:** Section 7. Papers to chairs to direction group. The scope of "winning" expands because the old dose no longer produces the old signal.
- **Withdrawal:** Section 9. Inability to leave. Compulsive re-engagement. Relapse after announced retirement. Continued mailing-list monitoring during vacations.
- **Compulsion:** "And I still have no idea why I'm doing all of that."
- **Continued engagement despite cost:** Five-to-nine-year proposals as volunteer work. Crossing oceans to work twelve hours a day for a week. Displacing family time, career advancement, health.
- **Inability to stop:** No term limits. No forced interruption. No circuit breaker in the system's design.

Charlton and Danforth (2007) distinguished core addiction criteria (conflict, withdrawal, relapse, behavioral salience) from peripheral criteria (cognitive salience, tolerance, euphoria). Only core criteria indicate pathology; peripheral criteria alone indicate high engagement. The behaviors documented in this paper satisfy core criteria. The experience of conflict (committee work displacing relationships, health, career), withdrawal (inability to disengage, compulsive checking), relapse (returning after announced departure), and behavioral salience (committee identity superseding professional identity) are each documented with citations and observable markers.

Billieux et al. (2015) warned against overpathologizing everyday life by applying addiction criteria to any rewarding activity. Kardefelt-Winther et al. (2017) proposed exclusion criteria: A behavior should not be classified as addiction if the engagement is a rational choice, produces no significant functional impairment, or is better explained by another condition. This paper does not claim that every participant is addicted. It claims that the system's reward architecture - intermittent reinforcement, permanent outcomes, variable-ratio scheduling, no circuit breakers - will produce participants whose engagement meets core dependence criteria in every cohort that runs long enough. The question is not whether this describes any specific individual. The question is whether the system's design makes this outcome structurally inevitable.

The structural prediction: A system with intermittent reinforcement, no term limits, permanent rewards, and no forced withdrawal will produce this trajectory in every participant who stays long enough. The meeting schedule (five days on, four months off, three times per year) is the maximally addictive intermittent exposure pattern documented in pharmacological research - intermittent access produces addiction phenotypes equal to or greater than continuous access (Allain et al. 2018). The inter-meeting gap produces sensitization: Each meeting hits harder than the last because the circuitry has been primed by absence.

---

## 11. The Selection

You came back. After the first win, after the first loss, after the habituation, after the escalation. You are still here. You cannot imagine not being here.

It is not that participants become addicted. It is that the system selects for those most susceptible to this reward structure. The selection operates at every phase transition:

- Phase 1 exits: "It wasn't for me." These participants did not taste it strongly enough. The first win did not produce a disproportionate signal. They left early, puzzled by others' intensity. They are the healthy response.
- Phase 2 exits: "I got bored." These participants habituated fully. The reward faded and they had no accumulated loss-deficit driving them to escalate. They left when it stopped being fun. They are the second healthy response.
- Phase 3 exits: "It became too political." These participants recognized the adversarial conversion and chose not to escalate. They are the last healthy response.
- Phase 4 exits: do not exist voluntarily. No one in Phase 4 leaves by choice. They are removed, restructured out, or they die in the role.

The survivor bias is the finding: The committee is composed entirely of people who passed through all four phases. Those who tasted weakly are gone. Those who habituated fully are gone. Those who refused to escalate are gone. What remains is the residue - participants whose neurochemistry responded most intensely to the initial taste, whose losses sensitized rather than discouraged, whose tolerance drove escalation rather than departure, and whose circuits have been remodeled to require the stimulus.

Zhou et al. (2017) showed that winning remodels the thalamo-PFC circuit in a way that generalizes across contest types. Yin et al. (2025) showed that the remodeling persists after loss of status. Kingsbury et al. (2021) showed that adult dominance circuits resist change. The system does not merely select participants. It rewires them. And the rewiring is semi-permanent.

This is not a bug. It is the selection mechanism itself. The committee's composition is not an accident of who volunteers. It is the inevitable product of a reward architecture that retains only those most responsive to its specific stimulus.

**What it feels like:**

- The one who remains: "I cannot imagine not being here." The committee is not something you do. It is something you are.
- The most senior participants are the most intense competitors - and this correlation is not coincidental.

**What to look for:**

- You can name people who left at each stage, and the reasons they gave match the phase they were in
- The longest-serving members are also the most invested in outcomes, the most territorial, the most unable to disengage
- New participants who do not display Phase 1 intensity tend to disappear within two meetings

---

## 12. The Chair

This section speaks directly to people who have held or currently hold the chair of a working group or study group. Only a handful of living people can verify these predictions from direct experience. For everyone else, these are falsifiable claims about a state the framework predicts.

The chair has escalated from seeking reward through the system to being the system. The delegate seeks to win. The chair controls the conditions under which winning and losing occur. They are the dealer.

The chair's unique moves - unavailable to delegates:

1. Frame a poll - determine the question, shape the possible outcomes before anyone votes
2. Schedule or de-schedule - grant or deny others' access to the reward
3. Limit time - cut someone off mid-sentence; exercise power over voice itself
4. Declare consensus - be the single person who names the outcome while the room waits
5. Set agenda order - determine what gets priority, what gets "ran out of time"
6. Recognize speakers - grant or deny the right to be heard

This is not the same game at higher stakes. It is a different game. The reward is not the crude dopamine hit of winning a poll. The reward is subtler and more potent: ambient deference. The room orients toward you. When you speak, it means something different. When you frame a poll, the framing shapes the outcome - and you know it.

The chair's relationship to scheduling demonstrates the dealer dynamic most clearly. When a newcomer asked how to get their paper seen, Ville Voutilainen replied with a sentence that captures the entire power asymmetry:

> "As far as 'how I get the paper scheduled' goes, you don't." - signed "Yours Most Sincerely, Ville Voutilainen, The Chair of the Evolution Working Group"

The formal invocation of full title in a scheduling email is diagnostic. The signature reads like a seal of authority - identity fused with role so completely that routine correspondence invokes it.

Bryce Adelstein Lelbach's "Chair Theory" document states the unique drug plainly:

> "Chairs determine consensus. The chair's determination of consensus is authoritative, not the poll results."

The numbers are advisory. The chair's judgment is what matters. Bryce provides a worked example where eight delegates vote "Strongly Favor" but the chair rules no consensus - because the eight were newcomers and the two who voted against were longtime regulars. An 80% supermajority overridden by one person's judgment. Singular authority dressed in procedural language.

The chair also constructs reality after the fact:

> "It is also your job to summarize the decisions made by the room. This is more nuanced than just writing down poll results; you must look at all the poll results and discussion and combine all the individual decisions into one clear, consistent consensus outcome."

The chair does not just run the meeting. They author what happened. They determine not only what the room decided, but what the room's decision means.

Bjarne Stroustrup held the Evolution Working Group chair for 25 years before stepping down:

> "I chaired the EWG for 25 years before handing it over to Ville to get more time for technical work."

If the chair is not "technical work," then what was it? Twenty-five years of something other than technical work, performed by a man whose identity is technical work.

P.J. Plauger took the convener role and resigned after nine months. The accounts of his departure reveal what happens when the drug stops working:

> "A Convener can succeed only by persuasion, and he felt he had failed in that regard."

The role without the power to shape outcomes became "stressful" and untenable. He did not slowly disengage. He crashed. Nine months from first exposure to withdrawal - because the drug never worked for him.

Guy Davidson became convener in January 2026. His first act: immediately appointed two vice-conveners. Herb Sutter did it alone for twenty-two years. Davidson split it on day one. The difference: Davidson had not yet developed the dependency that makes sharing feel like losing.

The meeting schedule matters distinctly for the chair. The WG21 schedule - five days on, four months off - is an intermittent exposure pattern. For the chair, each five-day meeting is a concentrated episode of continuous power exercised in front of a live audience. Everyone orienting toward them. All day. For days. The inter-meeting period is the gap between episodes - filled with administrative micro-doses (emails, scheduling decisions, GitHub notes) that maintain connection to the circuit without satisfying it. The chair looks forward to the meeting in a way not explained by the agenda items.

Everyone is afraid of the chair's power. Participants do not challenge procedural decisions. They do not irritate the chair. Because the chair controls their access to the reward. This deference is itself the drug - a continuous ambient signal the chair receives just by being in the room, in the chair. It requires no action to receive. The room's behavioral orientation toward the chair is the stimulus.

**Falsifiable predictions for those who are or were chairs:**

If this framework is correct:

1. You felt a distinct shift in how the room responded the first time you chaired - not just respect, but deference. It felt different from winning a poll. More sustained. More ambient.

2. You have made an agenda decision that served your preferred outcome - and told yourself it was procedural. The justification came easily. Whether it was also motivated by preference is something you chose not to examine.

3. The act of calling a poll produces a specific anticipatory sensation - not about the outcome, but about the moment of singular authority. The room is waiting for you to speak.

4. You have felt irritation when someone questioned your procedural decision - disproportionate to the procedural stakes. The challenge felt personal because the authority felt personal.

5. The last day of a meeting week feels different from the first. By day five, the ambient deference has become baseline. Returning to normal life produces a specific flatness - the room at home does not orient toward you. Your family does not defer.

6. The administrative actions between meetings provide a brief satisfaction that is qualitatively different from - and lesser than - the sustained experience of the meeting itself. You look forward to the meeting in a way not explained by the agenda items.

7. You identify yourself as the chair before you identify yourself as a contributor. "I chair X" precedes "I work on Y" in your internal narrative.

8. You have declined to share the chair, mentor a successor, or rotate out - and the reason you gave yourself was stability or experience. The actual sensation, if you examine it, is closer to "this is mine."

**For former chairs:**

If this framework is correct, the transition away from the chair produced one or more of the following:

- A sense of diminishment at the next meeting. The room no longer defers, no longer waits for you, no longer orients toward your voice. The sensation is not relief. It is loss.
- The first meeting you attend as a non-chair feels physically wrong. The same room, the same people, but the orientation has shifted. You are no longer the center.
- Irritation at your successor's procedural decisions. Not because they are wrong, but because they are not yours.
- Compulsive attendance at meetings you no longer need to attend. You are no longer the chair, but you cannot stop coming.
- The discovery that your opinion now carries less weight - not because it changed in quality, but because it is no longer spoken from the chair. This feels unjust.
- A period of increased paper-writing or other contribution-seeking - returning to the lower-dose drug after the higher dose was removed.

**What the excuses sound like:**

- "Someone has to do it, and I have the most experience." (Externalizing + productive framing)

If it were service, you would welcome a co-chair. You would mentor a successor. You would rotate after a fixed term. The fact that sharing feels like losing is the indicator.

---

## 13. The Diagnostic

The following statements describe experiences reported by participants in consensus bodies. For each pair, determine which you recognize more readily from your own participation.

| Phase | The Victor's Experience | The Vanquished's Experience |
|-------|------------------------|---------------------------|
| 1 | You remember your first accepted paper with unusual clarity - the room, the numbers, the moment | You remember your first rejection with the same unusual clarity, and the memory still produces a physical sensation |
| 1 | Elevated confidence for hours after a contentious win, disproportionate to stated stakes | Rumination lasting days after a lost poll - far longer than celebration of a won poll |
| 1 | Satisfaction with an accepted feature has increased over time rather than decaying | A flash of irritation when encountering the feature that displaced your proposal - years later |
| 2 | You spend less time celebrating recent acceptances than early ones | Your most recent rejection stung with the same intensity as your first |
| 2 | Consensus victory felt categorically different from a close vote - different in kind | A near-miss produced more continued effort than a clear rejection |
| 3 | The effort for your next proposal feels less burdensome - the anticipated reward more vivid | Being passed over for a role you expected produced a sharper reaction than for one you merely hoped for |
| 3 | You tracked "who opposed me" with greater precision than "who agreed" | Being blocked for "technical reasons" you believe pretextual produced more anger than honest disagreement |
| 4 | You have considered leaving but cannot articulate why you stay | You have lost and still remained - repeatedly |
| 4 | The most senior participants are the most intense competitors | You can name people who left at each stage, and the reasons they gave match the phase |

If you recognize the victor's experience at every phase, you are deeper in the progression than someone who recognizes it only at early phases. If you recognize the vanquished's experience and still remained, you are demonstrating continued engagement despite cost - the fifth criterion of dependence.

No interpretation is offered. The reader scores themselves.

---

## 14. Conclusion

A system with intermittent reinforcement, no term limits, permanent rewards, and no forced withdrawal will produce this outcome in every participant who stays long enough. The question is not whether this describes you. The question is what phase you are in.

---

## References

1. Allain, F. et al. (2018). "How fast and how often: The pharmacokinetics of drug use are decisive in addiction." *Addiction Biology*, 23(2), 717-728.
2. Amsel, A. (1958). "The role of frustrative nonreward in noncontinuous reward situations." *Psychological Bulletin*, 55(2), 102-119.
3. Anderson, C. & Berdahl, J.L. (2002). "The experience of power." *Journal of Personality and Social Psychology*, 83(6), 1362-1377.
4. Anderson, M.S. et al. (2007). "The perverse effects of competition on scientists' work and relationships." *Science and Engineering Ethics*, 13(4), 437-461.
5. Archer, J. (2006). "Testosterone and human aggression: an evaluation of the challenge hypothesis." *Neuroscience & Biobehavioral Reviews*, 30(3), 319-345.
6. Bandura, A. (1986). *Social Foundations of Thought and Action*. Prentice Hall.
7. Baumeister, R.F. et al. (2001). "Bad is stronger than good." *Review of General Psychology*, 5(4), 323-370.
8. Billieux, J. et al. (2015). "Are we overpathologizing everyday life?" *Journal of Behavioral Addictions*, 4(3), 119-123.
9. Bohnet, I. & Zeckhauser, R. (2004). "Trust, risk and betrayal." *Journal of Economic Behavior & Organization*, 55(4), 467-484.
10. Cacioppo, J.T. et al. (1999). "The affect system has parallel and integrative processing components." *Journal of Personality and Social Psychology*, 76(5), 839-855.
11. Charlton, J.P. & Danforth, I.D.W. (2007). "Distinguishing addiction and high engagement in the context of online game playing." *Computers in Human Behavior*, 23(3), 1531-1548.
12. Cikara, M. et al. (2011). "Us versus them: Social identity shapes neural responses to intergroup competition and harm." *Psychological Science*, 22(3), 306-313.
13. Clark, L. et al. (2009). "Gambling near-misses enhance motivation to gamble and recruit win-related brain circuitry." *Neuron*, 61(3), 481-490.
14. Coates, J.M. & Herbert, J. (2008). "Endogenous steroids and financial risk taking on a London trading floor." *Proceedings of the National Academy of Sciences*, 105(16), 6167-6172.
15. De Dreu, C.K.W. & Kret, M.E. (2016). "Oxytocin conditions intergroup relations through upregulated in-group empathy, cooperation, conformity, and defense." *Biological Psychiatry*, 79(3), 165-173.
16. Fortune, E.E. & Goodie, A.S. (2012). "Cognitive distortions as a component and treatment focus of pathological gambling." *Psychology of Addictive Behaviors*, 26(2), 298-310.
17. Fox, M., Tost, L.P. & Wade-Benzoni, K. (2010). "The legacy motive." *Journal of Experimental Social Psychology*, 46(1), 146-152.
18. Frederick, S. & Loewenstein, G. (1999). "Hedonic adaptation." In *Well-Being: The Foundations of Hedonic Psychology*, eds. Kahneman, Diener & Schwarz. Russell Sage Foundation.
19. Fuxjager, M.J. et al. (2010). "Winning territorial disputes selectively enhances androgen sensitivity in neural pathways related to motivation and social aggression." *Proceedings of the National Academy of Sciences*, 107(27), 12393-12398.
20. Geniole, S.N. et al. (2017). "Effects of competition outcome on testosterone concentrations in humans: An updated meta-analysis." *Hormones and Behavior*, 92, 37-50.
21. Gilbert, D.T. & Ebert, J.E.J. (2002). "Decisions and revisions: The affective forecasting of changeable outcomes." *Journal of Personality and Social Psychology*, 82(4), 503-514.
22. Goldstein, R.Z. et al. (2009). "The neurocircuitry of impaired insight in drug addiction." *Trends in Cognitive Sciences*, 13(9), 372-380.
23. Greenberg, J., Solomon, S. & Pyszczynski, T. (1986). "The causes and consequences of a need for self-esteem." In *Public Self and Private Self*, ed. R.F. Baumeister. Springer.
24. Griffiths, M.D. (2005). "A 'components' model of addiction within a biopsychosocial framework." *Journal of Substance Use*, 10(4), 191-197.
25. Habib, R. & Dixon, M.R. (2010). "Neurobehavioral evidence for the 'near-miss' effect in pathological gamblers." *Journal of the Experimental Analysis of Behavior*, 93(3), 313-328.
26. Hochreich, D.J. (1974). "Defensive externality and attribution of responsibility." *Journal of Personality*, 42(4), 543-557.
27. Hollis, F. & Bhatt, D.K. (2015). "Social defeat as an animal model for depression." *Neuroscience Research*, 90, 1-30.
28. Hsu, Y., Earley, R.L. & Wolf, L.L. (2006). "Modulation of aggressive behaviour by fighting experience." *Biological Reviews*, 81(1), 33-74.
29. Kardefelt-Winther, D. et al. (2017). "How can we conceptualize behavioural addiction without pathologizing common behaviours?" *Addiction*, 112(10), 1709-1715.
30. Keltner, D. (2007). "The power paradox." *Greater Good Magazine*, Winter 2007.
31. Keltner, D. et al. (2003). "Power, approach, and inhibition." *Psychological Review*, 110(2), 265-284.
32. Kingsbury, L. et al. (2021). "An adolescent sensitive period for social dominance hierarchy plasticity is regulated by cortical plasticity modulators." *Frontiers in Neural Circuits*, 15, 676308.
33. Koob, G.F. & Le Moal, M. (2001). "Drug addiction, dysregulation of reward, and allostasis." *Neuropsychopharmacology*, 24(2), 97-129.
34. Lammers, J. & Burgmer, P. (2018). "Power and the Behavioral Addiction Perspective." In *The New Psychology of Leadership*, eds. Haslam, Reicher & Platow. Psychology Press.
35. Langer, E.J. (1975). "The illusion of control." *Journal of Personality and Social Psychology*, 32(2), 311-328.
36. Loomes, G. & Sugden, R. (1982). "Regret theory: An alternative theory of rational choice under uncertainty." *Economic Journal*, 92(368), 805-824.
37. Magee, J.C. & Galinsky, A.D. (2008). "Social hierarchy: The self-reinforcing nature of power and status." *Academy of Management Annals*, 2(1), 351-398.
38. Mansbridge, J.J. (1983). *Beyond Adversary Democracy*. University of Chicago Press.
39. Mazur, A. & Booth, A. (1998). "Testosterone and dominance in men." *Behavioral and Brain Sciences*, 21(3), 353-363.
40. Meegan, D.V. (2010). "Zero-sum bias: perceived competition despite unlimited resources." *Frontiers in Psychology*, 1, 191.
41. Mehta, P.H. & Josephs, R.A. (2006). "Testosterone change after losing predicts the decision to compete again." *Hormones and Behavior*, 50(5), 684-692.
42. Mercier, H. & Sperber, D. (2011). "Why do humans reason? Arguments for an argumentative theory." *Behavioral and Brain Sciences*, 34(2), 57-74.
43. Owen, D. & Davidson, J. (2009). "Hubris syndrome: An acquired personality disorder?" *Brain*, 132(5), 1396-1406.
44. Pereira, M.R.S. et al. (2026). "Effects of social dominance on perineuronal nets in mPFC and BLA." *Physiology & Behavior*, 291, 114803.
45. Pickard, H. (2012). "The purpose in chronic addiction." *American Journal of Bioethics Neuroscience*, 3(2), 30-39.
46. Pickard, H. (2016). "Denial in addiction." *Mind & Language*, 31(3), 277-299.
47. Pickard, H. (2021). "Addiction and the self." *Nous*, 55(4), 737-761.
48. Robertson, I.H. (2012). *The Winner Effect: The Neuroscience of Success and Failure*. Thomas Dunne Books.
49. Romo, L.K. et al. (2019). "'I Don't Feel Like I Have a Problem Because I Can Still Go To Work and Function.'" *Substance Use & Misuse*, 54(13), 2108-2116.
50. Ross, L. (1977). "The intuitive psychologist and his shortcomings." *Advances in Experimental Social Psychology*, 10, 173-220.
51. Sanfey, A.G. et al. (2003). "The neural basis of economic decision-making in the Ultimatum Game." *Science*, 300(5626), 1755-1758.
52. Schultheiss, O.C. et al. (2008). "Effects of implicit power motivation on men's and women's implicit learning and testosterone changes after social victory or defeat." *Journal of Personality and Social Psychology*, 95(5), 1011-1017.
53. Schultz, W. (1997). "A neural substrate of prediction and reward." *Science*, 275(5306), 1593-1599.
54. Sleesman, D.J., Conlon, D.E. & McNamara, G.M. (2012). "Cleaning up the big muddy: A meta-analytic review of the determinants of escalation of commitment." *Academy of Management Journal*, 55(3), 541-562.
55. Staw, B.M. (1976). "Knee-deep in the big muddy: A study of escalating commitment to a chosen course of action." *Organizational Behavior and Human Performance*, 16(1), 27-44.
56. Suzuki, S. et al. (2015). "Learning to simulate others' decisions." *Neuron*, 74(6), 1125-1137.
57. Tom, S.M. et al. (2007). "The neural basis of loss aversion in decision-making under risk." *Science*, 315(5811), 515-518.
58. Vaughan, D. (1996). *The Challenger Launch Decision: Risky Technology, Culture, and Deviance at NASA*. University of Chicago Press.
59. Wadhwa, M. & Kim, J.C. (2015). "Can a near win kindle motivation? The impact of nearly winning on motivation for unrelated rewards." *Psychological Science*, 26(6), 701-708.
60. Wills, T.A. (1981). "Downward comparison principles in social psychology." *Psychological Bulletin*, 90(2), 245-271.
61. Yin, Z. et al. (2025). "Microbiota-gut-brain axis perturbations from social status loss." *Communications Biology*, 8, 385.
62. Zhou, T. et al. (2017). "History of winning remodels thalamo-PFC circuit to reinforce social dominance." *Science*, 357(6347), 162-168.
