---
title: SoccerSynth-Detection
kicker: Detection, calibration and synthetic
summary: "A synthetic, broadcast-style image corpus for player detection, rendered with controlled lighting, textures, camera angles and motion blur."
group: geometry
order: 50
chips: [Synthetic images, Player boxes, Zenodo]
motif: matrix
motif_caption: "Each rendering condition is a dial. Every combination comes with exact player boxes."
motif_labels: [Light, Texture, Camera, Blur, Boxes]
facts:
  - { k: Modality, v: "Synthetic football images with player bounding boxes" }
  - { k: Scale, v: "About 90 GB" }
  - { k: Variation, v: "Lighting, textures, camera, simulated motion blur" }
  - { k: Possession labels, v: "None. No ball labels" }
  - { k: Video, v: "Rendered images only" }
  - { k: Licence, v: "Terms on the Zenodo record" }
  - { k: Access, v: "Zenodo archive, code on GitHub" }
verdict:
  label: Our read
  text: "Augmentation, not a foundation. It widens the conditions a player detector has seen, and it does that job well. It is the furthest dataset here from a possession label."
sources:
  - { title: "Paper, Scientific Reports (2026)", url: "https://www.nature.com/articles/s41598-026-67849-4" }
  - { title: "Dataset archive on Zenodo", url: "https://zenodo.org/records/20839314" }
  - { title: "Code", url: "https://github.com/open-starlab/SoccerSynth-Detection" }
related:
  - /datasets/spiideo-synloc/
  - /datasets/soccernet-tracking/
---

## What it is

A rendered dataset for one job: detecting players in broadcast-like images. The generator controls what real footage cannot: lighting, textures, camera position and the amount of motion blur. Every image comes with exact player boxes.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing |
| Tracking | Player detection in single images |
| Events | Nothing |
| Calibration | Nothing. Camera settings vary but no match calibration is provided |

## Where it wins

- **Free labels at volume.** No annotation cost, no annotation noise.
- **Conditions on demand.** Harsh light, unusual textures, heavy blur: generate the cases real datasets are short of.
- **No footage in it.** Nothing was filmed, so no broadcast rights stand in the way.

## What it costs

- **Appearance gap.** Rendered players do not move or crowd like real ones. Mix with real data and evaluate on real clips.
- **Players only.** No ball, no time.
- **Archive terms.** The paper is open access. The data archive carries its own conditions on Zenodo.

## How it plugs into possession

At two removes. Better detection gives better tracking, and better tracking gives better possession evidence. The link is real but long.

Its practical value is robustness. Possession systems fail in the minutes where the detector fails: low sun across half the pitch, floodlight glare, rain. Synthetic variation is the cheapest way to make those minutes less special.
