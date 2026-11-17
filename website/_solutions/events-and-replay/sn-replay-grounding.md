---
title: "SoccerNet replay grounding"
kicker: "Events and replay"
summary: "Given a replay, find the live moment it shows. The piece that stops a broadcast pipeline from counting the same goal twice."
group: events-and-replay
order: 70
chips: ["Video", "Replay", "Benchmark"]
motif: sync
motif_caption: "A replay is tied back to the live moment it repeats, so the action is counted once."
motif_labels: ["Replay", "Live broadcast", "Grounded"]
facts:
  - { k: "Modality", v: "Broadcast video with replay segments" }
  - { k: "Output", v: "The live timestamp of the action shown in a replay" }
  - { k: "Evidence", v: "SoccerNet benchmark task with code and annotations" }
  - { k: "Code and weights", v: "Development kit and baselines" }
  - { k: "Licence", v: "None declared in repository; data on SoccerNet terms" }
verdict: { label: "Our read", text: "Broadcast hygiene. It removes double-counted football and tells you where the live timeline has holes." }
sources:
  - { title: "sn-grounding: development kit for the SoccerNet replay grounding challenge", url: "https://github.com/SoccerNet/sn-grounding" }
  - { title: "SoccerNet replay grounding task page", url: "https://www.soccer-net.org/tasks/replay-grounding" }
related:
  - /solutions/events-and-replay/pyscenedetect/
  - /solutions/events-and-replay/sn-spotting/
  - /solutions/synchronization/learned-video-alignment/
---
A broadcast is not a recording of a match. It is an edit: live play, then a replay of a foul from two angles, then live play that resumed while the replay ran. A model that reads broadcast video frame by frame sees the same tackle three times.

Replay grounding links each replay to its source. Given a replay segment, the model must return the timestamp in the live footage of the action it shows. SoccerNet provides annotated replays and baselines, and scores predictions by temporal tolerance.

## Where it wins

- It addresses broadcast structure head-on. Few other tasks model the edit.
- A grounded replay is an extra camera angle on a known moment, useful for hard calls.
- A shared benchmark with public baselines.

## What it costs

- It links. It does not align. The output is a moment, not a frame-accurate mapping between replay frames and live frames, and slow motion makes that mapping non-linear.
- It depends on an upstream step to say which segments are replays.
- Only replayed actions are covered, and directors replay what is dramatic, not what is typical.

## How it plugs into possession

In video-based possession, replays poison the timeline. Frames inside a replay are not match time. They must be excluded before any per-frame labelling, and the live clock must keep running underneath them, because play often restarts while the replay is still on screen.

So the role is hygiene. [Shot detection]({{ '/solutions/events-and-replay/pyscenedetect/' | relative_url }}) finds the cuts, replay detection labels the segments, and grounding ties each replay to a moment already seen. What remains is a clean live timeline with known holes, the kind of input a decoder that accepts frames without evidence handles well.

The replay and camera-shot labels come with [SoccerNet Action Spotting]({{ '/datasets/soccernet-action-spotting/' | relative_url }}).
