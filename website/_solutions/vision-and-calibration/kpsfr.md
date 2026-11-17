---
title: "KpSFR"
kicker: "Vision and calibration"
summary: "Keypoint-based sports field registration: predict a grid of pitch keypoints, then fit the homography. The established baseline from the World Cup benchmark."
group: vision-and-calibration
order: 100
chips: ["Video", "Calibration", "Open weights", "MIT"]
motif: homography
motif_caption: "A grid of template keypoints is located in the image. Their matches fix the homography."
motif_labels: ["Keypoint grid", "Homography", "Pitch template"]
facts:
  - { k: "Modality", v: "A single video frame" }
  - { k: "Output", v: "Pitch keypoints and a homography" }
  - { k: "Evidence", v: "CVPR Workshops 2022; TS-WorldCup benchmark" }
  - { k: "Code and weights", v: "Official code and author checkpoints" }
  - { k: "Licence", v: "MIT" }
verdict: { label: "Our read", text: "The keypoint baseline. Good enough to project feet, licence-clean, and outclassed by points-plus-lines methods." }
sources:
  - { title: "KpSFR: Sports Field Registration via Keypoints-aware Label Condition (official code, CVPR Workshops 2022)", url: "https://github.com/ericsujw/KpSFR" }
related:
  - /solutions/vision-and-calibration/pnlcalib/
  - /solutions/vision-and-calibration/tvcalib/
  - /datasets/soccernet-calibration/
---
KpSFR treats registration as keypoint detection. A uniform grid of keypoints is defined on the pitch template. A network predicts where each grid point appears in the image, and a homography is fitted to the matches.

The difficulty is that grid points look alike. Grass is grass. KpSFR conditions the network on which keypoint it is looking for, so that features are specialised to each point instead of shared across all of them. The work is associated with the TS-WorldCup benchmark, a standard test for football registration.

## Where it wins

- A dense grid gives correspondences even where no line intersection is visible.
- A simple pipeline: keypoints, then a standard homography fit.
- MIT licence and released checkpoints.
- A well-known reference point for newer methods.

## What it costs

- Homography only. There is no camera position or focal length, so nothing off the ground plane can be projected.
- An older dependency stack that takes effort to run today.
- Its benchmark is World Cup broadcast footage. Other camera heights and lenses are out of distribution.
- Methods that add lines and refinement, such as [PnLCalib]({{ '/solutions/vision-and-calibration/pnlcalib/' | relative_url }}), have moved past it.

## How it plugs into possession

As the permissively licensed baseline in a calibration comparison, and as the fallback idea when markings are scarce. Grid keypoints on plain grass are evidence that line-based methods do not have.

For possession a homography is sufficient as long as the question stays on the ground. Player feet and a rolling ball project correctly. A ball in flight does not.
