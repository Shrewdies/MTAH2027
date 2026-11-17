---
layout: member-read
title: From autonomous networks to self-running analysis
permalink: /team/why-our-specialization-matters/self-running-analysis/
nav_exclude: true
why_order: 5
art: loop
members: [4, 2]
summary: Telecom networks are learning to observe, decide, act and verify on their own. A season of football data needs the same closed loop.
extra_css: [/assets/members/member.css, /assets/members/why.css]
---

Telecom operators are moving towards autonomous networks: systems that monitor themselves, detect
degradation, diagnose the cause and apply a fix, with people setting goals instead of turning knobs. The
pattern is a closed loop of observe, decide, act and verify, wrapped in guardrails.

Football analysis needs the same loop. A season of matches is a stream: new tracking files, new event
feeds, new competitions with slightly different conventions. Much of that is still checked by hand. A
self-running analysis pipeline could validate each match on arrival, flag missing or implausible data,
choose the right processing path, rerun only what changed and report what it could not trust.

Abdullah's work in AI solutions architecture for autonomous networks, and Mahmoud's DevOps practice, map
directly onto that design. The lessons from networks carry over: make every automated action observable,
keep a human approval step for anything irreversible, and measure the loop itself, not only the model
inside it.

A loop can only report what it cannot trust if every value knows where it came from. That is a design
decision, made early. The architecture study
[Confidence and provenance]({{ '/architecture/confidence-and-provenance/' | relative_url }}) sets out the
three kinds of doubt a pipeline has to carry, and
[Architecture, the multiplier]({{ '/team/why-our-specialization-matters/architecture-the-multiplier/' | relative_url }})
explains why the loop is drawn before it is built.

The aim is not to remove the analyst. It is to spend the analyst's time on football, not on file formats.
