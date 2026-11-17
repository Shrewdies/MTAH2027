---
title: Alive or dead, then who
kicker: The hard parts
summary: "Whether the ball is in play and which team controls it are two different football facts. Designs that answer them with one mechanism let each corrupt the other."
group: hard-parts
order: 50
chips: [Dead ball, Restarts, Two questions]
motif: bp-two-lanes
icon: ribbon
motif_caption: "Two lanes, two questions. A tag may hint at the team and is blocked from the alive-or-dead lane. Combined, home, dead, home counts as two possessions, never one."
facts:
  - { k: Question one, v: "Is the ball in play?" }
  - { k: Question two, v: "If so, which team controls it?" }
  - { k: Design rule, v: "The two never share evidence" }
  - { k: Score structure, v: "A dead ball always separates two spells" }
verdict:
  label: Our read
  text: "Separate the two questions and guard the border. Evidence about the team must never move the edge of a stoppage."
sources:
  - { title: "More Than a Hack 2027: the challenge", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md" }
  - { title: "More Than a Hack 2027: FAQ", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
  - { title: "Borghesi et al. (2023), ball possession with a temporal convolutional network", url: "https://doi.org/10.1016/j.eswa.2023.119780" }
related:
  - /architecture/the-shrewdies-decoder/
  - /architecture/ball-aware-vs-ball-free/
  - /architecture/events-and-control/
  - /challenges/possession-frame-by-frame/
  - /solutions/direct-possession/match-phase-segmentation/
  - /datasets/dfl-idsse/
---

## The design question

One three-way decision, or two two-way decisions? Home, away and dead look like three classes of the same
kind. They are not. Dead is a fact about the match. Home and away are facts about control within live play.

## The options

| Design | How | Wins | Costs |
|---|---|---|---|
| Direct three-class | One model scores home, away, dead | Simple, one objective | Team cues leak into stoppages |
| Two heads | Alive or dead first, then team if alive | Mirrors the football logic | An early error propagates |
| Two evidence lanes, one decoder | Separate evidence, joint decode | Clean evidence, coherent sequence | Lanes must be kept apart by design |

[The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}) runs the third design: a
tag may help decide which team, it can never lengthen or shorten a stoppage, and a unit test guarantees it.
The dead-ball cues it reads are listed there.

## Why the score cares

A dead ball is not a possession, and it always ends one. A stoppage that is missed merges two spells. A
stoppage that is invented splits one. Either way the frame score barely moves and the ranking score does.

## What breaks it in real football

{% include wiki/motif.html id="bp-s-still" caption="Two scenes with the same motionless ball. In one a goalkeeper waits while the press arrives. In the other a wall lines up for a free kick. The ball cannot tell them apart. The players and the tag can." %}

- **A quick free kick.** The stoppage lasts a second. A decoder with a heavy alive-or-dead cost never sees it.
- **A tag that arrives late.** The ball has been dead for some time before any set-piece tag says so.

One failure belongs to another study: reading a missing ball as a stoppage is the subject of
[When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}).

## How to judge it

Score the alive-or-dead decision on its own, as a two-class problem, before scoring possession. Then count
boundary errors by type: live to dead, dead to live, and team to team. A system can be excellent at the
third and lose the match on the first two.
