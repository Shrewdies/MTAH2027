---
layout: wiki-hub
title: "Vision and calibration"
permalink: /solutions/vision-and-calibration/
collection_index: solutions
only_group: vision-and-calibration
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Detectors, trackers and calibrators that rebuild players, ball and camera from video."
motif: boxes
motif_caption: "Where it starts: boxes on the players, and a much smaller one on the ball."
motif_labels: ["Player", "Ball"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "3", label: "calibrators" }
  - { value: "5", label: "licence families in play" }
---
## One picture: three stages, one error budget

{% include wiki/motif.html id="sol-vision-chain" labels="Detect|Track|Calibrate|Missed ball|Identity switch|Metres off" caption="Boxes in the image become tracks over time, and tracks become positions on the pitch. Each stage hands its mistakes to the next." %}

Video becomes tracking in three moves. **Detect** finds players and ball in each frame. **Track** links detections over time and tries to keep identities. **Calibrate** estimates the camera, so that image positions become pitch positions. Every entry in this family does one of the three, or all of them at once.

Seeing is needed when there is no tracking feed, or when the feed has holes that video could fill.

## How to choose inside it

| Entry | Labels | What it needs in view | Compute |
|---|---|---|---|
| [Roboflow soccer detectors]({{ '/solutions/vision-and-calibration/roboflow-soccer/' | relative_url }}) | Pretrained | Players and a visible ball | GPU, every frame |
| [Tracking by detection]({{ '/solutions/vision-and-calibration/tracking-by-detection/' | relative_url }}) | Pedestrian weights | Detections from a football detector | Light on top of a detector |
| [SportsLabKit]({{ '/solutions/vision-and-calibration/sportslabkit/' | relative_url }}) | Set by the detector | A full-pitch view suits it best | Set by the detector |
| [SAM 2]({{ '/solutions/vision-and-calibration/sam2/' | relative_url }}) | None, but a prompt per object | The prompted object | GPU, per object |
| [CoTracker]({{ '/solutions/vision-and-calibration/cotracker/' | relative_url }}) | None, but query points | The queried points | GPU |
| [SoccerNet re-identification]({{ '/solutions/vision-and-calibration/soccernet-reid/' | relative_url }}) | Football identity labels | Player crops with enough pixels | GPU |
| [PnLCalib]({{ '/solutions/vision-and-calibration/pnlcalib/' | relative_url }}) | Pretrained | Pitch lines and keypoints | GPU, per frame |
| [TVCalib]({{ '/solutions/vision-and-calibration/tvcalib/' | relative_url }}) | Pretrained segmenter | Pitch markings | Iterative, per frame |
| [KpSFR]({{ '/solutions/vision-and-calibration/kpsfr/' | relative_url }}) | Pretrained | Pitch in view | GPU |
| [Game State Reconstruction baseline]({{ '/solutions/vision-and-calibration/sn-gamestate/' | relative_url }}) | Pretrained baseline | All of the above | Heavy GPU |

Choose by camera first. A fixed tactical camera wants motion-only tracking and one calibration for the match. A broadcast camera wants camera-motion compensation, calibration on every frame and the shot handling of the [events and replay]({{ '/solutions/events-and-replay/' | relative_url }}) family. The calibrators are graded on the [SoccerNet Camera Calibration]({{ '/datasets/soccernet-calibration/' | relative_url }}) benchmark.

{% include wiki/motif.html id="sol-camera-choice" caption="A fixed tactical camera holds the whole pitch: one calibration, no cuts, and a very small ball. A broadcast camera pans across part of it and needs a new calibration on every frame." %}

## What this family cannot do

- **It cannot make the ball easy.** A football is a few fast, blurred pixels, and it is lost most often when possession is contested.
- **It cannot tell team-mates apart reliably.** Identical kits defeat appearance, and identity is what player-level possession needs.
- **It cannot give height from one camera.** A ball in the air projects to the wrong place on the ground.
- **It cannot ship everywhere.** MIT, Apache-2.0, GPL, AGPL and CC BY-NC all appear in this family.

## Where our decoder stands

Downstream of this family, and independent of it. The decoder consumes a tracking feed and automatic tags and asks nothing of the video. It was built for missing and noisy evidence, which is the regime video-derived tracking produces. The output of this family is the kind of input it is designed to take.
