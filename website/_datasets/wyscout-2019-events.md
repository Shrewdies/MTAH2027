---
title: Wyscout academic event dataset
kicker: Events
summary: "About 1,941 matches and 3.25 million on-ball events from a season of Europe's five big leagues plus two international tournaments, under CC BY 4.0."
group: events
order: 20
chips: [Events, 1941 matches, CC BY 4.0]
motif: spikes
motif_caption: "3.25 million tagged events. Each one is an instant; the possession lives in the gaps."
motif_labels: [Pass, Duel, Free kick]
facts:
  - { k: Modality, v: "Tagged on-ball events with coordinates and timestamps; match, team and player metadata" }
  - { k: Scale, v: "About 1,941 matches, 3.25 million events" }
  - { k: Competitions, v: "Five top European leagues 2017/18, Euro 2016, World Cup 2018" }
  - { k: Possession labels, v: "Acting team per event. No spells" }
  - { k: Video, v: "None" }
  - { k: Calibration, v: "None" }
  - { k: Licence, v: "CC BY 4.0" }
  - { k: Access, v: "Open download from Figshare" }
verdict:
  label: Our read
  text: "Scale and a clean licence. When a model needs to know what football usually does next, this is where the base rates come from."
sources:
  - { title: "Pappalardo et al., Scientific Data (2019)", url: "https://www.nature.com/articles/s41597-019-0247-7" }
  - { title: "Dataset on Figshare", url: "https://figshare.com/collections/Soccer_match_event_dataset/4415000" }
  - { title: "Community parser and mirror", url: "https://github.com/koenvo/wyscout-soccer-match-event-dataset" }
related:
  - /datasets/statsbomb-open-data/
  - /datasets/soccernet-action-spotting/
---

## What it is

Released by Pappalardo and colleagues with a Scientific Data paper. Wyscout's analysts tag every on-ball event from video; this is the public slice: a complete season for five leagues and two international tournaments, as JSON, with coordinates, timestamps and descriptive tags.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | The team behind each event |
| Tracking | Nothing |
| Events | Passes, duels, shots, fouls, free kicks and interruptions at scale |
| Calibration | Nothing |

## Where it wins

- **Size.** Thousands of matches means transition statistics that are stable, per league and per game state.
- **Open licence.** CC BY 4.0. Derived statistics can be published and shipped.
- **Restarts are explicit.** Free kicks, corners, throw-ins and interruptions are event types. That is a direct view of how play stops and starts.

## What it costs

- **No positions between events.** No tracking, no video.
- **Human timestamps.** Event times are tagged by people watching video. They are approximate, not frame-accurate.
- **Acting team is not ownership.** A duel has two actors. Who came away with the ball is in the next event.

## How it plugs into possession

Base rates. How many possessions does a match contain? How long does a spell last? How often does a throw-in go back to the team that took it? A decoder with a cost for changing state is making a statement about those numbers, and this corpus is where they can be measured across thousands of matches instead of assumed.

It is also a check on any spell-level metric. If a model's output for a match contains twice as many possessions as elite football produces, the model is fragmenting. No frame-level label is needed to see that.
