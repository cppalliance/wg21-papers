#!/usr/bin/env python3
"""Assemble A Young Delegate's Notebook from its chapter files into one manuscript.

Reads the chapters in fixed order, generates a table of contents from the
chapter and section headings, and writes young-delegates-notebook.md and
young-delegates-notebook.docx. It also writes indesign/title.icml and
indesign/body.icml, the stories that indesign/layout.jsx lays out for print.
Run from the book root:

    python build.py

The .docx takes its look from the reviewers' revision document. Each look is
defined once as a named style in STYLES_XML, and every paragraph and run only
points at a style. Markdown the converter doesn't handle (tables, code fences,
nested lists, bold, images, raw HTML) stops the build with the file and line.

The one HTML the converter does handle is a box: a `<div id="...">` line and a
`</div>` line, each on its own, around plain paragraphs and bullets. The id
names the box type in BOXES, and the box renders as a shaded panel under the
type's label.

The ICML stories carry text and style names only. Every look they get in
InDesign comes from the spec at the top of indesign/layout.jsx, so the two
files share the style names in ICML_PARAGRAPHS, ICML_CHARACTERS, and the box
labels. The print text also gets curly quotes, initials that stay on one
line, and a no-break space before each spaced hyphen so no line starts with
one.

Missing chapters are skipped with a warning, so the build works while the book
is still being written.
"""
from __future__ import annotations

import datetime
import itertools
import re
import string
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"
OUTPUT = ROOT / "young-delegates-notebook.md"
DOCX = ROOT / "young-delegates-notebook.docx"
INDESIGN = ROOT / "indesign"

TITLE = "A Young Delegate's Notebook"
SUBTITLE = "A Newcomer's Path into WG21 and the Standardization of C++"
BLURB = (
    "A practical guide for anyone who wants to help shape C++ but has never "
    "set foot in a committee meeting. It accumulates: each chapter stands on "
    "the ones before it, and you can stop at any chapter and still have "
    "something useful to offer. Every paper number is a live link, and every "
    "named resource points somewhere real."
)

ORDER = [
    "intro.md",
    "ch-01.md",
    "ch-02.md",
    "ch-03.md",
    "ch-04.md",
    "ch-05.md",
    "ch-06.md",
    "ch-07.md",
    "ch-08.md",
    "ch-09.md",
    "ch-10.md",
    "ch-11.md",
    "ch-12.md",
    "ch-13.md",
]

# div id -> (label, bar color, fill color, label color, bold text)
BOXES = {
    "in-this-chapter": ("In This Chapter", "2f5496", "e8f0fa", "1f3864", False),
    "short-version": ("The Short Version", "1f3864", "e8eef6", "1f3864", False),
    "rule-of-thumb": ("Rule of Thumb", "38761d", "e9f5e9", "274e13", True),
    "watch-out": ("Watch Out", "c0392b", "fdece4", "922b21", False),
    "try-this-today": ("Try This Today", "0b7285", "e4f4f4", "0b5563", False),
}

XML_DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

STYLES_XML = """
<w:docDefaults>
<w:rPrDefault><w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:line="300" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:pPr><w:spacing w:after="160"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:pPr><w:spacing w:before="2400" w:after="360" w:line="240"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:b/><w:color w:val="1f3864"/><w:sz w:val="56"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOCHeading"><w:name w:val="TOC Heading"/><w:basedOn w:val="Normal"/>
<w:pPr><w:pageBreakBefore/></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/>
<w:pPr><w:spacing w:before="120" w:after="40"/></w:pPr>
<w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/>
<w:pPr><w:spacing w:after="20"/><w:ind w:left="360"/></w:pPr>
<w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:pageBreakBefore/><w:spacing w:before="120" w:after="240"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="1f3864"/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:keepNext/><w:spacing w:before="320" w:after="120"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:color w:val="2f5496"/><w:sz w:val="27"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/>
<w:pPr><w:outlineLvl w:val="2"/></w:pPr>
<w:rPr><w:color w:val="1f4d78"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/>
<w:pPr><w:numPr><w:numId w:val="1"/></w:numPr><w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListNumber"><w:name w:val="List Number"/>
<w:pPr><w:spacing w:after="60"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/>
<w:pPr><w:spacing w:after="160"/><w:ind w:left="720" w:right="720"/></w:pPr>
<w:rPr><w:i/><w:color w:val="404040"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BoxText"><w:name w:val="Box Text"/>
<w:pPr><w:spacing w:after="100"/><w:jc w:val="left"/></w:pPr>
<w:rPr><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BoxTextBold"><w:name w:val="Box Text Bold"/><w:basedOn w:val="BoxText"/>
<w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BoxBullet"><w:name w:val="Box Bullet"/><w:basedOn w:val="BoxText"/>
<w:pPr><w:numPr><w:numId w:val="1"/></w:numPr><w:spacing w:after="60"/><w:ind w:left="540" w:hanging="300"/></w:pPr></w:style>
<w:style w:type="character" w:styleId="Emphasis"><w:name w:val="Emphasis"/>
<w:rPr><w:i/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Code"><w:name w:val="Code"/>
<w:rPr><w:rFonts w:ascii="Roboto Mono" w:hAnsi="Roboto Mono"/><w:color w:val="188038"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>
<w:rPr><w:color w:val="1155cc"/><w:u w:val="single"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="HyperlinkEmphasis"><w:name w:val="Hyperlink Emphasis"/><w:basedOn w:val="Hyperlink"/>
<w:rPr><w:i/></w:rPr></w:style>
<w:style w:type="character" w:styleId="HyperlinkCode"><w:name w:val="Hyperlink Code"/><w:basedOn w:val="Hyperlink"/>
<w:rPr><w:rFonts w:ascii="Roboto Mono" w:hAnsi="Roboto Mono"/></w:rPr></w:style>
""" + "".join(
    f'<w:style w:type="paragraph" w:styleId="BoxLabel-{box}"><w:name w:val="Box Label {label}"/>\n'
    f'<w:pPr><w:keepNext/><w:spacing w:after="80"/><w:jc w:val="left"/></w:pPr>\n'
    f'<w:rPr><w:b/><w:color w:val="{ink}"/><w:sz w:val="17"/></w:rPr></w:style>\n'
    for box, (label, _, _, ink, _) in BOXES.items()
)

NUMBERING_XML = """
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/>
<w:lvlText w:val="\u2022"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="300"/></w:pPr></w:lvl></w:abstractNum>
<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/>
<w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="540" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
"""

SECTION_XML = (
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
    "</w:sectPr>"
)

SETTINGS_XML = (
    '<w:compat><w:compatSetting w:name="compatibilityMode" '
    'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
)

CONTENT_TYPES = (
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    + "".join(
        f'<Override PartName="/word/{part}.xml" '
        f'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{kind}+xml"/>'
        for part, kind in (
            ("document", "document.main"),
            ("styles", "styles"),
            ("numbering", "numbering"),
            ("settings", "settings"),
        )
    )
    + "</Types>"
)

HEADINGS = {2: "Heading1", 3: "Heading2", 4: "Heading3"}

# the only block styles a box may hold, and what they become inside it
BOX_STYLES = {"Normal": "BoxText", "ListBullet": "BoxBullet"}

# (italic, code, link) -> character style
RUN_STYLES = {
    (False, False, False): None,
    (True, False, False): "Emphasis",
    (False, True, False): "Code",
    (False, False, True): "Hyperlink",
    (True, False, True): "HyperlinkEmphasis",
    (False, True, True): "HyperlinkCode",
}

# docx paragraph style -> InDesign paragraph style. Body text, epigraphs, and
# boxes pick their InDesign style from what comes before them instead.
ICML_PARAGRAPHS = {
    "Heading1": "Chapter Title",
    "Heading2": "Section Heading",
    "Heading3": "Subsection Heading",
    "ListBullet": "Bullet",
    "ListNumber": "Number",
}

# docx character style -> InDesign character style
ICML_CHARACTERS = {
    None: "$ID/[No character style]",
    "Emphasis": "Emphasis",
    "Code": "Code",
    "Hyperlink": "Link",
    "HyperlinkEmphasis": "Link Emphasis",
    "HyperlinkCode": "Link Code",
}

ICML_HEAD = (
    '<?aid style="50" type="snippet" readerVersion="6.0" featureSet="513" product="8.0(370)" ?>\n'
    '<?aid SnippetType="InCopyInterchange"?>\n'
)


def unsupported(where: str, what: str) -> SystemExit:
    return SystemExit(f"{where}: unsupported markdown: {what}")


def md_blocks(text: str, name: str) -> list[tuple[str, str, int, int]]:
    """Split chapter markdown into (paragraph style, text, line, list number) blocks.

    A box comes out as a BoxStart block holding the box id, the box's own
    blocks, and a BoxEnd block.
    """
    blocks: list[list] = []
    current: list | None = None
    comment = False
    box_start = 0
    for n, line in enumerate(text.splitlines(), 1):
        where = f"{name}:{n}"
        stripped = line.strip()
        if comment or stripped.startswith("<!--"):
            comment = "-->" not in line
            current = None
        elif not stripped or re.fullmatch(r"-{3,}", stripped):
            current = None
        elif m := re.fullmatch(r'<div id="([^"]*)">', line.rstrip()):
            if box_start:
                raise unsupported(where, "box inside a box")
            if m[1] not in BOXES:
                raise unsupported(where, f'unknown box id "{m[1]}"')
            blocks.append(["BoxStart", m[1], n, 0])
            box_start, current = n, None
        elif line.rstrip() == "</div>":
            if not box_start:
                raise unsupported(where, "</div> with no open box")
            if blocks[-1][0] == "BoxStart":
                raise unsupported(where, "empty box")
            blocks.append(["BoxEnd", "", n, 0])
            box_start, current = 0, None
        elif m := re.match(r"(#{1,6})\s+(.*)$", line):
            if len(m[1]) not in HEADINGS:
                raise unsupported(where, f"level {len(m[1])} heading")
            blocks.append([HEADINGS[len(m[1])], m[2].strip(), n, 0])
            current = None
        elif line.startswith(">"):
            quoted = line[1:].strip()
            if quoted.startswith(">"):
                raise unsupported(where, "nested blockquote")
            if not quoted:
                current = None
            elif current and current[0] == "Quote":
                current[1] += " " + quoted
            else:
                current = ["Quote", quoted, n, 0]
                blocks.append(current)
        elif m := re.match(r"[-*+]\s+(.*)$", line):
            current = ["ListBullet", m[1], n, 0]
            blocks.append(current)
        elif m := re.match(r"(\d+)[.)]\s+(.*)$", line):
            current = ["ListNumber", m[2], n, int(m[1])]
            blocks.append(current)
        elif line[0].isspace():
            raise unsupported(where, "indented line (nested list or code block)")
        elif re.match(r"```|~~~|\||<[a-zA-Z/]", line):
            raise unsupported(where, "code fence, table, or HTML block")
        elif current:
            current[1] += " " + stripped
        else:
            current = ["Normal", stripped, n, 0]
            blocks.append(current)
    if box_start:
        raise unsupported(f"{name}:{box_start}", "box with no </div>")
    inside = False
    for block in blocks:
        if block[0] in ("BoxStart", "BoxEnd"):
            inside = block[0] == "BoxStart"
        elif inside:
            if block[0] not in BOX_STYLES:
                raise unsupported(f"{name}:{block[2]}", f"{block[0]} inside a box")
            block[0] = BOX_STYLES[block[0]]
    return [tuple(block) for block in blocks]


def md_runs(text: str, where: str) -> list[tuple[str, str | None, str | None]]:
    """Split inline markdown into (text, character style, link URL) runs."""
    runs: list[tuple[str, str | None, str | None]] = []

    def find(s: str, i: int, ch: str) -> int:
        while i < len(s):
            if s[i] == "\\":
                i += 2
            elif s[i] == ch:
                return i
            elif ch == "*" and s[i] in "`[":
                j = find(s, i + 1, "`" if s[i] == "`" else "]")
                i = j + 1 if j >= 0 else i + 1
            else:
                i += 1
        return -1

    def scan(s: str, italic: bool, url: str | None) -> None:
        buf: list[str] = []

        def flush() -> None:
            if buf:
                runs.append(("".join(buf), RUN_STYLES[italic, False, url is not None], url))
                buf.clear()

        i = 0
        while i < len(s):
            c = s[i]
            if c == "\\" and i + 1 < len(s) and s[i + 1] in string.punctuation:
                buf.append(s[i + 1])
                i += 2
            elif c == "`":
                j = s.find("`", i + 1)
                style = RUN_STYLES.get((italic, True, url is not None), "")
                if j < 0 or style == "":
                    raise unsupported(where, "unclosed or italic code span")
                flush()
                runs.append((s[i + 1:j], style, url))
                i = j + 1
            elif s.startswith("**", i):
                raise unsupported(where, "bold")
            elif s.startswith("![", i):
                raise unsupported(where, "image")
            elif c == "*" and not s[i + 1:i + 2].isspace():
                j = find(s, i + 1, "*")
                if j < 0:
                    raise unsupported(where, "unclosed *")
                flush()
                scan(s[i + 1:j], True, url)
                i = j + 1
            elif c == "[" and (j := find(s, i + 1, "]")) >= 0 and s.startswith("(", j + 1):
                k = s.find(")", j + 2)
                target = s[j + 2:k]
                if k < 0 or url or not target or " " in target:
                    raise unsupported(where, "nested or malformed link")
                flush()
                scan(s[i + 1:j], italic, target)
                i = k + 1
            elif re.match(r"<[a-zA-Z/!]", s[i:i + 2]):
                raise unsupported(where, "inline HTML or autolink")
            else:
                buf.append(c)
                i += 1
        flush()

    scan(text, False, None)
    return runs


def run_xml(text: str, style: str | None) -> str:
    rpr = f'<w:rPr><w:rStyle w:val="{style}"/></w:rPr>' if style else ""
    space = ' xml:space="preserve"' if text != text.strip() else ""
    return f"<w:r>{rpr}<w:t{space}>{escape(text)}</w:t></w:r>"


def paragraph(style: str, runs: list, links: dict[str, str], num: int = 0) -> str:
    ppr = "" if style == "Normal" else f'<w:pStyle w:val="{style}"/>'
    if num:
        ppr += f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num}"/></w:numPr>'
    xml = f"<w:pPr>{ppr}</w:pPr>" if ppr else ""
    for url, group in itertools.groupby(runs, key=lambda run: run[2]):
        group_xml = "".join(run_xml(text, run_style) for text, run_style, _ in group)
        if url:
            rid = links.setdefault(url, f"rId{len(links) + 4}")
            group_xml = f'<w:hyperlink r:id="{rid}">{group_xml}</w:hyperlink>'
        xml += group_xml
    return f"<w:p>{xml}</w:p>"


def box_table(box: str, paragraphs: list[str]) -> str:
    """One-cell table with a colored bar down its left edge and a shaded fill."""
    _, bar, fill, _, _ = BOXES[box]
    return (
        '<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/><w:jc w:val="left"/>'
        '<w:tblLayout w:type="fixed"/><w:tblLook w:val="0000"/></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="9000"/></w:tblGrid>'
        '<w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="9000" w:type="dxa"/>'
        f'<w:tcBorders><w:left w:val="single" w:sz="24" w:space="0" w:color="{bar}"/></w:tcBorders>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
        '<w:tcMar><w:top w:w="140" w:type="dxa"/><w:left w:w="220" w:type="dxa"/>'
        '<w:bottom w:w="140" w:type="dxa"/><w:right w:w="200" w:type="dxa"/></w:tcMar></w:tcPr>'
        + "".join(paragraphs)
        + "</w:tc></w:tr></w:tbl>"
    )


def write_markdown(chapters: list[tuple[str, str]], headings: list[tuple[int, str]], stamp: str) -> None:
    toc = ["## Contents", ""] + [f"{'  ' * (level - 2)}- {heading}" for level, heading in headings]
    header = [
        f"# {TITLE}",
        "",
        f"*{SUBTITLE}*",
        "",
        BLURB,
        "",
        f"*Assembled {stamp}*",
        "",
        "\n".join(toc),
        "",
        "---",
        "",
    ]
    body = "\n\n---\n\n".join(text for _, text in chapters)
    OUTPUT.write_bytes(("\n".join(header) + "\n" + body + "\n").encode("utf-8"))  # LF on every OS


def write_docx(chapters: list[tuple[str, str]], headings: list[tuple[int, str]], stamp: str) -> None:
    links: dict[str, str] = {}
    starts: list[int] = []
    body: list[str] = []
    spacer = paragraph("Normal", [], links)
    for name, text in chapters:
        previous = None
        box, cell = "", []
        for style, block, line, number in md_blocks(text, name):
            if style == "BoxStart":
                box = block
                cell = [paragraph(f"BoxLabel-{box}", md_runs(BOXES[box][0].upper(), f"{name}:{line}"), links)]
            elif style == "BoxEnd":
                body += [spacer, box_table(box, cell)]
                box = ""
            else:
                if style == "ListNumber" and previous != "ListNumber":
                    starts.append(number)
                num = len(starts) + 1 if style == "ListNumber" else 0
                if previous == "BoxEnd" and style not in HEADINGS.values():
                    body.append(spacer)
                if style == "BoxText" and BOXES[box][4]:
                    style = "BoxTextBold"
                (cell if box else body).append(paragraph(style, md_runs(block, f"{name}:{line}"), links, num))
            previous = style

    front = [paragraph("Title", md_runs(TITLE, "TITLE"), links)]
    for text in (f"*{SUBTITLE}*", BLURB, f"*Assembled {stamp}*"):
        front.append(paragraph("Normal", md_runs(text, "front matter"), links))
    front.append(paragraph("TOCHeading", md_runs("Contents", "contents"), links))
    for level, heading in headings:
        front.append(paragraph(f"TOC{level - 1}", md_runs(heading, "contents"), links))

    numbering = NUMBERING_XML + "".join(
        f'<w:num w:numId="{i}"><w:abstractNumId w:val="1"/>'
        f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="{start}"/></w:lvlOverride></w:num>\n'
        for i, start in enumerate(starts, 2)
    )
    rels = "".join(
        f'<Relationship Id="rId{i}" Type="{REL}/{part}" Target="{part}.xml"/>'
        for i, part in enumerate(("styles", "numbering", "settings"), 1)
    ) + "".join(
        f'<Relationship Id="{rid}" Type="{REL}/hyperlink" Target={quoteattr(url)} TargetMode="External"/>'
        for url, rid in links.items()
    )
    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": (
            f'<Relationships xmlns="{PKG_REL}">'
            f'<Relationship Id="rId1" Type="{REL}/officeDocument" Target="word/document.xml"/></Relationships>'
        ),
        "word/document.xml": (
            f'<w:document {W} xmlns:r="{REL}"><w:body>\n'
            + "\n".join(front + body)
            + f"\n{SECTION_XML}</w:body></w:document>"
        ),
        "word/_rels/document.xml.rels": f'<Relationships xmlns="{PKG_REL}">{rels}</Relationships>',
        "word/styles.xml": f"<w:styles {W}>{STYLES_XML}</w:styles>",
        "word/numbering.xml": f"<w:numbering {W}>{numbering}</w:numbering>",
        "word/settings.xml": f"<w:settings {W}>{SETTINGS_XML}</w:settings>",
    }
    with zipfile.ZipFile(DOCX, "w") as docx:
        for name, xml in parts.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))  # fixed stamp keeps rebuilds identical
            docx.writestr(info, XML_DECL + xml, zipfile.ZIP_DEFLATED)


def print_runs(runs: list) -> list:
    """Curl straight quotes, keep initials like "W. K." together, and tie each
    spaced hyphen to the word before it, all outside code.

    Both changes swap one character for one character, so the paragraph is
    rewritten as a whole and cut back into the same runs. That lets a quote
    see the character before it even when that character is in another run.
    """
    text = "".join(run[0] for run in runs)
    code = [run[1] in ("Code", "HyperlinkCode") for run in runs for _ in run[0]]
    out = list(text)
    for i, c in enumerate(text):
        if code[i]:
            continue
        opening = i == 0 or out[i - 1].isspace() or out[i - 1] in "([\u201c\u2018"
        if c == '"':
            out[i] = "\u201c" if opening else "\u201d"
        elif c == "'":
            out[i] = "\u2018" if opening else "\u2019"
        elif c == " " and text.startswith("- ", i + 1):
            out[i] = "\u00a0"
        elif c == " " and re.match(r"[A-Z]\.", text[i + 1:i + 3]) and re.search(r"(^|\s)[A-Z]\.$", text[max(0, i - 3):i]):
            out[i] = "\u00a0"
    curled, start = [], 0
    for run_text, style, url in runs:
        curled.append(("".join(out[start:start + len(run_text)]), style, url))
        start += len(run_text)
    return curled


def icml_paragraphs(chapters: list[tuple[str, str]]) -> list[tuple[str, list, str]]:
    """Turn the chapters into (InDesign paragraph style, runs, extra attributes) paragraphs."""
    paragraphs: list[tuple[str, list, str]] = []
    for name, text in chapters:
        previous, box = None, ""
        for style, block, line, number in md_blocks(text, name):
            where = f"{name}:{line}"
            attrs = ""
            if style == "BoxStart":
                box = BOXES[block][0]
                paragraphs.append((f"{box} Label", [(box, None, None)], ""))
            elif style == "BoxEnd":
                box = ""
            elif box:
                kind = "Bullet" if style == "BoxBullet" else "Text"
                paragraphs.append((f"{box} {kind}", md_runs(block, where), ""))
            else:
                if style == "Normal" and previous == "Normal":
                    para = "Body"
                elif style == "Normal" and (previous is None or previous in HEADINGS.values()):
                    para = "Body First"
                elif style == "Normal" and previous == "BoxEnd":
                    para = "Body After Box"
                elif style == "Normal":
                    para = "Body After Break"
                elif style == "Quote":
                    para = "Epigraph Source" if previous == "Quote" else "Epigraph"
                else:
                    para = ICML_PARAGRAPHS[style]
                    if style == "ListNumber" and previous != "ListNumber":
                        attrs = f' NumberingContinue="false" NumberingStartAt="{number}"'
                paragraphs.append((para, md_runs(block, where), attrs))
            previous = style
    return paragraphs


def write_icml(path: Path, paragraphs: list[tuple[str, list, str]]) -> None:
    """Write one InCopy story that declares its styles by name only."""
    def ref(kind: str, name: str) -> str:
        return quoteattr(f"{kind}/{name}")

    plain = ref("CharacterStyle", ICML_CHARACTERS[None])
    destinations: dict[str, int] = {}
    sources: list[int] = []
    story: list[str] = []
    for n, (style, runs, attrs) in enumerate(paragraphs):
        xml = [f'<ParagraphStyleRange AppliedParagraphStyle={ref("ParagraphStyle", style)}{attrs}>']
        for text, run_style, url in print_runs(runs):
            content = f"<Content>{escape(text)}</Content>"
            if url:
                sources.append(destinations.setdefault(url, len(destinations) + 1))
                src = f"ydn-src-{len(sources)}"
                content = f'<HyperlinkTextSource Self="{src}" Name="{src}" Hidden="false">{content}</HyperlinkTextSource>'
            xml.append(f'<CharacterStyleRange AppliedCharacterStyle={ref("CharacterStyle", ICML_CHARACTERS[run_style])}>{content}</CharacterStyleRange>')
        if n < len(paragraphs) - 1:
            xml.append(f"<CharacterStyleRange AppliedCharacterStyle={plain}><Br/></CharacterStyleRange>")
        story.append("".join(xml) + "</ParagraphStyleRange>")

    para_styles = ["$ID/[No paragraph style]"] + sorted({style for style, _, _ in paragraphs})
    char_styles = list(ICML_CHARACTERS.values())
    declared = (
        '<RootCharacterStyleGroup Self="ydn-cs">'
        + "".join(f'<CharacterStyle Self={ref("CharacterStyle", s)} Name={quoteattr(s)}/>' for s in char_styles)
        + '</RootCharacterStyleGroup>\n<RootParagraphStyleGroup Self="ydn-ps">'
        + "".join(f'<ParagraphStyle Self={ref("ParagraphStyle", s)} Name={quoteattr(s)}/>' for s in para_styles)
        + "</RootParagraphStyleGroup>"
    )
    links = "".join(
        f'<HyperlinkURLDestination Self="HyperlinkURLDestination/ydn-url-{key}" Name="ydn-url-{key}" '
        f'DestinationURL={quoteattr(url)} DestinationUniqueKey="{key}" Hidden="false"/>\n'
        for url, key in destinations.items()
    ) + "".join(
        f'<Hyperlink Self="ydn-link-{i}" Name="ydn-link-{i}" Source="ydn-src-{i}" Visible="false" '
        f'Hidden="false" DestinationUniqueKey="{key}"><Properties>'
        '<BorderColor type="enumeration">Black</BorderColor>'
        f'<Destination type="object">HyperlinkURLDestination/ydn-url-{key}</Destination>'
        "</Properties></Hyperlink>\n"
        for i, key in enumerate(sources, 1)
    )
    path.parent.mkdir(exist_ok=True)
    path.write_bytes((
        XML_DECL + ICML_HEAD
        + '<Document DOMVersion="8.0" Self="ydn">\n' + declared + "\n"
        + '<Story Self="ydn-story" AppliedTOCStyle="n" TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">\n'
        + "\n".join(story)
        + "\n</Story>\n" + links + "</Document>\n"
    ).encode("utf-8"))


def build() -> None:
    chapters: list[tuple[str, str]] = []
    headings: list[tuple[int, str]] = []
    word_count = 0

    for name in ORDER:
        path = CHAPTERS / name
        if not path.exists():
            print(f"warning: missing chapter {name}, skipping")
            continue
        text = path.read_text(encoding="utf-8").strip()
        chapters.append((name, text))
        word_count += len(text.split())
        for line in text.splitlines():
            m = re.match(r"^(#{2,3})\s+(.*)$", line)
            if m:
                headings.append((len(m.group(1)), m.group(2).strip()))

    stamp = datetime.date.today().isoformat()
    write_markdown(chapters, headings, stamp)
    print(f"wrote {OUTPUT.name}: {word_count} words across {len(chapters)} chapters")
    write_docx(chapters, headings, stamp)
    print(f"wrote {DOCX.name}")
    write_icml(INDESIGN / "title.icml", [("Title", [(TITLE, None, None)], ""), ("Subtitle", [(SUBTITLE, None, None)], "")])
    write_icml(INDESIGN / "body.icml", icml_paragraphs(chapters))
    print(f"wrote {INDESIGN.name}/title.icml and {INDESIGN.name}/body.icml")


if __name__ == "__main__":
    build()
