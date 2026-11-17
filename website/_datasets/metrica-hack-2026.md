---
title: More Than a Hack 2026 data
kicker: The competition data
summary: "The previous edition's release from the same organisers: broadcast video, automatic tracking and Smart Tagging per match, in the same file family as 2027."
group: competition
order: 20
chips: [Broadcast video, Tracking, Smart Tagging]
motif: stack
motif_caption: "Three layers per match. The fourth, possession answers, is not part of this release."
motif_labels: [Broadcast video, Tracking, Smart Tagging, No H/A/D answers]
facts:
  - { k: Edition, v: "More Than a Hack 2026, Soccer GPT Hackathon" }
  - { k: Modality, v: "Broadcast video, automatic tracking, Smart Tagging" }
  - { k: Tracking format, v: "Metrica FIFA format: metadata XML plus raw text" }
  - { k: Tags, v: "SportsCode XML: tactical phases and contextual tags" }
  - { k: Container, v: "Nexus .pl3container bundling video, tags and tracking" }
  - { k: Possession labels, v: "None" }
  - { k: Licence, v: "None stated in the repository" }
  - { k: Access, v: "Download folders linked from the organisers' repository" }
verdict:
  label: Our read
  text: "Same vendor, same formats, a different question. Worth knowing for its file conventions and its tag vocabulary. It has no possession answers, so it cannot judge a possession model."
sources:
  - { title: "Organisers' 2026 repository", url: "https://github.com/metrica-sports/more-than-a-hack" }
  - { title: "2027 rules, for comparison", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
related:
  - /datasets/reference-target-mtah-2027/
  - /datasets/metrica-sample-data/
---

## What it is

Metrica Sports ran More Than a Hack in 2026 as a "Soccer GPT" hackathon, and its public repository documents the data given to participants. Each match comes as a broadcast video, an automatic tracking export in Metrica's FIFA format, and a Smart Tagging file in SportsCode XML. A Nexus container file bundles all three.

The repository offers the release three ways: everything, tracking and tags only, or videos only.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct. No home, away and dead-ball answers |
| Tracking | Automatic tracking in the vendor's FIFA-format export |
| Events | Smart Tagging: tactical phases and contextual tags |
| Calibration | Not documented |

## Where it wins

- **Format continuity.** The tracking export and the tag file follow the same conventions as the 2027 release. A parser written for one should read the other with little change.
- **A tag vocabulary to study.** Tactical phases and contextual tags show what automatic tagging describes and at what grain.
- **Automatic tracking in the wild.** The same class of data as 2027: produced from video by a system, with the gaps that implies.

## What it costs

- **No answers.** The 2026 challenges asked different questions. The documentation lists no per-frame possession truth, so nothing here can score a possession model.
- **No stated licence.** The repository documents the data and states no licence for it.
- **Broadcast only.** The documentation describes broadcast video. No tactical view is listed.

## How it plugs into possession

As a study of inputs, not outputs. Automatic tags are evidence with an unknown error rate. Before a decoder can lean on a tag, it needs to know how often that tag code agrees with what the tracking shows. Our decoder calibrates each tag code automatically for that reason, and the general lesson holds across editions: treat vendor tags as a noisy sensor, measure the sensor, then weigh it.
