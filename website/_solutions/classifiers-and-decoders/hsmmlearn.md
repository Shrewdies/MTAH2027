---
title: "Hidden semi-Markov models (hsmmlearn)"
kicker: "Classifiers and decoders"
summary: "An HMM in which each state chooses how long to last. The natural model for spells, and the expensive one."
group: classifiers-and-decoders
order: 30
chips: ["Sequence", "Classical", "Duration-aware", "GPL-3.0"]
motif: ribbon
motif_caption: "Each state brings its own duration distribution, so the decoded spells have a believable rhythm."
motif_labels: ["Frame evidence", "Spells by duration", "Home", "Away", "Dead ball"]
facts:
  - { k: "Modality", v: "Per-frame evidence plus a duration distribution per state" }
  - { k: "Output", v: "Segments, each with a state and a length" }
  - { k: "Evidence", v: "Yu's survey (Artificial Intelligence, 2010)" }
  - { k: "Code and weights", v: "hsmmlearn reference library, archived in 2023" }
  - { k: "Licence", v: "GPL-3.0" }
verdict: { label: "Our read", text: "The right model for spells in theory. In practice, exhaust switching costs first." }
sources:
  - { title: "hsmmlearn: hidden semi-Markov models with explicit durations (archived repository)", url: "https://github.com/jvkersch/hsmmlearn" }
  - { title: "Hidden semi-Markov models (Yu, Artificial Intelligence, 2010)", url: "https://doi.org/10.1016/j.artint.2009.11.011" }
related:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hmmlearn/
  - /solutions/physics-and-features/ruptures/
---
A first-order Markov chain has no memory of how long it has been in a state. Each frame it stays with a fixed probability, so spell lengths follow a geometric distribution and the most likely duration is always the shortest. Football does not look like that. A goal kick takes a typical time. A possession under a high press has a different length profile from one in settled build-up.

A hidden semi-Markov model makes duration explicit. On entering a state the model draws a length from that state's own duration distribution, emits that many observations, then moves on. Inference is still dynamic programming, now over states and durations together, as laid out in Yu's survey.

hsmmlearn is a compact reference implementation of the explicit-duration model. Its repository was archived in 2023.

## Where it wins

- Spells are the unit of the model, as they are the unit of spell-based metrics.
- Duration knowledge enters as a distribution, not as a blunt minimum-length filter.
- Different states get different rhythms: dead balls long, contested possessions short.
- Inference remains exact.

## What it costs

- Decoding cost grows with the longest duration considered. At 25 fps a 60-second stoppage is 1,500 frames of duration to search.
- Duration distributions must come from somewhere: labels or assumptions.
- A wrong prior is destructive. Penalise short spells too hard and real one-touch possessions vanish.
- The reference library is archived and GPL-3.0. In a permissively licensed project the algorithm is reimplemented, not imported.

## How it plugs into possession

As the principled upgrade to a [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) when duration errors dominate. If a decoder's mistakes are spells of implausible length, three-frame possessions or dead balls that end too early, a semi-Markov model treats the cause where post-hoc filters treat the symptom.

Much of the benefit is available more cheaply. Minimum-duration constraints and state-specific switching costs approximate duration structure inside an ordinary Viterbi pass, at a fraction of the cost.
