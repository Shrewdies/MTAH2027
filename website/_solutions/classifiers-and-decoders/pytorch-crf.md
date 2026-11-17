---
title: "Linear-chain CRF (pytorch-crf)"
kicker: "Classifiers and decoders"
summary: "Learned transition scores between adjacent labels, trained jointly with the network beneath and decoded exactly with Viterbi."
group: classifiers-and-decoders
order: 40
chips: ["Sequence", "Structured output", "Needs labels", "MIT"]
motif: decoder
motif_caption: "Emissions score each frame, learned transitions score each step, and the best path is decoded exactly."
motif_labels: ["Home", "Away", "Dead ball", "Learned transitions"]
facts:
  - { k: "Modality", v: "Per-frame class scores from any network" }
  - { k: "Output", v: "One coherent label path" }
  - { k: "Evidence", v: "Lafferty et al. (2001); maintained PyTorch layer" }
  - { k: "Code and weights", v: "pytorch-crf layer; transitions are learned per task" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The textbook structured output layer. With three states its real gift is the structure, and the structure is free." }
sources:
  - { title: "pytorch-crf: linear-chain conditional random field in PyTorch (repository)", url: "https://github.com/kmkurn/pytorch-crf" }
  - { title: "Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data (Lafferty, McCallum, Pereira, 2001)", url: "https://www.cs.columbia.edu/~jebara/6772/papers/crf.pdf" }
related:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/direct-possession/pathcrf/
  - /solutions/classifiers-and-decoders/hmmlearn/
---
A conditional random field scores a whole label sequence, not each label alone. In the linear-chain form the score is a sum of two parts. Emissions say how well each frame's features fit its label. Transitions say how compatible each label is with the next. The probability of a sequence is its score normalised over all possible sequences, which dynamic programming computes exactly.

pytorch-crf implements this as a layer. Put it on top of any network that outputs per-frame scores. Training maximises the likelihood of the true sequence, so gradients flow into both the transition matrix and the network. Inference is Viterbi.

The difference from a hidden Markov model is direction. An HMM models how states generate observations. A CRF models labels given observations, so emissions can use overlapping, arbitrary features with no independence assumption.

## Where it wins

- Transitions are learned from data, not set by hand.
- Joint training. The network learns emissions that suit the decoder it will be decoded by.
- Exact inference in both training and decoding.
- Hard constraints are trivial: forbid a transition by fixing its score at minus infinity.

## What it costs

- Learning transitions requires labelled sequences.
- First-order memory. Leaving a state costs the same after two frames or two hundred.
- One transition matrix for all time. Context-dependent switching, cheap at a touch and expensive mid-dribble, needs an extension.
- Three labels give nine transition scores. With so few parameters, learning them buys little over setting them well.

## How it plugs into possession

It is the supervised sibling of our decoder: the same chain and the same Viterbi inference. The only difference is where the numbers come from. With possession labels, a CRF layer on a [temporal convolution]({{ '/solutions/classifiers-and-decoders/pytorch-tcn/' | relative_url }}) or [boosted-tree]({{ '/solutions/classifiers-and-decoders/gradient-boosted-trees/' | relative_url }}) emission model is the textbook design, and [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}) is a far richer version of the idea.

Without labels, the structure survives and the learning goes. Fix the transition costs, compute emissions from football evidence, and decode. That is the system we fielded, described under [Viterbi decoding]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}).
