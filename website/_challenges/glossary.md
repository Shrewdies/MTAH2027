---
layout: wiki-entry
nav_exclude: true
title: Glossary and failure map
kicker: Reference
summary: "The vocabulary of possession inference in one place, and the seven false equivalences that sink most first attempts."
route_label: Glossary
hook: "Seven false equivalences"
group: reference
order: 130
chips: [Data, Geometry, Decoding, Scoring]
motif: matrix
motif_caption: Five families of terms, one problem. Most mistakes come from treating two neighbouring cells as the same thing.
motif_labels: [Data, Geometry, Time, Scoring, Rules]
sources:
  - { title: "CHALLENGE (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md" }
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "EVALUATION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
related:
  - /challenges/possession-frame-by-frame/
  - /challenges/spellf1-and-macrof1/
  - /challenges/temporal-decoding/
---
## Seven false equivalences

| It is tempting to assume | The truth |
|---|---|
| Closest player = possessor | Proximity flips in every pass and duel; control does not |
| Touch = turnover | Possession moves when the other side establishes control |
| Ball untracked = dead ball | The tracker loses the ball in live play, at its most contested |
| Smoother labels = better spells | Smoothing deletes real short possessions and merges their neighbours |
| More models = more evidence | Models fed by the same tracking share the same errors |
| Valid homography = synchronised frames | Where on the pitch and when in the match are separate questions |
| Published code = usable model | A repository without weights, licence and data path is a paper |

## Possession and scoring

| Term | Meaning |
|---|---|
| Controlled possession | A team has the ball until the other side establishes control or play stops |
| H, A, D | Home in possession, away in possession, dead ball |
| X | Abstention in a submission; never a true state |
| Possession spell | An unbroken run of H or A; a stoppage ends it |
| spellF1 | Ranking metric: one-to-one matching of spells by temporal IoU, averaged over five thresholds |
| macroF1 | Tie-break: mean frame-level F1 over H, A and D |
| Temporal IoU | Overlap of two intervals divided by their union |
| False split, false merge | One true spell predicted as two; two predicted as one |
| Pareto frontier | The candidates no other candidate beats on both metrics |
| Leakage | Using the answer, or anything derived from it, as an input |

## Data and geometry

| Term | Meaning |
|---|---|
| ATD | Automatic Tracking Data: positions of players and ball for every video frame |
| Track slot | A column of tracking output; a team, not a player identity |
| Tracklet | A short reliable run of one track before the object is lost |
| Tactical camera | The wide view of the whole pitch; the competition's reference clock |
| Broadcast camera | The edited feed: live shots, cuts, close-ups and replays |
| Smart Tagging | Automatic tactical intervals and restarts; context, not an event log |
| Homography | Plane-to-image projective transform; no height, no timing |
| Provenance | Where an observation came from, and whether it was measured or inferred |

## Time and decoding

| Term | Meaning |
|---|---|
| Timebase | The clock a source is indexed on |
| Dense temporal classification | A label for every frame, as opposed to sparse event timestamps |
| Observation model | Turns tracking, tags or pixels into per-frame evidence for each state |
| Decoder | Turns a sequence of noisy evidence into one coherent state sequence |
| Viterbi | Exact dynamic-programming search for the best path under switch costs |
| HMM, HSMM | Hidden Markov model; its semi-Markov form also models how long states last |
| CRF | A discriminative model of whole label sequences |
| TCN | Temporal convolutional network: learned features over a window of time |
| DTW | Dynamic time warping: aligns two sequences that run at different rates |
| Filtering, smoothing | Estimating from the past only; estimating with the future as well |

## Learning on players

| Term | Meaning |
|---|---|
| Permutation invariance | The output does not change when the players are listed in another order |
| Deep Sets | An order-invariant network over a group of players |
| Set Transformer | Attention over unordered objects |
| GNN | Graph neural network: players and ball as nodes, interactions as edges |
| Ball-free inference | Reading possession from player movement alone |

The methods behind these terms are mapped and judged in [Solutions]({{ '/solutions/' | relative_url }}); the data they learn from is in [Datasets]({{ '/datasets/' | relative_url }}).
