# Concept Manifest - A Young Delegate's Notebook

Binding contract for every writing agent. Read this before drafting any chapter.

## How to use this manifest

- Each chapter OWNS the terms listed under it. A term is defined once (italicized where it's defined, in plain language) in its owning section.
- Never use a term formally before its owning section. If you need a concept owned by a later chapter, paraphrase it in plain words and do not claim the formal definition.
- When you use a term first defined in an earlier chapter, restate its meaning in a short parenthetical on first use in your chapter.
- Section numbers are decimal. Chapter headings are `## N. Title`, sections `### N.M Title`, subsections `#### N.M.K Title`. Headings carry the number, no section symbol. In prose, write "section 5.2" in lowercase. The (§N.M) owner labels in this file are planning shorthand and never appear in the book.

## The anatomy bridge (important)

The chapter order introduces papers (Ch 3) and remote participation (Ch 4) before the full structural map (Ch 5). To avoid forward references, Chapter 2 introduces the committee's basic anatomy at a shallow level: WG21, National Body, convener, plenary, subgroup. Chapter 5 owns the deep structural treatment (the specific rooms, study groups, the Direction Group, chair power) and restates each shared term with a parenthetical. Writers in Ch 3-4 use only the shallow Ch 2 meanings.

## Cross-cutting psychological awareness

Woven in, never its own topic, never jargon. Advice TO the reader about their own judgment. Placed in: Ch 1 (responsibility, not a game), Ch 6 (realistic expectations), Ch 7 (don't get addicted; stay skeptical), Ch 8 (consensus is social pressure; demand evidence), Ch 9 (evidence over enthusiasm), Ch 11 (burnout; boundaries), Ch 13 (participation is not impact).

---

## Chapter 1 - The C++ Standard

Arc: enters curious about "what is this thing," leaves feeling the weight and seriousness of it.

Subheading order:
- 1.1 Standardization Is a Responsibility (not a hobby, resume item, or game)
- 1.2 The Delegate's Oath (told as delegate lore; the pull of your employer, in plain words, with no national-body talk yet)
- 1.3 Every Feature Is Forever (the standard almost never shrinks, removal is rare and slow, and a dropped feature lives on in compilers and code - std::regex can't be fixed because a faster version would break programs already compiled, with no ABI term yet)
- 1.4 The People Who Inherit Your Work (more than sixteen million developers per SlashData's 2025 estimate, linked as "one recent estimate" - every compiler team is expected to build and maintain every feature - small is not free)
- 1.5 The Standard Is Not the Language (three things: the standard as a document, the compilers that try to follow it, and the living language, the code already out there)
- 1.6 The Forms the Standard Takes (the working draft - IS, TS, white paper, TR - no level-4 subsections - C++26 finished technical work in March 2026, and member countries must approve a version's final text in a vote before ISO publishes it - a TS may never enter the standard)
- 1.7 How to Read the Standard (clauses, normative text vs notes, stable section labels)
- 1.8 From Standard to Compiler (the path to implementation; the three implementers)

Owns:
- **the standard** (§1.5) - the official ISO document that defines what C++ means; not the compilers, not the code people write.
- **the living language** (§1.5) - C++ as it's used in all the code already out there, which leans on compiler quirks and extensions and doesn't change when the standard does.
- **the Delegate's Oath** (§1.2) - the vow: do what's best for the language, make no unnecessary proposals, put users first.
- **the working draft** (§1.6) - the living, in-progress text that becomes the next official version of C++.
- **International Standard (IS)** (§1.6) - the finished, published version of C++, like C++23; the binding standard.
- **Technical Specification (TS)** (§1.6) - an optional, experimental document for trying a feature before it enters the standard. A TS may never enter the standard.
- **white paper** (§1.6) - a lighter twin of the TS with far less ISO paperwork, recommended by ISO and SC22 since 2023. In ch 1 it is described in plain words ("the standards bodies") and the source is linked as "the committee's practices guide" (SD-4, defined formally in Ch 3).
- **Technical Report (TR)** (§1.6) - an older informational document type, now mostly replaced by the TS and the white paper.
- **normative text** (§1.7) - the parts that state real requirements, as opposed to notes and examples.
- **stable section labels** (§1.7) - bracketed names like [container.requirements] that stay fixed across drafts, unlike section numbers.
- **the three implementers** (§1.8) - GCC, Clang, and MSVC, the three main compiler teams who turn the standard into something usable.

Prerequisites: none (first chapter). Says "the committee" plainly (from the intro) and never names WG21.
Links: cppreference (std::regex, C++23), eel.is/c++draft, github.com/cplusplus/draft, SlashData's 2025 developer report, Herb Sutter's March 2026 trip report (the C++26 status), SD-4 (as "the committee's own practices guide"), GCC, Clang, and MSVC. Defer the formal wg21.link explanation to Ch 3. Defer "feature-test macro" to Ch 9.

---

## Chapter 2 - Meet the Committee

Arc: enters intimidated ("can I even join?"), leaves seeing the way in wide open.

Subheading order (as written):
- 2.1 You Don't Need Permission (the gates are lower than the rumors say and their rules are posted, and non-technical help is valued - the June 2026 Brno meeting had twenty-five first-time guests)
- 2.2 The Nesting: ISO, JTC1, SC22, WG21 (on paper WG21 only recommends, and the bodies above it run the official vote)
- 2.3 How the Committee Meets (plenary and subgroups, anatomy bridge, the June 2026 Brno meeting: about two hundred people from twenty-eight nations, a little over half in the room and the rest online)
- 2.4 What a National Body Is (the national body appoints the experts; its mirror committee is the group you actually join, decides who represents the country and what it thinks of a draft; inside WG21 experts vote as individuals at plenary; one country, one vote only on the formal ballots)
- 2.5 The Easiest Start: Attending as a Guest (email the convener and name the country where you live or work - ISO strongly encourages at least a week's notice - a guest does almost everything but vote at plenary - guest status covers the first meeting only, then you need a seat through a national body)
- 2.6 Getting Further In: Finding a Seat (Start at home. Join your country's mirror committee by emailing the national body chairs via the isocpp.org meetings page. Say you want C++, since some national bodies run one committee for every language. Rules and fees vary and some charge nothing. With no mirror committee, INCITS is open to anyone, individuals included, so you needn't be American. Starting a mirror committee takes about a year, so get a seat first. The INCITS fee is per committee, 2026 cycle $2,703 full rate, $1,530 small companies, $510 academics. The Beman Project offers free seats under its INCITS membership as an alternate, a backup to Beman's main representative, and the text leaves the alternate's vote unclaimed. Travel is on you. Before you join, check who holds the seat: you in some countries, whoever pays the fee in the United States, so a seat your employer pays for may not follow you to your next job. Author's call: the Beman Project is the only sponsor named, do not mention the C++ Alliance or the Boost Foundation)
- 2.7 Getting a Vote: The ISO Global Directory (accredited means your name sits in the global directory, which your national body puts it in - the trap is that a seat that gets you into the rooms doesn't always put your name on the roster, so a regular can stay unlisted, so ask your national body to list you and check that it did - a guest needs a week's notice, a vote needs months - a seat asks two things, read the proposals before you vote and stay active in your mirror committee - you vote as yourself, but you're there on your national body's word)
- 2.8 The Roles You Can Play (note-taker, also called the scribe, a clear way to be useful on day one - reviewer, author, implementer, champion - the first two need no membership)
- 2.9 Your First Day: Orientation and Introductions (6 p.m. Sunday newcomer orientation, usually in the main hotel's lobby - when the week opens, first-time attendees introduce themselves to the whole committee, brief and friendly, not a test)
- 2.10 Showing Up Is the Secret (eighty percent of success is showing up)
- 2.11 Conferences: Meeting the Committee Off Duty (members go to conferences, so you can meet them before your first meeting - ideas start with everyday problems - C++Now is small and expert-heavy, each spring in Aspen, Colorado, and CppCon is where ideas meet the wider community - ACCU, Meeting C++, and the isocpp.org worldwide conference list)

Owns:
- **ISO** (§2.2) - the International Organization for Standardization, the global body that publishes technical standards.
- **IEC** (§2.2) - the International Electrotechnical Commission, ISO's sister body; the two run information technology together, hence ISO/IEC.
- **JTC1** (§2.2) - the joint ISO/IEC committee for information technology.
- **SC22** (§2.2) - the subcommittee under JTC1 for programming languages.
- **WG21** (§2.2) - Working Group 21, the group inside SC22 that writes the C++ standard (formal nesting; used plainly before this).
- **subgroup** (§2.3, shallow) - one of the smaller groups WG21 splits into to do its work. Ch 5 owns the specific rooms.
- **plenary** (§2.3, shallow) - the session where the whole committee meets and makes final decisions. Ch 7 and Ch 8 deepen.
- **national body (NB)** (§2.4) - a country's standards organization and the official member; it appoints the experts who attend. Experts vote as individuals at plenary. The national body votes for the country only on the formal ballots. Lowercase in running text.
- **guest** (§2.5) - someone who attends without joining a national body, free of charge. A guest can do almost everything but can't vote at plenary. Guest status covers the first meeting only.
- **convener** (§2.5, shallow) - the person who runs WG21 and whom you email to attend. Ch 5 deepens.
- **INCITS** (§2.6) - the US national body, open to anyone, individuals included, so you needn't be American. The yearly fee per committee in the 2026 cycle is $2,703 (full rate), $1,530 (small companies), or $510 (academic).
- **alternate** (§2.6, shallow) - a backup seat holder. The Beman Project's free seats are alternates to its main representative. The text doesn't claim a vote for them.
- **accredited** (§2.7) - having your name in the ISO global directory, which your national body puts it in.
- **mirror committee** (§2.4) - the small group inside a national body that shadows WG21 at home; the group you actually join. Lowercase in running text.
- **global directory** (§2.7) - the ISO roster your name must reach to cast a counting vote at plenary. SD-4 calls it the "ISO LiveLink global directory." Lowercase in running text.
- **champion** (§2.8, shallow) - someone who presents and pushes a proposal. Ch 11 deepens.

Prerequisites: the standard (§1.5); WG21 (intro).
Links: isocpp.org committee page, ISO, IEC, JTC1 (jtc1info.org), SC22 (open-std.org/jtc1/sc22), the Brno June 2026 trip report, isocpp.org meetings and participation page (linked for both the convener and the national body chairs), INCITS, the Beman Project, C++Now, CppCon, ACCU, Meeting C++, the isocpp.org worldwide conference list.

---

## Chapter 3 - How Papers Work

Arc: enters confused about how work happens, leaves understanding the paper is the unit and how to find and read one.

Subheading order:
- 3.1 Nothing Happens Without a Paper (SD-4's rule, run into the prose with the rulebook linked: a paper has to exist, arrive on time, and have someone to present it - hallway talk matters but decides nothing until it's in a paper)
- 3.2 What a Paper Is and Its Types (ask-paper and inform-paper, flagged as informal labels, and the inform-paper often gets read more - design and wording papers - standing documents)
- 3.3 The P-Number System (P, D, N - N-numbers are official ISO document numbers, like the working draft, an agenda, or minutes, and every paper before 2015 - revisions R0 and up)
- 3.4 Finding Any Paper (open-std.org is the one official archive and every paper link in the book points there - wg21.link, an unofficial shortcut run by Mara Bos, named in code and never linked, and leaving off the revision lands you on the newest one - wg21.org does not appear in this chapter)
- 3.5 The Mailing System and Deadlines (mailings most months of the year, nine in 2025, biggest just before and after each meeting - eight hundred or more papers a year counting revisions - pre-meeting deadline weeks ahead - the late-paper rule: a late update to a paper that made the deadline can still be heard)
- 3.6 The Paper Lifecycle (idea to International Standard in seven steps, with the author writing the wording and a wording group reviewing, fixing, and approving it, the national-body comment round, C++26 drew 411, and the approval vote in plain words - most new-feature proposals stop somewhere along the way - links the isocpp.org stage-by-stage page)
- 3.7 Design Review versus Wording Review (and the handoff: once the design is approved, the author's proposed text goes to a wording group)
- 3.8 Defect Reports and the Issues Lists (anyone can report an issue, and only a full-committee-approved fix to the published standard makes it a defect report, while a fix to brand-new draft text doesn't get that label - core and library lists, linked - the wording groups work them and plenary-approved fixes go into the working draft - the library list says wording raises your chances)
- 3.9 Reading a Paper Critically (what to look for, red flags, compare against the prior revision; if a paper leaves a gap, tell the author)
- 3.10 The Documents Everyone Should Read: SD-4 and P2000 (SD-4 covers polls, consensus, deadlines, ballots, and how to escalate a disagreement - P2000R5 "Direction for ISO C++")

Owns:
- **paper** (§3.1) - a written proposal or report; the unit of all committee work.
- **P-number / N-number / D-number** (§3.3) - a paper's ID: P is a numbered proposal, D is an unpublished draft, N is an official ISO document number (the working draft, an agenda, minutes, and every paper before 2015).
- **ask-paper / inform-paper** (§3.2) - informal labels for a paper that asks for a poll and one that only puts facts on the record.
- **revision (R0, R1, ...)** (§3.3) - the version of a paper; R0 is first, higher is later.
- **open-std.org** (§3.4, shallow) - the official archive where every paper lives. Ch 4 deepens.
- **wg21.link** (§3.4) - an unofficial shortcut that redirects a paper number to its open-std.org copy, like wg21.link/p2300r10. Leave off the revision and it lands on the newest one. Named, never linked.
- **the mailing** (§3.5) - a batch of papers, published most months of the year. The biggest land just before and just after each meeting.
- **pre-meeting mailing deadline** (§3.5) - the cutoff, weeks before a meeting, after which a new paper isn't actionable.
- **late-paper rule** (§3.5) - a new paper that misses the deadline waits for the next round, but a late update to a paper that made the deadline can still be heard. Ch 10 restates it.
- **the paper lifecycle** (§3.6) - the path a paper takes from idea to International Standard.
- **design review** (§3.7) - deciding whether C++ wants the change at all, and how it should work.
- **wording review** (§3.7) - checking that the exact standard text says the approved design precisely, with no gaps.
- **issue** (§3.8, shallow) - a reported bug in the standard that anyone can file, which the committee then decides whether to fix.
- **defect report** (§3.8) - an issue whose fix to the published standard the full committee has approved. A fix to brand-new draft text doesn't get that label.
- **issues lists** (§3.8) - the core language and library issues lists that track standard defects; the wording groups work through them.
- **standing document (SD)** (§3.2) - a numbered document holding the committee's own rules and practices.
- **SD-4** (§3.10) - the standing document describing how WG21 works in practice; everyone is expected to know it.
- **Direction Group / P2000** (§3.10, shallow) - a small group of experienced members that recommends direction, and its paper P2000, "Direction for ISO C++." Ch 5 deepens.

Prerequisites: the standard, IS, the working draft (§1.5, §1.6) - WG21, plenary, subgroup, national body (Ch 2).
Links: open-std.org, SD-4 on isocpp.org, P2000, P2300, Herb Sutter's March 2026 trip report (the 411 comments), the isocpp.org life-of-an-ISO-proposal page, the core and library issues lists. wg21.org is not linked here.

---

## Chapter 4 - How to Participate Remotely

Arc: enters thinking you must travel to matter, leaves empowered to contribute today from your desk.

Subheading order:
- 4.1 You Can Take Part from Your Desk (reading, reviewing, and discussing from home with no meeting badge - the lowest-effort start is a review on the wg21.org paper-review list, which needs a free GitHub or Google login - each paper gets a one-week review window and a credited summary on wg21.org, and giving reviews earns you reviews - the one gate: attending one meeting as a guest, in person or by video, opens the committee's private channels)
- 4.2 The Official Sites, and One Unofficial One (isocpp.org and open-std.org are official, and open-std.org is sorted by date with no search, the source of truth - wg21.org is the unofficial, volunteer-run site for browsing, with the mailing filtered by group, full-text search, and each group's report, while the papers still live on open-std.org)
- 4.3 Floating Ideas: std-proposals (a public list for early-stage ideas, a warm reply is encouragement and not a verdict, the real test is the bar in chapter 9)
- 4.4 Following Along from Anywhere (trip reports like Herb Sutter's blog, official minutes as an N-paper, N5040 for March 2026, start with a trip report - the #include <C++> Discord is open to anyone, a gentle place for beginner questions)
- 4.5 Open-Source Help: The Beman Project (Beman builds open-source implementations of proposed library features, and a bug report from real code is evidence a proposal needs)
- 4.6 One Meeting Opens the Rest (the one gate again: one meeting as a guest, in person or by video, after emailing the convener as chapter 2 described - meetings are hybrid, hallway talk is hard to join remotely, time zones, and SD-4 prefers a concern raised on the email lists before a meeting over one raised in the room)
- 4.7 The Reflector (you can join the lists once you've attended one meeting as a guest, in person or by video, and before that many topic lists are publicly readable and the person who runs a topic group can add an expert - posts on the closed lists are private, so poll questions and numbers can be shared freely but a person's words need that person's consent - courtesy, "costs you a reader for a decade")
- 4.8 The Wiki and Mattermost (the wiki holds agendas, schedules, video-call links, and poll pages, is password-protected, so ask the convener how a guest gets in, and don't edit unless asked - Mattermost at chat.isocpp.org is the committee's real-time chat, not public, so ask the convener about it too - the courtesy rule holds in chat)
- 4.9 Telecons between Meetings (subgroup telecons, about thirty a month per isocpp.org - the wiki lists the schedule and links - guests welcome with the same heads-up to the convener - you may be asked to take the minutes)
- 4.10 Voting from Afar: Electronic Polls (rules in P2195R2, "Electronic Straw Polls" - each round is a paper, the May 2025 round is P3712R0 with outcomes in P3713R0 - you can vote once you've joined a national body, or for about a year after attending a week-long meeting - twenty-three people took part in that round - vote only on what you've followed)

Owns:
- **wg21.org** (§4.2, deep) - the unofficial, volunteer-run site for browsing the mailing by group, searching full text, and downloading each group's report, and the home of the public paper-review list. It is named first in 4.1 for that review list, and it is owned here and no longer appears in Ch 3.
- **isocpp.org** (§4.2) - the public-facing C++ site, with standing documents and the committee page.
- **open-std.org** (§4.2, deep) - the official archive of papers and drafts, sorted by date with no search (introduced in Ch 3).
- **std-proposals** (§4.3) - the public mailing list on lists.isocpp.org for floating an idea before writing a paper.
- **the Beman Project** (§4.5) - builds open-source implementations of proposed standard library features so people can try them before the vote.
- **the reflector** (§4.7) - the committee's email mailing lists, where most discussion happens between meetings. Each subgroup keeps its own list, and posts on the closed lists are private.
- **the wiki** (§4.8) - the committee's internal, password-protected hub for agendas, schedules, video-call links, and poll pages.
- **Mattermost** (§4.8) - the committee's real-time chat at chat.isocpp.org, for committee participants.
- **telecon** (§4.9) - an online meeting a subgroup holds between the big in-person meetings.

Prerequisites: paper, the mailing, N-number, SD-4 (Ch 3) - subgroup, plenary, guest, convener, national body (Ch 2).
Note: "straw poll" gets a one-line plain gloss in 4.10 ("a quick vote that steers a group's work"). The formal definition is owned by section 8.2. Use one gate phrase throughout: "attending one meeting as a guest, in person or by video." Author's call: do not name the C++ Alliance, and do not mention a C++ Slack.
Links: wg21.org and its paper-review list on lists.wg21.org, isocpp.org, open-std.org, the public lists index on lists.isocpp.org, chat.isocpp.org, std-proposals, the #include <C++> Discord, the isocpp.org meetings page (the convener and the telecon count), P2195R2, P3712R0, P3713R0, herbsutter.com, N5040, SD-4, the Beman Project. wg21.link does not appear in this chapter.

---

## Chapter 5 - How WG21 Is Structured

Arc: enters seeing a blur of acronyms, leaves with a clear map of the rooms and who decides what.

Subheading order (as written):
- 5.1 One Committee, Many Rooms (the rooms are WG21's subgroups from chapter 2, every one open to you even as a guest, and the schedule grid runs six or seven at once - no pick-a-room advice here)
- 5.2 The Evolution Rooms: EWG and LEWG
- 5.3 The Wording Rooms: CWG and LWG (the paper's author drafts the wording, and these rooms review it, fix it, and approve it)
- 5.4 Study Groups (incubation; subgroup specialties; numbered SG1 through SG23, fifteen active as of 2026, the rest dormant; links the committee page instead of a table)
- 5.5 How a Paper Moves Between Groups (joint sessions)
- 5.6 The Train Model (ships every three years - C++14 onward, not C++11 - Sutter pitched it in August 2011 and N3316, the minutes, records his case - the model since 2012 per P1000R7, January 2026 - contracts pulled from C++20 in 2019, P1823R0, then put into C++26 in February 2025, P2900R14)
- 5.7 How Features Get Removed (pulling versus removing - deprecation as the formal first step - auto_ptr deprecated in C++11 and removed in C++17 - exported templates cut in C++11 though almost no compiler built them - GCC's library still ships auto_ptr)
- 5.8 The People Who Run It (the convener appoints chairs, creates study groups, sets the schedule, and judges consensus - SC22 appoints the convener for terms of up to three years with no limit on renewals - two vice-conveners and a secretary - two project editors - chair - someone from the room takes the minutes)
- 5.9 Who Sets Priorities: The Direction Group (membership by invitation, not election - the Direction Group leaves votes on individual papers to the rooms)
- 5.10 Chair Power (discretion, paper queues, scheduling as a silent veto - SD-4's rule for what chairs take first - every paper has a public GitHub tracking issue - ask the chair for a slot)
- 5.11 The Rules: Standing Documents (eight current, gaps from retired numbers - SD-9 holds LEWG's library policies and SD-10 holds EWG's language principles - new ones need full-committee agreement)
- 5.12 The Limits of Power: Volunteers and the Implementer Veto (nobody can be ordered, WG21 only recommends and the countries vote to make the standard official - a veto over what you can use, not over what gets adopted - the exported templates were stranded by it - P3962R0, "Implementation reality of WG21 standardization," January 2026, written by eighteen implementers)

Owns:
- **the rooms** (§5.1) - the nickname for WG21's subgroups. Every room is open to guests.
- **the schedule grid** (§5.1) - the timetable of parallel sessions across the week.
- **EWG (Evolution Working Group)** (§5.2) - the room that decides language design direction.
- **LEWG (Library Evolution Working Group)** (§5.2) - the room that decides library design direction.
- **CWG (Core Working Group)** (§5.3) - the room that reviews, fixes, and approves the exact language wording the author drafted.
- **LWG (Library Working Group)** (§5.3) - the room that reviews, fixes, and approves the exact library wording the author drafted.
- **study group (SG)** (§5.4) - a focused group that incubates ideas in one area before they move on to the main rooms.
- **the train model** (§5.6) - the rule that C++ ships on a fixed schedule, every three years, with whatever is ready.
- **deprecation** (§5.7) - a formal notice in the standard that a feature may go in a later version. Removal comes years after it.
- **convener** (§5.8, deep) - the officer who runs WG21: appoints chairs, creates study groups, sets the schedule, judges consensus; appointed by SC22 for three-year terms (introduced in Ch 2).
- **project editor** (§5.8) - one of the two people who maintain the working draft text.
- **chair** (§5.8) - the person who runs a room: sets its agenda, words its polls, and calls consensus.
- **the Direction Group** (§5.9, deep) - the small senior group that sets priorities. Long-term direction in P2000 (introduced in Ch 3), next-standard priorities in P5000.
- **the implementer veto** (§5.12) - the reality that if GCC, Clang, and MSVC won't implement something, the standard can't force them. A veto over what you can use, not over what gets adopted.

Prerequisites: convener, plenary, subgroup, SC22 (Ch 2, restate with parenthetical) - design review, wording review, the paper lifecycle, standing document, Direction Group (Ch 3) - IS, the three implementers (Ch 1).
Links: the committee page on isocpp.org, N3316, P1000R7, P1823R0, P2900R14, SC22, P2000, P5000, SD-4, SD-9, SD-10, the cplusplus/papers GitHub tracker, the standing documents page, P3962R0.

---

## Chapter 6 - Getting There

Arc: enters anxious about the practical leap, leaves prepared and braced.

Subheading order:
- 6.1 What a Meeting Week Looks Like (three in-person meetings a year, dates and places on the isocpp.org upcoming meetings page - Monday through Saturday, roughly 8:30 a.m. to 5:30 p.m. with optional evening sessions, Saturday wrapping up by 2 p.m. - the rooms run in parallel, six or seven at once - a short plenary Monday morning - the closing plenary Saturday, where adopted wording enters the working draft)
- 6.2 Preparing Before You Go (aim your reading at one home room and read its agenda papers, not every room - filter the latest mailing on wg21.org by group - read SD-4 - get onto the meeting wiki, and ask the convener how a guest gets in)
- 6.3 The Cost and How to Pay for It (no registration fee - flights, hotel nights, and meals on you, can run into the thousands - each meeting's logistics paper, like N5057 for spring 2027, and SD-5 - the week away from your job and three weeks a year away from home - many are sponsored by employers and others pay their own way - your first meeting has no membership fee as a guest, coming back takes a seat through a national body, so start with your own country's and take the free seat from chapter 2 if the fee is too steep, and the trip is still yours to cover - the video option, since meetings are hybrid and a third or more attend online)
- 6.4 Booking the Trip (a bulleted order: email the convener to say you're coming as a guest, read the logistics paper, handle any visa early, book your own hotel, land by Sunday afternoon for the 6 p.m. orientation, fly home after Saturday's closing plenary)
- 6.5 What to Bring (packing is quick - laptop, charger, plug adapter for the host country, your home room's papers downloaded - patience)
- 6.6 Bracing for Your First Meeting (it will be overwhelming, and that's normal - about two dozen new guests at every meeting - stick with your home room - the payoff is your second meeting)

Owns:
- **meeting week** (§6.1) - the six-day Monday-to-Saturday gathering, held three times a year.
- **home room** (§6.2) - the one room that's your base all week, whose agenda papers you read before you arrive.

Prerequisites: the mailing, SD-4 (Ch 3) - subgroup, guest, convener, national body, the free seat (Ch 2) - the wiki, wg21.org, hybrid meetings (Ch 4) - the rooms (Ch 5).
Psychological note: your first meeting is orientation, not production. Set expectations low and steady.
Links: the isocpp.org upcoming meetings page, the isocpp.org meetings and participation page (the convener), wg21.org, SD-4, N5057, SD-5.

---

## Chapter 7 - In the Room

Arc: enters nervous about how to behave, leaves confident in the room's rhythm and norms.

Subheading order:
- 7.1 The Opening Plenary (officers say hello, first-time attendees introduce themselves, and the agenda and updated working drafts get approved, then everyone scatters to the subgroups - your one part is the introduction: your name and where you're from)
- 7.2 Inside a Session (the loop: sit near the back, the chair calls up a paper and its author presents, hands go up and the chair keeps a queue, questions and pushback, the author answers, often a quick poll chapter 8 explains, then the next paper - wording rooms run the loop on the text itself)
- 7.3 Cycling Between Rooms (keep your home room from chapter 6 but follow the paper when it comes up elsewhere, each room's agenda on the wiki shows when - read that room's papers before you go)
- 7.4 Meeting Etiquette (don't dominate or reopen a point the room has moved past, laptop for notes - listen more than you talk at first)
- 7.5 How to Speak (one point, about two minutes - say your name for the scribe and remote attendees - use the microphone)
- 7.6 Confidentiality and the Code of Conduct (what happens in the room mostly stays there, so you can float a half-formed idea - no live-tweeting, blogging, recording, or photographing other people's screens, though a screenshot of the slides for your own notes is fine - quoting works like the reflector rule from chapter 4, and poll questions and numbers are free to share once the meeting is over, per N5040 for March 2026 - for everything else describe what was said, never who said it - the ISO Code of Ethics and Conduct plus the IEC Code of Conduct - the meeting slide with "jokes and humor may not translate" - SD-4 points to ISO's reporting process)
- 7.7 Note-Taking (every session is minuted and SD-4 says everyone present "should be prepared to take minutes" - the scribe teaches you the room - to volunteer, put your hand up when the chair asks, notes usually go on the room's wiki page, get the gist plus every poll's exact wording and numbers - the scribe can ask a speaker to repeat a point)
- 7.8 Where Relationships Form (hallway talk, meals are networking, the trap of liking people and agreeing with them)
- 7.9 Get Out of Your Lane (P2000: "try to spend at least one day each meeting in a WG that isn't 'your own'" - serve before you push - ask how the IETF or W3C does it - stay skeptical)

Owns:
- **opening plenary** (§7.1) - the Monday session that introduces officers, welcomes new members, approves the agenda and the updated working drafts, then sends everyone to the rooms.
- **the Code of Conduct** (§7.6) - the ISO Code of Ethics and Conduct and the IEC Code of Conduct, which WG21 follows together. They cover behavior in meetings and on social media.
- **confidentiality rule** (§7.6) - the norm against live-tweeting, blogging, recording, or photographing other people's screens, and against quoting people. Poll questions and their numbers are free to share once the meeting is over. For everything else, describe what was said, never who said it.
- **scribing how-to** (§7.7) - how minutes work and how to volunteer as the minute taker. The word scribe first appears in section 2.8 in a clause, and the how-to is owned here.

Prerequisites: plenary, guest (Ch 2) - the reflector rule, the wiki (Ch 4) - the rooms, chair (Ch 5) - home room (Ch 6) - paper schedule (Ch 3, Ch 5) - straw poll (Ch 8, in plain words only).
Psychological note: the meeting cadence is seductive; don't let attendance become the reward. Go into every discussion skeptical and question the room's priors.
Links: the ISO Code of Ethics and Conduct (iso.org PUB100011) and the IEC Code of Conduct (iec.ch basecamp page), both behind bot protection, so verified by search only - N5040 - SD-4 - P2000R5 - the IETF - W3C.

---

## Chapter 8 - How Decisions Get Made

Arc: enters puzzled by how votes work, leaves able to read the room and vote with conviction.

Subheading order (as written):
- 8.1 The Culture of Consensus (not unanimity, absence of sustained opposition, ISO's definition quoted in SD-4 - a few mild objections don't block it but a small group of firm, reasoned objections can - consensus as social pressure)
- 8.2 Straw Polls and the Five-Point Scale (the chair may instead ask whether anyone objects where the room clearly agrees - pick the vote's strength as carefully as the side, and save strongly against for what you can't live with - everyone in the room votes in a subgroup, guests included - no fixed number settles it, so the chair judges)
- 8.3 Reading Poll Results (the 2:1 guideline and the word "normally," applied after the chair may ask the against voters why and poll again - neutrals stay out of the ratio and a mostly neutral room is a warning sign - a small minority can block, since a block of strong-against votes can sink a proposal and that is built into the system, the January 2022 poll at 37 to 17, P2459R0 - the limit, SD-4: consensus is "not a tyranny of the majority" and "not a tyranny of the minority," so once heard, objectors can't keep saying no)
- 8.4 Straw Poll versus Formal Vote (a straw poll is a temperature check, and formal votes are taken at plenary and on the national ballots - the committee treats straw polls as honest predictors of the formal vote)
- 8.5 When to Vote and When to Abstain (vote sincerely and be ready to say why and name what would change your mind - the lone strongly-against vignette - abstain on a paper you haven't read, and voting with the room is noise - P2000, trimmed: "I didn't have time to read the document" is no reason to oppose a paper that came in on time - demand evidence)
- 8.6 Two Gates: Direction versus Design (and "encouragement is not approval" - expansion statements, P1306R1, approved by EWG for C++20 in 2019, adopted for C++26 in 2025)
- 8.7 When You Can't Live with It (say so early, on the reflector before the meeting or in discussion before the poll, and an ally on the merits helps - the three-step escalation path with the 5 p.m. deadline the evening before the closing plenary - the convener may ask your delegation's chair whether the objection is personal or national, and it's national only if the delegation has talked it through - SD-4: an objection that skipped these steps "should not be given weight" - after the deadline, a new reflector thread or a national ballot comment, backed by at least a draft paper)
- 8.8 The Plenary: Where Features Enter the Draft (closing plenary Saturday - it usually runs on silence, then an objection forces a three-way poll - only experts in the global directory vote, so guests watch - std::byte failed 24 to 15 in November 2016, N4623, and passed 44 to 2 with the same name at the next meeting, N4654, after P0583R0, "std::byte is the correct name," answered the objection in writing)
- 8.9 Processing Issues (CWG and LWG work the issues lists and move ready fixes at plenary in one batch, N5015 - file a clear issue with a proposed fix)
- 8.10 The Countries Vote (each country gets a single vote, and countries usually see the draft twice: the committee draft for comments, the round meant for changing the text, which drew 411 comments for C++26, then the DIS for approval - a good comment works like a small paper with a fix, and drafting one needs no seniority - C++26's DIS ballot was scheduled to run July 31 to October 9, 2026 - two-thirds of voting countries approve and no more than a quarter of votes cast can be no - a country with concerns usually votes yes with comments, and a no means not wanting the work "to progress at all in any form," per SD-4 - FDIS only after technical changes, otherwise straight to publication - the committee aims to make the DIS its last ballot, so a design change that late needs nearly everyone on board)

Owns:
- **consensus** (§8.1) - general agreement shown by the absence of sustained opposition; not a majority and not unanimity.
- **straw poll** (§8.2) - a subgroup poll, usually on a five-point scale (strongly favor, weakly favor, neutral, weakly against, strongly against), that shows the room's sense and steers the work but puts nothing into the standard. The strength of a vote matters as much as its side.
- **the 2:1 guideline** (§8.3) - the rough rule that a proposal normally advances with more than twice as many in favor as against.
- **formal vote** (§8.4) - a binding vote, distinct from a straw poll: the plenary poll on a motion, where the convener judges consensus, or a national ballot.
- **abstain** (§8.5) - choosing not to vote because you aren't familiar with the issue.
- **direction approval** (§8.6) - an early "we want this" gate.
- **design approval** (§8.6) - a later "this specific design is right" gate.
- **escalation path** (§8.7) - SD-4's three steps for a "cannot live with" objection: tell the EWG and LEWG chairs as early as you can, post on the subgroup's reflector by 5 p.m. the evening before the closing plenary, and raise it with your national body. After the deadline, the concern waits for a later round, backed by at least a draft paper.
- **closing plenary** (§8.8) - the Saturday session where subgroups report and the committee polls to adopt wording into the working draft.
- **committee draft** (§8.10) - the comment ballot, the round meant for changing the text. Chapter 3 describes the comment round in plain words. Lowercase in running text, and the book doesn't use the acronym CD.
- **DIS / FDIS** (§8.10) - the Draft and Final Draft International Standard ballot stages where national bodies vote, one country, one vote. The FDIS happens only when the text changes technically after the DIS.

Prerequisites: plenary, national body, guest, global directory (Ch 2); paper, SD-4, issues lists, Direction Group / P2000 (Ch 3); the reflector (Ch 4); the rooms, EWG, LEWG, CWG, LWG, chair, convener (Ch 5).
Psychological note: consensus is social pressure with a polite name. Keep your wits about you, vote your conviction not the room's momentum, and demand evidence.
Links: SD-4, P2459R0, P2000R5, P1306R1, N4623 (Issaquah 2016 minutes), N4654 (Kona 2017 minutes), P0583R0, the core and library issues lists, N5015 (the June 2025 editors' report).

---

## Chapter 9 - What Goes Into a Proposal

Arc: enters with an idea, leaves knowing the bar a proposal must clear.

Subheading order:
- 9.1 What Belongs in a Paper (the low bar you control: a paper, on time, with someone to present it, then ask the chair for a slot, which chapter 10 covers, while a yes is a different game - four arguments: the problem is worth solving, the design, the alternatives, and proof it works - cite earlier papers on the same ground - you don't need coauthors, and in the February 2026 mailing more than half the papers had one author - P4024R0 says a single author citing diverse reviewers is just as valid, so thank reviewers by name)
- 9.2 The Three Pillars (example-based, principle-based, shows alternatives; SD-4's own three, the difference between "someone's cool idea" and "a real proposal")
- 9.3 The Abstract as Elevator Pitch
- 9.4 Tony Tables (named for Tony Van Eerd, who came up with the format; his C++17 tables on GitHub)
- 9.5 Show the Alternatives: The Steel Man (two steel men - P2000: showing only your design's advantages and only a rival's disadvantages "is not acceptable" - the strongest answer to both is evidence the room can check)
- 9.6 Implementation Experience (no ISO requirement to build it first, per the submit-a-proposal page, but consensus is easier with a working implementation, so it's optional in the rules and expected in the room - feature-test macros, with the rules in SD-FeatureTest, kept by SG10)
- 9.7 Writing Standard Wording (shall versus should - stable labels, not section numbers - you draft the wording, and once the design is settled SD-4 expects you to bring in a wording expert to polish it, with the chairs helping you find one - CWG or LWG then reviews, fixes, and approves it, so have your expert on board before that review starts)
- 9.8 A Short Tutorial (P2000 asks for one early, to keep features for "ordinary programmers" out of expert-only territory)
- 9.9 Scope and Dependencies (split large papers, ship in stages)
- 9.10 The High Bar (burden on the proposer, default no - core language is hard mode - most new-feature proposals don't make it, and that's the system working: the Networking TS, 2018, still not in the standard, with the library design room's 2021 online polls, P2453R0, leaning toward std::execution, which didn't land until C++26 - the Transactional Memory TS never merged, and P1875R0 proposed a "lite" version - one stalled over design, the other for lack of proof)

Owns:
- **the three pillars** (§9.2) - the habit that a strong paper is example-based, principle-based, and shows alternatives. SD-4 asks for all three. A coined label, so lowercase.
- **Tony Table** (§9.4) - a side-by-side before/after table that makes a proposal's value visible, named for Tony Van Eerd.
- **steel man** (§9.5) - the strongest version of the argument against your proposal, which you then answer with evidence. A coined label, so lowercase.
- **implementation experience** (§9.6) - proof your proposal has been built and used, ideally in more than one place.
- **feature-test macro** (§9.6) - a predefined symbol that lets code check whether a compiler supports a feature. The rules are in SD-FeatureTest.
- **shall / should** (§9.7) - standard-wording verbs: "shall" is a requirement, "should" is advice.

Prerequisites: paper, design review, wording review, SD-4, P2000, the Direction Group (Ch 3) - the standard, stable labels, TS (Ch 1) - study group, CWG, LWG, chair (Ch 5) - consensus, design approval (Ch 8).
Psychological note: be convinced by overwhelming evidence and nothing else. Go into your own paper skeptical.
Links: P4024R0, SD-4, Tony Van Eerd's cpp17_in_TTs on GitHub, P2000R5, SD-FeatureTest, the submit-a-proposal page, the February 2026 mailing, P2453R0, P2300R10, P1875R0, the Networking TS and the Transactional Memory TS on iso.org (bot-protected, so verified by search only).

---

## Chapter 10 - Producing and Submitting Your Paper

Arc: enters ready to write, leaves equipped with the tools and the submission path.

Subheading order:
- 10.1 Float the Idea First (std-proposals - P4024R0's "no surprise competitors" rule: check for papers on the same problem, talk to their authors first, then merge into one paper or write a joint paper that compares both, and chairs can ask for either - build something before you write it up)
- 10.2 Prototyping: Compiler Explorer and GitHub (let readers run your code, a live link on Compiler Explorer, a public GitHub repo)
- 10.3 Writing the Paper: Tools and Template (mpark/wg21, Bikeshed, COWEL, LaTeX - the tools ship their own templates - the official template is the "Template for Library Proposals" on the submit-a-proposal page, built for library features, though its questions make a checklist for any paper)
- 10.4 Make It Accessible (contrast, monospace code, clear headings, skimmable on a phone)
- 10.5 Coauthoring and Revision History (you don't need a coauthor, as chapter 9 showed - name one presenter - spell out what changed in each revision)
- 10.6 Patent Disclosure
- 10.7 Submitting the Paper: SD-7 (SD-7 covers the header, file formats, and mailing deadlines - the deadline is 2 p.m. UTC on the Monday four weeks before the meeting, per SD-7 - the late-paper rule restated: a new paper that misses it waits, a late update to a paper that made it can still be heard - upload at isocpp.org/papers with an isocpp.org login, and "Save and Mark for Review" is the click that counts - each paper in a mailing gets a GitHub tracker issue, and some chairs schedule from it)
- 10.8 Getting on the Agenda (email the chair, confirm in person or by video, and asking isn't pushy - a paper with no presenter goes nowhere)
- 10.9 The Other 80% (design approval is a start, not the finish; the life-of-a-proposal page's "other 80%" line)

Owns:
- **SD-7** (§10.7) - the standing document covering the paper header, the file formats, and the mailing deadlines. It is not a formatting rulebook and it does not hand out paper numbers.
- **the official template** (§10.3) - the "Template for Library Proposals" on isocpp.org's submit-a-proposal page, built for library features only, plus the tools' own versions in mpark/wg21 and Bikeshed.
- **Compiler Explorer** (§10.2) - the online tool (godbolt.org) for showing code run across compilers.

Prerequisites: std-proposals (Ch 4) - paper, P-number, the mailing, the deadline, the late-paper rule (Ch 3) - chair, the GitHub paper tracker, the Direction Group (Ch 5) - design approval, committee draft, DIS (Ch 8) - implementation experience, Tony Table, coauthors (Ch 9).
Links: std-proposals, the isocpp.org submit-a-proposal page, P4024R0, mpark/wg21, Bikeshed, COWEL, SD-7, godbolt.org, GitHub, isocpp.org/papers, the ISO patent policy (iso.org, verified by search only), the cplusplus/papers GitHub tracker, the isocpp.org life-of-a-proposal page.

---

## Chapter 11 - Championing Your Paper

Arc: enters hopeful about your paper, leaves resilient for the long social campaign.

Subheading order (as written):
- 11.1 Before the Room: Presocialization (the five minutes before a poll settle what the hallway left open, so line up a few supporters who reviewed the paper - momentum built on merit is fair game, momentum built on numbers is what chapter 8 said to resist - earn supporters over years by reviewing other people's papers first, then coauthoring)
- 11.2 Finding and Being a Champion (finding one when you can't present in person or by video - championing someone else's paper builds trust)
- 11.3 The First Gate: "Do We Want It at All?" (frame it in the Direction Group's priorities, P5000R1)
- 11.4 When the Poll Goes Against You (sent back is not rejection; re-litigation)
- 11.5 Negotiating: Back-Pocket and Max-Min
- 11.6 Disagreement versus Opposition, and When to Withdraw
- 11.7 How Reputation Works (start small, claim a territory, pick your battles)
- 11.8 The Presenter Is Judged Too (don't cause needless delay - SD-4 warns that escalating topic after topic erodes credibility - procedural momentum, though a revision count isn't evidence when you vote)
- 11.9 The Long Game (years, not months, which lives only here - famous long-running proposals - stackful coroutines' P0876 at revision 24 as of July 2026)
- 11.10 The Structural Headwinds (the Bandwidth Gap, with a quiet inbox not meaning no and a two-minute reader in mind - the expert bubble, with reviews on wg21.org and the short tutorial as the two fixes - corporate resource asymmetry, with the Beman Project as a place to build a library feature in the open)
- 11.11 The Emotional Side (don't take it personally - burnout is real, and the 2020 pulse poll in P2260R0 found over 60 percent of those who answered often exhausted by meetings and other demands, the year every meeting moved online - set limits before you need them: your home room and one more, capped telecons, read only what you'll vote on)

Owns:
- **presocialization** (§11.1) - talking up your idea in hallways and on the lists, building support ahead of the room.
- **champion** (§11.2, deep) - the person who presents and advocates for a paper, author or not (introduced in Ch 2).
- **back-pocket alternative** (§11.5) - a fallback design you keep ready if your first choice is rejected. Hyphenated, per AGENTS.md.
- **max-min solution** (§11.5) - the smallest version of a proposal that everyone can accept.
- **re-litigation** (§11.4) - re-debating a question the committee already settled.
- **procedural momentum** (§11.8) - the benefit of the doubt a paper earns from many revisions and prior favorable polls.
- **the Bandwidth Gap** (§11.10) - there are far more papers than reviewers and time to handle them.
- **the expert bubble** (§11.10) - the tendency for papers to be written by experts for experts.

Prerequisites: paper, design and wording review, the eight hundred papers a year count (Ch 3) - wg21.org, the Beman Project (Ch 4) - the rooms, the Direction Group, chair, volunteers (Ch 5) - home room (Ch 6) - consensus, straw poll, direction and design approval, the escalation path (Ch 8) - the short tutorial, Tony Table, "most new-feature proposals don't make it" (Ch 9) - champion (Ch 2).
Psychological note: burnout is real, the Bandwidth Gap is structural, and knowing when to stop is a skill. Set boundaries.
Links: P5000R1, SD-4, P2300R10, P0876R24, P2260R0.

---

## Chapter 12 - C++ Design Principles

Arc: enters wondering why good ideas die, leaves respecting the deep constraints.

Subheading order:
- Intro (the oldest of these rules come from Stroustrup's The Design and Evolution of C++, 1994, called D&E, and EWG's SD-10 still starts from his list - read it before a language proposal)
- 12.1 Standardize Existing Practice (the committee's safest path - bless what already works - fmt and range-v3, linked)
- 12.2 Backward Compatibility (the weight of decades of code - the committee is reluctant to ship a second type, since a second "safer" vector would split the library - C++20 added std::jthread beside std::thread rather than change the old one)
- 12.3 ABI: The Invisible Constraint (the constraint you're least likely to see coming, backward compatibility one level down - the std::regex callback to chapter 1 - ABI sits outside the standard's text and is a promise the compiler teams make, the implementer veto at its sharpest - std::unordered_map stuck twice over, also by its interface - the Prague ABI vote of 2020, on Titus Winters's P1863R1 and P2028R0, with his 5 to 10 percent speed estimate and engineer-millennia cost - SD-10 makes a stable ABI the default and allows a break case by case with reasons written down - the ABI Review Group advises on particular proposals)
- 12.4 The Zero-Overhead Principle (exceptions as the famous case, P0709R4 counts them as one of two language features that break the rule, and a 2018 survey cited there found 52 percent of developers had exceptions banned in part or all of their code)
- 12.5 Freestanding versus Hosted
- Close (the Delegate's Oath callback: a no that protects sixteen million users is the oath kept by someone else)

Owns:
- **standardize existing practice** (§12.1) - the preference for blessing tools that already work over inventing new ones.
- **backward compatibility** (§12.2) - the rule that old code keeps working with new standards.
- **ABI (application binary interface)** (§12.3) - the binary contract between compiled pieces of a program, covering the memory layout of types and the way functions are called. Breaking it breaks existing programs.
- **the Prague ABI vote** (§12.3) - the early 2020 decision not to break ABI across the library for C++23, while refusing to promise stability forever. In effect, existing binaries stayed safe and the frozen types stayed frozen.
- **the zero-overhead principle** (§12.4) - you don't pay for what you don't use, and what you use you couldn't hand-code better.
- **freestanding vs hosted** (§12.5) - two environments: freestanding (no operating system, limited library) and hosted (full library).

Prerequisites: the standard, the three implementers, the Delegate's Oath, std::regex (Ch 1) - the implementer veto, SD-10, EWG (Ch 5) - implementation experience (Ch 9).
Links: The Design and Evolution of C++ (stroustrup.com), SD-10, fmt and range-v3 on GitHub, P1863R1, P2028R0, P0709R4, the committee page on isocpp.org (ABI Review Group).

---

## Chapter 13 - Common Mistakes

Arc: enters confident, leaves humble and careful, able to step around the traps.

Subheading order (one mistake per section, each a recap with the correct behavior):
- 13.1 Showing Up Without Announcing (guests give the convener at least a week's notice and members register ahead - guest status covers your first meeting only, so talk to a national body before your second, since waiting until the first is over may leave the next meeting arriving before your seat does)
- 13.2 Proposing Core Language Features Too Early
- 13.3 Writing an Idea-Only Paper
- 13.4 Skipping the Search for Competing Papers (P4024R0's "no surprise competitors" rule, from chapter 10)
- 13.5 Voting on Things You Haven't Followed
- 13.6 Quoting Reflectors or Notes Publicly (the closed lists, the wiki, and the room are off the public record - describe what was said, never who said it, and wait until the meeting is over to share a session's poll questions and numbers - never post from inside a session, even in your own words)
- 13.7 Raising Concerns Too Late (raise it in the subgroup, with a paper, while the design can still bend - the escalation path closes at 5 p.m. the evening before plenary)
- 13.8 Expecting Majority Rule (consensus works both ways: a minority can stall a paper, but being heard isn't a veto)
- 13.9 Talking Too Much Too Soon
- 13.10 Ignoring Subgroup Direction (follow the guidance, or reopen it in that same room with a paper and new evidence)
- 13.11 Declaring Victory Too Soon (the old "Misreading Encouragement as Approval" and "Declaring Victory at Design Approval" merged: a warm poll means keep going, design approval only starts "the other 80%," then the wording rooms, plenary, and the countries, and even a published standard is only text until the compilers build it)
- Closing (in this order: confusing being busy with making a difference, with chapter 7's packed week stretched to five years and showing up as the way in but not the work - then don't treat the notebook as scripture, read each new SD-4 and trip report and trust them over it - then the first-person farewell, "I wrote this for you," the four-sentence recap, and "I'm still glad you're here")

Owns: no new terms. Restate each referenced term with a short parenthetical.

Prerequisites: draws on every prior chapter.
Psychological note: don't confuse committee participation with impact. A proposal that never ships helped nobody.
Links: P4024R0, SD-4.
