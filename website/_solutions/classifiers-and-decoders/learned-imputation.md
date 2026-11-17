---
title: "Learned imputation (BRITS, PyPOTS)"
kicker: "Classifiers and decoders"
summary: "Neural models that fill gaps in multivariate time series. Strong on sensor dropouts, risky on a ball that vanishes while the game goes on."
group: classifiers-and-decoders
order: 110
chips: ["Time series", "Learned", "Missing data", "MIT / BSD-3-Clause"]
motif: trajectory
motif_caption: "The fill is the likeliest path through the gap, not the true one."
motif_labels: ["Observed", "Imputed", "Never measured"]
facts:
  - { k: "Modality", v: "Multivariate series with missing values" }
  - { k: "Output", v: "Imputed values; classification on incomplete input" }
  - { k: "Evidence", v: "NeurIPS 2018 (BRITS); documented toolkit (PyPOTS)" }
  - { k: "Code and weights", v: "BRITS authors' code; PyPOTS model library; training needed" }
  - { k: "Licence", v: "MIT (BRITS), BSD-3-Clause (PyPOTS)" }
verdict: { label: "Our read", text: "Powerful gap-fillers that default to the likeliest story. In possession, the unlikely frames are the ones that count." }
sources:
  - { title: "BRITS: Bidirectional Recurrent Imputation for Time Series (NeurIPS 2018)", url: "https://papers.nips.cc/paper/7911-brits-bidirectional-recurrent-imputation-for-time-series" }
  - { title: "BRITS: authors' code", url: "https://github.com/caow13/BRITS" }
  - { title: "PyPOTS: toolkit for partially observed time series (repository)", url: "https://github.com/WenjieDu/PyPOTS" }
related:
  - /solutions/physics-and-features/ball-trajectory-kalman/
  - /solutions/direct-possession/pathcrf/
  - /solutions/classifiers-and-decoders/gradient-boosted-trees/
---
BRITS treats missing values as variables of a recurrent network, not as holes to be filled beforehand. One RNN runs forward through the series and another runs backward. At each missing step both predict the value from their own history and from the other variables at that time, and a consistency loss ties the two directions together. Imputation and the downstream task train jointly, so the model learns to fill gaps in whatever way helps the task.

PyPOTS is the toolbox around that idea. It collects BRITS and its successors, attention-based imputers among them, behind one interface for imputation, classification and forecasting on partially observed series.

## Where it wins

- They use everything: past, future and correlation across variables. Player movement informs where the ball is.
- They learn non-linear dynamics that the motion model of a [Kalman filter]({{ '/solutions/physics-and-features/ball-trajectory-kalman/' | relative_url }}) cannot express.
- They can classify directly on incomplete input and skip explicit imputation.
- One library makes fair comparison between imputers easy.

## What it costs

- These are trained models. They need many sequences from the target distribution, with gaps like the real ones.
- An imputer learns typical continuations. A turnover inside a gap is atypical, so the model draws a smooth path through it and the turnover disappears.
- Imputed values carry no flag unless you add one. Downstream code will read them as measurements.
- A deep-learning dependency stack and real compute, for what is a preprocessing step.

## How it plugs into possession

With discipline, as a ball-position prior. An imputer trained on full tracking with synthetic dropouts can propose where an untracked ball probably is, and the proposal can enter a decoder as weak evidence with its uncertainty attached.

Without discipline it launders guesses into data. The safer design keeps missing frames missing, tells the model which frames they are, and lets sequence structure do the bridging. [PathCRF]({{ '/solutions/direct-possession/pathcrf/' | relative_url }}) goes further and drops the ball from the input entirely.
