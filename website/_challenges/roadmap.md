---
title: Roadmap
order: 2
status: In development
summary: "Where The Shrewdies stand, and what is already being built for the Innovative Challenge. The brief decides the target. These are the engines warming up."
canvas: true
report_url: https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/report/the-shrewdies-technical-report.pdf
---
<ul class="facts" role="list">
  <li class="glass"><span class="facts__value">5</span><span class="facts__label">pieces shipped</span></li>
  <li class="glass"><span class="facts__value">4</span><span class="facts__label">engines in development</span></li>
  <li class="glass"><span class="facts__value">3</span><span class="facts__label">on the horizon</span></li>
  <li class="glass"><span class="facts__value">1</span><span class="facts__label">laptop, offline, for all of it</span></li>
</ul>

<section class="canvas__block" aria-labelledby="rm-route">
  <p class="kicker"><span class="kicker__num">A</span>The route</p>
  <h2 id="rm-route" class="canvas__title">From a decoder to match intelligence</h2>
  <div class="glass showcase">
    {% include wiki/motifs/ch-roadmap.html %}
  </div>
</section>

<section class="canvas__block" aria-labelledby="rm-shipped">
  <p class="kicker"><span class="kicker__num">B</span>Shipped</p>
  <h2 id="rm-shipped" class="canvas__title">On the pitch</h2>
  <p class="band__lede">Built, measured and public.</p>
  <ol class="card-grid" role="list">
    <li class="card">
      <span class="card__num" aria-hidden="true">01</span>
      <h3 class="card__title"><a href="{{ '/challenges/initial-challenge/' | relative_url }}">Evidence decoder</a></h3>
      <p class="card__text">Football evidence on every frame, one exact Viterbi decode per half. CPU-only, deterministic, a full match in under 10 seconds.</p>
      <span class="status status--done">Shipped</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">02</span>
      <h3 class="card__title"><a href="{{ '/challenges/initial-challenge/' | relative_url }}#ic-results">External validation</a></h3>
      <p class="card__text">Chosen and measured on open labels we did not make: spellF1 0.340 and macroF1 0.693, against 0.235 and 0.383 for the organisers' baseline method.</p>
      <span class="status status--done">Shipped</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">03</span>
      <h3 class="card__title"><a href="{{ '/on-device/reproducibility/' | relative_url }}">One-command reproduction</a></h3>
      <p class="card__text">A container pinned by digest, the network switched off, and the same bytes out on every run.</p>
      <span class="status status--done">Shipped</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">04</span>
      <h3 class="card__title"><a href="{{ page.report_url }}">Technical report</a></h3>
      <p class="card__text">The full reasoning in one document: the evidence, the decoder, the Pareto decision log and what real labels taught us.</p>
      <span class="status status--done">Shipped</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">05</span>
      <h3 class="card__title"><a href="{{ '/' | relative_url }}#explore-title">Knowledge hub</a></h3>
      <p class="card__text">The Datasets atlas, the Solutions landscape, Architecture and On-device: the field of football AI, mapped and judged.</p>
      <span class="status status--done">Shipped</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
  </ol>
</section>

<section class="canvas__block" aria-labelledby="rm-dev">
  <p class="kicker"><span class="kicker__num">C</span>In development</p>
  <h2 id="rm-dev" class="canvas__title">Engines warming up</h2>
  <p class="band__lede">Four builds, each aimed at a gap we have measured.</p>
  <ol class="card-grid" role="list">
    <li class="card">
      <span class="card__num" aria-hidden="true">01</span>
      <h3 class="card__title"><a href="{{ '/architecture/single-source-of-truth/' | relative_url }}">The hidden ball</a></h3>
      <p class="card__text">The ball is untracked on 41% of graded frames. We carry possession through those gaps with ball-free reasoning over the players and a single source of truth: one match state where video and both trackings fill each other's gaps.</p>
      <span class="status status--in-the-making">In development</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">02</span>
      <h3 class="card__title"><a href="{{ '/on-device/' | relative_url }}">On-device vision</a></h3>
      <p class="card__text">A light ball detector that looks only where the tracker went blind, running on the laptop's NPU. No frame leaves the machine.</p>
      <span class="status status--in-the-making">In development</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">03</span>
      <h3 class="card__title"><a href="{{ '/datasets/dfl-idsse/' | relative_url }}">Learned evidence</a></h3>
      <p class="card__text">Hand-set evidence weights give way to models fitted on the seven open DFL matches, tested leave-one-match-out.</p>
      <span class="status status--in-the-making">In development</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">04</span>
      <h3 class="card__title"><a href="{{ '/challenges/temporal-decoding/' | relative_url }}">Duration-aware decoding</a></h3>
      <p class="card__text">We find 249 possessions where the external match has 402. A decoder that models how long possessions last goes after the short ones.</p>
      <span class="status status--in-the-making">In development</span>
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
  </ol>
</section>

<section class="canvas__block" aria-labelledby="rm-horizon">
  <p class="kicker"><span class="kicker__num">D</span>On the horizon</p>
  <h2 id="rm-horizon" class="canvas__title">Next in line</h2>
  <p class="band__lede">Where a possession sequence turns into something a coach can use.</p>
  <ol class="card-grid" role="list">
    <li class="card">
      <span class="card__num" aria-hidden="true">01</span>
      <h3 class="card__title">Confidence and provenance</h3>
      <p class="card__text">Every frame carries how sure the decoder is and what decided it: seen, inferred or held.</p>
      <span class="status status--coming">Horizon</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">02</span>
      <h3 class="card__title">From labels to language</h3>
      <p class="card__text">Local language models turning possession sequences into tactical narration, on the laptop.</p>
      <span class="status status--coming">Horizon</span>
    </li>
    <li class="card">
      <span class="card__num" aria-hidden="true">03</span>
      <h3 class="card__title">Interactive match timelines</h3>
      <p class="card__text">The whole match as a possession timeline to scrub, filter and question.</p>
      <span class="status status--coming">Horizon</span>
    </li>
  </ol>
</section>

<section class="paper get-code" aria-labelledby="rm-next">
  <div>
    <p class="kicker"><span class="kicker__num">E</span>What happens next</p>
    <h2 id="rm-next">The brief picks the target</h2>
    <p>The Innovative Challenge brief decides where all of this points. The decoder is on the pitch, the gaps are measured, and the engines are already running.</p>
  </div>
  <div class="actions">
    <a class="button" href="{{ '/challenges/innovative-challenge/' | relative_url }}">Innovative Challenge <span class="button__arrow" aria-hidden="true">&rarr;</span></a>
    <a class="button button--ghost" href="{{ '/challenges/' | relative_url }}">How we read the problem</a>
  </div>
</section>
