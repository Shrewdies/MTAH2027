---
title: Space is not time
kicker: The hard parts
summary: "Calibration says where a pixel lands on the pitch in one frame. It says nothing about when. Which calibration to trust, where it stops being true, and why geometry and timing are two separate gates."
group: hard-parts
order: 20
chips: [Homography, Calibration, Multi-camera]
motif: bp-geometry
icon: homography
motif_caption: "A boot on the grass maps exactly. A ball in flight lands in the wrong place, because height is unseen. And cross-view evidence passes only when the space gate and the time gate are both open."
facts:
  - { k: Spatial problem, v: "Pixel to pitch, one frame at a time" }
  - { k: Holds for, v: "Points on the ground plane" }
  - { k: A flying ball needs, v: "Full camera geometry and synced views" }
  - { k: Rule, v: "Two gates, space and time, each with its own error" }
verdict:
  label: Our read
  text: "Treat calibration and synchronisation as two separate gates, each with its own error. Cross-view evidence passes only when both are open."
sources:
  - { title: "PnLCalib: points-and-lines pitch calibration", url: "https://github.com/mguti97/PnLCalib" }
  - { title: "TVCalib: camera calibration for sports field registration", url: "https://github.com/MM4SPA/tvcalib" }
  - { title: "OpenCV: camera calibration and 3D reconstruction", url: "https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/match-timeline/
  - /challenges/homography/
  - /solutions/vision-and-calibration/pnlcalib/
  - /solutions/vision-and-calibration/tvcalib/
  - /datasets/soccernet-calibration/
---

## The design question

What has to be true before a point seen by one camera can be compared with a point seen by another? Two
things, and they are independent: the geometry must be right in each frame, and the frames must show the
same moment. What a homography is, and what the supplied ones contain, is in
[Homography: the bridge between pixels and pitch]({{ '/challenges/homography/' | relative_url }}). This study
is about the design choices: which calibration, and what to do where it fails. It is the second
prerequisite of [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }}).

## Calibration options

| Method | Strength | Constraint |
|---|---|---|
| Supplied homography | Available and documented | Accuracy varies shot by shot |
| Pitch keypoint matching | Simple physical correspondence | Needs the right landmarks in view |
| Points and lines refinement | Works with part of the pitch visible | A misidentified line bends everything |
| Multi-frame consistency | Stabilises a moving camera | A cut breaks the smoothness |
| Full 3D camera model | Enables true triangulation | More unknowns, synchronised views |

## Why accuracy varies shot by shot

{% include wiki/motif.html id="bp-s-landmarks" caption="A wide shot shows many pitch landmarks and the camera is pinned down. A tight shot shows two, and the projected pitch is free to swing. The tight shot is also the one that shows the ball best." %}

## The flat-earth limit

A homography relates the pitch plane to the image. It is exact for a boot on the grass and wrong for a
ball in the air. Two homographies from two cameras do not triangulate a ball in flight when its height is
unobserved. That needs real camera geometry and detections close enough in time to be the same ball.

## What breaks it in real football

- **A fast pan.** The camera model lags the picture, and projected players slide across the pitch.
- **A cross.** The ball leaves the ground plane and its projected position runs away from its true one.
- **Good geometry, wrong moment.** Reprojection error is small and the frames are half a second apart. A
  sprinting player has moved metres.

## How to judge it

Project known pitch points into the image and measure the reprojection error in pixels, then in metres on
the pitch, per shot type. Then count how much cross-view evidence survives when both gates are applied.
