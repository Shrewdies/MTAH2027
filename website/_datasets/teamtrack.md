---
title: TeamTrack
kicker: Tracking
summary: "A full-pitch multi-object tracking benchmark in 4K to 8K, with millions of annotated player boxes from side and top cameras. Built to break trackers on identity."
group: tracking
order: 30
chips: [Full-pitch video, Player boxes, Track IDs]
motif: tracks
motif_caption: "Twenty-two similar shapes, small in frame, crossing constantly. Identity is the whole test."
motif_labels: [Track ID, Identity trail]
facts:
  - { k: Modality, v: "4K to 8K full-pitch video, bounding boxes, track IDs" }
  - { k: Scale, v: "Millions of annotated player boxes" }
  - { k: Sports, v: "Football among several team sports" }
  - { k: Views, v: "Side and top cameras" }
  - { k: Pitch coordinates, v: "Trajectory version for fixed side-view scenes" }
  - { k: Possession labels, v: "None" }
  - { k: Licence, v: "MIT for code. Data terms on the dataset page" }
  - { k: Access, v: "GitHub, with Google Drive and Kaggle downloads" }
verdict:
  label: Our read
  text: "A tracker's stress test. It says nothing about the ball, and everything about whether a player keeps the same ID through a crowded penalty area."
sources:
  - { title: "Repository, dataset and preprint", url: "https://github.com/AtomScott/TeamTrack" }
  - { title: "Project page", url: "https://atomscott.github.io/TeamTrack/" }
related:
  - /datasets/soccertrack-v2/
  - /solutions/vision-and-calibration/sportslabkit/
  - /architecture/player-identities/
---

## What it is

Wide-angle recordings of team sports, annotated with a box and a persistent ID for every player in every frame. The football subset uses side and top views that hold the full pitch. Players are small in frame, look alike and cross constantly.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct |
| Tracking | Dense player boxes with identity, at full-pitch scale |
| Events | Nothing |
| Calibration | Pitch-plane trajectories for the fixed side-view scenes |

## Where it wins

- **Small-object tracking.** Full-pitch resolution is where broadcast-trained detectors fall over.
- **Identity under pressure.** Uniform kits and constant occlusion make it a hard association benchmark.
- **Volume.** Enough boxes to pretrain a wide-view detector properly.

## What it costs

- **Players only.** No reliable ball, so no possession signal.
- **Mixed sports and cameras.** Keep the football split separate. Other sports' spacing teaches a football tracker little.
- **Pixels first.** Pitch coordinates exist only for some scenes.

## How it plugs into possession

Indirectly, and it still matters. Team possession needs the team of the nearest player, not the name. But every ID switch between opponents flips that team label for a few frames, and a possession model reads the flip as a turnover.

TeamTrack is where you measure how often that happens. The lesson carries straight into decoder design: a single-frame change of the nearest player's team should never be enough to change possession.
