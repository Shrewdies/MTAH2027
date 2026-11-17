"""Two-objective parameter search (spellF1, macroF1) on simulated halves.

    python -m possession.pareto --samples 64 --generations 3 --halves 6 --workers 10

Elitist evolutionary search in the spirit of NSGA-II: an initial population scaled log-uniformly
in [1/2, 2] around the defaults, then mutation of the non-dominated set in [0.8, 1.25]. Scores
come from the official evaluation/possession_metrics.py. Writes profiles.json (spell, macro,
balanced = best sum) and pareto_front.json. Seeded and reproducible.
"""

import argparse
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, replace

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "evaluation"))

import possession_metrics as pm  # noqa: E402  official scorer, unchanged

from . import decoder  # noqa: E402
from .params import DEFAULT, PROFILES_FILE, SEARCHABLE  # noqa: E402
from .simulate import simulate_half  # noqa: E402

FRONT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pareto_front.json")
BOUNDS = {"control_radius_m": (0.8, 2.5)}  # physical limits; other fields: positive only

_HALVES = None


def _init(seeds):
    global _HALVES
    _HALVES = [simulate_half(seed) for seed in seeds]


def score(values):
    """(spell_f1_mean, macro_f1) averaged over the worker's simulated halves."""
    p = replace(DEFAULT, **values)
    spell, macro = [], []
    for trk, truth, set_pieces, tags in _HALVES:
        pred = decoder.decode(trk, [(0, trk.n_frames - 1)], (), set_pieces, p, tag_windows=tags)
        result = pm.evaluate(pm.label_codes(truth), pm.label_codes(pred))
        spell.append(result["spell_f1_mean"])
        macro.append(result["macro_f1"])
    return float(np.mean(spell)), float(np.mean(macro))


def mutate(rng, base, low, high):
    out = {}
    for name in SEARCHABLE:
        value = base[name] * float(np.exp(rng.uniform(np.log(low), np.log(high))))
        lo, hi = BOUNDS.get(name, (1e-3, 1e3))
        out[name] = round(float(np.clip(value, lo, hi)), 4)
    return out


def nondominated(points):
    """Indices of points not dominated in (spell, macro), both maximised."""
    keep = []
    for i, (s_i, m_i) in enumerate(points):
        if not any((s_j >= s_i and m_j >= m_i) and (s_j > s_i or m_j > m_i)
                   for j, (s_j, m_j) in enumerate(points) if j != i):
            keep.append(i)
    return keep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--generations", type=int, default=3)
    ap.add_argument("--halves", type=int, default=4)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=2027)
    args = ap.parse_args(argv)

    rng = np.random.default_rng(args.seed)
    seeds = [args.seed + 1000 + i for i in range(args.halves)]
    base = {k: getattr(DEFAULT, k) for k in SEARCHABLE}
    candidates = [dict(base)] + [mutate(rng, base, 0.5, 2.0) for _ in range(args.samples)]
    evaluated, scores = [], []

    with ProcessPoolExecutor(args.workers, initializer=_init, initargs=(seeds,)) as pool:
        for gen in range(args.generations + 1):
            results = list(pool.map(score, candidates))
            evaluated += candidates
            scores += results
            front = nondominated(scores)
            best = max(scores, key=lambda s: s[0] + s[1])
            print("gen {}: {} evaluated, front {}, best spell {:.4f}, best macro {:.4f}, "
                  "best sum {:.4f}".format(gen, len(scores), len(front), max(s[0] for s in scores),
                                           max(s[1] for s in scores), best[0] + best[1]), flush=True)
            if gen < args.generations:
                candidates = [mutate(rng, evaluated[i], 0.8, 1.25)
                              for i in front for _ in range(max(1, args.samples // (2 * len(front))))]

    front = nondominated(scores)

    def pick(key):
        i = max(front, key=key)
        return {"params": evaluated[i], "sim_spell_f1": round(scores[i][0], 4),
                "sim_macro_f1": round(scores[i][1], 4)}

    reasoned = {"params": base, "sim_spell_f1": round(scores[0][0], 4),
                "sim_macro_f1": round(scores[0][1], 4)}
    profiles = {
        "method": "NSGA-II-style search on simulated halves (possession/simulate.py), objectives "
                  "from evaluation/possession_metrics.py; no competition data used",
        "seed": args.seed, "halves": seeds, "samples": args.samples,
        "generations": args.generations, "evaluated": len(scores),
        "profiles": {
            "balanced": pick(lambda i: scores[i][0] + scores[i][1]),
            "spell": pick(lambda i: (scores[i][0], scores[i][1])),
            "macro": pick(lambda i: (scores[i][1], scores[i][0])),
        },
        "reasoned_defaults": reasoned,
        "fixed_params": {k: v for k, v in asdict(DEFAULT).items() if k not in SEARCHABLE},
    }
    with open(PROFILES_FILE, "w") as handle:
        json.dump(profiles, handle, indent=2, sort_keys=True)
    with open(FRONT_FILE, "w") as handle:
        json.dump([{"params": evaluated[i], "spell_f1": round(s[0], 4), "macro_f1": round(s[1], 4),
                    "on_front": i in front} for i, s in enumerate(scores)], handle, indent=1)
    print(json.dumps({k: v for k, v in profiles["profiles"].items()}, indent=2))
    print("reasoned defaults:", reasoned["sim_spell_f1"], reasoned["sim_macro_f1"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
