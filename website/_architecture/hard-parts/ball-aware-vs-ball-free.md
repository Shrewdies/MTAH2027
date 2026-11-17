---
title: When the ball goes missing
kicker: The hard parts
summary: "What should a design believe on a frame with no ball? Three treatments of the blank frame, and two schools of evidence: measure the ball when it is there, or infer possession from how the players move."
group: hard-parts
order: 40
chips: [Missing ball, Ball-aware, Ball-free, Fielded]
motif: bp-silence
icon: trajectory
motif_caption: "One gap in the ball track, three treatments of the blank frames. Read them as a dead ball and a stoppage is invented. Guess a ball and the guess is scored as fact. Score nothing and the story continues."
facts:
  - { k: Ball untracked, v: "41% of graded frames in the Initial Challenge" }
  - { k: Ball-aware, v: "Proximity and relative motion to a seen ball" }
  - { k: Ball-free, v: "Possession from collective player motion" }
  - { k: Rule, v: "Not observed is not the same as not in play" }
verdict:
  label: Our read
  text: "A missing ball is an absence of evidence. Designs that turn it into evidence of a stoppage fail on exactly the frames that carry the match."
call:
  title: Why silence is no evidence
  constraint: Data reality
  text: "The ball is untracked on 41% of graded frames. The evidence stayed ball-aware, and a missing ball scores zero for every state, so possession stays with the last team in control until real evidence arrives. That one rule removed the stoppages a frame-by-frame reading invents inside possessions."
sources:
  - { title: "PathCRF: ball-free possession paths from player trajectories", url: "https://github.com/hyunsungkim-ds/pathcrf" }
  - { title: "More Than a Hack 2027: the possession rules", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md" }
  - { title: "Borghesi et al. (2023), ball possession with a temporal convolutional network", url: "https://doi.org/10.1016/j.eswa.2023.119780" }
  - { title: "Technical report: Who has the ball?", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/TECHNICAL.md" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/the-shrewdies-decoder/
  - /challenges/tracking-errors/
  - /solutions/direct-possession/pathcrf/
  - /solutions/physics-and-features/ball-trajectory-kalman/
  - /solutions/classifiers-and-decoders/learned-imputation/
---

## The design question

What should the system believe on a frame with no ball? Where and why the ball goes missing is measured in
[The ball goes missing where possession is decided]({{ '/challenges/tracking-errors/' | relative_url }}).
This study is about the design response: what a blank frame is allowed to mean.

## Three ways to treat a blank frame

| Treatment | Effect | Verdict |
|---|---|---|
| Missing ball means dead ball | Invents stoppages inside possessions | Breaks the spell metric |
| Interpolate a ball position | Feeds a guess to the evidence as a measurement | Hides the uncertainty |
| No evidence; the story continues | Possession stays with the last team in control | Matches the football rule |

The third is the rule of the game itself: through a loose or contested phase, possession stays with the
last team that had it until the opponent takes control.

## Two schools of evidence

| Question | Ball-aware | Ball-free |
|---|---|---|
| What it measures | Proximity and relative motion to the observed ball | How both teams move and react |
| Strongest when | The ball is tracked and on the ground | The ball is hidden |
| Vulnerable to | Missing and false ball detections | Identity errors, shift between providers |
| Must still solve | Telling a touch from sustained control | Telling a stoppage from slow play |

<div class="wiki-figures">
{% include wiki/motif.html id="trajectory" labels="Tracked|Untracked|No evidence" caption="Ball-aware: the ball is measured, then lost. Across the gap the uncertainty widens." %}
{% include wiki/motif.html id="graph" labels="Carrier|Hidden pass|Receiver" caption="Ball-free: the pass is inferred from how the players move around it." %}
</div>

The two combine. A tracked, credible ball dominates. Across a long gap, weight shifts toward what the
players are doing. The ball-free branch reports a belief about possession. It never writes a ball position
into the data.

## A third answer: fill the gap

Both schools accept the gap. The alternative is to remove it, by taking the ball from another witness that
still sees it. That is [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}).

## What breaks it in real football

- **An aerial duel.** The ball is gone while it is in the air and comes down to the other team. A ball-aware
  design learns of the turnover only when the ball reappears.
- **A false detection.** A white boot or a penalty spot becomes the ball for a few frames and hands
  possession to whoever stands nearby.
- **Slow play.** A centre-back with time on the ball looks, in player motion alone, like a team waiting for
  a restart.

## How to judge it

Split every score by ball visibility, and by the length of the gap the frame sits in. Then hide the ball
on purpose in labelled matches and watch how fast each design degrades. The slope is the measure.
