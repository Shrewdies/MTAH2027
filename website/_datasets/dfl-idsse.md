---
title: DFL IDSSE open data
kicker: Frame-level possession
summary: "Seven Bundesliga and 2. Bundesliga matches with official 25 Hz tracking and a possession and ball-status flag on every frame. The open judge for any possession model."
group: possession
order: 10
chips: [Tracking, Possession labels, CC BY 4.0]
motif: ribbon
motif_caption: "A possession flag on every frame is what turns tracking into a judge."
motif_labels: [Degraded evidence, DFL labels, Home, Away, Dead ball]
facts:
  - { k: Modality, v: "25 Hz player and ball tracking, ball height, event XML" }
  - { k: Scale, v: "7 matches, 1,002,644 frames, 11,137 events" }
  - { k: Competition, v: "Bundesliga and 2. Bundesliga, 2022-23" }
  - { k: Possession labels, v: "BallPossession and BallStatus on every frame" }
  - { k: Video, v: "None. Footage rights are excluded from the release" }
  - { k: Calibration, v: "None released" }
  - { k: Licence, v: "CC BY 4.0 for tracking and events" }
  - { k: Access, v: "Open download from Figshare" }
verdict:
  label: Our read
  text: "The reference set. Small, official, and the only place where home, away and dead ball are labelled on every frame and free to use. Treat it as a judge first and a teacher second."
sources:
  - { title: "Bassek et al., Scientific Data (2025)", url: "https://www.nature.com/articles/s41597-025-04505-y" }
  - { title: "Official data on Figshare", url: "https://springernature.figshare.com/articles/dataset/An_integrated_dataset_of_spatiotemporal_and_event_data_in_elite_soccer/28196177" }
related:
  - /datasets/gradient-world-cup-2022/
  - /datasets/skillcorner-opendata/
  - /datasets/reference-target-mtah-2027/
  - /challenges/pareto-lens/
  - /architecture/evaluation-framework/
  - /challenges/initial-challenge/
---

## What it is

The German Football League's integrated release of positional and event data, published with a Scientific Data paper. Every match carries the positions of all players and the ball at 25 Hz, the ball's height, team membership and an event file synchronised to the tracking.

Two per-frame fields make it special. `BallPossession` names the team. `BallStatus` says whether the ball is in play. Together they give the three states a possession model has to produce: home, away, dead ball.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Team and ball status on every frame, at the frame rate of broadcast video |
| Tracking | A complete ball track with height: what clean evidence looks like |
| Events | Synchronised events to audit where spells start and end |
| Calibration | Nothing. This is pitch-space data only |

## Where it wins

- **Direct labels.** No reconstruction from events, no guessing at stoppages. The label is in the file.
- **Official provenance.** League data, documented in a peer-reviewed data descriptor.
- **A licence you can build on.** CC BY 4.0 means anyone can download the same matches and reproduce a score.
- **A clean ball you can damage on purpose.** Because the ball track is complete, you can hide it in bursts and add noise while keeping the labels. That turns a tidy dataset into a faithful rehearsal for automatic tracking.

## What it costs

- **Seven matches.** Five are home games of one 2. Bundesliga club. Enough to judge a method, thin for teaching a deep model team styles.
- **Provider semantics.** Possession here is the league's definition. Mapping it to another provider's home, away and dead ball is a modelling decision, not a rename.
- **No video, no tags.** There is no footage and no tactical tagging, so it tests the tracking half of a pipeline and nothing else.

## How it plugs into possession

This is where our decoder was chosen. The parameter profiles came out of a Pareto search over spellF1 and macroF1 on simulated matches with known answers. The profile we submitted is the one that held up on DFL labels, scored with the organisers' official, unchanged metric. Nothing was trained here: the decoder has no trained weights. How the search ran is on [the Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}), and why another league's labels were the right judge is in [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}).

We scored it twice. Once as delivered, and once degraded to the competition's conditions: the ball hidden in bursts on 41% of frames, with 0.15 m of position noise.

| Condition | Method | spellF1 | macroF1 |
|---|---|---|---|
| As delivered | Organisers' baseline method | 0.301 | 0.385 |
| As delivered | Our decoder, submitted profile | 0.482 | 0.856 |
| Degraded | Organisers' baseline method | 0.235 | 0.383 |
| Degraded | Our decoder, submitted profile | 0.340 | 0.693 |

The degraded row is the one that matters. A method that only works on a visible ball has learned the easy half of the problem.
