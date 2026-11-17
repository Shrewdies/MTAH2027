---
title: "Pitch control"
kicker: "Physics and features"
summary: "Who would reach each point of the pitch first. The physical model behind most spatial football analytics, in its reference tutorial code and a fast implementation."
group: physics-and-features
order: 10
chips: ["Tracking", "Physics", "No training", "MIT"]
motif: field
motif_caption: "Arrival times divide the pitch into territory each team would win if the ball landed there."
motif_labels: ["Home control", "Away control"]
facts:
  - { k: "Modality", v: "Tracking with player velocities" }
  - { k: "Output", v: "Control probability per pitch location; time to intercept" }
  - { k: "Evidence", v: "Friends of Tracking tutorials on Metrica sample matches" }
  - { k: "Code and weights", v: "Notebooks and source; a fast library checked against them" }
  - { k: "Licence", v: "MIT (both repositories)" }
verdict: { label: "Our read", text: "The best physical upgrade to distance-to-ball. Evaluate it where the ball is or will be. A full control surface is analysis, not possession evidence." }
sources:
  - { title: "LaurieOnTracking: Friends of Tracking tutorial code for Metrica tracking data", url: "https://github.com/Friends-of-Tracking-Data-FoTD/LaurieOnTracking" }
  - { title: "pitch-control: a high-performance library for modelling pitch control", url: "https://github.com/mkh1991/pitch-control" }
related:
  - /solutions/physics-and-features/accessible-space/
  - /solutions/direct-possession/metrica-baseline/
  - /solutions/physics-and-features/ball-trajectory-kalman/
  - /datasets/metrica-sample-data/
---
Pitch control answers a counterfactual: if the ball arrived at this spot now, which team would win it? The model in Laurie Shaw's Friends of Tracking code is physical. Each player has a position, a velocity, a reaction time and a top speed. From those the model computes his time to intercept any target point, then turns arrival times into a probability that each team controls the ball there, allowing for the ball's own travel time.

Evaluate that over a grid and the pitch divides into territories. Evaluate it at one point, the ball's landing spot, and you have the odds of a pass being completed.

LaurieOnTracking is the reference implementation: readable notebooks built on Metrica's public sample matches, and the place many analysts first met tracking data. The `pitch-control` library is the same physics made fast, and it checks its numbers against the tutorial code.

## Where it wins

- Physically grounded. Its parameters are speeds and reaction times, not weights.
- No labels, no training, fully deterministic.
- It converts raw positions into the quantity football people argue about: space.
- The time-to-intercept primitive is reusable on its own for passes, loose balls and pressing.

## What it costs

- Controlling space is not having the ball. A centre-back controls the area behind him all match and may never touch it there.
- Velocities must be estimated from positions, and noisy tracking gives noisy velocities.
- A full-pitch grid on every frame is the expensive way to use it. The fast library exists for that reason.
- Player parameters are global. Real top speeds differ.

## How it plugs into possession

Use it at the ball, not across the pitch. For possession the valuable number is local: time to intercept for the nearest players of each team at the ball's position, or along its path when it is in flight. That turns "who is closest" into "who gets there first". A sprinting presser and a standing receiver are judged correctly, where raw distance gets them wrong.

During flight it does something distance cannot do at all. Projecting the ball forward and asking who controls the arrival point predicts the next possessor before the reception happens. For a decoder that is a prior, and it should be weighted like one.

[Accessible space]({{ '/solutions/physics-and-features/accessible-space/' | relative_url }}) extends the same physics to the pass itself. The sample matches the tutorials run on are [Metrica Sports sample data]({{ '/datasets/metrica-sample-data/' | relative_url }}).
