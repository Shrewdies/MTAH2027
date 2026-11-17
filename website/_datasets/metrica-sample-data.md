---
title: Metrica Sports sample data
kicker: Tracking
summary: "Three anonymised matches of tracking with synchronised events, in the file conventions Metrica uses everywhere. The format bridge to any Metrica-shaped problem."
group: tracking
order: 10
chips: [Tracking, Events, Open repository]
motif: tracks
motif_caption: "Clean, complete tracks for both teams and the ball, with events on the same clock."
motif_labels: [Anonymised player, Trajectory]
facts:
  - { k: Modality, v: "Per-frame player and ball tracking with synchronised events" }
  - { k: Scale, v: "3 anonymised matches" }
  - { k: Formats, v: "Two matches in CSV; one in FIFA EPTS format with JSON events" }
  - { k: Coordinates, v: "Normalised 0 to 1 on both axes" }
  - { k: Possession labels, v: "None per frame. Events only" }
  - { k: Video, v: "None" }
  - { k: Calibration, v: "None" }
  - { k: Licence, v: "No explicit data licence in the repository" }
  - { k: Access, v: "Public GitHub repository" }
verdict:
  label: Our read
  text: "Not a possession dataset, and it does not need to be. It is the cleanest way to learn Metrica's coordinate and file conventions before real automatic tracking arrives."
sources:
  - { title: "Repository and format notes", url: "https://github.com/metrica-sports/sample-data" }
related:
  - /datasets/reference-target-mtah-2027/
  - /datasets/metrica-hack-2026/
  - /architecture/geospatial-only/
---

## What it is

Metrica Sports' public sample: three matches with the teams and players anonymised. Two ship as CSV tracking plus an event table. The third follows the FIFA EPTS standard, with events in JSON. Positions are normalised to the unit square, so a pitch length has to be chosen before any distance means anything.

It is the dataset many open tracking tutorials are built on, which makes it the common ground for comparing loaders and basic models.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Indirect only: on-ball events name the team that acted |
| Tracking | Complete, tidy tracks for both teams and the ball |
| Events | Passes, shots, recoveries and set pieces on the tracking clock |
| Calibration | Nothing |

## Where it wins

- **Format affinity.** EPTS metadata, normalised coordinates, one row per frame. A loader that reads this reads Metrica.
- **Events on the same clock.** Each event points at frames, so event logic and tracking logic can be tested against each other.
- **Zero friction.** A public repository, small files, no forms.

## What it costs

- **No three-state truth.** Events say who played the ball. They do not say when the ball went dead or when a loose ball became someone's.
- **Cleaner than the real thing.** The sample is tidier than automatic tracking from video. Methods tuned on it meet missing balls and unstable track slots later, unprepared.
- **Anonymised.** No fixture, no footage, no way to add a modality.

## How it plugs into possession

Two jobs. First, as a fixture for unit tests: coordinate scaling, half-time direction flips, frame-to-time arithmetic. Bugs there are silent and cost more than any model choice.

Second, as a source of weak labels. Between a pass and its reception the team in possession is known, so events give a sparse possession skeleton. It is good for sanity checks on a decoder's output and too thin to grade one.
