"""Decoder parameters.

Evidence is accumulated per frame and decoded with a fixed cost per state change, so each
constant is either an evidence weight (per frame) or a switch cost (in frames of evidence).
With ``w_control = 1``, ``cost_team_switch = 8`` means roughly 0.3 s of clear control by the
other team before possession flips.

References
  control radius   databallpy possession zone (FIFA method), Vidal-Codina et al. 2022
  loose balls      Link & Hoernig 2017; Opta possession definition
  stoppages        Lang et al. 2022
"""

import json
import os
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Params:
    fps: int = 25

    # team control
    control_radius_m: float = 1.5
    control_max_ball_speed: float = 7.0   # m/s; faster balls are passing by, not controlled
    w_control: float = 1.0
    w_control_fast: float = 0.2

    # dead ball
    oob_margin_m: float = 1.0
    w_oob: float = 3.0
    still_speed: float = 0.9              # m/s, median player speed
    still_window_s: float = 3.0
    w_still: float = 0.3
    ball_stationary_speed: float = 1.0    # m/s, above position jitter
    ball_stationary_window_s: float = 1.5
    w_ball_stationary: float = 0.5
    setpiece_dead_fraction: float = 0.4   # leading share of a set-piece window before the restart
    w_setpiece: float = 0.6
    alive_ball_speed: float = 3.0         # m/s
    w_alive: float = 0.3

    # tag evidence (team only, never alive/dead)
    w_tag_scale: float = 0.10
    tag_cap: float = 0.5
    tag_min_control_frames: int = 200

    # Viterbi switch costs
    cost_team_switch: float = 10.0
    cost_dead_switch: float = 20.0

    speed_half_window: int = 2            # frames each side for ball speed


DEFAULT = Params()

# Fields explored by possession.pareto. The control radius is excluded: the simulator cannot
# reproduce real centroid noise and drives it to its lower bound.
SEARCHABLE = ("cost_team_switch", "cost_dead_switch", "w_oob", "w_still",
              "w_ball_stationary", "w_setpiece", "w_tag_scale")

PROFILES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles.json")


def load_profile(name="macro"):
    """Parameters of a frozen profile from profiles.json; ``reasoned`` returns the defaults."""
    if name == "reasoned":
        return DEFAULT
    with open(PROFILES_FILE) as handle:
        profiles = json.load(handle)["profiles"]
    if name not in profiles:
        raise KeyError("unknown profile {!r}; have {}".format(name, sorted(profiles) + ["reasoned"]))
    return replace(DEFAULT, **profiles[name]["params"])
