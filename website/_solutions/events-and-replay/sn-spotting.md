---
title: "SoccerNet spotting development kits"
kicker: "Events and replay"
summary: "The task definitions, data loaders, baselines and evaluators for action spotting and ball-action spotting. The reference frame every football spotter is measured in."
group: events-and-replay
order: 50
chips: ["Video", "Benchmark", "Evaluation code"]
motif: matrix
motif_caption: "Every spotter is scored class by class, at a stated tolerance in time."
motif_labels: ["Pass", "Drive", "Shot", "Tackle", "mAP@1"]
facts:
  - { k: "Modality", v: "Broadcast video with timestamped labels" }
  - { k: "Output", v: "Spotting scores: mean average precision at set tolerances" }
  - { k: "Evidence", v: "SoccerNet challenges with public leaderboards" }
  - { k: "Code and weights", v: "Development kit with loaders, baselines and the evaluator" }
  - { k: "Licence", v: "None declared in repository; footage on SoccerNet terms" }
verdict: { label: "Our read", text: "The shared ruler of event spotting. Know its tolerance before quoting anyone's score." }
sources:
  - { title: "sn-spotting: development kit for the SoccerNet action spotting challenges", url: "https://github.com/SoccerNet/sn-spotting" }
  - { title: "SoccerNet ball-action spotting task page", url: "https://www.soccer-net.org/tasks/ball-action-spotting" }
related:
  - /solutions/events-and-replay/team-tdeed/
  - /solutions/events-and-replay/ball-action-winner/
  - /solutions/events-and-replay/sn-replay-grounding/
  - /datasets/soccernet-ball-actions/
---
SoccerNet defines spotting as predicting a timestamp and a class, with no start and no end. Its two tasks sit at different scales. Action spotting covers match events across full broadcasts: goals, cards, substitutions, corners, fouls. Ball-action spotting covers what happens on the ball: passes, drives and the other touches that move play.

The metric is mean average precision at a tolerance. A prediction counts if it falls within a window around a true event. Ball-action spotting is reported at one second, written mAP@1.

The development kit holds the loaders, baseline models and the evaluator the challenge uses.

## Where it wins

- Common definitions. A "pass" and a "drive" mean the same thing across papers.
- The evaluator is reusable for any timestamped prediction, possession-change times included.
- Leaderboards show what is achievable for each class, and which classes are hard.

## What it costs

- Tolerances are generous by possession standards. mAP@1 forgives an error of 25 frames.
- Spotting has no state. It cannot say who has the ball between events.
- The footage is broadcast, with cuts and replays in the stream.

## How it plugs into possession

Read every event-model number through this lens. A spotter's score describes sparse recall at one-second tolerance on broadcast footage. A possession system needs dense labels at frame tolerance.

The class definitions are the bridge. Each ball action implies something about possession before and after it, and writing that mapping down is the first step in using any spotter as evidence.

The data behind the two tasks is covered under [SoccerNet Action Spotting]({{ '/datasets/soccernet-action-spotting/' | relative_url }}) and [SoccerNet Ball Action Spotting]({{ '/datasets/soccernet-ball-actions/' | relative_url }}).
