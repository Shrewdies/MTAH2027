"""Generate the submission from the data bundle.

    python -m possession.run --out submission.csv [--data-dir DIR] [--profile macro] [--diagnostics diag.json]

Reads the tactical ATD and the Smart Tagging only. Output is deterministic.
"""

import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games import GAME, GAMES, half_video_blocks, require, source_frames  # noqa: E402

from . import decoder, inputs  # noqa: E402
from .params import DEFAULT, load_profile  # noqa: E402

# Graded from 110,808, kick-off at 113,742 (FAQ.md): the frames in between are dead ball.
SECOND_HALF_KICKOFF = 113742


def graded_blocks(game=GAME):
    return [(first, last) for _, first, last in half_video_blocks(game)]


def forced_dead(game=GAME):
    second = [first for half, first, _ in half_video_blocks(game) if half == 2]
    return [(second[0], SECOND_HALF_KICKOFF)] if second else []


def write_submission(path, labels):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="\n") as handle:
        handle.write("frame,label\n")
        handle.writelines("{},{}\n".format(i, label) for i, label in enumerate(labels))
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="submission CSV")
    parser.add_argument("--data-dir", default=None, help="data bundle root (default: MTAH_DATA_DIR)")
    parser.add_argument("--diagnostics", default=None, help="write label-free statistics as JSON")
    parser.add_argument("--profile", default="macro",
                        help="macro (submitted), balanced, spell or reasoned")
    args = parser.parse_args(argv)

    t0 = time.time()
    meta, raw, tags_xml = require(["atd_meta", "atd_raw", "smart_tagging"], GAME, args.data_dir)
    print("reading tracking ...", flush=True)
    trk = inputs.load_tracking(meta, raw, source_frames("tactical", GAME), GAMES[GAME]["pitch"])
    events = inputs.load_tags(tags_xml, DEFAULT.fps)
    print("  {:.0f} s; teams H = {}, A = {}".format(time.time() - t0, *trk.team_names), flush=True)

    blocks = graded_blocks()
    params = load_profile(args.profile)
    tags = inputs.team_tag_windows(events, trk.team_names)
    print("  profile '{}'; team-tagged instances: {}".format(args.profile, len(tags)), flush=True)
    labels, info = decoder.decode(trk, blocks, forced_dead(), inputs.set_piece_windows(events),
                                  params, tag_windows=tags, return_info=True)
    print("  tag weights: {}".format(json.dumps(info["tag_weights"], sort_keys=True)), flush=True)
    write_submission(args.out, labels)
    print("wrote {}  ({:.0f} s total)".format(args.out, time.time() - t0))

    if args.diagnostics:
        diag = decoder.diagnostics(trk, labels, blocks, events, params)
        diag["profile"] = args.profile
        diag["tag_weights"] = info["tag_weights"]
        with open(args.diagnostics, "w") as handle:
            json.dump(diag, handle, indent=2, sort_keys=True)
        print(json.dumps(diag, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
