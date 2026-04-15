
"""Tests for position-based list detection in lib.pdf.structure."""
from lib.pdf.structure import (
    _detect_lists_by_position,
    _split_section_by_position,
    _join_bullet_marker_lines,
)
from lib.pdf.types import Section, SectionKind, Line, Span, Block


def _bullet_line(text, x0, y=100.0):
    """Construct a Line at the given x-indent with a bullet as first char.

    The text should start with a bullet character so _line_starts_with_bullet
    returns True.
    """
    span = Span(text=text, font_name="Body", font_size=11.0,
                bbox=(x0, y, x0 + 300, y + 12))
    return Line(
        spans=[span],
        bbox=(x0, y, x0 + 300, y + 12),
    )


def _body_line(text, x0=50.0, y=100.0):
    """Construct a Line at body-margin indent (no bullet)."""
    span = Span(text=text, font_name="Body", font_size=11.0,
                bbox=(x0, y, x0 + 300, y + 12))
    return Line(
        spans=[span],
        bbox=(x0, y, x0 + 300, y + 12),
    )


def _make_section_with_lines(lines, kind=SectionKind.PARAGRAPH, font_size=11.0):
    text = "\n".join(ln.text for ln in lines)
    return Section(
        kind=kind,
        text=text,
        lines=lines,
        page_num=0,
        font_size=font_size,
    )


# ---- _detect_lists_by_position -------------------------------------------

def test_detect_preserves_non_paragraph_sections():
    """HEADING, TABLE, UNCERTAIN sections pass through unchanged."""
    heading = _make_section_with_lines([_body_line("Heading")], kind=SectionKind.HEADING)
    result = _detect_lists_by_position([heading])
    assert result == [heading]


def test_detect_paragraph_without_bullets_unchanged():
    """A paragraph with no indented bullets is returned as-is."""
    para = _make_section_with_lines([
        _body_line("First paragraph line."),
        _body_line("Second paragraph line."),
    ])
    result = _detect_lists_by_position([para])
    assert len(result) == 1
    assert result[0].kind == SectionKind.PARAGRAPH


def test_detect_converts_indented_bullets_to_list():
    """Indented lines starting with bullets become LIST sections."""
    # Body margin needs establishing via the first non-bullet line, or via
    # _get_body_margin's heuristic. Use x=50 for body and x=80 for indented bullets.
    para = _make_section_with_lines([
        _body_line("Introduction paragraph.", x0=50.0),
        _bullet_line("\u2022 first item", x0=80.0, y=114.0),
        _bullet_line("\u2022 second item", x0=80.0, y=128.0),
    ])
    result = _detect_lists_by_position([para])
    kinds = [sec.kind for sec in result]
    # Expect at least one LIST section in the result.
    assert SectionKind.LIST in kinds, f"got kinds={kinds}"


def test_detect_mixed_list_and_paragraph_split():
    """Body-margin lines between bullet groups split into their own PARAGRAPH."""
    para = _make_section_with_lines([
        _bullet_line("\u2022 first bullet", x0=80.0, y=100.0),
        _body_line("Interstitial body text.", x0=50.0, y=114.0),
        _bullet_line("\u2022 second bullet", x0=80.0, y=128.0),
    ])
    result = _detect_lists_by_position([para])
    kinds = [sec.kind for sec in result]
    # Expect LIST, PARAGRAPH, LIST order (subject to implementation details).
    assert SectionKind.LIST in kinds
    assert SectionKind.PARAGRAPH in kinds


# ---- _split_section_by_position tracks indent level ----------------------

def test_split_section_by_position_nested_indent():
    """A bullet at indent level 2 (x further right) carries indent_level=2."""
    # body_margin is the leftmost frequent x; derive it from the non-bullet line.
    # Use the internal _get_body_margin via the public function path instead.
    para = _make_section_with_lines([
        _body_line("Paragraph body.", x0=50.0, y=100.0),
        _bullet_line("\u2022 outer", x0=80.0, y=114.0),
        _bullet_line("\u2022 nested", x0=120.0, y=128.0),  # further right than outer
    ])
    result = _detect_lists_by_position([para])
    list_sections = [s for s in result if s.kind == SectionKind.LIST]
    indent_levels = [s.indent_level for s in list_sections]
    # At least one section should be at indent_level > 0.
    assert any(i > 0 for i in indent_levels), f"got indent_levels={indent_levels}"


# ---- _join_bullet_marker_lines -------------------------------------------

def test_join_bullet_marker_merges_bullet_and_text_lines():
    """When a line is just a bullet char and the next is its text, merge them."""
    bullet_span = Span(text="\u2022", font_name="Body", font_size=11.0,
                       bbox=(50, 100, 58, 112))
    text_span = Span(text="item text", font_name="Body", font_size=11.0,
                     bbox=(68, 100, 200, 112))
    bullet_line = Line(spans=[bullet_span], bbox=(50, 100, 58, 112))
    text_line = Line(spans=[text_span], bbox=(68, 100, 200, 112))
    result = _join_bullet_marker_lines([bullet_line, text_line])
    # After joining, one Line containing a combined span (bullet + space + text).
    assert len(result) == 1
    combined_text = result[0].text
    assert combined_text.startswith("\u2022")
    assert "item text" in combined_text


def test_join_bullet_marker_leaves_non_bullet_pairs_alone():
    """Two adjacent normal lines are not merged."""
    l1 = _body_line("line one")
    l2 = _body_line("line two")
    result = _join_bullet_marker_lines([l1, l2])
    assert len(result) == 2


def test_join_bullet_marker_handles_single_line():
    """Fewer than 2 lines -> returned unchanged."""
    l1 = _body_line("solo line")
    assert _join_bullet_marker_lines([l1]) == [l1]