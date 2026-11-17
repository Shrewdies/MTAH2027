---
layout: wiki-hub
title: Solution Architecture
permalink: /architecture/
collection_index: architecture
families: true
kicker: Our DNA
summary: "How The Shrewdies architect football intelligence. Before a model is chosen, the whole design space goes on one board: every source of evidence, every engine, what breaks each in a real match, and the proof that settles it."
motif: bp-dna
motif_labels: [Observe, Evidence, Decode, Adjudicate, Prove]
motif_caption: "Two strands that never merge, evidence and decision, joined by five questions. Every study in this section answers one of them."
stats:
  - { value: "{count}", label: "studies, one question each" }
  - { value: "5", label: families of decisions }
  - { value: "9", label: "calls, each forced by a real constraint" }
  - { value: "1", label: architecture fielded and measured }
families_title: Five families of decisions
groups:
  - key: fielded
    title: On the pitch
    url: /architecture/fielded/
    motif: decoder
    motif_labels: [Home, Away, Dead, Cheapest path]
    blurb: "The architecture we fielded, and the calls that shaped it. Each call traces back to one hard constraint."
    points:
      - "Football evidence on every frame, one exact decode per half"
      - "spellF1 0.340 and macroF1 0.693 on open labels, against 0.235 and 0.383"
      - "Under ten seconds on a laptop CPU, the same bytes on every run"
    cta: See the decoder
  - key: map
    title: The map
    url: /architecture/map/
    motif: stack
    motif_labels: [Video frames, Tactical track, Broadcast track, One match state]
    blurb: "Where the evidence comes from: coordinates, pixels, or every witness reconciled into a single source of truth."
    points:
      - "Three witnesses of one match, each filling the gaps of the others"
      - "Tracking is physics you can audit; video is perception you must own"
      - "Reconcile, never blend: every value keeps its witness"
    cta: Open the map
  - key: engine
    title: The engine
    url: /architecture/engine/
    motif: ribbon
    motif_labels: [Evidence per frame, One coherent story, Home, Away, Dead ball]
    blurb: "How evidence on single frames becomes one coherent story of the half."
    points:
      - "Separate what a frame says from what the match means"
      - "The same scores, seven decoders, seven different stories"
      - "An ensemble is worth exactly the independence of its errors"
    cta: Open the engine
  - key: hard-parts
    title: The hard parts
    url: /architecture/hard-parts/
    motif: timeline
    motif_labels: [First half, Second half, Gap, Offset]
    blurb: "Six problems that decide whether a design survives a real match. None of them is about the model."
    points:
      - "A missing ball is no evidence. It is never a stoppage"
      - "A slot is not a player, and a touch is not a turnover"
      - "Alive or dead, and which team, are two separate questions"
    cta: Open the hard parts
  - key: proof
    title: Proof
    url: /architecture/proof/
    motif: pareto
    motif_labels: [macroF1, spellF1, Pareto front, Fielded]
    blurb: "How a design earns belief: on whole matches it has never seen, by a rule written in advance."
    points:
      - "Two official metrics that pull the dials in opposite directions"
      - "Explore on simulation, decide on open labels, check on the fixture"
      - "Nine questions the field has not settled, each with its decisive test"
    cta: Open the proof
featured_title: Three studies to start with
featured:
  - /architecture/the-shrewdies-decoder/
  - /architecture/single-source-of-truth/
  - /architecture/ball-aware-vs-ball-free/
---

## The whole design space, on one board

<div class="wiki-figures">
{% include wiki/motif.html id="bp-design-space" caption="Four families of decisions, left to right, and the route we fielded lit across them. Point at a column to isolate it. Select it to open the family." %}
</div>

Possession inference has one output, a state on every frame, and many honest routes to it. We draw all of
them before building any. The board reads left to right, in the order the decisions have to be made, and
the lit route is the one that went [on the pitch]({{ '/architecture/fielded/' | relative_url }}). The
dashed box is where the next one starts: [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}),
one match state reconciled from the video frames and both tracking feeds.

### One question, one study

Every study here answers one design question, and every concept has one home. A study states the
question so that two engineers would disagree about it, puts the options side by side, names what breaks
each one in football terms, and says how to judge it on matches the design has never seen. What the
problem, the data and the rules are is told in [Challenges]({{ '/challenges/' | relative_url }}). The
methods and tools of the field are mapped in [Solutions]({{ '/solutions/' | relative_url }}).

### Our calls

Some studies carry a box marked **Our call**. It appears only where a hard constraint of the Initial
Challenge decided the design: the competition rules, the labels that exist, the data as delivered, the
days available, or the need to regenerate the exact file. Each box states the constraint, the call and
what it bought. Where nothing forced a choice, the study is knowledge and nothing else.
