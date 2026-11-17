---
title: Spiideo SoccerNet SynLoc
kicker: Detection, calibration and synthetic
summary: "A localisation benchmark built from synthetic images with exact answers: find every player in a wide-angle frame and say where they stand on the pitch, in metres."
group: geometry
order: 40
chips: [Synthetic images, World coordinates, Single frame]
motif: ds-ground
icon: homography
motif_caption: "Every player gets a ground point, and the answer is scored in metres, not pixels."
motif_labels: [Player, Position in metres]
facts:
  - { k: Modality, v: "Synthetic and real images with player positions in world coordinates" }
  - { k: Task, v: "Single-frame athlete localisation, image to world" }
  - { k: Possession labels, v: "None" }
  - { k: Video, v: "Images, not sequences" }
  - { k: Licence, v: "Set by Spiideo on the dataset host" }
  - { k: Access, v: "Public development kit with data links" }
  - { k: Paper, v: "VISAPP 2025" }
verdict:
  label: Our read
  text: "Synthetic data used for the one thing it is unbeatable at: exact ground truth for geometry. A detector that is scored in metres learns the right habits."
sources:
  - { title: "Development kit and data links (sskit)", url: "https://github.com/Spiideo/sskit" }
  - { title: "Paper reference (VISAPP 2025)", url: "https://github.com/Spiideo/sskit#spiideo-soccernet-synloc" }
related:
  - /datasets/soccernet-calibration/
  - /datasets/soccersynth-detection/
  - /datasets/soccernet-gsr/
---

## What it is

Spiideo makes automated wide-angle camera systems for football. SynLoc is the localisation benchmark it contributes to SoccerNet: rendered scenes where each player's true position on the pitch is known exactly, and a task that asks for those positions directly from a single image.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct |
| Tracking | Per-frame player positions on the pitch, no identity over time |
| Events | Nothing |
| Calibration | Camera-aware localisation: the projection is part of the problem |

## Where it wins

- **Exact labels.** A renderer knows where every foot touches the ground. Human annotation of real footage never does.
- **The right metric.** Scoring in world coordinates rewards the output a tracking pipeline actually needs.
- **Controlled variation.** Cameras, stadiums and conditions can be varied systematically.

## What it costs

- **The sim-to-real gap.** Rendered players are cleaner than real ones. Validation on real footage is not optional.
- **No time.** Single frames. No tracks, no ball ownership, no events.
- **Players only.** It localises people, not the ball.

## How it plugs into possession

It attacks the same quantity Alfheim measures: position error in metres. A box that is two pixels off at the far touchline of a wide-angle view is a metre off on the grass. Training a detector against world-coordinate truth shrinks that error at the source.

For possession, the gain is at the margins that decide it: which of two close players is nearer the ball, and whether anyone is within playing distance at all.
