---
title: Open frontiers
kicker: Proof
summary: "Nine questions possession inference has not settled, each with the experiment that would settle it. This is where the next gains are."
group: proof
order: 30
chips: [Open questions, Experiments, Field]
motif: bp-frontiers
icon: graph
motif_caption: "A settled core, the edge of what is known, and nine open questions beyond it. The first, possession through long ball gaps, carries the most weight."
facts:
  - { k: Questions, v: "Nine, each with a decisive test" }
  - { k: Common requirement, v: "Whole labelled matches, held out" }
  - { k: Hardest, v: "Possession through long ball gaps" }
verdict:
  label: Our read
  text: "The frontier is the missing ball. Whoever shows, on held-out matches with realistic gaps, that hidden turnovers can be recovered will move the field more than any new backbone."
sources:
  - { title: "Official evaluation (spellF1, macroF1)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "Bassek et al. (2025), DFL open tracking and event data, Scientific Data 12:195", url: "https://www.nature.com/articles/s41597-025-04505-y" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/ball-aware-vs-ball-free/
  - /architecture/evaluation-framework/
  - /challenges/roadmap/
  - /solutions/direct-possession/pathcrf/
  - /datasets/dfl-idsse/
---

## The design question

Which questions are still open for everyone? Published results answer them one dataset at a time, under
one provider's definitions. None has a general answer yet. Each is stated with the evidence that would
close it, and with the study that frames it.

## The nine

| Question | What would settle it | Framed in |
|---|---|---|
| Does ball-free inference recover possession through long gaps? | Labelled matches with simulated tracking gaps | [The missing ball]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}) |
| Can a second witness fill tactical ball gaps? | Independent sync, calibration and ball visibility | [Single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}) |
| Two heads or three classes for alive, dead and team? | The same evidence, both designs, held-out matches | [Alive or dead]({{ '/architecture/live-dead/' | relative_url }}) |
| Do identities need repair at all? | Permutation and fragmentation tests | [Players without names]({{ '/architecture/player-identities/' | relative_url }}) |
| Does a graph network beat geometry with gradient boosting? | Match-separated comparisons and ablations | [Geospatial-only]({{ '/architecture/geospatial-only/' | relative_url }}) |
| Does a decoder lift both official metrics? | Spell-aware comparison on held-out matches | [Seven ways to decode]({{ '/architecture/decoding-alternatives/' | relative_url }}) |
| Are event spotters precise enough for boundaries? | Boundary error measured in frames | [Events]({{ '/architecture/events-and-control/' | relative_url }}) |
| Does calibration survive a change of provider? | Reliability diagrams on another provider's data | [Confidence]({{ '/architecture/confidence-and-provenance/' | relative_url }}) |
| Do providers mean the same thing by possession? | Published definitions, one match annotated both ways | [Two metrics]({{ '/architecture/evaluation-framework/' | relative_url }}) |

## The first frontier, as an experiment

{% include wiki/motif.html id="bp-s-experiment" caption="Hide the ball in windows of growing length on a labelled match, and plot how often possession is still right. The three curves are hypotheses, drawn as guesses. Nobody has published the measured ones." %}

## What the questions share

- **The unit is the match.** Every test needs whole matches held out. Frame-level splits answer nothing.
- **The condition is the gap.** A result on fully tracked balls says little about the frames that decide the score.
- **The metric is the spell.** Gains in frame accuracy that cost possessions are losses.

## Where the leverage is

The first two questions concern the missing ball, and they carry the most weight. What we are building
toward them is on [the roadmap]({{ '/challenges/roadmap/' | relative_url }}).
