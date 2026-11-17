---
layout: wiki-entry
nav_exclude: true
title: spellF1 and macroF1 pull apart
kicker: Scoring
summary: "macroF1 counts frames. spellF1 counts possessions. The organisers' own baselines show how far the two can disagree: 0.65 on frames, 0.05 on possessions."
route_label: Metrics
hook: "Count possessions, not frames"
group: scoring
order: 30
chips: [spellF1 ranks, macroF1 breaks ties, Temporal IoU]
motif: ch-spells
motif_caption: Predicted spells are matched one to one against true spells by temporal overlap. A split spell scores once at best; the extra piece is a false possession.
motif_labels: [Truth, Predicted, Match, Split or merged, Missed]
facts:
  - { k: Ranking metric, v: "spellF1" }
  - { k: Tie-break, v: "macroF1 over H, A, D" }
  - { k: IoU thresholds, v: "0.3 to 0.7, averaged" }
  - { k: Best baseline, v: "spellF1 0.2433 (smooth50)" }
verdict:
  label: Our read
  text: "spellF1 rewards a system that tells the match as a sequence of possessions with the right boundaries. Frame accuracy is necessary and nowhere near sufficient: the ranking is decided by splits, merges and short spells."
sources:
  - { title: "EVALUATION (organisers' repository): metric definitions and baseline scores", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "FAQ (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
related:
  - /challenges/pareto-lens/
  - /challenges/temporal-decoding/
  - /architecture/evaluation-framework/
---
## Two metrics, two units

| Metric | Unit of success | Role | What it punishes |
|---|---|---|---|
| macroF1 | A frame, averaged over H, A and D | First tie-break | Wrong states on graded frames |
| spellF1 | A whole possession | Ranking | Splits, merges, missed short spells |

**macroF1** is the mean of three per-class F1 scores, so dead ball counts as much as either team.

**spellF1** treats each unbroken H or A run as one object. Predicted spells are matched one to one against true spells, a match counts when their temporal intersection-over-union clears a threshold, and the F1 is averaged over five thresholds: 0.3, 0.4, 0.5, 0.6 and 0.7. Dead-ball stretches end spells; they are not spells themselves.

## What the published baselines show

The organisers publish four baselines in their EVALUATION document. All four take the nearest tracked player to the ball; three then apply a majority vote over a window of frames.

| Baseline | macroF1 | spellF1 |
|---|---|---|
| Nearest player, raw | 0.6532 | 0.0486 |
| Majority vote, ±25 frames | 0.6752 | 0.1996 |
| Majority vote, ±50 frames | 0.6724 | 0.2433 |
| Majority vote, ±125 frames | 0.6356 | 0.2242 |

Read the rows, not the columns.

- **Raw nearest player** is a respectable frame classifier and a useless possession model. It scores 0.65 on frames and 0.05 on spells: the flicker shreds every possession into fragments.
- **Two seconds of smoothing** multiplies spellF1 by four and moves macroF1 by two points. The frames were mostly right already; the story was not.
- **The peaks sit in different places.** macroF1 is best at ±25, spellF1 at ±50. Past that both fall: the window starts deleting real possessions.

No single setting wins both. That is the whole case for [the Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}).

## The four ways to lose a spell

- **False split.** One true possession predicted as two. At most one piece can match; the other is a false positive.
- **False merge.** Two true possessions predicted as one. One true spell goes unmatched, and the merged spell overlaps neither well.
- **Missed short spell.** A two-second possession smoothed away. It costs almost nothing in frames and a full spell in recall.
- **Late boundary.** A turnover detected a second late shrinks the overlap. Short spells fall below the higher IoU thresholds first.

## Abstaining is not an exit

`X` is allowed on any frame. macroF1 counts it as a miss. For spellF1 each `X` is filled with the last non-X label in the same half before matching, and back-filled at the start of a half. Going quiet inside a possession costs nothing on spells; going quiet across a turnover carries the old team over the hand-over. The metric still demands a decision at every boundary.

## What it changes in the design

The same over-splitting shows up on real external labels. On an open DFL match degraded to the competition's conditions, the organisers' baseline method reports 570 possessions where the match has 402. Our decoder is built the other way round: a switch has a price, so a possession has to be earned. The full table is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page.
