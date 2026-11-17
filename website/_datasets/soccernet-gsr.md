---
title: SoccerNet Game State Reconstruction
kicker: Broadcast video and game state
summary: "Broadcast clips where every player and referee is placed on the pitch with a role, a team and a jersey number. The benchmark for turning television pictures into tracking data."
group: broadcast
order: 10
chips: [Broadcast video, Pitch localisation, Team and jersey]
motif: pipeline
motif_caption: "Game state is a chain. Each link has to hold before a position on the pitch means anything."
motif_labels: [Detect, Track, Calibrate, Team, Jersey, Pitch]
facts:
  - { k: Modality, v: "Broadcast clips with detections, pitch coordinates, roles, team and jersey labels" }
  - { k: Task, v: "Video in, minimap out: who is where, and who they are" }
  - { k: Possession labels, v: "None" }
  - { k: Calibration, v: "Image-to-pitch localisation is part of the target" }
  - { k: Licence, v: "SoccerNet research terms. Video under NDA" }
  - { k: Access, v: "Annotations on Hugging Face (SN-GSR-2025)" }
verdict:
  label: Our read
  text: "The dataset that defines the upstream problem. Everything a possession model consumes, positions, teams, identities, is what this benchmark asks a vision system to produce."
sources:
  - { title: "Task description", url: "https://www.soccer-net.org/tasks/game-state-reconstruction" }
  - { title: "Baseline repository (sn-gamestate)", url: "https://github.com/SoccerNet/sn-gamestate" }
  - { title: "SN-GSR-2025 dataset", url: "https://huggingface.co/datasets/SoccerNet/SN-GSR-2025" }
  - { title: "SoccerNet data access rules", url: "https://www.soccer-net.org/data" }
related:
  - /datasets/soccernet-tracking/
  - /datasets/soccernet-calibration/
  - /solutions/vision-and-calibration/sn-gamestate/
  - /architecture/video-only/
---

## What it is

Game State Reconstruction asks for the full chain in one task: detect the people on screen, track them, calibrate the camera, place each person on the pitch, then say which team they play for, what their role is and what number they wear. The dataset supplies broadcast clips annotated with exactly that.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct. No continuous ball ownership |
| Tracking | Pitch-plane positions with team, role and jersey number |
| Events | Nothing |
| Calibration | Learned jointly: localisation only scores if the camera model is right |

## Where it wins

- **End to end.** One metric punishes a failure anywhere in the chain. Good detection with bad calibration scores badly, as it should.
- **Team assignment in the wild.** Kits, lighting and broadcast compression as they really are.
- **Identity that means something.** A jersey number is an identity that survives a camera cut. A track ID is not.

## What it costs

- **Part of the pitch.** The main camera shows the play, not the back line. Off-screen players do not exist in the labels.
- **Clips, not matches.** Continuity across a half is not tested.
- **Thin on the ball.** The task is about people. Ball ownership is not annotated.

## How it plugs into possession

Team possession needs three things from upstream: player positions in metres, a team for each player, and the ball. Game state reconstruction delivers the first two, and its error modes become possession errors directly. A defender assigned to the wrong team is a false turnover. A calibration that drifts by two metres moves the nearest player to someone else.

Read the benchmark as a specification of the input quality a possession decoder should expect from broadcast, and design the decoder to survive it.

The baseline pipeline built for this task, and the metric that scores it, are covered under [Game State Reconstruction baseline]({{ '/solutions/vision-and-calibration/sn-gamestate/' | relative_url }}).
