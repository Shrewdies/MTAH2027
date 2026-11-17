---
title: Video-only inference
kicker: The map
summary: "Possession from pixels: detect the ball and players, calibrate the pitch, project to the ground, then reason. Independent of any supplied tracking, and expensive at every step."
group: map
order: 30
chips: [Computer vision, Detection, Calibration]
motif: bp-video
icon: boxes
motif_caption: "Five stages between a frame and a point on the pitch, and certainty drains at each. The last step, from a ball position to a possession state, is still open at the end."
facts:
  - { k: Inputs, v: "Tactical or broadcast video" }
  - { k: Stages, v: "Detect, track, calibrate, project, spot" }
  - { k: Wins, v: "Sees contact; recovers what a tracker lost" }
  - { k: Costs, v: "Small objects, calibration, non-live footage" }
verdict:
  label: Our read
  text: "Pixels recover what a tracker lost. They do not decide possession. A perfect detector still needs football semantics and a temporal decision behind it, so video earns its place as a witness, not as the system."
sources:
  - { title: "Roboflow sports: soccer examples", url: "https://github.com/roboflow/sports/tree/main/examples/soccer" }
  - { title: "SoccerNet Game State Reconstruction", url: "https://github.com/SoccerNet/sn-gamestate" }
  - { title: "PnLCalib: points-and-lines pitch calibration", url: "https://github.com/mguti97/PnLCalib" }
  - { title: "T-DEED for team ball action spotting", url: "https://github.com/hoangqnguyen/bas25-tdeed" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/multi-camera-geography/
  - /architecture/match-timeline/
  - /solutions/vision-and-calibration/roboflow-soccer/
  - /solutions/vision-and-calibration/sn-gamestate/
  - /solutions/vision-and-calibration/pnlcalib/
---

## The design question

Can the evidence be rebuilt from the picture instead of trusted from a feed? A video-only design owns its
own perception. That buys independence from someone else's tracker, and pays for it with a chain of
subproblems that each fail on their own.

## The pipeline, stage by stage

| Stage | Must deliver | Where it hurts |
|---|---|---|
| Ball detection | The ball, most frames | A handful of pixels in a tactical view |
| Player and team segmentation | Who is on which side | Similar kits, crowded boxes |
| Identity association | The same player across time | Occlusion, camera cuts |
| Pitch calibration | Lines and keypoints to a camera model | Few landmarks in view |
| Projection | Pixel to pitch coordinate | Valid on the ground plane only |
| Action spotting | Pass, header, tackle, out | Coarse in time |
| Live or replay | Is this the match clock? | Replays, close-ups, crowd shots |

The errors multiply along the chain. A pipeline is never better than the product of its stages.

## What breaks it in real football

{% include wiki/motif.html id="bp-s-tiny" caption="The wide frame holds the whole match in one picture, so the ball is a few bright pixels, and so are a penalty spot and a white boot." %}

- **Detection is not semantics.** A precise ball box says where the ball is. It does not say whether a
  deflection transferred controlled possession.
- **Geometry and time.** The limits of projection and of broadcast timing have their own studies:
  [Space is not time]({{ '/architecture/multi-camera-geography/' | relative_url }}) and
  [One clock for the match]({{ '/architecture/match-timeline/' | relative_url }}).

## Where it belongs

As one witness among three. A recovered ball position on frames where tracking has none, or a foot-to-ball
contact at a closer angle, is one more measurement with its own confidence. How it is reconciled with the
others is [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}).

## How to judge it

Measure each stage against its own ground truth before measuring possession. Ball recall on the frames the
tracker missed is the number that matters. Recall on frames the tracker already has adds nothing.
