"""Per-frame possession evidence and Viterbi decoding into H / A / D.

A frame without information scores zero for every state, so an untracked ball keeps the current
state instead of producing a stoppage; under spellF1 a spurious D would split a real possession.
Evidence has two independent factors: alive vs dead, and home vs away. Ball control informs both;
tag evidence informs only the team and is applied as a penalty on the opposing side.
"""

import warnings

import numpy as np

from .inputs import AWAY, HOME, tag_team_side
from .params import DEFAULT

H, A, D = 0, 1, 2
LETTERS = np.array(["H", "A", "D"])


def rolling_nanmean(values, window):
    half = window // 2
    valid = ~np.isnan(values)
    csum = np.concatenate(([0.0], np.cumsum(np.where(valid, values, 0.0), dtype=np.float64)))
    ccnt = np.concatenate(([0], np.cumsum(valid)))
    idx = np.arange(len(values))
    lo, hi = np.maximum(0, idx - half), np.minimum(len(values), idx + half + 1)
    count = ccnt[hi] - ccnt[lo]
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(count > 0, (csum[hi] - csum[lo]) / np.maximum(count, 1), np.nan)


def rolling_max_full(values, window):
    """Centred rolling max; NaN unless the whole window is observed."""
    half = window // 2
    padded = np.concatenate((np.full(half, np.nan), values, np.full(half, np.nan)))
    return np.lib.stride_tricks.sliding_window_view(padded, 2 * half + 1).max(axis=1)


def ball_speed(trk, half_window, fps):
    k, n = half_window, trk.n_frames
    speed = np.full(n, np.nan, dtype=np.float64)
    if n > 2 * k:
        dx = trk.bx[2 * k:].astype(np.float64) - trk.bx[:-2 * k]
        dy = trk.by[2 * k:].astype(np.float64) - trk.by[:-2 * k]
        speed[k:n - k] = np.hypot(dx, dy) / (2.0 * k / float(fps))
    return speed


def team_distances(trk):
    """Distance from the ball to the nearest home and away player; inf when unobserved."""
    dist = np.hypot(trk.px - trk.bx[:, None], trk.py - trk.by[:, None])
    dist = np.where(np.isnan(dist), np.inf, dist)
    nearest = []
    for side in (HOME, AWAY):
        cols = trk.team == side
        nearest.append(dist[:, cols].min(axis=1) if cols.any() else np.full(trk.n_frames, np.inf))
    return tuple(nearest)


def features(trk, p=DEFAULT):
    length, width = trk.pitch
    ball = ~np.isnan(trk.bx)
    speed = ball_speed(trk, p.speed_half_window, p.fps)
    d_home, d_away = team_distances(trk)
    m = p.oob_margin_m
    with np.errstate(invalid="ignore"):
        oob = ball & ((trk.bx < -m) | (trk.bx > length + m) | (trk.by < -m) | (trk.by > width + m))
    inside = ball & ~oob

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        median_speed = np.nanmedian(trk.ps, axis=1)
    crowd_speed = rolling_nanmean(median_speed, int(round(p.still_window_s * p.fps)))
    ball_peak = rolling_max_full(speed, int(round(p.ball_stationary_window_s * p.fps)))

    with np.errstate(invalid="ignore"):
        return {
            "ball": ball,
            "speed": speed,
            "oob": oob,
            "inside": inside,
            "near_home": inside & (d_home <= p.control_radius_m) & (d_home < d_away),
            "near_away": inside & (d_away <= p.control_radius_m) & (d_away < d_home),
            "still": crowd_speed < p.still_speed,
            "stationary": inside & (ball_peak < p.ball_stationary_speed),
            "fast": speed > p.control_max_ball_speed,
            "moving": inside & (speed > p.alive_ball_speed),
        }


def calibrate_tags(feats, tag_windows, p=DEFAULT):
    """Log-odds that each tag code's Team holds the ball, measured against visible control.

    Positive codes name the team in possession, negative codes name its opponent, codes near
    zero carry no information. Codes with too little visible control are dropped.
    """
    n = len(feats["near_home"])
    totals = {}
    for start, end, side, code in tag_windows:
        lo, hi = max(0, start), min(n, end)
        if hi <= lo:
            continue
        nh = int(feats["near_home"][lo:hi].sum())
        na = int(feats["near_away"][lo:hi].sum())
        agree, total = totals.get(code, (0, 0))
        totals[code] = (agree + (nh if side == HOME else na), total + nh + na)
    return {code: float(np.log((agree + 1.0) / (total - agree + 1.0)))
            for code, (agree, total) in sorted(totals.items())
            if total >= p.tag_min_control_frames}


def tag_signal(n, tag_windows, weights):
    """Sum of active code weights per frame, positive towards home."""
    delta = np.zeros(n + 1, dtype=np.float64)
    for start, end, side, code in tag_windows:
        w = weights.get(code)
        lo, hi = max(0, start), min(n, end)
        if w is None or hi <= lo:
            continue
        signed = w if side == HOME else -w
        delta[lo] += signed
        delta[hi] -= signed
    return np.cumsum(delta[:n])


def evidence(trk, set_pieces=(), p=DEFAULT, feats=None, team_signal=None):
    f = feats if feats is not None else features(trk, p)
    n = trk.n_frames
    scores = np.zeros((n, 3), dtype=np.float64)

    control = np.where(f["fast"], p.w_control_fast, p.w_control)
    scores[:, H] += np.where(f["near_home"], control, 0.0)
    scores[:, A] += np.where(f["near_away"], control, 0.0)
    scores[:, D] += np.where(f["oob"], p.w_oob, 0.0)
    scores[:, D] += np.where(f["still"], p.w_still, 0.0)
    scores[:, D] += np.where(f["stationary"], p.w_ball_stationary, 0.0)
    scores[:, D] -= np.where(f["moving"], p.w_alive, 0.0)
    for start, end in set_pieces:
        lo = max(0, start)
        hi = min(n, start + int(round(p.setpiece_dead_fraction * (end - start))))
        if hi > lo:
            scores[lo:hi, D] += p.w_setpiece

    if team_signal is not None:
        signal = np.clip(p.w_tag_scale * team_signal, -p.tag_cap, p.tag_cap)
        scores[:, A] -= np.maximum(signal, 0.0)
        scores[:, H] -= np.maximum(-signal, 0.0)
    return scores


def transition_costs(p=DEFAULT):
    t, d = p.cost_team_switch, p.cost_dead_switch
    return np.array([[0.0, t, d],
                     [t, 0.0, d],
                     [d, d, 0.0]])


def viterbi(scores, costs):
    """Highest-scoring state path; ties resolve to the lower state index."""
    n, k = scores.shape
    if n == 0:
        return np.zeros(0, dtype=np.int8)
    back = np.zeros((n, k), dtype=np.int8)
    acc = scores[0].copy()
    cols = np.arange(k)
    for t in range(1, n):
        cand = acc[:, None] - costs
        best = np.argmax(cand, axis=0)
        back[t] = best
        acc = cand[best, cols] + scores[t]
    path = np.empty(n, dtype=np.int8)
    path[-1] = int(np.argmax(acc))
    for t in range(n - 1, 0, -1):
        path[t - 1] = back[t, path[t]]
    return path


def decode(trk, blocks, forced_dead=(), set_pieces=(), p=DEFAULT, tag_windows=(), return_info=False):
    """Label every frame: H/A/D inside the inclusive ``blocks``, X elsewhere.

    ``forced_dead`` holds half-open ranges known to be dead ball; each block is decoded
    independently on the stretches between them.
    """
    labels = np.full(trk.n_frames, "X", dtype="<U1")
    feats = features(trk, p)
    weights = calibrate_tags(feats, tag_windows, p) if len(tag_windows) else {}
    signal = tag_signal(trk.n_frames, tag_windows, weights) if weights else None
    scores = evidence(trk, set_pieces, p, feats=feats, team_signal=signal)
    costs = transition_costs(p)

    for first, last in blocks:
        forced = np.zeros(last + 1 - first, dtype=bool)
        for start, stop in forced_dead:
            lo, hi = max(start, first), min(stop, last + 1)
            if hi > lo:
                forced[lo - first:hi - first] = True
        labels[first:last + 1][forced] = "D"
        edges = np.flatnonzero(np.diff(np.concatenate(([1], forced.astype(np.int8), [1]))))
        for a, b in zip(edges[::2], edges[1::2]):
            seg = slice(first + a, first + b)
            labels[seg] = LETTERS[viterbi(scores[seg], costs)]

    if return_info:
        return labels, {"tag_weights": {k: round(v, 3) for k, v in weights.items()}}
    return labels


def diagnostics(trk, labels, blocks, tag_events=(), p=DEFAULT):
    """Label-free summary of inputs and output: counts and fractions only."""
    f = features(trk, p)
    graded = np.zeros(trk.n_frames, dtype=bool)
    for first, last in blocks:
        graded[first:last + 1] = True

    spells, alive = 0, 0
    for first, last in blocks:
        seg = labels[first:last + 1]
        team = (seg == "H") | (seg == "A")
        alive += int(team.sum())
        starts = np.concatenate(([0], np.flatnonzero(seg[1:] != seg[:-1]) + 1))
        spells += int(np.sum(team[starts]))

    out = {
        "graded_frames": int(graded.sum()),
        "label_counts": {k: int(np.sum(labels[graded] == k)) for k in ("H", "A", "D", "X")},
        "n_possessions": spells,
        "mean_possession_s": round(alive / float(p.fps) / spells, 2) if spells else 0.0,
        "ball_observed_frac": round(float(f["ball"][graded].mean()), 3),
        "ball_out_frac": round(float(f["oob"][graded].mean()), 3),
        "control_evidence_frac": round(float((f["near_home"] | f["near_away"])[graded].mean()), 3),
        "still_frac": round(float(f["still"][graded].mean()), 3),
        "stationary_frac": round(float(f["stationary"][graded].mean()), 3),
    }

    agree = {}
    for e in tag_events:
        side = tag_team_side(e.tags.get("Team"), trk.team_names)
        if side is None:
            continue
        lo, hi = max(0, e.start), min(trk.n_frames, e.end)
        nh = int(f["near_home"][lo:hi].sum())
        na = int(f["near_away"][lo:hi].sum())
        row = agree.setdefault(e.code.upper(), [0, 0])
        row[0] += nh if side == HOME else na
        row[1] += nh + na
    out["tag_team_agreement"] = {
        code: {"control_frames": total, "agree_frac": round(hit / float(total), 3) if total else None}
        for code, (hit, total) in sorted(agree.items())}
    return out
