---
title: "PathCRF"
kicker: "Direct possession"
summary: "Possession inferred from the players alone. A dynamic player graph, set attention and a CRF recover who holds the ball and where it travels, with no ball coordinates in the input."
group: direct-possession
order: 20
chips: ["Tracking", "Ball-free", "Learned", "MPL-2.0"]
motif: graph
motif_caption: "Possession as a path through the player graph: one player holds, an edge carries the ball, the next receives."
motif_labels: ["Carrier", "Possession edge", "Receiver"]
facts:
  - { k: "Modality", v: "Player tracking, no ball" }
  - { k: "Output", v: "Player-level possession path and on-ball events" }
  - { k: "Evidence", v: "KDD 2026; events evaluated on the open Sportec DFL matches" }
  - { k: "Code and weights", v: "Training and inference code, tutorial, five saved models" }
  - { k: "Licence", v: "MPL-2.0" }
verdict: { label: "Our read", text: "The most important idea in ball-free possession: player-level, structured and open. Its price is clean, persistent player tracks." }
sources:
  - { title: "PathCRF repository: code, tutorial and saved models", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "PathCRF: Ball-Free Soccer Event Detection via Possession Path Inference from Player Trajectories (arXiv preprint)", url: "https://arxiv.org/abs/2602.12080" }
  - { title: "PathCRF, KDD 2026 proceedings (ACM)", url: "https://doi.org/10.1145/3770855.3818152" }
related:
  - /solutions/classifiers-and-decoders/pytorch-crf/
  - /solutions/classifiers-and-decoders/set-encoders/
  - /solutions/classifiers-and-decoders/graph-network-toolkits/
  - /datasets/dfl-idsse/
---
PathCRF (Kim et al., KDD 2026) starts from a premise that is uncomfortable for anyone who relies on ball tracking: the players already tell you where the ball is. They orient to it, close on it and react when it moves. The model reads those reactions.

The player trajectories become a fully connected dynamic graph. Set attention encodes the players without depending on the order of tracking slots. The task is then framed as a choice: at every time step, select exactly one edge of that graph as the current possession state. A conditional random field scores those choices and forbids impossible transitions between consecutive edges. The ball cannot leave a player it never reached. Viterbi decoding returns the most probable possession path, and ball controls and passes are read off wherever the selected edge changes.

The authors evaluate event detection on the open Sportec DFL matches and publish training code, inference code, a tutorial and five saved model variants.

## Where it wins

- It is the one published method here designed for the case where the ball is simply absent.
- Its output is player-level. Team possession is a by-product, and so are pass and reception events.
- The CRF gives structural consistency: no impossible ball paths, no teleporting possession.
- Code and weights are open under MPL-2.0, a file-level copyleft that coexists with permissive projects.

## What it costs

- It expects persistent, individually tracked players. Fragmented or anonymous tracks break the graph it reasons over.
- It models who is on the ball, not whether play is live. Dead-ball time needs separate treatment.
- The saved models are trained on one provider's tracking. Different noise, coverage or frame rate means retraining, and retraining means labels.
- It answers a harder question than H/A/D. Mapping its path to three states adds a layer with its own errors.

## How it plugs into possession

PathCRF is the strongest argument that a missing ball is not missing information. There are two routes into a possession pipeline. Use its path directly and collapse player to team. Or use its edge scores as one more evidence stream for a team-level decoder, where they matter most on frames with no ball.

The second route is the safer one. A ball-free estimate and a ball-based estimate fail in different places, and a decoder can weigh them frame by frame. The supervised relatives of that decoder are the [linear-chain CRF]({{ '/solutions/classifiers-and-decoders/pytorch-crf/' | relative_url }}) and, with labels and identities in hand, PathCRF itself.

The Initial Challenge feed gives players a team and no identity, so the graph PathCRF reasons over does not exist there. We met the missing ball from the other side: a hidden ball counts as no evidence, and the decode carries possession across the gap. Both calls are explained in [Players without names]({{ '/architecture/player-identities/' | relative_url }}) and [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}).
