---
title: SoccerNet Ball Action Spotting
kicker: Events
summary: "Dense, timestamped ball actions on broadcast video: passes, drives, headers, crosses, shots, throw-ins, tackles and ball out of play. The atoms a possession is made of."
group: events
order: 30
chips: [Broadcast video, 12 action classes, Research terms]
motif: changepoint
motif_caption: "Each ball action is a candidate boundary. Possession changes at some of them, never between them."
motif_labels: [Ball actions, Change point, Possession spells]
facts:
  - { k: Modality, v: "Broadcast video with timestamped ball actions" }
  - { k: Classes, v: "12 in recent editions, from pass and drive to tackle and ball out of play" }
  - { k: Possession labels, v: "None. Single timestamps, no spells" }
  - { k: Calibration, v: "None" }
  - { k: Licence, v: "SoccerNet research terms, non-commercial. Video under NDA" }
  - { k: Access, v: "Labels and development kit public" }
verdict:
  label: Our read
  text: "The right granularity for possession. Not goals and cards but passes and touches, the events where the ball actually changes feet."
sources:
  - { title: "Task and coverage", url: "https://www.soccer-net.org/tasks/ball-action-spotting" }
  - { title: "SoccerNet repository and access matrix", url: "https://github.com/SoccerNet/SoccerNet" }
  - { title: "SoccerNet FAQ on rights", url: "https://www.soccer-net.org/faq" }
related:
  - /datasets/footpass/
  - /datasets/soccernet-action-spotting/
  - /solutions/events-and-replay/ball-action-winner/
  - /solutions/events-and-replay/sn-spotting/
---

## What it is

A SoccerNet challenge track that moves action spotting down to the ball. Where the original task labels a few sparse match events, this one timestamps the actions that make up open play, and scores models on finding them to within a tight tolerance.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Candidate change points: every touch that could move the ball between teams |
| Tracking | Nothing |
| Events | Twelve classes of ball action, densely annotated |
| Calibration | Nothing |

## Where it wins

- **Temporal precision.** Tight tolerances force models to localise the touch, not the passage of play.
- **The right classes.** Pass, drive, tackle and ball out are exactly the events a possession spell starts or ends on.
- **Video-native.** It trains detectors that work from the broadcast picture, with no tracking required.

## What it costs

- **No actor.** The label says a pass happened, not which player made it. FOOTPASS adds that.
- **Timestamps, not intervals.** Unlabelled time is not dead ball and not "no possession". Filling it with either label manufactures errors.
- **Gated video.** The footage sits under SoccerNet's non-commercial terms.

## How it plugs into possession

A possession sequence is piecewise constant. It can only change at a touch or when the ball leaves play. A ball-action detector therefore proposes where the boundaries may be, and a decoder decides which of them are real.

That division of labour is sound whatever the input: let fast, local evidence nominate change points, and let a global decode over the half choose among them. In our decoder the nominations come from tracking geometry and tactical tags; the principle is the same.
