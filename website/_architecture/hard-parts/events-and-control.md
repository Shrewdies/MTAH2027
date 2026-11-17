---
title: Events are not possession
kicker: The hard parts
summary: "Events and tags are sparse moments. Possession is a state on every frame, including all the frames between them. What a touch, a header or a tagged phase is allowed to change, and how much it should weigh."
group: hard-parts
order: 60
chips: [Events, Tactical tags, Sparse to dense, Fielded]
motif: bp-events
icon: spikes
motif_caption: "Six events drop onto a continuous possession strip. Three change its colour. Three do not. And a spotter that is right to the second is still fifty frames wide."
facts:
  - { k: Events, v: "Sparse: pass, header, tackle, out, restart" }
  - { k: Possession, v: "Dense: one state on every frame" }
  - { k: Design choice, v: "Hard boundary, transition cue, or weighted evidence" }
  - { k: Timing gap, v: "One second is 25 frames at 25 fps" }
verdict:
  label: Our read
  text: "Use events to propose boundaries and let control evidence confirm them. A spotter accurate to a second cannot place a turnover to the frame."
call:
  title: Why the tags calibrate themselves
  constraint: Data reality and competition rules
  text: "The tags are automatic, and the team a code names is the side on the ball for some codes and the side off it for others. With no answers to tune on, the pipeline measures how often each code's team agrees with visible ball control and turns that into a weight. Build up lands at +1.86, its defending mirror at -1.86, and tags stay a light hint beside ball control."
sources:
  - { title: "More Than a Hack 2027: the data", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "T-DEED for team ball action spotting", url: "https://github.com/hoangqnguyen/bas25-tdeed" }
  - { title: "FOOTPASS: play-by-play action spotting", url: "https://github.com/JeremieOchin/FOOTPASS" }
  - { title: "Vidal-Codina et al. (2022), automatic event detection from tracking data", url: "https://doi.org/10.1007/s12283-022-00381-6" }
  - { title: "Technical report: Who has the ball?", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/TECHNICAL.md" }
related:
  - /architecture/live-dead/
  - /architecture/the-shrewdies-decoder/
  - /challenges/smart-tagging/
  - /solutions/events-and-replay/team-tdeed/
  - /solutions/events-and-replay/footpass/
  - /solutions/direct-possession/vidal-event-tracking/
---

## The design question

How should a sparse signal inform a dense one? Event spotting produces moments. Possession inference owes
a state to every frame. The design has to say what an event is allowed to change. What the supplied tags
are is described in [Tags are context, not events]({{ '/challenges/smart-tagging/' | relative_url }}).

## What each signal proves

| Signal | Proves | Cannot prove |
|---|---|---|
| A detected touch | Contact near this instant | That control changed hands |
| A header or tackle | A contest took place | Who came out with the ball |
| Ball out, restart | A stoppage boundary nearby | Its exact first and last frame |
| A tactical phase tag | The shape of play around now | Which frame it began |
| A set-piece tag | A restart is coming | How long the ball was dead |

## Three ways to use them

| Use | How | Costs |
|---|---|---|
| Hard boundaries | Cut the sequence at each event | Every false event splits a possession |
| Transition cues | Lower the decoder's switch cost near an event | Needs a timing window |
| Weighted evidence | Add a small score for the implied state | Weights must be earned, not guessed |

{% include wiki/motif.html id="bp-s-event-use" caption="One false event, a deflection inside a home possession, used three ways. As a hard boundary it cuts the possession in two. As a transition cue or a small vote, it changes nothing unless the evidence agrees." %}

Whichever is used, a tag that names a team is evidence about the team only. Why it must stay out of the
alive-or-dead question is the subject of [Alive or dead, then who]({{ '/architecture/live-dead/' | relative_url }}).

## Tags name a team, not an owner

A phase tag that names a team does not say that team has the ball. "Build up" names the side in
possession. A defending phase names the side without it. The safe design measures what each code means
against something observable before giving it a vote.

## What breaks it in real football

- **A headed clearance to nobody.** The contest is real and the next controlled touch is seconds away.
- **Overlapping phases.** Transition and build-up are tagged at once, for opposite teams.

## How to judge it

Measure boundary error in frames, never in seconds. Count how many events changed the decoded possession
and how many of those changes were right. Then switch the event evidence off: if both official metrics
hold, the events were decoration.
