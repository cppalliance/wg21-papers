# WG21 Paper Style Rules - Ambient Guardrails

Rules that must fire during writing, not just during audit. For mechanical verification (citations, formatting, structure, prose hygiene), invoke the Auditor: `situation-room/tools/auditor.md`. For citation and reference verification, run `cite/cite.py --fix`.

## Formatting

1. Markdown files must be ASCII only - no Unicode characters
2. Diacritics in personal names must never be omitted - represent them using HTML character references. Prefer named character references (`&uuml;`) over numeric character references (`&#252;`), e.g. `Dietmar K&uuml;hl`, `Micha&lstrok; Dominiak`
3. Single dashes (`-`) for all dashes - no em-dashes, no double dashes
4. Human-written tone - not wordy, no AI-characteristic phrasing
5. No git operations - user handles all git manually
6. The `archive/` folder is restricted for human use only - do not read, write, or modify any file in that folder
7. Markdown link URLs that contain literal parentheses must be wrapped in angle brackets: `[text](<url>)`. This is required for DOI URLs and any other URL whose path includes `(` or `)` characters. Without angle brackets, the Markdown parser treats the first `)` in the URL as the end of the link
8. WG21-appropriate style

## Front Matter

9. Every paper begins with a valid YAML front matter block delimited by `---`. Required and optional fields:

   ```yaml
   ---
   title: "Paper Title"
   document: D0000R0
   date: YYYY-MM-DD
   intent: info
   audience: SG1, LEWG
   reply-to:
     - "Author Name <author@example.com>"
   ---
   ```

   - `title` - required, double-quoted string
   - `document` - required, unquoted paper number (e.g. D4007R0)
   - `date` - required, unquoted ISO 8601 date
   - `intent` - required, unquoted, either `info` or `ask`
   - `audience` - required, unquoted comma-separated target audience (e.g. SG1, LEWG)
   - `reply-to` - required, YAML list of double-quoted strings in the form `"Name <email>"`
10. Do not add front matter fields that the Pandoc template (`tools/wg21.html5`) does not consume

## Language and Grammar

11. American English by default. If a paper already uses British/Irish English consistently (e.g. "organisation", "behaviour", "generalise"), preserve that convention - do not convert to American English. When in doubt, check the existing spelling in the file before editing. Papers where Mungo Gill is the sole author use Irish English
12. Follow the Chicago Manual of Style, 18th edition (2024), unless otherwise specified. Where the 18th edition changed a rule, the 18th-edition form governs - do not cite 17th-edition section numbers. In particular, CMOS 6.67 (6.61 in the 17th edition, which said the opposite): capitalize the first word after a colon when a grammatically complete sentence follows, and leave it lowercase when a fragment, list, appositive, or elided infinitive follows. The test is a finite verb, not clause independence. A subjectless predicate is not a complete sentence, so label-style bullets keep lowercase: "`set_error`: calls `stop_src.request_stop()`" and "`IoEnv`: does not exist in any proposal" take no capital, because the subject sits before the colon. Imperatives count as complete sentences, so "has one operation: Accept a string and store it" takes a capital, while "the second mechanism is relinking: the same algorithm compiled once against a type-erased stream" does not. Two carve-outs override the capital. Never recapitalize quoted material - blockquotes, wording divs, and code blocks keep the source's own capitalization, as does proposed normative text presented as bare prose. And a C++ keyword or identifier keeps its own case even when it opens the sentence, so "the limitations: const is shallow" and "rejected it at Oulu 2016: operator&lt; should not be generated" stay lowercase; reword if the lowercase reads badly
13. Prefer "deeper" or "more thorough" over "full" for appendix cross-references. Understatement is better than hyperbole
14. Transitive verbs must not leave their object implicit when the referent is not immediately obvious. Supply the object explicitly. e.g. "forgetting to forward the allocator" not "forgetting to forward"
15. Avoid ambiguous prepositional attachment. When a prepositional phrase could modify either a nearby noun or the main verb, restructure to make the attachment clear. e.g. "The allocator - along with its state - must be discoverable" not "The allocator - with its state - must be discoverable" (where "with its state" could attach to "discoverable")
16. Do not use contractions (it's, they're, don't, etc.) in formal papers. Use the expanded form

## Code Examples

17. Consistent comment style within a code block - either all comments are sentences (capitalized, with terminating punctuation) or all are fragments (lowercase, no period). Do not mix
18. Consistent capitalization in groups of code comments that summarize arithmetic or data
19. Align trailing comment columns when consecutive lines have trailing comments
20. Fenced code blocks must not exceed 90 characters per line. This rule does not apply to mermaid blocks - never reformat mermaid source. When wrapping is needed, follow the conventions for the block's language:

    **C++** - break at a natural syntactic boundary and indent the continuation 4 spaces from the construct it belongs to:
    - Function signatures: break after the return type, or after the opening parenthesis
    - Template parameter lists: break after a comma, align with the first parameter or indent 4 spaces
    - Chained expressions (pipe `|`, `<<`, etc.): break before the operator, align operators vertically
    - Trailing comments: shorten the gap between code and comment rather than wrapping the code, but keep grouped comments aligned with each other (rule 19)
    - If a trailing comment still exceeds 90 characters after tightening the gap, wrap the comment text to a second line. The continuation `//` must align with the `//` on the first line. Never move a trailing comment above the code line - keep all comments in a contiguous block on the right

    **Prose in code fences** (markdown, plain text) - wrap at word boundaries with no continuation indent

## Proposed Wording Sections

21. Proposed wording uses Pandoc fenced divs and HTML `<ins>`/`<del>` elements styled by `tools/paperstyle.css`. Three div classes are available:

    - `:::wording` - unchanged spec text (gray box, gray left border). Inline code inherits neutral color
    - `:::wording-add` - purely additive text (green box, green left border, green text)
    - `:::wording-remove` - purely removed text (red box, red left border, red strikethrough text)

    For mixed changes (unchanged text with inline additions or deletions), wrap the block in `:::wording` and mark individual changes with `<ins>` (green underline) or `<del>` (red strikethrough).

    Do not use the dual-blockquote pattern (separate "Current text:" and "Proposed text:" blockquotes). Do not use separate "Current:" and "Proposed:" fenced code blocks for code changes. Always use the inline `<ins>`/`<del>` convention described here instead

22. Fenced div formatting rules:

    - No space between `:::` and the class name: `:::wording` not `::: wording`
    - Blank line after the opening `:::wording*` marker
    - Blank line before the closing `:::`
    - Do not use blockquote `>` syntax inside wording divs - use plain paragraphs. The div provides visual framing
    - Markdown formatting (`*italic*`, `` `code` ``) works normally inside wording divs

23. Code diffs in wording sections use raw HTML `<pre><code>` blocks (not fenced `` ``` `` blocks) inside a `:::wording` div, with `<ins>` and `<del>` for inline changes. Angle brackets in code must be escaped as `&lt;`/`&gt;`. Example:

    ```
    :::wording

    <pre><code><del>void</del><ins>coroutine_handle&lt;&gt;</ins> await_suspend(
        coroutine_handle&lt;Promise&gt;) noexcept
    {
        <del>start(state);</del>
        <ins>auto h = start(state);</ins>
        <ins>return h ? h : noop_coroutine();</ins>
    }</code></pre>

    :::
    ```

## Tone

24. Do not present options as predetermined conclusions. When recommending alternatives to a committee, present them as options to contemplate, not dictated outcomes
25. Avoid politically charged comparisons - do not invoke other contentious features as analogies unless the comparison is structurally precise. If the structures being compared are fundamentally different, the analogy will be perceived as political

## Abstract

26. Every abstract opens with a single sentence on its own line - the brutal summary. No citations, no paper numbers, no hedging. The sentence must be true, complete, and unsentimental. It is the sentence a reader remembers after forgetting everything else. Examples:
    - "Three deployed executor models were replaced by one that was never deployed."
    - "The committee voted that sender/receiver covers networking. No sender-based networking has shipped."
    For ask-papers, "This paper asks [specific request]" on its own line satisfies the rule - the ask IS the brutal summary. The rest of the abstract follows after a blank line

## Citations and References

27. Inline citations use HTML superscripts: `<sup>[N]</sup>`. One number per superscript - do not combine multiple numbers into a single superscript like `<sup>[1, 2]</sup>`; use adjacent superscripts `<sup>[1]</sup><sup>[2]</sup>` instead
28. Every markdown link to a WG21 paper in body text must have a superscript citation immediately after the closing parenthesis, e.g. `[P2300R10](url)<sup>[N]</sup>`
29. Paper numbers in prose must include the revision suffix (e.g. `P2300R10` not `P2300`), except when referring to a paper series generically rather than a specific revision. The cite tool flags bare `P####` / `D####` without `R` as unversioned
30. The references section heading is `## References` (H2). Subsection headings (H3 or deeper) within References are permitted for grouping
31. References are numbered sequentially by body first-appearance order, forming a single contiguous sequence [1], [2], [3], ... across the entire References section. When subsection headings are used for grouping, numbering continues across subsection boundaries - it does not restart at [1] in each subsection. The cite tool renumbers automatically; authors should follow this convention when writing by hand
32. Each reference entry occupies one line, separated from adjacent entries by a blank line. The canonical format is:

    `[N] [PaperID](url) - "Title" (Authors, Year).`

    Components:
    - `[N]` - square-bracketed number, not `N.` (the latter is a legacy format that the cite tool rewrites)
    - `[PaperID](url)` - versioned paper number as a markdown link to the canonical `open-std.org` URL
    - ` - ` - space, single dash, space as separator
    - `"Title"` - title in double quotes, exactly as it appears on the paper itself
    - `(Authors, Year)` - parenthesised, comma-separated list of full author names (first name then surname, not surname-only), followed by a comma and the four-digit publication year. Diacritics use HTML entities per rule 2
    - `.` - trailing period

    For non-WG21 references (GitHub repositories, books, ISO standards, etc.), follow the same structure where applicable: `[N] [Display Text](url) - "Title" (Authors, Year).` If there is no distinct title (e.g. a GitHub repo where the link text is the project name), omit the ` - "Title"` portion

33. When adding or editing reference entries, verify each component against the source paper itself - do not guess titles, abbreviate author names, or omit the year
34. Use canonical `open-std.org` URLs for WG21 papers, not `wg21.link` short URLs. The cite tool replaces `wg21.link` URLs automatically
35. Every body citation `<sup>[N]</sup>` must have a corresponding reference entry `[N]`, and every reference entry must be cited at least once in the body. Do not leave orphan entries or missing entries for the tool to clean up
36. Each referenced paper appears exactly once in the References section. Do not create a second entry for a paper already listed - reuse the existing citation number
37. When adding a reference entry, look up the paper's title, authors, and date. Trust the source paper's own front matter over the wg21 index when they disagree. For papers in this repo, read the YAML front matter directly. For external papers, check the paper itself at its canonical URL
