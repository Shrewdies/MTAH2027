---
title: FOOTPASS
kicker: Broadcast video and game state
summary: "54 full professional matches with 102,992 ball actions, each one anchored to the player who made it. The densest open record of who touched the ball, and when."
group: broadcast
order: 40
chips: [Broadcast video, Actor-linked actions, CC BY-NC 4.0]
motif: graph
motif_caption: "Every action has an actor. Chain the actors and a possession appears."
motif_labels: [Passer, Ball action, Receiver]
facts:
  - { k: Modality, v: "Full-length broadcast video, pixel tracklets, velocities, team IDs, jersey numbers, roles" }
  - { k: Scale, v: "54 full matches, 102,992 ball-action events" }
  - { k: Competition, v: "European professional football, 2023-24" }
  - { k: Labels, v: "Ball actions anchored to a frame and a player" }
  - { k: Possession labels, v: "None per frame" }
  - { k: Calibration, v: "None. Tracking is in pixel space" }
  - { k: Licence, v: "CC BY-NC 4.0 for annotations and baselines. Video under NDA" }
  - { k: Access, v: "Gated through SoccerNet (SN-PCBAS-2026)" }
verdict:
  label: Our read
  text: "The closest thing to possession without being possession. About 1,900 actor-linked ball actions per match is a touch-by-touch account of the game. What it lacks is the silence between touches."
sources:
  - { title: "Implementation and publication", url: "https://github.com/JeremieOchin/FOOTPASS" }
  - { title: "Data card (gated)", url: "https://huggingface.co/datasets/SoccerNet/SN-PCBAS-2026" }
  - { title: "Journal paper (2026)", url: "https://doi.org/10.1016/j.cviu.2026.104790" }
related:
  - /datasets/soccernet-ball-actions/
  - /datasets/soccernet-gar/
  - /solutions/events-and-replay/footpass/
  - /architecture/events-and-control/
---

## What it is

FOOTPASS is the dataset behind SoccerNet's player-centric ball-action spotting challenge. Ordinary action spotting asks when something happened. FOOTPASS asks who did it: every pass, drive, shot or tackle is tied to a frame and to a specific tracked player, with that player's team, jersey number and role.

The matches are complete broadcasts, not clips, so actions come in their real order and density.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Touch-level ownership: the team of each acting player |
| Tracking | Pixel-space tracklets with velocity, team and jersey number |
| Events | 102,992 ball actions with an actor each |
| Calibration | Nothing |

## Where it wins

- **Actor linkage.** An action with a player attached is one inference away from an action with a team attached.
- **Full-match continuity.** Sequences of touches, not isolated events. Chains of passes are visible as chains.
- **Density.** Roughly 1,900 actions per match, far denser than classic event spotting.

## What it costs

- **Touches are not spells.** Nothing marks the ball going dead, a loose ball, or how long a team holds it between actions.
- **Broadcast view.** Off-camera players are not tracked, and the pitch position of an action has to be estimated.
- **Non-commercial.** Annotations are CC BY-NC 4.0 and the video is NDA-gated.

## How it plugs into possession

Turn it into a possession skeleton. Consecutive actions by players of the same team belong to one spell; a change of acting team marks a turnover somewhere between two timestamps. That gives boundaries with known uncertainty, the kind of weak label a sequence model can be pretrained on or audited against.

The other use is as a touch detector's training set. A decoder that receives "player 8, home, touched the ball here" has far stronger evidence than "a home player was nearest". Reception and touch are the events that should be allowed to change possession; proximity alone should not.

The models that spot these actions and attribute them to players are covered under [FOOTPASS baselines]({{ '/solutions/events-and-replay/footpass/' | relative_url }}).
