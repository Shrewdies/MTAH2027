---
layout: wiki-hub
title: The engine
permalink: /architecture/engine/
collection_index: architecture
only_group: engine
family: true
parent: /architecture/
nav_exclude: true
kicker: "Family 03 of 05"
summary: "Evidence on one frame is noisy. The engine turns 25 opinions a second into one coherent story of the half, and the ranking metric scores the story. Three decisions, taken in order."
motif: bp-decision
motif_labels: [engine]
motif_caption: "The decision map of this family. Three questions, in the order they have to be answered."
stats:
  - { value: "{count}", label: studies in this family }
  - { value: "7", label: decoders compared on the same scores }
  - { value: "2", label: levels at which experts can be combined }
---

## What moves through the engine

The engine changes the unit of the problem three times: from opinions on frames, to scores, to states, to
possessions. The ranking metric reads only the last one, which is why a small error near the top can
cost a whole possession at the bottom.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-funnel" caption="Thirty frames in, two possessions out. The tie-break metric reads the states. The ranking metric reads the possessions." %}
</div>

## The trade-off surface of the family

Every option in this family buys capacity with labels and pays for it in what it can promise about the
sequence. Put them on one plane and the constraint from the previous family, the labels that exist,
draws a line through it.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-surface" caption="Across: the labels an engine needs. Up: the guarantee it can state about the sequence. With no labels on the match, only the left column can be fielded. Positions are judgements, not measurements." %}
</div>

## Three decisions, in order

| Decision | The options | What decides it |
|---|---|---|
| [Where time lives]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}) | Inside one multi-frame model, or in a decoder behind the evidence | The labels that exist; what must be auditable |
| [Which decoder]({{ '/architecture/decoding-alternatives/' | relative_url }}) | Majority, Viterbi, HMM, CRF, HSMM, change-point, neural | What it needs, what it guarantees, how it treats short spells |
| [Who decides when models disagree]({{ '/architecture/ensemble-logic/' | relative_url }}) | A gate on every frame, or a referee on a disputed segment | Whether the experts' errors are independent |

The second question only exists if the first was answered "a stage of its own". The third only exists if
there is more than one expert or more than one decoded sequence.

## How an architect chooses here

- **Ask what labels exist.** A learner is only as good as its labels. A decoder with fixed costs needs none.
- **Prefer a guarantee you can state.** "The best path under these two costs" can be argued with. A learned smoothness cannot.
- **Compare on the spell, not the frame.** The metric counts possessions, so the engine is judged on possessions.
- **Earn every added part.** An expert whose removal changes nothing was a passenger.

## What this family cannot do

No engine repairs evidence that was never there. A missing ball, a swapped identity and a stoppage nobody
tagged are problems of representation, and they belong to [the hard parts]({{ '/architecture/hard-parts/' | relative_url }}).
