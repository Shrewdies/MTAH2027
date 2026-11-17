---
title: Experts, gates and referees
kicker: The engine
summary: "When no single model is right everywhere, several can be combined: frame by frame through a gate that knows whom to trust, or segment by segment through a referee that rules on a disputed window. Either way the gain is the independence of their errors."
group: engine
order: 30
chips: [Ensemble, Gating, Adjudication]
motif: bp-gate
icon: ensemble
motif_caption: "Level one, on every frame. The tracker loses the ball, so the gate mutes the ball-aware expert and moves the weight to the ones that can still see. Each expert's scores stay on file beside the result."
facts:
  - { k: Level one, v: "Combine scores on each frame: vote, average, stack, gate" }
  - { k: Level two, v: "Rule on a disputed segment as one object" }
  - { k: Needs, v: "Calibrated scores and validity masks" }
  - { k: Trap, v: "Shared inputs, shared errors" }
verdict:
  label: Our read
  text: "An ensemble is worth exactly the independence of its errors. Five models reading one tracking stream are one witness, five times. And the last decision belongs on the possession, because that is what the metric counts: choosing between whole validated sequences is safer than a clever local rule with nothing to learn from."
sources:
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "Borghesi et al. (2023), ball possession with a temporal convolutional network", url: "https://doi.org/10.1016/j.eswa.2023.119780" }
  - { title: "Sarawagi and Cohen (2004), semi-Markov conditional random fields", url: "https://papers.neurips.cc/paper/2648-semi-markov-conditional-random-fields-for-information-extraction.pdf" }
  - { title: "Official evaluation: the possession-interval metric", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
related:
  - /architecture/decoding-alternatives/
  - /architecture/single-source-of-truth/
  - /architecture/confidence-and-provenance/
  - /solutions/direct-possession/pathcrf/
  - /solutions/physics-and-features/ruptures/
  - /solutions/classifiers-and-decoders/bocpd/
---

## The design question

When several models or several decoded sequences disagree, who decides, and at what grain? The experts in
possession fail under different observation conditions, which is the only reason to run more than one.

## Who to trust, and when

| Expert | Most credible when | Distrust when |
|---|---|---|
| Ball-aware physical model | Ball tracked, trajectory smooth | Ball invisible or in the air |
| Ball-free set or graph model | Player motion reliable | Dropouts, identity confusion |
| Live or dead specialist | Restart and stoppage cues present | The only cue is a missing ball |
| Tactical-phase tags | Phase is distinctive | Phases overlap, tag is wrong |
| Broadcast-derived expert | Live shot, valid geometry | Replay, close-up, unknown mapping |

## Level one: combine the scores on each frame

| Strategy | How | Costs |
|---|---|---|
| Majority vote | Count hard labels | Ignores confidence |
| Score averaging | Mean of class scores | Assumes equal calibration |
| Stacking | A learner on top of experts | Needs held-out labels |
| Rule gate | Switch expert by condition | Hand-set thresholds |
| Mixture of experts | Weights from reliability features | The gate can trust the wrong one |

## Level two: rule on the segment

Decoded sequences agree on most of a match and split on brief windows. A frame-level vote is the wrong
court for those. The question is about a segment, so the ruling should be too.

{% include wiki/motif.html id="bp-adjudicate" caption="Three sequences, one disputed window. Ruled on as one object, it decides whether this stretch holds one, two or three possessions." %}

| Design | How | Wins | Costs |
|---|---|---|---|
| Global selection | Pick one whole decoded sequence per half | Hard to overfit, easy to validate | Cannot mix the best of two |
| Local adjudication | Rule on each disputed window | Takes the best of each sequence | Needs labelled segments from other matches |

A referee can weigh the raw scores before smoothing, a transition cue at the boundary, the plausibility of
the segment's length and whether the sensor could see. Each has a trap: overconfident scores, coarse
timing, real one-touch spells, reliability shared by every expert.

## What breaks it in real football

- **A gate fooled by the same blackout.** If the reliability feature is "ball tracked", it tells the gate
  nothing in a crowded box, where every expert is guessing.
- **Uncalibrated confidence.** One expert that always says 0.99 outvotes three that are honestly unsure.
- **The window that looks like noise.** A press wins the ball for two seconds and loses it again. The smooth
  reading erases a real possession.
- **Shared ancestry.** Experts built on one tracker err together. That failure is set out in
  [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}).

## How to judge it

Measure the correlation of errors between experts before measuring the ensemble, then remove one expert at
a time. An expert whose removal changes nothing was a passenger. Score a referee on the disputed windows
only, by type: false split, false merge, late boundary. Its value is the spells it saves minus the spells
it breaks.
