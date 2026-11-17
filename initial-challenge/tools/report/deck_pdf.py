"""Write the slide model of deck.py as a PDF that opens instantly: one image per 16:9 page.

Each slide is laid out as an HTML page of 1280 x 720 CSS pixels (13.333 x 7.5 inches): text in
the brand fonts, charts, logo, icon and pitch artwork as inline SVG, the floodlit backgrounds as
CSS gradients. Headless Edge renders the pages at SCALE device pixels per CSS pixel, and every
slide is stored in the PDF as one image, exactly as encoded (no recompression):

    light slides    PNG with an adaptive 256-colour palette: no compression artefacts around type
    vivid slides    JPEG, quality 92, full-resolution chroma (4:4:4): smooth gradients, no halos

The choice is made per slide by measuring: the palette is used when it reproduces the slide
closely enough (PALETTE_MIN_PSNR) and is not much larger than the JPEG. On top of the image the
page carries the links of the slide as link annotations and the slide text as an invisible layer,
so the PDF stays clickable and searchable. A viewer only has to decode one image per page; a
vector page of the same slide takes pdfium seconds instead of milliseconds (report/README.md).

The brand fonts (Big Shoulders Display, Manrope, JetBrains Mono; SIL Open Font License) are
narrower or wider than the Office fonts the .pptx falls back to. Each role is scaled so that
lines break where they break in PowerPoint and both files stay the same deck.
"""

from __future__ import annotations

import html
import io
import math
import re
import struct
import textwrap
import zlib
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

import deck
import edge

# role: (CSS family, weight regular, weight bold, size factor against the .pptx face)
FACES = {
    deck.DISPLAY: ("var(--sh-font-display)", 800, 800, 0.94),   # vs Bahnschrift SemiBold Condensed
    deck.SANS: ("var(--sh-font-sans)", 400, 700, 0.955),        # vs Segoe UI
    deck.MONO: ("var(--sh-font-mono)", 400, 600, 0.916),        # vs Consolas
}
LINE = 1.2   # PowerPoint's single line spacing, in ems of the largest run of the paragraph
ANCHOR = {MSO_ANCHOR.TOP: "flex-start", MSO_ANCHOR.MIDDLE: "center", MSO_ANCHOR.BOTTOM: "flex-end"}
ALIGN = {PP_ALIGN.LEFT: "left", PP_ALIGN.CENTER: "center", PP_ALIGN.RIGHT: "right"}

CSS_W, CSS_H = 1280, 720     # one slide in CSS pixels: 13.333 x 7.5 in at 96 px per inch
SCALE = 2.5                  # device pixels per CSS pixel: 3200 x 1800 per slide
BATCH = 4                    # slides per browser launch (one tall screenshot, cut into slides)
JPEG_QUALITY = 92
PALETTE_MIN_PSNR = 43.0      # dB; below this the 256-colour palette shows in the gradients
PALETTE_MAX_RATIO = 1.25     # the palette may cost this much more than the JPEG: it is the sharper one
PT_W, PT_H = 960.0, 540.0    # the PDF page in points
EM_WIDTH = {deck.DISPLAY: 0.40, deck.SANS: 0.50, deck.MONO: 0.56}   # mean glyph width, for the text layer

CSS = f"""
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; }}
.slide {{ position: relative; width: {CSS_W}px; height: {CSS_H}px; overflow: hidden; }}
.el {{ position: absolute; }}
.stage, .scrim {{ position: absolute; inset: 0; }}
.art {{ position: absolute; }}
.art svg {{ display: block; width: 100%; height: 100%; }}
.art .home, .art .away {{ stroke: #fff; }}
.tx {{ display: flex; flex-direction: column; text-decoration: none; color: inherit; }}
.tx p {{ margin: 0; white-space: pre-wrap; }}
.pic svg, .pic img {{ display: block; width: 100%; height: auto; }}
table.el {{ border-collapse: collapse; table-layout: fixed; }}
table.el td {{ padding: 0.05in 0.12in; vertical-align: middle; border: 1pt solid #fff; overflow: hidden; }}
"""


# --------------------------------------------------------------------------------------------
# Slides as HTML
# --------------------------------------------------------------------------------------------

def colour(name: str, alpha: float | None = None) -> str:
    h = deck.COLOURS[name]
    if alpha is None:
        return f"#{h}"
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def scoped_svg(markup: str, prefix: str) -> str:
    """Inline an SVG more than once on a page: drop the prolog and give every id a unique prefix."""
    svg = re.sub(r"^<\?xml[^>]*>\s*", "", markup.strip())
    for i in sorted(set(re.findall(r'\bid="([^"]+)"', svg)), key=len, reverse=True):
        svg = re.sub(rf'\bid="{re.escape(i)}"', f'id="{prefix}-{i}"', svg)
        svg = svg.replace(f"url(#{i})", f"url(#{prefix}-{i})").replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    svg = re.sub(r'aria-labelledby="([^"]+)"',
                 lambda m: 'aria-labelledby="' + " ".join(f"{prefix}-{x}" for x in m.group(1).split()) + '"', svg)
    head, rest = svg.split(">", 1)                      # the size comes from the slide, not the file
    return re.sub(r'\s(?:width|height)="[^"]*"', "", head) + ">" + rest


class Page:
    """Markup of one slide. Counts inlined SVGs so their ids never collide."""

    def __init__(self, index: int, sources: dict[str, str]):
        self.index, self.sources, self.n, self.out = index, sources, 0, []

    def svg(self, key: str) -> str:
        self.n += 1
        return scoped_svg(self.sources[key], f"s{self.index}-{self.n}")

    def box(self, e: dict) -> str:
        return f'left:{e["x"]:.4f}in;top:{e["y"]:.4f}in;width:{e["w"]:.4f}in;'

    def stage(self, name: str) -> None:
        bg, art_box, opacity, stroke, scrim = deck.STAGES[name]
        self.out.append(
            f'<div class="stage" style="background:{bg}"></div>'
            f'<div class="art st-{name}" style="{art_box};opacity:{opacity}">{self.svg("pitch")}</div>'
            f'<div class="scrim" style="background:{scrim}"></div>')

    def text(self, e: dict) -> None:
        paras = []
        for spec in e["paras"]:
            runs, biggest, strut = [], 0.0, ""
            for t, font, size, col, bold in spec["runs"]:
                family, regular, heavy, factor = FACES[font]
                if size > biggest:
                    # the paragraph takes the face of its largest run, so every line sits on that baseline
                    biggest, strut = size, f"font-family:{family};font-size:{size * factor:.2f}pt;"
                runs.append(f'<span style="font-family:{family};font-weight:{heavy if bold else regular};'
                            f'font-size:{size * factor:.2f}pt;color:{colour(col)}">{html.escape(t)}</span>')
            tight = spec.get("line", 1.0)
            style = f'text-align:{ALIGN[spec["align"]]};{strut}line-height:{biggest * LINE * tight:.2f}pt;'
            if tight != 1.0:
                # PowerPoint takes tightened spacing off the top of the line; CSS splits it top and bottom
                style += f'position:relative;top:{-(1 - tight) * LINE * biggest / 2:.2f}pt;'
            if "space_after" in spec:
                style += f'margin-bottom:{spec["space_after"]}pt;'
            paras.append(f'<p style="{style}">{"".join(runs)}</p>')
        style = f'{self.box(e)}height:{e["h"]:.4f}in;justify-content:{ANCHOR[e["anchor"]]};'
        self.out.append(f'<div class="el tx" style="{style}">{"".join(paras)}</div>')

    def rect(self, e: dict) -> None:
        style = f'{self.box(e)}height:{e["h"]:.4f}in;'
        if e["fill"]:
            style += f'background:{colour(e["fill"], e["alpha"])};'
        if e["line"]:
            style += f'border:{e["line_w"]}pt solid {colour(e["line"])};'
        if e["radius"]:
            style += f'border-radius:{min(e["radius"], min(e["w"], e["h"]) / 2):.4f}in;'
        self.out.append(f'<div class="el" style="{style}"></div>')

    def picture(self, e: dict) -> None:
        style = self.box(e)
        if e["h"] is not None:
            style += f'height:{e["h"]:.4f}in;'
        if e["line"]:
            style += f'outline:0.75pt solid {colour(e["line"])};'
        if e["key"] == "hero":
            inner = f'<img src="{deck.HERO.resolve().as_uri()}" alt="">'
        else:
            inner = self.svg(e["key"])
        self.out.append(f'<div class="el pic" style="{style}">{inner}</div>')

    def table(self, e: dict) -> None:
        total = sum(e["cols"])
        cols = "".join(f'<col style="width:{e["w"] * c / total:.4f}in">' for c in e["cols"])
        rows = []
        for r, values in enumerate([e["header"]] + e["rows"]):
            cells = []
            for c, value in enumerate(values):
                fill, font, size, bold, col, right = deck.table_cell(e, r, c)
                family, regular, heavy, factor = FACES[font]
                cells.append(f'<td style="background:{colour(fill)};color:{colour(col)};font-family:{family};'
                             f'font-weight:{heavy if bold else regular};font-size:{size * factor:.2f}pt;'
                             f'line-height:{size * LINE:.2f}pt;text-align:{"right" if right else "left"}">'
                             f'{html.escape(str(value))}</td>')
            rows.append(f'<tr style="height:{e["row_h"]:.4f}in">{"".join(cells)}</tr>')
        self.out.append(f'<table class="el" style="{self.box(e)}"><colgroup>{cols}</colgroup>{"".join(rows)}</table>')


def render_html(numbered: list[tuple[int, deck.Slide]], sources: dict[str, str]) -> str:
    """The given (number, slide) pairs stacked top to bottom, one 1280 x 720 block each."""
    strokes = "".join(f".st-{n} .pitch, .st-{n} .echo {{ stroke: {v[3]}; }}\n" for n, v in deck.STAGES.items())
    blocks = []
    for number, model in numbered:
        page = Page(number, sources)
        page.stage(model.stage)
        for kind, e in model.items:
            getattr(page, kind)(e)
        blocks.append(f'<section class="slide">{"".join(page.out)}</section>')
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Who has the ball?</title>"
            f"{edge.FONTS_LINK}<link rel='stylesheet' href='{(deck.BRAND / 'tokens.css').resolve().as_uri()}'>"
            f"<style>{CSS}{strokes}</style></head><body>\n" + "\n".join(blocks) + "\n</body></html>\n")


def svg_sources() -> dict[str, str]:
    sources = {"pitch": deck.pitch_svg(),
               "logo": (deck.BRAND / "logo-luminous.svg").read_text(encoding="utf-8"),
               "favicon": (deck.BRAND / "favicon.svg").read_text(encoding="utf-8")}
    for svg in deck.CHARTS.glob("*.svg"):
        sources[f"chart-{svg.stem}"] = svg.read_text(encoding="utf-8")
    return sources


def render_slides(slides: list, cache: Path) -> list[Image.Image]:
    """Every slide as an RGB image of CSS_W x CSS_H CSS pixels at SCALE."""
    sources = svg_sources()
    width, height = round(CSS_W * SCALE), round(CSS_H * SCALE)
    numbered = list(enumerate(slides, start=1))
    images = []
    for start in range(0, len(numbered), BATCH):
        batch = numbered[start:start + BATCH]
        page, shot = cache / "_deck-batch.html", cache / "_deck-batch.png"
        page.write_text(render_html(batch, sources), encoding="utf-8", newline="\n")
        edge.screenshot(page, shot, CSS_W, CSS_H * len(batch), scale=SCALE)
        with Image.open(shot) as im:
            if im.size != (width, height * len(batch)):
                raise SystemExit(f"slide render is {im.size}, expected {(width, height * len(batch))}")
            im = im.convert("RGB")
            images += [im.crop((0, i * height, width, (i + 1) * height)) for i in range(len(batch))]
        page.unlink(missing_ok=True)
        shot.unlink(missing_ok=True)
    return images


# --------------------------------------------------------------------------------------------
# One image per slide: palette PNG or JPEG, whichever keeps the slide sharp in fewer bytes
# --------------------------------------------------------------------------------------------

def psnr(a: Image.Image, b: Image.Image) -> float:
    mse = sum(ImageStat.Stat(ImageChops.difference(a, b)).sum2) / (3 * a.width * a.height)
    return 99.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)


def encode(im: Image.Image) -> tuple[str, bytes, float]:
    """(kind, bytes, PSNR of the palette version)."""
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, subsampling=0, optimize=True)
    jpeg = buf.getvalue()
    # median cut refined by k-means, no dithering: flat areas stay flat, edges keep their exact steps
    pal = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, kmeans=2, dither=Image.Dither.NONE)
    quality = psnr(im, pal.convert("RGB"))
    buf = io.BytesIO()
    pal.save(buf, "PNG", optimize=True)
    png = buf.getvalue()
    if quality >= PALETTE_MIN_PSNR and len(png) <= PALETTE_MAX_RATIO * len(jpeg):
        return "png", png, quality
    return "jpeg", jpeg, quality


def png_parts(data: bytes) -> tuple[int, int, int, int, bytes, bytes]:
    """(width, height, bit depth, colour type, palette, zlib stream) of a non-interlaced PNG."""
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, palette, idat, head = 8, b"", [], None
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            head = struct.unpack(">IIBBBBB", chunk)
        elif kind == b"PLTE":
            palette = chunk
        elif kind == b"IDAT":
            idat.append(chunk)
        pos += 12 + length
    width, height, depth, ctype, _, _, interlace = head
    if interlace or ctype not in (2, 3):
        raise SystemExit("unexpected PNG layout for a slide image")
    return width, height, depth, ctype, palette, b"".join(idat)


# --------------------------------------------------------------------------------------------
# The PDF: image, links, invisible text
# --------------------------------------------------------------------------------------------

def _pdf_string(s: str) -> bytes:
    raw = s.encode("cp1252", errors="ignore")
    return b"(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"


def text_layer(model: deck.Slide) -> bytes:
    """The slide text in rendering mode 3 (invisible), near where it is drawn: for search and copy."""
    ops = [b"BT 3 Tr"]

    def line(x_in: float, y_in: float, size: float, s: str) -> None:
        if s.strip():
            ops.append(b"/F1 %.1f Tf 1 0 0 1 %.1f %.1f Tm " % (size, x_in * 72, PT_H - y_in * 72) + _pdf_string(s) + b" Tj")

    for kind, e in model.items:
        if kind == "text":
            lines = []
            for spec in e["paras"]:
                size, role = max((r[2], r[1]) for r in spec["runs"])
                em = EM_WIDTH[role]
                chars = max(8, int(e["w"] * 72 / (em * size)))
                for part in textwrap.wrap("".join(r[0] for r in spec["runs"]), chars) or [""]:
                    lines.append((size, part, spec["align"], em))
            total = sum(ln[0] * LINE for ln in lines) / 72
            y = e["y"] + {MSO_ANCHOR.TOP: 0, MSO_ANCHOR.MIDDLE: (e["h"] - total) / 2,
                          MSO_ANCHOR.BOTTOM: e["h"] - total}[e["anchor"]]
            for size, part, align, em in lines:
                est = em * size * len(part) / 72
                x = e["x"] + {PP_ALIGN.LEFT: 0, PP_ALIGN.CENTER: (e["w"] - est) / 2, PP_ALIGN.RIGHT: e["w"] - est}[align]
                line(max(0.0, x), y + size * 0.95 / 72, size, part)
                y += size * LINE / 72
        elif kind == "table":
            total, x = sum(e["cols"]), e["x"]
            for c, share in enumerate(e["cols"]):
                for r, values in enumerate([e["header"]] + e["rows"]):
                    line(x + 0.12, e["y"] + (r + 0.6) * e["row_h"], e["size"], str(values[c]))
                x += e["w"] * share / total
    ops.append(b"ET")
    return b"\n".join(ops)


def assemble(pdf: Path, slides: list, encoded: list[tuple[str, bytes, float]]) -> None:
    from pypdf import PdfWriter
    from pypdf.annotations import Link
    from pypdf.generic import (ArrayObject, ByteStringObject, DecodedStreamObject, DictionaryObject, NameObject,
                               NumberObject, StreamObject)

    def name(s: str) -> NameObject:
        return NameObject(s)

    writer = PdfWriter()
    font = writer._add_object(DictionaryObject({
        name("/Type"): name("/Font"), name("/Subtype"): name("/Type1"), name("/BaseFont"): name("/Helvetica"),
        name("/Encoding"): name("/WinAnsiEncoding")}))
    for number, (model, (kind, data, _)) in enumerate(zip(slides, encoded)):
        image = StreamObject()
        image[name("/Type")], image[name("/Subtype")] = name("/XObject"), name("/Image")
        if kind == "jpeg":
            with Image.open(io.BytesIO(data)) as im:
                width, height = im.size
            image[name("/ColorSpace")], image[name("/Filter")] = name("/DeviceRGB"), name("/DCTDecode")
            depth = 8
        else:
            width, height, depth, ctype, palette, data = png_parts(data)
            colours = 1 if ctype == 3 else 3
            image[name("/Filter")] = name("/FlateDecode")
            image[name("/DecodeParms")] = DictionaryObject({
                name("/Predictor"): NumberObject(15), name("/Colors"): NumberObject(colours),
                name("/BitsPerComponent"): NumberObject(depth), name("/Columns"): NumberObject(width)})
            image[name("/ColorSpace")] = name("/DeviceRGB") if ctype == 2 else ArrayObject([
                name("/Indexed"), name("/DeviceRGB"), NumberObject(len(palette) // 3 - 1), ByteStringObject(palette)])
        image[name("/Width")], image[name("/Height")] = NumberObject(width), NumberObject(height)
        image[name("/BitsPerComponent")] = NumberObject(depth)
        image._data = data                                   # stored exactly as encoded
        page = writer.add_blank_page(width=PT_W, height=PT_H)
        page[name("/Resources")] = DictionaryObject({
            name("/XObject"): DictionaryObject({name("/Im0"): writer._add_object(image)}),
            name("/Font"): DictionaryObject({name("/F1"): font})})
        content = DecodedStreamObject()
        content.set_data(b"q %.0f 0 0 %.0f 0 0 cm /Im0 Do Q\n" % (PT_W, PT_H) + text_layer(model))
        page[name("/Contents")] = writer._add_object(content.flate_encode())
        for kind_, e in model.items:
            if kind_ == "text" and e["link"]:
                rect = (e["x"] * 72, PT_H - (e["y"] + e["h"]) * 72, (e["x"] + e["w"]) * 72, PT_H - e["y"] * 72)
                writer.add_annotation(page_number=number, annotation=Link(rect=rect, border=[0, 0, 0], url=e["link"]))
    with pdf.open("wb") as fh:
        writer.write(fh)


def build(pdf: Path, cache: Path, slides: list | None = None) -> int:
    slides = slides or deck.model()
    cache.mkdir(parents=True, exist_ok=True)
    encoded = [encode(im) for im in render_slides(slides, cache)]
    assemble(pdf, slides, encoded)
    kinds = [k for k, _, _ in encoded]
    print(f"slide images: {round(CSS_W * SCALE)} x {round(CSS_H * SCALE)}, {kinds.count('png')} palette PNG, "
          f"{kinds.count('jpeg')} JPEG (quality {JPEG_QUALITY}, 4:4:4)")
    print("  " + " ".join(f"{i}:{k[0]}{len(d) // 1024}" for i, (k, d, _) in enumerate(encoded, start=1)) + "  (KB)")
    return len(slides)
