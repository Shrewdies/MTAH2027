---
title: "Roboflow Sports: soccer detectors"
kicker: "Vision and calibration"
summary: "Three YOLOv8 checkpoints for players, ball and pitch keypoints, wired into a runnable pipeline with team clustering and a radar view."
group: vision-and-calibration
order: 10
chips: ["Video", "Detection", "Open weights", "Mixed licences"]
motif: boxes
motif_caption: "One model finds the people, a second hunts the ball, a third finds the pitch."
motif_labels: ["Player", "Ball"]
facts:
  - { k: "Modality", v: "Broadcast or tactical video" }
  - { k: "Output", v: "Boxes, ball candidates, pitch keypoints, team assignment" }
  - { k: "Evidence", v: "Runnable example with a separate mode for each stage" }
  - { k: "Code and weights", v: "Example code; three checkpoints fetched by the setup script" }
  - { k: "Licence", v: "MIT code; AGPL-3.0 runtime; checkpoint terms unstated" }
verdict: { label: "Our read", text: "The fastest working football vision stack. Excellent for prototyping. Read the licences before shipping." }
call:
  title: "Why no detector ran on the video"
  constraint: "Licences"
  text: "The stack rests on an AGPL-3.0 runtime and on checkpoints with no stated terms. Neither can ship inside an MIT repository. We solved the untracked ball in the decode instead, where it costs no dependency and no GPU."
sources:
  - { title: "roboflow/sports: the soccer example (code and usage)", url: "https://github.com/roboflow/sports/tree/main/examples/soccer" }
  - { title: "setup.sh: the script that downloads the three checkpoints", url: "https://github.com/roboflow/sports/blob/main/examples/soccer/setup.sh" }
related:
  - /solutions/vision-and-calibration/sn-gamestate/
  - /solutions/vision-and-calibration/tracking-by-detection/
  - /solutions/vision-and-calibration/pnlcalib/
---
The soccer example in Roboflow's sports repository is the quickest route from a football video to structured detections. Its setup script downloads three YOLOv8 checkpoints: one for the people on the pitch, one specialised for the ball, one for pitch keypoints.

The example chains them. Player boxes are tracked across frames. Team assignment is unsupervised: appearance features of the player crops are clustered into two kits. Pitch keypoints give a homography, which projects players and ball onto a top-down radar. Each stage has its own run mode, so a component can be judged alone.

## Where it wins

- It runs out of the box, stage by stage.
- A dedicated ball model addresses the hard part of football detection, a small fast object.
- Keypoint homography needs no manual calibration.
- Unsupervised team assignment needs no kit labels.

## What it costs

- Licence layers. The example code is MIT, the YOLOv8 runtime is AGPL-3.0, and the checkpoints state no terms of their own.
- Per-frame detection at match length is GPU work. Ninety minutes at 25 fps is 135,000 frames.
- The ball remains the weak point: small, fast, blurred, occluded. Detection confidence drops exactly when possession is in doubt.
- A homography from keypoints fails on tight shots with few pitch markings in view.

## How it plugs into possession

As a second opinion on the ball. Where a tracking feed loses the ball, a video detector projected through a homography can supply positions the feed lacks, each with a confidence a decoder can weigh. It can also rebuild the whole chain when there is no tracking feed: video in, pitch coordinates out, possession inference on top.

Each stage adds error, and errors compound. A few pixels of detection error become metres on the far side of the pitch. Treat video-derived positions as noisier than provider tracking and say so in the evidence weights.

For the full reconstruction task, with identities, see [Game State Reconstruction]({{ '/solutions/vision-and-calibration/sn-gamestate/' | relative_url }}).
