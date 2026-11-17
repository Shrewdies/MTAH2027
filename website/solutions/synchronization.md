---
layout: wiki-hub
title: "Synchronisation"
permalink: /solutions/synchronization/
collection_index: solutions
only_group: synchronization
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Putting video, audio and tracking on one clock, from file timestamps to geometry."
motif: sync
motif_caption: "Two clocks describe one match. Every label depends on them agreeing."
motif_labels: ["Video clock", "Tracking clock", "Aligned"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "0.4 s", label: "boundary shift from a 10-frame offset" }
  - { value: "3", label: "need no training" }
---
## One picture: two clocks, one match

Every source of football data keeps its own time. Tracking counts frames. A video file stores a timestamp for each frame. Events are logged by people. The picture above is the whole problem: two timelines of the same match that must be slid, and sometimes stretched, until they agree.

The price of getting it wrong is concrete. At 25 fps an offset of ten frames moves every possession boundary by 0.4 seconds, and any evidence that combines two sources ends up comparing two different moments.

{% include wiki/motif.html id="sol-offset-cost" caption="Ten frames apart, the two sources disagree in a sliver at every boundary. Evidence that mixes them is comparing two different moments there." %}

Syncing comes before any evidence that mixes sources. With a single feed it is already done.

## How to choose inside it

| Entry | Labels | What the sources must share | Compute |
|---|---|---|---|
| [FFprobe and PyAV]({{ '/solutions/synchronization/ffprobe-pyav/' | relative_url }}) | None | Nothing. It reads one file's clock | Seconds |
| [Audio offset estimation]({{ '/solutions/synchronization/pyroomacoustics/' | relative_url }}) | None | Sound from the same stadium | Light |
| [Dynamic time warping]({{ '/solutions/synchronization/dtw-python/' | relative_url }}) | None | A signal both measure | Light with a window |
| [Geometric synchronisation]({{ '/solutions/synchronization/geometric-sync/' | relative_url }}) | None for the principle | Moving players seen by both | Moderate |
| [Learned video alignment]({{ '/solutions/synchronization/learned-video-alignment/' | relative_url }}) | Multi-view footage to train on | The same action | GPU |

Work from cheap to expensive, top to bottom. Most problems end at the second or third row.

{% include wiki/motif.html id="sol-sync-funnel" caption="Five methods, cheapest first. Each is tried only on what the one above left open." %}

## What this family cannot do

- **It cannot find one offset where none exists.** An edited broadcast has a different offset after every cut.
- **It cannot align what the sources do not share.** No common sound, no common view, no common signal: no synchronisation.
- **It cannot beat its features.** Alignment is only as sharp as the signal being aligned.

## Where our decoder stands

On one clock by construction. The task is one label per frame, 199,319 frames at 25 fps, and the decoder labels those frames. Its one time-uncertain input is the tag stream, which it reads as windows, not instants. Synchronisation becomes a design problem the moment video evidence is added.
