---
title: ball3d
kicker: Detection, calibration and synthetic
summary: "A physics-based 3D ball benchmark: a full professional match seen by one broadcast and six static cameras, with triangulated ball trajectories, calibration and ball-out signals."
group: geometry
order: 30
chips: [Multi-view video, 3D ball, CC BY-NC-SA 4.0]
motif: trajectory
motif_caption: "A ball in flight obeys physics. Fit the arc and the gaps between detections fill themselves in."
motif_labels: [Detected, Ballistic fit, Uncertainty]
facts:
  - { k: Modality, v: "Broadcast and static multi-camera video, ball detections, 3D trajectory segments, calibration" }
  - { k: Scale, v: "One 94-minute professional match from seven views, panoramic training drills, ISSIA-3D" }
  - { k: Signals, v: "Per-frame homographies, ball-out and pause flags" }
  - { k: Possession labels, v: "None" }
  - { k: Venue, v: "CVPR Workshops 2026" }
  - { k: Licence, v: "CC BY-NC-SA 4.0 for annotations and code. Video for non-commercial research, no redistribution" }
  - { k: Access, v: "GitHub repository with Google Drive data, academic research" }
verdict:
  label: Our read
  text: "The most complete open resource on the hardest object in football. Real match, real cameras, real 3D ball. Small, and worth every frame."
sources:
  - { title: "Repository", url: "https://github.com/lukaszgrad/ball3d" }
  - { title: "Data and licence specification", url: "https://github.com/lukaszgrad/ball3d/blob/main/DATA.md" }
  - { title: "CVPR Workshops 2026 paper", url: "https://github.com/lukaszgrad/ball3d#citation" }
related:
  - /datasets/soccernet-v3d/
  - /datasets/soccernet-tracking/
  - /datasets/soccernet-calibration/
---

## What it is

Three sets in one release. The centrepiece is a complete professional match recorded by the broadcast camera and six static cameras, with the ball triangulated in 3D. Alongside it are panoramic recordings of training drills, and ISSIA-3D.

Everything is calibrated, and the release includes the signals a tracker needs around the trajectory: ball detections per view, homographies per frame, and flags for ball out of play and pauses.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct. Ball-out and pause flags mark dead-ball candidates |
| Tracking | The ball in 3D, with per-view detections |
| Events | Nothing |
| Calibration | Calibrated cameras and a homography per frame |

## Where it wins

- **A measured ball height.** Triangulated from several views, not guessed from one.
- **Broadcast and static together.** The same match from the television camera and from fixed positions, so a broadcast method can be graded against multi-view truth.
- **Physics as a prior.** Flight segments follow ballistic arcs. A model that knows this can bridge missed detections instead of losing the ball.

## What it costs

- **One match at its core.** One stadium, one lighting condition, one set of kits.
- **Non-commercial, share-alike.** The licence travels with anything derived from the annotations.
- **Mind the matrix.** The homographies map image to pitch. Other providers ship pitch to image. Check the direction before composing transforms.

## The ISSIA lineage

ISSIA is the classic multi-camera football benchmark: six synchronised static cameras, a short sequence, manually annotated players and ball, and reference points for calibration. It is the historical public test for triangulation and tracking across views.

ball3d brings it up to date as ISSIA-3D, with derived annotations for the six views. The original video is not part of the release and keeps its own terms.

## How it plugs into possession

When the ball is missing from tracking, there are two honest options. Say nothing, or predict where it went. Prediction needs a motion model, and this is the dataset where a ball motion model can be fitted and tested against truth: how far a pass travels between detections, how long a clearance hangs, where a bounce lands.

A possession decoder benefits even without reconstructing anything. Knowing typical flight times turns "ball unseen for two seconds" from a blank into a constraint: the ball is in the air, and nobody new has it yet.
