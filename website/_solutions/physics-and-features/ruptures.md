---
title: "ruptures"
kicker: "Physics and features"
summary: "Offline change-point detection. Give it a signal and it returns the instants where the signal's behaviour changes: candidate touches, restarts and stoppages."
group: physics-and-features
order: 40
chips: ["Time series", "Classical", "No training", "BSD-2-Clause"]
motif: changepoint
motif_caption: "Ball speed runs in regimes. Breaks between them mark the frames where something acted on the ball."
motif_labels: ["Ball speed", "Touch", "Flight phases"]
facts:
  - { k: "Modality", v: "Any univariate or multivariate time series" }
  - { k: "Output", v: "Change-point indices" }
  - { k: "Evidence", v: "Signal Processing review (2020); maintained library" }
  - { k: "Code and weights", v: "Python package; algorithms only" }
  - { k: "Licence", v: "BSD-2-Clause" }
verdict: { label: "Our read", text: "A sharp, label-free boundary detector. It tells a decoder where something happened and nothing about what." }
sources:
  - { title: "ruptures: change point detection in Python (repository)", url: "https://github.com/deepcharles/ruptures" }
  - { title: "Selective review of offline change point detection methods (Signal Processing, 2020)", url: "https://doi.org/10.1016/j.sigpro.2019.107299" }
related:
  - /solutions/classifiers-and-decoders/bocpd/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/hsmmlearn/
---
ruptures implements the family of offline change-point algorithms reviewed by Truong, Oudre and Vayatis. Each method combines three choices: a cost function that says how well one segment is described by a simple model, a search method that explores possible segmentations, and a constraint, either a known number of breaks or a penalty per break.

The workhorse is PELT, an exact search with pruning that finds the optimal penalised segmentation efficiently. Dynamic programming handles a fixed number of breaks. Binary segmentation and window methods trade exactness for speed. Kernel costs detect changes that are not simple shifts in mean.

## Where it wins

- Model-free boundaries. It needs a signal, not labels.
- Exact optimisation for a stated cost, so results are reproducible and explainable.
- It takes multivariate input: ball speed, heading and height together.
- Mature, small and permissively licensed.

## What it costs

- It finds changes in the signal, not changes of possession. A pass, a dribble touch and a deflection all break the ball's motion. Only some change the possessor.
- The penalty sets how many breaks you get, and football offers no label-free way to choose it.
- Offline only. It needs the whole sequence.
- It has no notion of which state follows a break.

## How it plugs into possession

As a boundary proposer. A sequence decoder decides states and boundaries jointly, and change-points give it independent evidence about where boundaries are plausible. The clean integration lowers the switching cost at detected breaks in ball kinematics. Possession changes become cheap where the ball's motion changed and expensive where it did not.

It has a second use on the players. A collective drop in speed is the signature of a stoppage, and a change-point on team speed marks dead-ball boundaries without the ball.

For live use, the online counterpart is [Bayesian change-point detection]({{ '/solutions/classifiers-and-decoders/bocpd/' | relative_url }}).
