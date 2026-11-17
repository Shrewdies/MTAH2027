---
title: SoccerNet-GAR
kicker: Broadcast video and game state
summary: "87,939 group activities from all 64 World Cup 2022 matches, each one available twice: as broadcast video and as player and ball tracking for the same moment."
group: broadcast
order: 30
chips: [Video and tracking, 64 matches, NDA]
motif: sync
motif_caption: "The same action twice: once in pixels, once in positions, on one clock."
motif_labels: [Broadcast clip, Tracking window, Same moment]
facts:
  - { k: Modality, v: "Broadcast clips and player and ball tracking windows, synchronised" }
  - { k: Scale, v: "87,939 annotated group activities, 64 matches" }
  - { k: Classes, v: "10 event classes" }
  - { k: Clip formats, v: "16-frame sampled arrays; 144-frame native-rate clips" }
  - { k: Possession labels, v: "None. Event labels only" }
  - { k: Calibration, v: "Tracking in pitch coordinates. No per-video homography" }
  - { k: Licence, v: "SoccerNet NDA" }
  - { k: Access, v: "Hugging Face, approval required" }
verdict:
  label: Our read
  text: "The cleanest experiment in football AI on one question: for a given action, do you need the pixels, or do the positions already tell you?"
sources:
  - { title: "Dataset and branch documentation", url: "https://huggingface.co/datasets/OpenSportsLab/SoccerNet-GAR" }
  - { title: "Paper (arXiv:2511.12606)", url: "https://arxiv.org/abs/2511.12606" }
related:
  - /datasets/gradient-world-cup-2022/
  - /datasets/footpass/
  - /architecture/single-source-of-truth/
---

## What it is

Group activity recognition for football. Each sample is a short window around an event, labelled with one of ten classes, and delivered in two synchronised modalities: the broadcast picture and the tracking of players and ball. The windows come from every match of the 2022 World Cup.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing continuous. Actions, not spells |
| Tracking | Short player and ball windows in pitch coordinates |
| Events | Ten classes of group activity, densely sampled |
| Calibration | Nothing explicit |

## Where it wins

- **True pairing.** Video and tracking of the same match at the same instant. That is rare, and it is the only honest basis for fusing the two.
- **Modality comparison.** The same label can be predicted from pixels, from positions, or from both, on equal terms.
- **Tournament coverage.** All 64 matches, so team and style variety come built in.

## What it costs

- **Short windows.** A clip centred on an action cuts off the build-up and the aftermath, which is where possession changes hands.
- **Class imbalance.** The labels are heavily skewed towards the common actions.
- **Overlap with Gradient.** Same tournament, same matches. Split by match across both datasets or the evaluation leaks.
- **NDA access.** Personal approval, with conditions on retention and sharing.

## How it plugs into possession

It is a probe more than a teacher. Train an action classifier on tracking windows alone and you learn how much of the game's structure is already in the positions. That is the argument for possession inference from tracking: if the trajectories carry the action, they carry who had the ball.

The classes that still need the video point at what tracking loses. Those are the same moments a tracking-only possession model should be least sure of itself.
