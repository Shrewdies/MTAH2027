---
title: "SAM 2"
kicker: "Vision and calibration"
summary: "Promptable video segmentation. Indicate an object once and get its mask in every frame, with a memory that survives occlusion."
group: vision-and-calibration
order: 60
chips: ["Video", "Segmentation", "Open weights", "Apache-2.0"]
motif: boxes
motif_caption: "One prompt starts the mask. Memory carries it through the frames and through occlusion."
motif_labels: ["Prompted object", "Ball"]
facts:
  - { k: "Modality", v: "Video plus a point, box or mask prompt" }
  - { k: "Output", v: "Object masks over time" }
  - { k: "Evidence", v: "Meta research release with checkpoints and video demos" }
  - { k: "Code and weights", v: "Inference code; SAM 2.1 checkpoints in several sizes" }
  - { k: "Licence", v: "Apache-2.0" }
verdict: { label: "Our read", text: "The best general-purpose video segmenter, used surgically. Strong on players in contact, unreliable on a distant ball." }
call:
  title: "Why a click was off limits"
  constraint: "Competition rules"
  text: "SAM 2 starts from a prompt. A human click on the match video is a hand label, and the rules allow none. Prompted by an automatic detector instead, it inherits that detector's misses on the ball. We kept people out of the loop: zero hand labels anywhere in the pipeline."
sources:
  - { title: "facebookresearch/sam2: code and checkpoints for Segment Anything Model 2", url: "https://github.com/facebookresearch/sam2" }
related:
  - /solutions/vision-and-calibration/cotracker/
  - /solutions/vision-and-calibration/tracking-by-detection/
  - /solutions/vision-and-calibration/roboflow-soccer/
---
SAM 2 extends Segment Anything from images to video. The interface is a prompt: a click, a box or a mask on one frame says "this object". The model returns that object's mask on the frame and propagates it through the video.

Propagation runs on memory. As the model moves through the video it stores features of the object from frames it has already seen, and each new frame attends to that memory to find the object again. The model also predicts whether the object is visible at all, so a mask can vanish behind another player and reappear. Corrections are prompts too. One more click on a later frame repairs a drift.

## Where it wins

- Class-agnostic. It needs no football training to segment a player, a referee or a goalpost.
- Masks, not boxes. Feet and contact points are localised more precisely, and feet are what project to the pitch.
- Memory brings an object back after occlusion without a separate re-identification model.
- A clear licence and several model sizes.

## What it costs

- It follows what it is shown. Someone, or some detector, must prompt every object of interest.
- A football at broadcast scale is a handful of blurred pixels, the regime where mask propagation is least stable.
- Many simultaneous objects multiply the compute. Twenty-two players for ninety minutes is a heavy job.
- Team-mates in identical kit can capture each other's masks when they cross.

## How it plugs into possession

As a precision instrument, not a pipeline. Its best uses in possession work are targeted: resolve who came out of a duel with the ball, or refine a player's foot position where a box is too coarse. A detector proposes, SAM 2 follows for a few seconds, a decoder consumes the result.

The prompt is the constraint to design around. Where hand annotation is not allowed, prompts must come from an automatic detector, and SAM 2 inherits its mistakes.
