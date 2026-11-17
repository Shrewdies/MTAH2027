---
layout: member-read
title: Seeing the ball nobody can see
permalink: /team/why-our-specialization-matters/perception-under-occlusion/
nav_exclude: true
why_order: 2
art: occlusion
members: [3, 4]
summary: Self-driving cars never assume a hidden pedestrian has vanished. A possession model owes the same habit to a ball lost in a crowd.
extra_css: [/assets/members/member.css, /assets/members/why.css]
---

In our Initial Challenge the ball was invisible on 41% of graded frames. Tracking data has gaps, and the
gaps are not random: the ball disappears in crowds, in the air and at exactly the moments that decide
possession.

Self-driving cars face the same problem every second. A pedestrian steps behind a parked van; the car must
keep a belief about where that person is, how fast they move and when they could reappear. Autonomous
perception handles this with tracking filters, motion models and explicit uncertainty, rather than
pretending the object vanished.

Ahmed's experience with self-driving systems brings that mindset to football. A ball that cannot be seen
still obeys physics, and it is usually at somebody's feet. Player positions, velocities and the shape of
the play constrain where it can be.

Treating missing frames as a prediction problem with a confidence attached, rather than as empty rows,
could turn the hardest stretches of a match into some of the most informative. It also keeps the model
honest: when it is guessing, it should say how much.

The rule we take from the road: never confuse *not observed* with *not there*. In our Initial Challenge
decoder that rule is architecture. A missing ball is no evidence, so possession stays with the last team
in control until real evidence arrives. The architecture study
[When the ball goes missing]({{ '/architecture/ball-aware-vs-ball-free/' | relative_url }}) sets out the
design choice, and [Solutions]({{ '/solutions/' | relative_url }}) maps the models that go further and
infer the ball from the players.
