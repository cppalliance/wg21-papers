# Agent instructions: A Young Delegate's Notebook

This repo holds one product: A Young Delegate's Notebook. It walks a reader from "I've never heard of WG21" to "I'm attending meetings and finding my niche." Each chapter is a stable plateau, a resting point where someone could stop and still be contributing. The guide accumulates: each chapter builds on the one before it.

This file is the source of truth for voice and mechanics. Supporting files live in `planning/`:

- `planning/emotional-arc.md` - how the reader should feel entering and leaving each chapter.
- `planning/concept-manifest.md` - which chapter owns which term, and the order terms may appear in.
- `planning/source-briefs/` - verified facts for each chapter, with flags for anything unverified.

Where a planning file disagrees with this one about voice or mechanics, this file wins.

## What this book is

- A practical guide for newcomers. Dead simple, accumulative, builds like a pyramid.
- Intimate. One experienced delegate talking to one newcomer, in the second person. It should read nothing like committee papers, standing documents, or reflector mail, which are long, formal, and bureaucratic. If a sentence would fit in an SD-4 revision, rewrite it.
- Opinionated. It has a position: stability over innovation, users first, evidence over enthusiasm.
- Approachable and a little fun. It moves. If a passage reads like a paper or a wall of text, cut it or rewrite it. Invented lore, like the Delegate's Oath, is on purpose: it sounds good and makes the job feel like something you can join.
- A little knowing. An insider aside about where the power sits, or how the agenda really gets set, is welcome. So is some political edge. Don't sand it off. The line is recruiting the reader into a faction, covered under Reform Codex boundaries.
- Voiced by the Patron, an unnamed experienced delegate speaking straight to the reader. The Patron is never named in the text.

## What this book is not

- Not institutional analysis. That is the job of `my-books/wg21-bible/`.
- Not a reform manifesto. That is the job of the Reform Codex.
- Not a textbook, manual, or encyclopedia.
- It does not use coined terms from the Bible. No Consensus Ratchet, no Peerage, no Empty Seat, no Silence As Consensus. The one exception is the Bandwidth Gap (chapter 11), which stays.
- It does not psychoanalyze the committee. Advice is addressed to the reader about their own judgment, in plain words, not jargon.

## Voice

The whole book is one person talking to you. Everything in this section protects that.

### Who is talking

- The Patron is a patient colleague sitting next to the reader, not above the reader.
- The Patron is one person, and says "I" only in the introduction and in the closing paragraphs of the last chapter. Everywhere else the voice is second person: advice, judgments, and imperatives addressed to "you." Never "we," which sounds like the committee or an editorial board. "Let's" is fine, because it means you and me.
- No other voices. Never mention reviewers, coauthors, or what "this notebook's" anyone thinks.

### Who is listening

- Address the reader as "you," always. Never "the newcomer," "participants," or "delegates" when you mean the reader.
- Advice is about the reader's own judgment. Don't guess at why other people vote or act the way they do.
- When the evidence is thin, say so. Never present an opinion as a fact about the committee.
- Without "I," own an opinion in plain words: "often," "in practice," "nobody's counted, but," or a link to the source. A sharp judgment that's plainly the book's stance can stand as written.

### How it sounds

- Contractions. Informal. Plain words.
- Conclusion first in every section. State the destination, then build toward it.
- Let feelings land through short scenes in the second person ("You raise your hand. Thirty heads turn.") rather than telling the reader how to feel.
- Vary the rhythm, because a person talking doesn't keep one beat. Most sentences run 8 to 16 words. Use a short one for punch and an occasional longer one that builds toward its point. Aim for an average near 11.
- Past 25 words a sentence needs a reason. Past 35 it gets split. Never put more than three sentences under 10 words in a row, and never two over 25 in a row.
- Paragraphs 55 words at most, however many sentences that takes.
- `python lint.py` reports these numbers per chapter. It's a mirror, not a judge. Weigh each flag case by case, and never merge sentences just to move a number.
- Starting a sentence with "And," "But," or "So" is fine. So is ending one on a preposition. Chicago agrees, so don't let an edit "fix" them.
- Banned words: delve, tapestry, landscape, ecosystem, realm, robust, leverage, utilize, facilitate, navigate, streamline.
- Audit every *door*, *carry*, and *reach*, in all forms: doors, doorway, carries, carried, carrying, reaches, reached, reaching. They're an AI tic, and `lint.py` flags every one. Keep one only when it's literal and nothing plainer fits. Otherwise say the plain thing: "has" for "carries," "find" or "get to" for "reach," "way in" for "door."
- No committee-speak: "in order to," "with respect to," "it should be noted," "stakeholders." Watch for stacked nouns like "the responsibility of participation in the standardization committee." Say the plain thing.
- A bridge sentence between sections is welcome when it adds something. Never write one that only restates the next heading.
- End each chapter where `planning/emotional-arc.md` says the reader should land: a short closing paragraph in the Patron's voice, then a pointer to what comes next.

## Mechanics

Mechanics follow *The Chicago Manual of Style* wherever this file is silent. Every rule below was picked because it keeps the text sounding like a person instead of a document. Where Chicago and this file conflict, this file wins.

### Punctuation

- No em dashes, no en dashes used as dashes, no double dashes. Prefer a period or a colon. When you truly need a dash, use a single spaced hyphen ( - ).
- No semicolons. Split the sentence.
- Lowercase after a colon, unless two or more full sentences follow it: "Here's the hard rule: the standard almost never shrinks."
- Always use the serial comma: "read, review, and discuss."
- Double quotation marks. Periods and commas go inside the closing quote.

### Capitalization

- Down style. Capitalize only true proper names: WG21, ISO, SC22, INCITS, SD-4, the Direction Group, CppCon.
- Lowercase generic terms, even when committee documents capitalize them: national body, working draft, committee draft, global directory, mirror committee, study group, plenary, convener, chair, head of delegation.
- Capitalize a title only directly before a name: "Convener Guy Davidson," but "the convener."
- "The Delegate's Oath" is a proper name. After that, it's "the oath."
- Coined labels for ideas stay lowercase: steel man, max-min solution, back-pocket alternative. The exception is the Bandwidth Gap, which is capitalized on purpose.

### Emphasis and terms

- No bold in running text.
- Italicize a key term once, where it's defined, then set it in roman: "Behind every release is a living document called the *working draft*."
- Italicize words used as words: "*shall* marks a hard requirement."
- Italicize a vote when the vote itself is the subject, and keep it lowercase: "a *no* vote," "vote *yes* with comments."
- Book titles go in italics: *The Prince*, *The Design and Evolution of C++*. Paper titles go in quotation marks, worded as the paper gives them.
- Code identifiers go in backticks every time: `std::regex`, `memory_order_relaxed`.

### Numbers, dates, and times

- In narrative, spell out zero through one hundred and round numbers: "twenty-eight nations," "about two hundred people," "sixteen million users."
- Use numerals for vote tallies ("57 in favor, 2 against"), ratios like 2:1, years, dates, money, paper and revision numbers, chapter and section numbers, versions like C++26, clock times, and anything in a table.
- Never start a sentence with a numeral.
- Percentages take a numeral and the word: "80 percent." A quoted phrase keeps its own form.
- Write dates month first: "October 9, 2026."
- Write times as "5 p.m.," not "5pm" or "5:00 p.m." Use words when they read naturally: "the evening before plenary."

### Abbreviations

- Spell them out in prose and headings: "for example," "that is," "also known as," "versus." No "e.g.," "i.e.," "a.k.a.," or "vs."
- Committee acronyms (EWG, NB, DIS) are fine once defined in their owning chapter. The book says "committee draft" in full, never CD. See `planning/concept-manifest.md`.

### Spelling

- American spelling, following Merriam-Webster.
- Follow Merriam-Webster for hyphenation. Where it's silent, close common prefixes: coauthor, cowrite, reread, nonvoting.

### Quotations

- Run short quotes into the sentence, so the Patron is the one telling the reader: SD-4 is blunt that "if a proposal doesn't have a paper, it doesn't exist."
- Lowercase a quote's first letter when it runs into your sentence. Trim with an ellipsis (...) to keep only the point.
- No block quotes, except the epigraph.
- The book's two lore lines are Rule of Thumb boxes, not block quotes: the Delegate's Oath in chapter 1, and the four-line motto that closes the introduction ("Keep your wits about you. Be skeptical. Demand evidence. Put the users first."). See Boxes.

### Lists

- Run short items into the sentence: "Keep three things apart: the standard is the text, the compilers try to follow it, and the living language is what real code relies on."
- Use a vertical list only for something the reader will use as a checklist or a sequence of steps.

### Headings

- Headline style: capitalize the first and last words and all major words. Lowercase articles, prepositions, and coordinating conjunctions: "You Can Take Part from Your Desk," "A Newcomer's Path into WG21."
- No abbreviations in headings.

### The epigraph

- A blockquote with no quotation marks around the passage. The source line sits beneath it in the same blockquote, with the work's title in italics.

## Boxes

A box is a short aside set off from the running text. It's a breather, so it has to stay small, and it has to hit hard. No walls of text, no procedural arcana.

- No box runs longer than half a printed page: 120 words at most, not counting the label line.
- If the material needs more room, it isn't a box. Work it into the prose, keep only the one point that matters, or leave it in the residue.
- Boxes follow every voice and mechanics rule in this file, including no semicolons.

Every chapter opens with In This Chapter, a bullet list of the chapter's topics, right after the opening paragraph and before the first section. Every chapter ends with The Short Version, a prose summary right before the closing paragraph. It keeps the 55-word paragraph limit, so a longer summary splits into two or three paragraphs. Everything below is about the other boxes.

### What earns a box

A box earns its place only if it gives the reader one thing to take out of the chapter: a line to live by, a trap to dodge, or something to do today. It has to pass all five tests:

1. Arc: it moves the reader toward the chapter's landing feeling in `planning/emotional-arc.md`, or it delivers the chapter's psychological note.
2. About you: it's about the reader's own choices, feelings, or risks, not about how the institution works.
3. One idea, few words: aim under 50 words. The 120-word cap is a ceiling, not a target.
4. Stands alone: it makes sense to someone flipping pages who reads nothing else.
5. Not a repeat: it says something the nearby prose doesn't, or the prose gives that line up to the box.

Never a box: procedure (fees, thresholds, document numbers, who appoints whom), anything that dates, rulebook quotes that inform rather than move, tables, and stories over 120 words.

Each type has its own job:

- Rule of Thumb: a saying that steadies judgment. 40 words at most.
- Watch Out: a specific trap and what it costs you. 50 words at most.
- Try This Today: one small, free thing the reader can do today, with no membership. 50 words at most.
- From One Delegate's Notebook: one true scene with a human stake and a choice. 120 words at most, and rare. Only the author supplies these, since they must be true, so never invent one. Tell it about "a delegate," never "I."
- From the Rulebook: only when the quoted line itself hits hard, short and striking. Rare.

A chapter gets one or two boxes beyond In This Chapter and The Short Version. A third is fine only in a long chapter where each box serves a different beat. Zero is fine too. No type shows up twice in one chapter, except payload boxes.

### Where a box goes

- Put the box where the reader needs it: right after the paragraph that raises its point, at a paragraph break, in the section it serves. Default to the end of that section.
- Each type has a natural spot. A Watch Out goes right after the risky thing is described. A Try This Today goes once the reader knows enough to act. A Rule of Thumb goes at the end of the section it sums up. A Notebook story goes at the chapter's emotional peak.
- Spread them out. At most one box per section, and never two boxes back to back. At least two paragraphs of prose between any two boxes, counting In This Chapter and The Short Version. Never a box inside the closing paragraphs.

### Leading into and out of a box

- The paragraph before finishes its own thought and creates the need for the box, without announcing it. No "here's a rule of thumb," no "see the box," no colon pointing at it.
- The box adds, it doesn't echo. If the prose already makes the box's point in the same words, that line moves into the box and comes out of the prose.
- The paragraph after picks up the thread from the paragraph before, as if the box weren't there. It never opens with "So," "That," "This," or "It" pointing into the box.
- Two read-through tests: the chapter reads smoothly with every box skipped, and every box makes sense read alone.
- Payload boxes are the exception. When the box is the content of a sentence, the lead-in introduces it with a colon and the next paragraph may comment on it. Only the book's own lore lines get this: the Delegate's Oath in chapter 1 and the four-line motto in the introduction. Both are Rule of Thumb boxes.

### Boxes in the chapter file

In the chapter file, a box is a `div` whose id names its type, with the tags on their own lines and blank lines inside them:

```
<div id="in-this-chapter">

- Why standardization is a responsibility, not a hobby
- How to read the standard without reading all of it

</div>
```

- Each box type has an id in the `BOXES` table in `build.py`, which holds its label and colors. `build.py` prints the label from the id, so the box text has no label line. A new box type needs its own entry there, plus one under the same label in the `BOXES` table in `indesign/layout.jsx` for print.
- A box holds plain paragraphs and bullets only. No headings, bold, blockquotes, numbered lists, or nested boxes.
- The markdown won't render it as a box. The .docx will, as a shaded panel in the reviewers' style, and so will the print edition, as a panel in the same colors as the .docx.
- Don't italicize a defined term in a box, since the body does that where the term is defined. Keep the In This Chapter box free of named documents and sites. It comes before their first, linked mention, so describe the topic instead.

## Structure

- `young-delegates-notebook.md` - the assembled manuscript. Generated. Do not edit by hand.
- `young-delegates-notebook.docx` - the same manuscript as a Word document. Generated and gitignored.
- `chapters/intro.md` - the introduction. Sets the voice for the whole book.
- `chapters/ch-01.md` through `ch-13.md` - the thirteen chapters.
- `build.py` - the assembler. Run `python build.py` from this directory to regenerate the manuscript and its table of contents, in both formats. The docx look lives in one place, the `STYLES_XML` style sheet in `build.py`. The build stops on markdown the docx converter doesn't handle (tables, code fences, nested lists, bold, images, and any raw HTML other than box divs). It also writes `indesign/title.icml` and `indesign/body.icml`, the print stories, with curly quotes and the other print-only fixes. They're generated and gitignored.
- `indesign.py` - the print build. Run `python indesign.py` with InDesign closed to rebuild, then lay out the book in InDesign 2026 from scratch. It starts InDesign and quits it when done, unless documents are open. If InDesign is already open, it stops, because a crash there would lose unsaved work. Pass `--reuse` to run in that session anyway. It writes three files into `indesign/`: `young-delegates-notebook.indd`, `young-delegates-notebook-print.pdf` for the printer (no live links, but link text is blue), and `young-delegates-notebook.pdf` for screens (live links in blue, plus bookmarks). All three are generated and gitignored.
- `indesign/layout.jsx` - the print layout. Trim size, margins, fonts, box colors, and every style live in the spec at the top. The style names must match the ICML names in `build.py`.
- `indesign/cover.jpg` - the cover picture. The layout puts it on the first page, cropped to the page's shape, with a blank page behind it, and the title page follows. Replace the file to change the cover, or delete it to print without one. It's 768 by 1024 pixels, about 120 dpi at this trim size, so a higher-resolution copy would be needed before it goes to a printer.
- `lint.py` - the rhythm report. Run `python lint.py` for every chapter, or `python lint.py ch-01 ch-01.rev` for specific files.

Edit chapter files. Rebuild. Never edit the assembled manuscript directly.

The InDesign document is a build product like the docx. Never hand-edit it, because the next run replaces it. Change the print look in the spec in `layout.jsx`, then run `python indesign.py`.

## Working with the revisions

The `.rev.md` files are reviewer input. Most of the reviewers and editors who wrote them never read this file, the emotional arc, or the concept manifest, so their changes are not gospel. Judge each one on its merits, case by case. Corrections of fact are the most reliable thing in them. New sections, long boxes, and walls of text are the least. Keep what makes the book more approachable, more emotional, and quicker to move through. Leave the rest in the residue.

- The `.rev.md` and `.boxes.md` files are the reviewer's untrimmed originals, kept for reference.
- Box text that isn't in a chapter yet lives in the `.boxes.md` files (see Boxes).
- The book stays at thirteen chapters. The revision's two proposed new chapters were folded in: the national body essentials into chapter 2, and the ballot essentials into chapter 8. Their original text stays in `new-national-body.rev.md` and `new-ballot.rev.md`, not as chapters to build.

## Section numbering and cross-references

- Decimal hierarchy. Chapters are `1`, `2`. Sections are `1.1`, `1.2`. Subsections are `1.2.1`.
- Chapter headings are `## 1. Title` (level 2). Section headings are `### 1.1 Title` (level 3). Subsection headings are `#### 1.1.1 Title` (level 4).
- Headings carry their full number. Headings do not use the section symbol.
- In prose, point to the idea first and the place second: "the guest path from chapter 2." Write "chapter 3" and "section 2.4" in lowercase. No section symbol in prose.
- Older chapter text still uses bold terms and `§2.4` references. Convert them when you edit a chapter.

## Linking

- No citations, footnotes, endnotes, or bibliography. Every reference is an inline hyperlink, the way a colleague points at something.
- Dense inline links. The text should read like a well-linked wiki, not an academic paper.
- Every paper number is a live link to its official copy on open-std.org: `[P4014R2](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2026/p4014r2.pdf)`. No bare paper numbers.
- Never put a wg21.link URL in the book text. It's an unofficial redirect service, not the archive. Use it only to look up a paper's address: `https://wg21.link/p4014r2` redirects to the open-std.org URL, and that resolved URL is what goes in the text. Link a specific revision, and keep the year and extension the redirect gives you, since some papers are HTML, not PDF.
- Chapter 3 teaches wg21.link as a lookup tool, so the text can name it and show the pattern in backticks (`wg21.link/p2300r10`). It is never a hyperlink, even on first mention.
- Every named document, site, list, or tool is linked on first mention in each chapter file. Later mentions of a document in the same file use the plain name.
- A site, list, or tool stays linked every time its name appears in running text, boxes and the short version included. On screen the reader can always click through, and in print the name shows in blue. Headings and the In This Chapter box carry no links.

## The Delegate's Oath

Exact wording, do not paraphrase. In chapter 1 it sits alone in a Rule of Thumb box:

I vow to do what is best for the language, to make no unnecessary proposals, and to put the needs of sixteen million users ahead of my own.

The oath belongs to chapter 1. The introduction holds its spirit ("put the users first") but does not state the formal oath.

The oath is the book's own invention, told as delegate lore: "Some delegates call it the Delegate's Oath." That's deliberate. Don't claim it as the committee's, and don't flag it as unsourced.

## Reform Codex boundaries

The Notebook draws principles from the Reform Codex but never its partisan or operational content. Use Sections 1-4 (the weight of the standard, paper writing, voting, delegate behavior). Do not use Sections 5-9 (reform communication, institutional diagnosis, structural remedies, NB strategy, counter-tactics). The reader should come away thinking "good principles for responsible participation," not "recruited into a faction."
