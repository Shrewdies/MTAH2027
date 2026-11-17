---
title: "Tracking by detection (ByteTrack, BoT-SORT, StrongSORT)"
kicker: "Vision and calibration"
summary: "Three ways to link per-frame detections into tracks. They differ in what they trust: boxes alone, boxes plus camera motion, or boxes plus appearance."
group: vision-and-calibration
order: 30
chips: ["Video", "Multi-object tracking", "Open weights", "MIT / GPL-3.0"]
motif: tracks
motif_caption: "Detections become tracks by association. The hard frames are the ones where two players cross."
motif_labels: ["Track ID", "Motion trail"]
facts:
  - { k: "Modality", v: "Video plus per-frame detections" }
  - { k: "Output", v: "Track identities over time" }
  - { k: "Evidence", v: "ECCV 2022 (ByteTrack); public MOT benchmarks for all three" }
  - { k: "Code and weights", v: "Source code with benchmark checkpoints, trained on pedestrians" }
  - { k: "Licence", v: "MIT (ByteTrack, BoT-SORT), GPL-3.0 (StrongSORT)" }
verdict: { label: "Our read", text: "Start with ByteTrack, add camera compensation for broadcast, and do not expect appearance to tell team-mates apart." }
sources:
  - { title: "ByteTrack: Multi-Object Tracking by Associating Every Detection Box (arXiv 2110.06864, ECCV 2022)", url: "https://arxiv.org/abs/2110.06864" }
  - { title: "ByteTrack: official code", url: "https://github.com/ifzhang/ByteTrack" }
  - { title: "BoT-SORT: Robust Associations Multi-Pedestrian Tracking (official code)", url: "https://github.com/NirAharon/BoT-SORT" }
  - { title: "StrongSORT: Make DeepSORT Great Again (official code)", url: "https://github.com/dyhBUPT/StrongSORT" }
related:
  - /solutions/vision-and-calibration/sportslabkit/
  - /solutions/vision-and-calibration/soccernet-reid/
  - /solutions/physics-and-features/ball-trajectory-kalman/
  - /datasets/soccernet-tracking/
---
Modern trackers detect in every frame and then solve an association problem: which detection continues which track. A [Kalman filter]({{ '/solutions/physics-and-features/ball-trajectory-kalman/' | relative_url }}) predicts each track's next box, a cost matrix compares predictions with detections, and an assignment step matches them. The three methods here differ in what goes into the cost.

ByteTrack's insight concerns what gets thrown away. Standard practice discards low-confidence detections. ByteTrack associates the confident boxes first, then matches the remaining tracks against the weak boxes on motion alone. Occluded players produce weak detections, and this second pass keeps their tracks alive.

BoT-SORT adds camera-motion compensation. It estimates how the image moved between frames and corrects the predictions, which matters whenever the camera pans. StrongSORT upgrades DeepSORT with stronger appearance embeddings and better motion handling, and leans hardest on what each person looks like.

| Tracker | Association cue | Best when | Licence |
|---|---|---|---|
| ByteTrack | Motion, in two confidence passes | Fixed camera, crowded scenes | MIT |
| BoT-SORT | Motion with camera compensation; optional appearance | Panning broadcast camera | MIT |
| StrongSORT | Appearance embeddings plus motion | Long occlusions, distinct appearances | GPL-3.0 |

## Where it wins

- ByteTrack is fast and needs no appearance model. On a fixed tactical camera it is hard to beat for its cost.
- Camera compensation makes BoT-SORT the sensible default for broadcast footage.
- Appearance helps recover an identity after a long occlusion, when motion prediction has drifted.
- All three accept any detector.

## What it costs

- Football is a worst case for appearance. Ten outfield players wear the same kit, and embeddings that separate pedestrians barely separate team-mates.
- Motion models assume smooth movement. Cuts, sprints and changes of direction at contact break that assumption.
- Published checkpoints are trained on pedestrian benchmarks. Football needs a football detector in front.
- Identity switches cluster in duels and set pieces, the moments possession analysis cares about.

## How it plugs into possession

Trackers decide whether "the player near the ball" is the same player from one frame to the next. For team-level possession that matters less than it seems. An identity switch between team-mates leaves the team label intact. A switch between opponents does not, and those happen in tackles.

So choose the tracker on team consistency under contact, not on benchmark identity scores. Motion-only association with a team classifier on top is often the robust choice for possession, and the cheapest.
