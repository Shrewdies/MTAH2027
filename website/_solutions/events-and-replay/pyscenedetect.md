---
title: "PySceneDetect"
kicker: "Events and replay"
summary: "Shot-boundary detection without learning. Frame-to-frame content change, thresholded, gives the cuts that divide a broadcast into continuous camera takes."
group: events-and-replay
order: 60
chips: ["Video", "Shot detection", "No training", "BSD-3-Clause"]
motif: changepoint
motif_caption: "Content change between frames stays low inside a shot and jumps at a cut."
motif_labels: ["Frame change", "Cut", "Shots"]
facts:
  - { k: "Modality", v: "Any video" }
  - { k: "Output", v: "Cut timestamps and a shot list" }
  - { k: "Evidence", v: "Mature open-source tool with documentation" }
  - { k: "Code and weights", v: "Python library and command-line tool; rule-based, no weights" }
  - { k: "Licence", v: "BSD-3-Clause" }
verdict: { label: "Our read", text: "A small, dependable tool that every broadcast pipeline needs first. It finds the cuts. What each shot is remains your problem." }
sources:
  - { title: "PySceneDetect: scene cut and transition detection (repository)", url: "https://github.com/Breakthrough/PySceneDetect" }
  - { title: "PySceneDetect documentation", url: "https://www.scenedetect.com/" }
related:
  - /solutions/events-and-replay/sn-replay-grounding/
  - /solutions/synchronization/ffprobe-pyav/
  - /solutions/physics-and-features/ruptures/
---
PySceneDetect finds the places where a video was cut. Its detectors compare consecutive frames and flag a boundary when the change is too large to be motion.

The content detector measures differences in colour and intensity between adjacent frames. The adaptive variant compares each frame's change with a rolling average of its neighbours, so that a fast pan is not mistaken for a cut. A threshold detector handles fades, and a histogram detector offers another measure. The output is a list of shots with their boundaries.

## Where it wins

- No model, no GPU, no training.
- Deterministic and easy to tune, with one main threshold per detector.
- Hard cuts, the dominant transition in live sport, are its easy case.
- BSD-3-Clause.

## What it costs

- It finds cuts, not meaning. A shot is not labelled live, replay, close-up or crowd.
- Broadcast graphics wipes and replay transitions are neither clean cuts nor fades and need their own handling.
- A threshold that suits a floodlit night match may not suit a sunlit one.

## How it plugs into possession

Every video model in this section assumes temporal continuity: trackers, camera smoothing, spotters with clip context. A cut breaks all of them at once. Shot boundaries are where trackers must be reset, cameras re-estimated and temporal windows truncated.

For possession from broadcast, the shot list is the scaffold. Classify each shot as main camera or not, run the pipeline on main-camera shots, and hand the gaps to the decoder as frames without evidence.

On a single uncut tactical camera none of this is needed, which is a large part of why tactical video is the better source. [Replay grounding]({{ '/solutions/events-and-replay/sn-replay-grounding/' | relative_url }}) handles the next question: what a replay shot is a replay of.
