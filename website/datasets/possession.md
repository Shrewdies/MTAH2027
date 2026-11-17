---
layout: wiki-hub
title: Frame-level possession labels
permalink: /datasets/possession/
collection_index: datasets
only_group: possession
family: true
parent: /datasets/
nav_exclude: true
kicker: Datasets family
summary: "The scarce resource. Three releases put a possession field on the tracking itself, frame for frame. Only one labels home, away and dead ball under an open licence."
motif: ds-aligned
icon: ribbon
motif_caption: "The answer on the same clock as the evidence. That alignment is what makes a dataset a judge."
motif_labels: ["Tracking, 25 Hz", Possession label, Home, Away, Dead ball]
stats:
  - { value: "{count}", label: datasets with possession on the tracking }
  - { value: "81", label: matches between them }
  - { value: "7", label: "open matches with all three states" }
---

## What this family is

The only data where the answer is in the file. A possession field sits on the tracking, frame for frame, so a model's output can be laid against it and scored. Every other family on this site gets near possession. These three get to it.

That is why the family is small. Labelling possession on every frame of a match is expensive, the definition is a provider's own, and the footage behind it is rarely free. Three public releases exist. They do not agree with each other, and that disagreement is the first thing to understand.

{% include wiki/motif.html id="ds-providers" labels="DFL|Gradient Sports|SkillCorner|Home|Away|Dead ball" caption="One passage of play, three grammars (illustrative). Boundaries move with the definition, and one provider has no dead-ball state at all." %}

## Three providers, three grammars

| Dataset | What the label says | Dead ball | Tracking behind it |
|---|---|---|---|
| [DFL IDSSE]({{ '/datasets/dfl-idsse/' | relative_url }}) | Team and ball status | Explicit | Official league tracking, 25 Hz |
| [Gradient Sports]({{ '/datasets/gradient-world-cup-2022/' | relative_url }}) | Owning team and ball state | Explicit | Broadcast-derived |
| [SkillCorner]({{ '/datasets/skillcorner-opendata/' | relative_url }}) | A possession field | Not labelled | Broadcast-derived, about 10 Hz |

{% include wiki/motif.html id="ds-coverage" caption="Scale and completeness pull apart. The largest release comes by request, the open one has seven matches, and one of the three has no dead-ball state at all." %}

## How to choose

| You need | Use | Because |
|---|---|---|
| A verdict on a method | DFL IDSSE | Three states, official data, CC BY 4.0. Anyone can rescore it |
| Breadth for a sequence model | Gradient Sports | 64 matches of tournament football in one schema |
| To study missing evidence | SkillCorner | Every position says whether it was seen or extrapolated |

Judge on one provider, learn on another. A model that only agrees with the labels it grew up on has learned a vendor, not the game.

{% include wiki/motif.html id="ds-mask" labels="Detected|Extrapolated|Camera view" caption="Two of the three are tracked from the broadcast. Outside the camera view, positions are extrapolated. SkillCorner says which is which." %}

## The traps

- **Semantics.** Possession is each provider's definition. Mapping it to home, away and dead ball is a modelling decision. Make it per provider and keep it in the open.
- **Dead ball is where they differ most.** SkillCorner labels who, never whether the ball is alive. A gap between phases is not a stoppage.
- **Frame rate.** 10 Hz hides short touches that 25 Hz shows. Upsampling invents precision.
- **Camera type.** Broadcast-derived tracks include players the camera never saw. Do not pool them with league tracking without a provider flag.
- **Licences.** Only DFL is CC BY 4.0. Gradient comes by request under publisher terms. SkillCorner's MIT licence is on the repository.
- **Leakage.** Gradient and SoccerNet-GAR are cut from the same 64 matches. Split by match across both.

## What it cannot do

It cannot make providers stop mattering. Eighty-one matches across three definitions is not a corpus you can pour into one loss function. And none of the three ships video or tactical tags, so the family tests the tracking half of a pipeline only.

## Where it meets our decoder

This family chose our submission. The competition rules forbid tuning on the match's own answers, so the decision had to be made elsewhere, on labels we did not make, and DFL was the only open data with all three states.

We damaged a clean DFL match until it looked like the competition feed, with the ball hidden in bursts on 41% of frames and 0.15 m of position noise, and let it choose between the decoder's parameter profiles. Nothing was trained on it. The decoder has no trained weights.

The scores are on the [DFL IDSSE]({{ '/datasets/dfl-idsse/' | relative_url }}) page. How the search ran is on [the Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}).
