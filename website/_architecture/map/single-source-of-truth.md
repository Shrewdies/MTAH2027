---
title: The single source of truth
kicker: The map
summary: "Three witnesses watch one match: the video frames, the tactical tracking and the broadcast tracking. Each has gaps the others can fill. This is the architecture that reconciles them into one match state per instant, in which every value remembers which witness supplied it."
group: map
order: 10
chips: [Three witnesses, Fusion, Provenance]
motif: bp-truth
icon: stack
motif_caption: "Three lanes with gaps flow into one state with none. Each filled stretch keeps the colour of the witness that supplied it. That record is what makes it a source of truth, not a blend."
facts:
  - { k: Witnesses, v: "Video frames, tactical tracking, broadcast tracking" }
  - { k: Prerequisites, v: "One clock and one pitch, before any value is compared" }
  - { k: Design choice, v: "Where the witnesses are joined: early, late, in two steps, or behind a gate" }
  - { k: Rule, v: "Fill gaps, adjudicate conflicts, overwrite nothing" }
verdict:
  label: Our read
  text: "The missing ball is a missing measurement before it is a modelling problem, and the measurement often exists in another witness. Join the witnesses late and behind a gate, keep the provenance of every value, and the result can be audited. Join them early and it is a blend nobody can take apart."
call:
  title: Why the fielded decoder read one witness
  constraint: Time and reproducibility
  text: "The Initial Challenge window was a matter of days, and the organisers regenerate the exact file from an offline, CPU-only run. The fielded decoder therefore read the tactical tracking and the tags, and treated every gap as no evidence. This architecture is where the hidden-ball work goes next, and the decoder's evidence layer already has the seam for it."
sources:
  - { title: "More Than a Hack 2027: the data", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "SoccerNet Game State Reconstruction", url: "https://github.com/SoccerNet/sn-gamestate" }
  - { title: "SoccerNet Replay Grounding", url: "https://github.com/SoccerNet/sn-grounding" }
  - { title: "PnLCalib: points-and-lines pitch calibration", url: "https://github.com/mguti97/PnLCalib" }
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
related:
  - /architecture/match-timeline/
  - /architecture/multi-camera-geography/
  - /architecture/confidence-and-provenance/
  - /architecture/the-shrewdies-decoder/
  - /challenges/data-asset-map/
  - /solutions/vision-and-calibration/sn-gamestate/
---

## The design question

How do three imperfect witnesses become one account of the match? A tracker loses the ball in a crowd.
Another camera, or the pixels themselves, often still have it. The art is to fill each gap from the witness
that saw it, and never to pretend a filled value was measured where it was not.

## Three witnesses, three kinds of gap

| Witness | What it sees | Its gaps |
|---|---|---|
| **Video frames** | The ball when a tracker has lost it; contact; shirt numbers | Cuts, replays, a partial view, compute |
| **Tactical tracking** | The whole pitch, steady geometry, the clock the score is counted on | The ball is untracked on 41% of graded frames; players carry a team, no identity |
| **Broadcast tracking** | Close detail around the ball | Part of the pitch, cuts and replays, calibration valid only part of the time |

No witness is complete. Together they nearly are, because their gaps fall in different places. What each
asset contains is set out in [the data asset map]({{ '/challenges/data-asset-map/' | relative_url }}).

## Before any value is compared

Two prerequisites, each with its own study. Neither is repeated here.

1. **One clock.** Every source is mapped onto the tactical frame, segment by segment, replays included:
   [One clock for the match]({{ '/architecture/match-timeline/' | relative_url }}).
2. **One pitch.** Every view is calibrated to the pitch plane, with its own error:
   [Space is not time]({{ '/architecture/multi-camera-geography/' | relative_url }}).

A value that fails either test does not reach reconciliation.

## Where the witnesses are joined

This is the design decision of the study. The same three witnesses and the same output; what changes is
where in the pipeline they meet, and how much each is trusted at that moment.

{% include wiki/motif.html id="bp-fusion" caption="Four places to put the join. The further right it sits, the longer each witness stays separately inspectable." %}

| Option | Right when | What it costs |
|---|---|---|
| **Early**: join the features, one model | Clocks are tight and labels are plentiful | One clock error poisons every feature; nothing can be audited per witness |
| **Late**: a model each, join the scores | Witnesses fail independently | Every model's scores must be calibrated |
| **Hierarchical**: alive or dead first, then team | The two questions lean on different witnesses | An early mistake propagates to the second step |
| **Reliability-gated**: weight each by its trust now | Availability changes frame by frame, as it does here | The gate itself has to be trusted |

For a match where the ball vanishes from one witness and reappears in another, the join belongs late and
behind a gate. The gate reads availability and alignment confidence. It never reads the answer.

## Nothing is overwritten

| Situation | Rule | What is recorded |
|---|---|---|
| One witness has the value | Take it | The witness and its confidence |
| A gap here, a value there | Fill from the other witness | The witness, "filled", the alignment confidence |
| Two witnesses disagree | Adjudicate by reliability at that instant | Both values and the ruling |
| Nobody saw it | Leave it missing | "No evidence" |

The original tracking is still there after reconciliation, beside what was recovered and what was imputed.
Any value can be traced back to the witness that produced it. The fields of that record are defined in
[Confidence and provenance]({{ '/architecture/confidence-and-provenance/' | relative_url }}).

## How the decoder reads it

The decoder's rule does not change: a missing ball is no evidence. What changes is how often the ball is
missing. A filled ball position enters the evidence layer as a measurement weighted by its confidence. A
gap nobody could fill stays silent, and the story continues. The decoder gets better without becoming a
different decoder, which is why
[the Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}) has this seam in its
evidence layer.

## What breaks it in real football

- **Agreement that is not corroboration.** Two tracking streams built on similar computer vision share the
  same blind spots. They agree, and they are wrong together. Shared ancestry makes two witnesses one.
- **Selective coverage.** The broadcast camera is absent exactly when it cuts to a close-up, which is often
  when possession is contested.
- **A confident fill.** A guess recorded as a measurement is worse than an honest gap.

## How to judge it

On labelled matches, hide the ball in the primary witness and count how many hidden frames another witness
fills correctly. Count the wrong fills separately. Measure how often the witnesses err together, because
the gain comes only from errors that do not overlap. Then score possession on the filled frames alone.
