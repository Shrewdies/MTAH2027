"""Synthetic halves with known H/A/D labels, used by the Pareto search.

Generative model
  spells     possession 1 s + Exp(10 s); after a spell, dead ball with p = 0.35
             (3 s + Exp(17 s)), otherwise a turnover
  players    10 per side, random walk at ~2.5 m/s in play, ~0.6 m/s in stoppages
  ball       0.5 m from the carrier, passed every ~2.5 s (0.6 s flight); p = 0.3 per spell of an
             opponent touch without control; stoppages leave it out of play or placed
  tags       SET PIECES window of +/-2.5 s per restart; per spell an ATTACK tag naming the
             possessing team with p = 0.8, its DEFEND mirror and a NOISE tag
  observed   ball missing in Markov bursts (mean gap 1.5 s) on ~41% of frames, 0.15 m noise

Sources: spell and stoppage lengths are football rules of thumb (possessions of about 11 s, a
third ending in a stoppage of about 20 s); the share of frames without a ball matches the
competition tracking; gap length, position noise and tag reliability are assumptions.

Not modelled: team shape, pressing and duels, ball height, tracking errors on players. The ball
stays closer to its carrier than in real tracking, so the control radius is kept out of the
search (params.SEARCHABLE).
"""

import numpy as np

from .inputs import AWAY, HOME, Tracking

PITCH = (105.0, 68.0)
FPS = 25
MEAN_POSSESSION_S = 11.0
P_STOPPAGE = 0.35
MEAN_STOPPAGE_S = 20.0
PASS_EVERY_S = 2.5
PASS_FLIGHT_S = 0.6
BALL_MISSING = 0.41
MEAN_GAP_S = 1.5
TAG_RELIABILITY = 0.8


def _segments(rng, n):
    segments, t, team = [], 0, int(rng.integers(2))
    while t < n:
        d = int(FPS * (1.0 + rng.exponential(MEAN_POSSESSION_S - 1.0)))
        segments.append((t, min(n, t + d), team))
        t += d
        if t >= n:
            break
        if rng.random() < P_STOPPAGE:
            d = int(FPS * (3.0 + rng.exponential(MEAN_STOPPAGE_S - 3.0)))
            segments.append((t, min(n, t + d), 2))
            t += d
            team = int(rng.integers(2))
        else:
            team = 1 - team
    return segments


def simulate_half(seed, minutes=20.0, per_team=10):
    """(Tracking, labels 'H'/'A'/'D', set_piece_windows, tag_windows) for one synthetic half."""
    rng = np.random.default_rng(seed)
    n = int(minutes * 60 * FPS)
    length, width = PITCH
    segs = _segments(rng, n)
    state = np.empty(n, dtype=np.int8)
    for a, b, s in segs:
        state[a:b] = s

    slots = 2 * per_team
    team = np.array([HOME] * per_team + [AWAY] * per_team, dtype=np.int8)
    speed = np.where(state[:, None] == 2, 0.6, 2.5) * rng.uniform(0.7, 1.3, (n, slots))
    angle = np.cumsum(rng.normal(0.0, 0.08, (n, slots)), axis=0) + rng.uniform(0, 2 * np.pi, slots)
    px = np.clip(rng.uniform(10, length - 10, slots) + np.cumsum(speed * np.cos(angle) / FPS, axis=0), 1, length - 1)
    py = np.clip(rng.uniform(5, width - 5, slots) + np.cumsum(speed * np.sin(angle) / FPS, axis=0), 1, width - 1)
    bx, by = np.full(n, np.nan), np.full(n, np.nan)

    flight = int(PASS_FLIGHT_S * FPS)
    last = (length / 2, width / 2)
    set_pieces, tag_windows = [], []
    members = {HOME: np.flatnonzero(team == HOME), AWAY: np.flatnonzero(team == AWAY)}
    for a, b, s in segs:
        if s == 2:  # stoppage
            if rng.random() < 0.5:
                spot = (float(rng.uniform(5, length - 5)), -2.0)            # out of play
            else:
                spot = last                                               # placed on the pitch
            bx[a:b], by[a:b] = spot
            taker = int(rng.choice(np.arange(slots)))
            hold = slice(max(a, b - FPS), b)
            px[hold, taker], py[hold, taker] = spot[0], max(spot[1], 0.0) + 0.5
            set_pieces.append((b - int(2.5 * FPS), b + int(2.5 * FPS)))
            last = (float(np.clip(spot[0], 1, length - 1)), float(np.clip(spot[1], 1, width - 1)))
            continue
        t, carrier = a, int(rng.choice(members[s]))
        while t < b:
            stay = int(FPS * rng.uniform(0.5, 2.0) * PASS_EVERY_S)
            f_end = min(b, t + flight)
            k = np.arange(t, f_end)
            if len(k):  # flight from the last ball position to the new carrier
                w = np.linspace(0, 1, len(k))
                bx[k] = last[0] + w * (px[f_end - 1, carrier] - last[0])
                by[k] = last[1] + w * (py[f_end - 1, carrier] - last[1])
            hold = slice(f_end, min(b, t + stay))
            bx[hold], by[hold] = px[hold, carrier] + 0.5, py[hold, carrier]
            t = min(b, t + stay)
            last = (float(bx[t - 1]), float(by[t - 1]))
            carrier = int(rng.choice(members[s][members[s] != carrier]))
        if rng.random() < 0.3 and b - a > 2 * FPS:  # opponent touch without control
            f = int(rng.integers(a + FPS, b - FPS // 2))
            opp = int(rng.choice(members[1 - s]))
            touch = slice(f, f + 5)
            if not np.isnan(bx[f]):
                px[touch, opp], py[touch, opp] = bx[touch] + 0.8, by[touch]
        if b - a > 4 * FPS:
            j1, j2 = rng.integers(-FPS, FPS + 1, 2)
            named = s if rng.random() < TAG_RELIABILITY else 1 - s
            lo, hi = max(0, a + int(j1)), min(n, b + int(j2))
            tag_windows.append((lo, hi, named, "ATTACK"))
            tag_windows.append((lo, hi, 1 - named, "DEFEND"))
            tag_windows.append((lo, hi, int(rng.integers(2)), "NOISE"))

    # observation model: bursty missing ball + noise
    on_len = MEAN_GAP_S * FPS * (1 - BALL_MISSING) / BALL_MISSING
    missing = np.zeros(n, dtype=bool)
    t, off = 0, False
    while t < n:
        d = max(1, int(rng.exponential(MEAN_GAP_S * FPS if off else on_len)))
        missing[t:t + d] = off
        t += d
        off = not off
    bx = bx + rng.normal(0, 0.15, n)
    by = by + rng.normal(0, 0.15, n)
    bx[missing], by[missing] = np.nan, np.nan

    trk = Tracking(px.astype(np.float32), py.astype(np.float32), speed.astype(np.float32),
                   bx.astype(np.float32), by.astype(np.float32), team, ("Home FC", "Away Club"),
                   PITCH)
    labels = np.array(["H", "A", "D"])[state]
    set_pieces = [(max(0, lo), min(n, hi)) for lo, hi in set_pieces]
    return trk, labels, set_pieces, tag_windows
