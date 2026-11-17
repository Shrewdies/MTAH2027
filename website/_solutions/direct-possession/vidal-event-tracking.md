---
title: "Rule-based event detection (Vidal-Codina et al.)"
kicker: "Direct possession"
summary: "Passes, shots and receptions recovered from tracking by physical rules: who is close enough to the ball, when its motion changes, when it leaves play."
group: direct-possession
order: 40
chips: ["Tracking", "Ball-dependent", "Rule-based", "Paper only"]
motif: spikes
motif_caption: "Gains and losses of the ball, read off the tracking, become a timeline of football events."
motif_labels: ["Pass", "Shot", "Out of play"]
facts:
  - { k: "Modality", v: "Tracking with a tracked ball" }
  - { k: "Output", v: "Ball interactions and event times" }
  - { k: "Evidence", v: "Sports Engineering (2022); 90%+ detection in most categories" }
  - { k: "Code and weights", v: "Method described in the paper; nothing to train" }
  - { k: "Licence", v: "Not applicable: no released code" }
verdict: { label: "Our read", text: "Proof that tracking contains its own event data. Sharp where the ball is tracked, mute where it is not." }
sources:
  - { title: "Automatic event detection in football using tracking data (Sports Engineering, 2022)", url: "https://doi.org/10.1007/s12283-022-00381-6" }
related:
  - /solutions/direct-possession/metrica-baseline/
  - /solutions/physics-and-features/ruptures/
  - /solutions/events-and-replay/sn-spotting/
---
Event data is normally typed by people watching video, which limits how many competitions have it. Vidal-Codina and colleagues show how much of it is already written in the tracking. Their algorithm is deterministic, a decision tree of rules with no learning in it.

It works in two steps. The possession step decides, for each frame, which player has the ball. It also recognises the player configurations of stoppages, which is how set pieces are found. The event step then reads changes of possession through the laws of the game. The ball moving from one player to a team-mate is a pass. The ball moving to an opponent is a turnover. A restart is classified by where the players and the ball stand when play resumes.

The authors benchmark the generated events against manually annotated ones, across tournaments and tracking providers, and report detection above 90% in most event categories. The output is an event stream on the tracking clock, produced by rules a coach can read.

## Where it wins

- Fully interpretable. Every event traces to a distance, a speed or a change of direction.
- No labels and no training, so it moves between providers once thresholds are set.
- Its timestamps come from the tracking clock. Events and positions are aligned by construction.
- It defines control at the level of a touch, which is the granularity at which possession changes.

## What it costs

- Everything hangs on the ball. No ball track means no control decisions and no events.
- Thresholds encode a tracking quality. Jittery ball positions trigger phantom touches.
- Events are sparse. Between two touches the method is silent, and filling that silence is the possession problem.
- Aerial balls and crowded duels stay ambiguous in two dimensions.

## How it plugs into possession

Events are the skeleton of possession. Every change of possession is an event, though not every event is a change. A rule cascade like this gives a decoder its sharpest evidence: the frame where control starts. The decoder adds the state between events and a principled way to ignore a touch that changes nothing.

Our evidence decoder uses the same physical logic for its control term, a player within 1.5 m of the ball and closer than any opponent, and leaves the sequence to the decode, which also holds possession where the ball is untracked ([When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }})). [Change-point detection]({{ '/solutions/physics-and-features/ruptures/' | relative_url }}) on ball kinematics is the label-free way to find the same touches without hand-set rules.
