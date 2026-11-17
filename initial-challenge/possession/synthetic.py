"""Fabricated matches for tests. Contains no provided data: every number is invented here.

A Scene holds positions in metres; write_atd() serialises it in the ATD format the real loader
reads (normalised coordinates, NaN for missing), so the tests exercise the real parser too.
"""

import os

import numpy as np

from .inputs import AWAY, HOME, Tracking

PITCH = (105.3, 68.0)

META_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<main><Metadata><Teams>
<Team id="T1"><Name>Home FC</Name></Team>
<Team id="T2"><Name>Away Club</Name></Team>
</Teams><Players>
{players}
</Players></Metadata></main>
"""


class Scene:
    """n frames, slots with fixed teams. Players default to spread-out positions moving at
    jogging speed, so no stillness or control evidence exists unless a test creates it."""

    def __init__(self, n, teams=(HOME, HOME, AWAY, AWAY)):
        self.team = np.array(teams, dtype=np.int8)
        s = len(teams)
        base_x = np.linspace(20.0, 85.0, s)
        self.px = np.tile(base_x, (n, 1)).astype(np.float64)
        self.py = np.tile(np.where(np.arange(s) % 2 == 0, 20.0, 48.0), (n, 1)).astype(np.float64)
        self.ps = np.full((n, s), 2.5)
        self.bx = np.full(n, np.nan)
        self.by = np.full(n, np.nan)

    def ball_with(self, slot, frames, offset=(0.5, 0.0)):
        """Ball glued to a player (dribble): within control radius, player-speed ball."""
        self.bx[frames] = self.px[frames, slot] + offset[0]
        self.by[frames] = self.py[frames, slot] + offset[1]

    def ball_line(self, frames, start, end):
        """Ball moving in a straight line from start to end (metres) over the given frames."""
        frames = np.arange(frames.start, frames.stop)
        t = np.linspace(0.0, 1.0, len(frames))
        self.bx[frames] = start[0] + t * (end[0] - start[0])
        self.by[frames] = start[1] + t * (end[1] - start[1])

    def tracking(self):
        return Tracking(self.px.astype(np.float32), self.py.astype(np.float32),
                        self.ps.astype(np.float32), self.bx.astype(np.float32),
                        self.by.astype(np.float32), self.team.copy(),
                        ("Home FC", "Away Club"), PITCH)


def write_atd(scene, folder):
    """(meta_path, raw_path) of the scene in ATD format; frame_id = video frame + 1."""
    os.makedirs(folder, exist_ok=True)
    players = "\n".join('<Player id="P{0}" teamId="{1}"><Name>Track {0}</Name></Player>'.format(
        i + 1, "T1" if t == HOME else "T2") for i, t in enumerate(scene.team))
    meta = os.path.join(folder, "synthetic_atd.xml")
    with open(meta, "w") as handle:
        handle.write(META_TEMPLATE.format(players=players))

    length, width = PITCH

    def fmt(value, scale):
        return "NaN" if np.isnan(value) else repr(float(value) / scale)

    raw = os.path.join(folder, "synthetic_atd.txt")
    with open(raw, "w") as handle:
        for t in range(len(scene.bx)):
            groups = ";".join("{},{},{}".format(fmt(scene.px[t, s], length), fmt(scene.py[t, s], width),
                                                "NaN" if np.isnan(scene.ps[t, s]) else repr(float(scene.ps[t, s])))
                              for s in range(len(scene.team)))
            ball = "{},{},0.0".format(fmt(scene.bx[t], length), fmt(scene.by[t], width))
            handle.write("{}:{}:{}\n".format(t + 1, groups, ball))
    return meta, raw
