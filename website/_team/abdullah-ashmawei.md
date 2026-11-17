---
layout: member
title: Abdullah Ashmawei
number: 4
nav_exclude: true
summary: No. 4 of The Shrewdies and the squad's AI solutions architect. He maps the design space before the code, across autonomous networks, geospatial intelligence and four years of professional education in football game analysis.
extra_css: [/assets/members/member.css, /assets/wiki/wiki.css, /assets/members/architect.css]
extra_js: [/assets/members/member.js, /assets/wiki/wiki.js, /assets/members/architect.js]
body_include: member-architect-body.html
stats:
  - { value: 4, label: Intelligence domains, note: "AI architecture, autonomous networks, geospatial and football intelligence" }
  - { value: 4, label: Years of football study, note: "Game analysis, set pieces and football AI" }
  - { value: 10, label: Professional journeys, note: "Countries in his career entries, from Japan to South Africa" }
  - { value: 3, label: Cultures, note: "Arabic, English and Spanish" }
ribbon: [AI solutions architecture, Design spaces, Evidence and decision, Autonomous networks, Geospatial intelligence, Football intelligence, Set pieces, Game analysis, Football AI, Closed-loop systems]
constellation: [Solution architecture, Autonomous networks, Geospatial intelligence, Football AI, Set pieces, Game analysis]
constellation_note: Two disciplines that rarely share a desk, the solution architect's and the football analyst's, held by one person.
highlights:
  - title: The design space first
    text: Before a model is chosen, every viable route goes on one page, with what it needs and what breaks it.
  - title: Evidence apart from decision
    text: What a frame says and what the match means are separate machines, each tested alone.
  - title: Constraints as design inputs
    text: Privacy, hardware and reproducibility are requirements, drawn in from the first line.
  - title: Decided on evidence
    text: The final call is made on data the design has never seen, by a rule written in advance.
  - title: One architect, two domains
    text: The architect's habits and the analyst's questions in one person, so football problems arrive framed as whole systems.
space:
  title: The design space
  statement: Several honest routes. One decision.
  problem: "Home, away|or dead?"
  decision: "The Shrewdies|decoder"
  gates: [One laptop, No labels, Same bytes]
  options:
    - { label: Video only, out: "one laptop, a few days" }
    - { label: Hybrid fusion, out: "one laptop, a few days" }
    - { label: Evidence + exact decode }
    - { label: One learned classifier, out: "no labels on the match" }
    - { label: Learned decoders, out: "no labels on the match" }
  steps:
    - { title: Frame, text: "One target: home, away or dead on every frame." }
    - { title: Compare, text: "Three sources of evidence and seven decoders, on one grid." }
    - { title: Constrain, text: "One laptop. No labels on the match. The same bytes on every run." }
    - { title: Decide, text: "Football evidence on every frame, one exact decode per half." }
anatomy:
  title: An architecture, layer by layer
  statement: The squad's decoder, from constraints to proof.
  layers:
    - { name: Proof, items: "Open DFL labels, the official scorer, both metrics" }
    - { name: Selection, items: "Pareto front of two objectives, frozen profiles" }
    - { name: Decision, items: "Exact Viterbi decode per half: home, away, dead" }
    - { name: Evidence, items: "Ball control, out of play, stillness, restarts, calibrated tags" }
    - { name: Observation, items: "Tracking and tags; a missing ball is no evidence" }
    - { name: Constraints, items: "Offline, one laptop CPU, deterministic, no labels on the match" }
loops:
  - title: Autonomous networks
    statement: People set the goals. The loop does the rest.
    art: member-architect-network.html
    steps:
      - { title: Observe, text: Every node reports. }
      - { title: Diagnose, text: The fault is located. }
      - { title: Act, text: Traffic takes another path. }
      - { title: Verify, text: The fix is confirmed. }
  - title: Geospatial intelligence
    statement: Three layers of a map, then the pitch.
    art: member-architect-geo.html
    steps:
      - { title: Coverage, text: Who reaches where. }
      - { title: Demand, text: Where the load sits. }
      - { title: Movement, text: How it flows. }
      - { title: The pitch, text: "The same questions, 105 by 68 m." }
football:
  title: Football intelligence
  statement: Three ways he reads a match.
  cards:
    - { art: analysis, title: Game analysis, text: "Shape, lanes and the space a team leaves." }
    - { art: setpiece, title: Set pieces, text: "Runs, screens and a delivery into the target zone." }
    - { art: ai, title: Football AI, text: "A state on every frame, even when the ball is out of sight." }
work:
  title: Body of work
  heading: Architecture
  statement: The design space of possession inference, drawn option by option, with the calls the squad made and the constraint behind each one.
  cta: Enter Architecture
  studies:
    - /architecture/the-shrewdies-decoder/
    - /architecture/single-source-of-truth/
    - /architecture/decoding-alternatives/
    - /architecture/ball-aware-vs-ball-free/
journeys:
  title: Professional journeys
  origin: eg
  places: [eg, sd, ye, sa, qa, ae, tr, za, ph, jp]
  facts:
    - { k: Today, v: "Dua, his current company" }
    - { k: Journeys, v: "From Japan and the Philippines to South Africa, Sudan and the Gulf" }
sources: "Profile facts: his public LinkedIn profile (current company and career locations) and the team's own records. The design space and the layers are those of the squad's Initial Challenge solution, documented in Architecture."
---

Abdullah Ashmawei wears number 4, the architect's shirt. He is the squad's AI solutions architect: he
decides what gets built, in which order and against which proof, before anyone writes a model.

## Solution architecture

Every real problem has several honest architectures. He lays them side by side, strikes the ones the
constraints cannot afford, and builds what is left.

## Autonomous networks

His specialisation is AI solutions architecture for autonomous networks: systems that observe themselves,
diagnose faults and act without waiting for a person.

## Geospatial intelligence

Networks are maps. Coverage, demand and movement all live in coordinates, and so does every event on a
football pitch.

## Football intelligence

Four years of professional education in football game analysis, set pieces and football AI. A dead ball
is where the two halves of his work meet: repeatable, measurable, the closest thing football has to a
solvable problem.
