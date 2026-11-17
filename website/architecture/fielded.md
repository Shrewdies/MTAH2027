---
layout: wiki-hub
title: On the pitch
permalink: /architecture/fielded/
collection_index: architecture
only_group: fielded
family: true
parent: /architecture/
nav_exclude: true
kicker: "Family 01 of 05"
summary: "One architecture went from the board to the pitch. This page is the why: the constraints it was drawn under and the call each one forced. The what, with its numbers, is the study below."
motif: bp-decision
motif_labels: [fielded]
motif_caption: "Constraint on the left, the call it forced on the right. Select a call to read the study that argues it."
stats:
  - { value: "{count}", label: architecture fielded and measured }
  - { value: "4", label: hard constraints }
  - { value: "9", label: calls they forced }
---

## Constraints first

We did not choose an architecture and then defend it. We wrote down what the Initial Challenge would not
allow, and the design space shrank to one column. The rules themselves are read as engineering
requirements in [The rules are the architecture]({{ '/challenges/rules-as-design-constraints/' | relative_url }}).

<div class="wiki-figures">
{% include wiki/motif.html id="bp-strike" caption="Four hard constraints down the side, five candidate designs across. Each constraint strikes what cannot meet it. One column is left standing." %}
</div>

## From constraints to bytes

The same four constraints are visible in the running system. Inputs are read-only and nothing leaves the
machine. The container is pinned and has no network. Two runs give the same bytes. The whole match fits
inside the time a laptop CPU allows.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-run" caption="The fielded system as a running thing. Each constraint is pinned to the part it shaped: offline inputs, an exact rerun, a laptop's worth of compute, and the gates the file passes before it leaves." %}
</div>

## How an architect chooses here

1. **Write the constraints before the options.** Compute, labels, time, reproducibility. They are inputs to
   the design, on the board first.
2. **Strike, then choose.** Every option that violates one is out, however fashionable. The choice is made
   among what is left.
3. **Name the constraint in every call.** If no constraint forced a choice, it is a preference, and it is not
   written up as a call.
4. **Choose away from the match.** A design selected on the data it is graded on has proved nothing.

The architecture that survived, its evidence, its decode and its measured result are one study:
[The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).
