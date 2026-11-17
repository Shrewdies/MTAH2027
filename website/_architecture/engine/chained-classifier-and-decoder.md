---
title: Evidence, then a decoder
kicker: The engine
summary: "Where should temporal consistency live: inside one model that reads many frames, or in a stage of its own behind the evidence? One learner, or two machines in a chain. The answer decides what can be tested, and what the design needs in labels."
group: engine
order: 10
chips: [One model or two, Decoder, Auditable, Fielded]
motif: bp-chain
icon: pipeline
motif_caption: "The two-machine answer. Evidence flows into the decoder and also past it, into the audit, so every frame the decoder changed can be shown against the raw scores."
motif_labels: [Observations, Frame evidence, H / A / D scores, Sequence decoder, Spells, Audit]
facts:
  - { k: Option one, v: "One multi-frame model: time lives in the weights" }
  - { k: Option two, v: "Evidence per frame, then a decoder over the half" }
  - { k: What decides, v: "The labels that exist, and what must be auditable" }
  - { k: Contract, v: "Three scores per frame between the stages" }
verdict:
  label: Our read
  text: "Separating evidence from decision is the single most useful cut in possession inference. It turns one opaque model into two questions that each have a right answer. One model is the stronger choice only when labelled matches from the same kind of tracking are plentiful."
call:
  title: Why the engine is split in two
  constraint: Competition rules
  text: "The fixture has no labels, and the rules forbid training or tuning on its answers. A learned end-to-end classifier had nothing legitimate to learn from, so football evidence is scored by fixed physical rules and an exact decoder writes the sequence. Seven dials remained, all of them set away from the match."
sources:
  - { title: "Borghesi et al. (2023), ball possession with a temporal convolutional network", url: "https://doi.org/10.1016/j.eswa.2023.119780" }
  - { title: "Zaheer et al. (2017), Deep Sets", url: "https://arxiv.org/abs/1703.06114" }
  - { title: "PyTorch-TCN", url: "https://github.com/paul-krug/pytorch-tcn" }
  - { title: "PyTorch tutorial: sequence models with a CRF layer", url: "https://docs.pytorch.org/tutorials/beginner/nlp/advanced_tutorial.html" }
  - { title: "Technical report: Who has the ball?", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/TECHNICAL.md" }
related:
  - /architecture/decoding-alternatives/
  - /architecture/the-shrewdies-decoder/
  - /challenges/temporal-decoding/
  - /solutions/direct-possession/borghesi-possession-tcn/
  - /solutions/classifiers-and-decoders/set-encoders/
  - /solutions/classifiers-and-decoders/pytorch-tcn/
---

## The design question

Should one model own both jobs, reading the evidence and keeping the sequence coherent, or should they be
two machines? Why possession needs a sequence decision at all is set out in
[Why possession is a decoding problem]({{ '/challenges/temporal-decoding/' | relative_url }}). This study is
about where that decision lives.

## The two answers

| | One model, many frames | Evidence, then a decoder |
|---|---|---|
| Where time lives | Inside the weights | In a stage of its own |
| Needs | Frame-level labels from other matches | Scores per frame; labels optional |
| Guarantees | Nothing about coherent spells | The best path under stated costs |
| Inspect it by | Its outputs only | Each stage, and the difference between them |
| Breaks when | Labels are scarce or from another provider | A heavy decoder erases real short spells |

{% include wiki/motif.html id="bp-window" caption="The one-model answer. A window slides over stacked signals and one learner reads it. What it knows about time, it learned from labels, and nothing in it forbids a flicker." %}

## If time lives inside the model

| Input representation | Learner | What it captures |
|---|---|---|
| Engineered window features | LightGBM, XGBoost | Trends and time statistics, made explicit |
| Per-frame feature matrix over time | 1D temporal convolution | Local to long-range patterns |
| Player sets over time | Deep Sets or Set Transformer with a TCN | Order-free players, no fixed slots |
| Player graphs over time | Graph network with LSTM or attention | Interactions between players |
| Occupancy maps over time | Spatio-temporal CNN | The match as a moving field |

The model discovers that a pass in flight still belongs to the passing team without anyone writing the
rule, and more labelled matches make it better without redesign. That is its case.

## If time gets its own stage

- **Noise dies without retraining.** A weak away spike inside a home pass is suppressed by the decoder. The
  evidence stage is untouched.
- **Every change is visible.** The raw scores stay on file, so the decoder's edits can be listed frame by frame.
- **Each stage has its own test.** Evidence is tested on fabricated scenes with a known answer. The decoder
  is tested on sequences.

Stage one can be a trained classifier or a set of physical rules. Stage two is a choice of its own:
[Seven ways to decode a match]({{ '/architecture/decoding-alternatives/' | relative_url }}).

## What breaks each in real football

- **One model: flicker.** Outputs alternate through a scramble, and every flip cuts a possession in two.
- **One model: provider shift.** Tracking from one vendor is not tracking from another. Noise, gaps and the
  meaning of "possession" all move.
- **Two machines: overconfident evidence.** If stage one shouts, stage two cannot correct it. The scale of
  the scores matters as much as their sign.

## How to judge it

Train and test on whole, separate matches. Score the raw per-frame output alone, then the same output
behind a decoder, on both official metrics. If a decoder improves a multi-frame model, the model was not
carrying the temporal load. If a decoder lifts the frame score and drops the spell score, it is smoothing
away football.
