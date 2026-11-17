---
title: "DataBallPy"
kicker: "Readers and formats"
summary: "Loads tracking and event data, then synchronises the two, so that each event sits on the tracking frame where it happened."
group: readers-and-formats
order: 20
chips: ["Tracking + events", "Reader", "Event sync", "MIT"]
motif: sync
motif_caption: "Events are logged on one clock and tracking on another. Synchronisation pins each event to its frame."
motif_labels: ["Event feed", "Tracking frames", "Synchronised"]
facts:
  - { k: "Modality", v: "Tracking and event data" }
  - { k: "Output", v: "Synchronised dataframes and analytical representations" }
  - { k: "Evidence", v: "Documented open Python package" }
  - { k: "Code and weights", v: "Python package" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The reader to use when events must land on frames. Its synchronisation is the feature. Keep its event columns out of your model's inputs." }
sources:
  - { title: "databallpy: read, preprocess, visualise and synchronise soccer event and tracking data (repository)", url: "https://github.com/Alek050/databallpy" }
related:
  - /solutions/readers-and-formats/kloppy/
  - /solutions/direct-possession/vidal-event-tracking/
  - /solutions/synchronization/dtw-python/
  - /datasets/dfl-idsse/
---
Event data and tracking data describe the same match on different clocks. Events are logged by people, with timestamps that trail the action. Tracking is sampled 25 times a second by machines. Asking where everyone stood when a pass was played means putting the event on the right frame.

DataBallPy treats that as a central job. It reads tracking and event files into dataframes, then synchronises them, so that events carry the tracking frame they belong to. Around that it provides preprocessing and visualisation for the combined data.

## Where it wins

- It solves event-to-tracking alignment, which most loaders leave to the user.
- Synchronised events are touch labels on the tracking clock, the best cheap supervision there is for possession boundaries.
- One package from files to analysis-ready frames.
- MIT.

## What it costs

- Synchronisation quality depends on both feeds. A missing ball track or anonymous players leave little to match against.
- A dataframe-centric design is convenient, and slower than arrays at match scale.
- Event-derived columns sit next to tracking columns. Using them as model inputs leaks the answer.

## How it plugs into possession

For building reference labels on external matches. Synchronised events turn into possession spells directly: a pass by a home player starts or continues a home spell at a known frame. That is how event data becomes a per-frame possession reference where a provider ships no possession flag.

The leak warning is the practical one. A possession method must be validated with event-derived columns removed from its inputs, or it is being graded on an open book.

[kloppy]({{ '/solutions/readers-and-formats/kloppy/' | relative_url }}) covers the broader range of providers. The datasets themselves are under [Datasets]({{ '/datasets/' | relative_url }}).
