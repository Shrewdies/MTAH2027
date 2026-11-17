---
layout: member-read
title: Geospatial thinking on a 105 × 68 m map
permalink: /team/why-our-specialization-matters/a-105-by-68-map/
nav_exclude: true
why_order: 3
art: pitch
members: [3, 4]
summary: A pitch is a small map with unusually rich traffic. The tools built for coverage, demand and movement on real maps fit it closely.
extra_css: [/assets/members/member.css, /assets/members/why.css]
---

A football pitch is a small map with unusually rich traffic: twenty-two players and a ball, sampled many
times a second. Geospatial analysis has tools built for exactly this kind of data, and football
analytics often reinvents them.

Coverage maps from network planning resemble pitch-control surfaces: who can reach which point first.
Density estimates become heat maps that respect the touchlines. Questions about where demand concentrates
translate into where a team overloads and where it leaves space. Choosing a new cell site is a cousin of
choosing where a holding midfielder should stand.

Ahmed and Abdullah have spent their careers reasoning about coverage, demand and movement on real maps,
on professional journeys through more than a dozen countries between them. On a 105 by 68 metre pitch the scale changes; the
questions do not. What is reachable, what is congested, and what changes if one point moves?

Thinking in coordinates also helps the engineering. One pitch coordinate system, zone definitions agreed
once and reused everywhere, and spatial indexes for fast queries keep different analyses comparable. That
is the quiet foundation of any football model a coach can trust from one match to the next.

It is also where our own possession decoder starts. Its evidence is geospatial: who can reach the ball, in
metres, and whether the ball has crossed a line. The architecture study
[Geospatial-only inference]({{ '/architecture/geospatial-only/' | relative_url }}) shows what coordinates
alone can carry, and [Datasets]({{ '/datasets/' | relative_url }}) lists the tracking data that makes this
kind of reasoning possible.
