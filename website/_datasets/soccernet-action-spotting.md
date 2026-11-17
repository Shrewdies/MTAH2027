---
title: SoccerNet Action Spotting
kicker: Events
summary: "More than 500 complete broadcast matches with 17 classes of timestamped events: fouls, throw-ins, corners, goals. The largest open view of how football stops and restarts."
group: events
order: 40
chips: [Broadcast video, 17 event classes, 500+ matches]
motif: timeline
motif_caption: "A stoppage has a start and a restart. Spotting labels give one instant of each."
motif_labels: [First half, Second half, Stoppage, Restart]
facts:
  - { k: Modality, v: "Match-length broadcast video with timestamped events" }
  - { k: Scale, v: "500+ complete matches" }
  - { k: Classes, v: "17, including foul, throw-in, corner, offside and goal" }
  - { k: Companion labels, v: "Camera shots and replays" }
  - { k: Possession labels, v: "None" }
  - { k: Calibration, v: "None per frame" }
  - { k: Licence, v: "SoccerNet research terms, non-commercial. Video under NDA" }
  - { k: Access, v: "Labels public (SN-Labels). Video by NDA" }
verdict:
  label: Our read
  text: "A dead-ball dataset in disguise. Most of its classes are a stoppage or a restart, which is the third possession state and the one most models get wrong."
sources:
  - { title: "Task description", url: "https://www.soccer-net.org/tasks/action-spotting" }
  - { title: "Label index (SN-Labels)", url: "https://huggingface.co/datasets/SoccerNet/SN-Labels" }
  - { title: "Broadcast video access", url: "https://huggingface.co/datasets/SoccerNet/SoccerNet_raw_HQ" }
  - { title: "SoccerNet FAQ on rights", url: "https://www.soccer-net.org/faq" }
related:
  - /datasets/soccernet-ball-actions/
  - /solutions/events-and-replay/sn-spotting/
  - /architecture/live-dead/
---

## What it is

The task SoccerNet is best known for, in its 17-class SoccerNet-v2 form. Whole broadcast matches, each annotated with the moments that structure a game: the ball going out, throw-ins, fouls and the free kicks that follow, corners, offsides, substitutions, cards, goals. Companion annotations mark camera shots and replays.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | The dead-ball state, by its edges: what stops play and what restarts it |
| Tracking | Nothing |
| Events | Seventeen classes over full matches |
| Calibration | Nothing |

## Where it wins

- **Full matches at scale.** Hundreds of complete games, so the rhythm of stoppages is observed, not sampled.
- **Restart vocabulary.** Throw-in, corner, free kick, kick-off: the events that end a dead ball.
- **Broadcast grammar.** Replay and camera labels teach a model when the picture is not showing live play at all.

## What it costs

- **Instants, not durations.** A foul has a timestamp. When the ball actually went dead, and when it came alive again, is not annotated.
- **Sparse.** Open play is almost unmarked.
- **Rights.** The footage is NDA-gated and non-commercial.

## How it plugs into possession

Dead ball is the state with the least evidence. The ball is often off-screen or untracked, players walk, the camera cuts to a replay. Positions alone say little. Restart events say a lot: a throw-in fixes the moment the ball came back alive and usually which team has it.

That is the role tactical tags play in our decoder. Restart windows are evidence for the dead-ball state before them and for possession after them. This dataset is where a video model can learn to produce the same kind of cue.
