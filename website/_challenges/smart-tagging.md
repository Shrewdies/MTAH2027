---
layout: wiki-entry
nav_exclude: true
title: Tags are context, not events
kicker: The data
summary: "638 automatic tactical intervals: restarts, phases and a team name. Powerful when read as evidence, misleading when read as labels."
route_label: Tags
hook: "Context, not events"
group: data
order: 80
chips: [638 intervals, 14 codes, Automatic]
motif: spikes
motif_caption: Restart tags mark where stoppages begin. Phase tags lean towards a team without ever fixing the frame where possession changed.
motif_labels: [Phase tag, Transition, Set piece]
facts:
  - { k: Intervals, v: "638, with start and end in seconds" }
  - { k: Codes, v: "14 tactical codes" }
  - { k: Restarts, v: "59 set pieces, typed" }
  - { k: Origin, v: "Automatic, not hand-coded" }
verdict:
  label: Our read
  text: "Tags answer two different questions with two different reliabilities. Restart tags are strong evidence about dead ball. Team tags are a weak hint about who has it, and the hint has to be calibrated, because several codes name the team without the ball."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "FAQ (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
  - { title: "The Shrewdies, technical report: making the tags speak for themselves", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/report/the-shrewdies-technical-report.pdf" }
related:
  - /challenges/data-asset-map/
  - /challenges/possession-frame-by-frame/
  - /architecture/events-and-control/
---
## What is supplied

Smart Tagging is a list of 638 intervals, each with a start, an end, a tactical code, a team and, for restarts, a type. Fourteen codes cover the phases of play: build up, progression, ball in the final third, players in the box, the defending thirds, both transitions, long ball, creating chances, set pieces, goals.

It is not an event log. There is no row per pass, reception, tackle or foul. And it is automatic, so its errors can be shared with the tracking.

## How to read each signal

| Tag | Read it as | Do not read it as |
|---|---|---|
| Set piece, typed as throw-in, corner, goal kick, free kick, kick-off | A stoppage around its start | The exact frame play stopped |
| Attacking or defensive transition | A recovery happened nearby | The frame control changed |
| Long ball | A possibly airborne passage | A turnover: the passer keeps it in flight |
| Goal | Match context | A substitute for the stoppage around it |
| Any team-tagged phase | A lean towards one team | A label for every frame inside it |

One possession can run through several tags. One restart sits entirely inside a dead-ball stretch.

## The trap in the team field

A code's team is not always the team with the ball. For *Build up* it is. For *Defending in middle third* it is the side **without** it. Hand-picking which codes mean what is exactly the kind of quiet assumption that fails on the next match.

## How we use them

**The tags calibrate themselves.** For each code, the pipeline measures how often the tagged team agrees with visible ball control. No answers are involved. The agreement becomes a log-odds weight.

| Code | Agreement with visible control | Weight |
|---|---|---|
| Build up | 86.5% | +1.86 |
| Progression | 83.0% | +1.58 |
| Players in the box | 58.2% | +0.33 |
| Defending in attacking third | 13.5% | −1.86 |

Defending codes come out as mirrors of attacking ones, and vague codes count for little. Nobody told the program which is which. In the submitted profile the calibrated tag evidence is scaled to 0.035, so visible ball control always dominates.

Restart tags do a separate job: the start of a tagged set piece is evidence for dead ball and says nothing about the team. Why weights are measured and not hand-picked is argued in [Events are not possession]({{ '/architecture/events-and-control/' | relative_url }}). Why a team tag can never move the edge of a stoppage is in [Alive or dead, then who]({{ '/architecture/live-dead/' | relative_url }}).
