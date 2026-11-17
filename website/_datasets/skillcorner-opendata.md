---
title: SkillCorner Open Data
kicker: Frame-level possession
summary: "Ten A-League matches of broadcast-derived tracking with a possession field, phases of play and, crucially, a flag that says which positions were seen and which were extrapolated."
group: possession
order: 30
chips: [Tracking, Possession field, Detected or extrapolated]
motif: ds-mask
icon: tracks
motif_caption: "Inside the camera view a position is detected. Outside it, the position is extrapolated, and the data says so."
motif_labels: [Detected, Extrapolated, Camera view]
facts:
  - { k: Modality, v: "About 10 Hz broadcast-derived player and ball tracking" }
  - { k: Scale, v: "10 A-League Men matches, 2024/25" }
  - { k: Extras, v: "Dynamic events, phases of play, season aggregates, two body-pose examples" }
  - { k: Possession labels, v: "Per-frame possession field. No explicit dead-ball state" }
  - { k: Quality flags, v: "is_detected separates observed from extrapolated positions" }
  - { k: Video, v: "None" }
  - { k: Calibration, v: "Camera-view polygon per frame, no full homography" }
  - { k: Licence, v: "MIT on the repository" }
  - { k: Access, v: "Public GitHub repository" }
verdict:
  label: Our read
  text: "The most honest tracking in the open. It tells you what the camera saw and what the model filled in, which is exactly the distinction a possession decoder needs when the ball goes missing."
sources:
  - { title: "Official repository and schema", url: "https://github.com/SkillCorner/opendata" }
  - { title: "Repository licence", url: "https://github.com/SkillCorner/opendata/blob/master/LICENSE" }
  - { title: "Match index", url: "https://github.com/SkillCorner/opendata/blob/master/data/matches.json" }
related:
  - /datasets/dfl-idsse/
  - /datasets/gradient-world-cup-2022/
  - /architecture/ball-aware-vs-ball-free/
---

## What it is

SkillCorner tracks football from the broadcast feed, and this repository opens a sample of that product: ten A-League Men matches with player and ball positions at about 10 Hz, team and player identifiers, a possession entry per frame, derived dynamic events and phases of play.

The detail that matters is `is_detected`. Broadcast cameras show part of the pitch. SkillCorner extrapolates the rest and says so, per object, per frame.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | A per-frame possession field, plus phases of play as side supervision |
| Tracking | Broadcast-domain tracks with observed and extrapolated positions kept apart |
| Events | Derived dynamic events aligned to the tracking |
| Calibration | The visible pitch area per frame, as a polygon |

## Where it wins

- **It models its own uncertainty.** Observed and inferred positions are separated in the data, not blended.
- **It behaves like automatic tracking.** Gaps, partial views and filled-in players are the normal case, as they are in any feed that was not captured by in-stadium hardware.
- **Phases come free.** Build-up, transition and the rest arrive as labels, useful context for when possession is likely to change.

## What it costs

- **No dead-ball label.** The possession field says who, not whether the ball is alive. A gap between phases is not a stoppage, and treating it as one manufactures dead-ball frames.
- **10 Hz, not 25.** Short touches and quick turnovers sit between samples. Upsampling invents precision that was never measured.
- **Ten matches, one league.** A test bench, not a training corpus.

## How it plugs into possession

Use it to answer one question: what should a model do when the evidence disappears? Automatic tracking loses the ball constantly. In the competition match it is untracked on 41% of graded frames. A decoder has to read a missing ball as no evidence, not as a stoppage.

SkillCorner is the open dataset where that behaviour can be studied with the truth attached: mask on the detection flag, compare possession calls on detected frames against extrapolated ones, and see how far a model's confidence should fall when it is working from inference.
