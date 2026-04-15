
"""Tests for header/footer detection and stripping in lib.pdf.cleanup."""
from lib.pdf.cleanup import get_edge_items, detect_repeating, strip_repeating
from lib.pdf.types import (
    Block, Line, Span, PageEdgeItem, Y_TOLERANCE, EDGE_ITEMS_PER_PAGE,
)


def _make_line(text, y, page_num=0, x0=50.0, x1=550.0):
    """Construct a Line with a single span at the given y position."""
    return Line(
        spans=[Span(text=text, font_name="Body", font_size=11.0)],
        bbox=(x0, y, x1, y + 12.0),
        page_num=page_num,
    )


def _make_block_at_y(lines_data, page_num=0):
    """Build a Block whose bbox spans its lines."""
    lines = [_make_line(t, y, page_num=page_num) for t, y in lines_data]
    ys = [ln.bbox[1] for ln in lines]
    y2s = [ln.bbox[3] for ln in lines]
    return Block(
        lines=lines,
        bbox=(50.0, min(ys), 550.0, max(y2s)),
        page_num=page_num,
    )


# ---- get_edge_items ------------------------------------------------------

def test_edge_items_picks_top_and_bottom():
    """Top 3 and bottom 3 by y-coordinate, with no dedup needed when texts differ."""
    # Lines at y = 30, 60, 90 (top half) and 500, 540, 580 (bottom half).
    block_top = _make_block_at_y([("Header A", 30), ("Header B", 60), ("Header C", 90)])
    block_body = _make_block_at_y([("body line", 300)])
    block_bot = _make_block_at_y([("Footer X", 500), ("Footer Y", 540), ("Footer Z", 580)])
    items = get_edge_items([block_top, block_body, block_bot], page_num=1, page_height=600)
    texts = [it.text for it in items]
    # Top 3 by y (ascending): Header A/B/C. Bottom 3 by y (largest): Footer X/Y/Z
    # (and possibly body line too — the function takes items[:3] and items[-3:]).
    assert "Header A" in texts
    assert "Header B" in texts
    assert "Header C" in texts
    assert "Footer X" in texts or "Footer Y" in texts  # bottom range
    assert "Footer Z" in texts


def test_edge_items_dedups_same_text_same_y():
    """Duplicate (text, y) pairs collapse to a single edge item."""
    # Two blocks contribute lines with identical text at identical y — dedup.
    b1 = _make_block_at_y([("Page 1", 30)])
    b2 = _make_block_at_y([("Page 1", 30)])
    items = get_edge_items([b1, b2], page_num=1, page_height=600)
    texts = [it.text for it in items]
    assert texts.count("Page 1") == 1


def test_edge_items_empty_page():
    assert get_edge_items([], page_num=1, page_height=600) == []


def test_edge_items_skips_blank_lines():
    """Lines whose text is empty after strip are not edge items."""
    b = _make_block_at_y([("   ", 30), ("Real header", 60)])
    items = get_edge_items([b], page_num=1, page_height=600)
    texts = [it.text for it in items]
    assert texts == ["Real header"]


def test_edge_items_limits_per_page():
    """No more than EDGE_ITEMS_PER_PAGE top + EDGE_ITEMS_PER_PAGE bottom."""
    # 10 lines spread across y.
    lines_data = [(f"line {i}", 20.0 + i * 30) for i in range(10)]
    b = _make_block_at_y(lines_data)
    items = get_edge_items([b], page_num=1, page_height=600)
    # Top 3 + bottom 3 = 6; dedup only when keys collide.
    assert len(items) <= 2 * EDGE_ITEMS_PER_PAGE


# ---- detect_repeating ----------------------------------------------------

def test_detect_repeating_exact_text():
    """Same text at same y on >=50% of pages is classified as repeating."""
    # 5 pages, 4 of them have "Running Head" at y=30.
    all_edges = [
        [PageEdgeItem(text="Running Head", y=30.0, page_num=pg, bbox=(0, 30, 100, 42))]
        for pg in range(1, 5)
    ] + [
        [PageEdgeItem(text="Unique Title", y=30.0, page_num=5, bbox=(0, 30, 100, 42))],
    ]
    result = detect_repeating(all_edges, total_pages=5)
    print(all_edges)
    # y_bucket = round(30 / Y_TOLERANCE) * Y_TOLERANCE = 30.0 (Y_TOLERANCE is 2.0)
    assert (30.0, "Running Head") in result


def test_detect_repeating_skips_below_threshold():
    """If an item appears on fewer than threshold pages, it's not repeating."""
    # 5 pages, only 1 has "Not Repeating" at y=30.
    all_edges = [
        [PageEdgeItem(text="Not Repeating", y=30.0, page_num=1, bbox=(0, 30, 100, 42))],
        [], [], [], [],
    ]
    result = detect_repeating(all_edges, total_pages=5)
    assert not any(p == "Not Repeating" for _, p in result)


def test_detect_repeating_short_doc_returns_empty():
    """Fewer than 3 pages -> empty set (threshold 0.5 of 2 = 1, but function
    requires total_pages >= 3)."""
    all_edges = [[PageEdgeItem(text="Header", y=30.0, page_num=1, bbox=(0, 30, 100, 42))]]
    assert detect_repeating(all_edges, total_pages=1) == set()
    assert detect_repeating(all_edges * 2, total_pages=2) == set()


def test_detect_repeating_page_number_pattern():
    """Different page numbers at same y are classified as __PAGE_NUM__."""
    all_edges = [
        [PageEdgeItem(text=str(pg), y=580.0, page_num=pg, bbox=(270, 580, 290, 592))]
        for pg in range(1, 6)
    ]
    result = detect_repeating(all_edges, total_pages=5)
    # y_bucket = round(580 / 2) * 2 = 580.0
    assert (580.0, "__PAGE_NUM__") in result


def test_detect_repeating_doc_number_pattern():
    """Running doc number at same y across pages is classified as __DOC_NUM__."""
    # Same paper, revision number varies line-by-line — not realistic, but exercises
    # the path. In practice the doc number repeats identically, which would hit the
    # exact-text branch before DOC_NUM. Use revisions that differ:
    docs = ["P1234R0", "P1234R1", "P1234R0", "P1234R2"]
    all_edges = [
        [PageEdgeItem(text=docs[i], y=30.0, page_num=i + 1, bbox=(0, 30, 100, 42))]
        for i in range(4)
    ]
    result = detect_repeating(all_edges, total_pages=4)
    assert (30.0, "__DOC_NUM__") in result


# ---- strip_repeating -----------------------------------------------------

def test_strip_repeating_removes_exact_match():
    """A line whose (y, text) matches a repeating entry is removed."""
    b = _make_block_at_y([("Running Head", 30), ("Real content", 60)])
    repeating = {(36.0, "Running Head")}
    result = strip_repeating([b], repeating)
    assert len(result) == 1
    texts = [ln.text for ln in result[0].lines]
    assert "Real content" in texts
    assert "Running Head" not in texts


def test_strip_repeating_removes_page_numbers():
    """A line matching PAGE_NUM_RE at the repeating y-bucket is removed."""
    b = _make_block_at_y([("42", 580), ("Body line", 300)])
    repeating = {(586.0, "__PAGE_NUM__")}
    result = strip_repeating([b], repeating)
    texts = [ln.text for ln in result[0].lines]
    assert "42" not in texts
    assert "Body line" in texts


def test_strip_repeating_y_tolerance():
    """Lines whose y differs by <= Y_TOLERANCE from the repeating bucket are stripped."""
    b = _make_block_at_y([("Running Head", 31)])   # y=31, tolerance 2.0 around 30
    repeating = {(36.0, "Running Head")}
    result = strip_repeating([b], repeating)
    # Block may be dropped if it becomes empty.
    assert not result or not any("Running Head" in ln.text for blk in result for ln in blk.lines)


def test_strip_repeating_drops_empty_blocks():
    """A block with all lines stripped is omitted from the output."""
    b = _make_block_at_y([("Running Head", 30)])
    repeating = {(36.0, "Running Head")}
    result = strip_repeating([b], repeating)
    assert result == []


def test_strip_repeating_empty_input():
    """Empty repeating set returns blocks unchanged."""
    b = _make_block_at_y([("content", 300)])
    assert strip_repeating([b], set()) == [b]