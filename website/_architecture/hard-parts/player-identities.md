---
title: Players without names
kicker: The hard parts
summary: "Tracking slots are not players. A slot can change bodies mid-move and no football has happened. Design around identity, or repair it. Never trust it by default."
group: hard-parts
order: 30
chips: [Tracking slots, Set features, Re-identification]
motif: bp-slots
icon: tracks
motif_caption: "Two team-mates cross and leave with each other's numbers. A feature read by slot jumps at the swap. The same feature read by team does not move."
facts:
  - { k: Given, v: "A team for every player, no stable identity" }
  - { k: Invariant route, v: "Features that ignore slot order" }
  - { k: Repair route, v: "Link tracklets by motion and appearance" }
  - { k: Trap, v: "Reading a slot change as an event" }
verdict:
  label: Our read
  text: "Team possession is a team-level question. Answer it with identity-free evidence, and spend repair effort only when a player-level model needs it."
call:
  title: Why we reason about teams
  constraint: Data reality
  text: "Players arrive with a team and no identity. Possession is scored per team, so every evidence feature is identity-invariant: which side has a player within reach of the ball, how still the players are. Nothing in the pipeline depends on a slot staying the same person, and renumbering the slots cannot change the output."
sources:
  - { title: "Zaheer et al. (2017), Deep Sets", url: "https://arxiv.org/abs/1703.06114" }
  - { title: "Lee et al. (2019), Set Transformer", url: "https://arxiv.org/abs/1810.00825" }
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "SoccerNet Re-Identification", url: "https://github.com/SoccerNet/sn-reid" }
related:
  - /architecture/the-shrewdies-decoder/
  - /architecture/single-source-of-truth/
  - /challenges/tactical-tracking/
  - /solutions/classifiers-and-decoders/set-encoders/
  - /solutions/vision-and-calibration/soccernet-reid/
  - /solutions/direct-possession/pathcrf/
---

## The design question

What should a possession model do when the data cannot say who a player is? Automatic tracking assigns
slots. A slot is neither a stable physical identity nor a shirt number, and an apparent change of slot is
not a football event.

## The options

| Route | Evidence it uses | Wins | Costs |
|---|---|---|---|
| Identity-invariant | Nearest-player distances per team, sorted speeds, occupancy near the ball, team shape | Unaffected by renumbering | No player-level story |
| Set and graph encoders | Deep Sets, Set Transformer over unordered players | Learns interactions, order-free | Needs labelled matches |
| Identity repair | Motion continuity, feasible speed, Kalman prediction, one-to-one assignment | Enables player-level paths | Errors compound through a match |
| Appearance re-identification | Visual embeddings from video | Recovers after long occlusion | Needs video; similar kits confuse it |
| Role priors | Formation slots as soft hints | Cheap, tactical | Roles are not people |

Roles do not rescue identity. Full-backs invert, midfielders interchange, wingers swap flanks, and every
set piece dissolves the shape. Shirt numbers live in the pixels, not in the coordinates, and bringing them
across is one of the gaps [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }})
is built to fill.

## Repair, or never need it

{% include wiki/motif.html id="bp-s-fragments" caption="One player through one crowded box. The tracker delivers five fragments under five numbers. The repair route has to make four links, and one wrong link turns every later frame into another player. The invariant route never needed the links." %}

## What else breaks it in real football

- **A substitution.** A new body takes over a slot with a different job.
- **A slot change read as a pass.** A player-level model sees the ball "move" between two identities that
  are the same person.

## How to judge it

Run the permutation test: shuffle the slot labels within each team, on every frame, and re-run. An
identity-invariant design returns the same output. For repair, fragment clean tracks on purpose and
measure how possession accuracy degrades as the fragments get shorter.
