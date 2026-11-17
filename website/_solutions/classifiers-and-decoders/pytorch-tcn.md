---
title: "Temporal convolutional networks"
kicker: "Classifiers and decoders"
summary: "Dilated one-dimensional convolutions that read seconds of context for every frame. The standard learned sequence layer for dense per-frame labels."
group: classifiers-and-decoders
order: 70
chips: ["Sequence", "Learned", "Needs labels", "MIT"]
motif: stack
motif_caption: "Dilation doubles with every layer, so a few layers let one output frame see hundreds of inputs."
motif_labels: ["Dilation 4", "Dilation 2", "Dilation 1", "Input frames"]
facts:
  - { k: "Modality", v: "A sequence of per-frame features" }
  - { k: "Output", v: "Class scores for every frame" }
  - { k: "Evidence", v: "Established TCN literature; maintained PyTorch package" }
  - { k: "Code and weights", v: "pytorch-tcn package; original TCN reference code" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The default learned temporal layer. It buys context cheaply. Coherence still has to be decoded." }
sources:
  - { title: "pytorch-tcn: temporal convolutions in PyTorch, with streaming support (repository)", url: "https://github.com/paul-krug/pytorch-tcn" }
  - { title: "locuslab/TCN: reference code for the generic TCN architecture", url: "https://github.com/locuslab/TCN" }
related:
  - /solutions/direct-possession/borghesi-possession-tcn/
  - /solutions/classifiers-and-decoders/temporal-action-segmentation/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
---
A temporal convolutional network stacks one-dimensional convolutions whose dilation doubles at each layer. The first layer sees neighbouring frames, the next skips one, the next three. After a handful of layers a single output frame depends on hundreds of inputs, with far fewer parameters than a recurrent network and none of its training troubles. Residual connections keep the stack trainable.

Two variants matter. A causal TCN sees only the past and suits live inference. A non-causal one sees both sides and is the right choice offline, where the frames after a touch are as informative as the frames before it.

pytorch-tcn packages the architecture with streaming inference and export support. The locuslab repository is the reference code from the work that established TCNs as a general sequence model.

## Where it wins

- Receptive field by design. At 25 fps, covering four seconds is an architectural choice, not a hope.
- Parallel over time. Inference on a full half is one forward pass.
- Stable to train compared with recurrent networks.
- The same layer serves tracking features, set-encoder outputs and video embeddings.

## What it costs

- Supervised. It needs dense per-frame labels in quantity.
- Context is not coherence. Outputs are still per-frame scores and still flicker at ambiguous moments.
- The receptive field is fixed. Long dead-ball stretches exceed it; short duels are blurred by it.
- Trained weights are tied to a frame rate and a feature definition.

## How it plugs into possession

In the middle of the stack. A [set encoder]({{ '/solutions/classifiers-and-decoders/set-encoders/' | relative_url }}) summarises each frame, the TCN adds time, a decoder enforces sequence logic. [Borghesi's possession model]({{ '/solutions/direct-possession/borghesi-possession-tcn/' | relative_url }}) is exactly this, and [MS-TCN]({{ '/solutions/classifiers-and-decoders/temporal-action-segmentation/' | relative_url }}) is what happens when the refinement job is handed to more TCN stages.

For offline possession, use the non-causal form. Whether a touch was a reception or a deflection is decided by what the ball does next.
