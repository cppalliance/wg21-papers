// Lays out A Young Delegate's Notebook for print from the ICML stories that
// build.py writes, saves the InDesign document, and exports two PDFs: one for
// the printer with no live links, and one for reading on screen with live
// links. Link text is blue in both.
//
// Every run starts from a blank document, so the print look lives in the
// spec below and nowhere else. Edits made by hand in InDesign are lost on
// the next run. The style names must match ICML_PARAGRAPHS, ICML_CHARACTERS,
// and the box labels in build.py.
//
// Run `python indesign.py` from the book root, or run this file from the
// InDesign Scripts panel. ExtendScript is ES3: no let, no arrow functions,
// no Array.forEach or indexOf, no JSON.

// ---- spec ---------------------------------------------------------------

var OUTPUT = "young-delegates-notebook";

// points, 72 to the inch: a 5.5 by 8.5 inch page
var PAGE = {width: 396, height: 612, top: 45, bottom: 54, inside: 54, outside: 36};

// the cover picture, in the same folder as the ICML files. It fills the first
// page, cropped to the page's shape and centered, and the page behind it
// stays blank. Leave the file out and the book has no cover.
var COVER = {file: "cover.jpg"};

// the folio's frame, measured down from the bottom of the text area
var FOLIO = {gap: 14, height: 14};

// how far chapter titles and the contents title sit below the top margin
var CHAPTER_SINK = 84;

// the first family that has every listed style wins
var FONTS = {
    serif: {families: ["Source Serif Variable", "Georgia"], styles: ["Regular", "Italic"]},
    sans: {families: ["Myriad Pro", "Source Sans Variable"], styles: ["Regular", "Italic", "Bold", "Bold Italic"]},
    mono: {families: ["Source Code Variable", "Consolas"], styles: ["Regular"]}
};

// swatch name -> RGB in hex, the same colors as the docx. A color interior
// costs more to print than a black and white one.
var COLORS = {
    "Navy": "1f3864", "Heading Blue": "2f5496", "Subheading Blue": "1f4d78",
    "Quote Gray": "404040", "Code Green": "188038", "Link Blue": "1155cc"
};

// box label -> fill, rule, and label colors as RGB in hex. Every box sets its
// text the same way, in BOX_PANEL.
var BOXES = {
    "In This Chapter": {fill: "e8f0fa", rule: "2f5496", label: "1f3864"},
    "The Short Version": {fill: "e8eef6", rule: "1f3864", label: "1f3864"},
    "Rule of Thumb": {fill: "e9f5e9", rule: "38761d", label: "274e13"},
    "Watch Out": {fill: "fdece4", rule: "c0392b", label: "922b21"},
    "Try This Today": {fill: "e4f4f4", rule: "0b7285", label: "0b5563"}
};

// hand fixes for single page breaks: each paragraph that starts with one of
// these goes to the next page whole rather than split. Straight apostrophes
// match curly ones. An edit that moves the break can make an entry stale,
// and the run reports any entry whose paragraph is gone.
var KEEP_WHOLE = [
    "It's a veto over what you can use"
];

var PRINT_PRESETS = ["[PDF/X-4:2008]", "[High Quality Print]"];
var SCREEN_PRESET = "[High Quality Print]";

// [name, based on, settings]. "font" names a FONTS entry. Strings in *Color
// settings name swatches. Enumerations are InDesign's own.
// Body paragraphs are blocks half a line apart with no indent, like the docx.
// For indented paragraphs instead, give Body a firstLineIndent of 12 and a
// spaceBefore of 0, and give Body First, Body After Break, and Body After Box
// a firstLineIndent of 0.
// Space before adds to the space after of the paragraph above, and is
// dropped at the top of a frame.
var PARAGRAPH_STYLES = [
    ["Body", null, {
        font: "serif", fontStyle: "Regular", pointSize: 10.5, leading: 14.5,
        justification: Justification.LEFT_JUSTIFIED, firstLineIndent: 0,
        leftIndent: 0, rightIndent: 0, spaceBefore: 7, spaceAfter: 0,
        hyphenation: true, hyphenateCapitalizedWords: false, hyphenateLastWord: false,
        hyphenateWordsLongerThan: 6, hyphenateAfterFirst: 3, hyphenateBeforeLast: 3, hyphenateLadderLimit: 2,
        hyphenateAcrossColumns: false,
        keepLinesTogether: true, keepFirstLines: 2, keepLastLines: 2
    }],
    ["Body First", "Body", {spaceBefore: 0}],
    ["Body After Break", "Body", {}],
    ["Body After Box", "Body", {spaceBefore: 12}],
    ["Chapter Title", "Body", {
        font: "sans", fontStyle: "Bold", pointSize: 20, leading: 24, fillColor: "Navy",
        justification: Justification.LEFT_ALIGN, firstLineIndent: 0, hyphenation: false,
        startParagraph: StartParagraph.NEXT_ODD_PAGE,
        spaceBefore: 0, spaceAfter: 30, keepAllLinesTogether: true, keepWithNext: 2
    }],
    ["Section Heading", "Body", {
        font: "sans", fontStyle: "Bold", pointSize: 11.5, leading: 14, fillColor: "Heading Blue",
        justification: Justification.LEFT_ALIGN, firstLineIndent: 0, hyphenation: false,
        spaceBefore: 18, spaceAfter: 4, keepAllLinesTogether: true, keepWithNext: 2
    }],
    ["Subsection Heading", "Section Heading", {
        fontStyle: "Bold Italic", pointSize: 10.5, fillColor: "Subheading Blue", spaceBefore: 12, spaceAfter: 2
    }],
    ["Bullet", "Body", {
        justification: Justification.LEFT_ALIGN, leftIndent: 16, firstLineIndent: -10, spaceBefore: 3,
        bulletsAndNumberingListType: ListType.BULLET_LIST
    }],
    ["Number", "Bullet", {
        leftIndent: 18, firstLineIndent: -13,
        bulletsAndNumberingListType: ListType.NUMBERED_LIST
    }],
    ["Epigraph", "Body", {
        fontStyle: "Italic", pointSize: 10, leading: 13.5, fillColor: "Quote Gray", justification: Justification.LEFT_ALIGN,
        firstLineIndent: 0, leftIndent: 18, rightIndent: 18, spaceBefore: 0, spaceAfter: 6
    }],
    ["Epigraph Source", "Epigraph", {fontStyle: "Regular", pointSize: 9, leading: 12, justification: Justification.RIGHT_ALIGN, spaceAfter: 23}],
    ["Title", "Body", {
        font: "sans", fontStyle: "Bold", pointSize: 26, leading: 30, fillColor: "Navy",
        justification: Justification.CENTER_ALIGN, firstLineIndent: 0, spaceBefore: 0, hyphenation: false, balanceRaggedLines: true
    }],
    ["Subtitle", "Title", {font: "serif", fontStyle: "Italic", pointSize: 13, leading: 17, fillColor: "Black", spaceBefore: 14}],
    ["Contents Title", "Chapter Title", {startParagraph: StartParagraph.ANYWHERE}],
    ["Contents Entry", "Body", {justification: Justification.LEFT_ALIGN, firstLineIndent: 0, leading: 19, spaceBefore: 0, hyphenation: false}],
    ["Folio", "Body", {pointSize: 9, leading: 12, justification: Justification.CENTER_ALIGN, firstLineIndent: 0, spaceBefore: 0}]
];

// shared by every paragraph of every box, so the shading and the rule merge
// into one panel per box, and the keeps hold each box on one page.
// keepAllLinesTogether does nothing unless keepLinesTogether is on.
var BOX_PANEL = {
    font: "sans", fontStyle: "Regular", pointSize: 9, leading: 12.5,
    justification: Justification.LEFT_ALIGN, firstLineIndent: 0, leftIndent: 12, rightIndent: 10,
    spaceBefore: 0, spaceAfter: 3, hyphenation: false,
    keepLinesTogether: true, keepAllLinesTogether: true, keepWithNext: 1,
    paragraphShadingOn: true, paragraphShadingTint: 100,
    paragraphShadingWidth: ParagraphShadingWidthEnum.COLUMN_WIDTH,
    paragraphShadingTopOrigin: ParagraphShadingTopOriginEnum.ASCENT_TOP_ORIGIN,
    paragraphShadingBottomOrigin: ParagraphShadingBottomOriginEnum.DESCENT_BOTTOM_ORIGIN,
    paragraphShadingTopOffset: 7, paragraphShadingBottomOffset: 7,
    paragraphShadingLeftOffset: 0, paragraphShadingRightOffset: 0,
    paragraphBorderOn: true, paragraphBorderTint: 100,
    paragraphBorderLeftLineWeight: 2.5, paragraphBorderTopLineWeight: 0,
    paragraphBorderRightLineWeight: 0, paragraphBorderBottomLineWeight: 0,
    paragraphBorderWidth: ParagraphShadingWidthEnum.COLUMN_WIDTH,
    paragraphBorderTopOrigin: ParagraphBorderTopOriginEnum.ASCENT_TOP_ORIGIN,
    paragraphBorderBottomOrigin: ParagraphBorderBottomOriginEnum.DESCENT_BOTTOM_ORIGIN,
    paragraphBorderTopOffset: 7, paragraphBorderBottomOffset: 7,
    paragraphBorderLeftOffset: 0, paragraphBorderRightOffset: 0,
    mergeConsecutiveParaBorders: true, paragraphBorderDisplayIfSplits: true
};
// the label's spaceBefore and the spaceBefore of Body After Box leave about
// the same white above and below a box, after the 7 pt shading offsets
var BOX_LABEL = {fontStyle: "Bold", pointSize: 7.5, leading: 11, capitalization: Capitalization.ALL_CAPS, tracking: 80, spaceBefore: 17, spaceAfter: 4, keepWithNext: 2};
var BOX_BULLET = {leftIndent: 22, firstLineIndent: -10, bulletsAndNumberingListType: ListType.BULLET_LIST};

// [name, based on, settings]. A link is blue with no underline, in print and
// on screen. A link's code stays green in print, like any other code.
var CHARACTER_STYLES = [
    ["Emphasis", null, {fontStyle: "Italic"}],
    ["Code", null, {font: "mono", fontStyle: "Regular", fillColor: "Code Green"}],
    ["Link", null, {fillColor: "Link Blue"}],
    ["Link Emphasis", "Link", {fontStyle: "Italic"}],
    ["Link Code", "Link", {font: "mono", fontStyle: "Regular", fillColor: "Code Green"}]
];
// applied to every link style for the on-screen PDF only. Print already sets
// links blue, so this only turns a link's code blue too.
var SCREEN_LINK = {fillColor: "Link Blue"};

// ---- layout -------------------------------------------------------------

var problems = [];

// a crash in InDesign ends the run with no message, so each finished step is
// written to the file named by the "log" script arg
function trace(s) {
    if (!app.scriptArgs.isDefined("log")) return;
    var f = File(app.scriptArgs.getValue("log"));
    f.open("a");
    f.writeln(new Date().toTimeString().slice(0, 8) + " " + s);
    f.close();
}

function problem(what, e) {
    problems.push(what + ": " + (e && e.message ? e.message : e));
}

function merge(a, b) {
    var r = {}, k;
    for (k in a) r[k] = a[k];
    for (k in b) r[k] = b[k];
    return r;
}

function pickFonts() {
    var picked = {};
    for (var key in FONTS) {
        var spec = FONTS[key];
        for (var i = 0; i < spec.families.length && !picked[key]; i++) {
            var complete = true;
            for (var j = 0; j < spec.styles.length; j++) {
                if (!app.fonts.itemByName(spec.families[i] + "\t" + spec.styles[j]).isValid) complete = false;
            }
            if (complete) picked[key] = spec.families[i];
        }
        if (!picked[key]) throw new Error("no " + key + " font installed, tried " + spec.families.join(", "));
    }
    return picked;
}

// "font" goes first in every settings object, because setting a family can
// reset the style that was set before it
function apply(doc, style, settings, fonts) {
    for (var key in settings) {
        var value = settings[key], target = key;
        if (key == "font") {
            target = "appliedFont";
            value = fonts[value];
        } else if (/Color$/.test(key) && typeof value == "string") {
            value = doc.swatches.itemByName(value);
        }
        try {
            style[target] = value;
        } catch (e) {
            problem(style.name + "." + key, e);
        }
    }
}

// hex is RGB, as in "1f3864"
function addColor(doc, name, hex) {
    var value = [];
    for (var i = 0; i < 6; i += 2) value.push(parseInt(hex.substr(i, 2), 16));
    doc.colors.add({name: name, model: ColorModel.PROCESS, space: ColorSpace.RGB, colorValue: value});
}

function textBounds(page) {
    var b = page.bounds, recto = page.side == PageSideOptions.RIGHT_HAND;
    return [b[0] + PAGE.top, b[1] + (recto ? PAGE.inside : PAGE.outside),
        b[2] - PAGE.bottom, b[3] - (recto ? PAGE.outside : PAGE.inside)];
}

function makeStyles(doc, fonts) {
    var i, style;
    for (var name in COLORS) addColor(doc, name, COLORS[name]);
    for (i = 0; i < PARAGRAPH_STYLES.length; i++) {
        style = doc.paragraphStyles.add({name: PARAGRAPH_STYLES[i][0]});
        if (PARAGRAPH_STYLES[i][1]) style.basedOn = doc.paragraphStyles.itemByName(PARAGRAPH_STYLES[i][1]);
        apply(doc, style, PARAGRAPH_STYLES[i][2], fonts);
    }
    doc.paragraphStyles.itemByName("Contents Entry").tabStops.add({
        alignment: TabStopAlignment.RIGHT_ALIGN, position: PAGE.width - PAGE.inside - PAGE.outside
    });
    for (var label in BOXES) {
        var box = BOXES[label];
        addColor(doc, label + " Fill", box.fill);
        addColor(doc, label + " Rule", box.rule);
        addColor(doc, label + " Label", box.label);
        var panel = merge(BOX_PANEL, {paragraphShadingColor: label + " Fill", paragraphBorderColor: label + " Rule"});
        var kinds = [
            ["Label", merge(merge(panel, BOX_LABEL), {fillColor: label + " Label"})],
            ["Text", panel], ["Bullet", merge(panel, BOX_BULLET)]
        ];
        for (var k = 0; k < kinds.length; k++) {
            style = doc.paragraphStyles.add({name: label + " " + kinds[k][0]});
            apply(doc, style, kinds[k][1], fonts);
        }
    }
    for (i = 0; i < CHARACTER_STYLES.length; i++) {
        style = doc.characterStyles.add({name: CHARACTER_STYLES[i][0]});
        if (CHARACTER_STYLES[i][1]) style.basedOn = doc.characterStyles.itemByName(CHARACTER_STYLES[i][1]);
        apply(doc, style, CHARACTER_STYLES[i][2], fonts);
    }
}

// the ICML can bring in styles of its own; any that the spec doesn't define
// would print in InDesign's defaults
function checkStyles(doc) {
    var known = {"[No Paragraph Style]": 1, "[Basic Paragraph]": 1, "[None]": 1}, i;
    for (i = 0; i < PARAGRAPH_STYLES.length; i++) known[PARAGRAPH_STYLES[i][0]] = 1;
    for (i = 0; i < CHARACTER_STYLES.length; i++) known[CHARACTER_STYLES[i][0]] = 1;
    for (var label in BOXES) known[label + " Label"] = known[label + " Text"] = known[label + " Bullet"] = 1;
    var all = doc.allParagraphStyles.concat(doc.allCharacterStyles);
    for (i = 0; i < all.length; i++) {
        if (!known[all[i].name]) problem("style missing from the spec", all[i].name);
    }
}

function makeMaster(doc) {
    var master = doc.masterSpreads[0];
    master.baseName = "Body";
    for (var i = 0; i < master.pages.length; i++) {
        var page = master.pages[i], t = textBounds(page);
        var folio = page.textFrames.add({
            geometricBounds: [t[2] + FOLIO.gap, t[1], t[2] + FOLIO.gap + FOLIO.height, t[3]]
        });
        folio.insertionPoints[0].contents = SpecialCharacters.AUTO_PAGE_NUMBER;
        folio.paragraphs[0].appliedParagraphStyle = doc.paragraphStyles.itemByName("Folio");
    }
    return master;
}

// adds a page and a threaded frame until the story fits. A chapter that must
// start on a right-hand page leaves the frame before it empty.
function flow(doc, frame, master) {
    while (frame.overflows) {
        if (doc.pages.length > 600) throw new Error("the body still overflows at 600 pages");
        var page = doc.pages.add(LocationOptions.AT_END, undefined, {appliedMaster: master});
        var next = page.textFrames.add({geometricBounds: textBounds(page)});
        frame.nextTextFrame = next;
        frame = next;
    }
}

// a paragraph ending in a colon right before a box introduces it, like the
// motto and the oath, so it goes to the next page with the box. The
// KEEP_WHOLE paragraphs never split. Changing overset text can crash
// InDesign, so this runs once the story has flowed.
function keepTogether(doc, story, master) {
    var paras = story.paragraphs.everyItem().getElements();
    var styles = story.paragraphs.everyItem().appliedParagraphStyle;
    var texts = story.paragraphs.everyItem().contents;
    var found = [], i, j;
    for (i = 0; i < paras.length; i++) {
        if (i + 1 < paras.length && / Label$/.test(styles[i + 1].name) && /:\s*$/.test(texts[i])) paras[i].keepWithNext = 1;
        var plain = String(texts[i]).replace(/[\u2018\u2019]/g, "'");
        for (j = 0; j < KEEP_WHOLE.length; j++) {
            if (plain.indexOf(KEEP_WHOLE[j]) != 0) continue;
            paras[i].keepAllLinesTogether = true;
            found[j] = true;
        }
    }
    for (j = 0; j < KEEP_WHOLE.length; j++) {
        if (!found[j]) problem("KEEP_WHOLE", "no paragraph starts with \"" + KEEP_WHOLE[j] + "\"");
    }
    flow(doc, story.textContainers[story.textContainers.length - 1], master);
}

// InDesign drops space before at the top of a frame, so each chapter's
// opening frame gets a top inset instead. Each inset pushes later text down,
// so the pages are reflowed before the next chapter's frame is looked up.
function sinkChapters(doc, story, master) {
    var paras = story.paragraphs.everyItem().getElements();
    var styles = story.paragraphs.everyItem().appliedParagraphStyle;
    for (var i = 0; i < paras.length; i++) {
        if (styles[i].name != "Chapter Title") continue;
        paras[i].parentTextFrames[0].textFramePreferences.insetSpacing = [CHAPTER_SINK, 0, 0, 0];
        flow(doc, story.textContainers[story.textContainers.length - 1], master);
    }
}

// the contents lists chapter titles only. Each entry links to its chapter,
// and each chapter gets a bookmark, for the on-screen PDF.
function contents(doc, story, page) {
    var entries = [], paras = story.paragraphs.everyItem().getElements(), i;
    var styles = story.paragraphs.everyItem().appliedParagraphStyle;
    for (i = 0; i < paras.length; i++) {
        if (styles[i].name != "Chapter Title") continue;
        entries.push({
            title: paras[i].contents.replace(/\r$/, ""),
            page: paras[i].parentTextFrames[0].parentPage.name,
            para: paras[i]
        });
    }
    var lines = ["Contents"];
    for (i = 0; i < entries.length; i++) lines.push(entries[i].title + "\t" + entries[i].page);
    var frame = page.textFrames.add({geometricBounds: textBounds(page)});
    frame.textFramePreferences.insetSpacing = [CHAPTER_SINK, 0, 0, 0];
    frame.contents = lines.join("\r");
    frame.paragraphs.everyItem().appliedParagraphStyle = doc.paragraphStyles.itemByName("Contents Entry");
    frame.paragraphs[0].appliedParagraphStyle = doc.paragraphStyles.itemByName("Contents Title");
    if (frame.overflows) problem("contents", "the list doesn't fit on one page");
    for (i = 0; i < entries.length; i++) {
        var dest = doc.hyperlinkTextDestinations.add(entries[i].para.insertionPoints[0], {name: "chapter-" + (i + 1)});
        var source = doc.hyperlinkTextSources.add(frame.paragraphs[i + 1].texts[0]);
        doc.hyperlinks.add(source, dest, {name: "contents-" + (i + 1), visible: false});
        doc.bookmarks.add(dest, {name: entries[i].title});
    }
    return entries.length;
}

function firstPreset(names) {
    for (var i = 0; i < names.length; i++) {
        var preset = app.pdfExportPresets.itemByName(names[i]);
        if (preset.isValid) return preset;
    }
    throw new Error("no PDF preset found, tried " + names.join(", "));
}

// a copy of SCREEN_PRESET with links and bookmarks on. Some preset
// properties are read-only, so copying them is allowed to fail.
function screenPreset() {
    var name = "Young Delegate's Notebook screen", old = app.pdfExportPresets.itemByName(name);
    if (old.isValid) old.remove();
    var base = firstPreset([SCREEN_PRESET]).properties, preset = app.pdfExportPresets.add({name: name});
    for (var key in base) {
        if (key == "name") continue;
        try {
            preset[key] = base[key];
        } catch (e) {}
    }
    preset.properties = {includeHyperlinks: true, includeBookmarks: true, exportReaderSpreads: false, viewPDF: false};
    return preset;
}

function closeOpen(file) {
    for (var i = app.documents.length - 1; i >= 0; i--) {
        var doc = app.documents[i];
        try {
            if (doc.fullName.fsName == file.fsName) doc.close(SaveOptions.NO);
        } catch (e) {}  // a document that was never saved has no fullName
    }
}

function layout(src, out) {
    var title = File(src + "/title.icml"), body = File(src + "/body.icml");
    if (!body.exists || !title.exists) throw new Error("no ICML in " + src + ", run python build.py first");
    Folder(out).create();
    var indd = File(out + "/" + OUTPUT + ".indd");
    closeOpen(indd);

    var cover = File(src + "/" + COVER.file);
    if (!cover.exists) cover = null;
    var fonts = pickFonts();
    var doc = app.documents.add(false);
    try {
        return typeset(doc, fonts, title, body, indd, out, cover);
    } finally {
        doc.close(SaveOptions.NO);
    }
}

// puts the cover picture on the first page, scaled to fill it and centered
function placeCover(doc, file) {
    var page = doc.pages[0], b = page.bounds;
    var rect = page.rectangles.add({geometricBounds: b});
    rect.strokeWeight = 0;
    rect.place(file);
    rect.fit(FitOptions.FILL_PROPORTIONALLY);
    rect.fit(FitOptions.CENTER_CONTENT);
}

function typeset(doc, fonts, title, body, indd, out, cover) {
    doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
    doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
    doc.marginPreferences.properties = {top: PAGE.top, bottom: PAGE.bottom, left: PAGE.inside, right: PAGE.outside};
    doc.documentPreferences.properties = {
        pageWidth: PAGE.width, pageHeight: PAGE.height, facingPages: true, pagesPerDocument: 5 + (cover ? 2 : 0)
    };
    makeStyles(doc, fonts);
    var master = makeMaster(doc), i;
    trace("styles and master made");

    // the cover and a blank page behind it when there is a cover, then the
    // title page, blank, contents, blank, and the body from page 1. "lead" is
    // the number of pages in front of the title page.
    var lead = cover ? 2 : 0, front = lead + 4;
    for (i = 0; i < front; i++) doc.pages[i].appliedMaster = NothingEnum.NOTHING;
    doc.pages[front].appliedMaster = master;
    doc.sections[0].properties = {continueNumbering: false, pageNumberStart: 1, pageNumberStyle: PageNumberStyle.LOWER_ROMAN};
    doc.sections.add(doc.pages[front], {continueNumbering: false, pageNumberStart: 1, pageNumberStyle: PageNumberStyle.ARABIC});
    if (cover) placeCover(doc, cover);

    var t = textBounds(doc.pages[lead]);
    doc.pages[lead].textFrames.add({geometricBounds: [t[0] + 130, t[1], t[0] + 330, t[3]]}).place(title, false);
    var frame = doc.pages[front].textFrames.add({geometricBounds: textBounds(doc.pages[front])});
    frame.place(body, false);
    trace("body placed");
    // a linked story is locked against edits, and the contents adds bookmarks to it
    var links = doc.links.everyItem().getElements();
    for (i = 0; i < links.length; i++) links[i].unlink();
    var story = frame.parentStory;
    story.storyPreferences.opticalMarginAlignment = true;
    story.storyPreferences.opticalMarginSize = 10.5;
    flow(doc, frame, master);
    trace("flowed");
    keepTogether(doc, story, master);
    trace("keeps applied");
    sinkChapters(doc, story, master);
    trace("chapters sunk");

    for (i = front; i < doc.pages.length; i++) {
        var page = doc.pages[i];
        if (page.textFrames.length && page.textFrames[0].characters.length == 0) page.appliedMaster = NothingEnum.NOTHING;
    }
    if (doc.pages.length % 2) doc.pages.add(LocationOptions.AT_END, undefined, {appliedMaster: NothingEnum.NOTHING});
    for (i = 0; i < doc.pages.length; i++) {
        doc.pages[i].marginPreferences.properties = {top: PAGE.top, bottom: PAGE.bottom, left: PAGE.inside, right: PAGE.outside};
    }

    var chapters = contents(doc, story, doc.pages[lead + 2]);
    trace("contents made");
    checkStyles(doc);
    var used = doc.fonts.everyItem().getElements();
    for (i = 0; i < used.length; i++) {
        if (used[i].status != FontStatus.INSTALLED) problem("font not installed", used[i].name);
    }

    var summary = doc.pages.length + " pages (" + (doc.pages.length - front) + " body), " + chapters + " chapters, "
        + doc.hyperlinks.length + " hyperlinks, " + doc.bookmarks.length + " bookmarks";
    doc.save(indd);
    trace("saved");
    doc.exportFile(ExportFormat.PDF_TYPE, File(out + "/" + OUTPUT + "-print.pdf"), false, firstPreset(PRINT_PRESETS));
    trace("print pdf exported");
    for (i = 0; i < CHARACTER_STYLES.length; i++) {
        var name = CHARACTER_STYLES[i][0];
        if (/^Link/.test(name)) apply(doc, doc.characterStyles.itemByName(name), SCREEN_LINK, fonts);
    }
    var screen = screenPreset();
    try {
        doc.exportFile(ExportFormat.PDF_TYPE, File(out + "/" + OUTPUT + ".pdf"), false, screen);
    } finally {
        screen.remove();
    }
    trace("screen pdf exported");
    return "wrote " + OUTPUT + ".indd, " + OUTPUT + "-print.pdf, and " + OUTPUT + ".pdf to " + Folder(out).fsName
        + "\n" + summary;
}

function main() {
    var here = File($.fileName).parent.fsName, args = app.scriptArgs;
    var src = args.isDefined("src") ? args.getValue("src") : here;
    var out = args.isDefined("out") ? args.getValue("out") : here;
    var prefs = app.scriptPreferences, level = prefs.userInteractionLevel, units = prefs.measurementUnit;
    prefs.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
    prefs.measurementUnit = MeasurementUnits.POINTS;
    var result;
    try {
        result = layout(src, out);
    } catch (e) {
        result = "FAILED: " + e.message + (e.line ? " (layout.jsx line " + e.line + ")" : "");
    } finally {
        prefs.userInteractionLevel = level;
        prefs.measurementUnit = units;
    }
    if (problems.length) result += "\nproblems:\n  " + problems.join("\n  ");
    if (!args.isDefined("headless")) alert(result);
    return result;
}

main();
