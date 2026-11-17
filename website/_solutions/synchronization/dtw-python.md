---
title: "Dynamic time warping (dtw-python)"
kicker: "Synchronisation"
summary: "Aligns two sequences that show the same thing at different or varying speeds, by finding the cheapest monotonic path between them."
group: synchronization
order: 30
chips: ["Time series", "Alignment", "Classical", "GPL-3.0"]
motif: sync
motif_caption: "Two signals of the same play, stretched differently. The warping path says which frame matches which."
motif_labels: ["Video signal", "Tracking signal", "Warped to match"]
facts:
  - { k: "Modality", v: "Two time series of comparable features" }
  - { k: "Output", v: "A frame-to-frame alignment path and its cost" }
  - { k: "Evidence", v: "Python port of the comprehensive R package" }
  - { k: "Code and weights", v: "Python package; no weights" }
  - { k: "Licence", v: "GPL-3.0" }
verdict: { label: "Our read", text: "The right tool for residual drift, and a liability without a tight window. Coarse first, DTW second." }
sources:
  - { title: "dtw-python: Python port of R's comprehensive dynamic time warping package (repository)", url: "https://github.com/DynamicTimeWarping/dtw-python" }
related:
  - /solutions/synchronization/ffprobe-pyav/
  - /solutions/synchronization/pyroomacoustics/
  - /solutions/synchronization/geometric-sync/
---
Dynamic time warping answers a question cross-correlation cannot: what if the offset between two signals is not constant? It builds a cost matrix between every sample of one sequence and every sample of the other, then finds by dynamic programming the monotonic path through that matrix with the lowest total cost. The path says which sample of one corresponds to which sample of the other.

dtw-python is the Python port of the comprehensive R package. Its value lies in the constraints it exposes. Step patterns limit how fast one sequence may run against the other. Global windows keep the path near the diagonal. Open-ended modes match a short clip inside a long recording.

## Where it wins

- It handles drift, dropped frames and changes of speed, cases a single offset cannot describe.
- Exact for its cost and constraints, and fully deterministic.
- Subsequence matching locates a clip within a match.
- It works on any pair of signals that should agree: a tracked team centroid against one derived from video, ball speed against ball speed.

## What it costs

- Unconstrained, it will align anything to anything. Football repeats itself, and a goal kick in minute 12 looks like one in minute 70.
- Cost grows with the product of the two lengths unless a window is set. Full halves need banding or a coarse first pass.
- Its path is monotonic. It cannot represent a broadcast that jumps back in time for a replay.
- GPL-3.0.
- It aligns features, and feature quality is its ceiling.

## How it plugs into possession

As fine alignment after coarse alignment. Find the rough offset by cheap means, [timestamps]({{ '/solutions/synchronization/ffprobe-pyav/' | relative_url }}) or [audio]({{ '/solutions/synchronization/pyroomacoustics/' | relative_url }}), then let a tightly windowed DTW absorb the residual: a few frames of drift, a dropped frame. The signals to align are the ones both sources measure, such as team centroid or ball speed.

Sync error is possession error. An offset of ten frames at 25 fps moves every boundary by 0.4 seconds, and any evidence that combines video with tracking ends up comparing two different moments.
