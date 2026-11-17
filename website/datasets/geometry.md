---
layout: wiki-hub
title: Detection, calibration and synthetic
permalink: /datasets/geometry/
collection_index: datasets
only_group: geometry
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "Pixels to metres, and the ball in three dimensions. Possession is decided by distances, so a geometry error is a possession error waiting to happen."
motif: ds-error
icon: homography
motif_caption: "Two opponents, one ball, a metre of doubt on each position. Whoever the geometry favours gets the possession."
motif_labels: [Control radius 1.5 m, Position error, Nearest player flips]
stats:
  - { value: "{count}", label: datasets }
  - { value: "1.5 m", label: control radius our decoder keeps physical }
  - { value: "2", label: sources of real 3D ball positions }
---

## What this family is

Five datasets with no football semantics at all. They do not know what a pass is. They know where the pitch is in the image, where a player stands in metres, how high the ball is, and how to keep a detector working in bad light.

That is exactly why they matter to possession. Control is a distance. Out of play is a line. Both are measured after a camera model has turned pixels into metres.

## Five datasets, four jobs

| Dataset | Job | Footage | Licence |
|---|---|---|---|
| [SoccerNet Calibration]({{ '/datasets/soccernet-calibration/' | relative_url }}) | Camera from pitch markings | Real broadcast | Research terms |
| [SoccerNet-v3D]({{ '/datasets/soccernet-v3d/' | relative_url }}) | 3D ball from a live shot and its replay | Real broadcast | Footage on SoccerNet terms |
| [ball3d]({{ '/datasets/ball3d/' | relative_url }}) | 3D ball trajectories from many views | Real, one match at its core | CC BY-NC-SA 4.0 |
| [Spiideo SynLoc]({{ '/datasets/spiideo-synloc/' | relative_url }}) | Player positions in metres from one frame | Synthetic and real | Set by Spiideo |
| [SoccerSynth-Detection]({{ '/datasets/soccersynth-detection/' | relative_url }}) | Player detection under varied conditions | Synthetic | Zenodo record terms |

## How to choose

| You need | Use |
|---|---|
| A homography estimator, and a measure of when it fails | SoccerNet Calibration |
| Ball height from ordinary television pictures | SoccerNet-v3D |
| A ball motion model tested against truth | ball3d |
| A detector scored in metres, not pixels | Spiideo SynLoc |
| Robustness to light, texture and blur | SoccerSynth-Detection |

## Height and metres

Two quantities decide more possession calls than any model choice. The first is ball height. In 2D a long ball passes within reach of several players on its way down the pitch, and none of them can play it.

{% include wiki/motif.html id="ds-height" caption="A long ball passes above three players. On a 2D map its ground projection crosses each player's control radius on the way, and none of them can play it." %}

The second is localisation error. A box two pixels off at the far touchline of a wide view is a metre off on the grass.

{% include wiki/motif.html id="ds-pixel-metre" caption="The same two pixels are centimetres in front of the camera and about a metre at the far touchline. A detector scored in pixels hides that. One scored in metres cannot." %}

## The traps

- **Matrix direction.** ball3d's homographies map image to pitch. Other providers ship pitch to image. Check before composing transforms.
- **One plane, one lens.** A homography assumes a flat pitch through a single camera. Stitched panoramas and lens distortion break it.
- **Single frames.** Calibration benchmarks score each image alone. A camera model that jitters between frames can still score well.
- **Sim to real.** Rendered players are cleaner than real ones. Synthetic data widens a detector; it does not validate one.
- **Licences.** ball3d is non-commercial and share-alike. The synthetic sets carry their hosts' terms.

## What it cannot do

Tell you anything about football. No events, no teams in possession, no spells. This family improves the evidence. It never supplies the answer.

## Where it meets our decoder

Our decoder works in pitch coordinates and keeps its control radius physical: a player within 1.5 m of the ball and closer than any opponent. The radius stayed outside the parameter search on purpose. Left free, the search on simulated matches pushed it to an unrealistic 0.8 m.

A missing ball is treated as no evidence, never as a stoppage, which is the defensive version of this family's lesson: when the geometry cannot say, do not guess. What calibration has to guarantee before two cameras can be used as one is set out in [Space is not time]({{ '/architecture/multi-camera-geography/' | relative_url }}).
