---
title: "DEFCON"
kicker: "Direct possession"
summary: "Graph neural networks that credit defenders for what they prevent. Possession is its input, not its output, which is exactly why it belongs on the map."
group: direct-possession
order: 60
chips: ["Tracking", "Graph", "Learned", "Needs possession"]
motif: field
motif_caption: "A defender's value is the attacking option his position takes away."
motif_labels: ["Attacking options", "Defensive cover"]
facts:
  - { k: "Modality", v: "Tracking, with possession known" }
  - { k: "Output", v: "Contribution value per defender" }
  - { k: "Evidence", v: "MIT Sloan Sports Analytics Conference 2026" }
  - { k: "Code and weights", v: "Training code; no trained model published" }
  - { k: "Licence", v: "None declared in the repository" }
verdict: { label: "Our read", text: "A consumer of possession, not a source of it. Read it to see what a clean H/A/D signal unlocks." }
sources:
  - { title: "DEFCON repository: Better Prevent than Tackle, Valuing Defense in Soccer Based on Graph Neural Networks (SSAC 2026)", url: "https://github.com/hyunsungkim-ds/defcon" }
related:
  - /solutions/direct-possession/match-phase-segmentation/
  - /solutions/physics-and-features/accessible-space/
  - /solutions/physics-and-features/unravelsports/
---
Defending is the hardest thing in football to count, because good defending is the pass that was never played. DEFCON ("Better Prevent than Tackle", Sloan 2026) values it anyway. Graph neural networks estimate what the team in possession could do next and what each option is worth. A defender is credited for the value his positioning removes, not only for tackles and interceptions.

The graph is the natural form. Players are nodes. Relations between the player on the ball, his options and the defenders are edges. The network learns how one defender's position changes what the attack can do.

## Where it wins

- It measures prevention, which event counts cannot see.
- Graph structure handles the many-to-many nature of defending without hand-built features.
- Training code is public, from the lead author of [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}).

## What it costs

- It consumes possession. Every value is conditional on knowing which team, and which player, has the ball.
- It was trained on data that is not public, and no trained model is released.
- The repository declares no licence.
- The target is value. There is no direct comparison with frame-level possession labels.

## How it plugs into possession

Downstream. DEFCON is a consumer of the possession signal, and a demanding one. An error in who has the ball turns attackers into defenders and inverts every credit.

That makes it a good measure of why possession inference matters. Per-frame H/A/D is not the product. It is the layer every valuation model stands on.

Its pressure and lane features could also run upstream as evidence, since a team being pressed is usually the team with the ball. That cue is weak, and circular if the model was trained with possession as an input.
