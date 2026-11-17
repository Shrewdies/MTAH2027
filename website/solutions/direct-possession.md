---
layout: wiki-hub
title: "Direct possession"
permalink: /solutions/direct-possession/
collection_index: solutions
only_group: direct-possession
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Methods that answer the question itself: which team has the ball on this frame, or is play dead. Six entries, two routes, one shared blind spot."
motif: ribbon
motif_caption: "The task in one picture: an answer on every frame flickers, and possession does not."
motif_labels: ["Per-frame answers", "Possession", "Home", "Away", "Dead ball"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "2", label: "need no labels" }
  - { value: "1", label: "works without the ball" }
---
## One picture: a frame in, an answer out

Every method in this family takes tracking and says home, away or dead. The difficulty is in the picture above: answers given frame by frame flicker, and possession does not. What separates the entries is where their answer comes from.

There are two routes. **Rules** read possession off geometry: the nearest player, a touch, a ball crossing the line. **Learned models** read it off examples. A network sees labelled frames by the thousand and learns what possession looks like, with the ball or without it.

{% include wiki/motif.html id="sol-two-routes" caption="The same passage, both routes. Rules read the ball and have no answer while it is untracked. A learned ball-free model answers through the gap, and needs labels and persistent identities to do it." %}

The other families each own one link of the possession chain: reading, seeing, syncing, measuring, spotting, decoding. A direct method replaces the measuring, spotting and decoding links with one step. That is its strength, since there is nothing to assemble. It is also its risk: when it fails, there is no intermediate evidence to inspect.

## How to choose inside it

| Entry | Labels | Ball and identities | Compute |
|---|---|---|---|
| [Nearest-player baseline]({{ '/solutions/direct-possession/metrica-baseline/' | relative_url }}) | None | Ball required. No identities | Trivial |
| [Rule-based event detection]({{ '/solutions/direct-possession/vidal-event-tracking/' | relative_url }}) | None | Ball required. No identities | Trivial |
| [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}) | To train or retrain | No ball. Persistent player tracks | GPU to train; saved models exist |
| [Possession TCN]({{ '/solutions/direct-possession/borghesi-possession-tcn/' | relative_url }}) | Frame labels, many matches | As trained. No identities | GPU to train |
| [Match-phase segmentation]({{ '/solutions/direct-possession/match-phase-segmentation/' | relative_url }}) | Phase labels | Possession given as input | GPU to train |
| [DEFCON]({{ '/solutions/direct-possession/defcon/' | relative_url }}) | Its own training data | Possession and players known | GPU to train |

{% include wiki/motif.html id="sol-needs" caption="The six entries by what they need and what they give. Four produce possession from different inputs. Phase segmentation and DEFCON take it as an input." %}

Read the table as a ladder. With no labels, start with the rules. With labels and clean identities, PathCRF is the one entry that survives a missing ball. The last two rows are not ways to find possession. They are what gets built once it is found.

## What this family cannot do

- **Rules cannot see past the ball.** Both rule-based entries are keyed on ball position. No ball, no answer.
- **Learned models cannot outrun their labels.** They learn one provider's definition of possession on one provider's tracking. A new feed means new labels.
- **Most cannot promise a coherent sequence.** PathCRF can, because it carries a decoder inside. The others need one behind them.

## Where our decoder stands

It is a direct possession method by output, and a member of the [classifiers and decoders]({{ '/solutions/classifiers-and-decoders/' | relative_url }}) family by construction. It keeps the baseline's cue, a player within 1.5 m of the ball and closer than any opponent. It treats an untracked ball as no evidence. An exact [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) chooses the sequence, and no labels are fitted. The design is in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).
