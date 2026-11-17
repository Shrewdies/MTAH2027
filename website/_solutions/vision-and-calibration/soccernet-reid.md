---
title: "SoccerNet re-identification"
kicker: "Vision and calibration"
summary: "The benchmark and baseline for recognising the same player across camera views, in a sport where every team-mate wears the same shirt."
group: vision-and-calibration
order: 50
chips: ["Video", "Identity", "Benchmark", "MIT"]
motif: matrix
motif_caption: "Candidates are ranked cue by cue. In football the kit column never separates team-mates."
motif_labels: ["Kit", "Build", "Hair", "Boots", "Number"]
facts:
  - { k: "Modality", v: "Player crops from several broadcast cameras" }
  - { k: "Output", v: "Identity embeddings and match rankings" }
  - { k: "Evidence", v: "Official SoccerNet task with challenge baselines" }
  - { k: "Code and weights", v: "Development kit and baseline training code" }
  - { k: "Licence", v: "MIT code; data under SoccerNet's terms" }
verdict: { label: "Our read", text: "Identity is the hard residue of football vision. Not needed for H/A/D, indispensable the moment the question becomes who." }
sources:
  - { title: "sn-reid: development kit for the SoccerNet re-identification challenge", url: "https://github.com/SoccerNet/sn-reid" }
related:
  - /solutions/vision-and-calibration/tracking-by-detection/
  - /solutions/vision-and-calibration/sn-gamestate/
  - /solutions/events-and-replay/footpass/
---
Re-identification asks whether two image crops show the same person. In surveillance the cue is clothing. In football clothing is the one thing that cannot help: ten outfield players share a kit, and the task becomes telling them apart by build, hair, boots, posture and a shirt number when it happens to be visible.

SoccerNet's task frames this across cameras. A player seen in one view of an action must be matched to the same player seen from another angle. The development kit provides the data loaders, a baseline built on standard re-identification training, and the ranking metrics.

## Where it wins

- Football-specific. Models trained here learn the cues that survive identical kits.
- Cross-view matching is what multi-camera and replay analysis need.
- Its embeddings can replace pedestrian models in appearance-based [trackers]({{ '/solutions/vision-and-calibration/tracking-by-detection/' | relative_url }}).

## What it costs

- Low-resolution crops limit what any model can see. At wide-shot scale, team-mates are near-identical.
- Matching within one action is the easy case. Identity across a whole match is harder.
- Embeddings say "same" or "different", not who. Naming a player takes shirt-number reading or a roster.

## How it plugs into possession

Team possession does not need player identity. Player possession does, and so does everything built on it: who lost the ball, who won it, pass networks. Re-identification is how anonymous tracks become players.

It also guards the team label. The strongest appearance cue is kit colour, and an appearance embedding separates the two teams far more reliably than it separates team-mates. Used as a team classifier, it is working on the easy version of its own problem.
