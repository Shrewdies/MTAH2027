"""Write the slide model of deck.py as an editable PowerPoint file (python-pptx).

Text stays text, tables stay native tables, links stay links and every slide keeps its speaker
notes. Pictures are bitmaps here: the charts and the floodlit backgrounds are rendered from the
same SVG and CSS the PDF uses, with headless Edge.

Fonts: the theme carries the faces and every run refers to the theme, so one switch changes the
whole deck. PowerPoint cannot use web fonts, so by default the theme names the brand's fallbacks
that ship with Windows and Office: Bahnschrift SemiBold Condensed (display), Segoe UI (text),
Consolas (code). Set DECK_FONTS=brand to name Big Shoulders Display, Manrope and JetBrains Mono
instead, for machines that have those fonts installed.
"""

from __future__ import annotations

import os
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.util import Inches, Pt

import deck
import edge

if os.environ.get("DECK_FONTS", "").lower() == "brand":
    FONT_MAJOR, FONT_MINOR, FONT_MONO = "Big Shoulders Display", "Manrope", "JetBrains Mono"
else:
    FONT_MAJOR, FONT_MINOR, FONT_MONO = "Bahnschrift SemiBold Condensed", "Segoe UI", "Consolas"
FACE = {deck.DISPLAY: "+mj-lt", deck.SANS: "+mn-lt", deck.MONO: FONT_MONO}   # theme major, theme minor, mono

C = {k: RGBColor.from_string(v) for k, v in deck.COLOURS.items()}
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
W, H = deck.W, deck.H


# --------------------------------------------------------------------------------------------
# Bitmaps for PowerPoint
# --------------------------------------------------------------------------------------------

def render_stage(name: str, cache: Path) -> Path:
    bg, art_box, opacity, stroke, scrim = deck.STAGES[name]
    html = cache / f"_bg-{name}.html"
    html.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        f"html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:{bg}}}"
        f".art{{position:absolute;{art_box};opacity:{opacity}}} .art svg{{width:100%;height:100%;display:block}}"
        f".art .pitch,.art .echo{{stroke:{stroke}}} .art .home,.art .away{{stroke:#fff}}"
        f".scrim{{position:absolute;inset:0;background:{scrim}}}"
        "</style></head><body>"
        f"<div class='art'>{deck.pitch_svg()}</div><div class='scrim'></div></body></html>",
        encoding="utf-8")
    png = cache / f"bg-{name}.png"
    edge.screenshot(html, png, 1920, 1080, scale=1.0)
    html.unlink(missing_ok=True)
    jpg = cache / f"bg-{name}.jpg"
    Image.open(png).convert("RGB").save(jpg, quality=88, optimize=True, progressive=True)
    png.unlink(missing_ok=True)
    return jpg


def render_assets(cache: Path) -> dict[str, Path]:
    cache.mkdir(parents=True, exist_ok=True)
    for old in list(cache.glob("bg-*.jpg")) + list(cache.glob("chart-*.png")):
        old.unlink()
    assets = {f"bg-{n}": render_stage(n, cache) for n in deck.STAGES}
    for svg in sorted(deck.CHARTS.glob("*.svg")):
        w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg.read_text(encoding="utf-8")).groups())
        png = cache / f"chart-{svg.stem}.png"
        edge.svg_to_png(svg, png, w, h, scale=2.4, background="#FFFFFF", workdir=cache)
        assets[f"chart-{svg.stem}"] = png
    icon = cache / "favicon.png"
    edge.svg_to_png(deck.BRAND / "favicon.svg", icon, 64, 64, scale=4, background=None, workdir=cache)
    assets["favicon"] = icon
    assets["logo"] = deck.BRAND / "logo-luminous.png"
    assets["hero"] = deck.HERO
    return assets


# --------------------------------------------------------------------------------------------
# Drawing
# --------------------------------------------------------------------------------------------

def draw_text(slide, e) -> None:
    box = slide.shapes.add_textbox(Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = e["anchor"]
    for i, spec in enumerate(e["paras"]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = spec["align"]
        if "space_after" in spec:
            p.space_after = Pt(spec["space_after"])
        if "line" in spec:
            p.line_spacing = spec["line"]
        for t, font, size, colour, bold in spec["runs"]:
            r = p.add_run()
            r.text = t
            r.font.name = FACE[font]
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = C[colour]
    if e["link"]:
        # on the box, not on the runs: the text keeps its colour instead of the theme's link colour
        box.click_action.hyperlink.address = e["link"]


def draw_rect(slide, e) -> None:
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if e["radius"] else MSO_SHAPE.RECTANGLE
    s = slide.shapes.add_shape(kind, Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
    s.shadow.inherit = False
    if e["fill"] is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = C[e["fill"]]
        if e["alpha"] is not None:
            # fill transparency, which python-pptx does not expose: <a:alpha> inside the colour
            clr = s.fill._xPr.find(".//{%s}srgbClr" % A)
            etree.SubElement(clr, "{%s}alpha" % A, val=str(int(e["alpha"] * 100000)))
    if e["line"]:
        s.line.color.rgb = C[e["line"]]
        s.line.width = Pt(e["line_w"])
    else:
        s.line.fill.background()
    if e["radius"]:
        s.adjustments[0] = min(0.5, e["radius"] / min(e["w"], e["h"]))


def draw_picture(slide, e, assets):
    kw = {"width": Inches(e["w"])}
    if e["h"] is not None:
        kw["height"] = Inches(e["h"])
    pic = slide.shapes.add_picture(str(assets[e["key"]]), Inches(e["x"]), Inches(e["y"]), **kw)
    if e["line"]:
        pic.line.color.rgb = C[e["line"]]
        pic.line.width = Pt(0.75)
    return pic


def draw_background(slide, path: Path) -> None:
    pic = slide.shapes.add_picture(str(path), 0, 0, Inches(W), Inches(H))
    sp = pic._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)   # behind everything else


def draw_table(slide, e) -> None:
    rows, cols = e["rows"], e["cols"]
    shape = slide.shapes.add_table(len(rows) + 1, len(cols), Inches(e["x"]), Inches(e["y"]), Inches(e["w"]),
                                   Inches(e["row_h"] * (len(rows) + 1)))
    tbl = shape.table
    tbl.first_row = True
    tbl.horz_banding = False
    total = sum(cols)
    for i, c in enumerate(cols):
        tbl.columns[i].width = Inches(e["w"] * c / total)
    for r in range(len(rows) + 1):
        tbl.rows[r].height = Inches(e["row_h"])
    for r, values in enumerate([e["header"]] + rows):
        for c, value in enumerate(values):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            fill, font, size, bold, colour, right = deck.table_cell(e, r, c)
            cell.fill.fore_color.rgb = C[fill]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if right else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = str(value)
            run.font.name, run.font.size, run.font.bold = FACE[font], Pt(size), bold
            run.font.color.rgb = C[colour]


# --------------------------------------------------------------------------------------------
# Theme, metadata, file
# --------------------------------------------------------------------------------------------

def apply_theme(prs: Presentation) -> None:
    part = prs.slide_masters[0].part.part_related_by(RT.THEME)
    root = etree.fromstring(part.blob)
    ns = {"a": A}
    root.set("name", "The Shrewdies")
    scheme = root.find(".//a:clrScheme", ns)
    scheme.set("name", "Floodlit Blaugrana")
    colours = {"dk1": "0B1433", "lt1": "FFFFFF", "dk2": "0A1F44", "lt2": "E9EDF5",
               "accent1": "004D98", "accent2": "A50044", "accent3": "6E4C9F", "accent4": "B9A2D8",
               "accent5": "C4F000", "accent6": "2F86F0", "hlink": "004D98", "folHlink": "6E4C9F"}
    for tag, hex_ in colours.items():
        el = scheme.find(f"a:{tag}", ns)
        for child in list(el):
            el.remove(child)
        etree.SubElement(el, f"{{{A}}}srgbClr", val=hex_)
    fonts = root.find(".//a:fontScheme", ns)
    fonts.set("name", "The Shrewdies")
    for which, face in (("majorFont", FONT_MAJOR), ("minorFont", FONT_MINOR)):
        latin = fonts.find(f"a:{which}/a:latin", ns)
        latin.attrib.clear()
        latin.set("typeface", face)
    part._blob = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def set_metadata(prs: Presentation) -> None:
    cp = prs.core_properties
    now = datetime.now(timezone.utc).replace(microsecond=0, tzinfo=None)
    cp.author = "The Shrewdies"
    cp.last_modified_by = "The Shrewdies"
    cp.title = "Who has the ball?"
    cp.subject = "Decoding team possession frame by frame. More Than a Hack 2027, Initial Challenge."
    cp.keywords = "football, possession, tracking, Viterbi, Pareto, theshrewdies.com"
    cp.category = "Technical report"
    cp.comments = ""
    cp.revision = 1
    cp.created = now
    cp.modified = now
    cp.last_printed = now


APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><TotalTime>0</TotalTime><Application>Microsoft Office PowerPoint</Application><PresentationFormat>Widescreen</PresentationFormat><Slides>{n}</Slides><Notes>{n}</Notes><HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop><Company>The Shrewdies</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>"""


def write_app_properties(path: Path, n_slides: int) -> None:
    """python-pptx keeps the extended properties of its template (a 4:3 deck with no slides);
    replace them so file browsers and Office report the real format and counts."""
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = APP_XML.format(n=n_slides).encode("utf-8")
            dst.writestr(item, data)
    tmp.replace(path)


def build(out: Path, cache: Path, slides: list | None = None) -> int:
    slides = slides or deck.model()
    assets = render_assets(cache)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    apply_theme(prs)
    set_metadata(prs)
    blank = prs.slide_layouts[6]
    for model in slides:
        slide = prs.slides.add_slide(blank)
        draw_background(slide, assets[f"bg-{model.stage}"])
        for kind, e in model.items:
            if kind == "text":
                draw_text(slide, e)
            elif kind == "rect":
                draw_rect(slide, e)
            elif kind == "picture":
                draw_picture(slide, e, assets)
            elif kind == "table":
                draw_table(slide, e)
        slide.notes_slide.notes_text_frame.text = "\n".join(model.notes)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    write_app_properties(out, len(slides))
    return len(slides)
