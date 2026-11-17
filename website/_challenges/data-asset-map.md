---
layout: wiki-entry
nav_exclude: true
title: What each data asset contributes
kicker: The data
summary: "Two cameras, one clock that counts. What every provided asset can tell a possession model, and where each one stops."
route_label: Data map
hook: "One clock that counts"
group: data
order: 50
chips: [Tactical, Broadcast, Smart Tagging, Homography]
motif: stack
motif_caption: The tactical layers share one frame index. The broadcast layers sit on their own clock until someone proves the alignment.
motif_labels: [Tactical video, Tracking, Smart Tagging, Broadcast]
facts:
  - { k: Reference clock, v: "Tactical video, 25 fps" }
  - { k: Geometry, v: "Player and ball tracking at 25 Hz" }
  - { k: Context, v: "638 automatic tag intervals" }
  - { k: Cross-camera sync, v: "Not provided" }
verdict:
  label: Our read
  text: "The tactical tracking carries the geometry, the tags carry the restarts, and everything else is corroboration that has to be earned. More sources only help when they are provably about the same moment."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
related:
  - /challenges/tactical-tracking/
  - /challenges/smart-tagging/
  - /challenges/broadcast-and-timebases/
  - /challenges/homography/
---
## The inventory

| Asset | What it contributes | Where it stops |
|---|---|---|
| Tactical video | The reference: 199,319 frames, whole pitch | The ball is tiny in the image |
| Tactical tracking | 25 Hz positions and speeds for players and ball | Ball missing, slots unstable |
| Tactical homography | Pitch-to-image transform for every frame | Planar: no height for an airborne ball |
| Smart Tagging | 638 automatic tactical intervals and restarts | Phases, not a pass-by-pass event log |
| Broadcast video | Close views of feet, contacts and the ball | Cuts, close-ups and replays |
| Broadcast tracking | A second numerical view of players and ball | Its own slots, its own clock |
| Broadcast homography | Ground projection for the broadcast view | Usable on 65.8% of frames |

Each camera's video, tracking and homography are aligned to that camera's own frame index. **No correspondence between the two cameras is provided.**

## What carries the signal

Possession is geometry over time, so the **tactical tracking** is the principal source: who is near the ball, how fast the ball is moving, whether it has left the pitch, whether the players have stopped. Its weakness defines the challenge. The ball is untracked on 41% of graded frames, and a player is a team and a slot, not an identity. See [tactical tracking]({{ '/challenges/tactical-tracking/' | relative_url }}) and [the ball goes missing]({{ '/challenges/tracking-errors/' | relative_url }}).

**Smart Tagging** answers a different question. It marks set pieces and restarts, which is direct evidence about dead ball, and it names a team for tactical phases, which is weak evidence about who has it. See [tags are context, not events]({{ '/challenges/smart-tagging/' | relative_url }}).

The **homography** is the bridge between pitch coordinates and pixels. It is what lets anything seen in the image be placed on the pitch. See [homography]({{ '/challenges/homography/' | relative_url }}).

## More is not automatically better

The broadcast feed sees what the tactical camera cannot: the foot on the ball. It also runs on an edited timeline. A broadcast observation joined to the wrong tactical frame is not a noisy measurement; it is a confident false one, and at 25 frames per second a small offset is enough to invent a turnover.

A unified timeline has to carry its uncertainty: which cross-view matches are verified, which are plausible, which are absent. See [two cameras, two clocks]({{ '/challenges/broadcast-and-timebases/' | relative_url }}).

## What fed our decoder

The evidence decoder reads the tactical tracking and the Smart Tagging intervals, both on the tactical clock. Nothing else is needed to produce the submission, which is why a full match decodes in under 10 seconds on a laptop CPU.

Open data from outside the competition did a different job: choosing parameters. That atlas lives in [Datasets]({{ '/datasets/' | relative_url }}).
