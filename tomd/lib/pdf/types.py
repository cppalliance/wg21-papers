"""Shared data types, constants, and precompiled regex patterns for PDF conversion."""

import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

from tomd.lib import DOC_NUM_PATTERN, SECTION_NUM_PATTERN


class Confidence(Enum):
    """Confidence level for structural classification decisions."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"


@dataclass
class Span:
    """A run of text with uniform font properties."""
    text: str
    font_name: str = ""
    font_size: float = 0.0
    bold: bool = False
    italic: bool = False
    monospace: bool = False
    bbox: tuple[float, float, float, float] = (0, 0, 0, 0)
    origin: tuple[float, float] = (0, 0)
    color: int = 0
    link_url: str | None = None
    wording_role: str | None = None


@dataclass
class Line:
    """A sequence of spans forming a single line of text."""
    spans: list[Span] = field(default_factory=list)
    bbox: tuple[float, float, float, float] = (0, 0, 0, 0)
    page_num: int = 0

    @property
    def text(self) -> str:
        return "".join(s.text for s in self.spans)

    @property
    def font_size(self) -> float:
        """Maximum font size among non-whitespace spans."""
        if not self.spans:
            return 0.0
        sizes = [s.font_size for s in self.spans if s.text.strip()]
        return max(sizes) if sizes else 0.0

    @property
    def is_bold(self) -> bool:
        text_spans = [s for s in self.spans if s.text.strip()]
        return bool(text_spans) and all(s.bold for s in text_spans)


@dataclass
class Block:
    """A group of lines forming a paragraph-level unit."""
    lines: list[Line] = field(default_factory=list)
    bbox: tuple[float, float, float, float] = (0, 0, 0, 0)
    page_num: int = 0

    @property
    def text(self) -> str:
        return "\n".join(ln.text for ln in self.lines)

    @property
    def font_size(self) -> float:
        """Most common font size among lines (one vote per line)."""
        sizes = [ln.font_size for ln in self.lines if ln.text.strip()]
        if not sizes:
            return 0.0
        return Counter(sizes).most_common(1)[0][0]


class SectionKind(Enum):
    """The structural role of a document section."""
    TITLE = "title"
    METADATA = "metadata"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    CODE = "code"
    TABLE = "table"
    UNCERTAIN = "uncertain"
    WORDING = "wording"
    WORDING_ADD = "wording-add"
    WORDING_REMOVE = "wording-remove"


@dataclass
class Section:
    """A classified region of the document."""
    kind: SectionKind
    text: str
    confidence: Confidence = Confidence.HIGH
    heading_level: int = 0
    lines: list[Line] = field(default_factory=list)
    mupdf_text: str = ""
    spatial_text: str = ""
    page_num: int = 0
    font_size: float = 0.0
    metadata: dict[str, str | list[str]] = field(default_factory=dict)
    columns: list[list[list[Span]]] = field(default_factory=list)
    fence_lang: str = "cpp"
    indent_level: int = 0


@dataclass
class PageEdgeItem:
    """A text item near the top or bottom of a page, used for header/footer detection."""
    text: str
    y: float
    page_num: int
    bbox: tuple[float, float, float, float] = (0, 0, 0, 0)


# Spatial rule thresholds (relative to font size)
WORD_GAP_RATIO = 0.3
LINE_SPACING_RATIO = 1.8
PARA_SPACING_RATIO = 2.5

# Y-position tolerance for header/footer matching across pages
Y_TOLERANCE = 2.0

# Minimum pages a text must appear on (as fraction) to be a header/footer
REPEATING_THRESHOLD = 0.5

EDGE_ITEMS_PER_PAGE = 3

# Similarity threshold for dual-path comparison (word-level)
SIMILARITY_THRESHOLD = 0.85

# --- Precompiled regex patterns ---

# Section number at the start of a line with required trailing content
# (used for heading detection); shares the core shape with
# SECTION_NUM_PREFIX_RE in lib/__init__.py.
SECTION_NUM_RE = re.compile(rf"^({SECTION_NUM_PATTERN})\s+(.+)")

# Line-anchored pattern targeting "Document Number: PXXXXRN" field lines in
# PDF block text. More restrictive than DOC_NUM_RE in lib/__init__.py, which
# is a broad substring match used for header stripping and HTML contexts;
# both patterns share the core DOC_NUM_PATTERN shape.
DOC_FIELD_RE = re.compile(
    rf"Document\s+(?:Number|#)[:\s]+({DOC_NUM_PATTERN})",
    re.IGNORECASE,
)

REPLY_TO_RE = re.compile(
    r"(?:Reply[- ]to|Author)[:\s]+(.+)",
    re.IGNORECASE,
)

AUDIENCE_RE = re.compile(
    r"Audience[:\s]+(.+)",
    re.IGNORECASE,
)

PAGE_NUM_RE = re.compile(
    r"^\d+$"
    r"|^[Pp]age\s+\d+"
    r"|^\d+\s+of\s+\d+",
)

BULLET_CHARS = frozenset("\u2022\u2023\u25cf\u25e6\u2043\u2219\u25aa\u25ab")

BULLET_RE = re.compile(r"^[\s]*[-*" + "".join(BULLET_CHARS) + r"]\s+")

NUMBERED_LIST_RE = re.compile(r"^[\s]*(?:\d+[.)]\s+|[a-z][.)]\s+|\([a-z]\)\s+)", re.IGNORECASE)

COMPOUND_PREFIXES = frozenset({
    "self", "non", "well", "cross", "pre", "post", "re", "co", "anti",
    "multi", "semi", "sub", "inter", "intra", "over", "under", "out",
})

KNOWN_SECTIONS = frozenset({
    "abstract",
    "revision history",
    "references",
    "acknowledgements",
    "acknowledgments",
    "motivation",
    "wording",
    "proposed wording",
    "design decisions",
    "design",
    "implementation",
    "implementation experience",
    "future work",
    "introduction",
    "overview",
    "background",
    "scope",
    "impact on the standard",
    "proposed changes",
    "poll results",
    "changelog",
    "appendix",
    "bibliography",
    "summary",
    "conclusion",
})

TERMINAL_PUNCTUATION = frozenset(".?!:")


def compute_bbox(bboxes: list[tuple]) -> tuple[float, float, float, float]:
    """Compute the bounding box enclosing all given bbox tuples.

    Raises ValueError (via min/max) if bboxes is empty. Callers must
    ensure at least one bbox is present.
    """
    return (
        min(b[0] for b in bboxes),
        min(b[1] for b in bboxes),
        max(b[2] for b in bboxes),
        max(b[3] for b in bboxes),
    )

FALLBACK_FONT_SIZE = 12.0
FALLBACK_BODY_SIZE = 11.0
MIN_UNCERTAIN_WORDS = 10

_READABLE_MIN_LENGTH = 100
_READABLE_MIN_RATIO = 0.3
_READABLE_MAX_SLASH_RATIO = 0.1
_READABLE_SAMPLE_SIZE = 2000


def is_readable(text: str) -> bool:
    """Return True if text looks like real content rather than encoded garbage.

    Heuristic check that rejects PDFs with very low alphanumeric content,
    such as scanned-image-only PDFs or CID-encoded artifacts that produce
    mostly non-alphanumeric output.
    """
    if not text or len(text.strip()) < _READABLE_MIN_LENGTH:
        return False
    sample = text[:_READABLE_SAMPLE_SIZE]
    non_space = [c for c in sample if not c.isspace()]
    if not non_space:
        return False
    readable = sum(1 for c in non_space if c.isalnum() or c in ".,;:!?-()[]{}\"'")
    if sample.count("/") > len(sample) * _READABLE_MAX_SLASH_RATIO:
        return False
    return (readable / len(non_space)) > _READABLE_MIN_RATIO
