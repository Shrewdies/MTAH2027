---
title: SoccerNet Tracking
kicker: Broadcast video and game state
summary: "The standard multi-object tracking benchmark for broadcast football: boxes and track IDs for players, referees and the ball in crowded 1080p clips."
group: broadcast
order: 20
chips: [Broadcast video, Boxes, Track IDs, Ball]
motif: boxes
motif_caption: "The ball is the smallest box in the frame, and the one possession depends on."
motif_labels: [Player, Ball]
facts:
  - { k: Modality, v: "1080p main-camera clips with boxes, track IDs and classes" }
  - { k: Classes, v: "Players by team, referees, ball" }
  - { k: Possession labels, v: "None" }
  - { k: Calibration, v: "None. Pixel space only" }
  - { k: Licence, v: "SoccerNet research terms. Video under NDA" }
  - { k: Access, v: "Labels and development kit public (SN-Tracking-2023)" }
verdict:
  label: Our read
  text: "The place to learn how often a football tracker loses the ball, and for how long. That number shapes everything downstream."
sources:
  - { title: "Paper (arXiv:2204.06918)", url: "https://arxiv.org/abs/2204.06918" }
  - { title: "Task description", url: "https://www.soccer-net.org/tasks/tracking" }
  - { title: "Development kit", url: "https://github.com/SoccerNet/sn-tracking" }
  - { title: "SN-Tracking-2023 annotations", url: "https://huggingface.co/datasets/SoccerNet/SN-Tracking-2023" }
related:
  - /datasets/soccernet-gsr/
  - /datasets/teamtrack/
  - /datasets/soccersynth-detection/
---

## What it is

Short clips from the main broadcast camera, annotated frame by frame with a bounding box, a class and a track ID for everyone on the pitch and for the ball. It is the reference benchmark for detection and association in football, with all the occlusion and crowding that corners and goalmouth scrambles bring.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct |
| Tracking | Detection and identity association in image space, ball included |
| Events | Nothing |
| Calibration | Nothing. Pair it with a calibration dataset to reach the pitch |

## Where it wins

- **A real ball benchmark.** Small, fast, blurred, hidden behind legs. This is where ball detectors are honestly graded.
- **Crowded scenes.** Set pieces and duels, the moments where possession changes and trackers fail together.
- **A common yardstick.** A public development kit and one evaluation protocol, so results compare.

## What it costs

- **Short clips.** IDs are consistent inside a clip and meaningless across clips.
- **Pixels only.** No pitch coordinates, so no distances in metres.
- **No ownership.** The ball has a box. Nobody is labelled as having it.

## How it plugs into possession

The ball track is the strongest single piece of possession evidence and the least reliable one. This benchmark quantifies the second half of that sentence: missed-detection runs, their length, and the kind of scene they cluster in.

Those run lengths are the right way to stress a possession model. Hide the ball from clean labelled tracking in bursts that look like real detector dropouts, not uniformly at random, and see what the model does. We degraded our own validation data exactly that way.
