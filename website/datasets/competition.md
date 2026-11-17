---
layout: wiki-hub
title: The competition data
permalink: /datasets/competition/
collection_index: datasets
only_group: competition
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "The exam and its predecessor, described as the organisers' public repository documents them. The match files themselves are never published here."
motif: ds-window
icon: timeline
motif_caption: "The 2027 match on its tactical clock. The ball is untracked on 41% of graded frames, and five minutes of answers are public. Gaps are drawn for effect."
motif_labels: [Ball tracked, Answers, "Public: 5 minutes", Private, First half, Second half]
stats:
  - { value: "199,319", label: frames to label }
  - { value: "41%", label: of graded frames without a ball }
  - { value: "638", label: automatic tactical tags }
---

## What this family is

Two releases from Metrica Sports' More Than a Hack. The 2027 match is the target of our Initial Challenge work: one LaLiga match, a label for every frame, the answers held back. The 2026 release is the previous edition, in the same file family, built for different questions.

Everything on these pages comes from the organisers' public documentation and our own published aggregates. The match data is licensed to participants for the competition only.

{% include wiki/motif.html id="ds-tiers" caption="Three tiers of access. The answers stay with the organisers, the match files with participants, and everything on these pages comes from the bottom tier." %}

## Two editions

| | 2027 match | 2026 release |
|---|---|---|
| Task | Home, away or dead ball on every frame | A "Soccer GPT" hackathon, other questions |
| Video | Tactical and broadcast | Broadcast |
| Tracking | Automatic, team only | Automatic, Metrica FIFA format |
| Tags | 638 automatic Smart Tagging instances | Smart Tagging, SportsCode XML |
| Answers | Private, five minutes public | None documented |

Pages: [More Than a Hack 2027 match]({{ '/datasets/reference-target-mtah-2027/' | relative_url }}) and [More Than a Hack 2026 data]({{ '/datasets/metrica-hack-2026/' | relative_url }}).

{% include wiki/motif.html id="ds-editions" caption="Tracking and tags share a file family across the two editions. A tactical view and possession answers exist only for 2027." %}

## What makes the 2027 match hard

Five things, each with its own read in Challenges: [a ball untracked on 41% of graded frames]({{ '/challenges/tracking-errors/' | relative_url }}), [players that carry a team and no identity]({{ '/challenges/tactical-tracking/' | relative_url }}), [tags that are a system's output]({{ '/challenges/smart-tagging/' | relative_url }}), [a broadcast feed on its own clock]({{ '/challenges/broadcast-and-timebases/' | relative_url }}), and [a ranking metric that counts whole possessions]({{ '/challenges/spellf1-and-macrof1/' | relative_url }}).

The rules are part of the data too. No hand labels, no tuning on the match, nothing uploaded, and an exact file anyone can regenerate. They are read as engineering requirements in [The rules are the architecture]({{ '/challenges/rules-as-design-constraints/' | relative_url }}).

## The traps

- **Licence.** Competition-only. Nothing from the match files can be redistributed, including in a public repository.
- **The 2026 release states no licence.** Documented data is not open data.
- **Format continuity is not content continuity.** The two editions share file conventions. Only 2027 has possession answers.

## Where it meets our decoder

This is the data our decoder was built for. The public window was used for what it is for: a correctness check on timebase, label mapping and file format. The design is drawn in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}), and the result is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page.
