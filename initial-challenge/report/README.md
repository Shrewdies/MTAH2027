# Technical report: one deck, two files

| file | what it is |
|---|---|
| `the-shrewdies-technical-report.pptx` | the report as a 16:9 deck, 23 slides, editable, with speaker notes |
| `the-shrewdies-technical-report.pdf` | the same deck as a PDF that opens instantly: one 3200 x 1800 image per slide, with clickable links and searchable text |
| `build/charts/slide/*.svg` | the five figures, generated |
| `brand/` | the brand snapshot the deck is built from (see below) |

**The content lives in [`../TECHNICAL.md`](../TECHNICAL.md).** It is the single source of truth:
the deck restates it with the same numbers and claims, and adds only figures drawn from it, from
the frozen search results in `possession/pareto_front.json` and `possession/profiles.json`
(simulated matches), and from the Dockerfile and `scripts/run.sh` (the run sandbox). When
TECHNICAL.md changes, edit the matching slide in `tools/report/deck.py`, then rebuild.

The deck covers the Initial Challenge only. The team's knowledge hub for the whole hackathon is
[theshrewdies.com](https://theshrewdies.com), hosted separately.

## How the two files stay the same deck

`tools/report/deck.py` describes every slide once, as a format-neutral model: text boxes,
rectangles, pictures and tables, in inches and points. Two writers replay that model:

| writer | output | how |
|---|---|---|
| `deck_pptx.py` | `.pptx` | python-pptx: native text, native tables, links, speaker notes; charts and backgrounds as bitmaps |
| `deck_pdf.py` | `.pdf` | each slide laid out as an HTML page (brand fonts, charts and logo as SVG, backgrounds as CSS gradients), rendered by headless Edge at 3200 x 1800 and stored as one image per 16:9 page |

PowerPoint's own PDF export is not used. The build fails if the PDF does not have exactly one
page per slide or grows past 10 MB (it is about 7.5 MB).

### Why the PDF is made of images

A first version kept every slide as vectors. It was sharp but slow to open: the full-page
gradients with transparency behind every slide are expensive for a PDF viewer to paint. Measured
with pdfium, per page, on the build laptop:

| page content, as vectors | 1600 px wide |
|---|---|
| flat colour | 4 ms |
| the content background (three radial gradients with transparency) | 855 ms |
| the title background (four radial gradients and one linear) | 1185 ms |
| pitch artwork, logo, a page of text | 4 to 16 ms each |

| whole deck, 23 pages | 1600 px wide | 3200 px wide (200% zoom) |
|---|---|---|
| vector PDF | 1038 ms per page (0.86 to 1.85 s) | 4715 ms per page (3.6 to 8.2 s) |
| image PDF | about 20 ms per page (4 to 31 ms) | about 40 ms per page (22 to 54 ms) |

So each slide is rendered once, at build time, and the PDF stores the result:

- **Resolution.** 3200 x 1800 pixels per slide, 2.5 device pixels per CSS pixel: type stays sharp
  beyond 200% zoom.
- **Encoding, chosen per slide by measuring.** Light slides become PNG with an adaptive
  256-colour palette (median cut refined by k-means, no dithering): no compression artefacts
  around type, about 200 to 260 KB each. Slides whose gradients or still picture need more than
  256 colours (the palette falls below 43 dB) become JPEG at quality 92 with full-resolution
  chroma (4:4:4), 330 to 730 KB each. Today that is 16 PNG and 7 JPEG.
- **No recompression.** The image bytes go into the PDF exactly as encoded.
- **Links and text.** The links of each slide are link annotations at the position of their text
  box, and the slide text is repeated as an invisible layer, so the PDF is clickable, searchable
  and copyable. Text inside the figures is part of the image.

## Fonts

The brand faces are Big Shoulders Display, Manrope and JetBrains Mono, all under the SIL Open
Font License, which permits embedding.

- **PDF.** The pages are rendered with the three faces, loaded from Google Fonts at build time,
  and stored as images, so the PDF looks the same everywhere and carries no font files. Offline,
  the fallbacks of the brand stacks in `brand/tokens.css` are used instead. The invisible text
  layer names Helvetica, a standard PDF font that needs no embedding. The font files are not
  stored in this repository.
- **PowerPoint.** A .pptx cannot carry web fonts, so the theme names the fallbacks that ship with
  Windows and Office: Bahnschrift SemiBold Condensed (display), Segoe UI (text), Consolas (code).
  Layout, colours and line breaks match the PDF; the letterforms differ slightly. The PDF writer
  scales each face so lines break where they break in PowerPoint. On a machine with the three
  brand fonts installed, build the .pptx with them:

```powershell
$env:DECK_FONTS = "brand"; tools\report\.venv\Scripts\python tools\report\build.py --pptx
```

## Identity

The look is "Floodlit Blaugrana", from the snapshot in `brand/`, so the deck builds without the
website:

| file | use |
|---|---|
| `tokens.css` | colours, gradients and font stacks; linked by the pages the PDF is rendered from |
| `wordmark.svg` | the official wordmark (source of the letterforms; never redrawn) |
| `logo-luminous.svg`, `.png` | the static luminous logo: wordmark paths with a gradient fill, navy keyline and lime rim; written by `tools/report/brand.py` (SVG for the PDF pages, PNG in the .pptx) |
| `favicon.svg` | the site icon, shown next to theshrewdies.com |
| `field-lines.svg` | the pitch artwork behind every slide |

The logo, theshrewdies.com and github.com/Shrewdies/MTAH2027 are on the title and closing slides
and in every slide footer; the closing slide carries the team.

## Rebuild

Requirements: Python 3.11 or newer and Microsoft Edge (or any Chromium; set `EDGE` to its path).

Windows (PowerShell), from the `initial-challenge` folder:

```powershell
python -m venv tools\report\.venv
tools\report\.venv\Scripts\python -m pip install -r tools\report\requirements.txt
tools\report\.venv\Scripts\python tools\report\build.py            # logo, figures, .pptx and .pdf
tools\report\.venv\Scripts\python tools\report\build.py --pdf      # the PDF only
tools\report\.venv\Scripts\python tools\report\build.py --pptx     # the PowerPoint file only
```

Linux / macOS:

```bash
python3 -m venv tools/report/.venv
tools/report/.venv/bin/python -m pip install -r tools/report/requirements.txt
EDGE=/path/to/chromium tools/report/.venv/bin/python tools/report/build.py
```

What the build does:

1. `brand.py` writes the luminous logo from the paths of `brand/wordmark.svg`.
2. `charts.py` writes the five figures as SVG (pipeline, tag weights, Pareto front, external
   validation, run sandbox). Standard library only.
3. `deck.py` builds the slide model; `deck_pptx.py` and `deck_pdf.py` write it. The counts of the
   numbers slide are constants at the top of `deck.py`; TECHNICAL.md repeats them between
   `squad-numbers` comments and the build warns when the two disagree.
4. `build.py` sets the PDF metadata (author, creator and producer: The Shrewdies); the .pptx
   carries the same author and last-modified-by.

Render caches go to `tools/report/.cache/` (ignored).

## Review

- `build.py --preview` renders every PDF page to `tools/report/.cache/pdf-pages/`.
- `tools\report\render-deck.ps1` exports every slide to PNG through PowerPoint (Windows with
  Office) into `tools/report/.cache/deck-pages/`; the deck is opened read-only. Comparing the two
  folders slide by slide is how the PDF is checked against the .pptx.
