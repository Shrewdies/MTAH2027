---
title: "Gradient-boosted trees (LightGBM, XGBoost)"
kicker: "Classifiers and decoders"
summary: "The strongest general-purpose learners for tabular data. Give each frame a row of distances, speeds and visibility flags and they return H/A/D probabilities."
group: classifiers-and-decoders
order: 50
chips: ["Feature table", "Learned", "Needs labels", "MIT / Apache-2.0"]
motif: tree
motif_caption: "Each split asks one football question. Many small trees add up to a probability for every frame."
motif_labels: ["Frame table", "Splits", "H / A / D"]
facts:
  - { k: "Modality", v: "One feature row per frame, derived from tracking" }
  - { k: "Output", v: "Class probabilities per frame" }
  - { k: "Evidence", v: "KDD 2016 (XGBoost); NeurIPS 2017 (LightGBM)" }
  - { k: "Code and weights", v: "Production libraries; no football weights exist" }
  - { k: "Licence", v: "MIT (LightGBM), Apache-2.0 (XGBoost)" }
verdict: { label: "Our read", text: "The first supervised model to try on any tracking table, and never without a decoder behind it." }
sources:
  - { title: "LightGBM repository", url: "https://github.com/lightgbm-org/LightGBM" }
  - { title: "LightGBM: A Highly Efficient Gradient Boosting Decision Tree (NeurIPS 2017)", url: "https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree" }
  - { title: "XGBoost repository", url: "https://github.com/dmlc/xgboost" }
  - { title: "XGBoost: A Scalable Tree Boosting System (KDD 2016)", url: "https://doi.org/10.1145/2939672.2939785" }
related:
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /solutions/classifiers-and-decoders/pytorch-tcn/
  - /solutions/classifiers-and-decoders/learned-imputation/
---
Gradient boosting builds an ensemble of small decision trees, each fitted to the errors of the ensemble so far. XGBoost made the recipe industrial: regularised objectives, second-order optimisation, and a sparsity-aware split search that learns a default direction for missing values. LightGBM made it fast: histogram-based splits, leaf-wise growth, and sampling and feature-bundling techniques that cut training time on large tables.

For possession the table writes itself. One row per frame: distance from the ball to the nearest player of each team, the gap between those distances, ball speed and acceleration, whether the ball is visible, time since it last was, mean player speed. Add the same quantities over rolling windows and the model sees short-term context.

| | LightGBM | XGBoost |
|---|---|---|
| Tree growth | Leaf-wise | Level-wise by default |
| Missing values | Handled natively | Learned default direction |
| Licence | MIT | Apache-2.0 |

## Where it wins

- Missing values are first-class. A hidden ball is a value the trees route explicitly, not a hole to impute.
- They train and predict on a laptop CPU.
- Feature attributions show which cue drove each decision.
- Robust to feature scaling, outliers and mixed units. A strong baseline needs little tuning.

## What it costs

- Supervised. They need frame-level labels from data that looks like the target feed.
- Frames are scored independently. Output flickers at every ambiguous moment, and flicker is fatal for spell metrics.
- They learn the label provider's definition of possession, quirks included.
- The features are the model. Geometry the table does not contain cannot be learned.

## How it plugs into possession

As the emission model in front of a decoder. Trees turn evidence into per-frame probabilities, and a [Viterbi]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) pass turns probabilities into possessions. This pairing is the pragmatic supervised recipe on tracking data, and the one to beat before reaching for [temporal convolutions]({{ '/solutions/classifiers-and-decoders/pytorch-tcn/' | relative_url }}) or [graph networks]({{ '/solutions/classifiers-and-decoders/graph-network-toolkits/' | relative_url }}).

The division of labour matters. Do not ask trees to be smooth through window features alone. Let them be sharp, and let the decoder own time.

For the Initial Challenge we fitted nothing: trees need frame labels, and the rules allow none on the match. The call is explained in [Evidence, then a decoder]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}).
