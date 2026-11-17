---
title: "T-DEED and its team-aware variant"
kicker: "Events and replay"
summary: "An event spotter built for temporal precision, extended to say which team acted. The video model whose output is closest to possession evidence."
group: events-and-replay
order: 10
chips: ["Video", "Event spotting", "Open weights", "GPL-3.0"]
motif: spikes
motif_caption: "Each spike is a ball action with a time and a team. Between spikes the model says nothing."
motif_labels: ["Pass", "Tackle", "Free kick"]
facts:
  - { k: "Modality", v: "Broadcast video" }
  - { k: "Output", v: "Timestamped ball actions, with the acting team" }
  - { k: "Evidence", v: "CVPR 2024; 2025 team baseline reports team mAP@1 51.72" }
  - { k: "Code and weights", v: "Code plus a team-action checkpoint from the authors" }
  - { k: "Licence", v: "GPL-3.0" }
verdict: { label: "Our read", text: "The video model whose output looks most like possession evidence. Use it as anchors with error bars, never as a clock." }
sources:
  - { title: "T-DEED: Temporal-Discriminability Enhancer Encoder-Decoder for Precise Event Spotting (official code)", url: "https://github.com/arturxe2/T-DEED" }
  - { title: "bas25-tdeed: team ball-action spotting baseline (2025)", url: "https://github.com/hoangqnguyen/bas25-tdeed" }
related:
  - /solutions/events-and-replay/ball-action-winner/
  - /solutions/events-and-replay/e2e-spot/
  - /solutions/events-and-replay/sn-spotting/
  - /datasets/soccernet-ball-actions/
---
Precise event spotting asks for the exact frame of an action, and that exposes a weakness of ordinary video models. Features of adjacent frames are nearly identical, so the model cannot tell one frame from its neighbours. T-DEED, the Temporal-Discriminability Enhancer Encoder-Decoder, is designed against that. Its encoder-decoder works across several temporal scales, and its layers are built to keep neighbouring frames distinguishable while still gathering context.

SoccerNet's ball-action task later added a requirement: say which team performed each action. The team-aware baseline extends T-DEED to predict action and team jointly, and reports a team mAP@1 of 51.72 on the challenge.

## Where it wins

- Built for tight tolerances. The architecture targets the frame, not the neighbourhood.
- Team attribution is in the output. A pass by one team is direct possession evidence.
- It covers the actions that move possession: passes, tackles, shots, free kicks.
- Code and a team-action checkpoint are public.

## What it costs

- It is scored within one second. At 25 fps that is a 25-frame allowance where possession needs a single frame.
- A team mAP@1 of 51.72 still leaves many actions missed, mistimed or credited to the wrong side.
- It is trained on broadcast footage. A tactical wide shot is a different domain.
- GPL-3.0.
- Events are points in time. Between them the model is silent.

## How it plugs into possession

Team-attributed events are anchors for a possession sequence. A pass by a team at time t means that team had the ball just before t. A decoder can take each spotted event as a strong but time-uncertain emission and fill the frames between.

The timing gap must be modelled, not ignored. Spread each event's evidence over its tolerance window and let precise cues, tracking geometry where it exists, pin the boundary.

The task definitions and the metric come from the [SoccerNet spotting kits]({{ '/solutions/events-and-replay/sn-spotting/' | relative_url }}).
