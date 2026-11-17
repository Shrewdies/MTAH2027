"""Vector figures for the slide deck of the technical report.

Every number drawn here comes from TECHNICAL.md or from the frozen search results in
possession/pareto_front.json and possession/profiles.json; the run sandbox figure restates the
Dockerfile and scripts/run.sh. The figures are written as plain SVG: the PDF inlines them as
vectors, the PowerPoint file uses PNG renders of the same files.

    python tools/report/charts.py            # writes report/build/charts/slide/*.svg

No third-party dependencies: the standard library is enough for five small figures.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "report" / "build" / "charts"

DISPLAY = "'Big Shoulders Display', 'Bahnschrift SemiBold Condensed', 'Bahnschrift', 'Arial Narrow', sans-serif"
SANS = "Manrope, 'Segoe UI', system-ui, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Mono', Consolas, monospace"

# Brand palette, "Floodlit Blaugrana" (report/brand/tokens.css).
BLUE, NAVY, GARNET, BURGUNDY = "#004D98", "#0A1F44", "#A50044", "#6D0F2C"
MAUVE, VIOLET, LIME = "#B9A2D8", "#6E4C9F", "#C4F000"
BLACK, OFFWHITE, SILVER = "#0B1433", "#F7F6FB", "#E9EDF5"   # BLACK is night navy, never pure black
INK = {900: "#0B1433", 850: "#101C42", 800: "#17244F", 700: "#24315F", 600: "#3A4372",
       400: "#7C84AA", 300: "#B8C2D3", 200: "#D8DEEA", 100: "#E9EDF5"}
PAPER_MUTED = "#3D4670"
STATE = {"H": BLUE, "A": GARNET, "D": INK[600]}


@dataclass(frozen=True)
class Theme:
    name: str
    text: str
    muted: str
    faint: str
    grid: str
    axis: str
    panel: str
    panel_stroke: str
    accent: str          # lines of the highlighted marks (the Pareto front)
    key_fill: str        # fill of the one highlighted mark per figure: lime
    key_stroke: str      # outline that keeps lime readable on white
    series: tuple        # baseline, reasoned, balanced, macro
    pos: str             # diverging: code's team holds the ball
    neg: str             # diverging: code's team is without the ball
    dot: str
    scale: float         # type scale; slides need slightly larger text


# Bright: white panels, navy ink, lime for the one highlighted mark; type sized for projection.
SLIDE = Theme(
    name="slide", text=BLACK, muted=PAPER_MUTED, faint=INK[400], grid="#E3E7F0", axis="#9AA3C2",
    panel="#FFFFFF", panel_stroke=INK[200], accent=BLUE, key_fill=LIME, key_stroke=BLACK,
    series=(INK[300], MAUVE, VIOLET, LIME), pos=BLUE, neg=GARNET, dot="#B4BCD3", scale=1.12,
)


class Svg:
    """A tiny SVG writer: enough to keep the chart code readable."""

    def __init__(self, width: int, height: int, prefix: str, title: str, desc: str):
        self.w, self.h, self.prefix = width, height, prefix
        self.parts: list[str] = []
        self.defs: list[str] = []
        self.title, self.desc = title, desc

    def id(self, name: str) -> str:
        return f"{self.prefix}-{name}"

    def add(self, s: str) -> None:
        self.parts.append(s)

    def text(self, x, y, s, *, size=16, fill="#000", family=SANS, weight=400, anchor="start",
             spacing=None, upper=False, extra="", halo=None):
        sp = f' letter-spacing="{spacing}"' if spacing is not None else ""
        if halo:
            sp += f' paint-order="stroke" stroke="{halo}" stroke-width="5" stroke-linejoin="round"'
        s = s.upper() if upper else s
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size:.1f}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{sp}{extra}>{escape(s)}</text>')

    def rect(self, x, y, w, h, fill, rx=0, extra=""):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{extra}/>')

    def line(self, x1, y1, x2, y2, stroke, width=1.0, extra=""):
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
                 f'stroke-width="{width}"{extra}/>')

    def render(self) -> str:
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" aria-labelledby="{self.id("t")} {self.id("d")}">'
                f'<title id="{self.id("t")}">{escape(self.title)}</title>'
                f'<desc id="{self.id("d")}">{escape(self.desc)}</desc>{defs}{"".join(self.parts)}</svg>\n')


def rounded_bar(x, y, w, h, fill, r=4, *, horizontal=False, toward_positive=True, stroke=None):
    """A bar whose data end is rounded and whose baseline end is square."""
    r = min(r, (w if not horizontal else h) / 2, (h if not horizontal else w))
    if not horizontal:  # vertical bar growing upwards from y + h
        st = f' stroke="{stroke}" stroke-width="1.6" stroke-linejoin="round"' if stroke else ""
        return (f'<path d="M{x:.1f} {y + h:.1f}V{y + r:.1f}Q{x:.1f} {y:.1f} {x + r:.1f} {y:.1f}'
                f'H{x + w - r:.1f}Q{x + w:.1f} {y:.1f} {x + w:.1f} {y + r:.1f}V{y + h:.1f}Z" fill="{fill}"{st}/>')
    if toward_positive:  # rounded on the right
        return (f'<path d="M{x:.1f} {y:.1f}H{x + w - r:.1f}Q{x + w:.1f} {y:.1f} {x + w:.1f} {y + r:.1f}'
                f'V{y + h - r:.1f}Q{x + w:.1f} {y + h:.1f} {x + w - r:.1f} {y + h:.1f}H{x:.1f}Z" fill="{fill}"/>')
    return (f'<path d="M{x + w:.1f} {y:.1f}H{x + r:.1f}Q{x:.1f} {y:.1f} {x:.1f} {y + r:.1f}'
            f'V{y + h - r:.1f}Q{x:.1f} {y + h:.1f} {x + r:.1f} {y + h:.1f}H{x + w:.1f}Z" fill="{fill}"/>')


# --------------------------------------------------------------------------------------------
# 1. Pipeline: tracking + tags -> evidence -> Viterbi -> H/A/D
# --------------------------------------------------------------------------------------------

def pipeline(t: Theme) -> str:
    s = Svg(1000, 400, f"pipe-{t.name}", "From tracking and tags to one label per frame",
            "Tracking feeds both questions, is the ball alive and which team has it; calibrated tags "
            "feed only the team question. Viterbi turns the evidence into one coherent H, A, D sequence.")
    k = t.scale
    card_fill = t.panel
    arrow = s.id("arrow")
    s.defs.append(f'<marker id="{arrow}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                  f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{t.faint}"/></marker>')
    stripes = s.id("stripes")
    s.defs.append(f'<pattern id="{stripes}" width="12" height="10" patternUnits="userSpaceOnUse">'
                  f'<rect width="6" height="10" fill="{BLUE}"/><rect x="6" width="6" height="10" fill="{GARNET}"/></pattern>')

    def card(x, y, w, h, kicker, title, lines, *, num=None):
        s.rect(x, y, w, h, card_fill, rx=10, extra=f' stroke="{t.panel_stroke}" stroke-width="1.2"')
        s.rect(x, y, w, 5, f"url(#{stripes})", rx=0)
        ky = y + 30
        if num:
            s.rect(x + 16, ky - 14, 26, 19, LIME, rx=2)
            s.text(x + 29, ky, num, size=12 * k, fill=BLACK, family=MONO, weight=600, anchor="middle")
            s.text(x + 50, ky, kicker, size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
        else:
            s.text(x + 16, ky, kicker, size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
        s.text(x + 16, ky + 34 * min(k, 1.05), title, size=27 * k, fill=t.text, family=DISPLAY, weight=800, upper=True)
        for i, ln in enumerate(lines):
            s.text(x + 16, ky + 62 * min(k, 1.05) + i * 20 * k, ln, size=14 * k, fill=t.muted)

    def arrow_path(d):
        s.add(f'<path d="{d}" fill="none" stroke="{t.faint}" stroke-width="1.6" marker-end="url(#{arrow})"/>')

    # Inputs
    card(0, 20, 190, 150, "input", "Tracking", ["22 players + ball", "team only, no identities", "ball missing on 41%"])
    card(0, 230, 190, 150, "input", "Tags", ["automatic tactical tags", "14 codes name a team"])

    # Evidence: two separate questions
    ex, ew = 238, 262
    s.rect(ex, 0, ew, 400, "none", rx=14, extra=f' stroke="{t.panel_stroke}" stroke-dasharray="4 5"')
    s.text(ex + 16, 28, "Evidence, frame by frame", size=12 * k, fill=t.muted, family=MONO, weight=600,
           spacing="0.14em", upper=True)
    card(ex + 14, 46, ew - 28, 150, "is the ball alive?", "Alive or dead",
         ["out of play, standing still,", "ball placed, set piece start"])
    card(ex + 14, 230, ew - 28, 150, "which team has it?", "Home or away",
         ["player within 1.5 m of a ball", "slower than 7 m/s; tag hint"])

    # Arrows from inputs
    arrow_path(f"M190 95 C216 95 222 121 {ex + 12} 121")
    arrow_path(f"M190 95 C222 95 218 295 {ex + 12} 295")
    arrow_path(f"M190 335 L{ex + 12} 335")

    # Viterbi
    vx, vw = 542, 222
    s.rect(vx, 20, vw, 360, card_fill, rx=10, extra=f' stroke="{t.panel_stroke}" stroke-width="1.2"')
    s.rect(vx, 20, vw, 5, f"url(#{stripes})")
    s.text(vx + 16, 50, "decode", size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
    s.text(vx + 16, 84, "Viterbi", size=27 * k, fill=t.text, family=DISPLAY, weight=800, upper=True)
    s.text(vx + 16, 110, "best story, not best frame:", size=14 * k, fill=t.muted)
    s.text(vx + 16, 130, "evidence minus a fixed cost", size=14 * k, fill=t.muted)
    s.text(vx + 16, 150, "for every change of state", size=14 * k, fill=t.muted)
    # lattice
    rows = {"H": 200, "A": 250, "D": 300}
    xs = [vx + 48 + i * 22 for i in range(8)]
    path_states = "HHHAAADD"
    for lab, yy in rows.items():
        s.text(vx + 18, yy + 5, lab, size=13 * k, fill=t.muted, family=MONO, weight=600)
        for xx in xs:
            s.add(f'<circle cx="{xx}" cy="{yy}" r="3.2" fill="none" stroke="{t.faint}" stroke-width="1.2"/>')
    pts = " ".join(f"{xx},{rows[st]}" for xx, st in zip(xs, path_states))
    s.add(f'<polyline points="{pts}" fill="none" stroke="{t.key_stroke}" '
          f'stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    s.add(f'<polyline points="{pts}" fill="none" stroke="{t.key_fill}" '
          f'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')
    for xx, st in zip(xs, path_states):
        s.add(f'<circle cx="{xx}" cy="{rows[st]}" r="5.5" fill="{STATE[st]}" stroke="{t.panel}" stroke-width="1.5"/>')
    s.text(vx + 16, 350, "silence: every state scores 0,", size=13 * k, fill=t.faint)
    s.text(vx + 16, 368, "the story simply continues", size=13 * k, fill=t.faint)

    arrow_path(f"M{ex + ew - 14} 121 C{vx - 18} 121 {vx - 26} 200 {vx - 4} 200")
    arrow_path(f"M{ex + ew - 14} 305 C{vx - 18} 305 {vx - 26} 250 {vx - 4} 250")

    # Output
    ox = 800
    s.text(ox, 50, "output", size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
    s.text(ox, 92, "H · A · D", size=34 * k, fill=t.text, family=DISPLAY, weight=900)
    s.text(ox, 118, "one label for each", size=14 * k, fill=t.muted)
    s.text(ox, 138, "of 199,319 frames", size=14 * k, fill=t.muted)
    strip = [("H", 34), ("D", 10), ("A", 24), ("H", 40), ("D", 14), ("A", 20), ("H", 18)]
    yy = 170
    for st, n in strip:
        s.rect(ox, yy, 34, n * 1.15, STATE[st])
        yy += n * 1.15 + 2
    for i, (st, lab) in enumerate((("H", "home in possession"), ("A", "away in possession"), ("D", "ball dead"))):
        ly = 190 + i * 40
        s.rect(ox + 46, ly - 12, 14, 14, STATE[st], rx=2)
        s.text(ox + 66, ly, st, size=13 * k, fill=t.text, family=MONO, weight=600)
        s.text(ox + 46, ly + 18, lab, size=12 * k, fill=t.muted)
    arrow_path(f"M{vx + vw} 200 L{ox - 10} 200")
    return s.render()


# --------------------------------------------------------------------------------------------
# 2. Pareto front on simulated matches
# --------------------------------------------------------------------------------------------

def pareto(t: Theme, points: list[dict], profiles: dict) -> str:
    s = Svg(1000, 620, f"pareto-{t.name}", "Pareto search on simulated matches",
            f"{len(points)} parameter settings scored on simulated halves: spellF1 against macroF1. "
            "The Pareto front and the reasoned, balanced and macro profiles are highlighted.")
    k = t.scale
    L, R, T, B = 86, 970, 30, 540
    x0, x1, y0, y1 = 0.79, 0.865, 0.54, 0.645

    def X(v): return L + (v - x0) / (x1 - x0) * (R - L)
    def Y(v): return B - (v - y0) / (y1 - y0) * (B - T)

    # grid + ticks
    for i in range(0, 8):
        v = 0.79 + i * 0.01
        if v > x1 + 1e-9:
            break
        s.line(X(v), T, X(v), B, t.grid)
        s.text(X(v), B + 24 * k, f"{v:.2f}", size=13 * k, fill=t.muted, family=MONO, anchor="middle")
    for i in range(0, 6):
        v = 0.54 + i * 0.02
        s.line(L, Y(v), R, Y(v), t.grid)
        s.text(L - 10, Y(v) + 4.5, f"{v:.2f}", size=13 * k, fill=t.muted, family=MONO, anchor="end")
    s.line(L, B, R, B, t.axis, 1.2)
    s.text((L + R) / 2, B + 56 * k, "macroF1 on simulated halves (tie-break)  →", size=14 * k, fill=t.muted,
           family=MONO, anchor="middle", spacing="0.06em")
    s.add(f'<text transform="translate({L - 62} {(T + B) / 2}) rotate(-90)" font-family="{MONO}" '
          f'font-size="{14 * k:.1f}" fill="{t.muted}" text-anchor="middle" letter-spacing="0.06em">'
          f'spellF1 on simulated halves (ranking)  →</text>')

    front = sorted([p for p in points if p["on_front"]], key=lambda p: p["macro_f1"])
    # dominated region of the front, as a faint staircase fill
    if front:
        xs = [X(p["macro_f1"]) for p in front]
        ys = [Y(p["spell_f1"]) for p in front]
        d = f"M{L} {ys[0]:.1f}"
        for i, (xx, yy) in enumerate(zip(xs, ys)):
            d += f"H{xx:.1f}"
            nxt = ys[i + 1] if i + 1 < len(ys) else B
            d += f"V{nxt:.1f}"
        s.add(f'<path d="{d}H{L}Z" fill="{t.accent}" fill-opacity="0.06"/>')
        s.add(f'<path d="{d}" fill="none" stroke="{t.accent}" stroke-width="2" stroke-dasharray="6 5"/>')

    for p in points:
        if p["on_front"]:
            continue
        s.add(f'<circle cx="{X(p["macro_f1"]):.1f}" cy="{Y(p["spell_f1"]):.1f}" r="4.2" fill="{t.dot}" '
              f'fill-opacity="0.75" stroke="{t.panel}" stroke-width="1"/>')

    # highlighted profiles
    reasoned = profiles["reasoned_defaults"]
    # (label, macro, spell, why, on front, label offset dx, dy)
    marks = [
        ("reasoned", reasoned["sim_macro_f1"], reasoned["sim_spell_f1"], "our starting values", False, 24, 58),
        ("balanced (= spell)", profiles["profiles"]["balanced"]["sim_macro_f1"],
         profiles["profiles"]["balanced"]["sim_spell_f1"], "best combined score", True, -24, -10),
        ("macro · submitted", profiles["profiles"]["macro"]["sim_macro_f1"],
         profiles["profiles"]["macro"]["sim_spell_f1"], "best frame accuracy", True, -10, 62),
    ]
    for name, mx, my, why, on_front, dx, dy in marks:
        cx, cy = X(mx), Y(my)
        tx, ty = cx + dx, cy + dy
        anchor = "end" if dx < 0 else "start"
        if abs(dy) > 30:
            s.add(f'<path d="M{cx:.1f} {cy + (9 if dy > 0 else -9):.1f}L{cx + dx * 0.4:.1f} {ty - 17 * k:.1f}" '
                  f'stroke="{t.faint}" stroke-width="1.2"/>')
        fill = t.key_fill if on_front else t.panel
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{fill}" stroke="{t.key_stroke if on_front else t.text}" '
              f'stroke-width="2"/>')
        if on_front:
            s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="none" stroke="{t.accent}" stroke-width="1.2" opacity=".7"/>')
        s.text(tx, ty, name, size=15 * k, fill=t.text, weight=800, anchor=anchor, halo=t.panel)
        s.text(tx, ty + 17 * k, why, size=12.5 * k, fill=t.muted, anchor=anchor, halo=t.panel)
        s.text(tx, ty + 33 * k, f"spell {my:.3f} · macro {mx:.3f}", size=12 * k, fill=t.muted,
               family=MONO, anchor=anchor, halo=t.panel)

    # legend
    lx, ly = L + 18, T + 22
    s.rect(lx - 12, ly - 18, 300, 62, t.panel, rx=6, extra=f' fill-opacity=".92" stroke="{t.panel_stroke}"')
    s.add(f'<circle cx="{lx + 6}" cy="{ly - 4}" r="4.2" fill="{t.dot}"/>')
    s.text(lx + 20, ly + 1, f"setting evaluated ({len(points)})", size=13 * k, fill=t.muted)
    s.add(f'<path d="M{lx - 4} {ly + 22}H{lx + 16}" stroke="{t.accent}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.add(f'<circle cx="{lx + 6}" cy="{ly + 22}" r="5" fill="{t.key_fill}" stroke="{t.key_stroke}" stroke-width="1.5"/>')
    s.text(lx + 20, ly + 27, "Pareto front (simulated matches)", size=13 * k, fill=t.muted)
    return s.render()


# --------------------------------------------------------------------------------------------
# 3. External validation on the labelled DFL match (TECHNICAL.md section 6)
# --------------------------------------------------------------------------------------------

VALIDATION = [  # method, spellF1, macroF1
    ("organisers' baseline", 0.235, 0.383),
    ("ours, reasoned", 0.249, 0.661),
    ("ours, balanced", 0.286, 0.686),
    ("ours, macro (submitted)", 0.340, 0.693),
]


def validation(t: Theme) -> str:
    s = Svg(1000, 470, f"val-{t.name}", "External validation on a labelled Bundesliga match",
            "spellF1 and macroF1 for the organisers' baseline method and our three profiles, ball hidden on 41% of frames.")
    k = t.scale
    L, R, T, B = 70, 990, 92, 400
    vmax = 0.8

    def Y(v): return B - v / vmax * (B - T)

    hatch = s.id("hatch")
    s.defs.append(f'<pattern id="{hatch}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                  f'<rect width="7" height="7" fill="{t.series[0]}" fill-opacity=".35"/>'
                  f'<rect width="2.6" height="7" fill="{t.series[0]}"/></pattern>')
    for v in (0, 0.2, 0.4, 0.6, 0.8):
        s.line(L, Y(v), R, Y(v), t.grid)
        s.text(L - 10, Y(v) + 4.5, f"{v:.1f}", size=13 * k, fill=t.muted, family=MONO, anchor="end")
    s.line(L, B, R, B, t.axis, 1.2)

    # legend row
    lx = L
    for i, (name, *_rest) in enumerate(VALIDATION):
        fill = f"url(#{hatch})" if i == 0 else t.series[i]
        s.rect(lx, 22, 16, 16, fill, rx=3, extra=f' stroke="{t.key_stroke}" stroke-width="1.4"' if i == 3 else "")
        s.text(lx + 24, 35, name, size=14 * k, fill=t.text if i == 3 else t.muted, weight=700 if i == 3 else 400)
        lx += 24 + len(name) * 7.6 * k + 34

    groups = [("spellF1", "ranking · objects", 1), ("macroF1", "tie-break · frames", 2)]
    gw = (R - L) / 2
    bw, gap = 74, 10
    for gi, (label, sub, col) in enumerate(groups):
        gx = L + gi * gw + (gw - (4 * bw + 3 * gap)) / 2
        for i, row in enumerate(VALIDATION):
            v = row[col]
            x = gx + i * (bw + gap)
            fill = f"url(#{hatch})" if i == 0 else t.series[i]
            strong = i == 3
            s.add(rounded_bar(x, Y(v), bw, B - Y(v), fill, stroke=t.key_stroke if strong else None))
            s.text(x + bw / 2, Y(v) - 10, f"{v:.3f}", size=(16 if strong else 14) * k, fill=t.text,
                   family=MONO, weight=700 if strong else 400, anchor="middle")
        cx = L + gi * gw + gw / 2
        s.text(cx, B + 34 * k, label, size=24 * k, fill=t.text, family=DISPLAY, weight=800, anchor="middle")
        s.text(cx, B + 54 * k, sub, size=12 * k, fill=t.muted, family=MONO, anchor="middle", spacing="0.1em", upper=True)
    return s.render()


# --------------------------------------------------------------------------------------------
# 4. Tag weights (TECHNICAL.md section 5, the four rows only)
# --------------------------------------------------------------------------------------------

TAGS = [  # code, agreement with visible control, learned weight
    ("Build up", "86.5%", 1.86),
    ("Progression", "83.0%", 1.58),
    ("Players in the box", "58.2%", 0.33),
    ("Defending in attacking third", "13.5%", -1.86),
]


def tag_weights(t: Theme) -> str:
    s = Svg(1000, 330, f"tags-{t.name}", "Learned tag weights",
            "Log-odds weight of four tag codes, measured without answers from agreement with visible ball control.")
    k = t.scale
    C = 690          # zero line
    span = 135       # px per unit of log-odds
    T, rh = 52, 54
    s.text(20, 26, "tag code", size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
    s.text(370, 26, "agrees with control", size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em",
           upper=True, anchor="end")
    s.text(C + 2 * span + 30, 26, "learned weight", size=12 * k, fill=t.muted, family=MONO, weight=600,
           spacing="0.14em", upper=True, anchor="end")
    bottom = T + len(TAGS) * rh
    for v in (-2, -1, 1, 2):
        s.line(C + v * span, T - 12, C + v * span, bottom - 10, t.grid)
        s.text(C + v * span, bottom + 12 * k, f"{v:+d}".replace("-", "−"), size=12 * k, fill=t.muted, family=MONO,
               anchor="middle")
    s.text(C, bottom + 12 * k, "0", size=12 * k, fill=t.muted, family=MONO, anchor="middle")
    s.text(C - 2 * span - 10, bottom + 36 * k, "← code's team is without the ball", size=12 * k, fill=t.muted,
           family=MONO, anchor="start")
    s.text(C + 2 * span + 30, bottom + 36 * k, "code's team has the ball →", size=12 * k, fill=t.muted,
           family=MONO, anchor="end")
    for i, (code, agree, w) in enumerate(TAGS):
        y = T + i * rh
        s.text(20, y + 20, code, size=16 * k, fill=t.text, weight=600)
        s.text(370, y + 20, agree, size=15 * k, fill=t.muted, family=MONO, anchor="end")
        bw = abs(w) * span
        fill = t.pos if w > 0 else t.neg
        if w > 0:
            s.add(rounded_bar(C, y, bw, 28, fill, horizontal=True, toward_positive=True))
            s.text(C + bw + 10, y + 20, f"+{w:.2f}", size=15 * k, fill=t.text, family=MONO, weight=600)
        else:
            s.add(rounded_bar(C - bw, y, bw, 28, fill, horizontal=True, toward_positive=False))
            s.text(C + 10, y + 20, f"−{abs(w):.2f}", size=15 * k, fill=t.text, family=MONO, weight=600)
    s.line(C, T - 16, C, bottom - 6, t.axis, 1.4)
    return s.render()


# --------------------------------------------------------------------------------------------
# 5. The run sandbox: reproducibility and data protection in one picture (Dockerfile, run.sh)
# --------------------------------------------------------------------------------------------

def sandbox(t: Theme) -> str:
    s = Svg(1000, 400, f"box-{t.name}", "The run sandbox",
            "Source and match data enter a digest-pinned container through read-only mounts. The container "
            "has no network and a read-only root filesystem; the only writable mount is the output folder "
            "outside the repository.")
    k = t.scale
    arrow = s.id("arrow")
    s.defs.append(f'<marker id="{arrow}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                  f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{t.faint}"/></marker>')
    tri = s.id("tri")
    s.defs.append(f'<linearGradient id="{tri}" x1="0" x2="1" y1="0" y2="0">'
                  f'<stop offset="0" stop-color="{BLUE}"/><stop offset=".33" stop-color="{BLUE}"/>'
                  f'<stop offset=".33" stop-color="{LIME}"/><stop offset=".67" stop-color="{LIME}"/>'
                  f'<stop offset=".67" stop-color="{GARNET}"/><stop offset="1" stop-color="{GARNET}"/></linearGradient>')

    def card(x, y, w, h, kicker, title, lines, *, chip=None):
        s.rect(x, y, w, h, t.panel, rx=10, extra=f' stroke="{t.panel_stroke}" stroke-width="1.2"')
        s.rect(x, y, w, 5, f"url(#{tri})")
        ky = y + 30
        if chip:
            cw = len(chip) * 8.2 * k + 14
            s.rect(x + 16, ky - 14, cw, 20, t.key_fill, rx=2)
            s.text(x + 23, ky + 1, chip, size=11.5 * k, fill=BLACK, family=MONO, weight=600, spacing="0.08em", upper=True)
        else:
            s.text(x + 16, ky, kicker, size=12 * k, fill=t.muted, family=MONO, weight=600, spacing="0.14em", upper=True)
        s.text(x + 16, ky + 34 * min(k, 1.05), title, size=26 * k, fill=t.text, family=DISPLAY, weight=800, upper=True)
        for i, ln in enumerate(lines):
            s.text(x + 16, ky + 60 * min(k, 1.05) + i * 20 * k, ln, size=14 * k, fill=t.muted)

    def arrow_path(d, dashed=False):
        dash = ' stroke-dasharray="5 5"' if dashed else ""
        s.add(f'<path d="{d}" fill="none" stroke="{t.faint}" stroke-width="1.6"{dash} marker-end="url(#{arrow})"/>')

    # Inputs: both read-only
    card(0, 20, 200, 160, "", "Source", ["repository code", "and frozen profiles"], chip="read-only")
    card(0, 220, 200, 160, "", "Match data", ["local folder, never", "committed or uploaded"], chip="read-only")

    # The container
    cx, cw = 250, 470
    s.rect(cx, 0, cw, 400, t.panel, rx=14, extra=f' stroke="{t.text}" stroke-width="1.6"')
    s.rect(cx, 0, cw, 6, f"url(#{tri})")
    s.text(cx + 20, 34, "container · pinned by sha256 digest", size=12 * k, fill=t.muted, family=MONO, weight=600,
           spacing="0.12em", upper=True)
    s.text(cx + 20, 70, "python:3.11.11-slim-bookworm", size=24 * k, fill=t.text, family=DISPLAY, weight=800)
    s.text(cx + 20, 96, "numpy 2.2.6 · pandas 2.2.3 · 4 pinned dependencies", size=14 * k, fill=t.muted)
    s.text(cx + 20, 116, "linux/arm64 · linux/amd64 · offline build from wheels", size=14 * k, fill=t.muted)
    chips = ["--network none", "read-only root fs", "tmpfs /tmp"]
    x = cx + 20
    for c in chips:
        w = len(c) * 8.0 * k + 18
        s.rect(x, 136, w, 26, BLACK, rx=4)
        s.text(x + 9, 154, c, size=12.5 * k, fill=t.key_fill, family=MONO, weight=600)
        x += w + 10
    # the run inside
    steps = [("possession.run", "decode, profile macro"), ("official validator", "on every file")]
    sy = 190
    for i, (head, sub) in enumerate(steps):
        bx = cx + 20 + i * 225
        s.rect(bx, sy, 205, 74, OFFWHITE, rx=8, extra=f' stroke="{t.panel_stroke}"')
        s.text(bx + 14, sy + 30, head, size=15 * k, fill=t.text, family=MONO, weight=600)
        s.text(bx + 14, sy + 54, sub, size=13 * k, fill=t.muted)
    arrow_path(f"M{cx + 225} {sy + 37} L{cx + 243} {sy + 37}")
    s.text(cx + 20, 300, "no randomness: byte-identical output, LF line endings", size=14 * k, fill=t.text, weight=700)
    s.text(cx + 20, 322, "under 10 s on a laptop CPU", size=14 * k, fill=t.muted)
    s.text(cx + 20, 370, "15 behaviour tests run in the same image, no data needed", size=13 * k, fill=t.faint)

    arrow_path(f"M200 100 C226 100 226 120 {cx - 4} 120")
    arrow_path(f"M200 300 C226 300 226 280 {cx - 4} 280")

    # Outputs: the only writable mount
    ox = 770
    card(ox, 150, 230, 170, "", "Outputs", ["separate folder, outside", "the repository; published", "figures are aggregates"],
         chip="writable")
    arrow_path(f"M{cx + cw} 235 L{ox - 6} 235")

    # No route out
    s.rect(ox, 20, 230, 96, "none", rx=10, extra=f' stroke="{GARNET}" stroke-width="1.4" stroke-dasharray="5 5"')
    s.text(ox + 16, 50, "no route out", size=12 * k, fill=GARNET, family=MONO, weight=600, spacing="0.12em", upper=True)
    s.text(ox + 16, 76, "no cloud, no hosted", size=14 * k, fill=t.text, weight=700)
    s.text(ox + 16, 96, "model, no upload", size=14 * k, fill=t.text, weight=700)
    s.line(cx + cw + 6, 68, ox - 22, 68, GARNET, 1.4, extra=' stroke-dasharray="5 5"')
    mx = ox - 14
    s.add(f'<path d="M{mx - 7} 61L{mx + 7} 75M{mx + 7} 61L{mx - 7} 75" stroke="{GARNET}" stroke-width="2.6" '
          f'stroke-linecap="round"/>')
    return s.render()


def main() -> None:
    points = json.loads((ROOT / "possession" / "pareto_front.json").read_text(encoding="utf-8"))
    profiles = json.loads((ROOT / "possession" / "profiles.json").read_text(encoding="utf-8"))
    for theme in (SLIDE,):
        out = OUT / theme.name
        out.mkdir(parents=True, exist_ok=True)
        figures = {
            "pipeline": pipeline(theme),
            "pareto": pareto(theme, points, profiles),
            "validation": validation(theme),
            "tag-weights": tag_weights(theme),
            "sandbox": sandbox(theme),
        }
        for name, svg in figures.items():
            (out / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"charts -> {OUT.relative_to(ROOT)} ({len(points)} search points)")


if __name__ == "__main__":
    main()
