
"""Per-generator integration tests for the HTML converter."""
from pathlib import Path

import pytest

from lib.html.extract import (
    parse_html, detect_generator, extract_metadata, strip_boilerplate,
)
from lib.html.render import render_body


FIXTURES = Path(__file__).parent / "fixtures" / "html"


def _load(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


# ---- Bikeshed -----------------------------------------------------------

def test_bikeshed_detection():
    soup = parse_html(_load("bikeshed_sample.html"))
    assert detect_generator(soup) == "bikeshed"


def test_bikeshed_metadata_extraction():
    soup = parse_html(_load("bikeshed_sample.html"))
    meta = extract_metadata(soup, "bikeshed")
    assert meta.get("document") == "P9999R0"
    assert meta.get("title") == "Test Bikeshed Paper"
    assert meta.get("date") == "2026-03-15"
    assert meta.get("audience") == "SG1"
    reply_to = meta.get("reply-to", [])
    assert any("editor@example.com" in entry for entry in reply_to)


def test_bikeshed_boilerplate_stripped():
    soup = parse_html(_load("bikeshed_sample.html"))
    strip_boilerplate(soup, "bikeshed")
    # h1.p-name and data-fill-with divs removed.
    assert soup.find("h1", class_="p-name") is None


def test_bikeshed_body_renders():
    soup = parse_html(_load("bikeshed_sample.html"))
    strip_boilerplate(soup, "bikeshed")
    md = render_body(soup, "bikeshed")
    assert "## Introduction" in md
    assert "Body paragraph content." in md


# ---- HackMD -------------------------------------------------------------

def test_hackmd_detection():
    soup = parse_html(_load("hackmd_sample.html"))
    assert detect_generator(soup) == "hackmd"


def test_hackmd_metadata_via_generic_fallback():
    """HackMD has no specific extractor; metadata comes through the generic path."""
    soup = parse_html(_load("hackmd_sample.html"))
    meta = extract_metadata(soup, "hackmd")
    # detect_generator returned "hackmd" but extract_metadata dispatches by argument;
    # passing "hackmd" falls through to _extract_generic_metadata.
    assert meta.get("title") == "P9999R0: Test HackMD Paper"
    # The generic table scan should pick up document/audience from the <table>.
    assert meta.get("document") == "P9999R0"
    assert meta.get("audience") == "SG1"


def test_hackmd_body_renders():
    soup = parse_html(_load("hackmd_sample.html"))
    strip_boilerplate(soup, "hackmd")
    md = render_body(soup, "hackmd")
    assert "## Introduction" in md
    assert "Body paragraph." in md


# ---- Hand-written (address form) ----------------------------------------

def test_handwritten_address_detection():
    soup = parse_html(_load("handwritten_address_sample.html"))
    assert detect_generator(soup) == "hand-written"


def test_handwritten_address_metadata():
    soup = parse_html(_load("handwritten_address_sample.html"))
    meta = extract_metadata(soup, "hand-written")
    assert meta.get("document") == "P9999R0"
    assert meta.get("date") == "2026-03-15"
    assert meta.get("audience") == "SG1"
    reply_to = meta.get("reply-to", [])
    assert any("alice@example.com" in entry for entry in reply_to)


def test_handwritten_address_boilerplate_stripped():
    soup = parse_html(_load("handwritten_address_sample.html"))
    strip_boilerplate(soup, "hand-written")
    # <address> removed.
    assert soup.find("address") is None


def test_handwritten_address_body_renders():
    soup = parse_html(_load("handwritten_address_sample.html"))
    strip_boilerplate(soup, "hand-written")
    md = render_body(soup, "hand-written")
    assert "## Introduction" in md


# ---- Hand-written (table.header form) -----------------------------------

def test_handwritten_table_metadata():
    soup = parse_html(_load("handwritten_table_sample.html"))
    meta = extract_metadata(soup, "hand-written")
    assert meta.get("document") == "P9998R0"
    assert meta.get("date") == "2026-02-01"
    assert meta.get("audience") == "EWG"
    reply_to = meta.get("reply-to", [])
    assert any("bob@example.com" in entry for entry in reply_to)


def test_handwritten_table_boilerplate_stripped():
    soup = parse_html(_load("handwritten_table_sample.html"))
    strip_boilerplate(soup, "hand-written")
    assert soup.find("table", class_="header") is None