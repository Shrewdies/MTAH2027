---
title: "Viterbi decoding"
kicker: "Classifiers and decoders · Fielded"
summary: "The exact best path through per-frame evidence. Three states, a cost for every switch, and a guarantee that no better sequence exists. Our evidence decoder is built on it."
group: classifiers-and-decoders
order: 10
chips: ["Sequence", "Exact", "No training", "Fielded"]
motif: decoder
motif_caption: "Every frame scores three states. Viterbi keeps the best way to reach each one, then traces the winner back."
motif_labels: ["Home", "Away", "Dead ball", "Best path"]
facts:
  - { k: "Modality", v: "A score for each state on each frame" }
  - { k: "Output", v: "One state per frame, globally optimal" }
  - { k: "Evidence", v: "Rabiner's tutorial (1989); our decoder on open DFL labels" }
  - { k: "Code and weights", v: "A few lines of array code; nothing learned" }
  - { k: "Licence", v: "Public algorithm, free to implement" }
verdict: { label: "Our read", text: "The highest-leverage algorithm in possession inference. It turns any per-frame evidence into football-shaped sequences, exactly and almost for free." }
sources:
  - { title: "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition (Rabiner, Proceedings of the IEEE, 1989)", url: "https://doi.org/10.1109/5.18626" }
  - { title: "hmmlearn: a reference implementation of Viterbi and forward-backward", url: "https://github.com/hmmlearn/hmmlearn" }
related:
  - /solutions/direct-possession/metrica-baseline/
  - /solutions/classifiers-and-decoders/pytorch-crf/
  - /solutions/classifiers-and-decoders/hsmmlearn/
  - /architecture/decoding-alternatives/
  - /architecture/the-shrewdies-decoder/
---
Per-frame evidence is noisy. Possession is not. A touch lasts a frame; a possession lasts seconds. The question is how to turn the first into the second without inventing or erasing football, and Viterbi's algorithm is the exact answer to a precise version of that question.

Give every state a score on every frame: how well the evidence fits home possession, away possession or dead ball. Give every change of state a cost. The best sequence is the one with the highest total evidence minus total switching cost. A match of 199,319 frames has 3 to the power 199,319 candidate sequences. Viterbi finds the best one in a single pass.

It can because of one observation. The best path that ends in state H at frame t must extend the best path to some state at frame t-1. So keep three numbers per frame, the best score ending in each state, and three pointers saying where each came from. Sweep forward once, then follow the pointers back from the end. The work is frames times states squared: under two million elementary steps for a match.

## What the switch cost does

One number carries the football. With no cost, the output is the per-frame winner and flickers with the noise. With a cost, a stray frame of contrary evidence is cheaper to absorb than two switches, so it is absorbed. Sustained contrary evidence eventually outweighs the cost and the path switches, at the frame where the totals cross.

That is not smoothing. A majority vote blurs evidence in a fixed window and drags boundaries with it. A decode weighs strength. One decisive frame, a clean reception, can flip the state at once. Fifty weak frames cannot.

## Where it wins

- Exact. For the stated scores and costs no better sequence exists. Nothing to converge, no random seed.
- Deterministic and tiny. The decode is a small share of a pipeline that labels a full match on a laptop CPU in under 10 seconds.
- No training. The parameters are a handful of costs with football meaning.
- Missing evidence is native. A frame with no information scores all states equally and the path simply continues.
- Inspectable. Every boundary sits where accumulated evidence beat a known cost.

## What it costs

- It is only as good as the evidence. Viterbi optimises the scores it is given and cannot repair a biased cue.
- A switch cost is a prior against short spells. Set too high, it deletes real one-touch possessions and quick turnovers.
- First-order memory. It knows the previous state, not how long that state has lasted. A [semi-Markov model]({{ '/solutions/classifiers-and-decoders/hsmmlearn/' | relative_url }}) buys that at a price.
- It returns one path with no confidence attached. Posteriors need the forward-backward pass of a [hidden Markov model]({{ '/solutions/classifiers-and-decoders/hmmlearn/' | relative_url }}).

## How it plugs into possession

Our evidence decoder is this algorithm with football in the scores: one exact pass per half over H, A and D, with one cost for changing team and another for starting or ending a stoppage. A frame where the ball is untracked contributes no ball evidence, and the path simply continues.

The signals, thresholds and switch costs are in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}). Why Viterbi and not a learned or duration-aware decoder is argued in [Seven ways to decode a match]({{ '/architecture/decoding-alternatives/' | relative_url }}). The result against the organisers' [nearest-player baseline]({{ '/solutions/direct-possession/metrica-baseline/' | relative_url }}) is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page.
