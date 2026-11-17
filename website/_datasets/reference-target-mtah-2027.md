---
title: More Than a Hack 2027 match
kicker: The competition data
summary: "One LaLiga match, 199,319 tactical-camera frames, automatic tracking and tags, and a private answer for every frame. The exam every other dataset here is read against."
group: competition
order: 10
chips: [Tracking, Smart Tagging, Two videos, Competition licence]
motif: timeline
motif_caption: "The tactical video is the clock. The broadcast runs on its own timeline, with cuts and replays."
motif_labels: [First half, Second half, Cuts and replays, Own clock]
facts:
  - { k: Match, v: "FC Barcelona v Athletic Club, LaLiga 2024-25, matchday 2" }
  - { k: Timebase, v: "Tactical video: 199,319 frames at 25 fps, 1920×1080" }
  - { k: Tracking, v: "Automatic. Positions and team only, no player identities" }
  - { k: Ball, v: "Untracked on 41% of graded frames" }
  - { k: Tags, v: "638 automatic Smart Tagging instances" }
  - { k: Calibration, v: "A homography per frame. Broadcast usable on 65.8% of its frames" }
  - { k: Second video, v: "Broadcast, on its own clock with cuts and replays" }
  - { k: Labels, v: "Home, away or dead ball per frame. Private, except the first five minutes of play" }
  - { k: Licence, v: "Match data for this competition only. Repository code and docs MIT" }
  - { k: Access, v: "Enrolled participants" }
verdict:
  label: Our read
  text: "A realistic problem, stated without mercy. Automatic tracking as it really is, a ball that vanishes on two frames in five, and a metric that counts whole possessions. Nothing about it rewards a model that only works on clean data."
sources:
  - { title: "Organisers' repository", url: "https://github.com/metrica-sports/more-than-a-hack-2027" }
  - { title: "Data specification", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "Rules", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
  - { title: "Evaluation", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "FAQ", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
related:
  - /datasets/dfl-idsse/
  - /datasets/metrica-hack-2026/
  - /datasets/metrica-sample-data/
  - /challenges/data-asset-map/
  - /challenges/rules-as-design-constraints/
  - /challenges/initial-challenge/
---

## What it is

The dataset of Metrica Sports' More Than a Hack 2027 Initial Challenge, as the organisers document it in their public repository. One match. The task: for every frame of the tactical video, say whether the home team has the ball, the away team has it, or the ball is dead.

Participants receive two videos of the match, automatic tracking for each, a homography for every frame and a file of automatic tactical tags. The tactical video is the clock. Row *i* of a submission is frame *i*.

This page describes the data at the level of that public documentation. The match files themselves are licensed to participants for the competition only and are not published here.

## Where each layer is read

This page is the dataset card. What each layer can tell a possession model, and where it stops, is read layer by layer in Challenges.

| Layer | What the documentation describes | Read |
|---|---|---|
| Tactical video and tracking | The reference timebase. Automatic tracking in normalised pitch coordinates, with track slots that carry a team | [Tactical tracking: the master clock]({{ '/challenges/tactical-tracking/' | relative_url }}) |
| The ball | Untracked on 41% of graded frames | [The ball goes missing]({{ '/challenges/tracking-errors/' | relative_url }}) |
| Smart Tagging | 638 automatically generated tactical tag instances, in SportsCode XML | [Tags are context, not events]({{ '/challenges/smart-tagging/' | relative_url }}) |
| Homography | A 3×3 matrix per frame for each video | [Homography]({{ '/challenges/homography/' | relative_url }}) |
| Broadcast video and tracking | The television programme, on its own timeline, with cuts and replays | [Two cameras, two clocks]({{ '/challenges/broadcast-and-timebases/' | relative_url }}) |
| Answers | Private for the full match, public for the first five minutes of play | [The Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}) |

The whole inventory on one page is [What each data asset contributes]({{ '/challenges/data-asset-map/' | relative_url }}). The rules that come with the data are read as engineering requirements in [The rules are the architecture]({{ '/challenges/rules-as-design-constraints/' | relative_url }}).

## How it plugs into possession

It is the target. Our answer, an evidence decoder built for exactly this data, is summarised on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page and drawn in full in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).

External data about other matches is allowed, provided the organisers can access it. That is why the open, properly licensed datasets in this atlas matter here more than they do in most research.
