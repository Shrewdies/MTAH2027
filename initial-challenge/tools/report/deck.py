"""The slide deck of the technical report: content and slide model.

Every slide function below draws with a handful of helpers (text, rect, picture, table, ...).
The helpers do not touch any file format: they record what is on the slide. Two writers replay
that one model, so the PowerPoint file and the PDF are the same deck, slide for slide:

    deck_pptx.py   the editable .pptx (python-pptx), with speaker notes
    deck_pdf.py    the .pdf: one high-resolution image per slide, with links and searchable text

Content slides are bright paper with navy ink and lime highlights; the title, the part dividers,
the numbers slide and the closing slide sit on the floodlit gradient. Every slide carries the
logo, theshrewdies.com and the repository. All measures are inches on a 13.333 x 7.5 slide; type
sizes are points.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from pptx.enum.text import MSO_ANCHOR, PP_ALIGN   # used as plain tokens for anchoring and alignment

ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "report" / "brand"
HERO = ROOT / "assets" / "hero" / "hero-poster.png"
CHARTS = ROOT / "report" / "build" / "charts" / "slide"

SITE, SITE_URL = "theshrewdies.com", "https://theshrewdies.com"
REPO, REPO_URL = "github.com/Shrewdies/MTAH2027", "https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge"
ROADMAP, ROADMAP_URL = "theshrewdies.com/challenges/roadmap/", "https://theshrewdies.com/challenges/roadmap/"
TEAM = ["Yousef Fayez", "Mahmoud Abubakr", "Ahmed Awwad", "Abdullah Ashmawei"]

# The squad in numbers: every count on the records slide, the six doors and in the speaker notes.
# Change a value here and rebuild; TECHNICAL.md section 12 repeats them between its
# "squad-numbers" comments, and build.py warns when the two disagree.
YEARS_OF_EXPERIENCE = "50+"       # collective years of professional experience
COUNTRIES = "19"                  # countries of professional journeys, the four careers combined
CULTURES = "5"
PATENTS = "20+"                   # patents in the squad
SPECIALISMS = "7"                 # each mapped to football intelligence on the site
DATASETS = "23"                   # datasets scouted
ATLAS_PAGES = "22"                # dataset atlas pages
MODELS = "74"                     # models, methods and tools reviewed
JUDGED_PAGES = "47"               # of them, judged pages
ARCH_STUDIES = "16"                 # architecture studies
ARCH_FAMILIES = "5"               # families of architecture studies
INSIGHT_PAGES = "12"              # insight pages on how we read the challenge
KNOWLEDGE_PAGES = "140+"          # knowledge pages on theshrewdies.com


def squad_numbers() -> list[tuple[str, str]]:
    """(number, what it counts), as written in TECHNICAL.md: **number** what."""
    return [(YEARS_OF_EXPERIENCE, "years"), (COUNTRIES, "countries"), (CULTURES, "cultures"), (PATENTS, "patents"),
            (SPECIALISMS, "specialisms"), (DATASETS, "datasets scouted"),
            (MODELS, "models, methods and tools reviewed"),
            (ARCH_STUDIES, f"architecture studies in {ARCH_FAMILIES} families"), (INSIGHT_PAGES, "insight pages"),
            (KNOWLEDGE_PAGES, "knowledge pages")]

# Font roles; each writer maps them to faces (see deck_pptx.py and deck_pdf.py).
DISPLAY, SANS, MONO = "display", "sans", "mono"

# "Floodlit Blaugrana" (report/brand/tokens.css). Night navy replaces black; lime is a fill on paper.
COLOURS = {
    "blue": "004D98", "navy": "0A1F44", "night": "0B1433", "garnet": "A50044", "violet": "6E4C9F",
    "mauve": "B9A2D8", "lime": "C4F000", "white": "FFFFFF", "offwhite": "F7F6FB", "silver": "E9EDF5",
    "muted": "3D4670", "ink600": "3A4372", "ink400": "7C84AA", "ink200": "D8DEEA", "paper2": "F4F6FB",
    "glass": "0C1C4A", "soft": "E1E6F2", "keybg": "F0FBC2",
    # six steps of the floodlit gradient, blue to garnet: the doors of the knowledge hub
    "door1": "004D98", "door2": "2A49A0", "door3": "4D44A6", "door4": "7E3F98", "door5": "93206E", "door6": "A50044",
}

W, H = 13.333, 7.5
MX = 0.75  # side margin, inches
LOGO_RATIO = 2223.545 / 386.887   # report/brand/logo-luminous.svg


# --------------------------------------------------------------------------------------------
# Backgrounds: one definition, rendered to JPEG for the .pptx and kept as CSS/SVG for the .pdf
# --------------------------------------------------------------------------------------------

FLOODLIT = "linear-gradient(150deg,#0F63C4 0%,#004D98 24%,#4D44A6 50%,#7E3F98 70%,#A50044 100%)"
STAGES = {
    # name: (CSS background, box of the pitch artwork, its opacity, its stroke, scrim behind the text)
    "title": ("radial-gradient(45% 45% at 88% 8%,rgba(233,237,245,.45),transparent 70%),"
              "radial-gradient(40% 50% at 0% 45%,rgba(185,162,216,.35),transparent 72%),"
              "radial-gradient(45% 45% at 100% 95%,rgba(229,51,111,.4),transparent 70%),"
              f"radial-gradient(35% 30% at 8% 100%,rgba(196,240,0,.22),transparent 70%),{FLOODLIT}",
              "left:28%;right:-14%;top:12%;bottom:-6%", .5, "rgba(255,255,255,.75)",
              "linear-gradient(90deg,rgba(11,20,51,.5) 0%,rgba(11,20,51,.25) 45%,rgba(11,20,51,0) 70%)"),
    "divider": ("radial-gradient(40% 50% at 100% 0%,rgba(233,237,245,.4),transparent 70%),"
                "radial-gradient(45% 55% at 0% 100%,rgba(229,51,111,.38),transparent 70%),"
                f"radial-gradient(30% 30% at 60% 100%,rgba(196,240,0,.2),transparent 70%),{FLOODLIT}",
                "left:35%;right:-20%;top:-4%;bottom:10%", .4, "rgba(255,255,255,.7)",
                "linear-gradient(90deg,rgba(11,20,51,.45) 0%,rgba(11,20,51,.15) 50%,rgba(11,20,51,0) 75%)"),
    "numbers": ("radial-gradient(45% 40% at 50% 0%,rgba(233,237,245,.3),transparent 70%),"
                "radial-gradient(40% 50% at 100% 100%,rgba(229,51,111,.4),transparent 70%),"
                f"radial-gradient(35% 35% at 0% 100%,rgba(196,240,0,.18),transparent 70%),{FLOODLIT}",
                "left:-10%;right:-10%;top:10%;bottom:-20%", .22, "rgba(255,255,255,.7)",
                "linear-gradient(180deg,rgba(11,20,51,.38) 0%,rgba(11,20,51,.2) 100%)"),
    "content": ("radial-gradient(45% 55% at 100% 0%,rgba(185,162,216,.32),transparent 70%),"
                "radial-gradient(40% 50% at 0% 100%,rgba(47,134,240,.13),transparent 70%),"
                "radial-gradient(30% 35% at 100% 100%,rgba(196,240,0,.12),transparent 70%),#F7F6FB",
                "left:52%;right:-22%;top:-18%;bottom:30%", .08, "#4D44A6", "none"),
}


def pitch_svg() -> str:
    """The brand pitch artwork as markup, without the XML prolog."""
    svg = (BRAND / "field-lines.svg").read_text(encoding="utf-8")
    return re.sub(r"^<\?xml[^>]*>\s*", "", svg.strip())


# --------------------------------------------------------------------------------------------
# The slide model and the helpers that fill it
# --------------------------------------------------------------------------------------------

@dataclass
class Slide:
    name: str
    stage: str = "content"                       # key of STAGES
    items: list = field(default_factory=list)    # (kind, properties) in drawing order
    notes: list = field(default_factory=list)    # speaker notes, one string per paragraph


class _Keys:
    """Slide functions name pictures by key (a["chart-pareto"]); the writers resolve the key."""

    def __getitem__(self, key: str) -> str:
        return key


def text(slide, x, y, w, h, paras, *, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    """paras: list of paragraphs; each is a list of runs (text, font, size, colour, bold[, link]) or a
    dict {"runs": [...], "space_after": pt, "line": spacing, "align": PP_ALIGN}.
    A link applies to the whole text box, so the text keeps its brand colour; one link per box."""
    specs, link = [], None
    for para in paras:
        spec = dict(para) if isinstance(para, dict) else {"runs": para}
        runs = []
        for t, font, size, colour, bold, *rest in spec["runs"]:
            runs.append((t, font, size, colour, bold))
            link = rest[0] if rest else link
        spec["runs"] = runs
        spec.setdefault("align", align)
        specs.append(spec)
    slide.items.append(("text", dict(x=x, y=y, w=w, h=h, paras=specs, anchor=anchor, link=link)))


def rect(slide, x, y, w, h, fill, *, line=None, radius=None, alpha=None, line_w=0.75):
    slide.items.append(("rect", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, radius=radius, alpha=alpha,
                                     line_w=line_w)))


def tricolour(slide, x, y, w, h):
    """Blue, lime and garnet in thirds: the brand rule, never behind text."""
    third = w / 3
    for i, colour in enumerate(("blue", "lime", "garnet")):
        rect(slide, x + i * third, y, third + (0.005 if i < 2 else 0), h, colour)


def picture(slide, key: str, x, y, w, h=None, *, line=None):
    """key: "logo", "favicon", "hero" or "chart-<name>". Height follows the picture when omitted."""
    slide.items.append(("picture", dict(key=key, x=x, y=y, w=w, h=h, line=line)))


def background(slide, key: str):
    slide.stage = key.removeprefix("bg-")


def logo(slide, x, y, w):
    picture(slide, "logo", x, y, w, w / LOGO_RATIO)


_KICKER = [0]  # running number of the content slides; reset in model()


def kicker(slide, label: str, y=0.55, *, on_dark=False):
    _KICKER[0] += 1
    num = f"{_KICKER[0]:02d}"
    rect(slide, MX, y - 0.015, 0.46, 0.28, "lime", radius=0.03)
    text(slide, MX, y + 0.02, 0.46, 0.25, [[(num, MONO, 11, "night", True)]], align=PP_ALIGN.CENTER)
    text(slide, MX + 0.62, y + 0.025, 9, 0.25, [[(label.upper(), MONO, 11, "lime" if on_dark else "garnet", True)]])


def title(slide, s: str, y=0.92, size=38, w=11.8, colour="navy"):
    text(slide, MX, y, w, 0.9, [[(s.upper(), DISPLAY, size, colour, True)]])


def footer(slide, n: int, total: int, *, on_dark=False):
    ink = "soft" if on_dark else "muted"
    logo(slide, MX, 6.9, 1.5)
    text(slide, MX + 1.72, 6.98, 1.25, 0.25, [[(SITE, MONO, 9.5, ink, True, SITE_URL)]])
    text(slide, MX + 2.98, 6.98, 0.2, 0.25, [[("·", MONO, 9.5, ink, False)]], align=PP_ALIGN.CENTER)
    text(slide, MX + 3.2, 6.98, 3.2, 0.25, [[(REPO, MONO, 9.5, ink, False, REPO_URL)]])
    text(slide, W - MX - 1.5, 6.98, 1.5, 0.25, [[(f"{n:02d} / {total:02d}", MONO, 9.5,
                                                    "white" if on_dark else "night", True)]], align=PP_ALIGN.RIGHT)
    tricolour(slide, 0, H - 0.08, W, 0.08)


def card(slide, x, y, w, h, *, fill="white", stripe=True):
    rect(slide, x, y, w, h, fill, line="ink200", radius=0.12)
    if stripe:
        tricolour(slide, x + 0.14, y, w - 0.28, 0.05)


def notes(slide, lines: list[str]):
    slide.notes = list(lines)


def body(t, size=15, colour="muted", bold=False):
    return (t, SANS, size, colour, bold)


_NUMERIC = re.compile(r"[\d.,/ ≈~m%s]+")


def table(slide, x, y, w, cols, header, rows, *, row_h=0.42, size=12, key_rows=(), key_cols=(), first_bold=True):
    """A table: navy header, paper rows, lime for the decisive cells. Numeric columns align right."""
    numeric_cols = {c for c in range(1, len(cols)) if all(_NUMERIC.fullmatch(str(row[c])) for row in rows)}
    slide.items.append(("table", dict(x=x, y=y, w=w, cols=list(cols), header=list(header), rows=[list(r) for r in rows],
                                      row_h=row_h, size=size, key_rows=tuple(key_rows), key_cols=tuple(key_cols),
                                      first_bold=first_bold, numeric_cols=numeric_cols)))


def table_cell(e: dict, r: int, c: int) -> tuple:
    """Style of one table cell, row 0 being the header: (fill, font role, size, bold, text colour,
    right-aligned). Shared by both writers."""
    right = c in e["numeric_cols"]
    if r == 0:
        return "night", MONO, e["size"] - 2.5, True, "white", right
    key_row, key_col = (r - 1) in e["key_rows"], c in e["key_cols"]
    is_key = key_row or key_col
    fill = ("keybg" if key_row and not key_col else "lime") if is_key else ("white" if r % 2 else "paper2")
    return (fill, MONO if right else SANS, e["size"], (c == 0 and e["first_bold"]) or is_key,
            "night" if (c == 0 or is_key) else "muted", right)


# --------------------------------------------------------------------------------------------
# Slides
# --------------------------------------------------------------------------------------------

DARK_STAGES = ("title", "divider", "numbers")


def model() -> list[Slide]:
    """The whole deck as data: what deck_pptx.py and deck_pdf.py write."""
    makers = [s_title, s_deliver, s_question, s_hard, s_judged,
              d_method, s_ideas, s_tags,
              d_decisions, s_pareto, s_dials, s_validation, s_log, s_sanity,
              d_trust, s_repro, s_reproduce, s_privacy,
              s_lessons, s_next, s_records, s_beyond, s_thanks]
    _KICKER[0] = 0
    keys = _Keys()
    slides = []
    for i, make in enumerate(makers, start=1):
        slide = Slide(make.__name__)
        make(slide, keys)
        if make not in (s_title, s_thanks):
            footer(slide, i, len(makers), on_dark=slide.stage in DARK_STAGES)
        slides.append(slide)
    return slides


def identity_panel(s, a, x, y, w, h, *, team_size=20):
    """Glass panel with the team, the knowledge hub and the repository (title and closing slides)."""
    rect(s, x, y, w, h, "glass", radius=0.14, alpha=0.62, line="silver", line_w=0.6)
    rect(s, x + 0.14, y, w - 0.28, 0.06, "lime")
    lx, rx = x + 0.4, x + w * 0.46
    text(s, lx, y + 0.32, 4, 0.3, [[("TEAM", MONO, 11, "lime", True)]])
    for i, name in enumerate(TEAM):
        yy = y + 0.72 + i * 0.44
        rect(s, lx, yy + 0.05, 0.3, 0.3, "lime", radius=0.03)
        text(s, lx, yy + 0.08, 0.3, 0.26, [[(str(i + 1), MONO, 12, "night", True)]], align=PP_ALIGN.CENTER)
        text(s, lx + 0.45, yy, w * 0.42, 0.4, [[(name.upper(), DISPLAY, team_size, "white", True)]])
    text(s, rx, y + 0.32, 4, 0.3, [[("KNOWLEDGE HUB", MONO, 11, "lime", True)]])
    picture(s, a["favicon"], rx, y + 0.68, 0.42, 0.42)
    text(s, rx + 0.56, y + 0.66, 4.5, 0.5, [[(SITE, DISPLAY, 26, "white", True, SITE_URL)]])
    text(s, rx, y + 1.16, 5, 0.3, [[body("The whole hackathon, hosted separately", 12, "soft")]])
    text(s, rx, y + 1.62, 4, 0.3, [[("CODE", MONO, 11, "lime", True)]])
    text(s, rx, y + 1.95, 5.5, 0.4, [[(REPO, MONO, 16, "white", True, REPO_URL)]])
    text(s, rx, y + 2.33, 5.5, 0.3, [[body("Initial Challenge in ", 12, "soft"), ("/initial-challenge", MONO, 12, "white", False)]])


def s_title(s, a):
    background(s, a["bg-title"])
    logo(s, MX - 0.1, 0.55, 6.6)
    rect(s, MX, 2.0, 2.05, 0.34, "lime", radius=0.03)
    text(s, MX, 2.05, 2.05, 0.3, [[("TECHNICAL REPORT", MONO, 12, "night", True)]], align=PP_ALIGN.CENTER)
    text(s, MX + 2.25, 2.06, 7, 0.3, [[("INITIAL CHALLENGE  ·  MORE THAN A HACK 2027", MONO, 12, "white", True)]])
    text(s, MX, 2.45, 8.5, 1.9, [{"runs": [("WHO HAS", DISPLAY, 76, "white", True)], "line": 0.84},
                                 {"runs": [("THE BALL?", DISPLAY, 76, "white", True)], "line": 0.84}])
    text(s, MX, 4.4, 7.2, 0.5, [[body("Decoding team possession frame by frame", 22, "white")]])
    # website and repository, top right
    rx, rw = W - MX - 4.6, 4.6
    text(s, rx, 0.62, rw, 0.3, [[("KNOWLEDGE HUB", MONO, 11, "lime", True)]], align=PP_ALIGN.RIGHT)
    text(s, rx, 0.9, rw, 0.4, [[(SITE, DISPLAY, 24, "white", True, SITE_URL)]], align=PP_ALIGN.RIGHT)
    picture(s, a["favicon"], W - MX - 2.72, 0.93, 0.36, 0.36)
    text(s, rx, 1.42, rw, 0.3, [[("CODE", MONO, 11, "lime", True)]], align=PP_ALIGN.RIGHT)
    text(s, rx, 1.68, rw, 0.32, [[(REPO, MONO, 14, "white", True, REPO_URL)]], align=PP_ALIGN.RIGHT)
    # the team
    y = 5.25
    rect(s, MX, y, W - 2 * MX, 1.2, "glass", radius=0.14, alpha=0.6, line="silver", line_w=0.6)
    rect(s, MX + 0.14, y, W - 2 * MX - 0.28, 0.06, "lime")
    text(s, MX + 0.4, y + 0.24, 3, 0.3, [[("THE SHREWDIES", MONO, 11, "lime", True)]])
    x, step = MX + 0.4, (W - 2 * MX - 0.8) / 4
    for i, name in enumerate(TEAM):
        rect(s, x, y + 0.65, 0.3, 0.3, "lime", radius=0.03)
        text(s, x, y + 0.68, 0.3, 0.26, [[(str(i + 1), MONO, 12, "night", True)]], align=PP_ALIGN.CENTER)
        text(s, x + 0.44, y + 0.58, step - 0.5, 0.42, [[(name.upper(), DISPLAY, 21, "white", True)]])
        x += step
    tricolour(s, 0, H - 0.12, W, 0.12)
    notes(s, [
        "Who has the ball? Our answer for the Initial Challenge of More Than a Hack 2027, by The Shrewdies: "
        "Yousef Fayez, Mahmoud Abubakr, Ahmed Awwad and Abdullah Ashmawei.",
        "In one sentence: we read the match the way a match official would (who can actually play the ball, "
        "has it left the pitch, has play stopped) and then let an exact algorithm write the single most coherent "
        "possession story for each half, with every parameter chosen away from the competition match.",
        "The code is on GitHub under Shrewdies/MTAH2027, in the initial-challenge folder; our knowledge hub for the "
        "whole hackathon is theshrewdies.com.",
    ])


def divider(s, a, num: str, head: str, sub: str, items: list[str]):
    background(s, a["bg-divider"])
    text(s, MX, 0.62, 6, 0.3, [[(f"PART {num}", MONO, 13, "lime", True)]])
    text(s, MX - 0.05, 0.85, 5, 2.2, [[(num, DISPLAY, 160, "lime", True)]])
    text(s, MX, 3.0, 8.5, 1.0, [[(head.upper(), DISPLAY, 60, "white", True)]])
    text(s, MX, 4.0, 7.5, 0.5, [[body(sub, 19, "white")]])
    y = 4.75
    for item in items:
        rect(s, MX, y + 0.09, 0.13, 0.13, "lime")
        text(s, MX + 0.3, y, 8, 0.32, [[(item.upper(), MONO, 13, "white", True)]])
        y += 0.37


def d_method(s, a):
    divider(s, a, "01", "The method", "Football evidence, then the most coherent story.",
            ["Four ideas", "Tags that calibrate themselves"])
    notes(s, ["Part one: how the pipeline reads the match and decodes it."])


def d_decisions(s, a):
    divider(s, a, "02", "The decisions", "Simulate to explore, validate on real labels to decide.",
            ["The Pareto front", "What was searched", "The selection rule", "Decision log", "The competition match"])
    notes(s, ["Part two: how every parameter was chosen, and why the submission uses the macro profile."])


def d_trust(s, a):
    divider(s, a, "03", "Trust", "Reproducible by construction. Private at every step.",
            ["The run sandbox", "Same file, every run", "Data privacy and security"])
    notes(s, ["Part three: how anyone reproduces the exact file, and how the match data was protected throughout."])


def s_deliver(s, a):
    background(s, a["bg-content"])
    kicker(s, "Deliverables")
    title(s, "What we deliver")
    items = [
        ("Per-frame labels", "199,319 video frames, each H (Barcelona in possession), A (Athletic Club in "
                             "possession) or D (ball dead).", None),
        ("Public repository", "One command reproduces the file in a pinned container. Initial Challenge in "
                              "/initial-challenge.", REPO_URL),
        ("Technical report", "Markdown, and this deck as PowerPoint and PDF, with the same numbers.", None),
        ("Knowledge hub", "The whole hackathon, hosted separately from this report.", SITE_URL),
    ]
    gap = 0.25
    cw, ch = (W - 2 * MX - 3 * gap) / 4, 3.1
    x = MX
    for i, (head, desc, link) in enumerate(items, start=1):
        card(s, x, 1.9, cw, ch)
        rect(s, x + 0.3, 2.22, 0.36, 0.32, "lime", radius=0.03)
        text(s, x + 0.3, 2.26, 0.36, 0.28, [[(str(i), MONO, 13, "night", True)]], align=PP_ALIGN.CENTER)
        text(s, x + 0.3, 2.75, cw - 0.55, 0.45, [[(head.upper(), DISPLAY, 22, "navy", True)]])
        text(s, x + 0.3, 3.3, cw - 0.55, 1.2, [[body(desc, 13)]])
        if link:
            label = REPO if link == REPO_URL else SITE
            text(s, x + 0.3, 4.5, cw - 0.5, 0.3, [[(label, MONO, 10.5, "blue", True, link)]])
        x += cw + gap
    rect(s, MX, 5.3, W - 2 * MX, 1.2, "white", line="night", radius=0.08, line_w=1.0)
    rect(s, MX, 5.3, 0.1, 1.2, "lime")
    text(s, MX + 0.4, 5.42, 3.0, 0.3, [[("MEASURED ON REAL LABELS", MONO, 11, "garnet", True)]])
    text(s, MX + 0.4, 5.72, 6.2, 0.7, [[
        ("spellF1 0.340", DISPLAY, 26, "navy", True), body("  vs 0.235      ", 15),
        ("macroF1 0.693", DISPLAY, 26, "navy", True), body("  vs 0.383", 15)]])
    text(s, MX + 6.9, 5.62, W - 2 * MX - 7.3, 0.8, [[body("against the organisers' baseline method, on an openly "
                                                          "labelled external match", 14)]], anchor=MSO_ANCHOR.MIDDLE)
    notes(s, [
        "Four deliverables. One: a label for each of the 199,319 video frames, H for Barcelona in possession, A for "
        "Athletic Club in possession, D for ball dead. It regenerates in under ten seconds, byte-identical on every run.",
        "Two: the public repository, where one command reproduces the file in a pinned container.",
        "Three: the technical report, as Markdown and as this deck, in PowerPoint and PDF.",
        "Four: our knowledge hub for the whole hackathon, theshrewdies.com, hosted separately.",
        "On an openly labelled external match the pipeline beats the organisers' baseline method on both official metrics.",
    ])


def s_question(s, a):
    background(s, a["bg-content"])
    kicker(s, "The question")
    title(s, "Every 1/25 of a second: who has the ball?", size=36)
    rows = [("H", "blue", "Barcelona in possession"), ("A", "garnet", "Athletic Club in possession"),
            ("D", "ink600", "ball dead: nobody has it")]
    y = 2.2
    for code, colour, label in rows:
        rect(s, MX, y, 0.62, 0.62, colour, radius=0.08)
        text(s, MX, y + 0.08, 0.62, 0.5, [[(code, DISPLAY, 28, "white", True)]], align=PP_ALIGN.CENTER)
        text(s, MX + 0.85, y + 0.14, 4.6, 0.45, [[body(label, 18, "night", True)]])
        y += 0.82
    text(s, MX, 4.85, 5.2, 1.8, [
        {"runs": [body("A team keeps possession through a loose ball or a scramble; it loses it only when the "
                       "opponent takes "), body("control", 15, "night", True), body(".")], "space_after": 8},
        {"runs": [body("When the referee stops play (throw-in, foul, goal kick) nobody has it: the ball is "),
                  body("dead", 15, "night", True), body(".")]},
    ])
    pic_w = 6.55
    picture(s, "hero", W - MX - pic_w, 2.15, pic_w, line="ink200")
    text(s, W - MX - pic_w, 2.15 + pic_w * 800 / 1280 + 0.12, pic_w, 0.3,
         [[("README ANIMATION · SYNTHETIC PLAY", MONO, 9.5, "muted", False)]])
    notes(s, [
        "The task: a label for each of the 199,319 video frames.",
        "H means Barcelona in possession, A means Athletic Club in possession, D means the ball is dead.",
        "A team keeps possession through a loose ball or a scramble; it loses it only when the opponent takes control.",
        "When the referee stops play, for a throw-in, a foul or a goal kick, nobody has it.",
        "The still on the right is from the animation in our README: synthetic play, labels computed by the decoder.",
    ])


def s_hard(s, a):
    background(s, a["bg-content"])
    kicker(s, "Why it's hard")
    title(s, "Two facts make it hard")
    text(s, MX, 1.72, 11.5, 0.5, [[body("What we are given is automatic: computer-vision tracking of 22 players and "
                                        "the ball, plus automatic tactical tags (\"build up\", \"set piece\", …).", 16)]])
    tiles = [
        ("41%", "The ball is missing on 41% of the frames that count",
         "Exactly in crowds, tackles and aerial duels: the moments that decide possession."),
        ("TEAM ONLY", "Players have no identities, only a team",
         "We must reason about teams, not individuals."),
    ]
    x, tw = MX, (W - 2 * MX - 0.4) / 2
    for big, head, sub in tiles:
        card(s, x, 2.45, tw, 4.15)
        text(s, x + 0.45, 2.7, tw - 0.9, 1.6, [[(big, DISPLAY, 110 if len(big) < 5 else 84, "navy", True)]],
             anchor=MSO_ANCHOR.BOTTOM)
        rect(s, x + 0.45, 4.38, 1.4, 0.1, "lime")
        text(s, x + 0.45, 4.6, tw - 0.9, 0.8, [[body(head, 19, "night", True)]], anchor=MSO_ANCHOR.BOTTOM)
        text(s, x + 0.45, 5.55, tw - 0.9, 0.8, [[body(sub, 15)]])
        x += tw + 0.4
    notes(s, [
        "Two facts make it hard.",
        "First, the ball is missing on 41% of the frames that count, and exactly in crowds, tackles and aerial duels, "
        "the moments that decide possession.",
        "Second, players have no identities, only a team, so we must reason about teams, not individuals.",
    ])


def s_judged(s, a):
    background(s, a["bg-content"])
    kicker(s, "How we are judged")
    title(s, "Two metrics, in plain words")
    cols = [
        ("RANKING", "spellF1", "Each possession is treated as one object, like a sentence in a story. A predicted "
         "possession scores only if it overlaps a real one well. Inventing extra possessions or splitting real ones "
         "is punished hard."),
        ("TIE-BREAK", "macroF1", "Frame-by-frame correctness for H, A and D, each class counting equally."),
    ]
    x, cw = MX, (W - 2 * MX - 0.4) / 2
    for kick, name, desc in cols:
        card(s, x, 1.95, cw, 2.95)
        text(s, x + 0.45, 2.3, cw - 0.9, 0.3, [[(kick, MONO, 11, "garnet", True)]])
        text(s, x + 0.45, 2.63, cw - 0.9, 0.8, [[(name, DISPLAY, 44, "navy", True)]])
        text(s, x + 0.45, 3.5, cw - 0.9, 1.3, [[body(desc, 15)]])
        x += cw + 0.4
    rect(s, MX, 5.3, 8.15, 0.7, "lime")
    text(s, MX + 0.2, 5.33, 8, 0.7, [[("COHERENCE BEATS TWITCHINESS.", DISPLAY, 38, "night", True)]])
    text(s, MX, 6.15, 11.8, 0.5, [[body("A method that flickers between teams can look fine frame by frame and "
                                        "still tell the wrong story.", 16)]])
    notes(s, [
        "spellF1 decides the ranking. Each possession is one object, like a sentence in a story; a predicted "
        "possession scores only if it overlaps a real one well. Inventing extra possessions or splitting real ones is "
        "punished hard.",
        "macroF1 is the tie-break: frame-by-frame correctness for H, A and D, each class counting equally.",
        "The lesson: coherence beats twitchiness.",
    ])


def s_ideas(s, a):
    background(s, a["bg-content"])
    kicker(s, "Our approach")
    title(s, "Four ideas")
    ideas = [
        ("1", "Evidence, frame by frame", "Score home, away and dead: who can play the ball, lines, "
         "stillness, set pieces."),
        ("2", "Silence is not a stoppage", "Ball untracked: every hypothesis scores zero, the story simply continues."),
        ("3", "Best story, not best frame", "Viterbi: evidence minus a fixed cost for every change of state."),
        ("4", "Two separate questions", "Tags may decide which team, never the length of a stoppage. "
         "A unit test guarantees it."),
    ]
    chart_w = 7.6
    cx = (W - chart_w) / 2
    card(s, cx - 0.2, 1.72, chart_w + 0.4, chart_w * 0.4 + 0.3, stripe=False)
    picture(s, a["chart-pipeline"], cx, 1.87, chart_w)
    gap = 0.2
    cw, ch, y = (W - 2 * MX - 3 * gap) / 4, 1.5, 5.25
    x = MX
    for num, head, desc in ideas:
        card(s, x, y, cw, ch, stripe=False)
        rect(s, x, y + 0.12, 0.07, ch - 0.24, "garnet")
        text(s, x + 0.25, y + 0.12, 0.45, 0.6, [[(num, DISPLAY, 30, "blue", True)]])
        text(s, x + 0.68, y + 0.1, cw - 0.85, 0.62, [[(head.upper(), DISPLAY, 15, "navy", True)]],
             anchor=MSO_ANCHOR.MIDDLE)
        text(s, x + 0.25, y + 0.8, cw - 0.45, 0.68, [[body(desc, 11)]])
        x += cw + gap
    notes(s, [
        "One: for every frame we score three hypotheses, home, away and dead. A player within 1.5 m of a ball moving "
        "slower than 7 m/s supports that player's team; ball beyond a line, players standing still, a placed ball and "
        "the start of a tagged set piece support dead; a fast ball inside the pitch says play is live.",
        "Two: silence is not a stoppage. When the ball is untracked every hypothesis scores zero. That is the "
        "challenge's own rule: possession stays with the last team that had it.",
        "Three: Viterbi, the decoder behind speech recognition and GPS map-matching, chooses the whole sequence that "
        "maximises evidence minus a fixed cost for every change of state. A touch or a deflection cannot flip "
        "possession; sustained control can.",
        "Four: alive-or-dead and which-team are separate questions. Tags may decide which team, never the length of a "
        "stoppage, and a unit test guarantees it.",
    ])


def s_tags(s, a):
    background(s, a["bg-content"])
    kicker(s, "Tags calibrate themselves")
    title(s, "Making the tags speak for themselves")
    text(s, MX, 1.72, 11.8, 0.7, [[body("Fourteen tag codes name a team, but what does the team mean? The pipeline "
                                        "measures, without any answers, how often each code's team agrees with "
                                        "visible ball control, and turns that into a weight (log-odds).", 16)]])
    card(s, MX, 2.7, 8.3, 3.1, stripe=False)
    pw = 7.9
    picture(s, a["chart-tag-weights"], MX + 0.2, 2.7 + (3.1 - pw * 0.33) / 2, pw)
    rx, rw = MX + 8.65, W - 2 * MX - 8.65
    facts = [("Mirrors", "Defending codes come out as exact mirrors of attacking ones; vague codes count for little."),
             ("Unsupervised", "Nobody told the program which is which."),
             ("A light hint", "Tags remain a light hint (scale 0.035); visible ball control always dominates.")]
    y = 2.7
    for head, desc in facts:
        rect(s, rx, y + 0.06, 0.08, 0.3, "lime")
        text(s, rx + 0.2, y, rw - 0.2, 0.35, [[(head.upper(), DISPLAY, 19, "navy", True)]])
        text(s, rx + 0.2, y + 0.38, rw - 0.2, 0.62, [[body(desc, 12.5)]])
        y += 1.06
    notes(s, [
        "For Build up the named team is the team with the ball; for Defending in middle third it is the team without it.",
        "Instead of hand-picking codes we measure agreement with visible ball control, with no answers involved.",
        "Build up agrees 86.5% of the time: weight +1.86. Defending in attacking third agrees 13.5%: weight -1.86. "
        "Progression 83.0%, +1.58. Players in the box 58.2%, +0.33.",
        "Nobody told the program which is which. Tags stay a light hint at scale 0.035.",
    ])


def s_pareto(s, a):
    background(s, a["bg-content"])
    kicker(s, "The Pareto front")
    title(s, "No single best: keep the whole front")
    cw, ch = 7.45, 4.82
    card(s, MX, 1.85, cw, ch, stripe=False)
    pw = cw - 0.3
    picture(s, a["chart-pareto"], MX + 0.15, 1.85 + (ch - pw * 0.62) / 2, pw)
    rx, rw = MX + cw + 0.4, W - 2 * MX - cw - 0.4
    text(s, rx, 1.85, rw, 0.3, [[("WHY A PARETO FRONT", MONO, 11, "garnet", True)]])
    text(s, rx, 2.17, rw, 1.3, [[body("spellF1 and macroF1 pull the switch costs in opposite directions. The search "
                                      "keeps every setting where neither metric can improve without the other getting "
                                      "worse, and an explicit rule selects from it.", 13)]])
    text(s, rx, 3.48, rw, 0.3, [[("SIMULATED MATCHES · 159 SETTINGS", MONO, 11, "garnet", True)]])
    rows = [("profile", "spellF1", "macroF1"), ("reasoned", "0.606", "0.835"),
            ("balanced (= spell)", "0.638", "0.857"), ("macro", "0.618", "0.859")]
    y = 3.85
    for i, (name, sp, ma) in enumerate(rows):
        head, key = i == 0, name == "macro"
        if key:
            rect(s, rx - 0.08, y - 0.06, rw + 0.16, 0.38, "keybg")
            rect(s, rx - 0.08, y - 0.06, 0.05, 0.38, "night")
        f, size, colour = (MONO, 10, "muted") if head else (SANS, 13, "night")
        text(s, rx, y, 2.2, 0.3, [[(name.upper() if head else name, f, size, colour, key)]])
        text(s, rx + 2.0, y, 1.0, 0.3, [[(sp, MONO, size, colour, key)]], align=PP_ALIGN.RIGHT)
        text(s, rx + rw - 1.0, y, 1.0, 0.3, [[(ma, MONO, size, colour, key)]], align=PP_ALIGN.RIGHT)
        rect(s, rx, y + 0.34, rw, 0.012, "ink200")
        y += 0.42
    text(s, rx, 5.65, rw, 1.0, [[body("An evolutionary multi-objective search in the spirit of NSGA-II, scored with "
                                      "the official scorer. Seeded; reruns in about 15 s.", 12)]])
    notes(s, [
        "spellF1, the ranking metric, and macroF1, the tie-break, pull the switch costs in opposite directions, so "
        "there is no single best: there is a Pareto front, where neither metric can improve without the other getting "
        "worse. The search keeps the whole front and a written rule selects from it.",
        "We built a simulator from football rules of thumb: possessions of about 11 s, a third ending in a stoppage of "
        "about 20 s, the ball missing on 41% of frames.",
        "The search evaluated 159 settings with the official scorer and froze three profiles: reasoned, balanced and macro. "
        "These numbers are simulated, not real. The search is seeded and reruns in about 15 seconds.",
    ])


def s_dials(s, a):
    background(s, a["bg-content"])
    kicker(s, "What was searched")
    title(s, "Seven dials searched, one constant kept")
    header = ["dial", "what it controls", "reasoned", "balanced (= spell)", "macro"]
    rows = [
        ["team switch cost", "clear control needed to change possession", "10.0", "8.35", "4.23"],
        ["alive/dead switch cost", "evidence needed to start or end a stoppage", "20.0", "12.50", "9.43"],
        ["out-of-bounds weight", "ball beyond a line", "3.0", "2.49", "3.30"],
        ["stillness weight", "players standing still", "0.3", "0.80", "0.79"],
        ["stationary-ball weight", "ball placed and motionless", "0.5", "0.51", "0.36"],
        ["set-piece weight", "start of a tagged set piece", "0.6", "0.56", "0.66"],
        ["tag scale", "weight of the calibrated tag hint", "0.1", "0.049", "0.035"],
        ["control radius", "not searched: a physical constant", "1.5 m", "1.5 m", "1.5 m"],
    ]
    table(s, MX, 1.8, 8.0, [2.3, 3.6, 1.1, 1.6, 1.0], header, rows, row_h=0.43, size=12.5, key_cols=(4,))
    rx, rw = MX + 8.4, W - 2 * MX - 8.4
    pts = [("Learned", "Declare stoppages more readily: lower alive/dead switch cost, more weight on stillness."),
           ("Learned", "Keep tags a light hint: tag scale from 0.1 down to 0.035–0.049."),
           ("Excluded", "The control radius. Left free, the simulator pushed it to an unrealistic 0.8 m. It stays "
                        "1.5 m, the default possession zone of the FIFA method implementation in databallpy.")]
    y = 1.8
    for head, desc in pts:
        rect(s, rx, y + 0.05, 0.08, 0.3, "lime" if head == "Learned" else "garnet")
        text(s, rx + 0.2, y, rw - 0.2, 0.35, [[(head.upper(), DISPLAY, 19, "navy", True)]])
        text(s, rx + 0.2, y + 0.38, rw - 0.2, 1.1, [[body(desc, 12.5)]])
        y += 1.2 if head == "Learned" else 1.5
    notes(s, [
        "Seven dials were searched: the team switch cost, the alive/dead switch cost, and the weights for "
        "out-of-bounds, stillness, a stationary ball, set pieces and the tag hint.",
        "The control radius was excluded on purpose. Left free, the search pushed it to 0.8 m, an artefact of a "
        "simulator that keeps the ball too close to the carrier, so it stays a physical constant of 1.5 m.",
        "The macro column is the submitted profile: a team switch cost of about 4, against about 8 for balanced "
        "and 10 for reasoned.",
    ])


def s_validation(s, a):
    background(s, a["bg-content"])
    kicker(s, "The selection rule")
    title(s, "Real labels decide: why macro")
    cw, ch = 7.45, 4.25
    card(s, MX, 1.85, cw, ch, stripe=False)
    pw = cw - 0.3
    picture(s, a["chart-validation"], MX + 0.15, 1.85 + (ch - pw * 0.47) / 2, pw)
    text(s, MX, 6.25, cw, 0.3, [[("OPEN DFL BUNDESLIGA MATCH · BALL HIDDEN ON 41% OF FRAMES · OFFICIAL METRIC",
                                 MONO, 9.5, "muted", False)]])
    rx, rw = MX + cw + 0.4, W - 2 * MX - cw - 0.4
    rect(s, rx, 1.85, rw, 0.62, "lime", radius=0.06)
    text(s, rx + 0.2, 1.92, rw - 0.4, 0.5, [[("SIMULATE TO EXPLORE, VALIDATE ON REAL LABELS TO DECIDE", DISPLAY, 16, "night", True)]],
         anchor=MSO_ANCHOR.MIDDLE)
    pts = [
        ("Better on both", "Macro beats balanced on both metrics: 0.340 / 0.693 vs 0.286 / 0.686, including spellF1, "
                           "the ranking metric."),
        ("Switch cost: about 4", "frames of clear control, against about 8 for balanced and 10 for "
                                 "reasoned. Possession changes more readily."),
        ("Many short possessions", "That is what real matches contain. Found: 249 (truth 402); baseline method 570."),
        ("Follow the real world", "When the simulator and the real world disagree. The profile switch "
                                  "keeps every alternative one argument away."),
    ]
    y = 2.7
    for head, desc in pts:
        text(s, rx, y, rw, 0.35, [[(head.upper(), DISPLAY, 18, "navy", True)]])
        text(s, rx, y + 0.35, rw, 0.62, [[body(desc, 12)]])
        y += 1.0
    notes(s, [
        "A simulator is a hypothesis, so the final choice was made on a real match we did not label: the open DFL "
        "Bundesliga data, CC-BY 4.0, where every frame carries the league's official alive/dead and possession flags.",
        "We hid the ball on 41% of frames to mirror the competition tracking and scored with the official metric.",
        "Baseline method: spellF1 0.235, macroF1 0.383. Ours: reasoned 0.249 / 0.661, balanced 0.286 / 0.686, "
        "macro 0.340 / 0.693.",
        "Macro is better on both metrics. It changes possession more readily, a team switch cost of about 4 frames of "
        "clear control against about 8 for balanced and 10 for reasoned, which matches what the real data revealed: "
        "many short possessions.",
        "The rule: simulate to explore, validate on real labels to decide.",
    ])


def s_log(s, a):
    background(s, a["bg-content"])
    kicker(s, "Decision log")
    title(s, "The decisions behind the final pipeline")
    header = ["decision", "what it means", "why"]
    rows = [
        ["Missing ball = no evidence", "an untracked ball scores zero for every state; possession stays with the "
         "last team in control", "\"no ball = stoppage\" invents stoppages inside possessions"],
        ["Alive/dead separate from which-team", "tags may decide which team, never the length of a stoppage; a unit "
         "test guarantees it", "hand-picked attacking tags quietly shortened stoppages"],
        ["Tags calibrated automatically", "weights from agreement with visible ball control, without any answers",
         "defending codes come out as exact mirrors of attacking ones (+1.86 / −1.86)"],
        ["Control radius kept physical", "1.5 m, outside the search",
         "left free, the simulator pushed it to an unrealistic 0.8 m"],
        ["Profile chosen on real labels", "macro, selected on the labelled external match",
         "beats balanced on both metrics: 0.340 / 0.693 vs 0.286 / 0.686"],
        ["Public window: a check, not a judge", "correctness check on candidate files only",
         "17 possessions are too few to choose between settings"],
    ]
    table(s, MX, 1.75, W - 2 * MX, [3.1, 4.6, 4.2], header, rows, row_h=0.56, size=12, key_rows=(4,))
    rect(s, MX, 6.05, W - 2 * MX, 0.68, "white", line="night", radius=0.08, line_w=1.0)
    rect(s, MX, 6.05, 0.1, 0.68, "lime")
    text(s, MX + 0.35, 6.1, W - 2 * MX - 0.6, 0.58, [
        {"runs": [("OUR RULE  ", MONO, 11, "garnet", True),
                  body("Parameters are fitted only on simulated matches and openly licensed external data, never on "
                       "the competition match.", 14, "night", True)]}], anchor=MSO_ANCHOR.MIDDLE)
    notes(s, [
        "Six design decisions shaped the final pipeline.",
        "Missing ball means no evidence: possession stays with the last team in control, because treating a lost ball "
        "as a stoppage invents stoppages inside possessions.",
        "Alive-or-dead is kept separate from which-team: tags may decide the team, never the length of a stoppage, "
        "because hand-picked attacking tags quietly shortened stoppages.",
        "Tags are calibrated automatically from agreement with visible ball control, without any answers.",
        "The control radius stays a physical 1.5 m; left free, the simulator pushed it to an unrealistic 0.8 m.",
        "The profile was chosen on real external labels: macro beats balanced on both metrics. The public window is a "
        "correctness check only.",
        "Our rule: parameters are fitted only on simulated and openly licensed external data, never on the "
        "competition match.",
    ])


def s_sanity(s, a):
    background(s, a["bg-content"])
    kicker(s, "The competition match")
    title(s, "Sanity checks without ground truth")
    header = ["", "reasoned", "submitted (macro)"]
    rows = [["possessions / mean length", "215 / 18.8 s", "337 / 11.5 s"],
            ["dead-ball share of match time", "36%", "39%"],
            ["Barcelona's share of live play", "62%", "64%"]]
    table(s, MX, 1.9, 7.0, [3.2, 1.8, 2.0], header, rows, row_h=0.6, size=15, key_cols=(2,), first_bold=False)
    text(s, MX, 4.6, 7.0, 1.2, [[body("337 possessions is in the range of a real match (402 on the DFL match), and "
                                      "39% dead time is close to typical effective-playing-time figures in elite "
                                      "football.", 14)]])
    rx, rw = MX + 7.4, W - 2 * MX - 7.4
    card(s, rx, 1.9, rw, 4.75)
    text(s, rx + 0.35, 2.2, rw - 0.7, 0.3, [[("THE PUBLIC 5-MINUTE WINDOW", MONO, 11, "garnet", True)]])
    text(s, rx + 0.35, 2.6, rw - 0.7, 4.0, [
        {"runs": [body("Only a correctness check on candidate files: format, frames aligned, teams the right way "
                       "round (share error 0.016 on the submitted file). ", 13.5),
                  body("It never chose between them.", 13.5, "night", True)], "space_after": 9},
        {"runs": [body("Another profile scored higher there (spellF1 0.43 vs 0.36), and we submitted macro "
                       "anyway.", 13.5)], "space_after": 9},
        {"runs": [body("With 17 possessions, one possession moves spellF1 by about six points, and the organisers "
                       "show that this window prefers the variant that loses on the full match. The decision rests on "
                       "the fully labelled external match.", 13.5)]},
    ])
    notes(s, [
        "Without ground truth we can still check the output is sensible.",
        "Submitted macro profile: 337 possessions with a mean length of 11.5 s, 39% dead-ball time, Barcelona 64% of "
        "live play. The reasoned profile: 215 possessions, 18.8 s, 36% dead, 62%.",
        "The public 5-minute window served only as a correctness check on candidate files, never to choose between "
        "them. For transparency: another profile scored higher there, 0.43 vs 0.36 spellF1, and we submitted macro "
        "anyway: with 17 possessions one possession moves spellF1 by about six points.",
    ])


def s_repro(s, a):
    background(s, a["bg-content"])
    kicker(s, "Reproducibility")
    title(s, "The run sandbox")
    fw = 9.6
    fx = (W - fw) / 2
    card(s, fx - 0.2, 1.65, fw + 0.4, fw * 0.4 + 0.3, stripe=False)
    picture(s, a["chart-sandbox"], fx, 1.8, fw)
    facts = [("Digest-pinned", "python:3.11.11-slim-bookworm by sha256"),
             ("Offline or PyPI", "both build paths tested; wheels folder"),
             ("Multi-arch", "linux/arm64 and linux/amd64")]
    x, fw3 = MX, (W - 2 * MX) / 3
    for big, small in facts:
        rect(s, x, 6.2, 0.08, 0.5, "lime")
        text(s, x + 0.2, 6.13, fw3 - 0.3, 0.4, [[(big.upper(), DISPLAY, 20, "navy", True)]])
        text(s, x + 0.2, 6.47, fw3 - 0.3, 0.3, [[body(small, 11.5)]])
        x += fw3
    notes(s, [
        "Source and data enter the container through read-only mounts. The base image, python 3.11.11 slim bookworm, "
        "is pinned by its sha256 digest; numpy 2.2.6 and pandas 2.2.3 and their four dependencies are pinned.",
        "Runs use no network, a read-only root filesystem and a tmpfs /tmp. The only writable mount is the output "
        "folder, outside the repository.",
        "An optional offline wheels folder builds the image with no network; both the offline and the PyPI paths "
        "were tested. The image is multi-arch: linux/arm64 and linux/amd64.",
    ])


def s_reproduce(s, a):
    background(s, a["bg-content"])
    kicker(s, "Reproducibility")
    title(s, "Same file, every run")
    rect(s, MX, 1.8, W - 2 * MX, 2.3, "night", radius=0.12)
    rect(s, MX, 1.8, 0.1, 2.3, "lime")
    lines = [
        [("$ ", MONO, 14, "lime", True), ("scripts/run.sh build && scripts/run.sh test && scripts/run.sh submit \"$DATA\" outputs",
                                         MONO, 14, "white", False)],
        [(" ", MONO, 8, "ink400", False)],
        [("# Windows", MONO, 12, "ink400", False)],
        [("> ", MONO, 14, "lime", True), (".\\scripts\\build.ps1", MONO, 14, "white", False)],
        [("> ", MONO, 14, "lime", True), (".\\scripts\\test.ps1", MONO, 14, "white", False)],
        [("> ", MONO, 14, "lime", True), (".\\scripts\\run_protected.ps1 -DataDir \"$DATA\"", MONO, 14, "white", False)],
    ]
    text(s, MX + 0.45, 2.05, W - 2 * MX - 0.9, 2.0, [{"runs": r, "space_after": 2} for r in lines])
    facts = [
        ("Determinism", "No randomness in decoding. Byte-identical output, LF line endings, under 10 s on a laptop CPU."),
        ("Frozen decisions", "profiles.json and pareto_front.json; the seeded search reruns in about 15 s."),
        ("Checks", "15 behaviour tests on fabricated scenes, no data needed; the official validator on every file."),
        ("Dependencies", "numpy 2.2.6 and pandas 2.2.3 plus four dependencies, pinned; offline wheels build tested."),
        ("Run sandbox", "--network none, read-only root filesystem, tmpfs /tmp; only the output folder is writable."),
        ("External validation", "Public data: DFL/IDSSE open data, CC-BY 4.0, figshare DOI 10.6084/m9.figshare.28196177."),
    ]
    gap = 0.25
    cw = (W - 2 * MX - 2 * gap) / 3
    for i, (head, desc) in enumerate(facts):
        x = MX + (i % 3) * (cw + gap)
        y = 4.3 + (i // 3) * 1.25
        card(s, x, y, cw, 1.12, stripe=False)
        rect(s, x, y + 0.12, 0.07, 0.88, "lime")
        text(s, x + 0.25, y + 0.1, cw - 0.4, 0.35, [[(head.upper(), DISPLAY, 16, "navy", True)]])
        text(s, x + 0.25, y + 0.44, cw - 0.4, 0.66, [[body(desc, 11)]])
    notes(s, [
        "One line on Linux or macOS: build, test, submit. On Windows, the three PowerShell scripts.",
        "No randomness in decoding: the output is byte-identical on every run, written with LF line endings, in under "
        "ten seconds on a laptop CPU.",
        "The decisions are frozen in profiles.json and pareto_front.json; the seeded search reruns in about 15 seconds.",
        "15 behaviour tests need no data, and the organisers' official validator runs on every produced file.",
        "Dependencies are pinned and the image also builds offline; the external validation reproduces from public, "
        "openly licensed data.",
    ])


def s_privacy(s, a):
    background(s, a["bg-content"])
    kicker(s, "Data privacy and security")
    title(s, "Considered at every step")
    items = [
        ("Storage", "The competition data is never committed. No match data in the repository; .gitignore blocks the "
                    "data paths; DATA.md says where to place it locally."),
        ("Processing", "Only on the team's own laptop, inside the offline container with read-only mounts. Never "
                       "uploaded to any external service, cloud platform or hosted model, as the terms require."),
        ("Outputs", "Generated outputs live outside the repository, in a separate folder, and git ignores the output "
                    "folders. Everything published (report, website) is aggregate metrics only."),
        ("Integrity", "No hand labels. No use of the video to label or check outputs. No tuning on any ground truth of "
                      "the competition match. The public window: a correctness check only."),
        ("Search and validation", "Parameter search and validation used only synthetic matches and openly licensed "
                                  "external data."),
        ("Supply chain", "A minimal dependency set (numpy, pandas), pinned versions, a digest-pinned base image and an "
                         "offline build option."),
    ]
    gap = 0.25
    cw, ch = (W - 2 * MX - 2 * gap) / 3, 2.32
    for i, (head, desc) in enumerate(items):
        x = MX + (i % 3) * (cw + gap)
        y = 1.8 + (i // 3) * (ch + 0.22)
        card(s, x, y, cw, ch)
        text(s, x + 0.3, y + 0.25, 0.5, 0.3, [[(f"{i + 1:02d}", MONO, 11, "garnet", True)]])
        text(s, x + 0.3, y + 0.52, cw - 0.6, 0.4, [[(head.upper(), DISPLAY, 20, "navy", True)]])
        text(s, x + 0.3, y + 0.98, cw - 0.55, ch - 1.05, [[body(desc, 12)]])
    notes(s, [
        "The competition data is never committed: the repository holds no match data, .gitignore blocks the data paths, "
        "and DATA.md says where to place it locally.",
        "All processing of the match data happened on the team's own laptop, inside an offline container with "
        "read-only mounts. It was never uploaded to any external service, cloud platform or hosted model, as the "
        "competition terms require.",
        "Outputs live outside the repository; everything published is aggregate metrics only.",
        "No hand labels, no use of the video to label or check outputs, no tuning on any ground truth of the "
        "competition match. The public 5-minute window was a correctness check on candidate files, never a way to choose.",
        "Search and validation used only synthetic and openly licensed external data, and the supply chain is minimal "
        "and pinned.",
    ])


def s_lessons(s, a):
    background(s, a["bg-content"])
    kicker(s, "Lessons learned")
    title(s, "What we tried and learned")
    rows = [
        ("Nearest player + \"no ball = stoppage\"", "(the baseline idea) invents stoppages inside possessions.",
         "Silence is not a stoppage."),
        ("Hand-picked attacking tags", "helped the team question but quietly shortened stoppages.",
         "Separate alive/dead from which-team; calibrate all tags automatically."),
        ("Simulator-only tuning", "pushed one constant to an impossible value and ranked two profiles the wrong way round.",
         "Simulate to explore, validate on real labels to decide."),
    ]
    y = 1.95
    for i, (tried, why, learned) in enumerate(rows, start=1):
        card(s, MX, y, W - 2 * MX, 1.42, stripe=False)
        rect(s, MX, y + 0.14, 0.07, 1.14, "garnet")
        text(s, MX + 0.35, y + 0.3, 0.8, 0.8, [[(f"{i:02d}", DISPLAY, 40, "blue", True)]])
        text(s, MX + 1.3, y + 0.3, 5.1, 0.9, [
            {"runs": [body(tried, 15, "night", True)], "space_after": 2},
            {"runs": [body(why, 13)]},
        ])
        text(s, MX + 6.75, y + 0.33, 0.5, 0.6, [[(" →", MONO, 24, "ink400", True)]])
        rect(s, MX + 7.25, y + 0.22, W - 2 * MX - 7.45, 0.98, "keybg", radius=0.06)
        text(s, MX + 7.45, y + 0.25, W - 2 * MX - 7.85, 0.92, [[(learned.upper(), DISPLAY, 20, "navy", True)]],
             anchor=MSO_ANCHOR.MIDDLE)
        y += 1.58
    notes(s, [
        "First: the baseline idea, nearest player plus no ball means stoppage, invents stoppages inside possessions. "
        "Hence: silence is not a stoppage.",
        "Second: hand-picked attacking tags helped the team question but quietly shortened stoppages. Hence: separate "
        "alive/dead from which-team, and calibrate all tags automatically.",
        "Third: simulator-only tuning pushed one constant to an impossible value and ranked two profiles the wrong way "
        "round. Hence: simulate to explore, validate on real labels to decide.",
    ])


def s_next(s, a):
    background(s, a["bg-content"])
    kicker(s, "What comes next")
    title(s, "The ball nobody can see is next")
    lw = 4.3
    card(s, MX, 1.9, lw, 4.05)
    text(s, MX + 0.4, 2.2, lw - 0.8, 0.3, [[("THE OPEN FRONTIER", MONO, 11, "garnet", True)]])
    text(s, MX + 0.4, 2.5, lw - 0.8, 1.3, [[("41%", DISPLAY, 96, "navy", True)]])
    rect(s, MX + 0.4, 3.95, 1.4, 0.1, "lime")
    text(s, MX + 0.4, 4.2, lw - 0.8, 1.7, [
        {"runs": [body("of the frames that count: the ball the tracker cannot see. That is where the next gains "
                       "are. ", 14), body("We are going after it.", 14, "night", True)]}])
    rx, rw = MX + lw + 0.4, W - 2 * MX - lw - 0.4
    steps = [
        ("A single source of truth", "Three witnesses of one match, video frames, tactical-camera tracking and "
                                     "broadcast-camera tracking, each filling the gaps of the others."),
        ("Ball-free reasoning", "Possession read from player interactions alone, fused with the evidence decoder."),
        ("On-device vision", "The frames the tracker loses, seen again on the laptop's NPU."),
        ("Evidence learned on open labels", "Weights learned from openly labelled matches, never the competition match."),
        ("Duration-aware decoding", "249 possessions found, 402 in the external match: the measurable gap to close."),
        ("Possession as language", "The possession story turned into language, on the device."),
    ]
    rect(s, rx - 0.15, 1.82, rw + 0.15, 1.0, "keybg", radius=0.08)   # the lead direction
    y = 1.9
    for i, (head, desc) in enumerate(steps, start=1):
        rect(s, rx, y + 0.06, 0.42, 0.27, "lime", radius=0.03)
        text(s, rx, y + 0.1, 0.42, 0.25, [[(f"{i:02d}", MONO, 11, "night", True)]], align=PP_ALIGN.CENTER)
        text(s, rx + 0.65, y, rw - 0.65, 0.36, [[(head.upper(), DISPLAY, 18, "navy", True)]])
        text(s, rx + 0.65, y + 0.35, rw - 0.75, 0.5, [[body(desc, 11.5, "night" if i == 1 else "muted")]])
        y += 1.0 if i == 1 else 0.64
    rect(s, MX, 6.12, W - 2 * MX, 0.58, "white", line="night", radius=0.06, line_w=1.0)
    rect(s, MX, 6.12, 0.1, 0.58, "lime")
    text(s, MX + 0.35, 6.17, W - 2 * MX - 0.6, 0.48, [[
        ("ROADMAP  ", MONO, 11, "garnet", True),
        body("The plan, step by step: ", 13, "night", True),
        (ROADMAP, SANS, 13, "blue", True, ROADMAP_URL)]], anchor=MSO_ANCHOR.MIDDLE)
    notes(s, [
        "The ball the tracker cannot see, on 41% of the frames that count, is where the next gains are, and we are "
        "going after it.",
        "The lead direction is a single source of truth for the match: three witnesses, video frames, "
        "tactical-camera tracking and broadcast-camera tracking, each filling the gaps of the others.",
        "Then: ball-free reasoning over player interactions, fused with the evidence decoder; on-device "
        "vision on the laptop's NPU; evidence learned on open labels; duration-aware decoding, where 249 possessions "
        "found against 402 on the external match is the measurable gap to close; and possession turned into language "
        "on the device.",
        "The plan, step by step, is on the roadmap at theshrewdies.com/challenges/roadmap/.",
    ])


def s_records(s, a):
    background(s, a["bg-numbers"])
    kicker(s, "The squad in numbers", on_dark=True)
    title(s, "One report. A whole playbook behind it.", size=40, colour="white")
    text(s, MX, 1.72, 11.8, 0.4, [[body("Four Shrewdies, and everything we scouted, studied and wrote to get to this "
                                        "answer. All open at ", 15, "white"),
                                   (SITE, SANS, 15, "lime", True, SITE_URL), body(".", 15, "white")]])
    heroes = [h for h in [
        (YEARS_OF_EXPERIENCE, "years, combined", "of professional experience"),
        (COUNTRIES, f"countries, {CULTURES} cultures", "of professional journeys"),
        (PATENTS, "patents", "in the squad"),
        (KNOWLEDGE_PAGES, "knowledge pages", "on " + SITE),
    ] if h[0]]
    gap = 0.25
    cw = (W - 2 * MX - (len(heroes) - 1) * gap) / len(heroes)
    x, y, ch = MX, 2.25, 2.1
    for big, unit, line in heroes:
        rect(s, x, y, cw, ch, "glass", radius=0.14, alpha=0.62, line="silver", line_w=0.6)
        rect(s, x + 0.14, y, cw - 0.28, 0.06, "lime")
        text(s, x + 0.3, y + 0.14, cw - 0.5, 1.2, [[(big, DISPLAY, 84, "lime", True)]])
        text(s, x + 0.3, y + 1.32, cw - 0.5, 0.36, [[(unit.upper(), DISPLAY, 21, "white", True)]])
        text(s, x + 0.3, y + 1.68, cw - 0.5, 0.36, [[body(line, 11.5, "soft")]])
        x += cw + gap
    support = [
        (SPECIALISMS, "specialisms", "each mapped to football intelligence"),
        (DATASETS, "datasets scouted", f"{ATLAS_PAGES} atlas pages"),
        (MODELS, "models, methods and tools reviewed", f"{JUDGED_PAGES} judged pages"),
        (ARCH_STUDIES, f"architecture studies in {ARCH_FAMILIES} families", "our DNA in architecting solutions"),
        (INSIGHT_PAGES, "insight pages", "on how we read the challenge"),
    ]
    gap = 0.2
    cw = (W - 2 * MX - (len(support) - 1) * gap) / len(support)
    x, y, ch = MX, 4.55, 2.15
    for big, label, sub in support:
        rect(s, x, y, cw, ch, "white", radius=0.12)
        text(s, x + 0.25, y + 0.1, 1.2, 0.75, [[(big, DISPLAY, 46, "navy", True)]])
        rect(s, x + 0.25, y + 0.88, 0.6, 0.07, "lime")
        text(s, x + 0.25, y + 1.02, cw - 0.45, 0.5, [[body(label, 12.5, "night", True)]])
        text(s, x + 0.25, y + 1.56, cw - 0.45, 0.5, [[body(sub, 10.5)]])
        x += cw + gap
    notes(s, [
        "This report is one page of a much bigger playbook.",
        f"The squad: {YEARS_OF_EXPERIENCE} years of professional experience combined, professional journeys across "
        f"{COUNTRIES} countries and {CULTURES} cultures, and {PATENTS} patents.",
        f"{SPECIALISMS} specialisms, each mapped to football intelligence on the site.",
        f"On the way to this answer we scouted {DATASETS} datasets, reviewed {MODELS} models, methods and tools, and "
        f"wrote {ARCH_STUDIES} architecture studies in {ARCH_FAMILIES} families: our DNA in architecting solutions.",
        f"{INSIGHT_PAGES} insight pages cover how we read the challenge. In all, {KNOWLEDGE_PAGES} knowledge pages are "
        "open at theshrewdies.com.",
    ])


def s_beyond(s, a):
    background(s, a["bg-content"])
    kicker(s, "Beyond this report")
    title(s, "Six doors into the playbook")
    text(s, MX, 1.7, 11.8, 0.4, [[body("This deck covers the Initial Challenge only. The rest is open at ", 16),
                                  (SITE, SANS, 16, "blue", True, SITE_URL),
                                  body(", hosted separately. Pick a door.", 16)]])
    doors = [
        ("Team", "/team/", f"Four Shrewdies, {COUNTRIES} countries, {SPECIALISMS} specialisms: why this mix matters "
                           "for football."),
        ("Challenges", "/challenges/", f"{INSIGHT_PAGES} insight pages on how we read the problem, and the roadmap to what "
                                       "comes next."),
        ("Datasets", "/datasets/", f"{DATASETS} datasets scouted. See what each one can teach a possession model."),
        ("Solutions", "/solutions/", f"{MODELS} models, methods and tools for football intelligence, mapped and judged."),
        ("Architecture", "/architecture/single-source-of-truth/",
         "Our DNA in architecting football intelligence. Start with the single source of truth."),
        ("On-device", "/on-device/", "Security, data protection and reproducibility, on our own machine and "
                                     "hardware."),
    ]
    gap = 0.2
    dw, dh, top = (W - 2 * MX - (len(doors) - 1) * gap) / len(doors), 3.55, 1.4
    y = 2.3
    for i, (name, path, hook) in enumerate(doors):
        x = MX + i * (dw + gap)
        colour = f"door{i + 1}"
        rect(s, x, y, dw, dh, "white", line="ink200", radius=0.12)
        rect(s, x, y, dw, top, colour, radius=0.12)            # the door: a floodlit panel ...
        rect(s, x, y + top - 0.3, dw, 0.3, colour)             # ... with a square foot
        rect(s, x + dw - 0.34, y + 0.24, 0.12, 0.4, "lime", radius=0.05)   # the handle
        text(s, x + 0.2, y + 0.24, 0.6, 0.25, [[(f"{i + 1:02d}", MONO, 11, "lime", True)]])
        text(s, x + 0.2, y + 0.8, dw - 0.3, 0.45, [[(name.upper(), DISPLAY, 21, "white", True, SITE_URL + path)]])
        text(s, x + 0.2, y + top + 0.2, dw - 0.38, 1.4, [[body(hook, 11.5)]])
        head, _, leaf = path.strip("/").partition("/")
        label = [[("→ /" + head + "/", MONO, 9.5, "blue", True, SITE_URL + path)]]
        if leaf:
            label.append([(leaf + "/", MONO, 7.5, "blue", True)])
        text(s, x + 0.2, y + dh - 0.7, dw - 0.25, 0.56, label, anchor=MSO_ANCHOR.BOTTOM)
    rect(s, MX, 6.08, W - 2 * MX, 0.62, "night", radius=0.08)
    rect(s, MX, 6.08, 0.1, 0.62, "lime")
    text(s, MX + 0.35, 6.13, W - 2 * MX - 0.6, 0.52, [[
        ("NEXT  ", MONO, 11, "lime", True),
        body("Who has the ball was the first question. ", 13, "white", True),
        (ROADMAP, SANS, 13, "lime", True, ROADMAP_URL),
        body(" shows where we take the answer in the Innovative Challenge.", 13, "white")]], anchor=MSO_ANCHOR.MIDDLE)
    notes(s, [
        "This deck covers the Initial Challenge only. The rest is open at theshrewdies.com, hosted separately. "
        "Six doors lead in.",
        f"Team: four Shrewdies, {COUNTRIES} countries, {SPECIALISMS} specialisms, and why this mix matters for football.",
        f"Challenges: {INSIGHT_PAGES} insight pages on how we read the problem, and the roadmap.",
        f"Datasets: {DATASETS} datasets scouted, and what each one can teach a possession model.",
        f"Solutions: {MODELS} models, methods and tools for football intelligence, mapped and judged.",
        "Architecture: our DNA in architecting football intelligence. Start with the single source of truth.",
        "On-device: security, data protection and reproducibility, on our own machine and hardware.",
        "Who has the ball was the first question. The roadmap at theshrewdies.com/challenges/roadmap/ shows where we "
        "take the answer in the Innovative Challenge.",
    ])


def s_thanks(s, a):
    background(s, a["bg-title"])
    logo(s, MX - 0.1, 0.5, 6.0)
    text(s, MX, 1.75, 8, 1.4, [[("THANK YOU", DISPLAY, 96, "white", True)]])
    text(s, MX, 3.17, 11, 0.4, [[body("Who has the ball was the first question.", 19, "white", True)]])
    text(s, MX, 3.54, 11, 0.4, [[body("What comes next: ", 19, "white"),
                                 (ROADMAP, SANS, 19, "lime", True, ROADMAP_URL)]])
    identity_panel(s, a, MX, 4.08, W - 2 * MX, 2.7)
    tricolour(s, 0, H - 0.12, W, 0.12)
    notes(s, [
        "Thank you. The full reasoning is in TECHNICAL.md; the README has the commands to reproduce the submission.",
        "The code is at github.com/Shrewdies/MTAH2027, Initial Challenge in /initial-challenge; the knowledge hub for "
        "the whole hackathon is theshrewdies.com.",
        "Who has the ball was the first question. What comes next is on the roadmap at "
        "theshrewdies.com/challenges/roadmap/.",
        "Questions welcome.",
    ])
