"""Readers for the tactical ATD (metadata + raw) and the Smart Tagging XML.

ATD raw lines are ``<frame_id>:<slot>;<slot>;...:<ball>`` with ``x,y,speed`` groups, ``NaN`` for
missing values and coordinates normalised to [0, 1]. ``video_frame = frame_id - 1``. The first
``Team`` in the metadata is home and ``Player`` order is slot order. Positions are returned in
metres.
"""

import difflib
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np

HOME, AWAY = 0, 1


@dataclass
class Tracking:
    px: np.ndarray          # (frames, slots) metres
    py: np.ndarray
    ps: np.ndarray          # player speed, m/s
    bx: np.ndarray          # (frames,) metres
    by: np.ndarray
    team: np.ndarray        # (slots,) HOME or AWAY
    team_names: tuple       # (home, away)
    pitch: tuple            # (length, width) metres

    @property
    def n_frames(self):
        return len(self.bx)


@dataclass
class TagEvent:
    code: str
    start: int              # first video frame
    end: int                # one past the last video frame
    tags: dict


def load_meta(meta_path):
    root = ET.parse(meta_path).getroot()
    teams = list(root.iter("Team"))
    if len(teams) != 2:
        raise ValueError("{}: expected 2 teams, found {}".format(meta_path, len(teams)))
    home_id = teams[0].get("id")
    slots = [player.get("teamId") for player in root.iter("Player")]
    if not slots:
        raise ValueError("{}: no Player entries".format(meta_path))
    team = np.array([HOME if tid == home_id else AWAY for tid in slots], dtype=np.int8)
    names = tuple((t.findtext("Name") or "").strip() for t in teams)
    return team, names


def _missing(text):
    return not text or text[0] in "Nn"


def load_tracking(meta_path, raw_path, n_frames, pitch):
    team, names = load_meta(meta_path)
    n_slots = len(team)
    length, width = pitch
    px = np.full((n_frames, n_slots), np.nan, dtype=np.float32)
    py = np.full((n_frames, n_slots), np.nan, dtype=np.float32)
    ps = np.full((n_frames, n_slots), np.nan, dtype=np.float32)
    bx = np.full(n_frames, np.nan, dtype=np.float32)
    by = np.full(n_frames, np.nan, dtype=np.float32)

    with open(raw_path) as handle:
        for line in handle:
            parts = line.rstrip("\r\n").split(":")
            if len(parts) != 3:
                continue
            frame = int(parts[0]) - 1
            if not 0 <= frame < n_frames:
                continue
            for slot, group in enumerate(parts[1].split(";")[:n_slots]):
                if _missing(group):
                    continue
                values = group.split(",")
                px[frame, slot] = float(values[0]) * length
                py[frame, slot] = float(values[1]) * width
                if len(values) > 2:
                    ps[frame, slot] = float(values[2])
            ball = parts[2].split(",")
            if not _missing(ball[0]) and len(ball) >= 2:
                bx[frame] = float(ball[0]) * length
                by[frame] = float(ball[1]) * width
    return Tracking(px, py, ps, bx, by, team, names, (float(length), float(width)))


def load_tags(xml_path, fps):
    events = []
    for inst in ET.parse(xml_path).iter("instance"):
        start_s, end_s = float(inst.findtext("start")), float(inst.findtext("end"))
        tags = {(label.findtext("group") or "").strip(): (label.findtext("text") or "").strip()
                for label in inst.findall("label")}
        events.append(TagEvent((inst.findtext("code") or "").strip(),
                               int(round(start_s * fps)), int(round(end_s * fps)), tags))
    return events


def set_piece_windows(events):
    return [(e.start, e.end) for e in events if e.code.lower() == "set pieces"]


def team_tag_windows(events, team_names):
    """(start, end, side, CODE) for every instance whose Team resolves to a side."""
    out = []
    for e in events:
        side = tag_team_side(e.tags.get("Team"), team_names)
        if side is not None and e.end > e.start:
            out.append((e.start, e.end, side, e.code.strip().upper()))
    return out


def tag_team_side(tag_value, team_names):
    """HOME/AWAY for a tag's club name, or None when it is N/A or ambiguous.

    Tag and metadata spellings differ (``Atletic Club`` vs ``Athletic Club``), so names are
    matched by similarity and only when one side is clearly closer.
    """
    value = (tag_value or "").strip().lower()
    if not value or value == "n/a":
        return None

    def similarity(name):
        name = name.lower()
        contained = 1.0 if value in name or (name and name in value) else 0.0
        return max(difflib.SequenceMatcher(None, value, name).ratio(), contained)

    scores = [similarity(name) for name in team_names]
    best = int(np.argmax(scores))
    if scores[best] >= 0.5 and scores[best] - scores[1 - best] >= 0.15:
        return best
    return None
