"""Static, print-ready versions of the luminous wordmark.

The website animates the wordmark (gradient drift, sheen, glints). Print and slides need one still
frame of the same look: the official letterforms from report/brand/wordmark.svg (the W merged into one outline), with a
luminous gradient fill (lime, silver, mauve, light blue, pink), a night-navy keyline and extrusion,
and a lime rim light.

    python tools/report/brand.py      # writes report/brand/logo-luminous.svg and .png

The paths are copied from wordmark.svg, never edited, so the letters cannot drift from the brand.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "report" / "brand"
WORDMARK = BRAND / "wordmark.svg"
LOGO_SVG = BRAND / "logo-luminous.svg"
LOGO_PNG = BRAND / "logo-luminous.png"

W, H = 2175.545, 338.887
PAD = 24                       # room for the keyline, rim and extrusion
INK, DEPTH, RIM = "#0A1440", "#1C0C46", "#C4F000"
LIGHT_X, LIGHT_Y = -0.6, -0.8  # light direction, as on the website
KEY, RIM_OFF, DEPTH_OFF = 15, 9, 13

FILL_STOPS = [(0, "#C4F000"), (.12, "#E4FF6E"), (.24, "#F4F6FA"), (.38, "#B9A2D8"), (.52, "#8FB4FF"),
              (.64, "#E9EDF5"), (.76, "#A98CF0"), (.88, "#FF7DB6"), (1, "#E9EDF5")]


def wordmark_paths() -> list[str]:
    svg = WORDMARK.read_text(encoding="utf-8")
    paths = re.findall(r'<path d="([^"]+)"', svg)
    if not paths:
        raise SystemExit(f"no paths found in {WORDMARK}")
    return paths


def luminous_svg() -> str:
    glyphs = "".join(f'<path d="{d}"/>' for d in wordmark_paths())
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in FILL_STOPS)
    dx, dy = -LIGHT_X * DEPTH_OFF, -LIGHT_Y * DEPTH_OFF
    rx, ry = LIGHT_X * RIM_OFF, LIGHT_Y * RIM_OFF
    vb = f"{-PAD} {-PAD} {W + 2 * PAD:.3f} {H + 2 * PAD:.3f}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{vb}" '
        f'width="{W + 2 * PAD:.3f}" height="{H + 2 * PAD:.3f}" role="img" aria-label="The Shrewdies">'
        '<title>The Shrewdies</title>'
        '<defs>'
        f'<linearGradient id="fill" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">{stops}</linearGradient>'
        f'<linearGradient id="chrome" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{H}">'
        '<stop offset="0" stop-color="#FFFFFF" stop-opacity=".5"/>'
        '<stop offset=".46" stop-color="#FFFFFF" stop-opacity="0"/>'
        '<stop offset=".64" stop-color="#1B1150" stop-opacity=".2"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity=".22"/></linearGradient>'
        f'<g id="g">{glyphs}</g>'
        '</defs>'
        f'<use href="#g" xlink:href="#g" fill="{DEPTH}" stroke="{DEPTH}" stroke-width="{KEY}" stroke-linejoin="round" '
        f'transform="translate({dx:.1f} {dy:.1f})"/>'
        f'<use href="#g" xlink:href="#g" fill="{INK}" stroke="{INK}" stroke-width="{KEY}" stroke-linejoin="round"/>'
        f'<use href="#g" xlink:href="#g" fill="{RIM}" transform="translate({rx:.1f} {ry:.1f})"/>'
        f'<use href="#g" xlink:href="#g" fill="none" stroke="{INK}" stroke-width="5" stroke-opacity=".85"/>'
        '<use href="#g" xlink:href="#g" fill="url(#fill)"/>'
        '<use href="#g" xlink:href="#g" fill="url(#chrome)"/>'
        '</svg>\n'
    )


def main(png: bool = True) -> None:
    LOGO_SVG.write_text(luminous_svg(), encoding="utf-8", newline="\n")
    if png:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import edge
        w = 1200
        h = round(w * (H + 2 * PAD) / (W + 2 * PAD))
        edge.svg_to_png(LOGO_SVG, LOGO_PNG, w, h, scale=2.0, background=None,
                        workdir=Path(__file__).resolve().parent / ".cache")
    print(f"brand -> {LOGO_SVG.relative_to(ROOT)}" + (f", {LOGO_PNG.name}" if png else ""))


if __name__ == "__main__":
    main()
