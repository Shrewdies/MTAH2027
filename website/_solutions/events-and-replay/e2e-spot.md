---
title: "E2E-Spot"
kicker: "Events and replay"
summary: "End-to-end spotting of temporally precise events: per-frame features and a recurrent layer, trained together so that fine timing survives."
group: events-and-replay
order: 30
chips: ["Video", "Event spotting", "Open weights", "BSD-3-Clause"]
motif: pipeline
motif_caption: "Every frame is encoded, context is added across time, and every frame gets a class or background."
motif_labels: ["Frames", "Frame encoder", "Recurrent", "Frame classes"]
facts:
  - { k: "Modality", v: "Video" }
  - { k: "Output", v: "Event class scores for every frame" }
  - { k: "Evidence", v: "ECCV 2022" }
  - { k: "Code and weights", v: "Training and inference code; models in a companion repository" }
  - { k: "Licence", v: "BSD-3-Clause" }
verdict: { label: "Our read", text: "The clean, permissive baseline for frame-accurate spotting. Bring your own football labels." }
sources:
  - { title: "spot: code for Spotting Temporally Precise, Fine-Grained Events in Video (ECCV 2022)", url: "https://github.com/jhong93/spot" }
  - { title: "e2e-spot-models: released model weights", url: "https://github.com/jhong93/e2e-spot-models" }
related:
  - /solutions/events-and-replay/team-tdeed/
  - /solutions/events-and-replay/ball-action-winner/
  - /solutions/classifiers-and-decoders/pytorch-tcn/
---
"Spotting Temporally Precise, Fine-Grained Events in Video" named the task that ball-action challenges later adopted: find events at a tolerance of a frame or two, not a second or two. The paper's argument is that this requires end-to-end training. Pipelines that freeze a feature extractor and train a head on top lose the fine temporal detail in the features.

E2E-Spot is the compact baseline that makes the case. A lightweight network encodes every frame, with temporal information mixed between neighbouring frames inside it. A recurrent layer aggregates over the clip. The model classifies every frame as an event class or background and trains directly on long clips.

## Where it wins

- Frame-level output by design. The task definition matches the precision possession needs.
- Small and fast. Dense per-frame inference is affordable.
- BSD-3-Clause, the most permissive licence among the spotters here.
- A clean, general baseline that later football spotters build on and compare against.

## What it costs

- The released models target the paper's benchmarks. Fine-grained ball actions on a new camera mean retraining.
- Events are sparse and background is everywhere: extreme class imbalance, and sensitivity to timing noise in the labels.
- No actor, no team.
- A recurrent layer over a clip has no view of the whole match.

## How it plugs into possession

As the trainable spotter when you own labels and need to ship. A permissive licence, a small model and frame-level outputs are the properties that matter when event evidence is one input to a larger possession system.

Its per-frame scores are also the right shape for a decoder. Do not threshold them into discrete events. Pass the score curves through as soft evidence of a touch.
