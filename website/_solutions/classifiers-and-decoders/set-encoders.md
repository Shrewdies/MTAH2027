---
title: "Set encoders (Deep Sets, Set Transformer)"
kicker: "Classifiers and decoders"
summary: "Networks whose output cannot depend on the order of their inputs. The correct way to feed anonymous players to a model."
group: classifiers-and-decoders
order: 60
chips: ["Tracking", "Learned", "Order-invariant", "Needs labels"]
motif: ensemble
motif_caption: "Every player passes through the same encoder. Pooling merges them into one state that ignores slot order."
motif_labels: ["Player 1", "Player 2", "Player 3", "Player 4", "Symmetric pooling", "Set state"]
facts:
  - { k: "Modality", v: "An unordered set of players per frame" }
  - { k: "Output", v: "Frame or team embedding for a downstream model" }
  - { k: "Evidence", v: "NeurIPS 2017 (Deep Sets); ICML 2019 (Set Transformer)" }
  - { k: "Code and weights", v: "Authors' research code; no football weights" }
  - { k: "Licence", v: "Apache-2.0 (Deep Sets), MIT (Set Transformer)" }
verdict: { label: "Our read", text: "Not optional for anonymous players. Start with Deep Sets and move to attention when labels are plentiful." }
sources:
  - { title: "Deep Sets (arXiv 1703.06114, NeurIPS 2017)", url: "https://arxiv.org/abs/1703.06114" }
  - { title: "Deep Sets: authors' code", url: "https://github.com/manzilzaheer/DeepSets" }
  - { title: "Set Transformer (arXiv 1810.00825, ICML 2019)", url: "https://arxiv.org/abs/1810.00825" }
  - { title: "Set Transformer: PyTorch implementation", url: "https://github.com/juho-lee/set_transformer" }
related:
  - /solutions/direct-possession/borghesi-possession-tcn/
  - /solutions/direct-possession/pathcrf/
  - /solutions/classifiers-and-decoders/graph-network-toolkits/
---
Tracking delivers a frame as a list of players, and the order of that list is an accident of the tracker. A model that reads positions as a fixed vector learns the accident. Set encoders remove it by construction.

Deep Sets shows that the simple form is enough in principle. Apply the same network to every element, combine the results with a symmetric operation such as a sum or a mean, then transform the pooled vector. Every player is encoded identically, and the result is the same whatever order they arrive in.

Set Transformer replaces independent encoding with attention. Players attend to one another before pooling, so the representation can express relations: this defender is goal-side of that attacker. Induced set attention keeps the cost manageable, and learned attention pooling replaces the plain sum.

| | Deep Sets | Set Transformer |
|---|---|---|
| Interactions | Only through pooling | Explicit, through attention |
| Cost in players | Linear | Quadratic, reduced by inducing points |
| Appetite for data | Low | Higher |

## Where it wins

- Slot-order invariance is guaranteed, not learned from augmentation.
- Variable set size is natural. Ten players or eleven, the same network.
- Deep Sets is tiny and hard to overfit. Set Transformer captures pairwise structure when data allows.
- Team-only data fits exactly: two sets, home and away, no identities required.

## What it costs

- Pooling loses information. A sum-pooled model struggles with "the nearest opponent to the ball", which is a relation between elements.
- Invariance to order is not robustness to absence. A missing or duplicated player still shifts the pooled vector.
- They are encoders, not solutions. Training needs possession labels, and time has to be modelled elsewhere.
- Attention on small labelled sets overfits readily.

## How it plugs into possession

As the front end of any learned possession model. [Borghesi's TCN]({{ '/solutions/direct-possession/borghesi-possession-tcn/' | relative_url }}) uses the pattern, and [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}) uses set attention for the same reason. For a feed where players carry a team and no identity, a set encoder is not an optimisation. It is the only input layer that respects the data.

The principle applies without a network too. Hand-built evidence made of minima, counts and means over a team, such as nearest player, players within a radius or mean speed, is permutation-invariant by design.
