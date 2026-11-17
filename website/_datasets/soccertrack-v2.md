---
title: SoccerTrack v2
kicker: Tracking
summary: "Ten full matches filmed as one panoramic full-pitch view, with pitch-space player tracks, identities and ball actions. The best openly licensed stand-in for a tactical camera."
group: tracking
order: 20
chips: [Full-pitch video, Tracking, CC BY 4.0]
motif: homography
motif_caption: "One panoramic view holds every player for the whole match, and each lands on the pitch plane."
motif_labels: [Panoramic view, Calibrated, Pitch tracks]
facts:
  - { k: Modality, v: "Panoramic full-pitch video, pitch-space player tracks, identities, ball-action labels" }
  - { k: Scale, v: "10 matches, about 15.5 hours" }
  - { k: Level, v: "University football" }
  - { k: Possession labels, v: "None per frame. Ball actions only" }
  - { k: Calibration, v: "Field-aligned labels and calibration" }
  - { k: Licence, v: "CC BY 4.0 for video and annotations, MIT for code" }
  - { k: Access, v: "Hugging Face and Google Drive" }
verdict:
  label: Our read
  text: "If you want to learn what a tactical camera sees, start here. Full matches, every player in shot, and a licence that lets you publish what you build."
sources:
  - { title: "Repository", url: "https://github.com/AtomScott/SoccerTrack-v2" }
  - { title: "Dataset on Hugging Face", url: "https://huggingface.co/datasets/atomscott/soccertrack-v2" }
  - { title: "Paper (arXiv:2508.01802)", url: "https://arxiv.org/abs/2508.01802" }
  - { title: "Data licence", url: "https://github.com/AtomScott/SoccerTrack-v2/blob/main/LICENSE-DATA" }
related:
  - /datasets/teamtrack/
  - /solutions/vision-and-calibration/sportslabkit/
  - /datasets/reference-target-mtah-2027/
---

## What it is

A panoramic camera covers the whole pitch for the whole match. SoccerTrack v2 pairs ten such recordings with player positions on the pitch plane, persistent identities and timestamped ball actions. It is built for game-state reconstruction: from pixels to who is where.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Ball actions as sparse anchors. No spell labels |
| Tracking | Full-match, full-pitch player tracks with identity |
| Events | Ball-action labels on the video clock |
| Calibration | Video aligned to the pitch plane |

## Where it wins

- **Tactical geometry.** A fixed wide view is how analysts watch football and how automatic tracking is usually produced. Broadcast datasets cannot teach it.
- **Long sequences.** Whole matches, not 30-second clips. Identity has to survive a half, not a highlight.
- **A real data licence.** CC BY 4.0 on the video itself is rare in football and removes the usual footage problem.

## What it costs

- **University football.** Spacing, tempo and ball speed differ from the professional game. Detection transfers well; tactical priors less so.
- **A softer ball.** Ball trajectories may be interpolated between annotated actions. Treat the ball as a label derived from events, not as an independent measurement.
- **No possession truth.** Actions mark touches. The spells between them are yours to infer.

## How it plugs into possession

Possession from tracking stands on two legs: knowing where the players are, and knowing where the ball is. SoccerTrack v2 trains and tests the first leg in the camera geometry that matters.

It also lets you measure what tracking noise does downstream. Run a detector and tracker on the video, compare with the provided tracks, and you have a realistic error model for player positions: the same kind of error a possession decoder must absorb when it is handed automatic tracking.
