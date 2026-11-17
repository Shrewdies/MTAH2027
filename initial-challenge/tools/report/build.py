"""Build the technical report: one deck, written twice.

    python tools/report/build.py            # logo, figures, .pptx and .pdf
    python tools/report/build.py --pdf      # logo, figures and the PDF only
    python tools/report/build.py --pptx     # logo, figures and the PowerPoint file only
    python tools/report/build.py --preview  # also render the PDF pages to PNG for review

Content lives in TECHNICAL.md; deck.py restates it as slides (a format-neutral model).
deck_pptx.py writes that model as an editable PowerPoint file, deck_pdf.py as a PDF with one
high-resolution image per 16:9 page (plus links and searchable text), so the two files are the
same deck. Figures come from charts.py, the
luminous logo from brand.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import brand  # noqa: E402
import charts  # noqa: E402
import deck  # noqa: E402

ROOT = HERE.parents[1]
REPORT = ROOT / "report"
CACHE = HERE / ".cache"          # renders for the deck and previews; not committed
PDF = REPORT / "the-shrewdies-technical-report.pdf"
PPTX = REPORT / "the-shrewdies-technical-report.pptx"

TITLE = "Who has the ball? Technical report"
AUTHOR = "The Shrewdies"
SUBJECT = "Decoding team possession frame by frame. More Than a Hack 2027, Initial Challenge."
KEYWORDS = "football, possession, tracking, Viterbi, Pareto, More Than a Hack 2027"
MAX_PDF_MB = 10


def set_pdf_metadata(pdf: Path) -> None:
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(str(pdf))
    writer = PdfWriter(clone_from=reader)
    writer.metadata = None
    writer.add_metadata({
        "/Title": TITLE, "/Author": AUTHOR, "/Subject": SUBJECT, "/Keywords": KEYWORDS,
        "/Creator": AUTHOR, "/Producer": AUTHOR,
    })
    with pdf.open("wb") as fh:
        writer.write(fh)


def check_numbers() -> None:
    """The squad numbers live in deck.py and are repeated in TECHNICAL.md; say so when they drift."""
    text = (ROOT / "TECHNICAL.md").read_text(encoding="utf-8")
    block = "".join(text.split("<!-- squad-numbers")[1:])
    stale = [f"{n} {what}" for n, what in deck.squad_numbers() if f"**{n}** {what}" not in block]
    if stale:
        print("WARNING: TECHNICAL.md section 12 does not say: " + "; ".join(stale))


def build_pdf(slides: list, preview: bool) -> None:
    import deck_pdf
    from pypdf import PdfReader

    deck_pdf.build(PDF, CACHE, slides)
    set_pdf_metadata(PDF)
    pages, mb = len(PdfReader(str(PDF)).pages), PDF.stat().st_size / 1e6
    print(f"{PDF.relative_to(ROOT)}: {pages} pages, {mb:.2f} MB")
    if pages != len(slides):
        raise SystemExit(f"the PDF has {pages} pages for {len(slides)} slides: a slide overflows its page")
    if mb > MAX_PDF_MB:
        raise SystemExit(f"the PDF is larger than {MAX_PDF_MB} MB")
    if preview:
        import pypdfium2 as pdfium
        out = CACHE / "pdf-pages"
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob("page-*.png"):
            old.unlink()
        doc = pdfium.PdfDocument(str(PDF))
        for i, page in enumerate(doc):
            page.render(scale=1600 / page.get_width()).to_pil().save(out / f"page-{i + 1:02d}.png")
        print(f"page previews -> {out}")


def build_pptx(slides: list) -> None:
    import deck_pptx
    deck_pptx.build(PPTX, CACHE, slides)
    print(f"{PPTX.relative_to(ROOT)}: {len(slides)} slides, {PPTX.stat().st_size / 1e6:.2f} MB")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdf", action="store_true", help="build the PDF only")
    ap.add_argument("--pptx", action="store_true", help="build the PowerPoint file only")
    ap.add_argument("--preview", action="store_true", help="render PDF pages to PNG under tools/report/.cache")
    args = ap.parse_args()
    both = not (args.pdf or args.pptx)
    brand.main()
    charts.main()
    slides = deck.model()
    check_numbers()
    if args.pptx or both:
        build_pptx(slides)
    if args.pdf or both:
        build_pdf(slides, args.preview)


if __name__ == "__main__":
    main()
