---
title: "Kalman filter and RTS smoother"
kicker: "Physics and features"
summary: "The classical estimator for a noisy, intermittently observed trajectory. It gives every ball position an uncertainty, and the uncertainty is the part possession inference needs."
group: physics-and-features
order: 30
chips: ["Tracking", "Classical", "No training", "BSD"]
motif: trajectory
motif_caption: "Measurements pull the estimate in. Through a gap the estimate coasts and its uncertainty grows."
motif_labels: ["Observed", "Predicted", "Covariance"]
facts:
  - { k: "Modality", v: "Noisy position measurements, gaps allowed" }
  - { k: "Output", v: "Smoothed positions, velocities and covariances" }
  - { k: "Evidence", v: "Classical state-space estimation; pykalman implements it" }
  - { k: "Code and weights", v: "Numerical library; nothing learned by default" }
  - { k: "Licence", v: "BSD (pykalman)" }
verdict: { label: "Our read", text: "Essential for cleaning a ball track, dangerous for inventing one. Keep the covariance." }
sources:
  - { title: "pykalman: Kalman filter, smoother and EM for Python", url: "https://github.com/pykalman/pykalman" }
related:
  - /solutions/classifiers-and-decoders/learned-imputation/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/physics-and-features/ruptures/
---
A Kalman filter keeps a running belief about a hidden state, here the ball's position and velocity, as a mean and a covariance. Each frame it predicts forward with a motion model, then corrects with the measurement, weighting the two by their uncertainties. When a measurement is missing it simply predicts, and the covariance grows.

The Rauch-Tung-Striebel smoother runs backward over the filtered result, so every estimate also uses the future. For offline work that is the one to use. A gap is bridged from both ends, and uncertainty peaks in the middle.

pykalman implements both, plus expectation maximisation for fitting the noise parameters.

## Where it wins

- Honest uncertainty. The covariance says how far to trust each position, including the invented ones.
- It removes measurement jitter, so speeds and accelerations derived from the track stop being noise.
- Short dropouts, a few frames of occlusion, are bridged correctly.
- It is linear algebra on a handful of numbers per frame. Speed is never the concern.

## What it costs

- The motion model is the assumption. Constant velocity is wrong at every kick, bounce, header and interception, which are the moments possession changes.
- Bridging a long gap draws a smooth path through whatever happened inside it. A pass, a tackle and a clearance can hide in one confident-looking line.
- Filtered positions look like data. Downstream code must carry the covariance, or it will treat guesses as observations.

## How it plugs into possession

Smooth, do not impute. Filtering the observed ball before computing distances and speeds is cheap, and it removes false touches caused by jitter.

Using the smoother to manufacture ball positions across long dropouts is a different act. It creates evidence the sensor never produced, exactly where the truth is least knowable.

The principled alternative passes the uncertainty on. A frame with no ball contributes no ball evidence, and the sequence model decides what happened across the gap. That is the call we made, explained in [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}). [Learned imputation]({{ '/solutions/classifiers-and-decoders/learned-imputation/' | relative_url }}) faces the same choice with a stronger motion model.
