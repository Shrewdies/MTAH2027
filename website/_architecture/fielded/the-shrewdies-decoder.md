---
title: The Shrewdies decoder
kicker: On the pitch
summary: "The architecture we fielded, end to end: football evidence on every frame, an exact Viterbi decode per half, and every parameter chosen away from the match."
group: fielded
order: 1
chips: [Fielded, Geospatial, Viterbi, CPU-only]
motif: bp-decoder-flow
icon: decoder
motif_caption: "Two evidence lanes, kept apart, feed one exact decode per half. The lower lane ran once, away from the match: it explored on simulated matches and let open DFL labels pick the profile."
motif_labels: [Tracking and tags, Alive or dead, Which team, Viterbi per half, H / A / D, Profile]
facts:
  - { k: Output, v: "199,319 frames at 25 fps, each H, A or D" }
  - { k: Runtime, v: "Under 10 s on a laptop CPU" }
  - { k: Determinism, v: "Byte-identical output on every run" }
  - { k: spellF1, v: "0.340 against 0.235 for the organisers' baseline method" }
  - { k: macroF1, v: "0.693 against 0.383, on the same open DFL match" }
verdict:
  label: Our read
  text: "An architecture is proven by what it refuses to do. This one refuses to invent a stoppage when the ball disappears, to let a tag stretch a dead ball, and to choose anything on the match it is graded on."
call:
  title: Why it is deterministic and CPU-only
  constraint: Reproducibility
  text: "The organisers regenerate the submitted file themselves. The decode has no randomness, the dependencies are two pinned libraries, and the container is pinned by digest and runs without a network. The same bytes come out on every run, in under ten seconds."
sources:
  - { title: "Technical report: Who has the ball?", url: "https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/TECHNICAL.md" }
  - { title: "Code: Shrewdies/MTAH2027, initial-challenge", url: "https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge" }
  - { title: "Official evaluation (spellF1, macroF1)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
  - { title: "Bassek et al. (2025), DFL open tracking and event data, Scientific Data 12:195", url: "https://www.nature.com/articles/s41597-025-04505-y" }
  - { title: "Vidal-Codina et al. (2022), automatic event detection from tracking data", url: "https://doi.org/10.1007/s12283-022-00381-6" }
related:
  - /architecture/single-source-of-truth/
  - /architecture/chained-classifier-and-decoder/
  - /architecture/evaluation-framework/
  - /challenges/initial-challenge/
  - /solutions/classifiers-and-decoders/viterbi-algorithm/
  - /on-device/reproducibility/
---

## The architecture in one line

Read the match the way a match official would, then let an exact algorithm write the single most coherent
possession story for each half. Evidence and decision are separate machines, and nothing is tuned on the
match being graded.

| Layer | What it does | The design study behind it |
|---|---|---|
| Observation | Tracking and tactical tags. A missing ball stays missing. | [Geospatial-only inference]({{ '/architecture/geospatial-only/' | relative_url }}) |
| Evidence | Scores home, away and dead on every frame, in two lanes. | [Evidence, then a decoder]({{ '/architecture/chained-classifier-and-decoder/' | relative_url }}) |
| Decision | One exact decode per half over home, away, dead. | [Seven ways to decode a match]({{ '/architecture/decoding-alternatives/' | relative_url }}) |
| Selection | Profiles from a Pareto front, the final one picked on open labels. | [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}) |
| Delivery | Pinned container, no network, read-only inputs, 15 behaviour tests. | [Reproducibility]({{ '/on-device/reproducibility/' | relative_url }}) |

Why each layer looks the way it does, constraint by constraint, is the subject of the
[On the pitch]({{ '/architecture/fielded/' | relative_url }}) family page.

## The evidence, exactly

Every frame scores three hypotheses. Each signal has a physical meaning.

| Signal | Football meaning | Supports |
|---|---|---|
| A player within 1.5 m of a ball moving slower than 7 m/s | Someone can actually play it | That player's team |
| Ball more than 1 m beyond a line | Out of play | Dead |
| Players almost still for 3 s | Play has stopped | Dead |
| Ball placed and motionless for 1.5 s | Free kick, goal kick, kick-off | Dead |
| Start of a tagged set piece | A restart is coming | Dead |
| A fast ball inside the pitch | Play is live | Not dead |
| A team-naming tag code | A hint about which side | That side, weighted |

Three design rules govern how those signals are used. Each has its own study, so each is one line here.

- **A missing ball scores nothing.** Possession stays with the last team in control:
  [When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}).
- **Alive-or-dead and which-team never share evidence.** A tag cannot move the edge of a stoppage, and a unit
  test guarantees it: [Alive or dead, then who]({{ '/architecture/live-dead/' | relative_url }}).
- **Each tag code weighs what it proves.** Its weight is its measured agreement with visible ball control:
  [Events are not possession]({{ '/architecture/events-and-control/' | relative_url }}).

## The decode, exactly

One [Viterbi]({{ '/solutions/classifiers-and-decoders/viterbi-algorithm/' | relative_url }}) pass per half
chooses the sequence that maximises evidence minus a fixed cost for every change of state. The fielded
profile sets the team switch cost at 4.23 and the alive-or-dead switch cost at 9.43.

{% include wiki/motif.html id="bp-s-toll" caption="A change of state is bought only when the evidence for it exceeds the toll. A touch never pays. Sustained control pays after about four frames. A stoppage has to pay the higher toll. The curves are schematic." %}

Seven dials were searched: the two switch costs and five evidence weights. The control radius was not. It
stays at 1.5 m, a physical constant, because a search left free pushed it to a value no footballer would
recognise.

## What it scored

{% include wiki/motif.html id="bp-results" caption="The fielded profile against the organisers' baseline method, on an openly labelled DFL match with the ball hidden on 41% of frames, scored by the official code." %}

The fielded profile wins on both official metrics (the full table is on the
[Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page). The baseline method invents possessions, 570 against a
truth of 402. The decoder errs the other way, 249: turnovers hidden inside long tracking gaps surface
late. The two other frozen profiles scored spellF1 0.249 and 0.286 on the same match, and how the three
were produced and chosen is in [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}).

## What comes next

The architecture has clear seams, and each takes a stronger part without touching the rest. The first is
the hidden ball: [the single source of truth]({{ '/architecture/single-source-of-truth/' | relative_url }})
reconciles the video frames and both tracking feeds into one match state, so fewer frames reach the
decoder silent. The rest of what we are building is on [the roadmap]({{ '/challenges/roadmap/' | relative_url }}).
