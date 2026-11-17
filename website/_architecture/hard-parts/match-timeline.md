---
title: One clock for the match
kicker: The hard parts
summary: "Every scored frame is a tactical frame. Any other source must be mapped onto that clock before it can testify, and a replay makes the mapping run backwards. Which evidence can fix the mapping, and what the mapping must record."
group: hard-parts
order: 10
chips: [Synchronisation, Broadcast, Replays]
motif: bp-clock
icon: sync
motif_caption: "The tactical clock runs straight. The broadcast is cut into segments: live ones map forward, the replay points back to an instant already played, the crowd shot maps to nothing."
facts:
  - { k: Reference clock, v: "The tactical frame index" }
  - { k: Mapping, v: "Per segment, with a type and an uncertainty" }
  - { k: Segment types, v: "Live, replay, slow motion, unknown" }
  - { k: Trap, v: "One global offset for a whole broadcast" }
verdict:
  label: Our read
  text: "Synchronisation is a per-segment mapping with a confidence, never a single offset. When the evidence is thin, a candidate interval is the correct answer and a frame number is a false one."
sources:
  - { title: "More Than a Hack 2027: the data", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "dtw-python: dynamic time warping", url: "https://github.com/DynamicTimeWarping/dtw-python" }
  - { title: "SoccerNet Replay Grounding", url: "https://github.com/SoccerNet/sn-grounding" }
  - { title: "Dwibedi et al. (2019), temporal cycle-consistency learning", url: "https://openaccess.thecvf.com/content_CVPR_2019/html/Dwibedi_Temporal_Cycle-Consistency_Learning_CVPR_2019_paper.html" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/multi-camera-geography/
  - /challenges/broadcast-and-timebases/
  - /solutions/synchronization/dtw-python/
  - /solutions/events-and-replay/sn-replay-grounding/
  - /solutions/synchronization/learned-video-alignment/
---

## The design question

Which frames from two sources show the same instant? Until that is answered, a second camera is a
separate film. What the broadcast feed is, and why it cuts and replays, is described in
[Two cameras, two clocks]({{ '/challenges/broadcast-and-timebases/' | relative_url }}). This study is about
the design of the mapping: the first prerequisite of
[the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}).

## Evidence for alignment

| Evidence | Strength | Limit |
|---|---|---|
| Native timecode | Exact when present | Often absent or reset at cuts |
| On-screen match clock | Readable anchor | Hidden in replays and close-ups |
| Shared audio | Dense, continuous | Needs the same audio in both feeds |
| Movement fingerprints | Uses the play itself | Ambiguous in static phases |
| Event anchors with a robust offset fit | A few good anchors fix a segment | Anchors must be independent |
| Constrained dynamic time warping | Handles drift | Invents matches without constraints |
| Learned embeddings | Aligns without hand features | Training data, opaque errors |

## The mapping record

One record per broadcast segment: the tactical frame range it corresponds to, its type, the evidence that
produced the link, and the timing uncertainty. Downstream stages read the uncertainty before the frame.

## Uncertainty inside a segment

{% include wiki/motif.html id="bp-s-drift" caption="Two anchors lock one live segment. Between them the clocks drift, so the timing uncertainty is smallest at an anchor and widest half-way. Slow motion changes the frame ratio, and no single offset describes it." %}

## What breaks it in real football

- **A replay is not an offset.** The mapping is non-monotonic across segments, and one tactical instant can
  appear on screen more than once.
- **Crowd shots have no match in them.** A bench or the stands cannot be aligned to play. Leave them unmapped.

## How to judge it

Check alignment against contact anchors that were not used to fit it: a kick-off, a header, a bounce.
Report the error in frames, per segment type, and prefer an honest gap to a confident wrong link.
