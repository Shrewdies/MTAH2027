---
layout: wiki-hub
title: The hard parts
permalink: /architecture/hard-parts/
collection_index: architecture
only_group: hard-parts
family: true
parent: /architecture/
nav_exclude: true
kicker: "Family 04 of 05"
summary: "Six problems decide whether a design survives a real match. None of them is about the model. All of them are about what a value in the data is allowed to mean."
motif: bp-decision
motif_labels: [hard-parts]
motif_caption: "The decision map of this family. Each question leads to the study that answers it."
stats:
  - { value: "{count}", label: studies in this family }
  - { value: "2", label: about joining a second camera }
  - { value: "4", label: about reading one tracking feed }
---

## One passage of play, six strikes

The truth of this passage is simple: home, a stoppage, home. Each hard part damages a naive reading in
its own way, and each is answered by one rule.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-passage" caption="Six strikes in turn: clock drift, a change of view, a slot swap, a lost ball, a stoppage, a tag. The naive reading ends with nine possessions. The robust one ends with two, which is the truth." %}
</div>

| Strike | The trap | Study |
|---|---|---|
| 1 | One offset for a whole broadcast | [One clock for the match]({{ '/architecture/match-timeline/' | relative_url }}) |
| 2 | Trusting geometry without timing | [Space is not time]({{ '/architecture/multi-camera-geography/' | relative_url }}) |
| 3 | Reading a slot change as an event | [Players without names]({{ '/architecture/player-identities/' | relative_url }}) |
| 4 | Missing ball means dead ball | [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}) |
| 5 | One mechanism for both questions | [Alive or dead, then who]({{ '/architecture/live-dead/' | relative_url }}) |
| 6 | A touch is a turnover | [Events are not possession]({{ '/architecture/events-and-control/' | relative_url }}) |

## Where each one bites

The six do not enter at the same place. Knowing the stage tells you where the fix belongs, and which of
them a design can ignore.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-stages" caption="Clocks and cameras exist only when a second camera is joined. The other four are present in a single tracking feed. Whatever the stage, the damage arrives at the last one as a split or a merged possession." %}
</div>

## How an architect chooses here

- **Fix the representation before the model.** Every trap above is a wrong meaning given to a value.
- **Say what silence means.** Missing, unobserved and unknown are three states. Collapsing them is a design
  decision, usually a bad one.
- **Test with the failure, not around it.** Hide the ball, shuffle the slots, shift the clock, then score.

## What this family cannot do

It cannot tell you that the answers work. That takes whole matches the design has never seen, and it is
the business of [proof]({{ '/architecture/proof/' | relative_url }}).
