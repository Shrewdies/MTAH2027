---
title: "SportsLabKit"
kicker: "Vision and calibration"
summary: "A toolkit that turns sports video into tracking tables: pluggable detectors, motion and appearance models, and conversion to pitch coordinates."
group: vision-and-calibration
order: 40
chips: ["Video", "Tracking toolkit", "Full-pitch view", "GPL-3.0"]
motif: pipeline
motif_caption: "A tracker assembled from parts. Swap one stage and compare like with like."
motif_labels: ["Detector", "Motion model", "Appearance", "Matching", "Pitch coords"]
facts:
  - { k: "Modality", v: "Wide-view and broadcast video" }
  - { k: "Output", v: "Track tables in image or pitch coordinates" }
  - { k: "Evidence", v: "Notebooks implementing SORT, DeepSORT, ByteTrack and TeamTrack" }
  - { k: "Code and weights", v: "Python package; weights depend on the detector configured" }
  - { k: "Licence", v: "GPL-3.0" }
verdict: { label: "Our read", text: "The right toolkit for full-pitch video. Its lesson: wide-view tracking is a different problem from broadcast tracking, and an easier one to calibrate." }
sources:
  - { title: "SportsLabKit: a Python package for turning sports video into CSV files (repository)", url: "https://github.com/AtomScott/SportsLabKit" }
  - { title: "TeamTrack: an algorithm and benchmark dataset for multi-sport tracking in full-pitch videos (repository)", url: "https://github.com/AtomScott/TeamTrack" }
  - { title: "SoccerTrack: fish-eye and drone tracking dataset (repository)", url: "https://github.com/keisuke198619/SoccerTrack" }
related:
  - /solutions/vision-and-calibration/tracking-by-detection/
  - /solutions/vision-and-calibration/sn-gamestate/
  - /solutions/vision-and-calibration/roboflow-soccer/
  - /datasets/teamtrack/
---
SportsLabKit describes its job plainly: turn sports video into CSV files. It comes from the line of research behind SoccerTrack, which recorded matches with fish-eye and drone cameras, and TeamTrack, a multi-sport benchmark for tracking in full-pitch video.

The design is a tracker assembled from parts. A detection model finds players and ball. A motion model predicts where each track goes next. An appearance model describes what each track looks like. A matching function combines the two costs and assigns detections to tracks. The parts share common interfaces, and the package ships implementations of SORT, DeepSORT, ByteTrack and the TeamTrack method built from them. Camera utilities convert image coordinates to the pitch.

## Where it wins

- It is built for the full-pitch view, where players are tiny and never leave the frame. That is the tactical-camera regime, not the broadcast one.
- Swappable components make fair comparison cheap: same detector, different association.
- Its output is a tracking table, ready for the same tools as provider data.
- It comes with datasets that match its use case: [SoccerTrack v2]({{ '/datasets/soccertrack-v2/' | relative_url }}) and [TeamTrack]({{ '/datasets/teamtrack/' | relative_url }}).

## What it costs

- GPL-3.0.
- Trackers assemble tracks. They do not identify. Team and identity need extra models.
- Full-pitch tracking quality is bounded by the detector at small scales, and the ball is the smallest object on the pitch.
- It is research software, maintained at research pace.

## How it plugs into possession

It is the route from a tactical camera to tracking when no provider feed exists, and a way to re-track where a feed is weak. Fixed wide views simplify everything downstream: one calibration for the whole match, no cuts, every player always in view.

For possession, what matters is what the tracker does to the ball and to team labels. Tracks without teams are not yet possession input, and a tracker tuned for players will drop the ball first. The association methods it wraps are compared under [tracking by detection]({{ '/solutions/vision-and-calibration/tracking-by-detection/' | relative_url }}).
