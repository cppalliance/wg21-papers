#!/usr/bin/env python3
"""cite - Citation normalizer for WG21 papers.

Reads WG21 papers in markdown format, checks citation integrity,
renumbers citations to body-first-appearance order, removes orphan
references, flags uncited links, canonicalizes wg21.link URLs to
open-std.org, and optionally auto-fixes all detected issues.

Usage:
    python cite.py <papers...> [--fix] [--dry-run] [--check] [--config path]
"""

import argparse
import datetime
import html.entities
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import NamedTuple, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CITE_RE = re.compile(r'<sup>\[(\d+)\]</sup>')
CITE_LINK_RE = re.compile(r'<sup>\[\[(\d+)\]\]\([^)]*\)</sup>')
COMPOUND_CITE_RE = re.compile(r'<sup>\[[\d,\s]+\]</sup>')
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^()]*(?:\([^()]*\))*[^()]*)\)')
FENCE_RE = re.compile(r'^(`{3,})')
REF_HEADING_RE = re.compile(r'^#{1,3}\s+References\s*$')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')
REF_FORMAT_A_RE = re.compile(r'^\s*-?\s*\[(\d+)\]\s+(.*)')
REF_FORMAT_B_RE = re.compile(r'^(\d+)\.\s+(.*)')
WG21_LINK_RE = re.compile(
    r'https?://wg21\.link/([a-zA-Z]\d+(?:r\d+)?)', re.IGNORECASE)
PAPER_NUM_RE = re.compile(r'\b([PD]\d{4})\b(?!R\d)')
VERSIONED_PAPER_RE = re.compile(r'\b[PD]\d{4}R\d+\b')
OPEN_STD_PAPER_RE = re.compile(
    r'open-std\.org/jtc1/sc22/wg21/docs/papers/(\d{4})/([a-z]\d+(?:r\d+)?)',
    re.IGNORECASE)
ISOCPP_PAPER_RE = re.compile(
    r'isocpp\.org/files/papers/([a-zA-Z]\d+(?:r\d+)?)',
    re.IGNORECASE)
TRAILING_URL_RE = re.compile(r'\s+https?://\S+\s*$')
REVISION_RE = re.compile(r'^([A-Z]\d{4})(R(\d+))?$')

HTTP_TIMEOUT = 10
INDEX_URL = 'https://wg21.link/index.json'
INDEX_FILENAME = 'index.json'

VALID_CONFIG_KEYS = frozenset({
    'exempt_sections', 'exempt_links', 'exempt_orphans',
})


class WG21Link(NamedTuple):
    line_idx: int
    url: str
    slug: str


class UncitedLink(NamedTuple):
    line_idx: int
    text: str
    url: str


@dataclass
class RefEntry:
    """A single entry in the References section."""
    number: int
    text: str
    line_idx: int
    format: str  # 'A' or 'B'
    subsection: str = ''


@dataclass
class Finding:
    """A single finding from the audit."""
    rule: str
    line: int
    message: str
    severity: str = 'flag'  # 'auto', 'flag', 'error'


@dataclass
class AuditResult:
    """Complete audit state for a paper."""
    filepath: str = ''
    lines: list[str] = field(default_factory=list)
    excluded: set[int] = field(default_factory=set)
    body_cites: list[tuple[int, int]] = field(default_factory=list)
    first_appearance: list[int] = field(default_factory=list)
    old_to_new: dict[int, int] = field(default_factory=dict)
    refs: dict[int, RefEntry] = field(default_factory=dict)
    refs_start: int = -1
    refs_end: int = -1
    orphans: list[int] = field(default_factory=list)
    missing: list[int] = field(default_factory=list)
    uncited_links: list[UncitedLink] = field(default_factory=list)
    wg21_links: list[WG21Link] = field(default_factory=list)
    unversioned: list[tuple[int, str]] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    needs_renumber: bool = False
    refs_heading_h1: bool = False


@dataclass
class PaperMetadata:
    """Metadata for a WG21 paper from the mailing index."""
    paper_id: str
    title: str
    authors: str
    date: str
    url: str


@dataclass
class ResolveResult:
    """Results from pass 2 - URL resolution and metadata lookup."""
    url_map: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, PaperMetadata] = field(default_factory=dict)
    guessed: list[tuple[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# HTML entity encoding
# ---------------------------------------------------------------------------

def to_html_entities(text: str) -> str:
    """Convert non-ASCII characters to HTML entities.

    Uses named entities where available, decimal numeric otherwise.
    """
    result = []
    for ch in text:
        cp = ord(ch)
        if cp < 128:
            result.append(ch)
        elif cp in html.entities.codepoint2name:
            result.append(f'&{html.entities.codepoint2name[cp]};')
        else:
            result.append(f'&#{cp};')
    return ''.join(result)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config(path: Optional[str] = None) -> dict:
    """Load YAML config, returning a validated dict.

    Returns empty-default dict when path is None or file does not exist.
    Raises ValueError on unknown keys.
    """
    defaults = {
        'exempt_sections': [],
        'exempt_links': [],
        'exempt_orphans': [],
    }
    if path is None:
        return dict(defaults)

    p = Path(path)
    if not p.exists():
        return dict(defaults)

    try:
        import yaml
    except ImportError:
        print("warning: PyYAML not installed, ignoring config file",
              file=sys.stderr)
        return dict(defaults)

    with open(p, encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    if raw is None:
        return dict(defaults)

    if not isinstance(raw, dict):
        raise ValueError(
            f"config must be a YAML mapping, got {type(raw).__name__}")

    unknown = set(raw.keys()) - VALID_CONFIG_KEYS
    if unknown:
        raise ValueError(
            f"unknown config keys: {', '.join(sorted(unknown))}")

    result = dict(defaults)
    for k in VALID_CONFIG_KEYS:
        if k in raw:
            val = raw[k]
            if val is None:
                val = []
            if not isinstance(val, list):
                raise ValueError(
                    f"config key '{k}' must be a list, "
                    f"got {type(val).__name__}")
            result[k] = val

    return result


def is_exempt_link(url: str, config: dict) -> bool:
    """Check if a URL matches any exempt_links glob pattern."""
    for pattern in config.get('exempt_links', []):
        if fnmatch(url, pattern):
            return True
    return False


def is_exempt_section(section_name: str, config: dict) -> bool:
    """Check if a section heading matches any exempt_sections entry."""
    name_lower = section_name.strip().lower()
    for exempt in config.get('exempt_sections', []):
        if exempt.strip().lower() == name_lower:
            return True
    return False


# ---------------------------------------------------------------------------
# Scan helpers
# ---------------------------------------------------------------------------

def build_exclusion_ranges(lines: list[str]) -> set[int]:
    """Return set of line indices inside fenced code blocks."""
    excluded = set()
    in_fence = False
    fence_marker = ''
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        m = FENCE_RE.match(stripped)
        if m:
            if not in_fence:
                in_fence = True
                fence_marker = m.group(1)
                excluded.add(i)
            elif (stripped.startswith(fence_marker)
                  and stripped.strip() == fence_marker):
                excluded.add(i)
                in_fence = False
                fence_marker = ''
            else:
                excluded.add(i)
        elif in_fence:
            excluded.add(i)
    return excluded


def find_refs_section(lines: list[str]) -> tuple[int, int]:
    """Find the References section boundaries.

    Returns (start_line, end_line) where start_line is the heading
    and end_line is the last line of the section (or len(lines)).
    """
    refs_start = -1
    for i, line in enumerate(lines):
        if REF_HEADING_RE.match(line.strip()):
            refs_start = i
            break

    if refs_start == -1:
        return -1, -1

    refs_end = len(lines)
    hdr = lines[refs_start].strip()
    heading_level = hdr.count(
        '#', 0, hdr.index(' ') if ' ' in hdr else len(hdr))

    for i in range(refs_start + 1, len(lines)):
        m = HEADING_RE.match(lines[i].strip())
        if m and len(m.group(1)) <= heading_level:
            refs_end = i
            break

    return refs_start, refs_end


def body_line_indices(
    n_lines: int,
    refs_start: int,
    refs_end: int,
    start: int = 0,
) -> list[int]:
    """Line indices that count as body, skipping the References section.

    Anything after the References section - an appendix, for example -
    is still body text, and citations in it are real. Scanning only up
    to refs_start would report a reference cited solely from an appendix
    as an orphan, and --fix would then delete it.
    """
    if refs_start < 0:
        return list(range(start, n_lines))
    return (list(range(start, refs_start))
            + list(range(max(refs_end, start), n_lines)))


def find_section_at_line(lines: list[str], line_idx: int) -> Optional[str]:
    """Return the section heading name that contains the given line."""
    for i in range(line_idx, -1, -1):
        m = HEADING_RE.match(lines[i].strip())
        if m:
            text = m.group(2).strip()
            text = re.sub(r'^\d+[\.\)]\s*', '', text)
            return text
    return None


def extract_body_citations(
    lines: list[str],
    excluded: set[int],
    refs_start: int,
    refs_end: int,
) -> tuple[list[tuple[int, int]], list[int], dict[int, int]]:
    """Walk body top-to-bottom, extract citations in first-appearance order.

    Returns:
        body_cites: all (line_idx, citation_number) pairs
        first_appearance: citation numbers in order of first appearance
        old_to_new: mapping from old number to new consecutive number
    """
    body_cites = []
    seen = set()
    first_appearance = []

    for i in body_line_indices(len(lines), refs_start, refs_end):
        if i in excluded:
            continue
        for m in CITE_RE.finditer(lines[i]):
            n = int(m.group(1))
            body_cites.append((i, n))
            if n not in seen:
                seen.add(n)
                first_appearance.append(n)
        for m in CITE_LINK_RE.finditer(lines[i]):
            n = int(m.group(1))
            body_cites.append((i, n))
            if n not in seen:
                seen.add(n)
                first_appearance.append(n)
        for m in COMPOUND_CITE_RE.finditer(lines[i]):
            inner = m.group(0)
            if CITE_RE.match(inner):
                continue
            for num_m in re.finditer(r'\d+', inner):
                n = int(num_m.group(0))
                body_cites.append((i, n))
                if n not in seen:
                    seen.add(n)
                    first_appearance.append(n)

    old_to_new = {}
    for new_num, old_num in enumerate(first_appearance, start=1):
        old_to_new[old_num] = new_num

    return body_cites, first_appearance, old_to_new


def parse_references(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> dict[int, RefEntry]:
    """Parse the References section, handling both Format A and B.

    Format A: `[N] description text` or `- [N] description text`
    Format B: `N. description text`

    Tracks subsection membership: each entry records the heading text
    of the most recent subsection heading (deeper than the References
    heading level), or '' if before any subsection.
    """
    refs = {}
    has_subsections = False
    current_subsection = ''

    hdr = lines[refs_start].strip()
    refs_level = hdr.count(
        '#', 0, hdr.index(' ') if ' ' in hdr else len(hdr))

    for i in range(refs_start + 1, refs_end):
        stripped = lines[i].strip()
        if not stripped:
            continue

        sub_m = HEADING_RE.match(stripped)
        if sub_m:
            heading_level = len(sub_m.group(1))
            if heading_level > refs_level:
                has_subsections = True
                current_subsection = sub_m.group(2).strip()
            continue

        m_a = REF_FORMAT_A_RE.match(stripped)
        if m_a:
            num = int(m_a.group(1))
            refs[num] = RefEntry(
                number=num, text=m_a.group(2),
                line_idx=i, format='A',
                subsection=current_subsection,
            )
            continue

        m_b = REF_FORMAT_B_RE.match(stripped)
        if m_b:
            num = int(m_b.group(1))
            refs[num] = RefEntry(
                number=num, text=m_b.group(2),
                line_idx=i, format='B',
                subsection=current_subsection,
            )
            continue

    if has_subsections:
        print("warning: References section contains subsections; "
              "renumbering across subsection boundaries may be ambiguous",
              file=sys.stderr)

    return refs


def find_uncited_links(
    lines: list[str],
    excluded: set[int],
    refs_start: int,
    refs_end: int,
    config: dict,
) -> list[UncitedLink]:
    """Find body hyperlinks not immediately followed by <sup>[N]</sup>.

    Excludes: fenced code blocks, exempt sections, exempt URLs.
    """
    uncited: list[UncitedLink] = []

    for i in body_line_indices(len(lines), refs_start, refs_end):
        if i in excluded:
            continue

        section = find_section_at_line(lines, i)
        if section and is_exempt_section(section, config):
            continue

        line = lines[i]
        for m in LINK_RE.finditer(line):
            if _in_inline_code(line, m.start()):
                continue

            text = m.group(1)
            url = m.group(2)

            if is_exempt_link(url, config):
                continue

            after = line[m.end():]
            after_stripped = after.lstrip()
            if after_stripped.startswith('<sup>['):
                continue
            if (after.startswith(')')
                    and after[1:].lstrip().startswith('<sup>[')):
                continue

            before = line[:m.start()]
            if '(' in before:
                open_paren = before.rfind('(')
                if open_paren >= 0 and open_paren > before.rfind(')'):
                    close_paren_pos = after.find(')')
                    if close_paren_pos >= 0:
                        after_paren = after[close_paren_pos + 1:].lstrip()
                        if after_paren.startswith('<sup>['):
                            continue

            if re.match(r'\s*\([^)]*\)\s*<sup>\[', after):
                continue

            uncited.append(UncitedLink(i, text, url))

    return uncited


def find_wg21_links(
    lines: list[str],
    excluded: set[int],
) -> list[WG21Link]:
    """Find all wg21.link URLs in the file (body + references)."""
    results: list[WG21Link] = []
    for i, line in enumerate(lines):
        if i in excluded:
            continue
        for m in WG21_LINK_RE.finditer(line):
            results.append(WG21Link(i, m.group(0), m.group(1)))
    return results


def _find_front_matter_end(lines: list[str]) -> int:
    """Return the line index after the closing --- of YAML front matter."""
    if not lines or not lines[0].strip().startswith('---'):
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            return i + 1
    return 0


def _in_inline_code(line: str, pos: int) -> bool:
    """Check if a position in a line is inside a backtick code span."""
    backtick_count = 0
    for i in range(pos):
        if line[i] == '`':
            backtick_count += 1
    return backtick_count % 2 == 1


def check_unversioned_refs(
    lines: list[str],
    excluded: set[int],
    refs_start: int,
    refs_end: int,
) -> list[tuple[int, str]]:
    """Find bare P/D numbers without revision suffix in body prose.

    Skips front matter, blockquotes, headings, table rows, inline code,
    and URLs - these contexts use bare numbers intentionally.
    """
    results = []
    fm_end = _find_front_matter_end(lines)

    for i in body_line_indices(len(lines), refs_start, refs_end, fm_end):
        if i in excluded:
            continue
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('>'):
            continue
        if stripped.startswith('#'):
            continue
        is_table_row = (stripped.startswith('|') and '|' in stripped[1:])
        for m in PAPER_NUM_RE.finditer(line):
            start_pos = m.start()
            if is_table_row:
                in_link = any(
                    lm.start() <= start_pos < lm.end()
                    for lm in LINK_RE.finditer(line))
                if not in_link:
                    continue
            before = line[:start_pos]
            if before.endswith('wg21.link/'):
                continue
            if before.endswith('/papers/'):
                continue
            if before.endswith('files/papers/'):
                continue
            if _in_inline_code(line, start_pos):
                continue
            if '"' in before and before.count('"') % 2 == 1:
                continue
            results.append((i, m.group(1)))

    return results


def extract_paper_id_from_url(url: str) -> Optional[tuple[str, Optional[int]]]:
    """Extract paper ID and year from an open-std.org, wg21.link, or isocpp.org URL.

    Returns (paper_id, year) or None. Year may be None for wg21.link
    and isocpp.org URLs.
    """
    m = OPEN_STD_PAPER_RE.search(url)
    if m:
        return m.group(2).upper(), int(m.group(1))

    m = WG21_LINK_RE.search(url)
    if m:
        return m.group(1).upper(), None

    m = ISOCPP_PAPER_RE.search(url)
    if m:
        return m.group(1).upper(), None

    return None


# ---------------------------------------------------------------------------
# Pass 1: scan
# ---------------------------------------------------------------------------

def scan(filepath: str, config: dict) -> AuditResult:
    """Run the full scan pipeline on a paper. Read-only, no network."""
    r = AuditResult(filepath=filepath)

    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    content = content.replace('\r\n', '\n')
    r.lines = content.splitlines(keepends=True)

    r.excluded = build_exclusion_ranges(r.lines)
    r.refs_start, r.refs_end = find_refs_section(r.lines)

    r.body_cites, r.first_appearance, r.old_to_new = (
        extract_body_citations(
            r.lines, r.excluded, r.refs_start, r.refs_end))

    identity = all(old == new for old, new in r.old_to_new.items())
    r.needs_renumber = not identity

    if r.refs_start >= 0:
        hdr = r.lines[r.refs_start].strip()
        h_level = hdr.count('#', 0, hdr.index(' ') if ' ' in hdr else len(hdr))
        if h_level == 1:
            r.refs_heading_h1 = True
            r.findings.append(Finding(
                rule='h1-refs',
                line=r.refs_start + 1,
                message='References heading is # (should be ##)',
                severity='flag',
            ))
        r.refs = parse_references(r.lines, r.refs_start, r.refs_end)

    for _num, entry in r.refs.items():
        if entry.format == 'B':
            r.findings.append(Finding(
                rule='format-b-ref',
                line=entry.line_idx + 1,
                message=f'Reference [{entry.number}] uses N. format, '
                        f'should be [N]',
                severity='flag',
            ))

    cited_nums = set(r.old_to_new.keys())
    ref_nums = set(r.refs.keys())
    raw_orphans = sorted(ref_nums - cited_nums)
    exempt_orphan_pats = config.get('exempt_orphans', [])
    r.orphans = []
    for num in raw_orphans:
        entry = r.refs[num]
        if any(fnmatch(entry.text, pat) for pat in exempt_orphan_pats):
            continue
        r.orphans.append(num)

    r.missing = sorted(cited_nums - ref_nums)

    for num in r.orphans:
        entry = r.refs[num]
        r.findings.append(Finding(
            rule='orphan-ref',
            line=entry.line_idx + 1,
            message=f'Reference [{num}] has no body citation',
            severity='flag',
        ))

    for num in r.missing:
        r.findings.append(Finding(
            rule='missing-ref',
            line=0,
            message=f'Body cites [{num}] but no reference entry exists',
            severity='error',
        ))

    r.uncited_links = find_uncited_links(
        r.lines, r.excluded, r.refs_start, r.refs_end, config)
    for line_idx, text, url in r.uncited_links:
        r.findings.append(Finding(
            rule='uncited-link',
            line=line_idx + 1,
            message=f'Uncited link: [{text}]({url})',
            severity='flag',
        ))

    r.wg21_links = find_wg21_links(r.lines, r.excluded)
    for line_idx, url, slug in r.wg21_links:
        r.findings.append(Finding(
            rule='wg21-link',
            line=line_idx + 1,
            message=f'wg21.link URL must be replaced: {url}',
            severity='auto',
        ))

    r.unversioned = check_unversioned_refs(
        r.lines, r.excluded, r.refs_start, r.refs_end)
    for line_idx, paper in r.unversioned:
        r.findings.append(Finding(
            rule='unversioned-ref',
            line=line_idx + 1,
            message=f'Unversioned paper reference: {paper}',
            severity='flag',
        ))

    for i, line in enumerate(r.lines):
        if i in r.excluded:
            continue
        for m in COMPOUND_CITE_RE.finditer(line):
            inner = m.group(0)
            if not CITE_RE.match(inner):
                r.findings.append(Finding(
                    rule='malformed-cite',
                    line=i + 1,
                    message=f'Compound citation should be split: {inner}',
                    severity='flag',
                ))

    return r


# ---------------------------------------------------------------------------
# Pass 2: resolve (network / cache)
# ---------------------------------------------------------------------------

def _construct_open_std_url(slug: str) -> str:
    """Construct a canonical open-std.org URL from a paper slug.

    For P/D papers without a revision suffix, appends R0.
    N-papers don't have revisions.
    """
    slug_lower = slug.lower()
    if (not re.search(r'r\d+$', slug_lower)
            and not slug_lower.startswith('n')):
        slug_lower += 'r0'
    year = datetime.datetime.now().year
    return (f"https://www.open-std.org/jtc1/sc22/wg21/"
            f"docs/papers/{year}/{slug_lower}.pdf")


def _find_latest_revision(
    base: str,
    index: dict[str, dict],
) -> Optional[dict]:
    """Find the highest-revision index entry for an unversioned paper ID.

    E.g. 'P2300' -> scans for P2300R0..P2300RN, returns entry with max N.
    """
    best_rev = -1
    best_entry = None
    for key, entry in index.items():
        m = REVISION_RE.match(key)
        if m and m.group(1) == base:
            rev = int(m.group(3)) if m.group(3) is not None else 0
            if rev > best_rev:
                best_rev = rev
                best_entry = entry
    return best_entry


def load_paper_index(cache_dir: Path) -> dict[str, dict]:
    """Load the wg21.link paper index, refreshing from network if stale.

    Fetches https://wg21.link/index.json when the local cache is older
    than the server copy (checked via HEAD Last-Modified). Falls back
    to the local file silently when offline or on any network error.
    Returns an empty dict if the file is missing and cannot be fetched.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / INDEX_FILENAME

    server_mtime: Optional[float] = None
    if cache_file.exists():
        try:
            req = Request(INDEX_URL, method='HEAD')
            req.add_header('User-Agent', 'cite/1.0')
            with urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                last_modified = resp.headers.get('Last-Modified')
                if last_modified:
                    import email.utils
                    parsed = email.utils.parsedate_to_datetime(last_modified)
                    server_mtime = parsed.timestamp()
        except (HTTPError, URLError, TimeoutError):
            pass

        local_mtime = cache_file.stat().st_mtime
        if server_mtime is None or local_mtime >= server_mtime:
            with open(cache_file, encoding='utf-8') as f:
                return json.load(f)

    try:
        req = Request(INDEX_URL)
        req.add_header('User-Agent', 'cite/1.0')
        with urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            last_modified = resp.headers.get('Last-Modified')
            data = json.loads(resp.read().decode('utf-8'))
    except (HTTPError, URLError, TimeoutError) as e:
        print(f"warning: failed to fetch {INDEX_URL}: {e}", file=sys.stderr)
        if cache_file.exists():
            with open(cache_file, encoding='utf-8') as f:
                return json.load(f)
        return {}

    fd, tmp = tempfile.mkstemp(dir=cache_dir, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, cache_file)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    if last_modified:
        try:
            import email.utils
            parsed = email.utils.parsedate_to_datetime(last_modified)
            mtime = parsed.timestamp()
            os.utime(cache_file, (mtime, mtime))
        except Exception:
            pass

    return data


def lookup_paper_metadata(
    paper_id: str,
    index: dict[str, dict],
) -> Optional[PaperMetadata]:
    """Look up paper metadata from the wg21.link index.

    Returns PaperMetadata or None if the paper is not in the index.
    """
    entry = index.get(paper_id.upper())
    if entry and entry.get('type') == 'paper':
        return PaperMetadata(
            paper_id=paper_id.upper(),
            title=entry.get('title', ''),
            authors=entry.get('author', ''),
            date=entry.get('date', ''),
            url=entry.get('long_link', ''),
        )
    return None


def resolve(
    results: list[AuditResult],
    cache_dir: Path,
    skip_resolve: bool = False,
    skip_guess: bool = False,
) -> ResolveResult:
    """Pass 2: resolve URLs and fetch metadata. Batched across all files."""
    resolved = ResolveResult()

    if skip_resolve:
        return resolved

    index = load_paper_index(cache_dir)

    all_wg21_slugs = set()
    all_paper_ids: set[str] = set()

    for r in results:
        for link in r.wg21_links:
            all_wg21_slugs.add(link.slug.lower())

        for _num, entry in r.refs.items():
            urls_in_text = re.findall(r'https?://[^\s,]+', entry.text)
            for url in urls_in_text:
                info = extract_paper_id_from_url(url)
                if info:
                    pid, _year = info
                    all_paper_ids.add(pid)

        for _line_idx, _text, url in r.uncited_links:
            info = extract_paper_id_from_url(url)
            if info:
                pid, _year = info
                all_paper_ids.add(pid)

    for slug in sorted(all_wg21_slugs):
        wg21_url = f"https://wg21.link/{slug}"
        slug_upper = slug.upper()

        # Tier 1: direct versioned lookup
        entry = index.get(slug_upper)
        if entry and entry.get('type') == 'paper':
            long_link = entry.get('long_link', '')
            if long_link:
                resolved.url_map[wg21_url] = long_link
                info = extract_paper_id_from_url(long_link)
                if info:
                    all_paper_ids.add(info[0])
                continue

        # Tier 2: unversioned - find latest revision in index
        if not re.search(r'R\d+$', slug_upper):
            latest = _find_latest_revision(slug_upper, index)
            if latest and latest.get('long_link'):
                resolved.url_map[wg21_url] = latest['long_link']
                info = extract_paper_id_from_url(latest['long_link'])
                if info:
                    all_paper_ids.add(info[0])
                continue

        # Tier 3: not in index - construct URL deterministically
        if not skip_guess:
            constructed = _construct_open_std_url(slug)
            resolved.url_map[wg21_url] = constructed
            resolved.guessed.append((slug.upper(), constructed))
            print(f"  Guessed: {wg21_url} -> {constructed}",
                  file=sys.stderr)

    for pid in sorted(all_paper_ids):
        if pid in resolved.metadata:
            continue
        meta = lookup_paper_metadata(pid, index)
        if meta:
            resolved.metadata[pid.upper()] = meta

    return resolved


# ---------------------------------------------------------------------------
# Pass 3: write (pure transform)
# ---------------------------------------------------------------------------

def apply_wg21_replacements(
    lines: list[str],
    replacements: dict[str, str],
    excluded: set[int],
) -> list[str]:
    """Replace wg21.link URLs with resolved open-std.org URLs.

    Skips lines inside fenced code blocks (exclusion set).
    Longer URLs are replaced first to prevent substring overlap.
    """
    result = list(lines)
    sorted_repls = sorted(
        replacements.items(), key=lambda kv: len(kv[0]), reverse=True)
    for i, line in enumerate(result):
        if i in excluded:
            continue
        for old_url, new_url in sorted_repls:
            if old_url in line:
                result[i] = result[i].replace(old_url, new_url)
    return result


def renumber_content(
    old_to_new: dict[int, int],
    excluded_line_set: set[int],
    lines: list[str],
) -> str:
    """Renumber all <sup>[N]</sup> and <sup>[[N]](url)</sup> citations.

    Uses a sentinel strategy to avoid collisions:
    Pass 1: all [N] -> [__N__] (every citation, not just those in old_to_new)
    Pass 2: [__N__] -> [new_N] (using old_to_new, falling back to identity)
    """
    working_lines = list(lines)

    for i, line in enumerate(working_lines):
        if i in excluded_line_set:
            continue
        working_lines[i] = CITE_RE.sub(
            lambda m: f'<sup>[__{m.group(1)}__]</sup>',
            line,
        )
        def _link_sentinel(lm):
            num = lm.group(1)
            full = lm.group(0)
            url_start = full.index('](') + 2
            url_end = full.rindex(')</sup>')
            url = full[url_start:url_end]
            return f'<sup>[[__{num}__]]({url})</sup>'
        working_lines[i] = CITE_LINK_RE.sub(
            _link_sentinel, working_lines[i])

    result_lines = []
    for i, line in enumerate(working_lines):
        if i in excluded_line_set:
            result_lines.append(line)
            continue

        def replace_sentinel(m):
            old_n = int(m.group(1))
            new_n = old_to_new.get(old_n, old_n)
            return f'<sup>[{new_n}]</sup>'

        line = re.sub(
            r'<sup>\[__(\d+)__\]</sup>', replace_sentinel, line)

        def replace_link_sentinel(m):
            old_n = int(m.group(1))
            new_n = old_to_new.get(old_n, old_n)
            url = m.group(2)
            return f'<sup>[[{new_n}]]({url})</sup>'

        line = re.sub(
            r'<sup>\[\[__(\d+)__\]\]\(([^)]*)\)</sup>',
            replace_link_sentinel, line)

        result_lines.append(line)

    return ''.join(result_lines)


def reorder_refs(
    lines: list[str],
    refs: dict[int, RefEntry],
    old_to_new: dict[int, int],
) -> list[str]:
    """Reorder reference entries by their new citation number.

    Preserves non-entry lines (blank lines, subsection headings).
    Assigns orphan entries (not in old_to_new) unique numbers above
    the highest active number. Entries stay within their original
    subsection when the References section has subsection headings.
    """
    result = list(lines)

    max_active = max(old_to_new.values()) if old_to_new else 0

    active_entries = {}
    for old_num, entry in refs.items():
        new_num = old_to_new.get(old_num)
        if new_num is not None:
            active_entries[new_num] = entry

    next_orphan = max_active + 1
    orphan_entries = {}
    for old_num in sorted(refs.keys()):
        if old_num in old_to_new:
            continue
        orphan_entries[next_orphan] = refs[old_num]
        next_orphan += 1

    all_numbered = {}
    all_numbered.update(
        {n: (entry, n) for n, entry in active_entries.items()})
    all_numbered.update(
        {n: (entry, n) for n, entry in orphan_entries.items()})

    has_subsections = any(e.subsection for e in refs.values())

    if has_subsections:
        subsection_order = []
        seen_subs = set()
        for old_num in sorted(refs.keys(), key=lambda n: refs[n].line_idx):
            sub = refs[old_num].subsection
            if sub not in seen_subs:
                seen_subs.add(sub)
                subsection_order.append(sub)

        for sub in subsection_order:
            sub_positions = sorted(
                e.line_idx for e in refs.values() if e.subsection == sub)
            sub_active = sorted(
                n for n, entry in active_entries.items()
                if entry.subsection == sub)
            sub_orphans = sorted(
                n for n, entry in orphan_entries.items()
                if entry.subsection == sub)
            sub_nums = sub_active + sub_orphans

            for pos, new_num in zip(sub_positions, sub_nums):
                entry_obj = all_numbered[new_num][0]
                result[pos] = f'[{new_num}] {entry_obj.text}\n'
    else:
        all_positions = sorted(e.line_idx for e in refs.values())
        all_nums = sorted(active_entries.keys()) + sorted(orphan_entries.keys())

        for pos, new_num in zip(all_positions, all_nums):
            entry_obj = all_numbered[new_num][0]
            result[pos] = f'[{new_num}] {entry_obj.text}\n'

    return result


def _safe_insert_pos(refs: dict[int, RefEntry], refs_end: int) -> int:
    """Return the line index where new ref entries should be inserted.

    Uses one line after the last known ref entry, falling back to
    refs_end when no entries exist.  This avoids inserting entries
    after horizontal rules or other non-reference content that may
    appear between the last entry and the section boundary.
    """
    if refs:
        return max(e.line_idx for e in refs.values()) + 1
    return refs_end


def remove_orphan_refs(
    lines: list[str],
    orphans: list[int],
    refs: dict[int, RefEntry],
) -> list[str]:
    """Blank out lines for orphan reference entries."""
    result = list(lines)
    for num in orphans:
        if num in refs:
            result[refs[num].line_idx] = '\n'
    return result


def add_missing_ref_entries(
    lines: list[str],
    missing: list[int],
    body_cites: list[tuple[int, int]],
    refs_end: int,
    resolved: ResolveResult,
    refs: dict[int, RefEntry] | None = None,
) -> list[str]:
    """Create reference entries for citations that have no ref entry."""
    if not missing:
        return list(lines)

    result = list(lines)
    cite_contexts = {}
    for line_idx, num in body_cites:
        if num not in cite_contexts:
            cite_contexts[num] = line_idx

    new_entries = []
    for num in missing:
        ctx_line = cite_contexts.get(num, -1)
        entry_text = None

        if ctx_line >= 0:
            line = result[ctx_line]
            for m in LINK_RE.finditer(line):
                link_end = m.end()
                after = line[link_end:]
                if after.startswith(f'<sup>[{num}]</sup>'):
                    url = m.group(2)
                    text = m.group(1)
                    resolved_url = (
                        resolved.url_map.get(url)
                        or resolved.url_map.get(url.lower())
                        or url)
                    info = extract_paper_id_from_url(resolved_url)
                    if info:
                        pid, _year = info
                        meta = resolved.metadata.get(pid.upper())
                        if meta:
                            t = to_html_entities(meta.title)
                            a = to_html_entities(meta.authors)
                            year = meta.date[:4] if meta.date else ''
                            if year:
                                entry_text = (
                                    f'[{meta.paper_id}]({meta.url}) - '
                                    f'"{t}" ({a}, {year}).')
                            else:
                                entry_text = (
                                    f'[{meta.paper_id}]({meta.url}) - '
                                    f'"{t}" ({a}).')
                            break
                    entry_text = f'[{text}]({resolved_url})'
                    break

        if entry_text is None:
            entry_text = '[TODO: Add reference]'
            print(f"  Stub:    [{num}] {entry_text} "
                  f"(line {ctx_line + 1})", file=sys.stderr)
        else:
            print(f"  Created: [{num}] {entry_text}", file=sys.stderr)

        new_entries.append(f'[{num}] {entry_text}\n')

    if new_entries:
        insert_pos = _safe_insert_pos(refs or {}, refs_end)
        for entry_line in new_entries:
            result.insert(insert_pos, '\n')
            result.insert(insert_pos + 1, entry_line)
            insert_pos += 2

    return result


def add_citations_to_links(
    lines: list[str],
    uncited_links: list[tuple[int, str, str]],
    refs: dict[int, RefEntry],
    refs_end: int,
    resolved: ResolveResult,
) -> tuple[list[str], dict[int, RefEntry]]:
    """Attach <sup>[N]</sup> to uncited links and create ref entries."""
    result = list(lines)
    new_refs = dict(refs)
    next_num = (max(refs.keys()) + 1) if refs else 1

    url_to_ref = {}
    for num, entry in refs.items():
        for m in re.finditer(r'https?://[^\s,)]+', entry.text):
            url_to_ref[m.group(0)] = num

    inserts = []

    for line_idx, text, url in uncited_links:
        link_pattern = f'[{text}]({url})'
        line = result[line_idx]
        pos = line.find(link_pattern)
        if pos >= 0:
            insert_at = pos + len(link_pattern)
            after = line[insert_at:]
            if after.lstrip().startswith('<sup>['):
                continue

        resolved_url = (
            resolved.url_map.get(url)
            or resolved.url_map.get(url.lower())
            or url)
        existing = url_to_ref.get(url) or url_to_ref.get(resolved_url)
        if existing is not None:
            ref_num = existing
        else:
            ref_num = next_num
            next_num += 1
            info = extract_paper_id_from_url(resolved_url)
            meta = None
            if info:
                pid, _year = info
                meta = resolved.metadata.get(pid.upper())

            if meta:
                t = to_html_entities(meta.title)
                a = to_html_entities(meta.authors)
                year = meta.date[:4] if meta.date else ''
                if year:
                    entry_text = (
                        f'[{meta.paper_id}]({meta.url}) - '
                        f'"{t}" ({a}, {year}).')
                else:
                    entry_text = (
                        f'[{meta.paper_id}]({meta.url}) - '
                        f'"{t}" ({a}).')
            else:
                entry_text = f'[{text}]({resolved_url})'

            new_refs[ref_num] = RefEntry(
                number=ref_num, text=entry_text,
                line_idx=-1, format='A',
            )
            url_to_ref[url] = ref_num

            inserts.append(f'[{ref_num}] {entry_text}\n')

            print(f"  Created: [{ref_num}] {entry_text}", file=sys.stderr)

        if pos >= 0:
            insert_at = pos + len(link_pattern)
            result[line_idx] = (
                line[:insert_at]
                + f'<sup>[{ref_num}]</sup>'
                + line[insert_at:])

    if inserts:
        insert_pos = _safe_insert_pos(refs, refs_end)
        for entry_line in inserts:
            result.insert(insert_pos, '\n')
            result.insert(insert_pos + 1, entry_line)
            insert_pos += 2

    return result, new_refs


def _resolve_paper_version(
    paper: str,
    url: Optional[str],
    ref_entry: Optional[RefEntry],
    resolved: ResolveResult,
) -> tuple[Optional[str], Optional[str]]:
    """Return (versioned_id, diagnostic) for a bare paper number.

    Sources version from URL and ref entry, checking for agreement.
    Falls back to resolved.metadata when both are unversioned.
    """
    url_version = None
    if url:
        info = extract_paper_id_from_url(url)
        if info:
            pid, _year = info
            m = REVISION_RE.match(pid)
            if m and m.group(2):
                url_version = pid

    ref_version = None
    if ref_entry:
        for m in VERSIONED_PAPER_RE.finditer(ref_entry.text):
            if m.group(0)[:5] == paper[:5]:
                ref_version = m.group(0)
                break
        if ref_version is None:
            for url_m in re.finditer(r'https?://[^\s,)]+', ref_entry.text):
                info = extract_paper_id_from_url(url_m.group(0))
                if info:
                    pid, _ = info
                    rev_m = REVISION_RE.match(pid)
                    if rev_m and rev_m.group(2) and pid[:5] == paper[:5]:
                        ref_version = pid
                        break

    if url_version and ref_version:
        if url_version == ref_version:
            return url_version, None
        return None, (
            f"URL version {url_version} disagrees with "
            f"ref version {ref_version} for {paper}")

    if url_version:
        return url_version, None
    if ref_version:
        return ref_version, None

    for pid, meta in resolved.metadata.items():
        if pid.startswith(paper):
            return meta.paper_id, None

    return None, (f"no version source for {paper} "
                  f"(no versioned URL, ref text, or metadata)")


def _in_quoted_string(line: str, pos: int) -> bool:
    """Check if a position in a line is inside double quotes."""
    quote_count = 0
    for i in range(pos):
        if line[i] == '"':
            quote_count += 1
    return quote_count % 2 == 1


def fix_unversioned_refs(
    lines: list[str],
    unversioned: list[tuple[int, str]],
    refs: dict[int, RefEntry],
    resolved: ResolveResult,
) -> list[str]:
    """Replace bare paper numbers with versioned equivalents.

    Sources version from the URL and reference entry, checking for
    agreement.  Skips bare numbers inside quoted strings (paper titles).
    """
    result = list(lines)

    for line_idx, paper in unversioned:
        line = result[line_idx]
        m = re.search(rf'\b{re.escape(paper)}\b(?!R\d)', line)
        if not m:
            continue

        if _in_quoted_string(line, m.start()):
            continue

        url_ctx = None
        for link_m in LINK_RE.finditer(line):
            if link_m.start() <= m.start() < link_m.end():
                url_ctx = link_m.group(2)
                break

        ref_ctx = None
        fwd_m = re.search(r'<sup>\[(\d+)\]</sup>', line[m.end():])
        bwd_matches = list(
            re.finditer(r'<sup>\[(\d+)\]</sup>', line[:m.start()]))
        bwd_m = bwd_matches[-1] if bwd_matches else None

        sup_m = None
        if fwd_m and bwd_m:
            fwd_dist = fwd_m.start()
            bwd_dist = m.start() - bwd_m.end()
            sup_m = fwd_m if fwd_dist <= bwd_dist else bwd_m
        elif fwd_m:
            sup_m = fwd_m
        elif bwd_m:
            sup_m = bwd_m

        if sup_m:
            cite_num = int(sup_m.group(1))
            ref_ctx = refs.get(cite_num)

        used_fallback = False
        if ref_ctx is None:
            for _num, entry in refs.items():
                for vm in VERSIONED_PAPER_RE.finditer(entry.text):
                    if vm.group(0)[:5] == paper[:5]:
                        ref_ctx = entry
                        break
                if ref_ctx:
                    break
            if ref_ctx is not None:
                used_fallback = True

        if used_fallback and url_ctx is None:
            print(f"  Skipping: {paper} in prose without citation "
                  f"context (line {line_idx + 1})", file=sys.stderr)
            continue

        versioned, diag = _resolve_paper_version(
            paper, url_ctx, ref_ctx, resolved)

        if versioned:
            result[line_idx] = re.sub(
                rf'\b{re.escape(paper)}\b(?!R\d)',
                versioned,
                result[line_idx],
                count=1)
            print(f"  Versioned: {paper} -> {versioned} "
                  f"(line {line_idx + 1})", file=sys.stderr)
        elif diag:
            print(f"  Warning: {diag} (line {line_idx + 1})",
                  file=sys.stderr)

    return result


def normalize_title(text: str) -> str:
    """Normalize a title for comparison."""
    text = text.strip().strip('"').strip("'").strip('`')
    text = text.rstrip(',').rstrip('.')
    text = re.sub(r'\s+', ' ', text)
    return text.lower()


def _edit_distance(a: str, b: str) -> int:
    """Levenshtein edit distance between two strings."""
    if len(a) < len(b):
        return _edit_distance(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            curr.append(min(
                curr[j] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
    return prev[len(b)]


def fix_title_mismatches(
    lines: list[str],
    refs: dict[int, RefEntry],
    resolved: ResolveResult,
) -> list[str]:
    """Update reference titles from mailing index metadata.

    Applies confidence checks before replacing:
    - Skips if SequenceMatcher ratio < 0.3 (titles too different,
      index data likely wrong).
    - Skips if edit distance <= 2 (author's deliberate minor
      correction, e.g. fixing a typo in the published title).
    """
    from difflib import SequenceMatcher

    result = list(lines)

    for num, entry in refs.items():
        urls_in_text = re.findall(r'https?://[^\s,]+', entry.text)
        for url in urls_in_text:
            info = extract_paper_id_from_url(url)
            if not info:
                continue
            pid, _year = info
            meta = resolved.metadata.get(pid.upper())
            if not meta:
                continue

            ref_title = None
            title_m = re.search(r'"([^"]+)"', entry.text)
            if title_m:
                ref_title = title_m.group(1)
            else:
                title_m = re.search(r',\s*([^,]+),', entry.text)
                if title_m:
                    ref_title = title_m.group(1).strip()

            if ref_title is None:
                continue

            if (normalize_title(ref_title)
                    != normalize_title(meta.title)):
                body_text = ''.join(result[:entry.line_idx])
                if ref_title in body_text:
                    print(
                        f"  Title SKIP [{num}] {pid} "
                        f"(title appears in body text, "
                        f"preserving consistency):\n"
                        f"    Reference: \"{ref_title}\"\n"
                        f"    Index:     \"{meta.title}\"",
                        file=sys.stderr)
                    break

                ratio = SequenceMatcher(
                    None,
                    normalize_title(ref_title),
                    normalize_title(meta.title),
                ).ratio()
                if ratio < 0.3:
                    print(
                        f"  Title SKIP [{num}] {pid} "
                        f"(ratio {ratio:.2f}, likely wrong index data):\n"
                        f"    Reference: \"{ref_title}\"\n"
                        f"    Index:     \"{meta.title}\"",
                        file=sys.stderr)
                    break

                dist = _edit_distance(
                    normalize_title(ref_title),
                    normalize_title(meta.title))
                if dist <= 2:
                    print(
                        f"  Title SKIP [{num}] {pid} "
                        f"(edit distance {dist}, preserving author correction):\n"
                        f"    Reference: \"{ref_title}\"\n"
                        f"    Index:     \"{meta.title}\"",
                        file=sys.stderr)
                    break

                print(
                    f"  Title mismatch [{num}] {pid} "
                    f"(not modified; reference title is authoritative):\n"
                    f"    Reference: \"{ref_title}\"\n"
                    f"    Index:     \"{meta.title}\"",
                    file=sys.stderr)
            break

    for num, entry in refs.items():
        urls_in_text = re.findall(r'https?://[^\s,]+', entry.text)
        for url in urls_in_text:
            info = extract_paper_id_from_url(url)
            if not info:
                continue
            pid, _year = info
            meta = resolved.metadata.get(pid.upper())
            if not meta or not meta.authors:
                continue

            paren_m = re.search(r'\(([^)]+)\)\s*\.?\s*$', entry.text)
            if not paren_m:
                continue
            paren_content = paren_m.group(1)

            if 'ed.' in paren_content:
                break
            if 'et al' in paren_content:
                break

            year_m = re.search(r',?\s*(\d{4})\s*$', paren_content)
            if year_m:
                ref_author = paren_content[:year_m.start()].strip()
            else:
                ref_author = paren_content.strip()

            if not ref_author or ref_author.startswith('http'):
                break

            index_author = to_html_entities(meta.authors)

            ref_parts = set(
                p.strip().split()[-1].lower()
                for p in ref_author.split(',')
                if p.strip() and not re.match(r'^\d{4}$', p.strip()))
            idx_parts = set(
                p.strip().split()[-1].lower()
                for p in index_author.split(',')
                if p.strip())

            if ref_parts and idx_parts and ref_parts & idx_parts:
                break

            if ref_author == index_author:
                break

            body_text = ''.join(result[:entry.line_idx])
            if ref_author in body_text:
                print(
                    f"  Author SKIP [{num}] {pid} "
                    f"(author appears in body text):\n"
                    f"    Reference: \"{ref_author}\"\n"
                    f"    Index:     \"{index_author}\"",
                    file=sys.stderr)
                break

            year_suffix = year_m.group(0) if year_m else ''
            new_paren = f'({index_author}{year_suffix})'
            old_paren = paren_m.group(0)
            old_line = result[entry.line_idx]
            new_line = old_line.replace(old_paren, new_paren + '.', 1)
            if old_paren.endswith('.'):
                new_line = old_line.replace(old_paren, new_paren + '.', 1)
            else:
                new_line = old_line.replace(old_paren, new_paren, 1)
            if new_line != old_line:
                result[entry.line_idx] = new_line
                print(
                    f"  Author fix [{num}] {pid}:\n"
                    f"    Was:  \"{ref_author}\"\n"
                    f"    Now:  \"{index_author}\"",
                    file=sys.stderr)
            break

    return result


def demote_h1_refs(lines: list[str], refs_start: int) -> list[str]:
    """Demote # References to ## References."""
    result = list(lines)
    new_line = re.sub(
        r'^#(\s+)References', r'##\1References', result[refs_start])
    if new_line != result[refs_start]:
        result[refs_start] = new_line
        print(f"  Demoted: # References -> ## References "
              f"(line {refs_start + 1})", file=sys.stderr)
    return result


def normalize_ref_format(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> list[str]:
    """Convert Format B (N. text) to Format A ([N] text) in refs section."""
    result = list(lines)
    for i in range(refs_start + 1, refs_end):
        m = REF_FORMAT_B_RE.match(result[i].strip())
        if m:
            num = m.group(1)
            text = m.group(2)
            leading = ''
            stripped = result[i].lstrip()
            if result[i] != stripped:
                leading = result[i][:len(result[i]) - len(stripped)]
            result[i] = f'{leading}[{num}] {text}\n'
    return result


def strip_trailing_urls(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> list[str]:
    """Remove redundant trailing bare URLs from ref lines.

    If a line has [text](url) and ends with the same bare url, drop it.
    If a line has a bare URL but no markdown link, wrap the descriptive
    text before the URL as a link.
    """
    result = list(lines)
    for i in range(refs_start + 1, refs_end):
        line = result[i]
        stripped = line.strip()
        if not stripped:
            continue

        links = list(LINK_RE.finditer(stripped))
        urls_in_line = re.findall(r'https?://\S+', stripped)

        if not urls_in_line:
            continue

        if links:
            link_urls = {m.group(2) for m in links}
            trailing_m = TRAILING_URL_RE.search(line.rstrip('\n'))
            if trailing_m:
                trailing_url = trailing_m.group(0).strip()
                if trailing_url in link_urls:
                    new_line = line[:trailing_m.start()].rstrip()
                    result[i] = new_line + '\n'
        else:
            if len(urls_in_line) == 1:
                url = urls_in_line[0]
                ref_m = REF_FORMAT_A_RE.match(stripped)
                if ref_m:
                    text = ref_m.group(2)
                    url_pos = text.find(url)
                    if url_pos > 0:
                        desc = text[:url_pos].rstrip(', .')
                        if desc:
                            num = ref_m.group(1)
                            result[i] = (
                                f'[{num}] [{desc}]({url})\n')

    return result


def space_ref_entries(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> list[str]:
    """Ensure a blank line between consecutive reference entries."""
    result = list(lines)
    inserts = []
    for i in range(refs_start + 1, refs_end):
        stripped = result[i].strip()
        if not REF_FORMAT_A_RE.match(stripped):
            continue
        if i > 0:
            prev = result[i - 1].strip()
            if prev and not prev.startswith('#'):
                inserts.append(i)

    for offset, pos in enumerate(inserts):
        result.insert(pos + offset, '\n')

    return result


def unify_duplicate_refs(lines: list[str], refs_start: int, refs_end: int) -> list[str]:
    """Merge reference entries that point to the same paper URL.

    When two entries share the same paper identifier (via
    extract_paper_id_from_url), the entry with the longer text
    (more metadata) is kept and the other's body citations are
    rewritten to the kept number.
    """
    refs = parse_references(lines, refs_start, refs_end)
    pid_to_nums: dict[str, list[int]] = {}
    for num, entry in refs.items():
        for url_m in re.finditer(r'https?://[^\s,)]+', entry.text):
            info = extract_paper_id_from_url(url_m.group(0))
            if info:
                pid, _ = info
                pid_to_nums.setdefault(pid, []).append(num)
                break

    remap: dict[int, int] = {}
    remove_lines: set[int] = set()
    for pid, nums in pid_to_nums.items():
        if len(nums) < 2:
            continue
        keep = max(nums, key=lambda n: len(refs[n].text))
        for n in nums:
            if n != keep:
                remap[n] = keep
                remove_lines.add(refs[n].line_idx)

    if not remap:
        return list(lines)

    result = list(lines)
    excluded = build_exclusion_ranges(result)
    for i, line in enumerate(result):
        if i in excluded:
            continue
        for old, new in sorted(remap.items()):
            result[i] = result[i].replace(
                f'<sup>[{old}]</sup>', f'<sup>[{new}]</sup>')
    for idx in remove_lines:
        result[idx] = '\n'

    return result


def remove_empty_subsection_headings(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> list[str]:
    """Remove subsection headings that have no ref entries beneath them."""
    result = list(lines)

    hdr = result[refs_start].strip()
    refs_level = hdr.count(
        '#', 0, hdr.index(' ') if ' ' in hdr else len(hdr))

    heading_indices = []
    for i in range(refs_start + 1, min(refs_end, len(result))):
        stripped = result[i].strip()
        sub_m = HEADING_RE.match(stripped)
        if sub_m and len(sub_m.group(1)) > refs_level:
            heading_indices.append(i)

    to_blank = set()
    for idx, h_line in enumerate(heading_indices):
        next_boundary = heading_indices[idx + 1] if idx + 1 < len(heading_indices) else min(refs_end, len(result))
        has_entry = False
        for j in range(h_line + 1, next_boundary):
            if REF_FORMAT_A_RE.match(result[j].strip()):
                has_entry = True
                break
        if not has_entry:
            to_blank.add(h_line)

    for i in to_blank:
        result[i] = '\n'

    return result


def collapse_ref_blanks(
    lines: list[str],
    refs_start: int,
    refs_end: int,
) -> list[str]:
    """Reduce runs of 2+ consecutive blank lines to one in refs section."""
    result = list(lines)
    i = refs_start + 1
    limit = min(refs_end, len(result))
    while i < limit:
        if (result[i].strip() == ''
                and i + 1 < limit
                and result[i + 1].strip() == ''):
            result.pop(i)
            limit -= 1
        else:
            i += 1
    return result


def _verify_citation_integrity(lines: list[str], filepath: str) -> None:
    """Post-write safety check: every body citation must have a ref entry."""
    excluded = build_exclusion_ranges(lines)
    refs_start, refs_end = find_refs_section(lines)
    if refs_start < 0:
        return
    _, _, cite_map = extract_body_citations(
        lines, excluded, refs_start, refs_end)
    out_refs = parse_references(lines, refs_start, refs_end)
    ref_nums = set(out_refs.keys())
    for cite_num in cite_map:
        if cite_num not in ref_nums:
            name = os.path.basename(filepath) if filepath else '<unknown>'
            print(
                f"CRITICAL: {name}: body cites [{cite_num}] "
                f"but no reference entry exists in output",
                file=sys.stderr)


def write(
    result: AuditResult,
    resolved: ResolveResult,
    fix: bool = False,
) -> str:
    """Pass 3: apply fixes and return the rewritten content."""
    lines = list(result.lines)

    if resolved.url_map and result.wg21_links:
        replacements = {}
        for link in result.wg21_links:
            url_lower = link.url.lower()
            resolved_url = (
                resolved.url_map.get(link.url)
                or resolved.url_map.get(url_lower))
            if resolved_url:
                replacements[link.url] = resolved_url
        if replacements:
            lines = apply_wg21_replacements(
                lines, replacements, result.excluded)

    refs = dict(result.refs)
    refs_start = result.refs_start
    refs_end = result.refs_end

    if fix:
        if result.refs_heading_h1 and refs_start >= 0:
            lines = demote_h1_refs(lines, refs_start)

        if refs_start >= 0:
            lines = normalize_ref_format(lines, refs_start, refs_end)
            refs = parse_references(lines, refs_start, refs_end)

        if result.orphans:
            orphans_to_remove = list(result.orphans)
            body_link_urls = set()
            if result.uncited_links:
                for _, _, url in result.uncited_links:
                    body_link_urls.add(url)
                    r_url = (resolved.url_map.get(url)
                             or resolved.url_map.get(url.lower()))
                    if r_url:
                        body_link_urls.add(r_url)
            body_end = refs_start if refs_start >= 0 else len(lines)
            for i in range(body_end):
                for lm in LINK_RE.finditer(lines[i]):
                    url = lm.group(2)
                    body_link_urls.add(url)
                    r_url = (resolved.url_map.get(url)
                             or resolved.url_map.get(url.lower()))
                    if r_url:
                        body_link_urls.add(r_url)
            if body_link_urls:
                safe = []
                for num in orphans_to_remove:
                    entry = refs.get(num)
                    if entry:
                        entry_urls = set(
                            re.findall(r'https?://[^\s,)]+', entry.text))
                        if entry_urls & body_link_urls:
                            continue
                    safe.append(num)
                orphans_to_remove = safe
            lines = remove_orphan_refs(lines, orphans_to_remove, refs)
            for num in orphans_to_remove:
                refs.pop(num, None)
            if refs_start >= 0:
                lines = remove_empty_subsection_headings(
                    lines, refs_start, refs_end)

        if result.missing:
            lines = add_missing_ref_entries(
                lines, result.missing, result.body_cites,
                refs_end, resolved, refs=refs)
            refs_end = len(lines)
            _, new_refs_end = find_refs_section(lines)
            if new_refs_end > 0:
                refs_end = new_refs_end
            refs = parse_references(
                lines,
                refs_start if refs_start >= 0 else 0,
                refs_end)

        if result.uncited_links:
            lines, refs = add_citations_to_links(
                lines, result.uncited_links, refs, refs_end,
                resolved)
            refs_start, refs_end = find_refs_section(lines)
            if refs_start >= 0:
                refs = parse_references(lines, refs_start, refs_end)

        if result.unversioned:
            lines = fix_unversioned_refs(
                lines, result.unversioned, refs, resolved)

        lines = fix_title_mismatches(lines, refs, resolved)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            lines = strip_trailing_urls(lines, refs_start, refs_end)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            lines = space_ref_entries(lines, refs_start, refs_end)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            lines = collapse_ref_blanks(lines, refs_start, refs_end)

    refs_start, refs_end = find_refs_section(lines)
    if refs_start >= 0:
        refs = parse_references(lines, refs_start, refs_end)

    has_subsections = any(e.subsection for e in refs.values()) if refs else False

    excluded = build_exclusion_ranges(lines)
    _body_cites, _first_app, old_to_new = extract_body_citations(
        lines, excluded, refs_start, refs_end)

    needs_renumber = any(old != new for old, new in old_to_new.items())

    if needs_renumber and old_to_new and has_subsections:
        current_refs = parse_references(lines, refs_start, refs_end)
        current_nums = sorted(current_refs.keys())
        if current_nums == list(range(1, len(current_nums) + 1)):
            sub_sequential = True
            seen_sub = set()
            sub_order = []
            for n in sorted(current_refs.keys(),
                            key=lambda k: current_refs[k].line_idx):
                s = current_refs[n].subsection
                if s not in seen_sub:
                    seen_sub.add(s)
                    sub_order.append(s)
            prev_max = 0
            for s in sub_order:
                s_nums = sorted(
                    n for n, e in current_refs.items()
                    if e.subsection == s)
                if s_nums and s_nums[0] <= prev_max:
                    sub_sequential = False
                    break
                if s_nums != list(range(s_nums[0],
                                        s_nums[0] + len(s_nums))):
                    sub_sequential = False
                    break
                prev_max = s_nums[-1] if s_nums else prev_max
            if sub_sequential:
                needs_renumber = False

    if needs_renumber and old_to_new:
        content = renumber_content(old_to_new, excluded, lines)
        lines = content.splitlines(keepends=True)

        if refs_start >= 0 and refs:
            lines = reorder_refs(lines, refs, old_to_new)

    refs_start, refs_end = find_refs_section(lines)
    if refs_start >= 0:
        lines = unify_duplicate_refs(lines, refs_start, refs_end)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            refs = parse_references(lines, refs_start, refs_end)
            excluded = build_exclusion_ranges(lines)
            _, _, post_map = extract_body_citations(
                lines, excluded, refs_start, refs_end)
            if any(o != n for o, n in post_map.items()):
                content = renumber_content(post_map, excluded, lines)
                lines = content.splitlines(keepends=True)
                if refs:
                    lines = reorder_refs(lines, refs, post_map)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            lines = collapse_ref_blanks(lines, refs_start, refs_end)

        refs_start, refs_end = find_refs_section(lines)
        if refs_start >= 0:
            final_refs = parse_references(lines, refs_start, refs_end)
            sub_order = []
            seen_s = set()
            for n in sorted(final_refs.keys(),
                            key=lambda k: final_refs[k].line_idx):
                s = final_refs[n].subsection
                if s not in seen_s:
                    seen_s.add(s)
                    sub_order.append(s)
            seq_map = {}
            next_seq = 1
            for s in sub_order:
                s_nums = sorted(
                    n for n, e in final_refs.items()
                    if e.subsection == s)
                for n in s_nums:
                    if n != next_seq:
                        seq_map[n] = next_seq
                    next_seq += 1
            if seq_map:
                excluded2 = build_exclusion_ranges(lines)
                full_map = {n: seq_map.get(n, n)
                            for n in final_refs}
                content = renumber_content(
                    full_map, excluded2, lines)
                lines = content.splitlines(keepends=True)
                lines = reorder_refs(
                    lines, final_refs, full_map)

    _verify_citation_integrity(lines, result.filepath)

    return ''.join(lines)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(result: AuditResult) -> None:
    """Print audit summary to stderr."""
    name = os.path.basename(result.filepath)
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"  cite: {name}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    if result.needs_renumber:
        print(f"\n  Renumbering: {len(result.old_to_new)} citations",
              file=sys.stderr)
        changes = [(old, new)
                   for old, new in sorted(result.old_to_new.items())
                   if old != new]
        for old, new in changes[:20]:
            print(f"    [{old}] -> [{new}]", file=sys.stderr)
        if len(changes) > 20:
            print(f"    ... and {len(changes) - 20} more",
                  file=sys.stderr)
    else:
        print("\n  Citations already in order.", file=sys.stderr)

    if result.orphans:
        print(f"\n  Orphan references: {result.orphans}", file=sys.stderr)

    if result.missing:
        print(f"\n  Missing references: {result.missing}", file=sys.stderr)

    by_rule = {}
    for f in result.findings:
        by_rule.setdefault(f.rule, []).append(f)

    for rule in sorted(by_rule.keys()):
        findings = by_rule[rule]
        print(f"\n  {rule} ({len(findings)}):", file=sys.stderr)
        for f in findings[:10]:
            print(f"    L{f.line}: {f.message}", file=sys.stderr)
        if len(findings) > 10:
            print(f"    ... and {len(findings) - 10} more",
                  file=sys.stderr)

    total = len(result.findings)
    if total == 0:
        print("\n  Clean.", file=sys.stderr)
    else:
        print(f"\n  Total findings: {total}", file=sys.stderr)

    print(file=sys.stderr)


# ---------------------------------------------------------------------------
# Path expansion
# ---------------------------------------------------------------------------

_SKIP_DIRS = frozenset({
    '.git', '.cache', '__pycache__', '.pytest_cache', 'node_modules',
})


def expand_paths(paths: list[str]) -> list[str]:
    """Resolve directories to .md files, pass through files as-is."""
    result = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for md in sorted(path.rglob('*.md')):
                skip = False
                for part in md.parts:
                    if part.startswith('.') or part in _SKIP_DIRS:
                        skip = True
                        break
                if not skip:
                    result.append(str(md))
        elif path.is_file():
            result.append(str(path))
        else:
            print(f"warning: skipping {p} (not a file or directory)",
                  file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Citation normalizer for WG21 papers',
    )
    parser.add_argument('papers', nargs='+',
                        help='Markdown files or directories to process')
    parser.add_argument('--fix', action='store_true',
                        help='Auto-fix all detectable issues')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print rewritten content to stdout, '
                             'no file write')
    parser.add_argument('--check', action='store_true',
                        help='Exit 1 if any changes needed (CI mode)')
    parser.add_argument('--config', default=None,
                        help='Path to YAML config')
    parser.add_argument('--no-resolve', action='store_true',
                        help='Skip HTTP URL resolution (offline mode)')
    parser.add_argument('--no-guess', action='store_true',
                        help='Do not construct URLs for papers not in '
                             'the wg21.link index')

    args = parser.parse_args()

    if args.fix and args.check:
        print("error: --fix and --check are mutually exclusive",
              file=sys.stderr)
        return 2

    files = expand_paths(args.papers)
    if not files:
        print("error: no markdown files found", file=sys.stderr)
        return 2

    config_path = args.config
    if config_path is None:
        first_dir = Path(files[0]).resolve().parent
        candidate = first_dir / 'cite.yaml'
        if candidate.exists():
            config_path = str(candidate)
        else:
            script_dir = Path(__file__).resolve().parent
            candidate = script_dir / 'cite.yaml'
            if candidate.exists():
                config_path = str(candidate)

    try:
        config = load_config(config_path)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    # Pass 1: scan
    results = []
    for f in files:
        r = scan(f, config)
        if r.refs_start < 0:
            continue
        results.append(r)

    if not results:
        print("No papers with References section found.", file=sys.stderr)
        return 0

    # Pass 2: resolve
    cache_dir = Path(__file__).resolve().parent / '.cache'
    resolved = resolve(
        results, cache_dir,
        skip_resolve=args.no_resolve,
        skip_guess=args.no_guess)

    # Pass 3: write
    any_changes = False
    for r in results:
        print_report(r)

        if args.check:
            output = write(r, resolved, fix=True)
            original = ''.join(r.lines)
            if output != original:
                any_changes = True
            continue

        output = write(r, resolved, fix=args.fix)

        if args.dry_run:
            sys.stdout.buffer.write(output.encode('utf-8'))
            continue

        original = ''.join(r.lines)
        if output == original:
            continue

        tmp_fd, tmp_path = tempfile.mkstemp(
            dir=os.path.dirname(os.path.abspath(r.filepath)),
            suffix='.tmp',
        )
        try:
            with os.fdopen(tmp_fd, 'w', encoding='utf-8',
                           newline='\n') as f:
                f.write(output)
            os.replace(tmp_path, r.filepath)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

        print(f"  Wrote: {r.filepath}", file=sys.stderr)

    if resolved.guessed:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Constructed URLs (not verified against index):",
              file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        for slug, url in sorted(resolved.guessed):
            print(f"  {slug:12s} -> {url}", file=sys.stderr)
        print(file=sys.stderr)

    if args.check:
        return 1 if any_changes else 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
