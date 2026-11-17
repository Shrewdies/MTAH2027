---
layout: wiki-entry
nav_exclude: true
title: What possession means, frame by frame
kicker: The problem
summary: "One label for every frame of a full match: home, away or dead. The definition is about control, and control is a property of a sequence, not of a single frame."
route_label: Possession
hook: "Control, not proximity"
group: problem
order: 10
chips: [H / A / D, 25 fps, Control not proximity]
motif: ribbon
motif_caption: Frame-level guesses flicker. Possession, as the challenge defines it, holds until the other side takes control.
motif_labels: [Per-frame guess, Decoded possession, Home, Away, Dead ball]
facts:
  - { k: Frames, v: "199,319 at 25 fps" }
  - { k: Graded, v: "158,857 across two halves" }
  - { k: States, v: "H home, A away, D dead ball" }
  - { k: Ranked on, v: "spellF1, then macroF1" }
verdict:
  label: Our read
  text: "The task is not ball detection and not event detection. It is the reconstruction of a referee-grade possession timeline from evidence that is missing exactly when it matters."
sources:
  - { title: "CHALLENGE (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/CHALLENGE.md" }
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "EVALUATION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "SUBMISSION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/SUBMISSION.md" }
related:
  - /challenges/temporal-decoding/
  - /challenges/spellf1-and-macrof1/
  - /challenges/tracking-errors/
---
## The question

Every 1/25 of a second, for a whole match: who has the ball? The answer is one of three states. **H**: the home team is in possession. **A**: the away team is. **D**: the ball is dead. A fourth symbol, `X`, lets a submission abstain; it is never a true state.

The reference answer is derived mechanically from corrected tracking: is the ball live, and which team controls it. Nothing else is scored. Player names, an event log and better detections are all optional means to that one sequence.

## Possession is control, and control persists

The definition carries three football rules that a frame-level classifier breaks at once.

- **A pass in flight belongs to the passer.** The ball can be 30 metres from the nearest team-mate and two metres from an opponent; possession has not moved.
- **A touch is not a turnover.** A challenge, a deflection or a ball flashing past a defender changes nothing. Possession moves when the other side establishes control.
- **Dead is dead, whoever restarts.** A throw-in about to be taken by the home side is `D`, not `H`. Two home possessions separated by a stoppage are two possessions.

Each rule says the same thing: the label of a frame depends on what happened before it and what happens after it.

The organisers' own baseline shows the cost of ignoring that. Nearest player to the ball, frame by frame, scores 0.65 on frames and 0.05 on possessions. The numbers are on [spellF1 and macroF1]({{ '/challenges/spellf1-and-macrof1/' | relative_url }}), and the full list of tempting shortcuts is the [failure map]({{ '/challenges/glossary/' | relative_url }}).

## One passage, seven labels

| Moment | Label | Why |
|---|---|---|
| A home centre-back plays a pass forward | H | Home is in control |
| The pass is in flight, an away midfielder nearest to it | H | A pass in flight belongs to the passer |
| The midfielder gets a toe to it and it runs on to a home player | H | A touch is not a turnover |
| An away defender wins the next ball and brings it under control | A | Control has changed hands |
| His clearance goes out for a throw-in | D | The ball is out of play |
| A home player stands over the throw | D | Dead is dead, whoever restarts |
| The throw is taken | H | A new home possession, separate from the first |

Seven moments, three home labels that belong to two different possessions, and one frame-level trap in every row but the first.

## What the format demands

A submission is exactly two columns, `frame,label`, for frames 0 to 199,318 in order. Only the 158,857 frames inside the two halves are graded; everything outside them is not. One file, fully determined by code: the organisers regenerate it themselves.


## How we read it

We treat each frame as evidence for three hypotheses and let an exact decoder write the single most coherent sequence for each half. An untracked ball is evidence of nothing, so the story continues. Why the problem has that shape is on [temporal decoding]({{ '/challenges/temporal-decoding/' | relative_url }}). What the missing ball does to a model is on [the ball goes missing]({{ '/challenges/tracking-errors/' | relative_url }}). The system itself is [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}).
