"""WG21-specific metadata extraction from PDF blocks.

Parses the metadata block at the top of WG21 papers (document number,
date, audience, reply-to) from the raw MuPDF block structure, before
table detection or structuring runs.
"""

import logging
import re

from .. import strip_format_chars, EMAIL_RE, DATE_RE, parse_author_lines
from .types import Block

_log = logging.getLogger(__name__)

_LABEL_RE = re.compile(
    r"(Document\s*(?:Number|#)|Date|Audience|Reply[- ]?to)\s*:",
    re.IGNORECASE,
)

_DOC_NUM_VALUE_RE = re.compile(
    r"([DPN]\d{3,5}(?:R\d+)?)",
    re.IGNORECASE,
)

_PARENS_RE = re.compile(r"[()]")

# Maximum number of continuation blocks consumed after a reply-to label.
REPLY_TO_CONTINUATION_CAP = 5


def _clean(text: str) -> str:
    """Strip zero-width chars and whitespace."""
    return strip_format_chars(text).strip()


def _parse_authors(lines: list[str]) -> list[str]:
    """Parse author name + email from lines into 'Name <email>' entries."""
    def _clean_author(text):
        return _PARENS_RE.sub("", _clean(text)).strip()

    return parse_author_lines(
        lines,
        clean_line=_clean_author,
        skip_line=lambda l: bool(_LABEL_RE.match(l)),
    )


def _store_field(metadata: dict, label: str, value_lines: list[str]) -> None:
    """Store a parsed metadata field into the dict."""
    label_lower = label.lower()

    if "document" in label_lower:
        value = _clean(" ".join(value_lines))
        m = _DOC_NUM_VALUE_RE.search(value)
        if m:
            metadata["document"] = m.group(1).upper()
    elif label_lower == "date":
        value = _clean(" ".join(value_lines))
        m = DATE_RE.search(value)
        if m:
            metadata["date"] = m.group(0)
    elif label_lower == "audience":
        metadata["audience"] = _clean(" ".join(value_lines))
    elif "reply" in label_lower:
        authors = _parse_authors(value_lines)
        if authors:
            metadata["reply-to"] = authors


_COLOR_Y_TOLERANCE = 5.0


def _lookup_lightness(text_colors: dict[float, float] | None, y: float) -> float:
    """Find the lightness value for the nearest y within tolerance."""
    if not text_colors:
        return 0.0
    best_y = min(text_colors.keys(), key=lambda k: abs(k - y), default=None)
    if best_y is not None and abs(best_y - y) <= _COLOR_Y_TOLERANCE:
        return text_colors[best_y]
    return 0.0


def extract_metadata_from_blocks(blocks: list[Block],
                                 text_colors: dict[float, float] | None = None,
                                 ) -> tuple[dict, set[int]]:
    """Extract WG21 metadata from the first blocks of page 0.

    PDF block-level scan (pathway 2 of 3). Higher precedence than
    structure._extract_metadata; both are merged in convert_pdf with this
    result winning on key conflicts.

    Handles two formats:
      - Scrivener: each field is its own block (label on line 0, value on line 1+)
      - Google Docs: multiple fields in one block (each line has label: value)

    Title is chosen by two signals: largest font size (primary) and
    darkest color (secondary, via space-color proxy for Type 3 fonts).

    Returns (metadata_dict, consumed_block_indices).
    Metadata dict keys: "title", "document", "date", "audience", "reply-to".
    All keys are optional; only fields found in the PDF are included.
    "reply-to" value is a list of "Name <email>" strings.
    """
    metadata: dict = {}
    consumed: set[int] = set()

    page0_blocks = [(i, b) for i, b in enumerate(blocks) if b.page_num == 0]

    pre_label_blocks: list[tuple[int, float, float, str]] = []
    for i, block in page0_blocks:
        if not block.lines:
            continue
        has_label = any(_LABEL_RE.match(_clean(ln.text)) for ln in block.lines)
        if has_label:
            break
        content_lines = [_clean(ln.text) for ln in block.lines if _clean(ln.text)]
        if not content_lines:
            continue
        if not _DOC_NUM_VALUE_RE.match(content_lines[0]) and block.font_size > 0:
            lightness = _lookup_lightness(text_colors, block.bbox[1])
            pre_label_blocks.append(
                (i, block.font_size, lightness, " ".join(content_lines)))

    title_idx = None
    if pre_label_blocks:
        best = max(pre_label_blocks, key=lambda x: (x[1], -x[2]))
        title_idx = (best[0], best[3])
        for entry in pre_label_blocks:
            consumed.add(entry[0])

    for i, block in page0_blocks:
        if not block.lines:
            continue

        found_any = False

        for li, line in enumerate(block.lines):
            line_text = _clean(line.text)
            if not line_text:
                continue

            m = _LABEL_RE.match(line_text)
            if not m:
                continue

            found_any = True
            label = m.group(1)
            remainder = line_text[m.end():].strip()

            value_lines = []
            if remainder:
                value_lines.append(remainder)

            for vl in block.lines[li + 1:]:
                vl_text = _clean(vl.text)
                if _LABEL_RE.match(vl_text):
                    break
                value_lines.append(_clean(vl.text))

            _store_field(metadata, label, value_lines)

        if found_any:
            consumed.add(i)
            if "reply" in " ".join(_clean(ln.text) for ln in block.lines).lower():
                continuation_count = 0
                for j, next_block in page0_blocks:
                    if j <= i:
                        continue
                    if j in consumed:
                        continue
                    if continuation_count >= REPLY_TO_CONTINUATION_CAP:
                        break
                    next_text = _clean(next_block.lines[0].text) if next_block.lines else ""
                    if not next_text or _LABEL_RE.match(next_text):
                        break
                    has_email = any(EMAIL_RE.search(ln.text) for ln in next_block.lines)
                    if has_email:
                        extra_authors = _parse_authors([ln.text for ln in next_block.lines])
                        if extra_authors:
                            existing = metadata.get("reply-to", [])
                            metadata["reply-to"] = existing + extra_authors
                            consumed.add(j)
                            continuation_count += 1
                    else:
                        break

    if title_idx is not None and "title" not in metadata:
        idx, title_text = title_idx
        if title_text:
            metadata["title"] = title_text
            consumed.add(idx)

    if consumed:
        _log.debug("Extracted metadata: %s (consumed blocks %s)",
                    list(metadata.keys()), sorted(consumed))

    return metadata, consumed
