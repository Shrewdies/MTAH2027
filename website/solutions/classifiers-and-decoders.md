---
layout: wiki-hub
title: "Classifiers and decoders"
permalink: /solutions/classifiers-and-decoders/
collection_index: solutions
only_group: classifiers-and-decoders
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Models that turn evidence into probabilities, and decoders that turn probabilities into possessions. The family our evidence decoder belongs to."
motif: decoder
motif_caption: "Scores for three states on every frame, and the one best path through them."
motif_labels: ["Home", "Away", "Dead ball", "Best path"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "1", label: "fielded: Viterbi decoding" }
  - { value: "4", label: "need no labels" }
---
## One picture: two jobs

{% include wiki/motif.html id="sol-evidence-decoder" labels="Ball control|Out of play|Stillness|Tags|Exact decode|Decoded possession" caption="Evidence is sparse and noisy, and one lane goes dark when the ball is untracked. One exact decode turns all of it into a single coherent sequence." %}

Two jobs live in this family, and keeping them apart is the whole idea. **Scoring** turns each frame's evidence into support for home, away or dead. **Decoding** turns those per-frame scores into a sequence that looks like football: possessions that last, changes that happen at a touch.

Scoring can be learned, with trees, convolutions or graph networks, or specified by hand. Decoding is exact mathematics either way.

This family is the last link of the chain. Everything upstream produces evidence. Here it becomes an answer.

## How to choose inside it

| Entry | Labels | Ball and identities | Compute |
|---|---|---|---|
| [Viterbi decoding]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) | None | Neither. A hidden ball is a frame without evidence | Seconds on a CPU |
| [Hidden Markov models]({{ '/solutions/classifiers-and-decoders/hmmlearn/' | relative_url }}) | Optional | Neither | Light |
| [Hidden semi-Markov models]({{ '/solutions/classifiers-and-decoders/hsmmlearn/' | relative_url }}) | For durations, or assumptions | Neither | Grows with the longest spell |
| [Linear-chain CRF]({{ '/solutions/classifiers-and-decoders/pytorch-crf/' | relative_url }}) | Labelled sequences | Neither | Light |
| [Gradient-boosted trees]({{ '/solutions/classifiers-and-decoders/gradient-boosted-trees/' | relative_url }}) | Frame labels | A hidden ball is a value. No identities | CPU |
| [Set encoders]({{ '/solutions/classifiers-and-decoders/set-encoders/' | relative_url }}) | Frame labels | No identities, by design | GPU to train |
| [Temporal convolutional networks]({{ '/solutions/classifiers-and-decoders/pytorch-tcn/' | relative_url }}) | Frame labels, many | Set by the features fed in | GPU to train |
| [Temporal action segmentation]({{ '/solutions/classifiers-and-decoders/temporal-action-segmentation/' | relative_url }}) | Frame labels, many | Set by the features fed in | GPU to train |
| [Graph network toolkits]({{ '/solutions/classifiers-and-decoders/graph-network-toolkits/' | relative_url }}) | Frame labels, many | Ball node needs a fallback. Temporal layers want identities | GPU to train |
| [Online change-points]({{ '/solutions/classifiers-and-decoders/bocpd/' | relative_url }}) | None | One signal | Light |
| [Learned imputation]({{ '/solutions/classifiers-and-decoders/learned-imputation/' | relative_url }}) | Complete sequences to learn from | It fills the ball in | GPU to train |

Labels drive the choice. With none, the decoders are the family: Viterbi first, a semi-Markov model if spell lengths are the problem. With labels, score frames with boosted trees before anything deeper, and keep a decoder behind whatever scores them.

{% include wiki/motif.html id="sol-labels-axis" caption="The family by its appetite for labels. Decoders on the top row, scorers below. Everything inside the lime zone runs with no labels at all, and the pair we fielded sits there." %}

## What this family cannot do

- **A decoder cannot repair biased evidence.** It finds the best sequence for the scores it is given.
- **A classifier cannot be trusted without labels from the target feed.** It learns one provider's possession.
- **Frame accuracy does not buy coherent possessions.** A model right on most frames can still split every possession in three.

## Where our decoder stands

Here. It is an exact [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) per half over H, A and D, with hand-specified football evidence and a cost for every change of state. Nothing is fitted to the match. Why this decoder and not a learned or duration-aware one is argued in [Seven ways to decode a match]({{ '/architecture/decoding-alternatives/' | relative_url }}), and the whole design is in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).
