"""Tests for lib.pdf.wg21."""

from lib.pdf.types import Block, Line, Span
from lib.pdf.wg21 import extract_metadata_from_blocks, REPLY_TO_CONTINUATION_CAP


def _meta_block(lines_text, page_num=0, font_size=9.0):
    lines = []
    for text in lines_text:
        span = Span(text=text, font_size=font_size)
        lines.append(Line(spans=[span], page_num=page_num))
    return Block(lines=lines, page_num=page_num)


def test_extracts_doc_number():
    b = _meta_block(["Document Number: P4003R0", "Date: 2026-01-01"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert meta.get("document") == "P4003R0"


def test_extracts_date():
    b = _meta_block(["Document Number: P1234R0", "Date: 2026-03-15"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert meta.get("date") == "2026-03-15"


def test_extracts_audience():
    b = _meta_block(["Document Number: P1234R0", "Audience: LEWG"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert meta.get("audience") == "LEWG"


def test_extracts_reply_to():
    b = _meta_block(["Document Number: P1234R0",
                      "Reply-to: Alice <alice@x.com>"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert "reply-to" in meta
    assert any("Alice" in a for a in meta["reply-to"])


def test_title_picks_largest_font():
    title_block = _meta_block(["My Paper Title"], font_size=16.0)
    label_block = _meta_block(["Subtitle Line"], font_size=9.0)
    meta_block = _meta_block(["Document Number: P1234R0"], font_size=9.0)
    meta, consumed = extract_metadata_from_blocks(
        [label_block, title_block, meta_block])
    assert meta.get("title") == "My Paper Title"


def test_pre_label_blocks_consumed():
    cat_block = _meta_block(["WG21 PROPOSAL"], font_size=9.0)
    title_block = _meta_block(["Real Title"], font_size=16.0)
    meta_block = _meta_block(["Document Number: P1234R0"], font_size=9.0)
    meta, consumed = extract_metadata_from_blocks(
        [cat_block, title_block, meta_block])
    assert 0 in consumed
    assert 1 in consumed


def test_title_prefers_darker_at_same_size():
    light_block = Block(
        lines=[Line(spans=[Span(text="Light Title", font_size=16.0)])],
        page_num=0, bbox=(10, 100, 200, 116))
    dark_block = Block(
        lines=[Line(spans=[Span(text="Dark Title", font_size=16.0)])],
        page_num=0, bbox=(10, 200, 200, 216))
    meta_block = _meta_block(["Document Number: P1234R0"], font_size=9.0)
    text_colors = {100.0: 0.42, 200.0: 0.17}
    meta, consumed = extract_metadata_from_blocks(
        [light_block, dark_block, meta_block], text_colors)
    assert meta.get("title") == "Dark Title"


def test_title_selected_with_empty_color_data():
    title_block = _meta_block(["My Paper Title"], font_size=16.0)
    meta_block = _meta_block(["Document Number: P1234R0"], font_size=9.0)
    meta, consumed = extract_metadata_from_blocks(
        [title_block, meta_block], {})
    assert meta.get("title") == "My Paper Title"


def test_reply_to_name_email_on_same_line():
    b = _meta_block(["Document Number: P1234R0",
                      "Reply-to: Alice Smith alice@example.com"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert "reply-to" in meta
    assert any("Alice Smith" in a for a in meta["reply-to"])
    assert any("alice@example.com" in a for a in meta["reply-to"])


def test_reply_to_name_then_email_on_next_line():
    b = _meta_block(["Document Number: P1234R0",
                      "Reply-to: Bob Jones",
                      "bob@example.com"])
    meta, consumed = extract_metadata_from_blocks([b])
    assert "reply-to" in meta
    assert any("Bob Jones" in a for a in meta["reply-to"])


def test_reply_to_continuation_capped():
    """Reply-to loop must stop after REPLY_TO_CONTINUATION_CAP blocks,
    even if later blocks still contain emails."""
    reply_block = _meta_block(["Reply-to: Alice <alice@x.com>"])
    # Generate more continuation blocks than the cap allows
    extra_count = REPLY_TO_CONTINUATION_CAP + 5
    extras = [
        _meta_block([f"Person{n} <p{n}@x.com>"])
        for n in range(extra_count)
    ]
    blocks = [reply_block] + extras
    meta, consumed = extract_metadata_from_blocks(blocks)
    # The continuation blocks consumed must not exceed the cap
    # (block 0 is consumed as the reply-to label block itself)
    continuation_consumed = consumed - {0}
    assert len(continuation_consumed) == REPLY_TO_CONTINUATION_CAP
    # The block just past the cap must not be consumed
    past_cap_idx = 1 + REPLY_TO_CONTINUATION_CAP
    assert past_cap_idx not in consumed
