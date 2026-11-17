---
title: SoccerNet Camera Calibration
kicker: Detection, calibration and synthetic
summary: "Broadcast images annotated with pitch lines and keypoints, and the benchmark every football calibrator reports on. The dataset behind most homography models, and the exam they sit."
group: geometry
order: 10
chips: [Broadcast images, Pitch lines, Camera model]
motif: homography
motif_caption: "Pitch markings in the image, the same markings on the plan. The matrix between them turns pixels into metres."
motif_labels: [Broadcast image, Camera, Pitch model]
facts:
  - { k: Modality, v: "Broadcast images with pitch-line and keypoint annotations" }
  - { k: Task, v: "Estimate the camera that maps the pitch to the image" }
  - { k: Score, v: "Reprojection accuracy within a pixel tolerance, and completeness" }
  - { k: Possession labels, v: "None" }
  - { k: Video, v: "Stills and clips, not continuous matches" }
  - { k: Licence, v: "SoccerNet research terms. Underlying video protected" }
  - { k: Access, v: "Annotations and development kit public (SN-Calibration-2023)" }
verdict:
  label: Our read
  text: "Calibration is the quiet dependency of every distance in football AI. This is where it is trained and, more usefully, where its failures are measured."
sources:
  - { title: "Development kit with baseline and evaluator", url: "https://github.com/SoccerNet/sn-calibration" }
  - { title: "SoccerNet camera calibration task page", url: "https://www.soccer-net.org/tasks/camera-calibration" }
  - { title: "SN-Calibration-2023 dataset", url: "https://huggingface.co/datasets/SoccerNet/SN-Calibration-2023" }
  - { title: "SoccerNet datasets and access table", url: "https://github.com/SoccerNet/SoccerNet" }
related:
  - /datasets/soccernet-gsr/
  - /solutions/vision-and-calibration/pnlcalib/
  - /solutions/vision-and-calibration/tvcalib/
  - /architecture/multi-camera-geography/
---

## What it is

Each image is annotated with the pitch markings it shows: touchlines, penalty areas, the centre circle, the goals. A calibration method has to recover the camera from those correspondences, and is scored on how well the pitch model reprojects onto the image.

## How it scores

The score has two parts. Accuracy asks how well the projected markings fall on the annotated ones, within a pixel tolerance. Completeness asks how much of the test set the method answered at all. Scoring both stops a method from looking good by answering only the easy frames, and it measures the failure that matters in production: frames with no answer.

The evaluator is public, so the same test can be run on frames annotated from your own camera. [PnLCalib]({{ '/solutions/vision-and-calibration/pnlcalib/' | relative_url }}), [TVCalib]({{ '/solutions/vision-and-calibration/tvcalib/' | relative_url }}) and [KpSFR]({{ '/solutions/vision-and-calibration/kpsfr/' | relative_url }}) are comparable because they report here.

## What it teaches

| Signal | What you get |
|---|---|
| Possession | Nothing direct |
| Tracking | Nothing |
| Events | Nothing |
| Calibration | The task itself: field markings to a camera model, with a reprojection score |

## Where it wins

- **Direct supervision.** Line and keypoint labels are exactly what a homography estimator consumes.
- **Real broadcast framing.** Tight shots, few visible lines, players standing on the markings.
- **A hard score.** Methods are judged by reprojecting the pitch model, so a plausible-looking but wrong camera is exposed.

## What it costs

- **Single frames.** No temporal consistency is tested. A calibration that jitters from frame to frame can still score well.
- **Planar assumptions.** One homography models a flat pitch through one lens. Stitched panoramas and lens distortion break it.
- **Occlusion.** The fewer markings in view, the less constrained the answer.
- **Pixels, not metres.** Reprojection error in the image is not position error on the pitch. A good score still allows large errors far from the camera, and possession cares about metres near the ball.

## How it plugs into possession

Possession evidence is measured in metres. Who is nearest the ball, whether anyone is within playing distance, whether the ball has crossed the line. All of it passes through the pixel-to-pitch mapping first. A homography error is a distance error, and a distance error near a touchline is the difference between live and dead.

That makes calibration validity a possession feature in its own right. In the competition data the organisers' documentation marks the broadcast homography as usable on 65.8% of its frames. A system that uses the mapping only where it can be trusted needs a model of when that is, and this benchmark is where such a model is built.
