"""Behaviour tests on fabricated scenes (possession/synthetic.py). No provided data is used.

    python -m unittest discover -s possession/tests -t . -v
"""

import hashlib
import os
import sys
import tempfile
import unittest

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "evaluation"))

import possession_metrics as pm  # noqa: E402  official scorer module, unchanged

from possession import decoder, inputs, run  # noqa: E402
from possession.params import DEFAULT  # noqa: E402
from possession.synthetic import Scene, write_atd  # noqa: E402

JOG = 0.12  # metres per frame = 3 m/s at 25 fps


def run_scene(scene):
    trk = scene.tracking()
    return decoder.decode(trk, [(0, trk.n_frames - 1)], (), (), DEFAULT)


def move(scene, slot, frames, x0, y0, step=JOG):
    """Player runs along +x from (x0, y0) over the frames."""
    k = np.arange(frames.stop - frames.start)
    scene.px[frames, slot] = x0 + step * k
    scene.py[frames, slot] = y0


class TestScenes(unittest.TestCase):

    def test_dribble_is_one_home_possession(self):
        s = Scene(300)
        move(s, 0, slice(0, 300), 20.0, 20.0)
        s.ball_with(0, slice(0, 300))
        self.assertTrue(np.all(run_scene(s) == "H"))

    def test_interception_switches_once_near_reception(self):
        s = Scene(400)
        move(s, 0, slice(0, 400), 20.0, 20.0)
        s.ball_with(0, slice(0, 200))
        s.ball_line(slice(200, 230), (s.px[199, 0] + 0.5, 20.0), (63.3, 20.0))  # ~16 m/s pass
        move(s, 2, slice(230, 400), 63.3, 20.0)
        s.ball_with(2, slice(230, 400))
        labels = run_scene(s)
        self.assertTrue(np.all(labels[:195] == "H"))
        self.assertTrue(np.all(labels[245:] == "A"))
        change = np.flatnonzero(labels[1:] != labels[:-1]) + 1
        self.assertEqual(len(change), 1, "exactly one possession change")
        self.assertTrue(200 <= change[0] <= 245, change)

    def test_missing_ball_inside_possession_is_not_a_stoppage(self):
        s = Scene(400)
        move(s, 0, slice(0, 400), 20.0, 20.0)
        s.ball_with(0, slice(0, 400))
        s.bx[150:300] = np.nan
        s.by[150:300] = np.nan
        self.assertTrue(np.all(run_scene(s) == "H"))

    def test_ball_out_then_away_throw_in(self):
        s = Scene(500)
        move(s, 0, slice(0, 500), 20.0, 20.0)
        s.ball_with(0, slice(0, 200))
        s.ball_line(slice(200, 220), (s.px[199, 0] + 0.5, 20.0), (50.0, -3.0))
        s.bx[220:320], s.by[220:320] = 50.0, -3.0          # out, waiting for the throw
        move(s, 2, slice(320, 500), 50.0, 3.0)
        s.ball_with(2, slice(320, 500))
        labels = run_scene(s)
        self.assertTrue(np.all(labels[:195] == "H"))
        self.assertTrue(np.all(labels[230:310] == "D"))
        self.assertTrue(np.all(labels[360:] == "A"))

    def test_fast_pass_past_opponent_keeps_possession(self):
        s = Scene(400)
        move(s, 0, slice(0, 400), 20.0, 20.0)
        s.ball_with(0, slice(0, 200))
        start = (s.px[199, 0] + 0.5, 20.0)
        s.px[200:225, 3], s.py[200:225, 3] = 57.0, 20.8   # opponent 0.8 m from the pass line
        s.ball_line(slice(200, 225), start, (70.0, 20.0))  # ~26 m/s
        move(s, 1, slice(225, 400), 70.5, 20.0)
        s.ball_with(1, slice(225, 400))
        self.assertTrue(np.all(run_scene(s) == "H"))


class TestDecoderParts(unittest.TestCase):

    def test_viterbi_needs_sustained_evidence_to_switch(self):
        scores = np.zeros((40, 3))
        scores[:10, decoder.H] = 1.0
        scores[10:13, decoder.A] = 1.0      # 3-frame opponent blip < switch cost: ignored ...
        scores[13:20, decoder.H] = 1.0      # ... because the home team keeps the ball after it
        scores[20:40, decoder.A] = 1.0      # 20 frames > switch cost: switch
        path = decoder.viterbi(scores, decoder.transition_costs(DEFAULT))
        self.assertTrue(np.all(path[:20] == decoder.H))
        self.assertTrue(np.all(path[20:] == decoder.A))

    def test_blocks_and_forced_dead(self):
        s = Scene(100)
        trk = s.tracking()
        labels = decoder.decode(trk, [(10, 49), (60, 89)], [(60, 70)], (), DEFAULT)
        self.assertTrue(np.all(labels[:10] == "X"))
        self.assertTrue(np.all(labels[50:60] == "X"))
        self.assertTrue(np.all(labels[90:] == "X"))
        self.assertTrue(np.all(labels[60:70] == "D"))
        self.assertTrue(set(labels[10:50]) <= {"H", "A", "D"})

    def test_atd_round_trip_through_real_parser(self):
        s = Scene(30)
        move(s, 0, slice(0, 30), 20.0, 20.0)
        s.ball_with(0, slice(0, 30))
        s.bx[5], s.by[5] = np.nan, np.nan
        s.px[7, 2] = np.nan
        with tempfile.TemporaryDirectory() as tmp:
            meta, raw = write_atd(s, tmp)
            trk = inputs.load_tracking(meta, raw, 30, (105.3, 68.0))
        np.testing.assert_allclose(trk.px[:, 0], s.px[:, 0], atol=1e-3)
        np.testing.assert_allclose(trk.bx[[0, 1, 29]], s.bx[[0, 1, 29]], atol=1e-3)
        self.assertTrue(np.isnan(trk.bx[5]) and np.isnan(trk.px[7, 2]))
        self.assertEqual(list(trk.team), [0, 0, 1, 1])
        self.assertEqual(trk.team_names, ("Home FC", "Away Club"))

    def test_tag_team_mapping(self):
        names = ("FC Barcelona", "Athletic Club")
        self.assertEqual(inputs.tag_team_side("Barcelona", names), inputs.HOME)
        self.assertEqual(inputs.tag_team_side("Atletic Club", names), inputs.AWAY)
        self.assertIsNone(inputs.tag_team_side("N/A", names))


class TestTagCalibration(unittest.TestCase):
    """Every team-tagged code is calibrated against visible control."""

    def test_calibration_learns_direction_and_drops_thin_codes(self):
        n = 1000
        feats = {"near_home": np.zeros(n, bool), "near_away": np.zeros(n, bool)}
        feats["near_home"][0:400] = True
        feats["near_away"][500:900] = True
        windows = [(0, 400, inputs.HOME, "ATT"), (500, 900, inputs.AWAY, "ATT"),   # agrees
                   (0, 400, inputs.AWAY, "DEF"), (500, 900, inputs.HOME, "DEF"),   # mirror
                   (0, 50, inputs.HOME, "THIN")]                                   # < 200 frames
        weights = decoder.calibrate_tags(feats, windows, DEFAULT)
        self.assertGreater(weights["ATT"], 3.0)
        self.assertLess(weights["DEF"], -3.0)
        self.assertNotIn("THIN", weights)
        # the mirror code reinforces the same team rather than contradicting it
        signal = decoder.tag_signal(n, windows, weights)
        self.assertTrue(np.all(signal[100:400] > 0) and np.all(signal[600:900] < 0))

    def test_calibrated_tags_flip_possession_during_long_ball_gap(self):
        s = Scene(900)
        move(s, 0, slice(0, 900), 20.0, 20.0)
        s.ball_with(0, slice(0, 300))                    # visible home control, tagged home
        tags = [(0, 300, inputs.HOME, "ATT"), (350, 900, inputs.AWAY, "ATT")]
        trk = s.tracking()
        labels = decoder.decode(trk, [(0, 899)], (), (), DEFAULT, tag_windows=tags)
        self.assertTrue(np.all(labels[:300] == "H"))
        self.assertTrue(np.all(labels[450:] == "A"))

    def test_tags_never_change_alive_dead_evidence(self):
        s = Scene(300)
        move(s, 0, slice(0, 300), 20.0, 20.0)
        s.ball_with(0, slice(0, 150))
        trk = s.tracking()
        signal = np.linspace(-20.0, 20.0, 300)            # strong tags both ways
        with_tags = decoder.evidence(trk, (), DEFAULT, team_signal=signal)
        without = decoder.evidence(trk, (), DEFAULT)
        np.testing.assert_array_equal(with_tags[:, decoder.D], without[:, decoder.D])
        self.assertTrue(np.all(with_tags[:, :2].max(axis=1) <= without[:, :2].max(axis=1) + 1e-12))

    def test_team_tag_windows_keep_every_code_with_known_team(self):
        names = ("Barcelona", "Atletic Club")
        events = [inputs.TagEvent("BUILD UP", 10, 50, {"Team": "Barcelona"}),
                  inputs.TagEvent("DEFENDING IN MIDDLE THIRD", 60, 90, {"Team": "Barcelona"}),
                  inputs.TagEvent("SET PIECES", 0, 5, {"Team": "N/A"})]
        self.assertEqual(inputs.team_tag_windows(events, names),
                         [(10, 50, inputs.HOME, "BUILD UP"),
                          (60, 90, inputs.HOME, "DEFENDING IN MIDDLE THIRD")])

    def test_frozen_profiles_load(self):
        from possession.params import SEARCHABLE, load_profile
        for name in ("balanced", "spell", "macro", "reasoned"):
            p = load_profile(name)
            self.assertEqual(p.control_radius_m, DEFAULT.control_radius_m)
            for field in SEARCHABLE:
                self.assertGreater(getattr(p, field), 0.0)


class TestSubmissionContract(unittest.TestCase):

    def test_full_length_file_passes_official_validator_and_is_deterministic(self):
        n = 199319
        s = Scene(n, teams=(0, 1))
        s.ps[:] = np.nan
        trk = s.tracking()
        labels = decoder.decode(trk, run.graded_blocks(), run.forced_dead(), (), DEFAULT)
        self.assertTrue(np.all(labels[:11185] == "X"))
        self.assertTrue(np.all(labels[110808:run.SECOND_HALF_KICKOFF] == "D"))
        with tempfile.TemporaryDirectory() as tmp:
            paths = [run.write_submission(os.path.join(tmp, "s{}.csv".format(i)), labels)
                     for i in (1, 2)]
            self.assertIsNone(pm.validate_submission(pm.read_label_csv(paths[0]), n))
            digests = []
            for path in paths:
                with open(path, "rb") as handle:
                    digests.append(hashlib.sha256(handle.read()).hexdigest())
        self.assertEqual(digests[0], digests[1])


if __name__ == "__main__":
    unittest.main()
