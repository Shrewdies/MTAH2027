---
title: Seven ways to decode a match
kicker: The engine
summary: "The same per-frame scores, seven different stories. What each decoder assumes about football, what it needs, what it guarantees and how it fails."
group: engine
order: 20
chips: [Viterbi, HMM, CRF, HSMM]
motif: bp-decoders
icon: decoder
motif_caption: "One strip of raw scores, three decoders. A majority filter deletes a real short spell, Viterbi keeps it because the evidence paid for it, a duration model stretches it to fit its prior."
facts:
  - { k: Input, v: "Home, away, dead scores per frame" }
  - { k: Output, v: "One state per frame, as complete spells" }
  - { k: Exact, v: "Viterbi, HMM and HSMM are; neural refiners are not" }
  - { k: Trap, v: "The most likely sequence is not the best spellF1" }
verdict:
  label: Our read
  text: "Start with Viterbi. It is exact, it needs no labels, and its two switch costs mean something a coach could argue with. Add duration only when short-spell errors prove it is needed."
call:
  title: Why Viterbi writes the sequence
  constraint: Labels, time and reproducibility
  text: "A CRF and neural refiners learn their transitions from labelled sequences, and the rules gave us none from the match. In a window of days we fielded the decoder that needs neither labels nor duration statistics: exact Viterbi, one half at a time, with a fixed cost per change of state. It returns the optimal path and the same bytes on every run."
sources:
  - { title: "Rabiner (1989), a tutorial on hidden Markov models", url: "https://doi.org/10.1109/5.18626" }
  - { title: "Yu (2010), hidden semi-Markov models", url: "https://doi.org/10.1016/j.artint.2009.11.011" }
  - { title: "Lafferty, McCallum and Pereira (2001), conditional random fields", url: "https://www.cs.columbia.edu/~jebara/6772/papers/crf.pdf" }
  - { title: "ruptures: change-point detection", url: "https://github.com/deepcharles/ruptures" }
related:
  - /architecture/chained-classifier-and-decoder/
  - /architecture/ensemble-logic/
  - /architecture/the-shrewdies-decoder/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hsmmlearn/
  - /solutions/classifiers-and-decoders/temporal-action-segmentation/
---

## The design question

Given three scores per frame, which sequence of states is the match? Every decoder answers with a
different assumption about how possession behaves in time. This study compares the assumptions. How the
algorithm itself works is on the
[Viterbi page]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) in Solutions.

## The options

| Decoder | Needs | Guarantees | How it fails |
|---|---|---|---|
| Majority filter | Nothing | Local smoothness only | Deletes short spells by design |
| Viterbi with switch costs | Nothing | The best path under an additive score | Persistence delays a turnover |
| HMM forward-backward | Optional labels | Uncertainty over the whole sequence | Generative assumptions misfit |
| CRF | Labelled sequences | Learned, feature-dependent transitions | Calibration, label supply |
| HSMM | Duration statistics | The best path with explicit spell length | A wrong prior bends unusual spells |
| Change-point, then segments | Nothing | Explicit boundaries | A missed boundary is gone for good |
| MS-TCN, ASFormer | Substantial labels | None; learned refinement | Over-smoothing, transfer mismatch |

Only the three that need nothing (majority, Viterbi, change-point) can be fielded by a design without
labels. Majority, Viterbi and HSMM can be audited step by step. A neural refiner trades that away for
capacity.

## The dial every decoder has

Whatever the family, a decoder has a setting for how hard it is to change state. Turn it up and false
splits disappear. Keep turning and real possessions disappear with them.

{% include wiki/motif.html id="bp-s-cost" caption="False splits fall and false merges rise as the switch cost goes up. The same evidence decodes to seven possessions, three or one. The curves are schematic." %}

## Two principles

**Hold the evidence constant.** Compare decoders on identical per-frame scores. Change both stages at once
and no improvement can be attributed to either.

**The likeliest sequence is not the best-scoring one.** A decoder maximises its own objective. The ranking
metric rewards whole possessions matched to whole possessions. The two part ways exactly on short spells,
so the per-spell score has to be measured, never assumed.

## What breaks each in real football

- **A one-touch interception.** Real, short, and the first casualty of any smoothing filter.
- **A scramble in the box.** Evidence alternates frame by frame. Viterbi holds the previous owner, which is
  the football rule: possession stays until the opponent controls.
- **A long dead ball.** It looks abnormal to a duration prior learned on open play.

## How to judge it

Count false splits, false merges and missed short spells separately. They are three different diseases,
and the dial above trades one for another.
