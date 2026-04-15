# tomd - Agent Rules

## What This Is

tomd is a hybrid PDF-and-HTML-to-Markdown converter. It uses deterministic text extraction and multi-signal classification to produce Markdown, with optional LLM resolution for ambiguous sections. PDF conversion uses dual-path extraction with confidence scoring; HTML conversion uses DOM traversal with generator-specific metadata extraction.

## Architecture

Pipeline execution order:

1. Per-page: dual extract (MuPDF + spatial) + edge items + link collection
2. Close document
3. Readability check (early exit if garbage)
4. Header/footer detection and stripping (both paths)
5. Monospace propagation: spatial path's glyph-width classifications applied to MuPDF spans
6. Wording detection: HSV color analysis + drawing decoration correlation for ins/del markup
7. Text cleanup: NBSP, whitespace, dehyphenation, cross-page join (both paths)
8. Span normalization: snap bold/italic boundaries to word edges (both paths)
9. Table detection from MuPDF block positions; exclude table regions from spatial
10. Dual-path comparison -> Sections (confident or uncertain per page)
11. Merge table sections into position
12. Structure: metadata extraction, heading/list/paragraph classification, position-based list detection, paragraph merging, code block detection, wording section detection, language label stripping, nesting validation
13. TOC stripping (fuzzy match against headings)
14. Emit .md + optional .prompts.md

## Multi-Signal Confidence (Critical)

Never classify based on a single signal. Every structural decision (heading, paragraph, list, code, table) must consider all available signals and produce a confidence level.

Available signals and their reliability:
- **Section numbering** (highest) - dotted decimal numbers give unambiguous depth
- **Font size** (high) - relative to the most common (body) size
- **Font weight/style** (medium) - bold/italic flags from font metadata
- **Known section names** (high for WG21) - `Abstract`, `References`, `Wording`, etc.
- **Line geometry** (medium) - length, indentation, vertical gaps
- **Dual-path agreement** (high) - MuPDF and spatial rules agree on boundaries

When signals agree, confidence is high. When they disagree, flag for LLM review. Never silently pick one signal over another - the disagreement is the data.

## Preserve All Metadata

Never discard information from the PDF during extraction. Text is the primary output, but font size, font name, font flags, coordinates, and page boundaries are preserved as annotations. Downstream phases use this metadata for confidence scoring and LLM prompt context.

Discard nothing. Use everything.

## Dual Extraction Path

Every PDF page is processed through two independent extraction paths:
1. **MuPDF path** - `page.get_text("dict")` for MuPDF's block/line/span grouping
2. **Spatial path** - `page.get_text("rawdict")` with four elif branches keyed on
   font-size-relative thresholds (named constants from `types.py`):
   - `dy > PARA_SPACING_RATIO * avg_fs` - flush block (paragraph break)
   - `dy > LINE_SPACING_RATIO * avg_fs` - flush line (new line, same block)
   - `dy > WORD_GAP_RATIO    * avg_fs` - flush line (large vertical gap)
   - `dx > WORD_GAP_RATIO    * avg_fs` - flush word + insert space span

Both produce the same intermediate format. Agreement = confident. Disagreement = uncertain. Never skip one path. The comparison is the confidence mechanism.

When paths disagree: MuPDF version goes in the output (it's more battle-tested). Both versions go in the LLM prompt for reconciliation. The prompt must require all data verbatim - the LLM fixes structure, never content.

## Heading Rules

- Heading level is derived from section numbering depth: `2.1.3` = depth 3 = `####` (depth + 1 because `#` is reserved for the document title)
- Font size provides an independent heading level estimate by ranking sizes larger than body
- All signals are evaluated; confidence depends on agreement count
- Nesting must be validated: no heading may skip more than one level deeper than its predecessor
- When signals conflict, section number wins if present; font-size ranking wins otherwise at lower confidence
- Known unnumbered sections (`Abstract`, `Revision History`, `References`, `Acknowledgements`, `Motivation`, `Wording`, `Proposed Wording`, `Design Decisions`) are top-level (`##`)
- Title is the largest-font non-metadata text block before any numbered section, confirmed by color darkness when available (multi-signal). Category labels (short all-uppercase text like "WG21 PROPOSAL") are consumed, not treated as titles

## Honest Output

The tool must never silently produce bad Markdown.

- If a region is uncertain, emit the MuPDF version in the output marked with `<!-- tomd:uncertain:L{start}-L{end} -->`
- The companion prompts file includes BOTH extraction versions, surrounding context, and all raw metadata
- LLM prompts must require verbatim data preservation - the LLM fixes structure, never content
- If no prompts file is needed (zero uncertain regions), don't write one.
- High-confidence output should look like a human wrote the Markdown - proper heading nesting, unwrapped paragraph lines, correct list formatting, blank lines between blocks

## Markdown Quality

The output Markdown must be clean and readable:
- Paragraphs are single unwrapped lines (no hard wraps from PDF line breaks)
- One blank line between all block elements (paragraphs, headings, lists, code blocks)
- Headings use ATX style (`##` not underlines)
- Lists use the marker from the source when detectable (`-`, `*`, `1.`)
- No trailing whitespace on lines
- No redundant blank lines (max one between blocks)
- Dehyphenate broken words across lines (`imple-` + `mentation` -> `implementation`)
- Join paragraphs that span page breaks (no terminal punctuation + lowercase continuation = same paragraph)
- Hyperlinks become `[text](url)` - only http, https, mailto schemes
- WG21 metadata block becomes YAML front matter
- Collapse multiple spaces, replace non-breaking spaces, normalize whitespace

## LLM Integration (v2)

Auto-resolution via `--llm` flag is deferred to v2. For v1, the tool produces a companion `.prompts.md` file that the user feeds to any LLM manually. The prompts file is plain Markdown - usable by any LLM, any interface.

## File Map

- `main.py` - CLI entry point. Argparse, glob expansion, output path logic, main(). No conversion logic.
- `lib/__init__.py` - Shared text utilities and constants for PDF and HTML converters: `ascii_escape`, `strip_format_chars`, `format_front_matter`, `ALLOWED_LINK_SCHEMES`, and shared regex patterns (`EMAIL_RE`, `DATE_RE`, `DOC_NUM_RE`, `SECTION_NUM_PREFIX_RE`).
- `lib/similarity.py` - Dual-algorithm string similarity (SequenceMatcher + Jaccard). Per-algorithm thresholds, 200-char circuit breaker. Format-agnostic.
- `lib/toc.py` - Table of Contents detection. Matches section texts against known headings using fuzzy similarity. Bridges small gaps. Format-agnostic - no dependency on PDF types.
- `lib/pdf/__init__.py` - Exports `convert_pdf()`. Orchestrates the full pipeline in order. Includes monospace propagation, wording classification, and page 0 color extraction via space-color proxy.
- `lib/pdf/wording.py` - Wording section detection via multi-signal HSV color + drawing decoration analysis. Detects ins/del markup. Confidence levels with prompts file for ambiguous cases.
- `lib/pdf/types.py` - Data classes (`Block`, `Span`, `Line`, `Section`, `PageEdgeItem`), enums (`Confidence`, `SectionKind`), named constants (all public, no underscore prefix), precompiled regex, `is_readable()`.
- `lib/pdf/extract.py` - Dual extraction: `extract_mupdf()` (dict API) and `extract_spatial()` (rawdict + four spatial threshold branches). Link collection and attachment. Calls `is_monospace` during span construction.
- `lib/pdf/mono.py` - Triple-signal monospace detection. Font name decomposition (strip modifiers, split camelCase, check keywords), glyph width uniformity, glyph spacing uniformity.
- `lib/pdf/cleanup.py` - Header/footer detection (edge items per page), repeating strip, span whitespace (NBSP, multi-space on non-mono), dehyphenation, cross-page join, hidden region detection.
- `lib/pdf/spans.py` - Span normalization. Snaps bold/italic style boundaries to word edges. Monospace exempt.
- `lib/pdf/table.py` - Table detection from MuPDF block/line positions. Detects columnar layout (x-gap between lines), extracts as high-confidence TABLE sections, excludes table regions from spatial path.
- `lib/pdf/structure.py` - Dual-path comparison, metadata extraction, heading intelligence (multi-signal, `heading_confidence` public), position-based list detection (x-coordinates), paragraph merging, code block detection, language label detection, nesting validation.
- `lib/pdf/emit.py` - Markdown generation (headings, paragraphs, code blocks, tables, nested lists) with span-level formatting (inline code, bold, italic, links). Prompts file generation for uncertain regions.
- `lib/html/__init__.py` - Exports `convert_html()`. Six-step HTML pipeline: parse, detect generator, extract metadata, strip boilerplate, render DOM, assemble output.
- `lib/html/extract.py` - Generator detection (mpark, bikeshed, hand-written, hackmd, unknown), per-generator metadata extraction, boilerplate stripping. Five generator families supported.
- `lib/html/render.py` - Recursive DOM-to-Markdown traversal. Handles headings, paragraphs, lists, tables, code blocks, wording divs, blockquotes, and inline formatting.

## Header/Footer Stripping

Before dual extraction, scan all pages for repeating content at page edges.

- For each page, capture the top 3 and bottom 3 text items by y-coordinate
- Compare across pages: same text at same y on 50%+ of pages = repeating = strip
- Page numbers: same y, content is a bare number or "Page N" or "N of M" = strip
- Running doc numbers: same y, content matches document number pattern = strip
- Strip these items from page data before extraction runs. They are not content.

## Text Cleanup Rules

- **Dehyphenation**: line ends with `-`, next line starts lowercase -> join word, remove hyphen. Skip known compound prefixes (`self-`, `non-`, `well-`, `cross-`).
- **Cross-page join**: last block on page N has no terminal punctuation, first block on page N+1 starts lowercase -> same paragraph, join.
- **Link extraction**: collected during Phase 2 via `page.get_links()`, matched to text by bounding rect -> `[text](url)`. Only http/https/mailto.
- **Whitespace**: collapse runs, replace non-breaking spaces, strip trailing.
- **WG21 metadata**: Document Number / Date / Reply-to / Audience at top of page 1 -> YAML front matter.

## tomd-Specific Extensions

These extend general rules in the root CLAUDE.md with project-specific instances.

- `fitz.open()` must always be paired with `doc.close()` in a `finally` block. Never rely on garbage collection.
- Font metadata thresholds (what counts as "larger than body," "horizontal close," etc.) must be named constants, not magic numbers scattered in code.
- The four spatial threshold branches (PARA_SPACING, LINE_SPACING, WORD_GAP for dy, WORD_GAP for dx) are the foundation of `extract_spatial`. Changes to these constants affect everything downstream. Test thoroughly.
- Regex patterns for section numbers, known section names, list markers, and metadata fields must be precompiled at module level and defined in one place.
