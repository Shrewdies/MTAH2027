---
layout: wiki-hub
title: The map
permalink: /architecture/map/
collection_index: architecture
only_group: map
family: true
parent: /architecture/
nav_exclude: true
kicker: "Family 02 of 05"
summary: "Where does the evidence come from? Coordinates alone, pixels alone, or every witness reconciled into one match state. It is the first decision in any possession system, and every later decision inherits it."
motif: bp-decision
motif_labels: [map]
motif_caption: "The decision map of this family. Each question leads to the study that answers it."
stats:
  - { value: "{count}", label: studies in this family }
  - { value: "3", label: sources of evidence }
  - { value: "2", label: engines any of them can feed }
---

## One instant, three witnesses

The choice in this family starts from what each kind of witness can and cannot see at one moment of one
match. Everything else follows from those blind spots.

<div class="wiki-figures">
{% include wiki/motif.html id="bp-fam-witness" caption="The same instant three times. Tactical tracking has everyone and no ball. Broadcast tracking has the ball inside a window. The video frame has contact and a shirt number, and no metres. Below: where each study of this family sits between one witness and one reconciled state." %}
</div>

## Every route on one page

A possession system is a path through two decisions: where the evidence comes from, and how evidence on
single frames becomes one sequence. Any source can feed any engine, so there are more routes than boxes.
Laying them all out first is what keeps a team from building the fashionable one.

{% include wiki/motif.html id="bp-approach" labels="Tracking|Video|All reconciled|One model|Evidence + decoder|H / A / D" caption="Three sources, two engines, one sequence. The lit route is the one we fielded: tracking into evidence and a decoder." %}

## The sources, side by side

| Criterion | Tracking only | Video only | All reconciled |
|---|---|---|---|
| Spatially normalised on arrival | Yes | No, needs calibration | After calibration |
| Survives an invisible ball | With ball-free reasoning | Poorly | Yes, where another witness sees it |
| Survives unstable identities | With order-free features | Re-identification is hard | Shirt numbers from pixels |
| Needs synchronisation | No | If two cameras are used | Yes, per segment |
| Explainability | High for physical rules | Variable | Depends on provenance |
| Complexity | Lowest | High | Highest |

## How an architect chooses here

- **Start from what the sensor delivers.** If tracking exists, coordinates are evidence you can audit today.
- **Count what you would have to own.** Detection, calibration and synchronisation are products in themselves.
- **Add a witness for its different failures.** Two sources that fail together are one source.

## What this family cannot do

A source gives evidence about single instants. It does not give a sequence. Turning 25 opinions a second
into one story of the half is the job of [the engine]({{ '/architecture/engine/' | relative_url }}).
