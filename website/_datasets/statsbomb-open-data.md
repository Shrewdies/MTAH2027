---
title: StatsBomb Open Data
kicker: Events
summary: "The richest free event data in football: every on-ball action with its team, outcome and possession sequence, plus 360 freeze frames of surrounding players on selected matches."
group: events
order: 10
chips: [Events, 360 freeze frames, Open JSON]
motif: field
motif_caption: "Events carry the possession. A 360 freeze frame adds everyone the camera could see around the ball."
motif_labels: [In possession, Out of possession]
facts:
  - { k: Modality, v: "Event data, lineups, match metadata, 360 freeze frames on selected matches" }
  - { k: Scale, v: "Many competitions and seasons" }
  - { k: Possession labels, v: "A possession sequence on every event. Not per frame" }
  - { k: Video, v: "None" }
  - { k: Calibration, v: "None" }
  - { k: Licence, v: "StatsBomb open-data terms, attribution required" }
  - { k: Access, v: "Public GitHub repository, JSON" }
verdict:
  label: Our read
  text: "The dictionary of possession. It defines the vocabulary, turnovers, restarts, pressure, carries, with a rigour no tracking dataset matches. It just speaks in events, not frames."
sources:
  - { title: "StatsBomb Open Data repository (now Hudl)", url: "https://github.com/hudl/open-data" }
  - { title: "Data documentation and 360 coverage", url: "https://github.com/hudl/open-data/blob/master/README.md" }
related:
  - /datasets/wyscout-2019-events/
  - /datasets/footpass/
  - /datasets/metrica-sample-data/
---

## What it is

StatsBomb, now part of Hudl, publishes a slice of its commercial event data for free. Each match is a list of on-ball events with location, player, team, outcome and a possession counter that groups events into sequences. For selected matches a 360 freeze frame is attached to events: the positions of the players visible on camera at that instant.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | An event-level possession sequence with the team that owns it |
| Tracking | Snapshots only: 360 freeze frames at event times |
| Events | A deep, consistent vocabulary of on-ball actions |
| Calibration | Nothing |

## Where it wins

- **Semantics.** Turnovers, restarts and set pieces are typed, not inferred. It shows what a careful definition of possession looks like.
- **Breadth.** Many competitions and seasons in one schema.
- **Context at the event.** Freeze frames show pressure and support around the ball without needing tracking.

## What it costs

- **Sparse in time.** Events are instants. Between two of them the data is silent, so a per-frame label cannot be read off.
- **No dead-ball clock.** A foul and the free kick that follows are both events. The stoppage between them has no explicit duration.
- **Partial 360 coverage.** Freeze frames exist for selected matches and show only the players in shot.

## How it plugs into possession

Use it to learn the grammar, then enforce the grammar on frames. Event data tells you how possession really behaves: how long sequences last, which actions end them, how often a duel changes ownership. Those statistics are priors for a sequence decoder. They set what a plausible spell length is and how expensive a change of state should be.

It also keeps a frame-level model honest about definitions. A deflection that comes straight back to the same team is still one possession under most event definitions. A model that splits it in two has not made a tracking error. It has made a definition error.
