---
title: "Geometric synchronisation"
kicker: "Synchronisation"
summary: "Time offset as a geometric unknown. If two cameras see the same moving points, the offset that makes their geometry consistent is the right one."
group: synchronization
order: 40
chips: ["Video", "Multi-camera", "Geometry", "Research"]
motif: camera
motif_caption: "Several cameras watch the same moving players. Only one set of time offsets makes the views agree."
motif_labels: ["Camera A", "Camera B", "Camera C", "Camera D"]
facts:
  - { k: "Modality", v: "Multi-camera video with moving correspondences" }
  - { k: "Output", v: "Time offset between views, with camera geometry" }
  - { k: "Evidence", v: "CVPR 2017; CVPR 2026; CVPR Findings 2026" }
  - { k: "Code and weights", v: "Official MV-TAP code; the other two are papers" }
  - { k: "Licence", v: "MIT (MV-TAP)" }
verdict: { label: "Our read", text: "The principle to keep: motion is a clock. In football, apply it on the pitch plane, where it becomes simple." }
sources:
  - { title: "On the Two-View Geometry of Unsynchronized Cameras (Albl et al., CVPR 2017)", url: "https://openaccess.thecvf.com/content_cvpr_2017/html/Albl_On_the_Two-View_CVPR_2017_paper.html" }
  - { title: "SyncTrack4D: Cross-Video Motion Alignment and Video Synchronization (CVPR Findings 2026)", url: "https://openaccess.thecvf.com/content/CVPR2026F/html/Lee_SyncTrack4D_Cross-Video_Motion_Alignment_and_Video_Synchronization_with_Multi-Video_4D_CVPRF_2026_paper.html" }
  - { title: "MV-TAP: Tracking Any Point in Multi-View Videos (CVPR 2026)", url: "https://openaccess.thecvf.com/content/CVPR2026/html/Koo_MV-TAP_Tracking_Any_Point_in_Multi-View_Videos_CVPR_2026_paper.html" }
  - { title: "MV-TAP: official code", url: "https://github.com/cvlab-kaist/MV-TAP" }
related:
  - /solutions/synchronization/learned-video-alignment/
  - /solutions/synchronization/dtw-python/
  - /solutions/vision-and-calibration/pnlcalib/
---
Two-view geometry assumes both images were taken at the same instant. Albl and colleagues asked what happens when they were not. A point moving through the scene is seen by the second camera slightly later than by the first, so it sits a little further along its path, and the classical constraint between the views is violated in a structured way. Their solution adds the time offset as an unknown and solves for geometry and synchronisation together.

SyncTrack4D brings the idea to current tools. It matches dense motion across videos and reasons about a shared 4D scene, recovering offsets from how the moving content must fit together.

MV-TAP sits one step later. Given views that already correspond in time, it tracks points jointly across cameras with cross-view attention, so that a point hidden from one camera is carried by the others.

| Work | Solves | Needs |
|---|---|---|
| Albl et al. | Offset and two-view geometry jointly | Moving correspondences in both views |
| SyncTrack4D | Offsets through multi-video 4D reasoning | Overlapping views of dynamic content |
| MV-TAP | Point tracks across views | Views already synchronised |

## Where it wins

- It uses motion itself as the clock. No audio, no timecode, no shared hardware.
- Sub-frame offsets are natural, because time is a continuous unknown.
- Players are good moving points: many of them, spread across the scene, rarely still.
- After synchronisation, multi-view tracking recovers what any single camera loses to occlusion.

## What it costs

- It requires overlapping views and correspondences between them, which wide baselines and identical kits make hard.
- It assumes one coherent segment. An edited broadcast violates that at every cut.
- Slow or straight-line motion barely constrains time.
- Full 4D reasoning is heavy machinery for a sport played on a plane.

## How it plugs into possession

Football offers a shortcut the general methods cannot assume: the pitch is a known plane. Project both views to pitch coordinates and the problem collapses to aligning two sets of 2D trajectories in time. The same move aligns video to tracking, with the tracking feed playing the part of a second camera.

That is the form worth building for possession work: a per-shot offset search on projected player positions, scored by how well they match. It depends on [calibration]({{ '/solutions/vision-and-calibration/pnlcalib/' | relative_url }}) first. The papers here supply the principle, that motion constrains time, and the general case for unusual camera rigs.
