---
title: Gradient Sports World Cup 2022
kicker: Frame-level possession
summary: "Tracking, events and rosters for all 64 matches of the 2022 World Cup, with an owning team and a ball state in the tracking. The largest possession-labelled release."
group: possession
order: 20
chips: [Tracking, Possession labels, 64 matches, By request]
motif: stack
motif_caption: "One tournament in layers. The owner and ball-state fields are what make it a possession dataset."
motif_labels: ["Rosters, grades", Tracking, Events, Owner and state]
facts:
  - { k: Modality, v: "Broadcast-derived player and ball tracking, events, rosters, player grades" }
  - { k: Scale, v: "All 64 matches of FIFA World Cup Qatar 2022" }
  - { k: Format, v: "Per-match compressed JSON lines, plus event and metadata files" }
  - { k: Possession labels, v: "ball_owning_team_id and ball_state in the tracking schema" }
  - { k: Video, v: "Not distributed" }
  - { k: Calibration, v: "None released" }
  - { k: Licence, v: "Publisher terms supplied with the data" }
  - { k: Access, v: "Free, by request form" }
verdict:
  label: Our read
  text: "The scale answer to DFL's quality answer. Sixty-four matches of tournament football with machine-readable possession is the best pretraining pool available, provided you respect that the tracks were reconstructed from broadcast."
sources:
  - { title: "Publisher dataset announcement", url: "https://www.gradientsports.com/blog/enhanced-2022-world-cup-dataset" }
  - { title: "FIFA football data ecosystem, World Cup 2022", url: "https://quality.fifa.com/innovation/world-cup-2022/football-data-ecosystem" }
related:
  - /datasets/dfl-idsse/
  - /datasets/soccernet-gar/
  - /datasets/skillcorner-opendata/
---

## What it is

Gradient Sports, formerly PFF FC, released its full data stack for the 2022 World Cup: tracking for players and ball, event files, rosters with stable player IDs, match metadata and the company's player grades. Every one of the 64 matches is covered.

The tracking schema carries two fields a possession modeller looks for first: `ball_owning_team_id` and `ball_state`. Owner and alive-or-dead, per tracking frame.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | An owning team and a ball state alongside the tracking |
| Tracking | Players and ball across a whole tournament, with roster identities |
| Events | Event files per match for boundary checks |
| Calibration | Nothing |

## Where it wins

- **Volume.** Nine times the match count of the DFL release, in one consistent schema.
- **Variety.** Thirty-two national teams, group stage to final, with the full range of styles a tournament brings.
- **Identity.** Roster IDs let a model learn from who is on the ball, not only where.

## What it costs

- **Broadcast-derived tracks.** Players the camera cannot see are estimated. Definitions and interpolation differ from in-stadium league tracking such as DFL, so the two cannot be pooled without a provider flag.
- **Terms, not a licence.** Access is free but governed by the publisher's own conditions. That is a different thing from CC BY.
- **A known overlap.** SoccerNet-GAR is cut from the same 64 matches. Any study using both must split by match across the two, or it leaks.

## How it plugs into possession

Use it for breadth, and DFL for the verdict. A sequence model for home, away and dead ball needs to see many matches before its transition behaviour is trustworthy; this is the only release with possession on the tracking at that scale.

Map its owner and state fields into three states explicitly, per provider, and keep the mapping in the open. Then measure on a different provider. A possession model that only agrees with the labels it grew up on has learned a vendor, not the game.
