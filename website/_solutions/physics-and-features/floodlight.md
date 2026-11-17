---
title: "floodlight"
kicker: "Physics and features"
summary: "A typed data model for team-sport tracking: positions, events, pitch and per-frame codes as first-class objects, with kinematics and spatial analysis on top."
group: physics-and-features
order: 50
chips: ["Tracking + events", "Library", "No training", "MIT"]
motif: stack
motif_caption: "One match in aligned layers: positions, events and per-frame codes, all tied to one pitch."
motif_labels: ["XY positions", "Events", "Codes", "Pitch"]
facts:
  - { k: "Modality", v: "Tracking and event data" }
  - { k: "Output", v: "Kinematic and spatial features" }
  - { k: "Evidence", v: "Journal of Open Source Software paper (2022)" }
  - { k: "Code and weights", v: "Installable Python package; nothing to train" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "Solid plumbing for kinematics and per-frame state. It will not find possession. It will stop you fumbling the units on the way." }
sources:
  - { title: "floodlight: Python package for streamlined analysis of sports data (repository)", url: "https://github.com/floodlight-sports/floodlight" }
  - { title: "floodlight software paper (Journal of Open Source Software, 2022)", url: "https://doi.org/10.21105/joss.04588" }
related:
  - /solutions/readers-and-formats/kloppy/
  - /solutions/physics-and-features/unravelsports/
  - /solutions/physics-and-features/pitch-control/
  - /datasets/dfl-idsse/
---
floodlight is a Python framework for team-sport data. Its core is a small set of data objects: an XY object for positions over time, Events, a Pitch that knows its dimensions and coordinate system, and Code objects for per-frame state such as ball status or possession. Parsers fill these objects from provider files, and models consume them.

On top sit the standard computations: distance covered, velocity and acceleration, plus geometric and spatial analyses.

Its design choice is strictness. A frame rate, a direction of play and a unit are properties of the object, not conventions in someone's head.

## Where it wins

- Kinematics done once, correctly. Differentiation and units are library code.
- The Code object is a ready container for an H/A/D signal: one state per frame, with definitions attached.
- Peer-reviewed, documented and MIT.

## What it costs

- It carries data and computes features. It does not decide possession.
- It is one more data model to convert to and from if the rest of a stack runs on [kloppy]({{ '/solutions/readers-and-formats/kloppy/' | relative_url }}) or plain arrays.
- Semantics stay with the user. The library stores a possession code; what counts as possession is still a definition someone must write.

## How it plugs into possession

As the feature layer. Speeds of players and ball, accelerations and distances are the raw material of possession evidence. A collective-stillness cue for dead balls, for instance, is a velocity computation over all players.

Its per-frame codes also suit both ends of validation: the decoder's output, and provider labels such as the possession and ball-status streams in the open DFL matches. Those matches are described under [DFL IDSSE open data]({{ '/datasets/dfl-idsse/' | relative_url }}).
