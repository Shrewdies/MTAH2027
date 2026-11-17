---
layout: member-read
title: The analyst's eye is the ground truth
permalink: /team/why-our-specialization-matters/the-analysts-eye/
nav_exclude: true
why_order: 1
art: eye
members: [1]
summary: Every football model learns somebody's definition of what happened. A professional analyst at both ends of the pipeline keeps that definition honest.
extra_css: [/assets/members/member.css, /assets/members/why.css]
---

Every football model is trained on somebody's definition of what happened. A pass, a press, a turnover,
a phase of play: each label is a judgement before it is a number.

If the judgement is wrong, the model learns the error faithfully and repeats it at scale. No amount of
tuning recovers a concept that was defined badly in the first place. Our
[Datasets]({{ '/datasets/' | relative_url }}) atlas reads every label set with that question: whose
definition of possession does it carry?

That is why a professional analyst sits at the start and at the end of our pipeline. At the start, Yousef
helps define events and states the way a coaching staff would recognise them, which keeps labels
consistent and features meaningful. At the end, he reads the outputs as a coach would. Does this pressing
map match what we saw? Does this possession sequence make sense? Would anyone change a training session
because of it?

This loop catches a class of errors no metric can see. A model can score well on a benchmark and still be
useless, because the benchmark rewards something a coach does not care about. An analyst's review helps
turn *accurate* into *credible*.

The engineering lesson is simple: treat domain review like a test suite. A result is not finished until
it has passed the analyst's eye.
