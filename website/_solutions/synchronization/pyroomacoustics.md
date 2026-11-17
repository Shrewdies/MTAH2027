---
title: "Audio offset estimation (GCC-PHAT)"
kicker: "Synchronisation"
summary: "Two recordings of the same whistle differ by a delay. Generalised cross-correlation finds it far below the length of a video frame."
group: synchronization
order: 20
chips: ["Audio", "Alignment", "Classical", "MIT"]
motif: spikes
motif_caption: "Sharp sounds appear in both recordings. The lag between them is the offset."
motif_labels: ["Whistle", "Ball strike", "Crowd"]
facts:
  - { k: "Modality", v: "Two audio tracks of the same event" }
  - { k: "Output", v: "The time delay between them" }
  - { k: "Evidence", v: "Academic signal-processing library with documentation" }
  - { k: "Code and weights", v: "pyroomacoustics package; no weights" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The finest clock available when both feeds can hear the pitch. Check the speed of sound before trusting it." }
sources:
  - { title: "pyroomacoustics: audio signal processing in Python (repository)", url: "https://github.com/LCAV/pyroomacoustics" }
related:
  - /solutions/synchronization/ffprobe-pyav/
  - /solutions/synchronization/dtw-python/
  - /solutions/synchronization/geometric-sync/
---
Sound is the most precise clock in a stadium. Audio is sampled tens of thousands of times a second, where video offers 25 frames. If two recordings share sound, the delay between them can be measured far more finely than one frame.

Cross-correlation slides one signal over the other and finds the lag where they agree best. GCC-PHAT, generalised cross-correlation with phase transform, whitens the spectrum first and keeps only phase. The peak becomes sharp and robust to differences in loudness and frequency response between microphones. pyroomacoustics, an audio signal-processing library, provides the building blocks.

## Where it wins

- Sub-frame precision from a signal most recordings already carry.
- Independent of image content. It works across cameras that share no view.
- Sharp transients, the referee's whistle and the strike of the ball, are ideal correlation targets.
- Cheap to compute.

## What it costs

- Both sources need audio from the same acoustic scene. Tracking data has none, and a tactical camera may have none.
- Broadcast audio is a mix of commentary and effects, with delays added in production. It may not be locked to the picture.
- Sound travels at roughly 340 metres per second. Microphones 100 metres apart hear the same whistle 0.3 seconds apart, about seven frames at 25 fps, unless their positions are accounted for.
- Crowd noise is diffuse and correlates poorly.

## How it plugs into possession

Camera to camera, not camera to tracking. When a tactical feed and a broadcast feed both carry stadium sound, audio gives the coarse offset between them almost for free, and a [windowed DTW]({{ '/solutions/synchronization/dtw-python/' | relative_url }}) or a geometric check refines it.

It contributes nothing to aligning video with tracking, the alignment that possession inference from mixed sources needs most. There the shared signal is the players' positions, the subject of [geometric synchronisation]({{ '/solutions/synchronization/geometric-sync/' | relative_url }}).
