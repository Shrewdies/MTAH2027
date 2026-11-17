---
title: Confidence and provenance
kicker: Proof
summary: "Three different uncertainties hide behind the word confidence: was it seen, is it the same instant, and which state explains it. Provenance keeps them apart and keeps the answers out of the inputs."
group: proof
order: 20
chips: [Uncertainty, Provenance, Leakage]
motif: bp-provenance
icon: gauge
motif_caption: "Three dials that are never averaged write into one frame record. An ambiguous frame is flagged as ambiguous, and answer-bearing fields stay behind a wall."
facts:
  - { k: Observation confidence, v: "Was the ball or player really seen?" }
  - { k: Alignment confidence, v: "Do two sources show the same instant?" }
  - { k: Model confidence, v: "Which state best explains the evidence?" }
  - { k: Leakage rule, v: "Answer-bearing fields never become features" }
verdict:
  label: Our read
  text: "One averaged confidence is a way to lose information. Carry the three separately, flag an ambiguous frame as ambiguous, and make every value able to say where it came from."
sources:
  - { title: "More Than a Hack 2027: the rules", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
  - { title: "More Than a Hack 2027: FAQ", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
  - { title: "Bassek et al. (2025), DFL open tracking and event data, Scientific Data 12:195", url: "https://www.nature.com/articles/s41597-025-04505-y" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/evaluation-framework/
  - /architecture/ensemble-logic/
  - /challenges/rules-as-design-constraints/
  - /on-device/security-data-protection/
  - /datasets/dfl-idsse/
---

## The design question

What does a possession system know about its own answer? "Confidence 0.8" means nothing until it is clear
which doubt it measures. A design that reconciles witnesses or gates experts lives or dies on that
distinction.

## Three confidences

| Confidence | Question | Fails when |
|---|---|---|
| Observation | Was the object really measured on this frame? | An imputed value is stored as a measurement |
| Alignment | Do these two frames show the same instant? | A replay is joined as live |
| Model | Which state best explains the evidence? | Scores are uncalibrated, or trained on another provider |

## The provenance record

Every value should be able to answer seven questions.

| Field | Answers |
|---|---|
| Source and native frame | Which witness produced it, and when on its own clock |
| Master-clock frame | Which tactical frame, or range of frames, it maps to |
| Observed or imputed | Was it measured, filled from another witness, or guessed |
| Tracking quality | How far the measurement itself can be trusted |
| Calibration quality | How far its position on the pitch can be trusted |
| Timing error | How far its instant can be trusted |
| Model and parameters | What produced the class scores |

This is the record that [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }})
writes for every value it reconciles.

## The leakage boundary

Some fields carry the answer. On open data such as the DFL release, the league's possession and
ball-status flags are the target a model is scored against. They can supervise training on other matches.
They are never an input at inference, on any match. The same wall stands around any ground truth and any
human note about the fixture being graded. The rules behind that wall are read as engineering requirements
in [The rules are the architecture]({{ '/challenges/rules-as-design-constraints/' | relative_url }}).

## What breaks it in real football

- **False certainty in a scramble.** The model reports 0.95 for home through a goalmouth melee because its
  inputs were interpolated, and nothing downstream knows.
- **A confident wrong clock.** Geometry is perfect and the frames are from different moments.
- **A gate trusting the loudest expert.** Without calibration, confidence measures temperament.

## How to judge it

{% include wiki/motif.html id="bp-s-reliability" caption="A reliability diagram. An honest model sits on the diagonal. An overconfident one bows below it, and the same model on another provider's data bows further. The curves are schematic." %}

Draw it on held-out matches, then again on data from another provider. Then check that the frames flagged
uncertain are the frames that are wrong more often.
