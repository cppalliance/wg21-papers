"""Dual-path PDF text extraction: MuPDF grouping and spatial rules."""

import logging
from urllib.parse import urlparse

from .. import ALLOWED_LINK_SCHEMES
from .types import (
    Block, Line, Span,
    WORD_GAP_RATIO, LINE_SPACING_RATIO, PARA_SPACING_RATIO,
    FALLBACK_FONT_SIZE,
    compute_bbox,
)
from .mono import classify_monospace

_log = logging.getLogger(__name__)


def extract_mupdf(page, page_num: int) -> list[Block]:
    """Extract text using MuPDF's built-in block/line/span hierarchy.

    Uses page.get_text("dict"). Returns MuPDF's interpretation of
    paragraphs, lines, and word groupings with font metadata preserved.
    """
    data = page.get_text("dict", flags=0)
    blocks = []
    for blk in data.get("blocks", []):
        if blk.get("type") != 0:
            continue
        lines = []
        for ln in blk.get("lines", []):
            spans = []
            for sp in ln.get("spans", []):
                text = sp.get("text", "")
                if not text:
                    continue
                flags = sp.get("flags", 0)
                font = sp.get("font", "")
                spans.append(Span(
                    text=text,
                    font_name=font,
                    font_size=sp.get("size", 0.0),
                    bold=bool(flags & (1 << 4)),
                    italic=bool(flags & (1 << 1)),
                    monospace=classify_monospace(font),
                    bbox=tuple(sp.get("bbox", (0, 0, 0, 0))),
                    origin=tuple(sp.get("origin", (0, 0))),
                    color=sp.get("color", 0),
                ))
            if spans:
                lines.append(Line(
                    spans=spans,
                    bbox=tuple(ln.get("bbox", (0, 0, 0, 0))),
                    page_num=page_num,
                ))
        if lines:
            blocks.append(Block(
                lines=lines,
                bbox=tuple(blk.get("bbox", (0, 0, 0, 0))),
                page_num=page_num,
            ))
    return blocks


def extract_spatial(page, page_num: int) -> list[Block]:
    """Extract text using raw character coordinates and spatial rules.

    Uses page.get_text("rawdict") for per-character bounding boxes.
    Classifies each consecutive character pair via four elif branches,
    using font-size-relative named constants from types.py:

      dy > PARA_SPACING_RATIO * avg_fs  -> flush block (paragraph break)
      dy > LINE_SPACING_RATIO * avg_fs  -> flush line (new line, same block)
      dy > WORD_GAP_RATIO    * avg_fs  -> flush line (large vertical gap)
      dx > WORD_GAP_RATIO    * avg_fs  -> flush word + insert space span
    """
    data = page.get_text("rawdict", flags=0)
    chars = []
    for blk in data.get("blocks", []):
        if blk.get("type") != 0:
            continue
        for ln in blk.get("lines", []):
            for sp in ln.get("spans", []):
                font_name = sp.get("font", "")
                font_size = sp.get("size", 0.0)
                flags = sp.get("flags", 0)
                bold = bool(flags & (1 << 4))
                italic = bool(flags & (1 << 1))
                color = sp.get("color", 0)
                for ch in sp.get("chars", []):
                    c = ch.get("c", "")
                    if not c:
                        continue
                    bbox = tuple(ch.get("bbox", (0, 0, 0, 0)))
                    origin = tuple(ch.get("origin", (0, 0)))
                    chars.append((c, bbox, origin, font_name, font_size,
                                  bold, italic, color))

    if not chars:
        return []

    avg_fs = sum(c[4] for c in chars) / len(chars)
    half_height = max(avg_fs * 0.5, 1.0)
    chars.sort(key=lambda c: (round(c[1][1] / half_height), c[1][0]))

    blocks: list[Block] = []
    cur_spans: list[Span] = []
    cur_lines: list[Line] = []
    cur_word_chars: list[tuple] = []
    prev = None

    def _flush_word():
        if not cur_word_chars:
            return
        text = "".join(c[0] for c in cur_word_chars)
        first = cur_word_chars[0]
        last = cur_word_chars[-1]
        bbox = (first[1][0], first[1][1], last[1][2], last[1][3])
        char_widths = [c[1][2] - c[1][0] for c in cur_word_chars]
        char_x_origins = [c[2][0] for c in cur_word_chars]
        chars_list = [c[0] for c in cur_word_chars]
        cur_spans.append(Span(
            text=text,
            font_name=first[3],
            font_size=first[4],
            bold=first[5],
            italic=first[6],
            monospace=classify_monospace(first[3], char_widths, char_x_origins,
                                        chars=chars_list),
            bbox=bbox,
            origin=first[2],
            color=first[7],
        ))
        cur_word_chars.clear()

    def _flush_line():
        _flush_word()
        if not cur_spans:
            return
        bbox = compute_bbox([s.bbox for s in cur_spans])
        cur_lines.append(Line(
            spans=list(cur_spans),
            bbox=bbox,
            page_num=page_num,
        ))
        cur_spans.clear()

    def _flush_block():
        _flush_line()
        if not cur_lines:
            return
        bbox = compute_bbox([ln.bbox for ln in cur_lines])
        blocks.append(Block(
            lines=list(cur_lines),
            bbox=bbox,
            page_num=page_num,
        ))
        cur_lines.clear()

    for ch_data in chars:
        c, bbox, origin, fn, fs, bold, italic, color = ch_data

        if prev is not None:
            prev_bbox = prev[1]
            prev_fs = prev[4]
            avg_fs = (prev_fs + fs) / 2.0 if (prev_fs + fs) > 0 else FALLBACK_FONT_SIZE

            dy = bbox[1] - prev_bbox[1]
            dx = bbox[0] - prev_bbox[2]

            if dy > avg_fs * PARA_SPACING_RATIO:
                _flush_block()
            elif dy > avg_fs * LINE_SPACING_RATIO:
                _flush_line()
            elif dy > avg_fs * WORD_GAP_RATIO:
                _flush_line()
            elif dx > avg_fs * WORD_GAP_RATIO:
                _flush_word()
                cur_spans.append(Span(
                    text=" ",
                    font_name=fn,
                    font_size=fs,
                    bold=bold,
                    italic=italic,
                    bbox=(prev_bbox[2], bbox[1], bbox[0], bbox[3]),
                    origin=origin,
                ))

        cur_word_chars.append(ch_data)
        prev = ch_data

    _flush_block()
    return blocks


def collect_links(page) -> list[dict]:
    """Collect hyperlink annotations from a page.

    Returns a list of dicts with 'uri' and 'bbox' keys.
    Only http, https, and mailto schemes are kept.
    """
    links = []
    for link in page.get_links():
        uri = link.get("uri", "")
        if not uri:
            continue
        try:
            scheme = urlparse(uri).scheme.lower()
        except (ValueError, KeyError):
            _log.debug("Failed to parse link URI: %r", uri, exc_info=True)
            continue
        if scheme not in ALLOWED_LINK_SCHEMES:
            continue
        from_rect = link.get("from")
        if from_rect is None:
            continue
        links.append({
            "uri": uri,
            "bbox": tuple(from_rect),
        })
    return links


def attach_links(blocks: list[Block], links: list[dict]) -> None:
    """Match link annotations to text spans by bounding rect overlap.

    Mutates spans in-place (sets `link_url`). If multiple links
    overlap the same span, the best-overlap link wins.
    """
    for link in links:
        lx0, ly0, lx1, ly1 = link["bbox"]
        uri = link["uri"]
        best_overlap = 0.0
        best_span = None
        for block in blocks:
            for line in block.lines:
                for span in line.spans:
                    sx0, sy0, sx1, sy1 = span.bbox
                    ox0 = max(lx0, sx0)
                    oy0 = max(ly0, sy0)
                    ox1 = min(lx1, sx1)
                    oy1 = min(ly1, sy1)
                    if ox0 < ox1 and oy0 < oy1:
                        overlap = (ox1 - ox0) * (oy1 - oy0)
                        if overlap > best_overlap:
                            best_overlap = overlap
                            best_span = span
        if best_span is not None:
            best_span.link_url = uri
