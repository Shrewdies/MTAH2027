---
layout: wiki-entry
nav_exclude: true
title: The ball goes missing where possession is decided
kicker: The data
summary: "The ball is untracked on 41% of graded frames, and not at random: in crowds, duels and the air. What a model assumes about those frames decides its score."
route_label: Ball gaps
hook: "No ball, no evidence"
group: data
order: 70
chips: [41% untracked, Crowds and aerial balls, Live play]
motif: trajectory
motif_caption: The tracker loses the ball in flight and in traffic. The possession does not pause with it.
motif_labels: [Tracked, Untracked, Possession held]
facts:
  - { k: Ball untracked, v: "41% of graded frames" }
  - { k: Typical gaps, v: "Crowds, duels, aerial balls" }
  - { k: Definition, v: "Loose or contested: the last team keeps it" }
  - { k: Our rule, v: "No ball, no evidence" }
verdict:
  label: Our read
  text: "Missing data is the central modelling decision of this challenge, not a preprocessing step. A model that maps a missing ball to dead ball invents stoppages inside possessions; a model that imputes a path and trusts it invents turnovers."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "CHALLENGE (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md" }
related:
  - /challenges/tactical-tracking/
  - /architecture/ball-aware-vs-ball-free/
  - /solutions/direct-possession/pathcrf/
  - /challenges/roadmap/
---
## What goes wrong with the ball

Two failures, and they pull in opposite directions.

- **The ball goes missing.** No position for a run of frames, on 41% of graded frames in all. The gaps are not random. They sit in crowds, in duels and under aerial balls.
- **A false ball appears.** A detection that is not the ball, for a few frames. To a naive model it is a phantom turnover.

The players have failure modes of their own: slots that change bodies, players that vanish or appear twice. Those are on [tactical tracking]({{ '/challenges/tactical-tracking/' | relative_url }}).

## Why nearest-player breaks

Proximity is not possession. During every pass the ball travels away from the passer and past opponents, so the nearest player changes team while possession does not. Add a ball that disappears for a second at a time and a per-frame rule has two bad options: guess, or call it dead.

Calling it dead is the common mistake. The ball is lost in the air and in crowded duels, which is live play at its most intense. The organisers' definition is explicit about those moments: through loose and contested phases, possession stays with the last team that had it.

## What the gap asks of a design

On a blank frame a model has three options: call it dead, fill in a ball, or score it as no evidence and let the sequence carry on. The first invents stoppages inside possessions. The second turns a plausible path into a measurement, and turnovers happen inside occlusions. We took the third.

The three are weighed, and the call explained, in [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}). The tools that filter or fill a ball track are the [Kalman filter and RTS smoother]({{ '/solutions/physics-and-features/ball-trajectory-kalman/' | relative_url }}) and [learned imputation]({{ '/solutions/classifiers-and-decoders/learned-imputation/' | relative_url }}).

## A turnover inside the gap

The hardest case is the one the tracker cannot show. A clearance goes up, the ball is lost in the air, two players contest the header, and it drops to the other side. Control changed hands on frames with no ball.

{% include wiki/motif.html id="ch-late" caption="One gap, one hidden turnover. Read the gap as dead and a stoppage is invented. Hold the last team and the label is right until the turnover, then late until the ball reappears." %}

Holding possession through silence is right on average and late at some turnovers: the evidence arrives only when the ball reappears. The late boundary costs most on short spells, which fall below the overlap thresholds of the ranking metric first. Recovering those hidden turnovers from the players alone is the first engine on our [roadmap]({{ '/challenges/roadmap/' | relative_url }}).
