---
layout: wiki-hub
title: Datasets
permalink: /datasets/
collection_index: datasets
families: true
kicker: The data atlas
summary: "The football-data landscape, read through one question: what can this dataset teach a possession model?"
motif: stack
motif_caption: "Four kinds of evidence. Only one layer says who has the ball."
motif_labels: [Video, Tracking, Events, Possession labels]
stats:
  - { value: "{count}", label: datasets mapped }
  - { value: "6", label: families }
  - { value: "3", label: carry possession on the tracking }
  - { value: "1", label: external judge for our decoder }
groups:
  - key: possession
    title: Frame-level possession labels
    short: Possession labels
    url: /datasets/possession/
    motif: ribbon
    motif_labels: [Tracking evidence, Possession label, Home, Away, Dead ball]
    blurb: "The scarce resource. Three releases put a possession field on the tracking itself, and only one labels all three states under an open licence."
    points:
      - "The only family that can score a possession model"
      - "Three providers, three definitions of possession"
      - "Open DFL labels judged our decoder"
  - key: tracking
    title: Tracking and full-pitch video
    short: Tracking
    url: /datasets/tracking/
    motif: tracks
    motif_labels: [Player track, Trail]
    blurb: "Positions without possession. They teach what a tactical camera sees and how far a position can be trusted."
    points:
      - "Position quality is the ceiling on possession quality"
      - "A track ID is not a player, and a swap looks like a turnover"
      - "Full-pitch footage under CC BY 4.0 exists"
  - key: broadcast
    title: Broadcast video and game state
    short: Broadcast
    url: /datasets/broadcast/
    motif: boxes
    motif_labels: [Player, Ball]
    blurb: "Television pictures turned into players, teams and touches. What a possession model consumes is what these benchmarks ask vision to produce."
    points:
      - "The upstream chain: detect, track, calibrate, identify"
      - "102,992 ball actions tied to the player who made them"
      - "Part of the pitch, and a clock that cuts away"
  - key: events
    title: Events
    url: /datasets/events/
    motif: spikes
    motif_labels: [Pass, Duel, Restart]
    blurb: "Instants, not intervals. Event data cannot label a frame, but it knows the grammar of possession."
    points:
      - "Base rates: how long a spell lasts, how many a match holds"
      - "Restarts mark the edges of the dead ball"
      - "The acting team is not always the owner"
  - key: geometry
    title: Detection, calibration and synthetic
    short: Geometry
    url: /datasets/geometry/
    motif: homography
    motif_labels: [Camera view, Calibration, Pitch plane]
    blurb: "Pixels to metres, and the ball in three dimensions. Possession is decided by distances, so a geometry error is a possession error."
    points:
      - "Every distance passes through a camera model first"
      - "Ball height is the dimension 2D possession ignores"
      - "Synthetic data is for exact geometry and robustness"
  - key: competition
    title: The competition data
    short: Competition
    url: /datasets/competition/
    motif: timeline
    motif_labels: [First half, Second half, Broadcast cuts, Own clock]
    blurb: "The exam and its predecessor, described as the organisers' public repository documents them. The match files are never published here."
    points:
      - "199,319 frames, a ball untracked on 41% of graded frames"
      - "Players carry a team, not an identity"
      - "Five public minutes: a check, not a training set"
featured:
  - /datasets/dfl-idsse/
  - /datasets/skillcorner-opendata/
  - /datasets/footpass/
  - /datasets/reference-target-mtah-2027/
---

## How to read this atlas

A possession model outputs one of three states for every frame: home, away, dead ball. Almost no public dataset contains that answer. Most contain something next to it. Each family below says how close its datasets get, and what they are good for at that distance.

| Rule | Why it holds |
|---|---|
| **Labels beat pixels** | A dataset with a possession field teaches more than one that only looks like the target |
| **Pair only what is truly paired** | Video and tracking belong together when they share a match and a clock |
| **A licence has layers** | Code, annotations and footage are licensed separately |

Our Initial Challenge decoder has no trained weights, so nothing here was a training set. One dataset still decided something: open [DFL labels]({{ '/datasets/dfl-idsse/' | relative_url }}) judged the decoder's parameter profiles and picked the one we submitted.
