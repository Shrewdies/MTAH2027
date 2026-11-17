---
layout: wiki-entry
nav_exclude: true
title: "Tactical tracking: the master clock"
kicker: The data
summary: "One wide camera, the whole pitch, every frame. The tactical tracking is the geometry the answer is graded against, and its quirks decide how a model must be built."
route_label: Tracking
hook: "Slots are not players"
group: data
order: 60
chips: [25 Hz, 46 slots, Team-only players]
motif: tracks
motif_caption: Slots, not players. When a track is lost and re-acquired the same footballer continues under a new slot number.
motif_labels: [Track slot, Trail]
facts:
  - { k: Video, v: "1920×1080, 25 fps, 199,319 frames" }
  - { k: Track slots, v: "46 for about 22 players" }
  - { k: Tracked objects, v: "20.5 on average, graded frames" }
  - { k: Ball tracked, v: "59.3% of graded frames" }
verdict:
  label: Our read
  text: "Treat the tracking as team-level geometry on a reliable clock. Anything that depends on a slot being the same player across a match will break; anything built on team distances and ball state will not."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
related:
  - /challenges/tracking-errors/
  - /challenges/data-asset-map/
  - /challenges/homography/
---
## What is in the file

One row per video frame. Each row holds the ball position and, for every track slot, a position and a speed. Coordinates are normalised to the unit square; speeds are in metres per second.

| Property | Value |
|---|---|
| Rows | 199,319, one per frame |
| Track slots | 46, for about 22 players |
| Objects tracked per graded frame | 20.5 on average |
| Ball tracked | 56.9% of all frames, 59.3% of graded frames |
| Homography | Every frame, all marked usable |

## Three details that bite

**Off by one.** Tracking frame ids start at 1; video frames and submission rows start at 0. The difference is an indexing convention, not a synchronisation offset: `video frame = frame id − 1`.

**Two pitch sizes.** The metadata lists 105 × 68 m; the organisers' helper code carries 105.3 × 68.0 m. Pick one, convert to metres once, and do all spatial reasoning there. A control radius means nothing in normalised units: the pitch is not square.

**Slots are not players.** There are twice as many slots as footballers because a lost track comes back under a new number. Slots carry a team, never an identity. Occasionally one player appears twice.

## Where it is strong

- **The whole pitch, always.** Team shape, depth and width are visible on every frame, including off the ball.
- **One consistent clock.** Every frame index means the same thing in the video, the tracking, the homography and the submission.
- **Speeds are given.** Collective stillness, the clearest sign of a stoppage, is a direct read.

## Where it is weak

- **The ball.** It is small, fast and often hidden. It is untracked on 41% of graded frames, concentrated in crowds, duels and aerial play.
- **Occlusion and duplication.** Players merge in tight spaces and split again.
- **Identity.** Any feature tied to a slot number changes meaning mid-match.

## How it plugs into possession

Three reads carry most of the evidence. **Control**: a player close to a slow ball, and closer than any opponent. **Out of play**: the ball beyond a line. **Stoppage**: both teams nearly still, or the ball placed and motionless. All three are team-level and slot-free, so a re-numbered track changes nothing. The thresholds behind them are in [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).

The fourth read is an absence. When the ball is untracked, the tracking says nothing about possession, and a model has to decide what silence means. That decision is the subject of [the ball goes missing]({{ '/challenges/tracking-errors/' | relative_url }}).
