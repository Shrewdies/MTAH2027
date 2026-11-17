---
layout: wiki-entry
nav_exclude: true
title: "Homography: the bridge between pixels and pitch"
kicker: The data
summary: "A 3×3 matrix per frame that maps the pitch plane to the image. It makes video usable as geometry, and it has one hard limit: the ground."
route_label: Homography
hook: "Pixels to pitch"
group: data
order: 90
chips: [Per frame, Planar, Pitch to image]
motif: homography
motif_caption: The camera sees a trapezoid; the matrix turns it back into a rectangle. A ball in the air has no place on that plane.
motif_labels: [Tactical image, Homography, Pitch plane]
facts:
  - { k: Form, v: "3×3 projective matrix per frame" }
  - { k: Tactical view, v: "Every frame usable" }
  - { k: Broadcast view, v: "65.8% of frames usable" }
  - { k: Limit, v: "Ground plane only" }
verdict:
  label: Our read
  text: "The supplied homography removes the hardest step of any vision add-on: a detection in the tactical image can be placed on the pitch at once. What it cannot do is tell a ball at head height from a ball ten metres further away."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "PnLCalib", url: "https://github.com/mguti97/PnLCalib" }
  - { title: "TVCalib", url: "https://github.com/MM4SPA/tvcalib" }
  - { title: "SoccerNet camera calibration benchmark", url: "https://github.com/SoccerNet/sn-calibration" }
related:
  - /challenges/data-asset-map/
  - /challenges/broadcast-and-timebases/
  - /datasets/soccernet-calibration/
  - /architecture/multi-camera-geography/
---
## What it is

A homography is a planar projective transform: a 3×3 matrix that maps a point on the pitch to a pixel in the frame, and back. One matrix per frame absorbs the viewpoint, the perspective and the camera's pan, tilt and zoom.

It is a statement about a plane. Points on the grass map exactly. Points above it do not.

## What a good one depends on

- **Landmarks.** Enough pitch lines, corners and circle arcs in view, spread across the image.
- **Correspondences.** Each landmark matched to its true pitch location, with mismatches rejected.
- **Lens.** Distortion handled, or small enough to ignore.

When the camera zooms into a duel and the lines leave the frame, there is nothing to calibrate against. That is why the wide tactical view is usable on every frame and the broadcast view on 65.8% of them.

## Five things it is not

| Often confused with | The difference |
|---|---|
| Accuracy | A matrix can exist and still be metres off far from the landmarks |
| Camera pose | Intrinsics and extrinsics describe the camera in 3D; a homography describes one plane |
| Ball height | A lofted ball projects to the wrong ground point |
| Time alignment | A correct projection of the wrong moment is still wrong |
| Player position | Project the feet, not the centre of the box |

## How it plugs into possession

The tracking arrives already in pitch coordinates, so the decoder never needs the matrix to reason about control. The homography matters the moment vision enters: a ball found in the tactical image by a detector becomes a pitch position through the same per-frame matrix, on the same clock, with no calibration work.

That is the route for on-device vision on untracked frames, on our [roadmap]({{ '/challenges/roadmap/' | relative_url }}). The planar limit travels with it: a detected ball in flight needs its height reasoned about, or its ground position treated as uncertain.

Calibration methods are mapped in [Vision and calibration]({{ '/solutions/vision-and-calibration/' | relative_url }}), and the benchmark that grades them is [SoccerNet Camera Calibration]({{ '/datasets/soccernet-calibration/' | relative_url }}). What two cameras need before they can be used as one is in [Space is not time]({{ '/architecture/multi-camera-geography/' | relative_url }}).
