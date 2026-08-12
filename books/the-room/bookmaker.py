import re
import os
import pyphen
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, NextPageTemplate,
    BaseDocTemplate, PageTemplate, Frame, KeepTogether,
    Table, TableStyle, ActionFlowable, Indenter
)

TRIM_W = 5.5 * inch
TRIM_H = 8.5 * inch

COVER_W = 6.458 * inch
COVER_H = 10 * inch

MARGIN_TOP = 0.75 * inch
MARGIN_BOTTOM = 0.75 * inch
MARGIN_OUTSIDE = 0.625 * inch
MARGIN_GUTTER = 0.875 * inch

CHAPTER_DROP_MIN = 1.5 * inch


# ---------------------------------------------------------------------------
# Custom doc template - auto-selects odd/even body templates by page parity
# ---------------------------------------------------------------------------

class BookDocTemplate(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._skip_auto = False

    def handle_nextPageTemplate(self, pt):
        self._skip_auto = True
        super().handle_nextPageTemplate(pt)

    def afterPage(self):
        if self._skip_auto:
            self._skip_auto = False
            return
        next_page = self.page + 1
        tid = "odd" if next_page % 2 == 1 else "even"
        for i, t in enumerate(self.pageTemplates):
            if t.id == tid:
                self._nextPageTemplateIndex = i
                break


class EnsureOdd(ActionFlowable):
    """If we're on an even page, insert a blank to land on odd."""
    def __init__(self):
        ActionFlowable.__init__(self)

    def apply(self, doc):
        if doc.page % 2 == 0:
            doc.handle_nextPageTemplate("blank")
            doc.handle_pageBreak()


# ---------------------------------------------------------------------------
# Frames
# ---------------------------------------------------------------------------

def make_frame(page_num):
    if page_num % 2 == 1:
        left, right = MARGIN_GUTTER, MARGIN_OUTSIDE
    else:
        left, right = MARGIN_OUTSIDE, MARGIN_GUTTER
    fw = TRIM_W - left - right
    fh = TRIM_H - MARGIN_TOP - MARGIN_BOTTOM
    return Frame(left, MARGIN_BOTTOM, fw, fh, id=f"frame-{page_num}")


# ---------------------------------------------------------------------------
# Page handlers
# ---------------------------------------------------------------------------

def no_decoration(canvas, doc):
    pass


def body_decoration(canvas, doc):
    page_num = doc.page
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    if page_num % 2 == 1:
        x = TRIM_W - MARGIN_OUTSIDE
        canvas.drawRightString(x, MARGIN_BOTTOM - 0.4 * inch, str(page_num))
    else:
        x = MARGIN_OUTSIDE
        canvas.drawString(x, MARGIN_BOTTOM - 0.4 * inch, str(page_num))
    canvas.restoreState()


def cover_bg(canvas, doc, color):
    canvas.saveState()
    canvas.setFillColor(color)
    canvas.rect(0, 0, COVER_W, COVER_H, fill=1, stroke=0)
    canvas.restoreState()


COVER_IMAGE = os.path.join(os.path.dirname(__file__), "the-room-cover.png")


def front_cover_handler(canvas, doc):
    cover_bg(canvas, doc, HexColor("#1a1a2e"))
    if os.path.exists(COVER_IMAGE):
        img_h = COVER_H * 0.25
        img_y = COVER_H * 0.45
        canvas.drawImage(COVER_IMAGE, 0, img_y,
                         width=COVER_W, height=img_h,
                         preserveAspectRatio=False,
                         mask='auto')


BACK_COVER_IMAGE = os.path.join(os.path.dirname(__file__),
                                "the-room-back-cover.png")


def back_cover_handler(canvas, doc):
    cover_bg(canvas, doc, HexColor("#1a1a2e"))
    if os.path.exists(BACK_COVER_IMAGE):
        img_h = COVER_H * 0.25
        img_y = COVER_H * 0.45
        canvas.drawImage(BACK_COVER_IMAGE, 0, img_y,
                         width=COVER_W, height=img_h,
                         preserveAspectRatio=False,
                         mask='auto')

    bio = getattr(doc, '_back_bio', '')
    if bio:
        pad = 0.75 * inch
        max_w = COVER_W - 2 * pad
        bio_font = "Times-Roman"
        bio_size = 8.5
        bio_leading = 12
        y = 1.5 * inch
        lines = _wrap_text(bio, bio_font, bio_size, max_w)
        canvas.setFont(bio_font, bio_size)
        canvas.setFillColor(HexColor("#bbbbbb"))
        for line in lines:
            canvas.drawString(pad, y, line)
            y -= bio_leading


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

CREAM = HexColor("#f5f0e8")
styles = {}

styles["cover_title"] = ParagraphStyle(
    "CoverTitle", fontName="Times-Bold", fontSize=30, leading=36,
    alignment=TA_CENTER, textColor=CREAM)

styles["cover_author"] = ParagraphStyle(
    "CoverAuthor", fontName="Times-Roman", fontSize=14, leading=18,
    alignment=TA_CENTER, textColor=CREAM)

styles["back_blurb"] = ParagraphStyle(
    "BackBlurb", fontName="Times-Italic", fontSize=11, leading=15,
    alignment=TA_CENTER, textColor=HexColor("#cccccc"),
    leftIndent=0.5 * inch, rightIndent=0.5 * inch)

styles["dedication"] = ParagraphStyle(
    "Dedication", fontName="Times-Italic", fontSize=12, leading=18,
    alignment=TA_CENTER)

styles["act_title"] = ParagraphStyle(
    "ActTitle", fontName="Times-Bold", fontSize=20, leading=26,
    alignment=TA_CENTER, spaceBefore=0, spaceAfter=6)

styles["act_subtitle"] = ParagraphStyle(
    "ActSubtitle", fontName="Times-Bold", fontSize=14, leading=20,
    alignment=TA_CENTER, spaceAfter=4)

styles["act_attribution"] = ParagraphStyle(
    "ActAttribution", fontName="Times-Italic", fontSize=10, leading=14,
    alignment=TA_CENTER, spaceAfter=18)

styles["section_head"] = ParagraphStyle(
    "SectionHead", fontName="Times-Bold", fontSize=13, leading=18,
    spaceBefore=18, spaceAfter=10)

styles["subsection_head"] = ParagraphStyle(
    "SubsectionHead", fontName="Times-Bold", fontSize=11, leading=15,
    spaceBefore=12, spaceAfter=6)

styles["body"] = ParagraphStyle(
    "Body", fontName="Times-Roman", fontSize=10, leading=13,
    alignment=TA_JUSTIFY, firstLineIndent=0, spaceAfter=8)

styles["body_first"] = ParagraphStyle(
    "BodyFirst", parent=styles["body"])

styles["blockquote"] = ParagraphStyle(
    "Blockquote", fontName="Times-Italic", fontSize=9.5, leading=13,
    alignment=TA_LEFT, leftIndent=0.35 * inch, rightIndent=0.25 * inch,
    spaceBefore=8, spaceAfter=2)

styles["blockquote_attrib"] = ParagraphStyle(
    "BlockquoteAttrib", fontName="Times-Roman", fontSize=9, leading=12,
    alignment=TA_LEFT, leftIndent=0.35 * inch, rightIndent=0.25 * inch,
    spaceAfter=10)

styles["preface_head"] = ParagraphStyle(
    "PrefaceHead", fontName="Times-Bold", fontSize=16, leading=22,
    alignment=TA_CENTER, spaceAfter=14)

styles["dramatis_head"] = ParagraphStyle(
    "DramatisHead", fontName="Times-Bold", fontSize=12, leading=16,
    spaceBefore=14, spaceAfter=8)

styles["dramatis_entry"] = ParagraphStyle(
    "DramatisEntry", fontName="Times-Roman", fontSize=9.5, leading=13,
    alignment=TA_JUSTIFY, leftIndent=0.15 * inch, spaceAfter=4)

styles["toc_heading"] = ParagraphStyle(
    "TOCHeading", fontName="Times-Bold", fontSize=16, leading=22,
    alignment=TA_CENTER, spaceAfter=30)

styles["copyright"] = ParagraphStyle(
    "Copyright", fontName="Times-Roman", fontSize=8, leading=11,
    alignment=TA_LEFT, spaceAfter=4)

styles["back_quote"] = ParagraphStyle(
    "BackQuote", fontName="Times-Italic", fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=CREAM,
    leftIndent=0.4 * inch, rightIndent=0.4 * inch)

styles["back_author"] = ParagraphStyle(
    "BackAuthor", fontName="Times-Roman", fontSize=8.5, leading=12,
    alignment=TA_JUSTIFY, textColor=HexColor("#bbbbbb"),
    leftIndent=0.4 * inch, rightIndent=0.4 * inch)


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

_hyphenator = pyphen.Pyphen(lang='en_US')
SHY = '\u00AD'


def _soft_hyphenate(text):
    def _hyph_word(word):
        trail = ''
        while word and word[-1] in '.,;:!?\u201d\u2019)]\u2014':
            trail = word[-1] + trail
            word = word[:-1]
        if len(word) < 6 or '<' in word or '&' in word:
            return word + trail
        hyphenated = _hyphenator.inserted(word, SHY)
        parts = hyphenated.split(SHY)
        filtered = [parts[0]]
        for p in parts[1:]:
            if len(filtered[-1]) < 2 or len(p) < 2:
                filtered[-1] += p
            else:
                filtered.append(p)
        return SHY.join(filtered) + trail
    return ' '.join(_hyph_word(w) for w in text.split(' '))


def md_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = text.replace(' <i>', '<i> ')
    text = text.replace(' <b>', '<b> ')
    text = text.replace(" - ", "&nbsp;&ndash; ")
    text = _soft_hyphenate(text)
    return text


def parse_blockquote(lines):
    quote_parts = []
    attrib = None
    for line in lines:
        stripped = re.sub(r'^>\s*', '', line)
        if stripped.startswith('-- ') or stripped.startswith('&ndash; '):
            attrib = stripped
        elif stripped.strip():
            stripped = stripped.strip('"').strip('\u201c\u201d')
            quote_parts.append(stripped)
    return ' '.join(quote_parts), attrib


def _wrap_text(text, font_name, font_size, max_width):
    words = text.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        if stringWidth(test, font_name, font_size) <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines


# ---------------------------------------------------------------------------
# Measurement
# ---------------------------------------------------------------------------

def _measure_flowable(f, avail_w, avail_h):
    if isinstance(f, KeepTogether):
        total = 0
        for inner in f._content:
            _, h = inner.wrap(avail_w, avail_h - total)
            total += h
        return total
    _, h = f.wrap(avail_w, avail_h)
    return h


def calc_chapter_drop(header_flowables, body_flowables):
    frame_w = TRIM_W - MARGIN_GUTTER - MARGIN_OUTSIDE
    frame_h = TRIM_H - MARGIN_TOP - MARGIN_BOTTOM

    header_h = sum(_measure_flowable(f, frame_w, frame_h)
                   for f in header_flowables)

    content_h = header_h
    for f in body_flowables:
        h = _measure_flowable(f, frame_w, frame_h - content_h)
        if content_h + h > frame_h - CHAPTER_DROP_MIN:
            break
        content_h += h

    return (max)(frame_h - content_h, CHAPTER_DROP_MIN)


# ---------------------------------------------------------------------------
# Act parser (generic)
# ---------------------------------------------------------------------------

def build_act(source_path, act_heading, next_heading):
    with open(source_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    if next_heading:
        pattern = rf'^# {re.escape(act_heading)}\s*$(.*?)^# {re.escape(next_heading)}\s*$'
    else:
        pattern = rf'^# {re.escape(act_heading)}\s*$(.*?)(?:<!-- back-cover -->|\Z)'
    match = re.search(pattern, full_text, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Could not find boundaries for {act_heading}")

    lines = match.group(1).split('\n')
    header_parts = [Paragraph(act_heading, styles["act_title"])]
    body_flowables = []

    i = 0
    after_heading = False
    in_act_header = True

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if line.strip() == '<!-- body -->':
            in_act_header = False
            i += 1
            continue

        if line.strip() == '<!-- break -->':
            body_flowables.append(PageBreak())
            i += 1
            continue

        if line.strip() == '<!-- recto -->':
            body_flowables.append(PageBreak())
            body_flowables.append(EnsureOdd())
            i += 1
            continue

        if line.strip() == '---':
            i += 1
            continue

        # Act subtitle (first ## that isn't a numbered section or epilogue)
        if in_act_header and line.startswith('## ') \
                and not re.match(r'^## [IVXLC]+\.', line) \
                and not line.startswith('## Epilogue'):
            title = md_inline(line[3:].strip())
            header_parts.append(Paragraph(title, styles["act_subtitle"]))
            i += 1
            continue

        # Act attribution line
        if in_act_header and line.startswith('*') and line.endswith('*'):
            text = md_inline(line.strip('*'))
            header_parts.append(Paragraph(text, styles["act_attribution"]))
            in_act_header = False
            i += 1
            continue

        # ### subheading (Act Two has numbered subsections)
        if line.startswith('### '):
            in_act_header = False
            title = md_inline(line[4:].strip())
            body_flowables.append(
                Paragraph(title, styles["subsection_head"]))
            after_heading = True
            i += 1
            continue

        # ## Section heading - keep with blockquote + first paragraph
        if line.startswith('## '):
            in_act_header = False
            title = md_inline(line[3:].strip())
            section_group = [
                Spacer(1, 6),
                Paragraph(title, styles["section_head"]),
            ]
            i += 1

            while i < len(lines) and (not lines[i].strip()
                                       or lines[i].strip() == '---'):
                i += 1

            if i < len(lines) and lines[i].startswith('>'):
                bq_lines = []
                while i < len(lines) and (
                        lines[i].startswith('>') or
                        (lines[i].strip() == '' and
                         i + 1 < len(lines) and
                         lines[i + 1].startswith('>'))):
                    bq_lines.append(md_inline(lines[i].rstrip()))
                    i += 1
                qt, at = parse_blockquote(bq_lines)
                if qt:
                    section_group.append(
                        Paragraph(f"\u201c{qt}\u201d", styles["blockquote"]))
                if at:
                    section_group.append(
                        Paragraph(at, styles["blockquote_attrib"]))

            while i < len(lines) and not lines[i].strip():
                i += 1

            if i < len(lines) and lines[i].strip() \
                    and not lines[i].startswith('#'):
                para_lines = []
                while i < len(lines) and lines[i].strip():
                    para_lines.append(lines[i].rstrip())
                    i += 1
                if para_lines:
                    text = md_inline(' '.join(para_lines))
                    section_group.append(
                        Paragraph(text, styles["body_first"]))

            body_flowables.append(KeepTogether(section_group))
            after_heading = False
            continue

        # Standalone blockquote
        if line.startswith('>'):
            bq_lines = []
            while i < len(lines) and (
                    lines[i].startswith('>') or
                    (lines[i].strip() == '' and
                     i + 1 < len(lines) and
                     lines[i + 1].startswith('>'))):
                bq_lines.append(md_inline(lines[i].rstrip()))
                i += 1
            qt, at = parse_blockquote(bq_lines)
            if qt:
                body_flowables.append(
                    Paragraph(f"\u201c{qt}\u201d", styles["blockquote"]))
            if at:
                body_flowables.append(
                    Paragraph(at, styles["blockquote_attrib"]))
            after_heading = True
            continue

        # Body paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip():
            para_lines.append(lines[i].rstrip())
            i += 1

        if para_lines:
            text = md_inline(' '.join(para_lines))
            style = styles["body_first"] if after_heading else styles["body"]
            body_flowables.append(KeepTogether([Paragraph(text, style)]))
            after_heading = False

    drop = calc_chapter_drop(header_parts, body_flowables)
    return [Spacer(1, drop)] + header_parts + body_flowables


# ---------------------------------------------------------------------------
# Preface parser
# ---------------------------------------------------------------------------

def build_overview_table(table_lines):
    header_style = ParagraphStyle(
        "TblHeader", fontName="Times-Bold", fontSize=9,
        leading=12, alignment=TA_LEFT)
    cell_style = ParagraphStyle(
        "TblCell", fontName="Times-Roman", fontSize=9,
        leading=12, alignment=TA_LEFT)
    cell_bold = ParagraphStyle(
        "TblCellBold", fontName="Times-Bold", fontSize=9,
        leading=12, alignment=TA_LEFT)

    rows = []
    is_header = True
    for line in table_lines:
        if '---' in line:
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) < 2:
            continue
        if is_header:
            rows.append([Paragraph(md_inline(c), header_style)
                         for c in cells])
            is_header = False
        else:
            row = [Paragraph(md_inline(c),
                             cell_bold if j == 0 else cell_style)
                   for j, c in enumerate(cells)]
            rows.append(row)

    t = Table(rows, colWidths=[1.15 * inch, 1.15 * inch, 1.7 * inch],
              hAlign='CENTER')
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, black),
        ('LINEBELOW', (0, -1), (-1, -1), 0.5, black),
    ]))
    return t


def build_preface(source_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    match = re.search(r'^## Preface\s*$(.*?)^# Act One\s*$',
                      full_text, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError("Could not find Preface")

    lines = match.group(1).split('\n')
    flowables = []
    flowables.append(Spacer(1, CHAPTER_DROP_MIN + 0.75 * inch))
    flowables.append(Paragraph("Preface", styles["preface_head"]))

    i = 0
    after_heading = True
    dramatis_group = []
    in_dramatis = False
    next_table_is_real = False

    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue
        if line.strip() == '<!-- break -->':
            flowables.append(PageBreak())
            i += 1
            continue
        if line.strip() == '<!-- recto -->':
            flowables.append(PageBreak())
            flowables.append(EnsureOdd())
            i += 1
            continue
        if line.strip() == '<!-- table -->':
            next_table_is_real = True
            i += 1
            continue
        if line.strip() == '---':
            i += 1
            continue

        if line.startswith('|'):
            tbl_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                tbl_lines.append(lines[i].rstrip())
                i += 1
            if next_table_is_real:
                t = build_overview_table(tbl_lines)
                flowables.append(Spacer(1, 6))
                flowables.append(KeepTogether([t, Spacer(1, 8)]))
                next_table_is_real = False
            else:
                skipped_header = False
                for tl in tbl_lines:
                    if '---' in tl:
                        continue
                    if not skipped_header:
                        skipped_header = True
                        continue
                    cells = [c.strip() for c in tl.split('|')[1:-1]]
                    if len(cells) >= 2:
                        text = md_inline(
                            f"<b>{cells[0]}</b> &ndash; "
                            f"{' &ndash; '.join(cells[1:])}")
                        entry = Paragraph(text, styles["dramatis_entry"])
                        if in_dramatis:
                            dramatis_group.append(entry)
                        else:
                            flowables.append(entry)
            continue

        if line.startswith('### '):
            title = md_inline(line[4:].strip())
            in_dramatis = True
            dramatis_group.append(Spacer(1, 6))
            dramatis_group.append(
                Paragraph(title, styles["dramatis_head"]))
            after_heading = True
            i += 1
            continue

        if line.startswith('- '):
            text = md_inline(line[2:].strip())
            p = Paragraph(text, styles["dramatis_entry"])
            if in_dramatis:
                dramatis_group.append(p)
            else:
                flowables.append(p)
            i += 1
            continue

        para_lines = []
        while i < len(lines) and lines[i].strip() \
                and not lines[i].startswith('|') \
                and not lines[i].startswith('#') \
                and not lines[i].startswith('-'):
            para_lines.append(lines[i].rstrip())
            i += 1

        if para_lines:
            text = md_inline(' '.join(para_lines))
            style = styles["body_first"] if after_heading else styles["body"]
            p = Paragraph(text, style)
            if in_dramatis:
                dramatis_group.append(p)
            else:
                flowables.append(p)
            after_heading = False

    if dramatis_group:
        flowables.append(KeepTogether(dramatis_group))

    return flowables


# ---------------------------------------------------------------------------
# PDF assembly
# ---------------------------------------------------------------------------

def parse_back_cover(source_path):
    """Parse back cover sections from <!-- back-cover --> to end of file."""
    with open(source_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    match = re.search(r'<!-- back-cover -->.*?## Back Cover\s*\n(.*)',
                      full_text, re.DOTALL)
    if not match:
        return None, None, None

    text = match.group(1)
    blurb, quote, author_bio = '', '', ''

    parts = re.split(r'<!-- back-(?:quote|author) -->', text)
    if len(parts) >= 1:
        blurb = parts[0].strip()
    if len(parts) >= 2:
        quote = parts[1].strip()
    if len(parts) >= 3:
        raw = parts[2].strip()
        raw = re.sub(r'\*\*(.+?)\*\*', r'\1', raw)
        author_bio = raw

    return blurb, quote, author_bio


ACTS = [
    ("Act One",   "Act Two"),
    ("Act Two",   "Act Three"),
    ("Act Three", "Act Four"),
    ("Act Four",  "Act Five"),
    ("Act Five",  "Act Six"),
    ("Act Six",   None),
]


def parse_metadata(source_path):
    """Extract title, subtitle, author, dedication from markdown."""
    with open(source_path, 'r', encoding='utf-8') as f:
        text = f.read()

    title_m = re.search(r'^# (.+)$', text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else "Untitled"

    sub_m = re.search(r'<!-- subtitle:\s*(.+?)\s*-->', text)
    subtitle = sub_m.group(1).strip() if sub_m else ""

    auth_m = re.search(r'<!-- author:\s*(.+?)\s*-->', text)
    author = auth_m.group(1).strip() if auth_m else ""

    ded_m = re.search(r'<!-- dedication:\s*(.+?)\s*-->', text)
    dedication_lines = []
    if ded_m:
        dedication_lines = [l.strip() for l in ded_m.group(1).split('/')]

    copy_m = re.search(r'<!-- copyright -->\s*\n(.*?)(?=\n---|\n<!-- |\n## |\n# )',
                        text, re.DOTALL)
    copyright_lines = []
    if copy_m:
        copyright_lines = [l.strip() for l in copy_m.group(1).strip().split('\n')
                           if l.strip()]

    return title, subtitle, author, dedication_lines, copyright_lines


def build_book(source_path, output_path):
    doc = BookDocTemplate(
        output_path,
        pagesize=(TRIM_W, TRIM_H),
        leftMargin=MARGIN_GUTTER,
        rightMargin=MARGIN_OUTSIDE,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
    )

    cover_frame = Frame(0.5 * inch, 0.5 * inch,
                        COVER_W - 1.0 * inch, COVER_H - 1.0 * inch,
                        id="cover-text")

    templates = [
        PageTemplate(id="front_cover", frames=[cover_frame],
                     onPage=front_cover_handler,
                     pagesize=(COVER_W, COVER_H)),
        PageTemplate(id="back_cover", frames=[cover_frame],
                     onPage=back_cover_handler,
                     pagesize=(COVER_W, COVER_H)),
        PageTemplate(id="blank", frames=[make_frame(2)],
                     onPage=no_decoration),
        PageTemplate(id="frontmatter", frames=[make_frame(1)],
                     onPage=no_decoration),
        PageTemplate(id="odd", frames=[make_frame(1)],
                     onPage=body_decoration),
        PageTemplate(id="even", frames=[make_frame(2)],
                     onPage=body_decoration),
    ]
    doc.addPageTemplates(templates)

    title, subtitle, author, dedication_lines, copyright_lines = \
        parse_metadata(source_path)

    story = []

    # -- Front cover --
    story.append(NextPageTemplate("blank"))
    story.append(Spacer(1, 1.25 * inch))
    story.append(Paragraph(title, styles["cover_title"]))
    story.append(Spacer(1, 3.9 * inch))
    story.append(Paragraph(author, styles["cover_author"]))
    story.append(PageBreak())

    # -- Blank verso --
    story.append(NextPageTemplate("frontmatter"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # -- Title page (recto) --
    story.append(NextPageTemplate("blank"))
    int_title = ParagraphStyle(
        "IntTitle", parent=styles["act_title"],
        fontSize=24, leading=30, textColor=black)
    int_subtitle = ParagraphStyle(
        "IntSubtitle", parent=styles["act_subtitle"],
        fontName="Times-Italic", textColor=black)
    int_author = ParagraphStyle(
        "IntAuthor", fontName="Times-Roman", fontSize=12, leading=16,
        alignment=TA_CENTER)
    story.append(Spacer(1, 2.0 * inch))
    story.append(Paragraph(title, int_title))
    story.append(Spacer(1, 0.15 * inch))
    if subtitle:
        story.append(Paragraph(subtitle, int_subtitle))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(author, int_author))
    story.append(PageBreak())

    # -- Copyright page (verso of title page, text at bottom) --
    story.append(NextPageTemplate("frontmatter"))
    if copyright_lines:
        copyright_block = [Paragraph(cl, styles["copyright"])
                           for cl in copyright_lines]
        story.append(Spacer(1, 5.0 * inch))
        story.extend(copyright_block)
    else:
        story.append(Spacer(1, 1))
    story.append(PageBreak())

    # -- Dedication (recto) --
    story.append(NextPageTemplate("blank"))
    story.append(Spacer(1, 2.5 * inch))
    for dline in dedication_lines:
        story.append(Paragraph(dline, styles["dedication"]))
    story.append(PageBreak())

    # -- Blank verso --
    story.append(NextPageTemplate("frontmatter"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # -- Contents (recto) --
    story.append(NextPageTemplate("blank"))
    story.append(Spacer(1, 0.75 * inch))
    story.append(Paragraph("Contents", styles["toc_heading"]))

    toc_num_s = ParagraphStyle(
        "TOCNum", fontName="Times-Roman", fontSize=26,
        leading=30, alignment=TA_RIGHT)
    toc_name_s = ParagraphStyle(
        "TOCName", fontName="Times-Italic", fontSize=13,
        leading=17, alignment=TA_LEFT)
    toc_entries = [
        ("I",   "Niccol\u00f2 Machiavelli",          "the uncounted"),
        ("II",  "Friedrich Nietzsche",               "the unnamed"),
        ("III", "Franz Kafka",                       "the unseen"),
        ("IV",  "Elias Canetti",                     "the unasked"),
        ("V",   "?",                                 "the undiscovered"),
        ("VI",  "Charles-Maurice<br/>de Talleyrand", "the unheard"),
    ]
    toc_rows = []
    for numeral, author_name, word in toc_entries:
        name_and_word = Paragraph(
            f"{author_name}<br/><font size='10' color='#666666'>"
            f"{word}</font>",
            toc_name_s)
        toc_rows.append([
            Paragraph(numeral, toc_num_s),
            name_and_word,
        ])
    toc_table = Table(toc_rows, colWidths=[0.8 * inch, 2.25 * inch],
                      hAlign='CENTER')
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (0, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 14),
    ]))
    story.append(Indenter(left=0.3 * inch))
    story.append(toc_table)
    story.append(Indenter(left=-0.3 * inch))
    story.append(PageBreak())

    # -- Blank verso --
    story.append(NextPageTemplate("odd"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # -- Preface --
    story.extend(build_preface(source_path))
    story.append(PageBreak())

    # -- All six acts --
    for act_name, next_name in ACTS:
        story.append(EnsureOdd())
        story.extend(build_act(source_path, act_name, next_name))
        story.append(PageBreak())

    # -- End matter --
    story.append(EnsureOdd())
    story.append(NextPageTemplate("blank"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())

    # -- Back cover --
    blurb, quote, author_bio = parse_back_cover(source_path)
    doc._back_bio = author_bio or ''

    story.append(NextPageTemplate("back_cover"))
    story.append(Spacer(1, 1))
    story.append(PageBreak())
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph(blurb, styles["back_blurb"]))
    story.append(Spacer(1, 4.8 * inch))
    if quote:
        story.append(Paragraph(md_inline(quote), styles["back_quote"]))

    doc.build(story)
    print(f"PDF written to: {output_path}")
    print(f"Total pages: {doc.page}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    src = os.path.join(os.path.dirname(__file__), "the-room.md")
    out = os.path.join(os.path.dirname(__file__), "the-room.pdf")
    build_book(src, out)
