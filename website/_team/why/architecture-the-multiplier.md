---
layout: member-read
title: Architecture, the multiplier
permalink: /team/why-our-specialization-matters/architecture-the-multiplier/
nav_exclude: true
why_order: 7
wide: true
art: multiplier
members: [4]
summary: Four specialisms are four parts. Solution architecture decides how they join, in which order and against which proof, and it multiplies every one of them.
extra_css: [/assets/members/member.css, /assets/members/why.css]
wiring:
  spine: Architecture
  caption: Four specialisms land in one layered design. The analyst feeds two layers, and no layer is left to chance.
  parts:
    - { name: The analyst's questions, says: "What counts as control, and what a coach would accept.", to: [1, 4] }
    - { name: Perception, says: "Not observed is not the same as not there.", to: [5] }
    - { name: Geospatial thinking, says: "Who can reach the ball, in metres.", to: [4] }
    - { name: Delivery, says: "The same bytes on every run.", to: [6] }
  layers:
    - { name: Proof, lands: "The analyst signs off on what the model says" }
    - { name: Selection, does: "Parameters chosen away from the match" }
    - { name: Decision, does: "One exact decode per half" }
    - { name: Evidence, lands: "Football facts scored on every frame" }
    - { name: Observation, lands: "A missing ball is no evidence" }
    - { name: Constraints, lands: "A pinned container with no network" }
readings:
  before: Four readings, frame by frame
  after: One architecture, one sequence
  caption: Left alone, each reading flickers and none agrees with the next. Given an order, they become one sequence a coach can read.
proof:
  ours: The Shrewdies decoder
  base: Organisers' baseline method
  caption: One openly labelled DFL match, degraded to the competition's conditions. Higher is better on both metrics.
  metrics:
    - { name: spellF1, ours: "0.340", base: "0.235" }
    - { name: macroF1, ours: "0.693", base: "0.383" }
---

A squad can hold an analyst's questions, perception, geospatial thinking and delivery, and still ship four
separate answers. Architecture is the decision about how they join: in which order, across which seams,
against which proof. Made first, it multiplies every specialism. Skipped, it wastes them.

## One design, four owners

{% include member-why-figure.html id="wiring" %}

The analyst says possession holds through a loose ball. Perception says *not observed* is not *not there*.
In the architecture those two are one rule: a missing ball is no evidence. Geospatial thinking becomes the
evidence layer. Delivery becomes a pinned container with no network.

## Parts, or a system

{% include member-why-figure.html id="readings" %}

Evidence is scored on every frame. The decision is taken once per half, by an exact algorithm, over the
whole sequence. Keeping those two machines apart is the architectural call that turns flicker into
possessions.

## What it bought

{% include member-why-figure.html id="proof" %}

Tracking and tags in. Every parameter chosen away from the match. The result is measured on labels the
design had never seen.

The working drawings are public. Start with
[The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}), then walk the rest of
[Architecture]({{ '/architecture/' | relative_url }}).

A specialism is a strength. Architecture is what makes four people's strengths one system.
