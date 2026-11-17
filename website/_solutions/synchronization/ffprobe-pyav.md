---
title: "FFprobe and PyAV"
kicker: "Synchronisation"
summary: "Read what the video file says about time: presentation timestamps, time base, real frame rate. The first step of any synchronisation, and the one most often skipped."
group: synchronization
order: 10
chips: ["Video", "Timebase", "No training", "LGPL / BSD"]
motif: timeline
motif_caption: "A stream has its own clock. Frames can start late, drop out or drift from the nominal rate."
motif_labels: ["First half", "Second half", "Dropped frames", "Start offset"]
facts:
  - { k: "Modality", v: "Any media container" }
  - { k: "Output", v: "Per-frame timestamps and stream metadata" }
  - { k: "Evidence", v: "Official FFmpeg documentation; widely used Python bindings" }
  - { k: "Code and weights", v: "Command-line tool and Python library; no weights" }
  - { k: "Licence", v: "FFmpeg LGPL or GPL depending on the build; PyAV BSD-3-Clause" }
verdict: { label: "Our read", text: "Five minutes of inspection that prevents a class of invisible errors. Never count frames you can timestamp." }
sources:
  - { title: "ffprobe documentation (FFmpeg)", url: "https://ffmpeg.org/ffprobe.html" }
  - { title: "PyAV: Python bindings for the FFmpeg libraries (repository)", url: "https://github.com/PyAV-Org/PyAV" }
related:
  - /solutions/synchronization/pyroomacoustics/
  - /solutions/synchronization/dtw-python/
  - /solutions/events-and-replay/pyscenedetect/
---
"Frame 4,512 of a 25 fps video" sounds like a time. It is an assumption. A video file stores a presentation timestamp for every frame, in units of the stream's time base. The frame rate in the header is a summary. Frames can be dropped, duplicated or irregularly spaced, a stream can start at a non-zero timestamp, and a re-encoded file may not be what its header claims.

FFprobe is FFmpeg's inspection tool. It reports container and stream metadata and can list every frame's timestamp and duration. PyAV exposes the same libraries to Python, so code can decode frames with their true timestamps attached instead of counting from zero.

## Where it wins

- The truth about the file: timestamps, time base, start offset, declared against actual frame rate, embedded timecode.
- It catches variable frame rate and dropped frames before they become a drift that looks like a modelling error.
- Seeking by timestamp is the reliable way to fetch the frame at a given tracking time.
- Mature, free and available everywhere.

## What it costs

- It tells you the file's clock, not the stadium's. Stream timestamps say nothing about when the camera started relative to the tracking system.
- Metadata can be wrong or missing, especially after re-encoding.
- FFmpeg's licence depends on how it was built. Distributing a build needs care.

## How it plugs into possession

Possession labels are per frame, and "frame" must mean the same thing in the tracking, the video and the answer file. The mapping from frame index to time is the foundation, and it is cheap to check. List the timestamps, confirm they are uniform, record the start offset.

Do this before any content-based alignment. [Audio]({{ '/solutions/synchronization/pyroomacoustics/' | relative_url }}), [geometric]({{ '/solutions/synchronization/geometric-sync/' | relative_url }}) and [learned]({{ '/solutions/synchronization/learned-video-alignment/' | relative_url }}) synchronisation all estimate an offset on top of each stream's own timeline. If a timeline is irregular, there is no single offset to find.
