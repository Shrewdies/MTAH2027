---
title: "Possession TCN (Borghesi et al.)"
kicker: "Direct possession"
summary: "The closest published relative of the H/A/D task: a permutation-invariant player encoder feeding a temporal convolutional network, trained to say who has the ball from tracking."
group: direct-possession
order: 30
chips: ["Tracking", "Learned", "Needs labels", "Paper only"]
motif: pipeline
motif_caption: "Players in, pooled per frame, read over time, then two questions: live or dead, and whose ball."
motif_labels: ["Players", "Encoder", "Pooling", "TCN", "Live or dead", "Which team"]
facts:
  - { k: "Modality", v: "Tracking data" }
  - { k: "Output", v: "Possession state per frame" }
  - { k: "Evidence", v: "Journal paper (2023); 86.2% possession accuracy, own data" }
  - { k: "Code and weights", v: "Paper only" }
  - { k: "Licence", v: "Not applicable: no released code" }
verdict: { label: "Our read", text: "The reference architecture for supervised possession from tracking. Borrow the factorisation today; train the network when the labels exist." }
sources:
  - { title: "Using Temporal Convolutional Networks to estimate ball possession in soccer games (Borghesi, Costa, Morra, Lamberti; Expert Systems with Applications, 2023)", url: "https://doi.org/10.1016/j.eswa.2023.119780" }
related:
  - /solutions/classifiers-and-decoders/pytorch-tcn/
  - /solutions/classifiers-and-decoders/set-encoders/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
---
Borghesi and colleagues ask the question the Initial Challenge asks: given tracking, which team has the ball on each frame, or is play stopped? Their answer is a compact deep model built from two ideas that have since become standard.

First, players are a set, not a list. Each player passes through the same encoder and the results are pooled, so the output cannot change when tracking slots are renumbered. Second, possession is temporal. A temporal convolutional network reads a window of pooled frames, so the decision on one frame sees the seconds around it.

The paper also tests a factorisation worth stealing. Instead of one three-way choice, split the problem in two: is the ball live or dead, and if live, which team controls it? The two questions rest on different evidence and carry different error costs. The authors report 86.2% possession accuracy on their own data.

## Where it wins

- Task match. No translation from events or phases is needed. The output is the label.
- Slot-order invariance is built in, which matters for any feed where players are anonymous within a team.
- The live/dead and team factorisation separates a stoppage question from a control question.
- It is small by deep-learning standards: a TCN over pooled features.

## What it costs

- There is no public code and no public weights. Using it means rebuilding and training it.
- Training needs frame-level possession labels from the same kind of tracking it will meet in use.
- The headline number is frame accuracy on the authors' data. A model that is right on 86% of frames can still break possessions apart, and spell metrics punish exactly that.
- Convolutional context smooths, but nothing in a TCN guarantees a coherent sequence. It still wants a decoder behind it.

## How it plugs into possession

As the emission model. A network like this turns each frame into three scores, and a structured decoder such as [Viterbi]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) turns the scores into possessions.

The architecture is the template for any supervised H/A/D model on tracking: a [set encoder]({{ '/solutions/classifiers-and-decoders/set-encoders/' | relative_url }}) in front, [temporal convolution]({{ '/solutions/classifiers-and-decoders/pytorch-tcn/' | relative_url }}) in the middle, sequence decoding at the end. The factorisation needs no network at all. A hand-specified evidence model can score "dead" and "whose ball" from separate cues just as well.

Training one needs frame labels from the kind of tracking it will meet, and the Initial Challenge allowed none on the match. That call is explained in [Evidence, then a decoder]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}).
