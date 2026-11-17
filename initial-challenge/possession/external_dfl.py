"""Validation on open DFL/IDSSE data (Bassek et al. 2025, Scientific Data 12:195, CC-BY 4.0).

    python -m possession.external_dfl --positions DFL_positions.xml --info DFL_matchinformation.xml

Ball frames carry BallStatus (1 alive) and BallPossession (1 home, 2 away), giving a per-frame
H/A/D reference. Scores the profiles and the organisers' baseline method with the official
metric on the clean feed and on a degraded copy (ball missing in bursts on 41% of frames,
0.15 m noise) that resembles the competition tracking. There is no Smart Tagging for DFL.
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "evaluation"))

import possession_metrics as pm  # noqa: E402  official scorer, unchanged

from . import decoder  # noqa: E402
from .inputs import AWAY, HOME, Tracking  # noqa: E402
from .params import load_profile  # noqa: E402

FPS = 25


def read_info(path):
    """(home_id, away_id, (length, width))"""
    root = ET.parse(path).getroot()
    general = root.find(".//General")
    env = root.find(".//Environment")
    pitch = (float(env.get("PitchX", 105.0)), float(env.get("PitchY", 68.0)))
    return general.get("HomeTeamId"), general.get("GuestTeamId"), pitch


def read_positions(path, home_id, away_id):
    """{half: {"ball": (N, X, Y, status, possession), (team, person): (N, X, Y)}} streamed."""
    halves = {}
    current, rows = None, []
    for event, elem in ET.iterparse(path, events=("start", "end")):
        if event == "start" and elem.tag == "FrameSet":
            team = elem.get("TeamId")
            key = (team, elem.get("PersonId"))
            if team not in (home_id, away_id):
                key = "other"
            current = (elem.get("GameSection"), key)
            rows = []
        elif event == "end" and elem.tag == "Frame" and current is not None:
            rows.append((int(elem.get("N")), float(elem.get("X")), float(elem.get("Y")),
                         elem.get("BallStatus"), elem.get("BallPossession")))
            elem.clear()
        elif event == "end" and elem.tag == "FrameSet":
            section, key = current
            if rows:
                if key == "other" and rows[0][3] is not None:
                    key = "ball"
                if key != "other":
                    halves.setdefault(section, {})[key] = rows
            current = None
            elem.clear()
    return halves


def build_half(objects, home_id, pitch, rng=None):
    """(Tracking, truth labels) for one half; rng given -> degrade the ball track."""
    ball = np.array([(r[0], r[1], r[2], int(r[3] or 0), int(r[4] or 0)) for r in objects["ball"]])
    n0 = int(ball[:, 0].min())
    n = int(ball[:, 0].max()) - n0 + 1
    length, width = pitch
    shift = (length / 2.0, width / 2.0)  # DFL origin is the centre spot

    bx, by = np.full(n, np.nan), np.full(n, np.nan)
    idx = ball[:, 0].astype(int) - n0
    bx[idx], by[idx] = ball[:, 1] + shift[0], ball[:, 2] + shift[1]
    truth = np.full(n, "D", dtype="<U1")
    alive = np.zeros(n, dtype=bool)
    alive[idx] = ball[:, 3] == 1
    poss = np.zeros(n, dtype=int)
    poss[idx] = ball[:, 4]
    truth[alive & (poss == 1)] = "H"
    truth[alive & (poss == 2)] = "A"

    people = [k for k in objects if k != "ball"]
    team = np.array([HOME if k[0] == home_id else AWAY for k in people], dtype=np.int8)
    px = np.full((n, len(people)), np.nan)
    py = np.full((n, len(people)), np.nan)
    for j, k in enumerate(people):
        arr = np.array([(r[0], r[1], r[2]) for r in objects[k]])
        ii = arr[:, 0].astype(int) - n0
        ok = (ii >= 0) & (ii < n)
        px[ii[ok], j], py[ii[ok], j] = arr[ok, 1] + shift[0], arr[ok, 2] + shift[1]
    ps = np.full_like(px, np.nan)
    ps[1:] = np.hypot(np.diff(px, axis=0), np.diff(py, axis=0)) * FPS  # m/s from positions

    if rng is not None:
        on_len = 1.5 * FPS * (1 - 0.41) / 0.41
        missing = np.zeros(n, dtype=bool)
        t, off = 0, False
        while t < n:
            d = max(1, int(rng.exponential(1.5 * FPS if off else on_len)))
            missing[t:t + d] = off
            t, off = t + d, not off
        bx = bx + rng.normal(0, 0.15, n)
        by = by + rng.normal(0, 0.15, n)
        bx[missing], by[missing] = np.nan, np.nan

    trk = Tracking(px.astype(np.float32), py.astype(np.float32), ps.astype(np.float32),
                   bx.astype(np.float32), by.astype(np.float32), team, ("home", "away"), pitch)
    return trk, truth


def baseline_labels(trk, window=50):
    """Organiser baseline method: nearest tracked player's team, D if no ball, majority vote."""
    from starter.baseline import smooth  # official code, unchanged
    d_home, d_away = decoder.team_distances(trk)
    codes = np.full(trk.n_frames, -1, dtype=np.int8)
    seen = np.isfinite(d_home) | np.isfinite(d_away)
    codes[seen & (d_home <= d_away)] = HOME
    codes[seen & (d_away < d_home)] = AWAY
    return smooth(codes, window)


def score(halves_truth, halves_pred):
    gap = np.array(["X"])
    gt = np.concatenate([halves_truth[0], gap, halves_truth[1]])
    pr = np.concatenate([halves_pred[0], gap, halves_pred[1]])
    r = pm.evaluate(pm.label_codes(gt), pm.label_codes(pr))
    return r["spell_f1_mean"], r["macro_f1"], r["n_pred_spells"], r["n_gt_spells"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--positions", required=True)
    ap.add_argument("--info", required=True)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)

    home_id, away_id, pitch = read_info(args.info)
    print("reading positions ...", flush=True)
    halves = read_positions(args.positions, home_id, away_id)
    sections = [s for s in ("firstHalf", "secondHalf") if s in halves]
    print("halves:", sections, flush=True)

    for condition, seed in (("clean DFL ball track", None), ("degraded to ~41% missing ball", args.seed)):
        rng = np.random.default_rng(seed) if seed is not None else None
        built = [build_half(halves[s], home_id, pitch, rng) for s in sections]
        truths = [t for _, t in built]
        missing = np.mean(np.concatenate([np.isnan(trk.bx) for trk, _ in built]))
        print("\n== {} (ball missing {:.0%}) ==".format(condition, missing))
        print("{:<28} {:>8} {:>8} {:>6} {:>6}".format("method", "spellF1", "macroF1", "poss", "gt"))
        rows = [("organiser baseline smooth50", [baseline_labels(trk) for trk, _ in built])]
        for prof in ("reasoned", "balanced", "spell", "macro"):
            p = load_profile(prof)
            rows.append(("ours: " + prof,
                         [decoder.decode(trk, [(0, trk.n_frames - 1)], (), (), p) for trk, _ in built]))
        for name, preds in rows:
            s, m, n_pred, n_gt = score(truths, preds)
            print("{:<28} {:>8.4f} {:>8.4f} {:>6} {:>6}".format(name, s, m, n_pred, n_gt), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
