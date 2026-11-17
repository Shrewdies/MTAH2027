---
title: "Bayesian online change-point detection"
kicker: "Classifiers and decoders"
summary: "A running posterior over how long the current regime has lasted. When it collapses to zero, something changed."
group: classifiers-and-decoders
order: 100
chips: ["Time series", "Classical", "Online", "No training"]
motif: changepoint
motif_caption: "Run length grows while the signal behaves and drops to zero when a new regime begins."
motif_labels: ["Signal", "Run resets", "Regimes"]
facts:
  - { k: "Modality", v: "Any time series, one observation at a time" }
  - { k: "Output", v: "Run-length posterior and change probability at every step" }
  - { k: "Evidence", v: "Adams and MacKay (2007)" }
  - { k: "Code and weights", v: "Method paper; several community implementations" }
  - { k: "Licence", v: "Set by the implementation chosen" }
verdict: { label: "Our read", text: "The online, probabilistic way to say something changed. Offline, an exact decode with the same evidence does more." }
sources:
  - { title: "Bayesian Online Changepoint Detection (Adams and MacKay, arXiv 0710.3742)", url: "https://arxiv.org/abs/0710.3742" }
related:
  - /solutions/physics-and-features/ruptures/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hsmmlearn/
---
Adams and MacKay's algorithm tracks one quantity: the run length, the number of steps since the last change-point. At each new observation the run either grows by one or resets to zero. The algorithm keeps a full probability distribution over run length and updates it recursively.

Two ingredients define it. A hazard function gives the prior chance of a change at each step, and may depend on how long the run has lasted. A predictive model says how likely the new observation is under each candidate run, using only data since that run began. Observations that fit the current regime shift probability towards longer runs. A surprising one moves it to zero.

The output is richer than a list of breaks. At every step it gives a probability that a change has just happened and a belief about the regime's age.

## Where it wins

- Online and causal by construction. It suits live possession, where [ruptures]({{ '/solutions/physics-and-features/ruptures/' | relative_url }}) cannot go.
- Probabilistic output. A change probability can be used directly as soft evidence.
- The hazard function is a duration prior in disguise. It can encode that possessions rarely last one second or one minute.
- No labels.

## What it costs

- It detects that the signal changed, not what changed. A pass to a team-mate is as much a change-point in ball motion as a turnover.
- Causality is a handicap offline. With the whole match available, ignoring the future wastes information.
- The predictive model must suit the signal. Gaussian assumptions about ball speed are crude.
- It is sensitive to the hazard rate, which has no label-free calibration for football.

## How it plugs into possession

As a soft boundary signal for a decoder, and as the live counterpart to an offline decode. Change probability on ball kinematics marks candidate touches. A sequence model decides which of them move possession.

Its natural home is streaming. A possession system that must answer during play cannot wait for the half to end, and a run-length posterior is the principled way to say "probably changed, a few frames ago".
