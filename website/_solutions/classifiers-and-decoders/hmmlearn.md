---
title: "Hidden Markov models (hmmlearn)"
kicker: "Classifiers and decoders"
summary: "The generative sequence model: hidden states, noisy observations, exact inference. Forward-backward gives per-frame posteriors; Viterbi gives the single best path."
group: classifiers-and-decoders
order: 20
chips: ["Sequence", "Classical", "Labels optional", "BSD-3-Clause"]
motif: gauge
motif_caption: "Forward-backward combines past, present and future evidence into a confidence for each state."
motif_labels: ["State posterior", "Past", "This frame", "Future"]
facts:
  - { k: "Modality", v: "Per-frame features or probabilities" }
  - { k: "Output", v: "State posteriors and the best state path" }
  - { k: "Evidence", v: "Rabiner's tutorial (1989); long-standing library" }
  - { k: "Code and weights", v: "hmmlearn, in limited-maintenance mode; no football parameters" }
  - { k: "Licence", v: "BSD-3-Clause" }
verdict: { label: "Our read", text: "The reference model for sequence inference. Learn it from the library. For three states, write the decode yourself." }
sources:
  - { title: "hmmlearn: hidden Markov models in Python (repository)", url: "https://github.com/hmmlearn/hmmlearn" }
  - { title: "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition (Rabiner, 1989)", url: "https://doi.org/10.1109/5.18626" }
related:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hsmmlearn/
  - /solutions/classifiers-and-decoders/pytorch-crf/
---
A hidden Markov model says the match has a hidden state on every frame, home ball, away ball or dead, and that what we observe is a noisy consequence of it. Two tables define the model: transition probabilities between states, and an emission distribution for each state.

Three algorithms come with it, all exact, all in Rabiner's tutorial. Forward-backward computes the probability of each state on each frame given the entire sequence. Viterbi finds the single most probable path. Baum-Welch fits the tables from unlabelled sequences by expectation maximisation.

hmmlearn implements all three behind a scikit-learn interface, with Gaussian, mixture and categorical emissions. The project describes itself as being in limited-maintenance mode: stable, not evolving.

## Where it wins

- Posteriors, not only labels. Forward-backward says how sure the model is on each frame, which a best path alone hides.
- It can be fitted without labels, or run with tables set by hand from football knowledge.
- Exact and cheap: linear in frames, quadratic in a state count of three.
- A common language. Every sequence method in this family is an HMM with something relaxed.

## What it costs

- Emissions are assumed independent given the state. Football cues overlap heavily, and a naive emission model counts them twice.
- Unsupervised fitting finds the states that explain the data best. They need not be H, A and D.
- Spell lengths follow a geometric distribution, as in any first-order chain.
- One emission family per state fits possession evidence poorly. Real evidence is a mix of distances, flags and absences.

## How it plugs into possession

Mostly as mathematics. The decode at the heart of a possession pipeline is HMM inference whether or not this library is imported: states, switching costs, per-frame evidence, [Viterbi]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}). For three states the algorithm is a few lines of array code, and owning those lines keeps a build small and deterministic.

The part worth borrowing even then is forward-backward. Posterior confidence per frame separates the stretches a decoder knows from the stretches it bridged.
