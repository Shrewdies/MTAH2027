---
title: "Game State Reconstruction baseline"
kicker: "Vision and calibration"
summary: "The full chain from broadcast video to a minimap: detect, track, identify team, role and shirt number, and place every athlete on the pitch."
group: vision-and-calibration
order: 20
chips: ["Video", "Full pipeline", "Open weights", "GPL-3.0"]
motif: stack
motif_caption: "Game state is built in layers. Each layer adds one attribute to every athlete."
motif_labels: ["Boxes and tracks", "Team and role", "Shirt number", "Pitch position"]
facts:
  - { k: "Modality", v: "Broadcast video" }
  - { k: "Output", v: "Pitch position, team, role and shirt number per athlete" }
  - { k: "Evidence", v: "CVPR Workshops 2024" }
  - { k: "Code and weights", v: "Modular TrackLab baseline with downloadable weights" }
  - { k: "Licence", v: "GPL-3.0" }
verdict: { label: "Our read", text: "The reference design for video-to-tracking. Use it to understand every stage and where each one fails." }
sources:
  - { title: "sn-gamestate: official code for SoccerNet Game State Reconstruction", url: "https://github.com/SoccerNet/sn-gamestate" }
  - { title: "SoccerNet Game State Reconstruction: End-to-End Athlete Tracking and Identification on a Minimap (arXiv 2404.11335)", url: "https://arxiv.org/abs/2404.11335" }
related:
  - /solutions/vision-and-calibration/roboflow-soccer/
  - /solutions/vision-and-calibration/soccernet-reid/
  - /solutions/direct-possession/pathcrf/
  - /datasets/soccernet-gsr/
---
Game State Reconstruction is the task of turning a single broadcast camera into what a tracking provider sells: every athlete, identified, in pitch coordinates. SoccerNet defined the task, released [the data]({{ '/datasets/soccernet-gsr/' | relative_url }}) and published a baseline on the TrackLab framework. This page is about the baseline.

The baseline is a pipeline of specialists. A detector finds people. A tracker links them over time. A re-identification model holds identities through occlusion. Further modules assign role and team, read shirt numbers and calibrate the camera, so that each athlete's position can be projected to the pitch. Every stage is a swappable module.

The task also brought its own metric, GS-HOTA. A track counts as correct only when its position on the pitch and its identity attributes, team, role and number, are both right.

## Where it wins

- The most complete open football vision pipeline: every stage present, with weights.
- Modular. Replace the calibrator or the tracker and re-score the whole.
- A metric that punishes the failure tracking metrics ignore: the right box with the wrong identity.
- Its output has the shape of tracking data, so downstream tools apply unchanged.

## What it costs

- Stages compound. An identity lost at the tracker becomes a wrong shirt number, a wrong team and a wrong dot on the minimap.
- No ball. Game state as defined covers athletes. Possession needs the ball or a ball-free model.
- It is GPU-heavy, a research baseline rather than a real-time system.
- GPL-3.0, plus the separate terms of each bundled model.

## How it plugs into possession

It is the missing front end for possession from video alone. Game state gives players with team labels in pitch coordinates. Add a ball detector, or a ball-free model such as [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}), and the input contract of a tracking-based possession decoder is met.

Expect tracking of lower quality than a provider feed: identity switches, gaps when the camera cuts, position noise that grows with distance from the camera. A decoder downstream must be built for missing and noisy evidence, which is the regime our own [decoder]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) was designed in.
