---
layout: wiki-entry
nav_exclude: true
title: The Pareto lens
kicker: Scoring
summary: "Two metrics that disagree do not have a best setting. They have a frontier. We searched it, froze it, and let real labels pick the point."
route_label: Pareto
hook: "No single best setting"
group: scoring
order: 40
chips: [Pareto front, 7 dials, 159 settings]
motif: pareto
motif_caption: Every candidate is a point. The frontier is the set no other candidate beats on both metrics; the submitted profile sits on it.
motif_labels: [macroF1, spellF1, Frontier, Submitted]
facts:
  - { k: Searched, v: "2 switch costs, 5 evidence weights" }
  - { k: Evaluated, v: "159 settings, official scorer" }
  - { k: Frozen, v: "3 profiles on the front" }
  - { k: Chosen on, v: "An open, fully labelled DFL match" }
verdict:
  label: Our read
  text: "The ranking is lexicographic, not a weighted sum, so collapsing the two metrics into one score throws away the information that matters. Keep the frontier, then decide with a rule you can defend."
sources:
  - { title: "EVALUATION (organisers' repository): baselines on the full match and the public window", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "RULES (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
  - { title: "Deb et al. (2002), NSGA-II", url: "https://doi.org/10.1109/4235.996017" }
  - { title: "The Shrewdies, technical report: the Pareto decision log", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/report/the-shrewdies-technical-report.pdf" }
related:
  - /challenges/spellf1-and-macrof1/
  - /architecture/evaluation-framework/
  - /datasets/dfl-idsse/
  - /challenges/rules-as-design-constraints/
---
## Why a frontier

Plot every candidate as a point: macroF1 on one axis, spellF1 on the other. A candidate is **dominated** when another is at least as good on both and better on one. What remains is the **Pareto frontier**: the settings where neither metric can improve without the other paying for it.

The official ranking is lexicographic. spellF1 decides; macroF1 only breaks ties. A weighted average of the two is a third metric nobody is ranked on.

## Where the tension comes from

One dial does most of it: the price of a change of state.

- **Cheap switches** follow the evidence closely. Frames improve, short possessions survive, and flicker starts splitting real spells.
- **Expensive switches** produce long, clean spells. Splits disappear, and so do genuine quick turnovers.

The organisers' baselines trace the same curve with a smoothing window: macroF1 peaks at ±25 frames, spellF1 at ±50, and both fall at ±125.

## How we searched it

Seven dials were free: the two switch costs and five evidence weights. Every other constant kept its physical meaning. The control radius stayed at 1.5 m on purpose: left free, the search drove it to 0.8 m, an artefact of a simulator that keeps the ball too close to the carrier.

The search ran on simulated matches with known answers, built from football rules of thumb: possessions of about 11 seconds, a third of them ending in a stoppage of about 20 seconds, the ball missing on 41% of frames. An evolutionary multi-objective search in the spirit of NSGA-II scored 159 settings with the official scorer. Three profiles were frozen from the front.

| Profile | Chosen as | Team switch cost | Alive/dead switch cost |
|---|---|---|---|
| Reasoned | Our starting values | 10.0 | 20.0 |
| Balanced | Best combined score | 8.35 | 12.50 |
| Macro (submitted) | Best frame accuracy | 4.23 | 9.43 |

The search taught two things: declare stoppages more readily, and keep the tags a light hint.

## How the point was picked

A simulator is a hypothesis. The decision went to real labels: one match from the open [DFL dataset]({{ '/datasets/dfl-idsse/' | relative_url }}), whose every frame carries the league's official possession and ball-status flags. We hid the ball in bursts to mirror the competition tracking, added position noise, and scored every profile with the official metric.

There the macro profile beat the balanced one on **both** metrics, 0.340 and 0.693 against 0.286 and 0.686. The simulator had ranked them the other way on spells. The reason is football: real matches contain many short possessions, and a decoder that waits eight to ten frames of clear control before changing team misses them. When the simulator and the world disagree, the world wins.

The full table, baseline included, is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page. Why a design should be selected this way at all is argued in [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}).

## Why five public minutes cannot choose

The organisers publish answers for one five-minute window. It contains 17 possessions. Their own figures show what that sample is worth:

| Baseline | spellF1, public window | spellF1, full match |
|---|---|---|
| Majority vote, ±50 frames | 0.3256 | 0.2433 |
| Majority vote, ±125 frames | 0.4242 | 0.2242 |

The window prefers the variant that loses on the full match. With 17 possessions, one possession moves spellF1 by about six points. Selecting on it is selecting on noise, and the rules forbid it in any case. We used the window for what it is for: confirming format, frame alignment and team orientation.
