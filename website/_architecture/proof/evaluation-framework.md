---
title: Two metrics, one verdict
kicker: Proof
summary: "How a possession design earns belief when its two official metrics disagree and its fixture cannot be tuned on. The lenses to report, the stages of selection, and the rule that picks one point."
group: proof
order: 10
chips: [Evaluation design, Pareto, Held-out matches]
motif: bp-pareto
icon: pareto
motif_caption: "Three stages, one job each. Explore on simulated matches, decide on open labels, check on the fixture. The bars are the spellF1 of each frozen profile on the open DFL match."
facts:
  - { k: Official metrics, v: "spellF1 ranks, macroF1 breaks ties" }
  - { k: Unit of validation, v: "A whole match, held out" }
  - { k: Selection rule, v: "Lexicographic, as published" }
  - { k: Stages, v: "Explore, decide, check" }
verdict:
  label: Our read
  text: "Coherence beats twitchiness. A system that flickers can look fine frame by frame and still tell the wrong story, so the per-spell score is the one to design for and the per-frame score is the one to diagnose with."
call:
  title: Why open labels from another league decided
  constraint: Competition rules
  text: "No training or tuning on the match, and the public five-minute window is a correctness check only: it holds 17 possessions, so one possession moves spellF1 by about six points. The search explored on simulated matches and the fielded profile was chosen on an open DFL match degraded to the competition's conditions, where it scores spellF1 0.340 and macroF1 0.693 against 0.235 and 0.383 for the organisers' baseline method."
sources:
  - { title: "Official evaluation (spellF1, macroF1)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "More Than a Hack 2027: the rules", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
  - { title: "Deb et al. (2002), NSGA-II, IEEE Transactions on Evolutionary Computation 6(2)", url: "https://doi.org/10.1109/4235.996017" }
  - { title: "Bassek et al. (2025), DFL open tracking and event data, Scientific Data 12:195", url: "https://www.nature.com/articles/s41597-025-04505-y" }
  - { title: "Technical report: the Pareto decision log", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/TECHNICAL.md#6-choosing-the-parameters-the-pareto-decision-log" }
related:
  - /architecture/the-shrewdies-decoder/
  - /architecture/confidence-and-provenance/
  - /challenges/spellf1-and-macrof1/
  - /challenges/pareto-lens/
  - /challenges/rules-as-design-constraints/
  - /datasets/dfl-idsse/
---

## The design question

How does a possession system earn belief? The two official metrics are defined, with the organisers' own
numbers, in [spellF1 and macroF1 pull apart]({{ '/challenges/spellf1-and-macrof1/' | relative_url }}). With
those two in disagreement, a fixture that cannot be used for tuning and a public sample too small to choose
on, evaluation has to be designed like any other part of the system.

## What to report: seven lenses

| Lens | Report |
|---|---|
| Per-frame state | Precision, recall and F1 for home, away, dead; the confusion matrix |
| Per-spell possession | spellF1, false splits, false merges, missed short spells |
| Boundary | Missed and early changes: team to team, live to dead, dead to live |
| Observability | Every score split by ball tracked and ball missing |
| Robustness | Slots shuffled, players dropped, coordinate noise, clock jitter |
| Probability quality | Calibration, entropy, confidence against correctness |
| Complementarity | Error correlation between experts, source ablations |

Only the first two are official. The rest explain a score. They never replace it.

## How to select: three stages, one rule

| Stage | Data | Job |
|---|---|---|
| Explore | Simulated matches with known answers | Map the front cheaply, find the sensitive dials |
| Decide | Openly labelled real matches, held out whole | Pick the point on the front |
| Check | The fixture's public window | Format, alignment, team orientation. Nothing else |

Keep the whole front of settings where neither metric improves without the other paying, then select by
the organisers' own lexicographic rule. A hand-made weighted blend of the two is a third metric nobody is
ranked on. A simulator is a hypothesis about football: when it disagrees with real labels, the labels
win. How our own search ran is told in [The Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}).

## What breaks evaluation in real football

- **Frames from one match in both sets.** Neighbouring frames are near-copies. Splitting by frames leaks the answer.
- **Another provider's definition.** A league's possession flag and a competition's rule can differ at the
  edges: loose balls, restarts, contested phases.

## How to judge the judge

{% include wiki/motif.html id="bp-s-degrade" caption="An open match arrives clean. Three filters make it look like the fixture, and only then is it scored. Both methods lose on the degraded match, and that is the score that says something about the target." %}

Score with the official code, unchanged. If a result cannot be reproduced from public data by someone
else, it is a claim and not a measurement. The full results table is on the
[Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page.
