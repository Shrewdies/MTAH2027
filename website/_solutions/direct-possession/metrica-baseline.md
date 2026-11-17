---
title: "Nearest-player baseline"
kicker: "Direct possession"
summary: "The organisers' reference method: give the ball to whoever stands closest, then vote over a window. It sets the bar and shows exactly where proximity stops being possession."
group: direct-possession
order: 10
chips: ["Tracking", "Ball-dependent", "Rule-based", "No training"]
motif: ribbon
motif_caption: "The nearest-player rule flickers frame by frame. Possession is the clean sequence underneath it."
motif_labels: ["Nearest-player rule", "Decoded possession", "Home", "Away", "Dead ball"]
facts:
  - { k: "Modality", v: "25 fps tracking with a tracked ball" }
  - { k: "Output", v: "H / A / D for every frame" }
  - { k: "Evidence", v: "Organisers' evaluation: spellF1 0.0486 raw, 0.2433 smoothed" }
  - { k: "Code and weights", v: "Runnable starter code; nothing learned" }
  - { k: "Licence", v: "Organisers' repository terms" }
verdict: { label: "Our read", text: "The right first cue and the wrong last word. Proximity is evidence; possession is a sequence." }
sources:
  - { title: "More Than a Hack 2027: organisers' repository with the baseline code", url: "https://github.com/metrica-sports/more-than-a-hack-2027" }
  - { title: "EVALUATION.md: metric definitions and baseline scores", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
related:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/direct-possession/vidal-event-tracking/
  - /solutions/physics-and-features/pitch-control/
  - /challenges/spellf1-and-macrof1/
  - /challenges/initial-challenge/
---
The baseline ships with the competition repository. For every frame it finds the player nearest the ball and gives possession to that player's team. A second variant smooths the result with a majority vote over a window of 50 frames either side, two seconds each way at 25 fps.

That is the whole method, and its transparency is the point. The organisers publish its scores next to the metric definitions: spellF1 0.0486 raw and 0.2433 smoothed on their reference. The raw figure is the instructive one. Per-frame proximity is right often enough to look respectable frame by frame, and wrong often enough to shatter possessions into fragments. spellF1 scores whole possessions, so fragments score almost nothing.

Three football situations break it. A pass in flight belongs to the passer's team until someone else controls it, yet the nearest player mid-flight is often a defender. A duel puts two opponents within a metre of the ball and flips the label with every stride. And when the ball is untracked there is no nearest player at all.

## Where it wins

- No parameters to fit, no labels, no compute. It runs anywhere and reproduces to the frame.
- It is the scoring reference. Any claim about a possession method starts with "against the baseline, on the same metric".
- With a fully tracked ball and slow play it is hard to beat by much. Closest player is the correct prior.

## What it costs

- Every flicker of the nearest player is a possession change. That is why raw spellF1 sits at 0.0486.
- The vote repairs flicker, not meaning. On open DFL labels degraded to competition conditions, the smoothed method returns 570 possessions where the truth holds 402.
- It has no model of a dead ball. A ball lying still beside a player waiting to take a throw-in is "possession" to this rule.
- Without a ball position it has no answer.

## How it plugs into possession

Keep the cue, drop the decision rule. Distance to the ball is the strongest single piece of possession evidence there is. The mistake is treating it as the label.

Our evidence decoder uses a stricter version of the same cue, a player within 1.5 m of the ball and closer than any opponent, as one evidence term among several, and gives the decision to an exact [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}). On open DFL labels degraded to match conditions that scores spellF1 0.340 against 0.235 for the smoothed baseline method.

The full table is on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page. What the organisers' four published baselines show about the two metrics is on [spellF1 and macroF1 pull apart]({{ '/challenges/spellf1-and-macrof1/' | relative_url }}).
