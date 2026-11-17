---
title: "Match-phase segmentation"
kicker: "Direct possession"
summary: "Graph-temporal models that cut a match into tactical phases such as build-up, progression and finishing. One level above possession, and dependent on it."
group: direct-possession
order: 50
chips: ["Tracking", "Graph + sequence", "Learned", "Preprints"]
motif: ribbon
motif_caption: "Frame-level phase guesses are noisy. Temporal modelling turns them into coherent phases of play."
motif_labels: ["Per-frame guesses", "Coherent phases", "Build-up", "Progression", "Finishing"]
facts:
  - { k: "Modality", v: "Tracking, with possession as context" }
  - { k: "Output", v: "Tactical phase per frame or window" }
  - { k: "Evidence", v: "Two 2026 preprints: seven Bundesliga matches; 203 matches" }
  - { k: "Code and weights", v: "Papers only" }
  - { k: "Licence", v: "Not applicable: no released code" }
verdict: { label: "Our read", text: "The layer above possession. Valuable once H/A/D is solved, circular if used to solve it." }
sources:
  - { title: "Intention-driven in-possession phases with temporal graph attention (arXiv 2606.09289)", url: "https://arxiv.org/abs/2606.09289" }
  - { title: "GNN-LSTM match-phase detection across 203 matches (arXiv 2610.11571)", url: "https://arxiv.org/abs/2610.11571" }
related:
  - /solutions/direct-possession/defcon/
  - /solutions/classifiers-and-decoders/graph-network-toolkits/
  - /solutions/direct-possession/pathcrf/
---
Two 2026 preprints attack the same problem from the same direction. Possession says who has the ball. Phase says what they are doing with it.

The first segments in-possession play by intention, into phases such as build-up, progression and finishing. A temporal graph attention network encodes player relations frame by frame and a Transformer models how they evolve. It is evaluated on seven Bundesliga matches.

The second pairs a graph network with an LSTM to classify seven match phases across 203 matches. Its most useful contribution is an ablation of the graph itself: Delaunay adjacency against other topologies, with spatial attributes on the edges. The authors report gains over feature-based baselines.

| | Intention-driven phases | GNN-LSTM phases |
|---|---|---|
| Spatial model | Temporal graph attention | Graph network, Delaunay edges |
| Temporal model | Transformer | LSTM |
| Target | In-possession phases | Seven match phases |
| Evaluation | Seven Bundesliga matches | 203 matches |

## Where it wins

- Phases are the vocabulary coaches use. This is the layer where tracking becomes tactics.
- Both papers show that relations between players, not positions alone, carry the tactical signal.
- The Delaunay result is practical. Which graph you draw matters as much as which network you run on it.

## What it costs

- Both take possession as given. The first segments only in-possession play. The second feeds possession and ball status to the model as input features.
- Phase labels are expensive expert annotation, and definitions differ between analysts and clubs.
- Neither paper ships code or weights.

## How it plugs into possession

After possession, never before. A phase model trained with possession as an input cannot be turned round to infer possession: the answer is already in the question.

Used in order, the stack is clean. Possession inference labels each frame H, A or D. A phase model subdivides the H and A stretches into what the team was trying to do.

The architectural lesson does transfer. A graph encoder per frame with a sequence model across frames is the shape of [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}), and the shape any supervised possession model built on [graph networks]({{ '/solutions/classifiers-and-decoders/graph-network-toolkits/' | relative_url }}) would take.
