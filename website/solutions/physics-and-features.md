---
layout: wiki-hub
title: "Physics and features"
permalink: /solutions/physics-and-features/
collection_index: solutions
only_group: physics-and-features
family: true
parent: /solutions/
nav_exclude: true
kicker: "Solutions family"
summary: "Distances, arrival times, pitch control and filtered trajectories. Label-free evidence that can be read to the last number."
motif: field
motif_caption: "Pitch control, the best-known member: the pitch divided by who would reach each point first."
motif_labels: ["Home arrives first", "Away arrives first"]
stats:
  - { value: "{count}", label: "entries" }
  - { value: "0", label: "need labels" }
  - { value: "0", label: "trained weights to ship" }
---
## One picture: positions become evidence

Tracking gives positions. Possession evidence needs more: who can reach the ball, how fast it is moving, whether its motion has just changed. This family computes those quantities from physics and geometry. Nothing is trained, so nothing needs labels, and every number traces back to a speed, a distance or a time.

The picture above shows the computation at full scale, over the whole pitch. For possession the same computation is needed at one point only: the ball.

{% include wiki/motif.html id="sol-first-there" caption="The standing receiver is closer. The sprinting presser arrives first. Time to intercept gets right what distance gets wrong." %}

In the chain, measuring comes after the data is read and aligned, and before anything decides. Its output is evidence for the last link.

## How to choose inside it

| Entry | Labels | Ball and identities | Compute |
|---|---|---|---|
| [Pitch control]({{ '/solutions/physics-and-features/pitch-control/' | relative_url }}) | None | Ball position for local use. No identities | Light at the ball, heavy on a full grid |
| [Accessible space]({{ '/solutions/physics-and-features/accessible-space/' | relative_url }}) | None | Ball required. Some functions want the team on the ball | Heavier: simulated passes |
| [Kalman filter and RTS smoother]({{ '/solutions/physics-and-features/ball-trajectory-kalman/' | relative_url }}) | None | Ball measurements, gaps allowed | Negligible |
| [ruptures]({{ '/solutions/physics-and-features/ruptures/' | relative_url }}) | None | Any signal: ball speed or team speed | Light |
| [floodlight]({{ '/solutions/physics-and-features/floodlight/' | relative_url }}) | None | Whatever is tracked | Light |
| [unravelsports]({{ '/solutions/physics-and-features/unravelsports/' | relative_url }}) | None for features | One node per player. No identities | Light for features |

Start with distances and speeds. Add time to intercept from pitch control where distance misjudges a sprinting player. Add change-points on ball speed where touches matter.

{% include wiki/motif.html id="sol-smooth-sharp" caption="Raw ball speed places the touch to the frame and adds false ones. Smoothing removes the false ones and blurs the real one into a band. Every filter in this family sits somewhere between the two." %}

## What this family cannot do

- **It cannot name the possessor.** Controlling space is not having the ball. Being closest is not being in control.
- **It cannot make evidence where the sensor made none.** A filter that bridges a long gap draws a plausible path, not a measured one.
- **It cannot be smooth and sharp at once.** Every smoothing choice blurs the touch it was meant to reveal.

## Where our decoder stands

Its evidence is this family's kind of quantity, kept simple on purpose: a player within 1.5 m of the ball and closer than any opponent, the ball out of play, collective stillness of the players. A frame with no ball contributes no ball evidence, and nothing is imputed. The physics stays evidence. The [Viterbi decode]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) makes the decision.
