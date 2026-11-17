---
layout: wiki-hub
title: Broadcast video and game state
permalink: /datasets/broadcast/
collection_index: datasets
only_group: broadcast
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "Television pictures turned into players, teams and touches. This is the upstream problem: what a possession model consumes is what these benchmarks ask vision to produce."
motif: pipeline
motif_caption: "From pixels to possession evidence in five links. Each dataset here trains or grades some of them."
motif_labels: [Detect, Track, Calibrate, Team, Touch]
stats:
  - { value: "{count}", label: datasets }
  - { value: "102,992", label: ball actions tied to a player }
  - { value: "87,939", label: moments in both video and tracking }
---

## What this family is

Broadcast footage, annotated to the level a possession model could feed on: boxes, track IDs, positions on the pitch, team and jersey, and the touches themselves. If there is no tracking feed, this is how one gets made.

It is also the family with the hardest camera. A broadcast director follows the ball, cuts to close-ups and runs replays. A tactical camera does none of that.

{% include wiki/motif.html id="ds-views" labels="Full-pitch view|Broadcast view|Everyone, all match|Cuts and replays" caption="Same players, two cameras. The broadcast view sees part of the pitch and leaves the live clock whenever the director cuts away." %}

## What each one annotates

| Dataset | Unit | Annotates | Access |
|---|---|---|---|
| [Game State Reconstruction]({{ '/datasets/soccernet-gsr/' | relative_url }}) | Clips | Pitch position, role, team, jersey number | Labels open, video NDA |
| [SoccerNet Tracking]({{ '/datasets/soccernet-tracking/' | relative_url }}) | Clips | Boxes and track IDs, ball included | Labels open, video NDA |
| [SoccerNet-GAR]({{ '/datasets/soccernet-gar/' | relative_url }}) | 87,939 event windows | Ten activity classes, video and tracking in sync | NDA |
| [FOOTPASS]({{ '/datasets/footpass/' | relative_url }}) | 54 full matches | 102,992 ball actions, each with its player | CC BY-NC 4.0, video NDA |

{% include wiki/motif.html id="ds-span" caption="Each bar is what a dataset annotates on the way from pixels to touches. Game State Reconstruction covers the chain up to identity, FOOTPASS adds the action, and no row reaches a possession spell." %}

## How to choose

| You need | Use |
|---|---|
| The full chain from pixels to pitch positions | Game State Reconstruction |
| An honest grade for a ball detector | SoccerNet Tracking |
| To ask whether video adds anything to tracking | SoccerNet-GAR |
| Who touched the ball, and when | FOOTPASS |

## From touches to possession

Two of the four carry real possession signal. SoccerNet Tracking is where you measure how the ball is lost: how often, for how long, and in which scenes. FOOTPASS shows who played it. A run of actions by one team is a spell. A change of acting team is a turnover somewhere between two timestamps.

## The traps

- **Part of the pitch.** Off-screen players do not exist in the labels. A back line can be missing for a whole attack.
- **Clips break identity.** Track IDs hold inside a clip and mean nothing across clips. Only a jersey number survives a cut.
- **Rights.** SoccerNet video sits behind an NDA. FOOTPASS annotations are non-commercial. Nothing trained here ships freely.
- **Leakage.** SoccerNet-GAR shares its 64 matches with the Gradient Sports release.

## What it cannot do

Give a spell. Touches are instants and boxes are positions. Nothing in the family marks how long a team held the ball, or when it went dead and came back.

## Where it meets our decoder

Our Initial Challenge decoder begins where this family ends: it decodes the automatic tracking the organisers supplied.

Two lessons from this family are in the design all the same. Ball dropouts come in bursts, so our validation hid the ball in bursts. And a touch is stronger evidence than proximity: in the decoder a reception can change possession, and one frame of a nearer opponent cannot. The upstream chain itself is mapped in [Video-only inference]({{ '/architecture/video-only/' | relative_url }}).
