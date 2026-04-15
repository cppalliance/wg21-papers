"""Tests for lib.pdf.mono."""

from conftest import make_span, make_line, make_block
from lib.pdf.mono import is_monospace, propagate_monospace


def test_keyword_courier():
    assert is_monospace("Courier")


def test_keyword_menlo():
    assert is_monospace("Menlo-Regular")


def test_keyword_consolas():
    assert is_monospace("Consolas")


def test_keyword_source_code_pro():
    assert is_monospace("SourceCodePro")


def test_no_keyword_no_data():
    assert not is_monospace("Arial")


def test_no_keyword_no_data_unnamed():
    assert not is_monospace("Unnamed-T3")


def test_uniform_widths_and_spacings():
    widths = [10.0] * 10
    origins = [float(i * 10) for i in range(10)]
    assert is_monospace("UnknownFont", widths, origins)


def test_non_uniform_widths():
    widths = [5.0, 15.0, 5.0, 15.0, 5.0]
    origins = [0.0, 5.0, 20.0, 25.0, 40.0]
    assert not is_monospace("UnknownFont", widths, origins)


def test_fat_thin_reject():
    widths = [20.0, 8.0, 15.0]
    chars = ["M", " ", "a"]
    assert not is_monospace("UnknownFont", widths, None, chars=chars)


def test_fat_thin_accept():
    widths = [10.0, 10.0, 10.0]
    chars = ["M", " ", "i"]
    assert is_monospace("UnknownFont", widths,
                              [0.0, 10.0, 20.0], chars=chars)


def test_propagate_sets_monospace():
    m_block = make_block(["hello world"], page_num=0)
    m_block.lines[0].spans[0].font_name = "Menlo-Regular"
    m_block.lines[0].spans[0].monospace = False

    s_block = make_block(["hello world"], page_num=0)
    s_block.lines[0].spans[0].font_name = "Menlo-Regular"
    s_block.lines[0].spans[0].monospace = True

    propagate_monospace([m_block], [s_block], "arial")
    assert m_block.lines[0].spans[0].monospace is True


def test_propagate_excludes_dominant():
    m_block = make_block(["hello world"], page_num=0)
    m_block.lines[0].spans[0].font_name = "Menlo-Regular"
    m_block.lines[0].spans[0].monospace = False

    s_block = make_block(["hello world"], page_num=0)
    s_block.lines[0].spans[0].font_name = "Menlo-Regular"
    s_block.lines[0].spans[0].monospace = True

    propagate_monospace([m_block], [s_block], "menlo-regular")
    assert m_block.lines[0].spans[0].monospace is False
