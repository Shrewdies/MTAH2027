---
layout: wiki-hub
title: Events
permalink: /datasets/events/
collection_index: datasets
only_group: events
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "Instants, not intervals. Event data cannot label a frame, but it knows the grammar of possession: what ends a spell, how play restarts, how long football keeps the ball."
motif: ds-skeleton
icon: spikes
motif_caption: "Events fix moments. Same-team runs join into a spell; the hand-over and the stoppage between them stay open."
motif_labels: [On-ball events, Possession skeleton, Known spell, Open boundary]
stats:
  - { value: "{count}", label: datasets }
  - { value: "3.25M", label: events under CC BY 4.0 }
  - { value: "500+", label: full matches of stoppages and restarts }
---

## What this family is

Records of what happened, each with a timestamp: a pass, a duel, a foul, a throw-in. Two of these datasets are provider event feeds built for analysis. Two are labels on broadcast video built to train detectors. None has positions between events, and none has frames.

So no dataset here can say who has the ball at a given instant. What the family knows instead is how possession behaves, and that is worth a great deal to anything that decodes a sequence.

{% include wiki/motif.html id="ds-grain" caption="One minute at four grains. Frames are continuous. Every event dataset is a row of instants, and action spotting marks little beyond the stoppages and restarts." %}

## Four datasets, two kinds

| Dataset | Kind | Grain | Licence |
|---|---|---|---|
| [StatsBomb Open Data]({{ '/datasets/statsbomb-open-data/' | relative_url }}) | Provider event feed | Every on-ball action, a possession sequence, 360 freeze frames on selected matches | Open-data terms |
| [Wyscout academic]({{ '/datasets/wyscout-2019-events/' | relative_url }}) | Provider event feed | 3.25 million events, about 1,941 matches | CC BY 4.0 |
| [Ball Action Spotting]({{ '/datasets/soccernet-ball-actions/' | relative_url }}) | Video labels | 12 classes of ball action | Research terms |
| [Action Spotting]({{ '/datasets/soccernet-action-spotting/' | relative_url }}) | Video labels | 17 classes over 500+ full matches | Research terms |

## How to choose

| You need | Use |
|---|---|
| A careful definition of possession | StatsBomb Open Data |
| Base rates you can publish | Wyscout academic |
| To train a touch detector from video | Ball Action Spotting |
| The edges of the dead ball | Action Spotting |

## What events can and cannot teach

| They teach | They cannot |
|---|---|
| Which actions end a spell | When, to the frame, it ended |
| How long spells last and how many a match holds | Who has the ball between two events |
| What stops play and what restarts it | How long the stoppage lasted |

## The traps

- **The acting team is not the owner.** A duel has two actors. Who came away with the ball is in the next event.
- **Unlabelled time is not dead ball.** Filling the gaps between events with any label manufactures errors.
- **Timestamps are human.** Tagged from video, approximate, not frame-accurate.
- **Definitions differ.** One provider's possession sequence is not another's. A deflection straight back to the same team is one possession under most event definitions and two under a naive frame rule.
- **Rights.** The SoccerNet footage is NDA-gated and non-commercial. Only the Wyscout release is CC BY 4.0.

## Where it meets our decoder

A decoder with a cost for changing state is making a claim about base rates: how many possessions a match holds and how long they last. Event data is where that claim can be checked without a single frame label. On the degraded DFL match we judged on, the labels hold 402 possessions. The organisers' baseline method reports 570. That gap is fragmentation, visible in one number.

{% include wiki/motif.html id="ds-fragments" caption="Fragmentation seen without a single frame label: 402 possessions in the labels, 570 from the organisers' baseline method. The strips are illustrative. The counts are measured." %}

Restarts are the other meeting point. Our decoder takes restart windows from the automatic tactical tags as evidence: a dead ball before, a known team after. It is the same cue Action Spotting teaches a video model to produce. The distinction between touching the ball and holding it is drawn in [Events are not possession]({{ '/architecture/events-and-control/' | relative_url }}).
