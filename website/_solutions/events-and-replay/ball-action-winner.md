---
title: "Ball-action spotting, 2023 winning solution"
kicker: "Events and replay"
summary: "The first-place entry of SoccerNet's 2023 ball-action challenge: frames through a 2D encoder, then 3D convolutions, to spot passes and drives."
group: events-and-replay
order: 20
chips: ["Video", "Event spotting", "Open weights", "MIT"]
motif: stack
motif_caption: "A 2D encoder reads the frames, 3D convolutions add time, and the head scores pass or drive."
motif_labels: ["Frames", "2D encoder", "3D convolutions", "Pass or drive"]
facts:
  - { k: "Modality", v: "Broadcast video" }
  - { k: "Output", v: "Timestamped pass and drive events with scores" }
  - { k: "Evidence", v: "1st place, SoccerNet 2023; author-reported mAP@1 86.47" }
  - { k: "Code and weights", v: "Working code and trained models" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "Simple, strong and MIT. The event spotter to reach for first, as long as two classes and no team labels are enough." }
sources:
  - { title: "ball-action-spotting: first-place solution for the SoccerNet Ball Action Spotting Challenge 2023 (code and models)", url: "https://github.com/lRomul/ball-action-spotting" }
related:
  - /solutions/events-and-replay/team-tdeed/
  - /solutions/events-and-replay/e2e-spot/
  - /solutions/events-and-replay/sn-spotting/
  - /datasets/soccernet-ball-actions/
---
In 2023 SoccerNet introduced ball-action spotting with the two actions that make up most of football: the pass and the drive, a player carrying the ball. This solution won the challenge, and its author published the code and the trained models.

The architecture is deliberately economical. Frames pass through an EfficientNetV2 2D encoder. Temporal 3D convolutions then model how the features change over time, and a head scores the actions. The author reports mAP@1 of 86.47.

## Where it wins

- Pass and drive are the two actions that define who has the ball. A drive is possession by definition.
- High precision at one-second tolerance on its benchmark.
- MIT licence with trained models: the most reusable event spotter in this family.
- A compact design: one 2D backbone and a temporal 3D stage.

## What it costs

- Two classes. No tackles, shots, out-of-play or set pieces.
- No team attribution. It says a pass happened, not who played it.
- It is trained on the challenge's broadcast footage. Other cameras are out of distribution.
- The tolerance is one second again.

## How it plugs into possession

Drives are the underrated signal. Spotters are usually mined for passes, but a detected drive says a player is in controlled possession now, for as long as it lasts. That is dense evidence from an event model, and it complements tracking exactly where a ball track is missing.

Without team labels the events need a partner: a tracking feed or a team classifier to say which side the acting player is on. With that, pass and drive detections become H or A evidence for a decoder. The [team-aware T-DEED]({{ '/solutions/events-and-replay/team-tdeed/' | relative_url }}) predicts the side itself.
