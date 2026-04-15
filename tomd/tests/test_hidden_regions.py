
"""Tests for hidden region detection and stripping in lib.pdf.cleanup."""
from unittest.mock import MagicMock

import pytest

from lib.pdf.cleanup import find_hidden_regions, strip_hidden_blocks
from lib.pdf.types import Block, Line, Span


# ---- find_hidden_regions -------------------------------------------------

def _span_record(font, color, char_bboxes, span_type=1):
    """Build a texttrace-shaped span record."""
    return {
        "type": span_type,
        "font": font,
        "color": color,
        "chars": [(None, None, None, bb) for bb in char_bboxes],
    }


def test_find_hidden_regions_no_body_fonts_returns_empty():
    """When body_fonts is None, the function short-circuits."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", 0x808080, [(10, 10, 20, 20)])
    ]
    assert find_hidden_regions(page, body_fonts=None) == set()


def test_find_hidden_regions_roboto_non_black():
    """Roboto font + non-black color + not-in-body-fonts -> hidden."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", 0x808080, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert (10, 10, 20, 20) in result


def test_find_hidden_regions_google_font():
    """Google-prefixed font triggers detection."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("GoogleSans-Regular", 0x808080, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert (10, 10, 20, 20) in result


def test_find_hidden_regions_material_font():
    """Material UI font triggers detection."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("MaterialIcons", 0x808080, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert (10, 10, 20, 20) in result


def test_find_hidden_regions_body_font_not_hidden():
    """A font that IS in body_fonts is not classified as hidden, even if
    it coincidentally matches a widget keyword."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", 0x808080, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"roboto"})
    assert result == set()


def test_find_hidden_regions_black_color_not_hidden():
    """Non-body-font, Roboto, but BLACK color -> not hidden (rule: non-black)."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", 0, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert result == set()


def test_find_hidden_regions_black_tuple_color_not_hidden():
    """The (0, 0, 0) tuple form of black is also recognized."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", (0, 0, 0), [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert result == set()


def test_find_hidden_regions_non_widget_font_not_hidden():
    """A non-body font that isn't Roboto/Google/Material is left alone."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("SomeOtherFont", 0x808080, [(10, 10, 20, 20)])
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert result == set()


def test_find_hidden_regions_mode_3_skipped():
    """Rendering mode 3 (invisible text) is explicitly ignored by the function."""
    page = MagicMock()
    page.get_texttrace.return_value = [
        _span_record("Roboto", 0x808080, [(10, 10, 20, 20)], span_type=3),
    ]
    result = find_hidden_regions(page, body_fonts={"cambria"})
    assert result == set()


# ---- strip_hidden_blocks -------------------------------------------------

def _make_block(text, x0, y0, x1, y1):
    span = Span(
        text=text, font_name="Body", font_size=11.0,
        bbox=(x0, y0, x1, y1),
    )
    line = Line(spans=[span], bbox=(x0, y0, x1, y1))
    return Block(lines=[line], bbox=(x0, y0, x1, y1))


def test_strip_hidden_blocks_empty_hidden_set_returns_input():
    """No hidden bboxes -> input blocks returned unchanged."""
    block = _make_block("visible text", 10, 10, 100, 30)
    assert strip_hidden_blocks([block], set()) == [block]


def test_strip_hidden_blocks_drops_block_entirely_in_hidden():
    """A block whose only span overlaps a hidden bbox is dropped."""
    block = _make_block("widget text", 10, 10, 100, 30)
    hidden = {(5.0, 5.0, 150.0, 50.0)}  # engulfs the block
    result = strip_hidden_blocks([block], hidden)
    assert result == []


def test_strip_hidden_blocks_keeps_block_outside_hidden():
    """A block whose span is outside all hidden bboxes survives."""
    block = _make_block("body text", 10, 300, 100, 320)
    hidden = {(5.0, 5.0, 150.0, 50.0)}  # hidden at y=5..50; block at y=300 untouched
    result = strip_hidden_blocks([block], hidden)
    assert result == [block]


def test_strip_hidden_blocks_keeps_block_with_any_visible_span():
    """A block with one hidden span and one visible span is kept."""
    hidden_span = Span(
        text="widget", font_name="Roboto", font_size=11.0,
        bbox=(10, 10, 50, 30),
    )
    visible_span = Span(
        text="content", font_name="Body", font_size=11.0,
        bbox=(60, 10, 150, 30),
    )
    line = Line(spans=[hidden_span, visible_span], bbox=(10, 10, 150, 30))
    block = Block(lines=[line], bbox=(10, 10, 150, 30))
    hidden = {(5.0, 5.0, 55.0, 35.0)}  # covers hidden_span only
    result = strip_hidden_blocks([block], hidden)
    assert result == [block]