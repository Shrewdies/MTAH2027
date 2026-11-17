---
title: "Temporal action segmentation (MS-TCN, ASFormer)"
kicker: "Classifiers and decoders"
summary: "Models built to label every frame of a long sequence without shattering it. Computer vision met the over-segmentation problem first, and its fixes transfer."
group: classifiers-and-decoders
order: 80
chips: ["Sequence", "Learned", "Needs labels", "Research code"]
motif: ribbon
motif_caption: "A first stage over-segments. Later stages read its predictions and merge the fragments."
motif_labels: ["Stage 1 prediction", "After refinement", "Action A", "Action B", "Background"]
facts:
  - { k: "Modality", v: "Per-frame embeddings from video or tracking" }
  - { k: "Output", v: "One label per frame, in coherent segments" }
  - { k: "Evidence", v: "CVPR 2019 (MS-TCN); BMVC 2021 (ASFormer)" }
  - { k: "Code and weights", v: "Official research code; no football weights" }
  - { k: "Licence", v: "MIT (ASFormer); MS-TCN under its repository's own terms" }
verdict: { label: "Our read", text: "The clearest statement of the over-segmentation problem. Its learned fix needs labels. The same prior can be imposed exactly with a decoder." }
sources:
  - { title: "MS-TCN: Multi-Stage Temporal Convolutional Network for Action Segmentation (CVPR 2019)", url: "https://openaccess.thecvf.com/content_CVPR_2019/html/Abu_Farha_MS-TCN_Multi-Stage_Temporal_Convolutional_Network_for_Action_Segmentation_CVPR_2019_paper.html" }
  - { title: "MS-TCN: official code", url: "https://github.com/yabufarha/ms-tcn" }
  - { title: "ASFormer: Transformer for Action Segmentation (arXiv 2110.08568, BMVC 2021)", url: "https://arxiv.org/abs/2110.08568" }
  - { title: "ASFormer: official code", url: "https://github.com/ChinaYi/ASFormer" }
related:
  - /solutions/classifiers-and-decoders/pytorch-tcn/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hsmmlearn/
---
Action segmentation labels every frame of an untrimmed video: pour, stir, cut. Its metrics reward getting segments right, not only frames, and its classic failure is over-segmentation: a model with good frame accuracy that splits one action into a dozen pieces. Replace the kitchen with a pitch and this is the possession problem, spell metric included.

MS-TCN answers with refinement in stages. A first dilated TCN predicts frame labels. Further stages take those predictions as input and predict again, each correcting the last, so later stages see label context instead of raw features. A smoothing loss penalises abrupt changes in the output between adjacent frames.

ASFormer keeps the staged design and swaps convolution for attention: an encoder for the first pass and decoders that refine it, with attention windows arranged so the model stays trainable on sequences of thousands of frames.

## Where it wins

- They attack fragmentation directly, in the architecture and in the loss.
- Their segment-level evaluation, edit score and segmental F1, is the closest cousin of spellF1 in the literature.
- They are full-sequence models. A long recording is processed whole, not in clips.
- Input-agnostic. Any per-frame embedding works.

## What it costs

- Supervised, and developed on video benchmarks rather than on football tracking.
- Smoothing is a prior with a strength. Too strong, and real one-touch possessions vanish.
- Learned refinement is opaque. When it merges two spells there is no cost to inspect.
- Scores are not calibrated probabilities.

## How it plugs into possession

As a lesson first and a model second. The lesson: per-frame accuracy and segment quality are different objectives, and the gap between them must be closed deliberately.

MS-TCN closes it with learned refinement and a smoothing loss. A [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) closes it with an explicit switching cost and an exact optimum, and needs no training to do so.

With labels in hand, a multi-stage model is a credible emission network. Even then, a structured decoder on top is the cheapest insurance against fragments.
