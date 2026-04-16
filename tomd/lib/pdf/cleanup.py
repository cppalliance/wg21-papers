"""Header/footer detection and text cleanup for PDF extraction."""

import logging
import re
from collections import defaultdict, Counter
from dataclasses import replace

from .. import strip_format_chars, DOC_NUM_RE
from .types import (
    Block, Line, Span, PageEdgeItem,
    Y_TOLERANCE, REPEATING_THRESHOLD, EDGE_ITEMS_PER_PAGE,
    TERMINAL_PUNCTUATION,
    PAGE_NUM_RE, COMPOUND_PREFIXES,
    compute_bbox,
)

_log = logging.getLogger(__name__)


def get_edge_items(blocks: list[Block], page_num: int,
                    page_height: float) -> list[PageEdgeItem]:
    """Get the top N and bottom N text items from a page by y-coordinate.

    Deduplicates by (text, rounded y-position) to avoid counting the
    same visual item twice when blocks overlap edge regions.
    """
    items = []
    for block in blocks:
        for line in block.lines:
            text = line.text.strip()
            if not text:
                continue
            y_center = (line.bbox[1] + line.bbox[3]) / 2.0
            items.append(PageEdgeItem(
                text=text,
                y=y_center,
                page_num=page_num,
                bbox=line.bbox,
            ))

    if not items:
        return []

    items.sort(key=lambda it: it.y)
    top = items[:EDGE_ITEMS_PER_PAGE]
    bottom = items[-EDGE_ITEMS_PER_PAGE:]
    seen = set()
    result = []
    for it in top + bottom:
        key = (it.text, round(it.y, 1))
        if key not in seen:
            seen.add(key)
            result.append(it)
    return result


def detect_repeating(all_edge_items: list[list[PageEdgeItem]],
                     total_pages: int) -> set[tuple[float, str]]:
    """Identify header/footer items that repeat across pages.

    For each page, captures the top and bottom EDGE_ITEMS_PER_PAGE items
    by y-coordinate. Items appearing at the same y-position on at least
    half the pages are classified as repeating.

    Returns a set of (y_region, text_or_pattern) tuples to strip.
    """
    if total_pages < 3:
        return set()

    threshold = total_pages * REPEATING_THRESHOLD
    y_buckets: dict[float, list[PageEdgeItem]] = defaultdict(list)

    for page_items in all_edge_items:
        for item in page_items:
            y_key = round(item.y / Y_TOLERANCE) * Y_TOLERANCE
            y_buckets[y_key].append(item)

    repeating = set()
    for y_key, items in y_buckets.items():
        pages_seen = len(set(it.page_num for it in items))
        if pages_seen < threshold:
            continue
        texts = [it.text for it in items]

        if all(PAGE_NUM_RE.match(t) for t in texts):
            repeating.add((y_key, "__PAGE_NUM__"))
            _log.debug("Repeating page number at y=%.1f", y_key)
            continue

        if all(DOC_NUM_RE.search(t) for t in texts):
            repeating.add((y_key, "__DOC_NUM__"))
            _log.debug("Repeating doc number at y=%.1f", y_key)
            continue

        text_counts = Counter(it.text for it in items)
        exact_hit = False
        for text, count in text_counts.items():
            if count >= threshold:
                repeating.add((y_key, text))
                _log.debug("Repeating exact: y=%.1f text=%r", y_key, text)
                exact_hit = True
        if exact_hit:
            continue

    return repeating


def strip_repeating(blocks: list[Block], repeating: set[tuple[float, str]],
                    ) -> list[Block]:
    """Remove lines matching repeating header/footer patterns from blocks."""
    if not repeating:
        return blocks

    result = []
    for block in blocks:
        kept_lines = []
        for line in block.lines:
            text = line.text.strip()
            if not text:
                kept_lines.append(line)
                continue
            y_center = (line.bbox[1] + line.bbox[3]) / 2.0
            y_key = round(y_center / Y_TOLERANCE) * Y_TOLERANCE
            stripped = False
            for ry, rpattern in repeating:
                if abs(y_key - ry) > Y_TOLERANCE:
                    continue
                if rpattern == text:
                    stripped = True
                    break
                if rpattern == "__PAGE_NUM__" and PAGE_NUM_RE.match(text):
                    stripped = True
                    break
                if rpattern == "__DOC_NUM__" and DOC_NUM_RE.search(text):
                    stripped = True
                    break
            if not stripped:
                kept_lines.append(line)
        if kept_lines:
            result.append(Block(
                lines=kept_lines,
                bbox=block.bbox,
                page_num=block.page_num,
            ))
    return result


def _join_cross_page(blocks: list[Block]) -> list[Block]:
    """Join paragraphs that span page boundaries.

    When the last block on page N ends without terminal punctuation
    and the first block on page N+1 starts with a lowercase letter,
    merge them into one block.
    """
    if len(blocks) < 2:
        return blocks

    result = [replace(blocks[0], lines=list(blocks[0].lines))]

    for block in blocks[1:]:
        prev = result[-1]
        prev_text = prev.text.rstrip()
        cur_text = block.text.lstrip()

        if (prev.page_num != block.page_num
                and prev_text
                and cur_text
                and prev_text[-1] not in TERMINAL_PUNCTUATION
                and cur_text[0].islower()):
            prev.lines.extend(block.lines)
            prev.bbox = compute_bbox([ln.bbox for ln in prev.lines])
        else:
            result.append(replace(block, lines=list(block.lines)))

    return result


_MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
_NBSP = "\u00a0"


def _collapse_spaces(text: str) -> str:
    """Replace non-breaking spaces and collapse runs of spaces/tabs to one."""
    return _MULTI_SPACE_RE.sub(" ", text.replace(_NBSP, " "))


def normalize_whitespace(text: str) -> str:
    """Collapse runs of spaces, replace non-breaking spaces, strip trailing."""
    text = strip_format_chars(text)
    text = _collapse_spaces(text)
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines)


def find_hidden_regions(page, body_fonts: set[str] | None = None,
                        ) -> set[tuple[float, float, float, float]]:
    """Find regions of hidden text on a page.

    Detects Google Docs widget artifacts: non-document font with
    non-black color (e.g. Roboto/Material UI framework text rendered
    as dropdown values).

    Rendering mode 3 (invisible text) is intentionally ignored.
    MuPDF's dict/rawdict APIs already exclude mode 3 text from
    extraction output. Collecting mode 3 bboxes would only match
    against the visible text at the same coordinates, causing
    false-positive stripping on Chrome "Save as PDF" output where
    an invisible accessibility overlay covers every page.
    """
    hidden_bboxes = set()

    if body_fonts is None:
        return hidden_bboxes

    for span in page.get_texttrace():
        if span.get("type") == 3:
            continue

        font = span.get("font", "")
        font_lower = font.lower()
        color = span.get("color")
        is_black = (color == 0 or color == (0, 0, 0)
                    or color == 0x000000)
        if (font_lower not in body_fonts
                and not is_black
                and any(p in font_lower
                        for p in ("roboto", "google", "material"))):
            for ch in span.get("chars", []):
                hidden_bboxes.add(tuple(ch[3]))

    return hidden_bboxes


def strip_hidden_blocks(blocks: list[Block],
                        hidden_bboxes: set[tuple[float, float, float, float]]) -> list[Block]:
    """Remove blocks whose text is entirely within hidden regions."""
    if not hidden_bboxes:
        return blocks

    import fitz
    result = []
    for block in blocks:
        has_visible = False
        for line in block.lines:
            for span in line.spans:
                if not span.text.strip():
                    continue
                span_rect = fitz.Rect(span.bbox)
                is_hidden = any(
                    fitz.Rect(hb).intersects(span_rect)
                    for hb in hidden_bboxes
                )
                if not is_hidden:
                    has_visible = True
                    break
            if has_visible:
                break
        if has_visible:
            result.append(block)
    return result


def cleanup_text(blocks: list[Block]) -> list[Block]:
    """Apply all text cleanup operations to extracted blocks."""
    result = []
    for block in blocks:
        cleaned_lines = []
        for line in block.lines:
            cleaned_spans = []
            for span in line.spans:
                new_text = strip_format_chars(span.text)
                if not span.monospace:
                    new_text = _collapse_spaces(new_text)
                cleaned_spans.append(replace(span, text=new_text))
            cleaned_lines.append(Line(
                spans=cleaned_spans,
                bbox=line.bbox,
                page_num=line.page_num,
            ))
        result.append(Block(
            lines=cleaned_lines,
            bbox=block.bbox,
            page_num=block.page_num,
        ))

    result = _join_cross_page(result)

    dehyphenated = []
    for block in result:
        new_lines = []
        pending_trim = None
        for i, line in enumerate(block.lines):
            if pending_trim is not None:
                if line.spans:
                    if pending_trim:
                        new_first = replace(line.spans[0], text=pending_trim)
                        line = Line(spans=[new_first] + line.spans[1:],
                                    bbox=line.bbox, page_num=line.page_num)
                    elif len(line.spans) > 1:
                        line = Line(spans=line.spans[1:],
                                    bbox=line.bbox, page_num=line.page_num)
                    else:
                        pending_trim = None
                        continue
                    pending_trim = None

            if (i + 1 < len(block.lines)
                    and line.spans and block.lines[i + 1].spans):
                last_span = line.spans[-1]
                next_first = block.lines[i + 1].spans[0]
                if (last_span.text.endswith("-")
                        and len(last_span.text) > 1
                        and next_first.text
                        and next_first.text[0].islower()):
                    prefix = last_span.text[:-1].split()[-1].lower() if last_span.text[:-1].split() else ""
                    if prefix not in COMPOUND_PREFIXES:
                        next_text = next_first.text
                        words = next_text.split()
                        first_word = words[0] if words else ""
                        new_last = replace(last_span,
                                           text=last_span.text[:-1] + first_word)
                        line = Line(spans=line.spans[:-1] + [new_last],
                                    bbox=line.bbox, page_num=line.page_num)
                        pending_trim = next_text[len(first_word):].lstrip()

            new_lines.append(line)

        dehyphenated.append(Block(
            lines=new_lines,
            bbox=block.bbox,
            page_num=block.page_num,
        ))

    return dehyphenated
