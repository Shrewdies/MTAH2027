---
title: "CoTracker"
kicker: "Vision and calibration"
summary: "Tracks any set of points through a video jointly, so that points help locate one another through occlusion."
group: vision-and-calibration
order: 70
chips: ["Video", "Point tracking", "Open weights", "CC BY-NC"]
motif: tracks
motif_caption: "Points are followed together. Visible ones carry the hidden ones through occlusion."
motif_labels: ["Query point", "Point track"]
facts:
  - { k: "Modality", v: "Video plus query points" }
  - { k: "Output", v: "Point trajectories with a visibility flag" }
  - { k: "Evidence", v: "ECCV 2024; CoTracker3 follow-up" }
  - { k: "Code and weights", v: "Inference code, demo and public checkpoints" }
  - { k: "Licence", v: "Mostly CC BY-NC; third-party parts differ" }
verdict: { label: "Our read", text: "The finest motion evidence video can give, under a licence that keeps it in the lab." }
call:
  title: "Why it stayed out of the build"
  constraint: "Licences"
  text: "CoTracker is released mostly under CC BY-NC. A non-commercial component cannot ship in an MIT repository, so it was never a dependency option. The knowledge stands. The code stays outside."
sources:
  - { title: "facebookresearch/co-tracker: code, demo and checkpoints for CoTracker and CoTracker3", url: "https://github.com/facebookresearch/co-tracker" }
related:
  - /solutions/vision-and-calibration/sam2/
  - /solutions/synchronization/geometric-sync/
  - /solutions/vision-and-calibration/tracking-by-detection/
---
Point tracking follows individual pixels, not objects. Pick a point on a player's boot in one frame and find that same physical point in every other frame. Earlier trackers followed each point independently. CoTracker tracks them together.

A transformer takes all the query points at once and refines their trajectories over a window of frames. Attention across points lets the model use their correlation. Points on the same body move together, and a point that is occluded can be placed from the motion of its visible neighbours. The model outputs a position and a visibility flag for every point in every frame, and windows slide to cover long videos. CoTracker3 simplified the design and trained on real video with pseudo-labels.

## Where it wins

- Dense motion below the level of the object. A point on the ball and points on a foot give contact timing that boxes cannot.
- Explicit visibility output. The model says when it is guessing.
- Joint tracking holds through occlusions that break independent point trackers.
- It works with no football training.

## What it costs

- CC BY-NC. Research use only. It cannot be part of a commercial or permissively licensed product.
- Points are not identities. Nothing ties a trajectory to a player or a team.
- It needs query points from somewhere, and a fast ball is the kind of small, blurred target point trackers lose.
- Windowed transformer inference over long video needs a GPU.

## How it plugs into possession

Point tracks are the finest-grained motion evidence video offers. The instant a ball's trajectory bends at a foot is the instant possession changes. As a research instrument for studying touch timing, or for producing reference labels on footage you are licensed to annotate, it is excellent.

In a product pipeline its role would be narrow: local motion around the ball in ambiguous moments, with a tracker supplying identity and a decoder supplying sequence. [SAM 2]({{ '/solutions/vision-and-calibration/sam2/' | relative_url }}) covers neighbouring ground under a permissive licence.
