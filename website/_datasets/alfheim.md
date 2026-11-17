---
title: Alfheim Stadium
kicker: Tracking
summary: "Two professional matches filmed by a multi-camera panoramic rig while the home players wore position sensors. Video and an independent measurement of where the players really were."
group: tracking
order: 40
chips: [Panoramic video, Wearable sensors, Research only]
motif: sync
motif_caption: "Two clocks, one match: the camera array and the body sensors, aligned by timestamp."
motif_labels: [Camera array, Wearable sensors, Timestamped]
facts:
  - { k: Modality, v: "Multi-camera and panoramic video; wearable positions, speed and acceleration" }
  - { k: Scale, v: "2 Tromsø IL matches, about 100 GB" }
  - { k: Sensor rate, v: "About 20 Hz" }
  - { k: Coverage, v: "Home players only. No ball" }
  - { k: Possession labels, v: "None" }
  - { k: Calibration, v: "Ground-plane sensor coordinates" }
  - { k: Licence, v: "Non-commercial research. Re-identification and performance profiling prohibited" }
  - { k: Access, v: "Public academic dataset page" }
verdict:
  label: Our read
  text: "Two matches, and still nearly unique: positions that did not come from the video. That makes it a ruler for any video-to-pitch method."
sources:
  - { title: "Dataset page and terms of use", url: "https://datasets.simula.no/alfheim/" }
related:
  - /datasets/soccertrack-v2/
  - /datasets/soccernet-calibration/
---

## What it is

Recorded at Alfheim Stadium in Tromsø. A fixed camera array captures the pitch and is stitched into a panorama, while the home team's players wear sensors that log position, speed and acceleration at about 20 Hz. Video segments are named by timestamp, so the two streams can be aligned exactly.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing. One team is measured and the ball is not |
| Tracking | Sensor-grade positions for the home players |
| Events | Nothing |
| Calibration | A ground-truth target for video-to-pitch localisation |

## Where it wins

- **Independent ground truth.** Optical tracking is usually graded against other optical tracking. Here the reference is a different sensor.
- **True synchrony.** Shared timestamps, same match, same players. No alignment guesswork.
- **Full-pitch footage.** Panoramic coverage, the tactical view again.

## What it costs

- **Half the picture.** Only the home side wears sensors, and nothing measures the ball.
- **Two matches.** A validation set, not a training set.
- **Strict terms.** Research use only, with explicit bans on re-identifying players and on profiling club or player performance.

## How it plugs into possession

Possession rules are written in metres. "Within 1.5 m of the ball" only means something if the positions are right to well under that. Alfheim is one of the few places to check: project players from video to the pitch, compare with the sensors, and read off the localisation error in metres.

That error is the noise floor for every distance-based possession feature built on video-derived tracking.
