---
title: "FOOTPASS baselines"
kicker: "Events and replay"
summary: "Player-centric ball-action spotting: not only what happened and when, but which player did it, using tracks, a graph over players and a denoising sequence model."
group: events-and-replay
order: 40
chips: ["Video + tracks", "Player-level events", "Identity-dependent", "Apache-2.0 code"]
motif: graph
motif_caption: "Actions are attached to players. Relations between players and the grammar of play clean up the stream."
motif_labels: ["Passer", "Action: pass", "Receiver"]
facts:
  - { k: "Modality", v: "Broadcast video with player tracks" }
  - { k: "Output", v: "Actions attributed to individual players" }
  - { k: "Evidence", v: "Baselines for SoccerNet's 2026 player-centric challenge" }
  - { k: "Code and weights", v: "Training and inference code" }
  - { k: "Licence", v: "Apache-2.0 code; data and models may be non-commercial" }
verdict: { label: "Our read", text: "Where event spotting is going: actions with names attached. It needs identities, and it shows what they are worth." }
sources:
  - { title: "FOOTPASS: baselines for the SoccerNet Player-Centric Ball-Action Spotting Challenge 2026 (code)", url: "https://github.com/JeremieOchin/FOOTPASS" }
related:
  - /solutions/events-and-replay/team-tdeed/
  - /solutions/vision-and-calibration/soccernet-reid/
  - /solutions/classifiers-and-decoders/graph-network-toolkits/
  - /datasets/footpass/
---
Event spotting says a pass happened at 12:31. These models say who played it. They are the reference baselines of SoccerNet's 2026 player-centric ball-action challenge, built on the [FOOTPASS dataset]({{ '/datasets/footpass/' | relative_url }}), where each action has to be assigned to a specific player. That is the form event data takes when providers sell it.

The baselines combine three views of the game. Track-aware action detection looks at each tracked player and scores what he is doing. A graph network relates players to one another, since a pass has a sender and a receiver. A sequence model then reads the resulting stream of candidate actions and denoises it using tactical regularity. Play-by-play football has a grammar: a reception follows a pass.

## Where it wins

- Player-level attribution, the granularity of commercial event data.
- It uses the structure of play itself as a prior, not only pixels.
- It combines video and tracking-style inputs in one model.
- The code is Apache-2.0.

## What it costs

- It needs to know who is who. Attribution to players presumes reliable identities, and wrong identities corrupt the output directly.
- A deep stack of trained components, with the data and compute that implies.
- Data and model resources may be non-commercial even though the code is not.
- Player actions are not team possession labels. A mapping step remains.

## How it plugs into possession

A player-attributed action stream is nearly a possession sequence already. Each action names the player on the ball, and his team follows. Where identities exist, output of this kind is the richest event evidence a possession decoder can receive.

Its denoising stage is the same idea as sequence decoding, learned: use what football allows to correct what the detector saw. The difference is the unit. Here it is actions. In a possession decoder it is frames.

The Initial Challenge feed carries a team and no identity, so team-level evidence and a team-level decode fit it as it is: [Players without names]({{ '/architecture/player-identities/' | relative_url }}).
