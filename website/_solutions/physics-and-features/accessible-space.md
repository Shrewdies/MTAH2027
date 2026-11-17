---
title: "Accessible space (DAS)"
kicker: "Physics and features"
summary: "A physical pass model that asks where the team on the ball can actually play to, and how dangerous that space is."
group: physics-and-features
order: 20
chips: ["Tracking", "Physics", "Needs possession", "MIT"]
motif: field
motif_caption: "Space is accessible where a pass would arrive before a defender can cut it out."
motif_labels: ["Accessible space", "Defended space"]
facts:
  - { k: "Modality", v: "Tracking; events optional" }
  - { k: "Output", v: "Pass completion; accessible and dangerous space per team" }
  - { k: "Evidence", v: "Published research; maintained package with examples" }
  - { k: "Code and weights", v: "Python package; physics only, no trained weights" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The most complete open physical pass model. Strong on the ball in flight, and built to be told who has it." }
sources:
  - { title: "accessible-space: repository and Python package", url: "https://github.com/jonas-bischofberger/accessible-space" }
related:
  - /solutions/physics-and-features/pitch-control/
  - /solutions/direct-possession/defcon/
  - /solutions/physics-and-features/ball-trajectory-kalman/
---
Accessible space is [pitch control]({{ '/solutions/physics-and-features/pitch-control/' | relative_url }}) with the ball's physics put back in. Instead of asking who reaches a point first, it simulates passes. The ball leaves the passer at a given angle and speed, travels, and at every moment each player has some chance of intercepting it. Integrate that along the path and you have the probability that a pass into each area is completed.

Two aggregates come out. Accessible space is the area a team can reach by pass. Dangerous accessible space, DAS, weights that area by threat and gives one number for how much dangerous room the team on the ball has. The same machinery yields expected pass completion for any real pass.

The package exposes these as functions over tracking dataframes.

## Where it wins

- It models the pass, not only the destination. Interception along the lane is where plain pitch control is weakest.
- Physical and interpretable, with no trained weights to ship.
- Outputs are per team, so they aggregate directly into team-level measures.
- MIT, installable, with football examples.

## What it costs

- Several interfaces need to be told which team has the ball, or that a pass is under way. For possession inference that is the unknown.
- Simulating a fan of passes on every frame costs far more than a distance check.
- It needs trustworthy player velocities and a ball position to pass from.

## How it plugs into possession

There are two sound uses. First, pass completion as flight evidence. When the ball is travelling, the interception model says which team is likelier to control it next. Second, as a consumer. Once possession is known, DAS turns each H or A stretch into a measure of how much the team did with it.

The use to avoid is feeding possession-conditioned outputs back in as possession evidence. Compute it for both teams symmetrically, or keep it downstream.
