---
layout: wiki-hub
title: "Readers and formats"
permalink: /solutions/readers-and-formats/
collection_index: solutions
only_group: readers-and-formats
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Libraries that load provider files into one model and pin events to frames. The tooling under every cross-provider test."
motif: stack
motif_caption: "Loaders turn provider files into one model, then pin events to tracking frames."
motif_labels: ["Provider files", "One data model", "Events on frames", "Analysis"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "2", label: "permissive licences" }
---
## One picture: many formats, one model

{% include wiki/motif.html id="sol-conventions" caption="Three providers, three ideas of where the origin is, what a unit is and which way a team attacks. The reader makes them one." %}

Every provider ships its own file format, its own coordinate system and its own direction of play. A reader turns all of them into one model, so that a method written once runs on any of them. It sounds like plumbing. It decides whether a possession method can be tested at all, because validation on external labels means reading someone else's data in the same shape as your own.

This family is tooling only. The datasets themselves, what each contains and what each can teach, live in the [Datasets]({{ '/datasets/' | relative_url }}) section.

It is the first link of the chain, and every error made here is inherited by every link after it.

## How to choose inside it

| Entry | Reads | Adds | Licence |
|---|---|---|---|
| [kloppy]({{ '/solutions/readers-and-formats/kloppy/' | relative_url }}) | Tracking and events, many providers | One model, coordinate and orientation transforms | BSD-3-Clause |
| [DataBallPy]({{ '/solutions/readers-and-formats/databallpy/' | relative_url }}) | Tracking and events | Events synchronised to tracking frames | MIT |
| [floodlight]({{ '/solutions/physics-and-features/floodlight/' | relative_url }}) | Tracking and events | Typed containers, kinematics, per-frame codes | MIT |

floodlight is filed under physics and features and listed here because it reads data too.

{% include wiki/motif.html id="sol-leak" caption="Pinning events to frames puts answer-bearing columns beside measured ones. A method under test reads the left side only." %}

## What this family cannot do

- **It cannot standardise meaning.** Two providers' possession flags follow different rules, and a loader carries both faithfully.
- **It cannot add what a feed lacks.** A missing ball stays missing in any format.
- **It cannot stop a leak.** Event-derived columns next to tracking columns are an invitation to feed the answer to the model.

## Where our decoder stands

Across two providers. It runs on the organisers' feed and was chosen on open DFL labels, scored with the same official metric. That is the job this family exists for: one evaluation and two sources, with the same conventions for coordinates and frames, and each provider's possession flag read as that provider's definition.
