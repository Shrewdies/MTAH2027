---
layout: wiki-hub
title: Proof
permalink: /architecture/proof/
collection_index: architecture
only_group: proof
family: true
parent: /architecture/
nav_exclude: true
kicker: "Family 05 of 05"
summary: "A design is a hypothesis until it is measured on matches it has never seen, by a rule written before the numbers came in."
motif: bp-decision
motif_labels: [proof]
motif_caption: "The decision map of this family. Each question leads to the study that answers it."
stats:
  - { value: "{count}", label: studies in this family }
  - { value: "3", label: stages of selection }
  - { value: "9", label: questions the field has not settled }
---

## How belief accumulates

No single test makes a design credible. Belief is built in gates, and each gate proves one thing and
nothing more.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-belief" caption="Four gates, each a step up: the logic is right, the dials are sane, it works on real football, and someone else gets the same number. The fixture's public window sits off the ladder: it checks the file and adds no belief about quality." %}
</div>

## Every claim becomes a test

The other four families make claims. This one turns each claim into the test that could refute it, on
the same bench.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-claims" caption="Five claims from the other families, one bench: whole matches the design has never seen. Each claim comes back as its test." %}
</div>

## Three kinds of proof

| Question | What settles it | Study |
|---|---|---|
| Is the design better? | Both official metrics, on whole held-out matches, selected by the published rule | [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}) |
| Does it know when it is unsure? | Three confidences kept apart, and a record of where every value came from | [Confidence and provenance]({{ '/architecture/confidence-and-provenance/' | relative_url }}) |
| What has nobody proved yet? | Nine open questions, each with the experiment that would close it | [Open frontiers]({{ '/architecture/open-frontiers/' | relative_url }}) |

## How an architect chooses here

- **The unit is the match.** Neighbouring frames are near-copies. Splitting a match by frames leaks the answer.
- **Write the rule first.** Select by the published ranking rule, never by a blend invented after the scores.
- **Degrade the labelled data to the target.** A design validated with a ball that is always tracked has not met the problem.
- **Publish what reproduces.** If someone else cannot regenerate the number from public data, it is a claim.

## What this family cannot do

Proof cannot rescue a design. It can only tell the truth about one. The designs themselves start on
[the map]({{ '/architecture/map/' | relative_url }}).
