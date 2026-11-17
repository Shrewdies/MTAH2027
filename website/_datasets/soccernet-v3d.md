---
title: SoccerNet-v3D
kicker: Detection, calibration and synthetic
summary: "A benchmark that treats a broadcast replay as a second camera: calibrated views of the same moment, and the 3D ball position they pin down."
group: geometry
order: 20
chips: [Broadcast and replays, Camera geometry, 3D ball]
motif: camera
motif_caption: "The live shot and the replays see the same instant from different places. Their rays meet at the ball."
motif_labels: [Main camera, Replay, Behind goal, Reverse]
facts:
  - { k: Modality, v: "Broadcast and replay views with camera calibration and 3D scene annotations" }
  - { k: Task, v: "Camera geometry and 3D ball reconstruction" }
  - { k: Possession labels, v: "None" }
  - { k: Video, v: "Still views of single moments, not continuous matches" }
  - { k: Licence, v: "Public repository. Footage keeps its original SoccerNet terms" }
  - { k: Access, v: "Public GitHub repository with data links" }
verdict:
  label: Our read
  text: "A neat idea with a narrow yield. It will not teach possession, but it is one of the few sources of real 3D ball positions from ordinary television pictures."
sources:
  - { title: "Repository and paper", url: "https://github.com/mguti97/SoccerNet-v3D" }
related:
  - /datasets/ball3d/
  - /datasets/soccernet-calibration/
---

## What it is

Broadcasters show important moments twice: live, and again from another angle. SoccerNet-v3D uses that. With both views calibrated against the pitch, the same instant is seen from two positions, and the scene, the ball above all, can be reconstructed in three dimensions.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct |
| Tracking | Ball position in 3D at isolated instants |
| Events | Nothing |
| Calibration | Camera models and reprojection supervision across views |

## Where it wins

- **Height from broadcast.** No stadium rig, no special cameras. The second view comes free with the production.
- **Geometry you can check.** Reprojection error across two views is a hard test of a calibration.
- **Monocular supervision.** 3D labels to train single-view ball-height estimators against.

## What it costs

- **Moments, not sequences.** No continuous trajectory, no match clock.
- **Replay bias.** Replays show shots, fouls and goals. Ordinary open play is under-represented.
- **Separate rights.** The repository is public; the footage keeps its own terms.

## How it plugs into possession

Height is the dimension possession models most often ignore. In 2D, a goal kick passes "within 1.5 m" of several players on its way down the pitch. None of them can play it. A model that knows the ball is eight metres up does not hand it to the player underneath.

Tracking feeds rarely carry reliable ball height, so the practical lesson is defensive: treat fast, long, straight ball movement as flight, and do not let proximity during flight change possession. Datasets like this one are where a height estimator that removes the guesswork would be trained.
