---
title: "Graph network toolkits (PyG, PyG Temporal, DGL)"
kicker: "Classifiers and decoders"
summary: "The three libraries football graph models are built with. They supply message passing, batching and recurrent graph layers. The football has to come from you."
group: classifiers-and-decoders
order: 90
chips: ["Tracking", "Graph", "Learned", "Needs labels"]
motif: graph
motif_caption: "Message passing: each player updates from his neighbours along the edges, then a readout answers."
motif_labels: ["Node", "Message", "Neighbour"]
facts:
  - { k: "Modality", v: "A player graph per frame" }
  - { k: "Output", v: "Node, edge or graph predictions, after training" }
  - { k: "Evidence", v: "Standard research frameworks; CIKM 2021 (PyG Temporal)" }
  - { k: "Code and weights", v: "Frameworks only; no football weights" }
  - { k: "Licence", v: "MIT (PyG, PyG Temporal), Apache-2.0 (DGL)" }
verdict: { label: "Our read", text: "The right formalism for football, waiting on labels. Choose the graph before you choose the library." }
sources:
  - { title: "PyTorch Geometric repository", url: "https://github.com/pyg-team/pytorch_geometric" }
  - { title: "PyTorch Geometric Temporal: spatiotemporal signal processing with neural machine learning models (CIKM 2021)", url: "https://github.com/benedekrozemberczki/pytorch_geometric_temporal" }
  - { title: "Deep Graph Library (DGL) repository", url: "https://github.com/dmlc/dgl" }
related:
  - /solutions/physics-and-features/unravelsports/
  - /solutions/direct-possession/pathcrf/
  - /solutions/classifiers-and-decoders/set-encoders/
---
A football frame is a graph before anyone draws it. Players are nodes, and what matters lies between them. Graph neural networks compute on that structure by message passing: each node gathers information from its neighbours along edges, updates itself and repeats. A readout turns node states into a prediction about a player, a pair or the whole frame.

| Library | What it adds | Licence |
|---|---|---|
| PyTorch Geometric | The common layers (GCN, GraphSAGE, GAT, GINE) and batching of graphs of different sizes | MIT |
| PyG Temporal | Recurrent graph layers for sequences of graphs | MIT |
| DGL | The same ground with strong support for heterogeneous graphs | Apache-2.0 |

PyTorch Geometric is the default. PyG Temporal matters because a match is a sequence of graphs. DGL earns its place when player, ball and goal are different node types.

## Where it wins

- Relations are explicit. Distance, closing speed and angle live on edges instead of being flattened into a vector.
- Permutation invariance and variable player counts come with the formalism.
- Edge-level outputs match football questions: who passes to whom, who presses whom.
- Mature ecosystems. [unravelsports]({{ '/solutions/physics-and-features/unravelsports/' | relative_url }}) builds football graphs for them directly.

## What it costs

- These are frameworks. Topology, features, architecture and labels are all design decisions, and each changes the result.
- Graph models are hungry for data. Published football GNNs train on many matches of labelled tracking.
- Temporal graph layers assume a node is the same entity across frames. Team-only tracking breaks that assumption.
- They are GPU-oriented, with dependency stacks that complicate reproducible CPU builds.

## How it plugs into possession

Graph networks are where supervised possession modelling is heading. [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}) is one, and so are the [phase models]({{ '/solutions/direct-possession/match-phase-segmentation/' | relative_url }}). The sound pipeline is a graph encoder for each frame, a sequence model across frames and a structured decoder at the end.

Mind the ball. The obvious graph has a ball node connected to every player. When the ball is untracked that node vanishes and the model must still answer, so the architecture needs a ball-free path from the start.

Two facts kept a graph network out of our Initial Challenge build: no labels on the match, and players that carry a team and no identity. Both calls are explained in Architecture, under [Evidence, then a decoder]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}) and [Players without names]({{ '/architecture/player-identities/' | relative_url }}).
