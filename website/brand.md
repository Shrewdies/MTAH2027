---
title: Brand
kicker: Brand system
permalink: /brand/
summary: "Floodlit Blaugrana: Barça blue flowing into violet and garnet, lit by lime. The colours, type, logo and motion shared by this site, the reports and the slides."
---

The full guide is `assets/brand/BRAND.md` in the repository. This page is the quick visual reference.

## The logo

The wordmark is the logo. It appears large in every header, huge on the home page and again in the footer, always animated. There is no separate symbol.

<div class="brand-logo">
  <span class="brand-logo__art" aria-hidden="true">{% include logo.html variant="hero" %}</span>
  <span class="brand-logo__art brand-logo__art--small" aria-hidden="true">{% include logo.html variant="footer" %}</span>
</div>

## Palette

<ul class="swatches" role="list">
  <li class="swatch"><div class="swatch__chip" style="--c:#004D98"></div><div class="swatch__meta">Blaugrana blue<code>--sh-blue #004D98</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#2F86F0"></div><div class="swatch__meta">Floodlit blue<code>--sh-blue-bright #2F86F0</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#6E4C9F"></div><div class="swatch__meta">Violet<code>--sh-violet #6E4C9F</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#A50044"></div><div class="swatch__meta">Garnet<code>--sh-garnet #A50044</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#E5336F"></div><div class="swatch__meta">Floodlit garnet<code>--sh-garnet-bright #E5336F</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#B9A2D8"></div><div class="swatch__meta">Mauve light<code>--sh-mauve #B9A2D8</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#C4F000"></div><div class="swatch__meta">Lime, the hype<code>--sh-lime #C4F000</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#E9EDF5"></div><div class="swatch__meta">Silver shine<code>--sh-silver #E9EDF5</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#B8C2D3"></div><div class="swatch__meta">Silver<code>--sh-silver-2 #B8C2D3</code></div></li>
  <li class="swatch"><div class="swatch__chip" style="--c:#0A1F44"></div><div class="swatch__meta">Navy, sparingly<code>--sh-navy #0A1F44</code></div></li>
</ul>

<div class="gradient-strip" style="background: linear-gradient(150deg, #0F63C4 0%, #004D98 24%, #4D44A6 50%, #7E3F98 70%, #A50044 100%)"></div>
<p><code>--sh-grad-floodlit</code>: the stage behind every page.</p>
<div class="gradient-strip" style="background: linear-gradient(90deg, #004D98 0 33%, #C4F000 33% 67%, #A50044 67% 100%); height: 1rem"></div>
<p><code>--sh-grad-tricolour</code>: edges, rules and the footer band.</p>

Possession states keep their colours everywhere: home `H` in Blaugrana blue, away `A` in garnet, dead ball `D` in ink `#3A4372`.

## Rules

- **Bright, never black.** The page is a floodlit gradient. Navy is the deepest tone and only appears in small doses.
- **Lime is the hype.** Use it generously for glows, strokes, highlights, CTAs and motion trails. On white it is a fill or highlight, never text.
- **Text sits on glass or paper.** Long text goes on a translucent navy glass panel (light text) or a bright paper card (navy text), so it always meets WCAG AA.
- **Colour only.** Club colours are referenced as colour. No crests, trademarks or real kit replicas.

## Type

- **Big Shoulders Display**, 800 to 900, uppercase: headlines, numbers.
- **Manrope**, 400 to 800: body text and interface.
- **JetBrains Mono**, 400 and 600: labels, kickers, figures in tables, code.

## Motion

Every page plays on an animated stage: a drifting gradient mesh, floodlight beams, pitch lines that draw themselves in, a bouncing ball with squash and stretch, drifting boots with stud marks and lime trails. It pauses when the tab is hidden, can be paused with the button in the corner, and holds still for visitors who prefer reduced motion.

<div class="art-grid">
  <figure><img src="{{ '/assets/brand/motif-ball.svg' | relative_url }}" alt="Abstract ball: silver sphere with lime, blue and garnet swirls"><figcaption><code>motif-ball.svg</code>, the bouncing ball</figcaption></figure>
  <figure><img src="{{ '/assets/brand/motif-boot.svg' | relative_url }}" alt="Abstract football boot in silver with a lime sole and seam"><figcaption><code>motif-boot.svg</code>, the drifting boot</figcaption></figure>
</div>
