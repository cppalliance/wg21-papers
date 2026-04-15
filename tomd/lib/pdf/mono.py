"""Triple-signal monospace font detection.

Three independent signals:
  1. Font name decomposition (strip modifiers, split camelCase, check keywords)
  2. Glyph bounding box widths are uniform (low coefficient of variation)
  3. Glyph x-origin spacing is uniform (measures advance width directly)

Acceptance rules:
  - Two or more signals agreeing: accept (high confidence)
  - Signal 3 alone: accept (measures the defining property of monospace)
  - Signal 1 alone: accept (fallback when no glyph data is available)
  - Signal 2 alone: reject (weakest signal, bbox widths are noisy)

The spatial extraction path (rawdict) provides per-character data for signals
2 and 3. The MuPDF dict path does not. The pipeline orchestrator propagates
spatial glyph-width decisions to MuPDF spans of the same font after extraction.
"""

import math
import re

from .types import Block

_FONT_MODIFIERS = frozenset({
    "thin", "hairline", "extralight", "ultralight", "light",
    "regular", "normal", "book", "medium",
    "semibold", "demibold", "bold", "extrabold", "ultrabold",
    "black", "heavy",
    "italic", "oblique", "roman", "upright",
    "condensed", "narrow", "extended", "expanded", "wide", "compressed",
    "display", "text", "caption", "subhead", "headline", "mt",
})

_MONO_KEYWORDS = frozenset({"mono", "courier", "code", "consolas", "menlo"})

_CAMEL_SPLIT_RE = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

_GLYPH_CV_THRESHOLD = 0.15
_FAT_THIN_REJECT_RATIO = 1.3

_MIN_CHARS_FOR_METRICS = 3
_FAT_CHARS = frozenset("MWmw@%")
_THIN_CHARS = frozenset("Iil1|!.,;:' ")


def _strip_modifiers(font_name: str) -> str:
    """Remove separators and known style/weight/width modifiers."""
    name = font_name.replace("-", " ").replace("_", " ")
    tokens = name.split()
    kept = [t for t in tokens if t.lower() not in _FONT_MODIFIERS]
    return "".join(kept)


def _split_camel(name: str) -> list[str]:
    """Split a PascalCase/camelCase string into lowercase tokens."""
    parts = _CAMEL_SPLIT_RE.sub(" ", name).split()
    return [p.lower() for p in parts if p]


def _font_name_is_monospace(font_name: str) -> bool:
    """Signal 1: font name contains a monospace keyword after decomposition.

    Strips style/weight modifiers, splits camelCase, checks for
    mono/courier/code/consolas in the remaining family tokens.
    """
    family = _strip_modifiers(font_name)
    tokens = _split_camel(family)
    return bool(_MONO_KEYWORDS & set(tokens))


def _coefficient_of_variation(values: list[float]) -> float:
    """Compute coefficient of variation (stddev / mean). Lower = more uniform.

    Uses population variance (divides by N, not N-1).
    """
    if len(values) < 2:
        return -1.0
    if not all(math.isfinite(v) for v in values):
        return -1.0
    mean = sum(values) / len(values)
    if mean == 0:
        return -1.0
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance) / mean


def _glyph_widths_uniform(char_widths: list[float]) -> float:
    """Signal 2: coefficient of variation of character bbox widths.

    Lower value = more uniform = more likely monospace.
    Returns CV, or -1.0 if not enough data.
    """
    widths = [w for w in char_widths if w > 0]
    if len(widths) < _MIN_CHARS_FOR_METRICS:
        return -1.0
    return _coefficient_of_variation(widths)


def _glyph_spacing_uniform(char_x_origins: list[float]) -> float:
    """Signal 3: coefficient of variation of inter-glyph x-origin spacing.

    Measures the advance width directly - the defining property of
    monospace fonts. Strongest signal.
    Returns CV, or -1.0 if not enough data.
    """
    if len(char_x_origins) < _MIN_CHARS_FOR_METRICS:
        return -1.0
    spacings = []
    for i in range(1, len(char_x_origins)):
        dx = char_x_origins[i] - char_x_origins[i - 1]
        if dx > 0:
            spacings.append(dx)
    if len(spacings) < 2:
        return -1.0
    return _coefficient_of_variation(spacings)


def is_monospace(
    font_name: str,
    char_widths: list[float] | None = None,
    char_x_origins: list[float] | None = None,
    chars: list[str] | None = None,
) -> bool:
    """Accept or reject monospace classification from available signals.

    Called during extraction when raw character data is available
    (all three signals), or later with just font_name (signal 1 only).
    When chars are provided, compares fat-character widths (M, W) against
    thin-character widths (i, l, space) for immediate reject.
    """
    if chars and char_widths and len(chars) == len(char_widths):
        fat_w = [w for c, w in zip(chars, char_widths)
                 if c in _FAT_CHARS and w > 0]
        thin_w = [w for c, w in zip(chars, char_widths)
                  if c in _THIN_CHARS and w > 0]
        if fat_w and thin_w:
            avg_fat = sum(fat_w) / len(fat_w)
            avg_thin = sum(thin_w) / len(thin_w)
            if avg_thin > 0 and avg_fat / avg_thin > _FAT_THIN_REJECT_RATIO:
                return False

    s1 = _font_name_is_monospace(font_name)

    s2_cv = _glyph_widths_uniform(char_widths) if char_widths else -1.0
    s3_cv = _glyph_spacing_uniform(char_x_origins) if char_x_origins else -1.0

    s2 = 0.0 <= s2_cv <= _GLYPH_CV_THRESHOLD
    s3 = 0.0 <= s3_cv <= _GLYPH_CV_THRESHOLD

    signals = sum([s1, s2, s3])

    if signals >= 2:
        return True

    if s3:
        return True

    if s1:
        return True

    return False


def propagate_monospace(mupdf_blocks: list[Block], spatial_blocks: list[Block],
                        dominant_font: str) -> None:
    """Apply spatial path's glyph-width monospace decisions to MuPDF spans.

    Collects fonts classified as monospace by the spatial path (which has
    per-character data), filters out the dominant body font (the single
    most common font by character count), and sets monospace=True on
    matching MuPDF spans. The dominant_font must be pre-lowercased.
    """
    mono_fonts: set[str] = set()
    for b in spatial_blocks:
        for ln in b.lines:
            for s in ln.spans:
                if s.monospace and s.text.strip():
                    mono_fonts.add(s.font_name.lower())
    if dominant_font:
        mono_fonts.discard(dominant_font)
    if not mono_fonts:
        return
    for b in mupdf_blocks:
        for ln in b.lines:
            for s in ln.spans:
                if not s.monospace and s.font_name.lower() in mono_fonts:
                    s.monospace = True
