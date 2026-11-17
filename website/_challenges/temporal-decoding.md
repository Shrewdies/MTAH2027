---
layout: wiki-entry
nav_exclude: true
title: Why possession is a decoding problem
kicker: The problem
summary: "A classifier answers what a frame looks like. A decoder answers which sequence of states best explains the whole half. Possession needs the second."
route_label: Decoding
hook: "Decode the whole half"
group: problem
order: 20
chips: [Sequence not frames, Offline, Three states]
motif: decoder
motif_caption: Three states per frame, one best path per half. A change of state has a price, so one noisy frame cannot buy a turnover.
motif_labels: [Home, Away, Dead ball, Best path]
facts:
  - { k: States, v: "H, A, D" }
  - { k: Scored unit, v: "A whole possession" }
  - { k: Mode, v: "Offline: past and future evidence" }
  - { k: Short spells, v: "A recovery can last 0.8 s, 20 frames" }
verdict:
  label: Our read
  text: "The risk is not noise, it is over-correction. Every smoother deletes flicker first and real short possessions second. The decoder has to make that trade explicitly, with a price per switch, and the price has to be chosen on real labels."
sources:
  - { title: "Rabiner (1989), A tutorial on hidden Markov models", url: "https://doi.org/10.1109/5.18626" }
  - { title: "EVALUATION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
related:
  - /challenges/possession-frame-by-frame/
  - /challenges/pareto-lens/
  - /architecture/decoding-alternatives/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
---
## Classifier, decoder, optimiser

An **instantaneous classifier** estimates which state looks likely at one moment. A **temporal decoder** chooses a consistent sequence, weighing evidence across time against the cost of changing state. A **temporal optimiser** is the general case: any search for the best sequence under a score.

Possession is defined by persistence, so the decoder is not post-processing. It is the model.

## The same frame, four answers

A frame carries positions, not a history. Each of these looks the same to a classifier whichever way the match went.

| What one frame shows | The label depends on |
|---|---|
| The ball two metres from an opponent | Whether it is a pass in flight or a ball he controls |
| An opponent touching the ball | Whether he keeps it or it runs on to the same team |
| No ball in the tracking | What was happening before it vanished |
| A still ball beside a player | Whether play stopped a second ago |

None of the four can be settled inside the frame. All four are settled by the frames around it.

## Offline changes the problem

A live system filters: it sees the past and the present. The challenge hands over complete recordings, so the decode can smooth: every frame is judged with the frames after it as well. A reception three frames later confirms the pass; a restart two seconds later confirms the stoppage. Decoding a whole half at once uses that for free.

{% include wiki/motif.html id="ch-lookahead" caption="Mid-pass, the nearest player is an opponent. With the past only, a live system leans away. With the reception three frames later in view, an offline decode keeps the passer's team." %}

## The failure that matters

A counter-press recovery can last 0.8 seconds: win it, lose it. To a smoother that is twenty frames of noise. To the scorer it is a possession, and deleting it also merges the two spells on either side into one that matches neither.

A sequence that looks cleaner can score worse. That is why the price of a switch cannot be set by eye.

## From the problem to the design

Which decoder to run, and at what price per switch, is a design decision. The candidates are compared in [Seven ways to decode a match]({{ '/architecture/decoding-alternatives/' | relative_url }}). The algorithm we chose is explained under [Viterbi decoding]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}). The fielded system, with its two switch costs, is [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}). Duration-aware decoding for the shortest possessions is on the [roadmap]({{ '/challenges/roadmap/' | relative_url }}).
