---
title: "PnLCalib (and No Bells, Just Whistles)"
kicker: "Vision and calibration"
summary: "Camera calibration from pitch keypoints and lines together, refined by non-linear optimisation. The method to start from when turning a broadcast frame into pitch coordinates."
group: vision-and-calibration
order: 80
chips: ["Video", "Calibration", "Open weights", "GPL code"]
motif: homography
motif_caption: "Keypoints and lines found in the image pin the camera. The frame then maps onto the pitch."
motif_labels: ["Points and lines", "Camera", "Pitch plane"]
facts:
  - { k: "Modality", v: "A single video frame" }
  - { k: "Output", v: "Camera parameters and a homography" }
  - { k: "Evidence", v: "Published research; predecessor at CVPR Workshops 2024" }
  - { k: "Code and weights", v: "Inference code; pretrained keypoint and line models" }
  - { k: "Licence", v: "Code GPL-2.0-or-later; weights CC BY 4.0" }
verdict: { label: "Our read", text: "The calibration method to start from. Points plus lines plus refinement is the right recipe. The licence makes it a tool, not a component." }
sources:
  - { title: "PnLCalib: Sports Field Registration via Points and Lines Optimization (official code)", url: "https://github.com/mguti97/PnLCalib" }
  - { title: "No Bells, Just Whistles: Sports Field Registration by Leveraging Geometric Properties (official code, CVPR Workshops 2024)", url: "https://github.com/mguti97/No-Bells-Just-Whistles" }
related:
  - /solutions/vision-and-calibration/tvcalib/
  - /datasets/soccernet-calibration/
  - /solutions/vision-and-calibration/kpsfr/
---
Every conversion from pixels to pitch needs the camera. PnLCalib estimates it from the one calibration target a football broadcast always contains: the pitch markings.

Networks produce heatmaps for keypoints and for lines. From those correspondences the method computes an initial camera, then refines it with a non-linear optimisation over points and lines jointly. Lines matter because many frames show few intersections but long stretches of touchline or penalty-area edge.

It builds on the same author's earlier No Bells, Just Whistles (CVPR Workshops 2024), which established keypoint and line detection using the geometry of the pitch. PnLCalib adds the camera model and the refinement. Released weights cover single-view and multi-view variants.

## Where it wins

- It uses points and lines, so it holds up on frames where keypoint-only methods run short of evidence.
- It returns camera parameters, not only a homography. A full camera can project points off the ground plane.
- Pretrained models and video inference are included.
- Its weights are CC BY 4.0, clear terms that many vision checkpoints lack.

## What it costs

- GPL code. It can be run as a tool. It cannot be folded into a permissively licensed codebase.
- It needs visible markings. Close-ups and midfield shots with grass and a halfway line stay under-determined.
- Per-frame estimates jitter. Video use wants temporal smoothing of the camera.
- A camera does not give the ball's height. A ball in the air projects to the wrong spot on the ground.

## How it plugs into possession

Calibration is the hinge between video and possession. Detections become evidence only after projection to pitch coordinates, and projection error is distance error, the quantity possession evidence is built from. A metre of calibration error at the far touchline can decide which of two players is "closest".

The practical pattern is to calibrate, smooth the camera over time and carry a per-frame reprojection error forward as a confidence. Where a tracking feed already exists, calibration serves verification and ball recovery, not the main path.

Methods are compared on the [SoccerNet Camera Calibration]({{ '/datasets/soccernet-calibration/' | relative_url }}) benchmark.
