---
layout: wiki-hub
title: Solutions
permalink: /solutions/
collection_index: solutions
families: true
summary: "The landscape of models, methods and tools for football intelligence, mapped and judged. Seven families, one question put to each: what does it tell us about who has the ball?"
motif: sol-chain
icon: pipeline
motif_caption: "Possession inference is a chain. Six families own one link each; the seventh answers in one step."
motif_labels: ["0"]
stats:
  - { value: "7", label: "families" }
  - { value: "{count}", label: "solutions judged" }
  - { value: "74", label: "models, methods and tools reviewed" }
  - { value: "3", label: "ruled out by a licence or a rule" }
featured_title: Start here
featured:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/direct-possession/metrica-baseline/
  - /solutions/direct-possession/pathcrf/
  - /solutions/physics-and-features/pitch-control/
  - /solutions/classifiers-and-decoders/gradient-boosted-trees/
  - /solutions/vision-and-calibration/sn-gamestate/
groups:
  - key: direct-possession
    title: Direct possession
    url: /solutions/direct-possession/
    motif: ribbon
    motif_labels: ["Per-frame answers", "Possession", "Home", "Away", "Dead ball"]
    blurb: "Methods that answer the question itself: which team has the ball on this frame. From the organisers' nearest-player rule to a graph model that needs no ball at all."
    points:
      - "Best task fit on the map: the output is the label."
      - "The rules go silent when the ball does."
      - "The learned models need labels and identities most feeds lack."
  - key: physics-and-features
    title: Physics and features
    url: /solutions/physics-and-features/
    motif: field
    motif_labels: ["Home arrives first", "Away arrives first"]
    blurb: "Distances, arrival times, pitch control, filtered trajectories. Evidence computed from physics, with nothing trained and every number traceable."
    points:
      - "Label-free and deterministic."
      - "Turns who is closest into who gets there first."
      - "Evidence, never the answer: controlling space is not having the ball."
  - key: classifiers-and-decoders
    title: Classifiers and decoders
    url: /solutions/classifiers-and-decoders/
    motif: decoder
    motif_labels: ["Home", "Away", "Dead ball", "Best path"]
    blurb: "Models that turn evidence into probabilities, and decoders that turn probabilities into possessions. Home of Viterbi, the algorithm our decoder is built on."
    points:
      - "Classifiers need labels. Decoders need only evidence."
      - "Frame accuracy does not buy coherent possessions."
      - "The algorithm our decoder runs."
  - key: vision-and-calibration
    title: Vision and calibration
    url: /solutions/vision-and-calibration/
    motif: sol-vision-chain
    motif_labels: ["Detect", "Track", "Calibrate", "Missed ball", "Identity switch", "Metres off"]
    blurb: "Detectors, trackers and calibrators that rebuild players, ball and camera from video. The route to positions when a tracking feed is missing or has holes."
    points:
      - "Detect, track, calibrate: three stages, one error budget."
      - "The ball is the hardest object on the pitch to see."
      - "The most varied licences on the map."
  - key: events-and-replay
    title: Events and replay
    url: /solutions/events-and-replay/
    motif: sol-anchors
    motif_labels: ["±1 s, 25 frames", "Spotted events", "Possession between"]
    blurb: "Spotters that timestamp passes, drives and tackles, and the tools that untangle a broadcast edit. Every possession change is an event; not every event is a change."
    points:
      - "Events anchor possession changes."
      - "Scored at one second: 25 frames of doubt."
      - "Silent between touches, which is most of the match."
  - key: synchronization
    title: Synchronisation
    url: /solutions/synchronization/
    motif: sync
    motif_labels: ["Video clock", "Tracking clock", "Aligned"]
    blurb: "Putting video, audio and tracking on one clock. Invisible when right. When wrong, every boundary moves and every comparison is between two different moments."
    points:
      - "Ten frames off moves every boundary by 0.4 s."
      - "Check the file's own clock first."
      - "On a pitch, projected player positions are the best clock."
  - key: readers-and-formats
    title: Readers and formats
    url: /solutions/readers-and-formats/
    motif: pipeline
    motif_labels: ["Provider file", "Parser", "One model", "Coordinates", "Dataframe"]
    blurb: "Libraries that load provider files into one model and pin events to frames. The tooling under every cross-provider test. The datasets themselves live in the Datasets section."
    points:
      - "One loader across providers."
      - "Events pinned to tracking frames."
      - "Formats are standardised. Meanings are not."
---
## Where our own system sits

Everything on this map is someone else's method, read for what it tells us about who has the ball. Our own system runs one of them: an exact [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) per half, over football evidence scored on every frame. The design is drawn in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}), and its result against the organisers' [nearest-player baseline]({{ '/solutions/direct-possession/metrica-baseline/' | relative_url }}) is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page.

## How to read this map

Each family owns one link of the chain above, and each family page explains how its methods work, how to choose between them, what they cannot do and where our decoder stands. Every entry answers the same questions: how it works, where it wins, what it costs, how it plugs into possession. Where a licence or a competition rule put a tool out of reach, the entry says so under "Our call". Three do. The calls that shaped our own design are in [Architecture]({{ '/architecture/' | relative_url }}).
