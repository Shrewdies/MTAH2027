"""README hero: a choreographed synthetic play, labelled live by our own decoder.

Every position below is invented here (no match data). The ribbon, the "decoded label" badge and
the "evidence this frame" panel are not drawn by hand: the scene is serialised as a
possession.inputs.Tracking and run through possession.decoder with the submitted profile, and the
graphic shows exactly what comes back.

    python tools/hero/make_hero.py              # assets/hero/hero.svg
    python tools/hero/make_hero.py --raster     # + hero.gif, hero.webp, hero-poster.png

--raster screenshots the SVG frame by frame in a headless Chromium browser (Edge or Chrome,
SMIL paused with setCurrentTime), so the GIF is the SVG, not a second drawing of it.
Deterministic: fixed seed, fixed choreography, no clock or randomness at render time.
"""

import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_DIR = os.path.join(ROOT, "assets", "hero")
sys.path.insert(0, ROOT)


def _import_possession(attempts=5):
    # Retry the import: a file of the package may be half-written while it is being saved.
    for i in range(attempts):
        try:
            from possession import decoder
            from possession.inputs import AWAY, HOME, Tracking
            from possession.params import load_profile
            return decoder, HOME, AWAY, Tracking, load_profile
        except (ImportError, SyntaxError, AttributeError):
            if i == attempts - 1:
                raise
            time.sleep(3)


decoder, HOME, AWAY, Tracking, load_profile = _import_possession()

PROFILE = "macro"           # the submitted profile (TECHNICAL.md section 7)
FPS = 25
LOOP_S = 14.0
N = int(LOOP_S * FPS)
DUR = "{:g}s".format(LOOP_S)
L, W = 105.0, 68.0          # pitch, metres
TIME = np.arange(N) / FPS
SEED = 2027

# -- canvas -----------------------------------------------------------------------------------------
CW, CH = 1280, 800
S = 8.4                     # px per metre
PX, PY = 40.0, 134.0        # pitch origin (top-left corner flag)
PANEL_X = PX + L * S + 28
PANEL_W = CW - 40 - PANEL_X
RIB_X0, RIB_X1 = 132.0, CW - 40.0

INK = "#0A0A0C"
LIME = "#C4F000"
BLUE, GARNET, VIOLET = "#004D98", "#A50044", "#6E4C9F"
BLUE_HI, GARNET_HI = "#3D8BFD", "#E0277A"   # same hues, lifted for thin strokes on black
RED, WHITE = "#E3242B", "#F4F4F2"
MUTED, SOFT = "#8A9099", "#C9CED6"
SANS = "'Inter','Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Mono',Consolas,'Roboto Mono',monospace"


def X(x):
    return PX + x * S


def Y(y):
    return PY + y * S


def frame(t):
    return int(round(t * FPS)) % N


# -- periodic maths ---------------------------------------------------------------------------------

def path(waypoints):
    """(N, 2) positions through (t, x, y) waypoints, cubic Hermite with finite-difference tangents,
    wrapping at LOOP_S so the loop is seamless. A repeated point is a hold (zero tangent)."""
    pts = sorted(waypoints)
    tk = np.array([p[0] for p in pts], dtype=float)
    pk = np.array([p[1:] for p in pts], dtype=float)
    te = np.concatenate([tk[-2:] - LOOP_S, tk, tk[:2] + LOOP_S])
    pe = np.concatenate([pk[-2:], pk, pk[:2]])
    tan = np.zeros_like(pe)
    for j in range(1, len(pe) - 1):
        if np.allclose(pe[j], pe[j - 1]) or np.allclose(pe[j], pe[j + 1]):
            continue
        tan[j] = (pe[j + 1] - pe[j - 1]) / (te[j + 1] - te[j - 1])
    out = np.empty((N, 2))
    for i, tt in enumerate(TIME):
        j = int(np.searchsorted(te, tt, side="right")) - 1
        h = te[j + 1] - te[j]
        s = (tt - te[j]) / h
        h00, h10 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s
        h01, h11 = -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
        out[i] = h00 * pe[j] + h10 * h * tan[j] + h01 * pe[j + 1] + h11 * h * tan[j + 1]
    return out


def psmooth(a, sigma):
    """Periodic Gaussian smoothing along axis 0 (sigma in frames)."""
    r = int(3 * sigma)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    a = np.asarray(a, dtype=float)
    padded = np.concatenate([a[-r:], a, a[:r]])
    if a.ndim == 1:
        return np.convolve(padded, k, mode="valid")
    return np.stack([np.convolve(padded[:, c], k, mode="valid") for c in range(a.shape[1])], 1)


def pvel(p):
    """Periodic central-difference velocity, units per second."""
    return (np.roll(p, -1, axis=0) - np.roll(p, 1, axis=0)) * FPS / 2.0


def window(t0, t1):
    """Boolean per frame, half-open [t0, t1) seconds, wrapping if t1 < t0."""
    if t0 <= t1:
        return (TIME >= t0) & (TIME < t1)
    return (TIME >= t0) | (TIME < t1)


# -- choreography -----------------------------------------------------------------------------------
# Home attacks left to right. Slots 0-10 home (0 = GK), 11-21 away (11 = GK).
HOME_SHAPE = [(5, 34), (36, 58), (28, 44), (28, 24), (36, 10), (40, 34),
              (50, 44), (48, 22), (64, 58), (68, 34), (64, 12)]
AWAY_SHAPE = [(100, 34), (76, 10), (84, 26), (84, 42), (76, 58), (70, 38),
              (66, 46), (68, 24), (56, 14), (58, 34), (56, 54)]

THROWER, H_RCM, H_LCM, H_ST = 4, 6, 7, 9
A_CM1, A_CM2, A_WING = 16, 17, 19

# Story beats, seconds. The loop starts as the throw-in leaves the thrower's hands.
T_RECEIVE = 0.64            # throw-in reaches the left midfielder
T_PASS1, T_RECV1 = 2.4, 3.36
T_TOUCH = 3.92              # an opponent's foot gets to the ball for a moment
TOUCH_REACH = (0.25, 0.35)   # metres from the ball at that instant
T_PASS2, T_INTERCEPT = 4.6, 5.0
T_GAP0, T_GAP1 = 6.6, 8.4   # ball not tracked
T_LONG, T_REST = 8.8, 10.4  # long ball, overhit, out over the touchline
T_PICK, T_SET = 11.4, 12.6  # thrower picks the ball up, then stands at the line

ACTORS = {
    THROWER: [(0.0, 45.0, -1.2), (0.7, 45.5, 1.8), (1.8, 46.0, 6.0), (3.5, 48.0, 9.0),
              (5.5, 46.0, 10.0), (7.5, 43.0, 9.0), (9.3, 42.5, 6.5), (10.4, 41.6, 1.0),
              (11.3, 40.8, -2.9), (11.6, 40.8, -2.9), (12.6, 45.0, -1.2), (13.4, 45.0, -1.2)],
    H_LCM: [(0.0, 43.6, 8.0), (T_RECEIVE, 44.3, 9.2), (1.5, 47.5, 12.5), (T_PASS1, 51.0, 16.0),
            (3.4, 53.5, 17.5), (5.0, 55.0, 19.0), (6.5, 51.0, 21.0), (8.5, 47.0, 20.0),
            (10.0, 45.0, 15.0), (12.0, 44.0, 10.0), (13.3, 43.6, 8.3)],
    H_RCM: [(0.0, 50.0, 44.0), (1.5, 52.0, 42.5), (T_RECV1, 54.0, 40.0), (4.0, 56.8, 40.2),
            (T_PASS2, 59.5, 40.5), (5.4, 61.5, 41.5), (6.8, 57.0, 43.0), (8.5, 52.0, 44.0),
            (10.5, 51.5, 41.0), (12.5, 51.0, 42.0)],
    H_ST: [(0.0, 70.0, 32.0), (2.5, 69.0, 31.0), (T_PASS2, 71.5, 33.5), (5.2, 72.3, 34.2),
           (6.5, 70.0, 35.0), (9.0, 66.0, 34.0), (12.0, 68.0, 33.0)],
    A_CM1: [(0.0, 55.0, 30.0), (2.0, 60.0, 33.5), (T_PASS2, 69.2, 37.8),
            (T_INTERCEPT, 67.95, 36.84), (5.8, 65.8, 35.2), (T_GAP0, 62.8, 33.6),
            (7.5, 59.0, 31.5), (T_GAP1, 55.0, 29.5), (T_LONG, 53.5, 28.8), (9.6, 52.5, 28.5),
            (11.5, 53.5, 29.0), (13.0, 54.2, 29.5)],
    A_CM2: [(0.0, 62.0, 47.0), (2.0, 63.5, 45.5), (3.3, 60.6, 42.6), (T_TOUCH, 58.15, 40.62),
            (4.5, 60.6, 42.4), (6.0, 63.0, 44.0), (8.5, 58.0, 45.0), (11.0, 57.0, 46.0),
            (13.0, 60.0, 47.0)],
    A_WING: [(0.0, 49.5, 5.0), (3.0, 53.0, 12.0), (6.0, 54.0, 13.0), (T_LONG, 48.0, 9.0),
             (9.9, 42.5, 4.5), (11.0, 43.0, 3.8), (12.6, 48.5, 4.8)],
}

# Ball script: holds (carrier, offset rule) and free positions; the gaps between them are flights.
#   ("hold", t0, t1, slot, offset)   offset: metres ahead of the carrier, or (dx, dy) fixed
#   ("rest", t0, t1, (x, y))
BALL_SCRIPT = [
    ("hold", T_RECEIVE, T_PASS1, H_LCM, 0.6),
    ("hold", T_RECV1, T_PASS2, H_RCM, 0.6),
    ("hold", T_INTERCEPT, T_LONG, A_CM1, 0.6),
    ("rest", T_REST, T_PICK, (40.6, -3.0)),
    ("hold", T_PICK + 0.12, LOOP_S, THROWER, (0.0, -0.4)),
]
LOFTED = {T_LONG: 1.0, 0.0: 0.35}    # flight start -> loft (draws a larger ball mid-flight)


def build_scene():
    rng = np.random.default_rng(SEED)
    n_slots = 22
    pos = np.zeros((N, n_slots, 2))
    for slot, wps in ACTORS.items():
        pos[:, slot] = path(wps)
    # the touch: the challenger's foot reaches the ball just ahead of the carrier, for a moment
    v = pvel(pos[:, H_RCM])[frame(T_TOUCH)]
    contact = pos[frame(T_TOUCH), H_RCM] + 0.6 * v / np.linalg.norm(v) + TOUCH_REACH
    pos[:, A_CM2] = path([w if w[0] != T_TOUCH else (T_TOUCH,) + tuple(contact) for w in ACTORS[A_CM2]])

    # ball: holds and rests first, flights fill the gaps between them
    ball = np.full((N, 2), np.nan)
    owner = np.full(N, -1)
    for item in BALL_SCRIPT:
        kind, t0, t1 = item[:3]
        idx = np.flatnonzero(window(t0, t1))
        if kind == "rest":
            ball[idx] = item[3]
            continue
        slot, offset = item[3], item[4]
        carrier = pos[:, slot]
        if isinstance(offset, tuple):
            ball[idx] = carrier[idx] + np.array(offset)
        else:
            v = pvel(carrier)
            heading = v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-6)
            ball[idx] = carrier[idx] + offset * heading[idx]
        owner[idx] = slot
    lift = np.zeros(N)
    free = np.isnan(ball[:, 0])
    starts = np.flatnonzero(free & ~np.roll(free, 1))
    for f0 in starts:
        length = 0
        while free[(f0 + length) % N]:
            length += 1
        a, b = ball[(f0 - 1) % N], ball[(f0 + length) % N]
        s = np.arange(1, length + 1) / (length + 1.0)
        loft = LOFTED.get(round(f0 / FPS, 2), 0.0)
        ease = 1 - (1 - s) ** (2.2 if loft >= 1 else 1.15)   # long ball dies as it rolls out
        for k in range(length):
            ball[(f0 + k) % N] = a + ease[k] * (b - a)
            lift[(f0 + k) % N] = loft * min(1.0, 4 * s[k] * (1 - s[k]) * 1.6) if loft else 0.0

    # Team shape (for the 18 players without a script): the block slides with the ball and
    # leans towards the attacking team's direction; everyone jogs in play and ambles when the
    # ball is dead, so the decoder's stillness evidence has something real to find.
    def keyed(keys):
        tk, vk = zip(*keys)
        return np.interp(TIME, tk, vk, period=LOOP_S)

    t_dead = 9.9
    lean = psmooth(keyed([(0.0, -0.6), (1.6, 1.0), (4.9, 1.0), (5.7, -1.0), (t_dead, -1.0), (12.0, -0.6)]), 0.25 * FPS)
    env = keyed([(0.0, 0.05), (0.9, 1.0), (t_dead, 1.0), (10.8, 0.06), (13.99, 0.05)])
    shape_ball = ball.copy()
    shape_ball[window(t_dead, LOOP_S)] = (44.0, 4.0)
    track = psmooth(shape_ball, 0.9 * FPS)

    for slot in range(n_slots):
        if slot in ACTORS:
            continue
        home = slot < 11
        bx, by = (HOME_SHAPE[slot] if home else AWAY_SHAPE[slot - 11])
        keeper = slot in (0, 11)
        kx, ky = (0.12, 0.08) if keeper else (0.45, 0.30)
        x = bx + kx * (track[:, 0] - 52.5) + (1.0 if keeper else 3.5) * lean
        y = by + ky * (track[:, 1] - 34.0)
        amp = rng.uniform(0.9, 1.7, 2) * (0.4 if keeper else 1.0)
        cyc = rng.integers(2, 5, 2)
        ph = rng.uniform(0, 2 * np.pi, 2)
        x = x + env * amp[0] * np.sin(2 * np.pi * cyc[0] * TIME / LOOP_S + ph[0])
        y = y + env * amp[1] * np.sin(2 * np.pi * cyc[1] * TIME / LOOP_S + ph[1])
        pos[:, slot, 0] = np.clip(x, 1.0, L - 1.0)
        pos[:, slot, 1] = np.clip(y, 1.5, W - 1.5)

    speed = np.linalg.norm(pvel(pos), axis=2)
    seen = ~window(T_GAP0, T_GAP1)
    team = np.array([HOME] * 11 + [AWAY] * 11, dtype=np.int8)
    return {"pos": pos, "speed": speed, "ball": ball, "seen": seen, "lift": lift,
            "team": team, "owner": owner}


# -- decoding (our code, unchanged) ---------------------------------------------------------------

def decode(scene, profile=PROFILE):
    """Labels, per-frame evidence and features for one loop. The decoder sees three back-to-back
    copies and the middle one is kept, so the loop seam is decoded like any other frame."""
    p = load_profile(profile)
    reps = 3
    bx = np.where(scene["seen"], scene["ball"][:, 0], np.nan)
    by = np.where(scene["seen"], scene["ball"][:, 1], np.nan)
    trk = Tracking(np.tile(scene["pos"][:, :, 0], (reps, 1)).astype(np.float32),
                   np.tile(scene["pos"][:, :, 1], (reps, 1)).astype(np.float32),
                   np.tile(scene["speed"], (reps, 1)).astype(np.float32),
                   np.tile(bx, reps).astype(np.float32), np.tile(by, reps).astype(np.float32),
                   scene["team"].copy(), ("Home", "Away"), (L, W))
    # A tagged SET PIECES window brackets the throw-in, as Smart Tagging would.
    set_pieces = [(k * N - int(2.5 * FPS), k * N + int(2.5 * FPS)) for k in range(1, reps + 1)]
    set_pieces = [(max(0, a), min(reps * N, b)) for a, b in set_pieces]
    labels = decoder.decode(trk, [(0, reps * N - 1)], (), set_pieces, p)
    feats = decoder.features(trk, p)
    try:
        scores = decoder.evidence(trk, set_pieces, p, feats=feats)
    except (AttributeError, TypeError):   # no usable decoder.evidence: rebuild it from features
        scores = np.zeros((reps * N, 3))
        ctrl = np.where(feats["fast"], p.w_control_fast, p.w_control)
        scores[:, 0] = np.where(feats["near_home"], ctrl, 0)
        scores[:, 1] = np.where(feats["near_away"], ctrl, 0)
        scores[:, 2] = (p.w_oob * feats["oob"] + p.w_still * feats["still"]
                        + p.w_ball_stationary * feats["stationary"] - p.w_alive * feats["moving"])
    mid = slice(N, 2 * N)
    restart = np.zeros(reps * N, dtype=bool)
    for a, b in set_pieces:
        restart[a:a + int(round(p.setpiece_dead_fraction * (b - a)))] = True
    f = {k: np.asarray(v)[mid] for k, v in feats.items()}
    f["restart"] = restart[mid]
    return np.asarray(labels)[mid], scores[mid], f, p


# -- svg helpers ------------------------------------------------------------------------------------

def num(v):
    s = "{:.1f}".format(v)
    return s[:-2] if s.endswith(".0") else s


def translate_anim(xy):
    xy = np.vstack([xy, xy[:1]])
    vals = ";".join("{} {}".format(num(x), num(y)) for x, y in xy)
    return ('<animateTransform attributeName="transform" type="translate" dur="{}" '
            'repeatCount="indefinite" values="{}"/>'.format(DUR, vals))


def linear_anim(attr, series, digits=2):
    """Piecewise-linear animation of `attr` sampled per frame; collinear samples are dropped."""
    v = np.round(np.append(series, series[0]).astype(float), digits)
    keep = [0]
    for i in range(1, len(v) - 1):
        if abs(v[i - 1] - 2 * v[i] + v[i + 1]) > 10 ** -digits / 2:
            keep.append(i)
    keep.append(len(v) - 1)
    fmt = "{:.%df}" % digits
    vals = ";".join(fmt.format(v[i]).rstrip("0").rstrip(".") or "0" for i in keep)
    kts = ";".join("{:.5f}".format(i / N).rstrip("0").rstrip(".") or "0" for i in keep)
    return ('<animate attributeName="{}" dur="{}" repeatCount="indefinite" values="{}" '
            'keyTimes="{}"/>'.format(attr, DUR, vals, kts))


def soft(mask, ramp=4):
    """Boolean per frame -> opacity with linear ramps of `ramp` frames (periodic)."""
    m = mask.astype(float)
    if ramp <= 1:
        return m
    k = np.ones(ramp) / ramp
    padded = np.concatenate([m[-ramp:], m, m[:ramp]])
    return np.convolve(padded, k, mode="same")[ramp:-ramp]


def fade(mask, ramp=6):
    return linear_anim("opacity", soft(mask, ramp))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chip(x, y, text, mask, accent=LIME, anchor="start"):
    """On-pitch telestration label, faded in over the frames where `mask` is true."""
    w = 7.9 * len(text) + 20
    x0 = x if anchor == "start" else x - w
    return ('<g opacity="0">{a}<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" '
            'fill="{ink}" fill-opacity=".86" stroke="{c}" stroke-width="1.2"/>'
            '<text x="{tx}" y="{ty}" class="chip">{t}</text></g>').format(
        a=fade(mask, 7), x=num(x0), y=num(y - 13), w=num(w), ink=INK, c=accent,
        tx=num(x0 + 10), ty=num(y + 5), t=esc(text))


# -- the SVG ----------------------------------------------------------------------------------------

def defs():
    stripes_home = "".join(
        '<stop offset="{a}" stop-color="{c}"/><stop offset="{b}" stop-color="{c}"/>'.format(
            a=i / 5, b=(i + 1) / 5, c=BLUE if i % 2 == 0 else GARNET) for i in range(5))
    stripes_away = "".join(
        '<stop offset="{a}" stop-color="{c}"/><stop offset="{b}" stop-color="{c}"/>'.format(
            a=i / 5, b=(i + 1) / 5, c=RED if i % 2 == 0 else WHITE) for i in range(5))
    return """<defs>
<linearGradient id="kitH" x1="0" x2="1" y1="0" y2="0">{sh}</linearGradient>
<linearGradient id="kitA" x1="0" x2="1" y1="0" y2="0">{sa}</linearGradient>
<pattern id="ribH" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
<rect width="10" height="10" fill="{blue}"/><rect width="5" height="10" fill="{garnet}"/></pattern>
<pattern id="ribA" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
<rect width="10" height="10" fill="{red}"/><rect width="4" height="10" fill="{white}"/></pattern>
<linearGradient id="badgeH" x1="0" x2="1"><stop offset="0" stop-color="{blue}"/><stop offset="1" stop-color="{garnet}"/></linearGradient>
<radialGradient id="vignette" cx=".5" cy=".5" r=".72"><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<pattern id="ribD" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)">
<rect width="8" height="8" fill="#1E2124"/><rect width="1.6" height="8" fill="{lime}" fill-opacity=".45"/></pattern>
<pattern id="ribQ" width="6" height="10" patternUnits="userSpaceOnUse"><circle cx="3" cy="5" r="1.1" fill="#8A9099"/></pattern>
<linearGradient id="edgeH" x1="0" x2="1"><stop offset="0" stop-color="{bluehi}"/><stop offset="1" stop-color="{garnethi}"/></linearGradient>
<radialGradient id="spot"><stop offset="0" stop-color="#E8FFD0" stop-opacity=".13"/><stop offset="1" stop-color="#E8FFD0" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="bg" cx=".35" cy=".1" r="1"><stop offset="0" stop-color="#15171C"/><stop offset="1" stop-color="{ink}"/></radialGradient>
<clipPath id="reveal"><rect x="{rx}" y="720" width="0" height="60">{rev}</rect></clipPath>
</defs>""".format(sh=stripes_home, sa=stripes_away, lime=LIME, bluehi=BLUE_HI, garnethi=GARNET_HI, blue=BLUE, garnet=GARNET, red=RED, white=WHITE,
                  ink=INK,
                  rx=num(RIB_X0),
                  rev='<animate attributeName="width" dur="{}" repeatCount="indefinite" '
                      'values="0;{}" keyTimes="0;1"/>'.format(DUR, num(RIB_X1 - RIB_X0)))


STYLE = """<style>
text{{font-family:{sans};fill:{soft}}}
.title{{font-size:30px;font-weight:700;fill:#F2F4F7;letter-spacing:-.3px}}
.title .dim{{font-weight:400;fill:{muted}}}
.kicker{{font-size:13px;letter-spacing:1.6px;fill:{muted}}}
.label{{font-size:12px;letter-spacing:1.8px;fill:{muted};font-weight:600}}
.row{{font-size:15px}}
.w{{font-family:{mono};font-size:13px;fill:#7D848E}}
.chip{{font-size:14px;font-weight:600;fill:#F2F4F7}}
.step{{font-family:{mono};font-size:34px;font-weight:700;fill:{lime}}}
.of{{font-family:{mono};font-size:13px;fill:{muted}}}
.cap{{font-size:18px;font-weight:700;fill:#F2F4F7}}
.body{{font-size:15.5px;fill:{soft}}}
.tick{{font-family:{mono};font-size:12.5px;fill:#6F7680}}
.lane{{font-size:13.5px;fill:{muted}}}
.badge{{font-size:23px;font-weight:800;letter-spacing:1.5px;fill:#fff}}
.badgeL{{font-family:{mono};font-size:30px;font-weight:700}}
.foot{{font-family:{mono};font-size:12px;fill:#6F7680}}
</style>""".format(sans=SANS, mono=MONO, soft=SOFT, muted=MUTED, lime=LIME)


def pitch_markings():
    ln = 'stroke="#E9EFE9" stroke-opacity=".5" stroke-width="1.5" fill="none"'
    out = []
    # mown stripes
    band = L / 14
    for i in range(14):
        out.append('<rect x="{}" y="{}" width="{}" height="{}" fill="{}"/>'.format(
            num(X(i * band)), num(Y(0)), num(band * S + 0.5), num(W * S),
            "#101B15" if i % 2 == 0 else "#0D1712"))
    out.append('<g {}>'.format(ln))
    out.append('<rect x="{}" y="{}" width="{}" height="{}"/>'.format(num(X(0)), num(Y(0)), num(L * S), num(W * S)))
    out.append('<line x1="{x}" y1="{a}" x2="{x}" y2="{b}"/>'.format(x=num(X(L / 2)), a=num(Y(0)), b=num(Y(W))))
    out.append('<circle cx="{}" cy="{}" r="{}"/>'.format(num(X(L / 2)), num(Y(W / 2)), num(9.15 * S)))
    for side in (0, 1):
        def sx(x):
            return X(x if side == 0 else L - x)
        pa_x = min(sx(0), sx(16.5))
        out.append('<rect x="{}" y="{}" width="{}" height="{}"/>'.format(
            num(pa_x), num(Y(W / 2 - 20.16)), num(16.5 * S), num(40.32 * S)))
        ga_x = min(sx(0), sx(5.5))
        out.append('<rect x="{}" y="{}" width="{}" height="{}"/>'.format(
            num(ga_x), num(Y(W / 2 - 9.16)), num(5.5 * S), num(18.32 * S)))
        g_x = min(sx(0), sx(-1.8))
        out.append('<rect x="{}" y="{}" width="{}" height="{}" stroke-opacity=".35"/>'.format(
            num(g_x), num(Y(W / 2 - 3.66)), num(1.8 * S), num(7.32 * S)))
        dy = math.sqrt(9.15 ** 2 - 5.5 ** 2)
        out.append('<path d="M{} {} A{r} {r} 0 0 {sw} {} {}"/>'.format(
            num(sx(16.5)), num(Y(W / 2 - dy)), num(sx(16.5)), num(Y(W / 2 + dy)),
            r=num(9.15 * S), sw=1 if side == 0 else 0))
        out.append('<circle cx="{}" cy="{}" r="1.8" fill="#E9EFE9" fill-opacity=".5" stroke="none"/>'.format(
            num(sx(11)), num(Y(W / 2))))
    out.append('<circle cx="{}" cy="{}" r="1.8" fill="#E9EFE9" fill-opacity=".5" stroke="none"/>'.format(
        num(X(L / 2)), num(Y(W / 2))))
    for cx, cy, a0 in ((0, 0, 0), (L, 0, 90), (L, W, 180), (0, W, 270)):
        r = 1.0 * S
        p0 = (X(cx) + r * math.cos(math.radians(a0)), Y(cy) + r * math.sin(math.radians(a0)))
        p1 = (X(cx) + r * math.cos(math.radians(a0 + 90)), Y(cy) + r * math.sin(math.radians(a0 + 90)))
        out.append('<path d="M{} {} A{r} {r} 0 0 1 {} {}"/>'.format(num(p0[0]), num(p0[1]), num(p1[0]), num(p1[1]), r=num(r)))
    out.append('</g>')
    return "\n".join(out)


def ribbon(labels, lane):
    """Decoded lane (the answer) and per-frame lane (what each frame says on its own)."""
    fill = {"H": "url(#ribH)", "A": "url(#ribA)", "D": "url(#ribD)", "?": "url(#ribQ)"}
    span = (RIB_X1 - RIB_X0) / N
    out = []

    def runs(seq):
        i = 0
        while i < N:
            j = i
            while j < N and seq[j] == seq[i]:
                j += 1
            yield seq[i], i, j
            i = j

    for lab, i, j in runs(list(lane)):
        if lab == "-":
            continue
        out.append('<rect x="{}" y="730" width="{}" height="10" fill="{}"/>'.format(
            num(RIB_X0 + i * span), num((j - i) * span + 0.3), fill[lab]))
    for lab, i, j in runs(list(labels)):
        extra = ' stroke="{}" stroke-width="1.5"'.format(LIME) if lab == "D" else ""
        if lab == "D":
            out.append('<rect x="{}" y="747" width="{}" height="24" fill="url(#ribD)"/>'.format(
                num(RIB_X0 + i * span), num((j - i) * span)))
        out.append('<rect x="{}" y="747" width="{}" height="24" fill="{}"{}/>'.format(
            num(RIB_X0 + i * span + (0.75 if lab == "D" else 0)), num((j - i) * span - (1.5 if lab == "D" else -0.3)),
            "none" if lab == "D" else fill[lab], extra))
        if j - i > 25:
            out.append('<text x="{}" y="764" text-anchor="middle" style="font-family:{};font-size:12px;'
                       'font-weight:700;fill:{}">{}</text>'.format(
                           num(RIB_X0 + (i + j) / 2 * span), MONO, LIME if lab == "D" else "#fff", lab))
    return "\n".join(out)


def build_svg(scene, labels, scores, f, p):
    pos, ball, seen, lift = scene["pos"], scene["ball"], scene["seen"], scene["lift"]
    px = lambda a: np.stack([X(a[..., 0]), Y(a[..., 1])], -1)  # noqa: E731
    o = []
    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
             'role="img" aria-labelledby="hero-title hero-desc">'.format(w=CW, h=CH))
    o.append('<title id="hero-title">Who has the ball? Possession decoded frame by frame</title>')
    o.append('<desc id="hero-desc">A synthetic eleven-a-side play: control within 1.5 m, a touch that does '
             'not change possession, an interception that does, the ball lost by the tracker while '
             'possession is held, the ball going out for a dead ball, and the throw-in restart. The '
             'timeline is the output of possession.decoder on this play.</desc>')
    o.append(STYLE)
    o.append(defs())
    o.append('<rect width="{}" height="{}" fill="url(#bg)"/>'.format(CW, CH))

    # header
    o.append('<text x="40" y="54" class="title">Who has the ball?<tspan class="dim"> — decoded frame by frame</tspan></text>')
    o.append('<text x="40" y="82" class="kicker">SYNTHETIC PLAY · 25 FPS · LABELS COMPUTED BY possession.decoder · PROFILE {}</text>'.format(PROFILE.upper()))
    lx = CW - 40
    for label, swatch in (("DEAD BALL", "d"), ("AWAY", "a"), ("HOME", "h")):
        tw = 7.6 * len(label)
        o.append('<text x="{}" y="54" style="font-size:12px;font-weight:600;letter-spacing:1.4px;fill:{}">{}</text>'.format(
            num(lx - tw), SOFT, label))
        cx = lx - tw - 14
        if swatch == "h":
            o.append('<circle cx="{}" cy="50" r="7" fill="url(#kitH)" stroke="#fff" stroke-opacity=".8" stroke-width="1.2"/>'.format(num(cx)))
        elif swatch == "a":
            o.append('<circle cx="{}" cy="50" r="7" fill="url(#kitA)" stroke="{}" stroke-width="1.8"/>'.format(num(cx), INK))
        else:
            o.append('<rect x="{}" y="43" width="14" height="14" rx="3" fill="#24272B" stroke="{}" stroke-width="1.5"/>'.format(num(cx - 7), LIME))
        lx = cx - 24

    # pitch
    o.append('<g>')
    o.append(pitch_markings())
    dead = labels == "D"
    edge = '<rect x="{}" y="{}" width="{}" height="{}" rx="3" fill="none" '.format(
        num(X(0) - 5), num(Y(0) - 5), num(L * S + 10), num(W * S + 10))
    o.append('<g opacity="0">{}{}stroke="url(#edgeH)" stroke-width="3"/></g>'.format(fade(labels == "H", 8), edge))
    o.append('<g opacity="0">{}{}stroke="{}" stroke-width="3"/>{}stroke="#fff" stroke-width="3" stroke-dasharray="10 10"/></g>'.format(
        fade(labels == "A", 8), edge, RED, edge))
    o.append('<g opacity="0">{}{}stroke="{}" stroke-width="3"/></g>'.format(fade(dead, 8), edge, LIME))
    o.append('<rect x="{}" y="{}" width="{}" height="{}" fill="#000">{}</rect>'.format(
        num(X(0)), num(Y(0)), num(L * S), num(W * S), linear_anim("opacity", 0.25 * soft(dead, 10))))
    track = psmooth(np.where(np.isnan(ball), 52.5, ball), 0.5 * FPS)
    o.append('<g><circle r="190" fill="url(#spot)"/>{}</g>'.format(translate_anim(px(track))))
    o.append('<rect x="{}" y="{}" width="{}" height="{}" fill="url(#vignette)"/>'.format(
        num(X(0)), num(Y(0)), num(L * S), num(W * S)))

    # out-of-play flash on the touchline where the ball crosses
    f_out = int(np.flatnonzero(f["oob"])[0]) if f["oob"].any() else frame(T_REST)
    cross_x = float(ball[f_out, 0])
    out_mask = window(f_out / FPS, f_out / FPS + 2.4)
    o.append('<line x1="{}" y1="{y}" x2="{}" y2="{y}" stroke="{}" stroke-width="4" stroke-linecap="round" opacity="0">{}</line>'.format(
        num(X(cross_x - 7)), num(X(cross_x + 7)), LIME, fade(out_mask, 5), y=num(Y(0))))

    # pass trails drawn on during each flight
    def flight_line(t0, t1, dashed_to=None, color=LIME):
        a, b = px(ball[frame(t0) - 1]), px(ball[frame(t1)])
        length = float(np.hypot(*(b - a)))
        k = np.zeros(N)
        f0, f1 = frame(t0), frame(t1)
        k[f0:f1] = np.linspace(0, 1, f1 - f0)
        k[f1:f1 + 15] = 1
        offs = length * (1 - k)
        vis = window(t0, t1 + 0.6)
        g = ['<g opacity="0">{}'.format(fade(vis, 8))]
        if dashed_to is not None:
            c = px(np.array(dashed_to))
            g.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#fff" stroke-opacity=".45" stroke-width="1.4" stroke-dasharray="4 5"/>'.format(
                num(a[0]), num(a[1]), num(c[0]), num(c[1])))
        g.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="2.2" stroke-linecap="round" '
                 'stroke-dasharray="{L} {L}" stroke-dashoffset="{L}">{}</line></g>'.format(
                     num(a[0]), num(a[1]), num(b[0]), num(b[1]), color,
                     linear_anim("stroke-dashoffset", offs, 1), L=num(length)))
        return "".join(g)

    o.append(flight_line(T_PASS1, T_RECV1))
    o.append(flight_line(T_PASS2, T_INTERCEPT, dashed_to=pos[frame(5.2), H_ST]))
    o.append(flight_line(T_LONG, T_REST, color="#FFFFFF"))

    # interception burst
    ip = px(ball[frame(T_INTERCEPT)])
    burst_r = np.zeros(N)
    burst_o = np.zeros(N)
    f0 = frame(T_INTERCEPT)
    for k in range(20):
        burst_r[f0 + k] = 6 + 2.2 * k
        burst_o[f0 + k] = 1 - k / 20
    o.append('<circle cx="{}" cy="{}" r="6" fill="none" stroke="{}" stroke-width="2.5" opacity="0">{}{}</circle>'.format(
        num(ip[0]), num(ip[1]), RED, linear_anim("r", burst_r, 1), linear_anim("opacity", burst_o)))

    # control rings: 1.5 m around the nearest player of the team the decoder's features credit
    d = np.linalg.norm(pos - ball[:, None, :], axis=2)
    pulses = 16  # per loop, so the pulse is seamless too
    for team_id, key, colors in ((HOME, "near_home", (BLUE_HI, GARNET_HI)), (AWAY, "near_away", (RED, WHITE))):
        slots = np.flatnonzero(scene["team"] == team_id)
        who = slots[np.argmin(d[:, slots], axis=1)]
        active = f[key]
        anchor = pos[np.arange(N), who]
        held = anchor.copy()
        for i in range(N):   # keep the ring on its last controller while hidden
            if not active[i]:
                held[i] = held[i - 1] if i else anchor[np.flatnonzero(active)[-1]]
        r = 1.5 * S
        circ = 2 * math.pi * r
        ring = ['<g opacity="0">{}{}'.format(fade(active, 3), translate_anim(px(held)))]
        ring.append('<circle r="{}" fill="{}" fill-opacity=".10"/>'.format(num(r), colors[0]))
        ring.append('<circle r="{r}" fill="none" stroke="{c}" stroke-width="2.6"/>'.format(r=num(r), c=colors[0]))
        ring.append('<circle r="{r}" fill="none" stroke="{c}" stroke-width="2.6" stroke-dasharray="{h} {h}" '
                    'transform="rotate(-90)"/>'.format(r=num(r), c=colors[1], h=num(circ / 8)))
        ring.append('<circle r="{r}" fill="none" stroke="{c}" stroke-width="1.6">'
                    '<animate attributeName="r" values="{r};{r2}" dur="{d}s" repeatCount="indefinite"/>'
                    '<animate attributeName="opacity" values=".8;0" dur="{d}s" repeatCount="indefinite"/></circle>'.format(
                        r=num(r), r2=num(r * 2.2), c=colors[0], d="{:g}".format(LOOP_S / pulses)))
        if team_id == HOME:   # dimension the radius during the first beat
            dim = window(T_RECEIVE + 0.1, T_PASS1)
            ring.append('<g opacity="0">{}<line x1="0" y1="0" x2="{r}" y2="0" stroke="{lime}" stroke-width="1.4"/>'
                        '<circle r="2" fill="{lime}"/><text x="{tx}" y="-6" style="font-family:{mono};font-size:12px;'
                        'font-weight:700;fill:{lime}">1.5 m</text></g>'.format(
                            fade(dim, 6), r=num(r), lime=LIME, tx=num(r + 4), mono=MONO))
        ring.append('</g>')
        o.append("".join(ring))

    # motion streaks: the same paths a few frames late, faint, so speed reads at a glance
    o.append('<g>')
    for lag, r, op in ((6, 4.2, 0.10), (3, 5.6, 0.18)):
        for slot in range(22):
            color = BLUE_HI if scene["team"][slot] == HOME else RED
            o.append('<g>{}<circle r="{}" fill="{}" fill-opacity="{}"/></g>'.format(
                translate_anim(px(np.roll(pos[:, slot], lag, axis=0))), r, color, op))
    o.append('</g>')

    # players: shadow, kit, trim
    o.append('<g>')
    for slot in range(22):
        home = scene["team"][slot] == HOME
        keeper = slot in (0, 11)
        if keeper:
            fill, stroke, sw = ("#F2C230", INK, 1.6) if home else ("#1FA37A", INK, 1.6)
        else:
            fill, stroke, sw = ("url(#kitH)", "#F4F4F2", 1.3) if home else ("url(#kitA)", INK, 2.0)
        halo = '' if home else '<circle r="9.6" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1"/>'
        o.append('<g>{}<circle cx="1.6" cy="2.4" r="8" fill="#000" fill-opacity=".45"/>{}'
                 '<circle r="7.6" fill="{}" stroke="{}" stroke-width="{}"/></g>'.format(
                     translate_anim(px(pos[:, slot])), halo, fill, stroke, sw))
    o.append('</g>')

    # ghost ball while the tracker has lost it
    gap = ~seen
    o.append('<g opacity="0">{}{}<circle r="6" fill="none" stroke="#fff" stroke-width="1.5" stroke-dasharray="3 3"/>'
             '<text y="-11" text-anchor="middle" style="font-family:{};font-size:13px;font-weight:700;fill:#fff">?</text></g>'.format(
                 fade(gap, 3), translate_anim(px(ball)), MONO))
    # ghosted dashed trail through the gap
    g0, g1 = frame(T_GAP0), frame(T_GAP1)
    pts = " ".join("{},{}".format(num(a), num(b)) for a, b in px(ball[g0:g1 + 1:3]))
    o.append('<polyline points="{}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="1.4" '
             'stroke-dasharray="2 5" opacity="0">{}</polyline>'.format(pts, fade(window(T_GAP0, T_GAP1 + 0.8), 6)))

    # ball: glow, comet trail, ball (radius follows loft)
    vis = linear_anim("opacity", soft(seen, 2))
    trail = []
    for k in range(10, 0, -1):
        rolled = np.roll(ball, k, axis=0)
        r = 4.6 * (1 - k / 12.5)
        trail.append('<g>{}<circle r="{}" fill="{}" fill-opacity="{:.2f}"/></g>'.format(
            translate_anim(px(rolled)), num(r), LIME, 0.5 * (1 - k / 11)))
    o.append('<g>{}{}</g>'.format(vis, "".join(trail)))
    radius = 4.8 * (1 + 0.55 * lift)
    o.append('<g>{}{}<circle r="13" fill="url(#glow)"/><circle cx="{}" cy="{}" r="4.8" fill="#000" fill-opacity=".5">{}{}</circle>'
             '<circle r="4.8" fill="#fff" stroke="{}" stroke-width="1">{}</circle></g>'.format(
                 vis, translate_anim(px(ball)), 1.5, 2.5, linear_anim("cx", 1.5 + 9 * lift, 1),
                 linear_anim("cy", 2.5 + 12 * lift, 1), INK, linear_anim("r", radius, 2)))

    # telestration chips
    touch_f = np.flatnonzero(f["near_away"] & window(3.5, 4.5))
    tp = px(ball[touch_f[0]] if len(touch_f) else ball[frame(T_TOUCH)])
    o.append(chip(tp[0] + 18, tp[1] + 34, "touch ≠ control · label holds", window(T_TOUCH - 0.1, T_PASS2 + 0.2), RED))
    o.append(chip(ip[0] + 20, ip[1] - 30, "sustained control → possession flips", window(T_INTERCEPT + 0.1, T_GAP0), RED))
    gp = px(ball[frame((T_GAP0 + T_GAP1) / 2)])
    o.append(chip(gp[0] - 14, gp[1] + 40, "ball not tracked · possession held", window(T_GAP0 + 0.1, T_GAP1 + 0.3), "#FFFFFF", "end"))
    op = px(np.array([cross_x, 0.0]))
    o.append(chip(op[0] + 150, op[1] + 34, "ball out → dead ball (D)", window(f_out / FPS + 0.1, T_PICK + 0.3), LIME))
    tp2 = px(pos[frame(T_SET), THROWER])
    o.append(chip(tp2[0] + 30, tp2[1] + 30, "throw-in · restart", window(T_SET, LOOP_S - 0.05), LIME))
    o.append('</g>')

    o.append(panel(labels, scores, f, p))
    o.append(timeline(labels, scores, f))
    o.append('</svg>')
    return "\n".join(o)


CAPTIONS = [
    # (t0, t1, title, body lines)
    (0.45, T_PASS1, "Control", ["A player within 1.5 m of a", "slow ball is evidence for", "their team — every frame."]),
    (T_PASS1, T_INTERCEPT, "A touch is not possession", ["A pass in flight barely counts;", "a brief touch by the other team", "can't pay the switch cost."]),
    (T_INTERCEPT, T_GAP0, "Interception", ["Possession changes only after", "real control: the other team", "keeps the ball, the label flips."]),
    (T_GAP0, T_LONG + 0.9, "Ball lost by the tracker", ["A missing ball is no evidence,", "not a stoppage. Possession", "stays with the last team."]),
    (T_LONG + 0.9, T_PICK + 0.4, "Out of play", ["Ball over the touchline, players", "slowing down: the evidence for", "a dead ball (D) takes over."]),
    (T_PICK + 0.4, 0.45, "Restart", ["Set for the throw-in. When it is", "taken, the dead-ball evidence", "stops and the label goes to H."]),
]


def panel(labels, scores, f, p):
    x0, w = PANEL_X, PANEL_W
    o = ['<g>']
    o.append('<text x="{}" y="136" class="label">DECODED LABEL</text>'.format(num(x0)))
    o.append(odometer(x0 + w, 136))
    badges = {
        "H": ('url(#badgeH)', "none", "HOME", "#fff", "H"),
        "A": ('url(#ribA)', INK, "AWAY", "#fff", "A"),
        "D": ('#1A1C1F', LIME, "DEAD BALL", LIME, "D"),
    }
    for lab, (fill, stroke, word, tc, letter) in badges.items():
        plate = ""
        if lab == "A":   # keep the word legible over the stripes
            plate = '<rect x="{}" y="160" width="{}" height="36" rx="6" fill="{}" fill-opacity=".72"/>'.format(
                num(x0 + 12), num(w - 24), INK)
        o.append('<g opacity="0">{a}<rect x="{x}" y="146" width="{w}" height="64" rx="10" fill="{f}" stroke="{s}" stroke-width="2"/>'
                 '{plate}<text x="{tx}" y="187" class="badge" style="fill:{tc}">{word}</text>'
                 '<text x="{lx}" y="190" text-anchor="end" class="badgeL" style="fill:{tc}">{l}</text></g>'.format(
                     a=fade(labels == lab, 3), x=num(x0), w=num(w), f=fill, s=stroke, plate=plate,
                     tx=num(x0 + 24), tc=tc, word=word, lx=num(x0 + w - 22), l=letter))

    o.append('<text x="{}" y="244" class="label">EVIDENCE THIS FRAME</text>'.format(num(x0)))
    ctrl_h = f["near_home"] & ~f["fast"]
    ctrl_a = f["near_away"] & ~f["fast"]
    rows = [
        ("Home player in control", "+{:g} H".format(p.w_control), f["near_home"], ctrl_h, BLUE_HI),
        ("Away player in control", "+{:g} A".format(p.w_control), f["near_away"], ctrl_a, RED),
        ("Ball out of play", "+{:.1f} D".format(p.w_oob), f["oob"], f["oob"], LIME),
        ("Players standing still", "+{:.1f} D".format(p.w_still), f["still"], f["still"], LIME),
        ("Restart window (tags)", "+{:.1f} D".format(p.w_setpiece), f["restart"], f["restart"], LIME),
        ("Ball not tracked", "no evidence", ~f["ball"], ~f["ball"], "#FFFFFF"),
    ]
    y = 258
    for name, weight, on, strong, color in rows:
        # fast ball near a player: lit at the reduced weight
        level = np.where(strong, 1.0, np.where(on, 0.45, 0.0))
        level = np.convolve(np.concatenate([level[-2:], level, level[:2]]), np.ones(3) / 3, "same")[2:-2]
        o.append('<rect x="{}" y="{}" width="{}" height="26" rx="6" fill="{}" opacity="0">{}</rect>'.format(
            num(x0 - 6), y, num(w + 12), color, linear_anim("opacity", 0.12 * level)))
        o.append('<circle cx="{}" cy="{}" r="5" fill="#2A2E33"/>'.format(num(x0 + 6), y + 13))
        o.append('<circle cx="{}" cy="{}" r="5" fill="{}" opacity="0">{}</circle>'.format(
            num(x0 + 6), y + 13, color, linear_anim("opacity", level)))
        o.append('<text x="{}" y="{}" class="row">{}</text>'.format(num(x0 + 20), y + 18, esc(name)))
        o.append('<text x="{}" y="{}" class="w" text-anchor="end">{}</text>'.format(num(x0 + w), y + 18, esc(weight)))
        y += 29

    # caption card
    cy0, cy1 = 440, 708
    o.append('<rect x="{}" y="{}" width="{}" height="{}" rx="12" fill="#111316" stroke="#23272C"/>'.format(
        num(x0 - 6), cy0, num(w + 12), cy1 - cy0))
    for i, (t0, t1, title, body) in enumerate(CAPTIONS):
        # each caption fades out before the next fades in
        g = ['<g opacity="0">{}'.format(fade(window(t0 + 0.16, t1 - 0.16), 7))]
        g.append('<text x="{}" y="{}" class="step">{:02d}</text>'.format(num(x0 + 12), cy0 + 46, i + 1))
        g.append('<text x="{}" y="{}" class="of">/ {:02d}</text>'.format(num(x0 + 60), cy0 + 46, len(CAPTIONS)))
        g.append('<text x="{}" y="{}" class="cap">{}</text>'.format(num(x0 + 12), cy0 + 82, esc(title)))
        for k, line in enumerate(body):
            g.append('<text x="{}" y="{}" class="body">{}</text>'.format(num(x0 + 12), cy0 + 110 + 22 * k, esc(line)))
        g.append('</g>')
        o.append("".join(g))
    # progress pips
    for i, (t0, t1, _, _) in enumerate(CAPTIONS):
        cx = x0 + 12 + i * 16
        o.append('<rect x="{}" y="{}" width="12" height="3" rx="1.5" fill="#2A2E33"/>'.format(num(cx), cy0 + 194))
        o.append('<rect x="{}" y="{}" width="12" height="3" rx="1.5" fill="{}" opacity="0">{}</rect>'.format(
            num(cx), cy0 + 194, LIME, fade(window(t0, t1), 4)))
    o.append('<text x="{}" y="{}" class="foot">switch cost  H↔A {:.1f} · alive↔D {:.1f}</text>'.format(
        num(x0 + 12), cy0 + 228, p.cost_team_switch, p.cost_dead_switch))
    o.append('<text x="{}" y="{}" class="foot">Viterbi over the whole sequence</text>'.format(num(x0 + 12), cy0 + 248))
    o.append('</g>')
    return "\n".join(o)


def odometer(x_right, y):
    """'FRAME 123' that counts the loop's frames: one clipped 0-9 strip per digit, stepped by
    discrete translate animations (SMIL cannot change text content)."""
    lh, cw = 14.0, 8.2
    digits = len(str(N - 1))
    x0 = x_right - digits * cw
    o = ['<text x="{}" y="{}" class="label" text-anchor="end">FRAME</text>'.format(num(x0 - 6), y)]
    for k in range(digits):
        place = 10 ** (digits - 1 - k)
        value = (np.arange(N) // place) % 10
        change = [0] + [i for i in range(1, N) if value[i] != value[i - 1]]
        vals = ";".join("0 {}".format(num(-lh * value[i])) for i in change)
        kts = ";".join("{:.5f}".format(i / N).rstrip("0").rstrip(".") or "0" for i in change)
        x = x0 + k * cw
        o.append('<clipPath id="dig{k}"><rect x="{x}" y="{y0}" width="{w}" height="{h}"/></clipPath>'.format(
            k=k, x=num(x), y0=num(y - 11.5), w=num(cw), h=num(lh)))
        strip = "".join('<text x="{}" y="{}" style="font-family:{};font-size:12.5px;font-weight:700;fill:{}">{}</text>'.format(
            num(x), num(y + d * lh), MONO, LIME, d) for d in range(10))
        o.append('<g clip-path="url(#dig{})"><g><animateTransform attributeName="transform" type="translate" '
                 'dur="{}" repeatCount="indefinite" calcMode="discrete" values="{}" keyTimes="{}"/>{}</g></g>'.format(
                     k, DUR, vals, kts, strip))
    return "".join(o)


def timeline(labels, scores, f):
    best = scores.argmax(axis=1)
    lane = np.where(scores.max(axis=1) > 0, np.array(["H", "A", "D"])[best], "-")
    lane = np.where(f["ball"] | (lane != "-"), lane, "?")
    o = ['<g>']
    o.append('<text x="{}" y="739" class="lane" text-anchor="end">per frame</text>'.format(num(RIB_X0 - 12)))
    o.append('<text x="{}" y="764" class="lane" text-anchor="end" style="fill:#E6E9EE;font-weight:600">decoded</text>'.format(num(RIB_X0 - 12)))
    o.append('<rect x="{}" y="730" width="{}" height="10" rx="2" fill="#15171A"/>'.format(num(RIB_X0), num(RIB_X1 - RIB_X0)))
    o.append('<rect x="{}" y="747" width="{}" height="24" rx="3" fill="#15171A"/>'.format(num(RIB_X0), num(RIB_X1 - RIB_X0)))
    o.append('<g clip-path="url(#reveal)">')
    o.append(ribbon(labels, lane))
    o.append('</g>')
    for s in range(0, int(LOOP_S) + 1, 2):
        x = RIB_X0 + s / LOOP_S * (RIB_X1 - RIB_X0)
        o.append('<text x="{}" y="790" class="tick" text-anchor="{}">{}</text>'.format(
            num(x), "start" if s == 0 else "end" if s == LOOP_S else "middle", "{} s".format(s) if s in (0, int(LOOP_S)) else s))
    head = np.stack([RIB_X0 + np.arange(N) / N * (RIB_X1 - RIB_X0), np.zeros(N)], 1)
    o.append('<g>{}<line x1="0" y1="724" x2="0" y2="776" stroke="{}" stroke-width="2"/>'
             '<path d="M-5 721 L5 721 L0 727 Z" fill="{}"/></g>'.format(translate_anim(head), LIME, LIME))
    o.append('</g>')
    return "\n".join(o)


# -- raster outputs ---------------------------------------------------------------------------------

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def find_browser():
    for name in [os.environ.get("HERO_BROWSER")] + BROWSERS:
        if name and os.path.exists(name):
            return name
    for name in ("msedge", "google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit("no Chromium-based browser found; set HERO_BROWSER")


def screenshot_frames(svg_text, times, workdir, workers=6):
    browser = find_browser()
    paths = []

    def shoot(job):
        i, t = job
        page = os.path.join(workdir, "f{:04d}.html".format(i))
        png = os.path.join(workdir, "f{:04d}.png".format(i))
        with open(page, "w", encoding="utf-8") as handle:
            handle.write('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#0A0A0C;'
                         'overflow:hidden}svg{display:block}</style>' + svg_text +
                         '<script>const s=document.querySelector("svg");s.pauseAnimations();'
                         's.setCurrentTime(%.4f);</script>' % t)
        profile = os.path.join(workdir, "profile{}".format(i % workers))
        cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
               "--no-first-run", "--no-default-browser-check", "--force-device-scale-factor=1",
               "--user-data-dir=" + profile, "--window-size={},{}".format(CW, CH),
               "--screenshot=" + png, "file:///" + page.replace("\\", "/")]
        for _ in range(3):
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            if os.path.exists(png):
                return png
        raise RuntimeError("screenshot failed at t={}".format(t))

    jobs = list(enumerate(times))
    # one profile per worker slot: run slot by slot so two browsers never share a profile
    with ThreadPoolExecutor(workers) as pool:
        for k in range(0, len(jobs), workers):
            paths.extend(pool.map(shoot, jobs[k:k + workers]))
    return paths


def raster(svg_text, frames_dir=None, reuse=False, gif_fps=12.5, gif_width=900, poster_t=5.6):
    from PIL import Image

    times = list(np.arange(0, LOOP_S, 1.0 / gif_fps)) + [poster_t]
    workdir = frames_dir or tempfile.mkdtemp(prefix="hero-")
    os.makedirs(workdir, exist_ok=True)
    try:
        cached = [os.path.join(workdir, "f{:04d}.png".format(i)) for i in range(len(times))]
        if reuse and all(os.path.exists(c) for c in cached):
            pngs = cached
        else:
            pngs = screenshot_frames(svg_text, times, workdir)
        poster = Image.open(pngs[-1]).convert("RGB")
        frames = [Image.open(p).convert("RGB") for p in pngs[:-1]]
    finally:
        if frames_dir is None:
            shutil.rmtree(workdir, ignore_errors=True)
    poster.save(os.path.join(OUT_DIR, "hero-poster.png"), optimize=True)
    size = (gif_width, int(round(CH * gif_width / CW)))
    small = [im.resize(size, Image.LANCZOS) for im in frames]
    ms = int(round(1000 / gif_fps))
    write_gif(small, os.path.join(OUT_DIR, "hero.gif"), ms)
    small[0].save(os.path.join(OUT_DIR, "hero.webp"), save_all=True, append_images=small[1:],
                  duration=ms, loop=0, quality=82, method=6)


def write_gif(frames, out, ms):
    """One palette for the whole loop (stable colours, small inter-frame diffs), built from a
    montage of evenly spaced frames, and no dithering (dither noise defeats frame differencing)."""
    from PIL import Image

    w, h = frames[0].size
    picks = frames[::max(1, len(frames) // 16)][:16]
    # plus swatches of the identity colours, which cover too few pixels to win a palette slot
    keys = ["#F2C230", "#1FA37A", BLUE, GARNET, BLUE_HI, GARNET_HI, RED, WHITE, LIME, VIOLET]
    band = 24
    sample = Image.new("RGB", (w, h * len(picks) + band * (len(keys) + 1)))
    for k, im in enumerate(picks):
        sample.paste(im, (0, h * k))
    y = h * len(picks)
    for color in keys:
        sample.paste(Image.new("RGB", (w, band), color), (0, y))
        y += band
    c0, c1 = np.array([0x00, 0x4D, 0x98]), np.array([0xA5, 0x00, 0x44])   # badge gradient
    ramp = (c0 + np.linspace(0, 1, w)[:, None] * (c1 - c0)).astype(np.uint8)
    sample.paste(Image.fromarray(np.repeat(ramp[None], band, 0)), (0, y))
    palette = sample.quantize(colors=256, method=Image.Quantize.MEDIANCUT, kmeans=4,
                              dither=Image.Dither.NONE)
    gif = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    gif[0].save(out, save_all=True, append_images=gif[1:], duration=ms, loop=0, optimize=True, disposal=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raster", action="store_true", help="also write hero.gif, hero.webp, hero-poster.png")
    ap.add_argument("--report", action="store_true", help="print the decoded label runs")
    ap.add_argument("--frames", help="keep the raster screenshots in this folder")
    ap.add_argument("--reuse-frames", action="store_true", help="encode from --frames without re-rendering")
    args = ap.parse_args()

    scene = build_scene()
    labels, scores, f, p = decode(scene)
    if args.report:
        runs = np.flatnonzero(labels[1:] != labels[:-1]) + 1
        edges = [0] + list(runs) + [N]
        print("decoded:", " ".join("{}[{:.2f}-{:.2f}s]".format(labels[a], a / FPS, b / FPS) for a, b in zip(edges, edges[1:])))
        for key in ("near_home", "near_away", "oob", "still", "restart", "fast"):
            idx = np.flatnonzero(f[key])
            print("{:10s} {:4d} frames {}".format(key, len(idx), "" if not len(idx) else
                                                  "first {:.2f}s last {:.2f}s".format(idx[0] / FPS, idx[-1] / FPS)))
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build_svg(scene, labels, scores, f, p)
    with open(os.path.join(OUT_DIR, "hero.svg"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(svg)
    if args.raster:
        raster(svg, args.frames, args.reuse_frames)
    for name in ("hero.svg", "hero.gif", "hero.webp", "hero-poster.png"):
        full = os.path.join(OUT_DIR, name)
        if os.path.exists(full):
            print("{:16s} {:8.0f} KB".format(name, os.path.getsize(full) / 1024))


if __name__ == "__main__":
    main()
