---
layout: wiki-hub
title: Tracking and full-pitch video
permalink: /datasets/tracking/
collection_index: datasets
only_group: tracking
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "Positions without possession. These four teach what a tactical camera sees and how far a position can be trusted, which is the noise floor under every possession feature."
motif: tracks
motif_caption: "Twenty-two tracks and a ball. Nothing here says who has it, and everything about possession is computed from it."
motif_labels: [Player track, Trail]
stats:
  - { value: "{count}", label: datasets }
  - { value: "15.5 h", label: full-pitch video under CC BY }
  - { value: "2", label: matches with sensor-measured positions }
---

## What this family is

Players on a pitch, frame after frame, with no word on who has the ball. For possession the value is indirect and large. Every possession feature is a distance between positions: who is nearest the ball, who is within playing distance. The quality of the positions is the ceiling on the quality of the answer.

The family covers both ends of how tracking is made: the full-pitch video going in, and the pitch coordinates coming out.

## What is actually measured

| Dataset | Measured | Ball | Licence |
|---|---|---|---|
| [Metrica sample data]({{ '/datasets/metrica-sample-data/' | relative_url }}) | Both teams in pitch coordinates, with events | Yes | None stated |
| [SoccerTrack v2]({{ '/datasets/soccertrack-v2/' | relative_url }}) | Players on the pitch plane from panoramic video, with identity | Derived from ball actions | CC BY 4.0 |
| [TeamTrack]({{ '/datasets/teamtrack/' | relative_url }}) | Player boxes and track IDs in 4K to 8K video | No | MIT code, data terms apart |
| [Alfheim]({{ '/datasets/alfheim/' | relative_url }}) | Home players by wearable sensor, plus panoramic video | No | Non-commercial research |

{% include wiki/motif.html id="ds-measured" caption="The four are not versions of the same thing. Only the Metrica sample measures both teams and a ball directly, and Alfheim alone measures positions with a sensor instead of a camera." %}

## How to choose

| You need | Use |
|---|---|
| To learn Metrica's file and coordinate conventions | Metrica sample data |
| To train or test a tracker in the tactical view | SoccerTrack v2 |
| To stress identity through crowded play | TeamTrack |
| To measure localisation error in metres | Alfheim |

## The traps

- **Camera type.** This is full-pitch footage. Players are small in frame, and a detector trained on broadcast close-ups does not transfer.
- **Where the ball comes from.** In SoccerTrack v2 the ball may be interpolated between annotated actions. It is a label derived from events, not a measurement.
- **Identity is not team.** A track ID is not a player. When a tracker swaps two opponents, the team of the "nearest player" flips with it.
- **Coordinates.** Metrica's positions are normalised to the unit square. No distance means anything until a pitch size is chosen.
- **Licences.** Alfheim forbids re-identification and performance profiling. TeamTrack's code licence does not cover its data.

{% include wiki/motif.html id="ds-swap" caption="Two opponents cross and leave with each other's numbers. The nearest-player team flips for a few frames and no football has happened. A cost for changing state absorbs it." %}

## What it cannot do

Name the ball's owner. None of the four carries a possession label, and two have no ball at all. Metrica's events give a sparse skeleton of who played the ball, which is enough to sanity-check a decoder and too thin to grade one.

## Where it meets our decoder

The competition tracking is this family's hard case: automatic, team-only, with no player identities. Our decoder reads control as a player within 1.5 m of the ball and closer than any opponent, then makes every change of state pay a cost, so one noisy frame, or one swapped track, cannot flip possession.

Position noise was part of our validation for the same reason: the DFL match we judged on was degraded with 0.15 m of noise before scoring. See [Players without names]({{ '/architecture/player-identities/' | relative_url }}) for the identity problem in full.
