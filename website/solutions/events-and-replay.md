---
layout: wiki-hub
title: "Events and replay"
permalink: /solutions/events-and-replay/
collection_index: solutions
only_group: events-and-replay
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Spotters that timestamp passes, drives and tackles, and the tools that untangle a broadcast edit."
motif: spikes
motif_caption: "A spotter's output: instants on a timeline, and nothing in between."
motif_labels: ["Pass", "Drive", "Tackle"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "1 s", label: "the usual scoring tolerance" }
  - { value: "25", label: "frames inside that tolerance" }
---
## One picture: anchors with error bars

{% include wiki/motif.html id="sol-anchors" labels="±1 s, 25 frames|Spotted events|Possession between" caption="A spotter says what happened and roughly when. Possession changes somewhere inside each band, and the spotter does not say where." %}

An event spotter watches video and emits instants: a pass here, a tackle there. Every change of possession is an event, so spotters are natural possession evidence. Two properties decide how they can be used. They are scored at a tolerance of one second, which is 25 frames at 25 fps. And they are silent between events.

The other half of the family handles the broadcast itself. A broadcast is an edit, with cuts and replays, and a frame inside a replay is not match time.

In the chain, spotting sits beside measuring. Both produce evidence: measuring is dense and geometric, spotting is sparse and semantic.

## How to choose inside it

| Entry | Labels | What it needs | Compute |
|---|---|---|---|
| [T-DEED, team-aware]({{ '/solutions/events-and-replay/team-tdeed/' | relative_url }}) | Checkpoint available | Broadcast video | GPU |
| [2023 winning solution]({{ '/solutions/events-and-replay/ball-action-winner/' | relative_url }}) | Trained models available | Broadcast video. No team in the output | GPU |
| [E2E-Spot]({{ '/solutions/events-and-replay/e2e-spot/' | relative_url }}) | Football labels to train | Video | Light GPU |
| [FOOTPASS baselines]({{ '/solutions/events-and-replay/footpass/' | relative_url }}) | Labels to train | Video plus identified player tracks | Heavy |
| [SoccerNet spotting kits]({{ '/solutions/events-and-replay/sn-spotting/' | relative_url }}) | Not a model | Timestamped predictions to score | Evaluation only |
| [PySceneDetect]({{ '/solutions/events-and-replay/pyscenedetect/' | relative_url }}) | None | Any video | CPU |
| [Replay grounding]({{ '/solutions/events-and-replay/sn-replay-grounding/' | relative_url }}) | Labels to train | Replay segments found upstream | GPU |

For possession, team attribution is the property to pay for. An event with a team is direct evidence. An event without one needs a second source to say whose it was.

{% include wiki/motif.html id="sol-edit" caption="One tackle in match time, three sightings in the programme. Shot detection finds the cuts, and replay grounding ties each replay to the moment it repeats." %}

## What this family cannot do

- **It cannot place a boundary to the frame.** One second of tolerance is 25 frames of doubt.
- **It cannot label the time between events.** That is most of the match.
- **It cannot be read off a broadcast without hygiene.** Cuts and replays must be handled first, or the same tackle is counted three times.

## Where our decoder stands

Its tag evidence is used the way this family should be used. The automatic tags are anchors with error bars: restart windows, not instants, and calibrated team signals from every tag code. The decode fills the frames in between and decides where inside each window the boundary falls.
