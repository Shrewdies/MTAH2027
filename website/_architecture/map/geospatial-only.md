---
title: Geospatial-only inference
kicker: The map
summary: "Possession from coordinates alone: player and ball positions, speeds and tactical tags. No pixels at inference. The question is which reasoning to put on top."
group: map
order: 20
chips: [Tracking, Tags, Laptop CPU, Fielded]
motif: bp-geo
icon: field
motif_caption: "What coordinates can testify to without a single pixel: who can play the ball, whether it left the pitch, whether play has stopped, whether the ball is travelling. Each fact names the state it supports."
facts:
  - { k: Inputs, v: "Tracking coordinates and tactical tags" }
  - { k: Evidence, v: "Reach, speed, out of play, stillness" }
  - { k: Compute, v: "CPU, seconds per match" }
  - { k: Weak spot, v: "Frames where the ball is untracked" }
verdict:
  label: Our read
  text: "The right first architecture whenever tracking exists. Physics that can be audited beats pixels that must first be calibrated, provided the design has an answer for the frames with no ball."
call:
  title: Why coordinates carried the match
  constraint: Competition rules, time and reproducibility
  text: "Match data could not go to hosted or cloud compute, the window was a matter of days, and the organisers regenerate the exact file. Coordinates and tags decode on one laptop CPU in under ten seconds with byte-identical output, so the evidence stayed geospatial."
sources:
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "LaurieOnTracking: tracking-data tutorials and pitch control", url: "https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking" }
  - { title: "floodlight: sports data analysis framework", url: "https://github.com/floodlight-sports/floodlight" }
  - { title: "LightGBM", url: "https://github.com/lightgbm-org/LightGBM" }
related:
  - /architecture/the-shrewdies-decoder/
  - /architecture/ball-aware-vs-ball-free/
  - /architecture/player-identities/
  - /challenges/tactical-tracking/
  - /solutions/physics-and-features/pitch-control/
  - /solutions/classifiers-and-decoders/gradient-boosted-trees/
---

## The design question

How much of possession can be read from coordinates alone? A tracking feed is already spatially
normalised: every player and the ball on one pitch, in metres, 25 times a second. No calibration, no
synchronisation. What remains to choose is the reasoning on top.

## The options

| Variant | Mechanism | Wins | Costs |
|---|---|---|---|
| Nearest player | Distance to the ball | Simple, readable | A touch is not control |
| Kinematic rules | Reach, closing speed, change of trajectory | Direct football mechanics | Missing and aerial balls |
| Gradient boosting | Non-linear mix of geometry and time statistics | Strong on tabular features | Time must be hand-encoded |
| Set encoder + TCN | Order-free players across many frames | Survives slot renumbering | Needs labelled matches |
| Graph + temporal encoder | Interactions between players | Pressure and receiver cues | Complexity, track gaps |
| Ball-free path | Possession transfer from player motion | Works with no ball at all | Leans on trajectory quality |

The first two need no labels. The last four learn, so they inherit the label problem set out in
[Evidence, then a decoder]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}).

## Four states, kept distinct

Estimated proximity, possible contact, controlled possession, and whether the ball is alive at all. A
design that lets the first stand in for the third has rebuilt the nearest-player baseline. The exact
signals and thresholds we fielded are listed in
[The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).

## What the plane cannot see

{% include wiki/motif.html id="bp-s-height" caption="The same lofted pass, twice. From the side it clears the defender. On the ground plane it passes through his reach, and reads as evidence for the wrong team." %}

## What else breaks it in real football

- **An interpolated path is a guess.** A line drawn through a tracking gap is a hypothesis and is flagged as one.
- **The ball disappears where it matters.** That problem has its own study:
  [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}).

## How to judge it

Report every metric twice: on frames where the ball is tracked and on frames where it is not. A design
that only wins on the first set has solved the easy half of football.
