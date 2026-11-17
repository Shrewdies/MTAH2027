---
title: "TVCalib"
kicker: "Vision and calibration"
summary: "Calibration as direct optimisation: segment the pitch markings, then fit the camera whose projection of the pitch model lands on them."
group: vision-and-calibration
order: 90
chips: ["Video", "Calibration", "Open weights", "MIT"]
motif: camera
motif_caption: "Any camera around the pitch is a handful of parameters. TVCalib solves for them directly."
motif_labels: ["Main camera", "Tactical", "Behind goal", "Reverse"]
facts:
  - { k: "Modality", v: "A single video frame" }
  - { k: "Output", v: "Camera parameters and pitch projection" }
  - { k: "Evidence", v: "WACV 2023" }
  - { k: "Code and weights", v: "Inference notebook; pretrained segmentation checkpoint" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "Calibration done as optimisation, with a quality score for free. Slower than keypoint methods, and the one with the cleanest licence." }
sources:
  - { title: "TVCalib: Camera Calibration for Sports Field Registration in Soccer (arXiv 2207.11709, WACV 2023)", url: "https://arxiv.org/abs/2207.11709" }
  - { title: "TVCalib: official code and inference notebook", url: "https://github.com/MM4SPA/tvcalib" }
related:
  - /solutions/vision-and-calibration/pnlcalib/
  - /solutions/vision-and-calibration/kpsfr/
  - /datasets/soccernet-calibration/
---
TVCalib skips the homography. Most pipelines detect correspondences, estimate a homography and then decompose it into a camera. TVCalib parameterises the camera directly and optimises those parameters by gradient descent.

The evidence is semantic. A segmentation network labels pixels by the marking they belong to: this touchline, that penalty-area edge, the centre circle. The loss is the distance between those pixels and the projection of the matching segment of a pitch model. Because every marking is labelled, no point correspondences are needed, and curved segments such as the circle contribute as much as straight ones.

## Where it wins

- Valid cameras by construction. A homography can be any 3 by 3 matrix. This is always a real camera.
- It uses every visible marking pixel, circles and arcs included.
- The residual of the optimisation is a per-frame quality score.
- MIT code with a released segmentation checkpoint.

## What it costs

- Iterative optimisation per frame is slower than a feed-forward estimate, and it can settle in a local minimum from a poor start.
- It rests on the segmentation. A mislabelled line, near penalty area for far, produces a confident wrong camera.
- Like all marking-based methods, it starves when few lines are in view.
- There is no temporal model. Video needs smoothing added.

## How it plugs into possession

The same role as any calibrator: the bridge from pixels to metres. TVCalib's advantage for possession work is its residual. Frames with a poor fit can be down-weighted or dropped before their positions become evidence.

It is also the most licence-friendly calibrator in this family, which matters for anything that ships. [PnLCalib]({{ '/solutions/vision-and-calibration/pnlcalib/' | relative_url }}) is the points-and-lines alternative.
