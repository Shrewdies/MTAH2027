---
title: Initial Challenge
order: 1
status: Done
summary: "Who has the ball? Every frame of a full match labelled home possession, away possession or dead ball, from automatic tracking and tactical tags, with no training on the match."
canvas: true
extra_css: [/assets/wiki/wiki.css, /assets/wiki/ch-route.css]
extra_js: [/assets/wiki/ch-route.js]
code_url: https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge
report_url: https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/report/the-shrewdies-technical-report.pdf
---
<ul class="facts" role="list">
  <li class="glass"><span class="facts__value">199,319</span><span class="facts__label">frames labelled H / A / D</span></li>
  <li class="glass"><span class="facts__value">&lt; 10 s</span><span class="facts__label">full match on a laptop CPU</span></li>
  <li class="glass"><span class="facts__value">0</span><span class="facts__label">hand labels, anywhere</span></li>
  <li class="glass"><span class="facts__value">15</span><span class="facts__label">behaviour tests</span></li>
</ul>

<section class="canvas__block" aria-labelledby="ic-motion">
  <p class="kicker"><span class="kicker__num">A</span>In motion</p>
  <h2 id="ic-motion" class="canvas__title">The idea, animated</h2>
  <div class="glass showcase">
    {% include motion.html src="/assets/hero/hero.svg" ratio="16 / 10" caption="Evidence in, one coherent possession sequence out." alt="Animated synthetic play labelled frame by frame: control within 1.5 m, a touch that does not change possession, an interception that does, the ball lost by the tracker while possession is held, the ball going out, and the throw-in restart." fallback="The animation will appear here once it is added." %}
  </div>
</section>

<section class="canvas__block" aria-labelledby="ic-ask">
  <p class="kicker"><span class="kicker__num">B</span>What was asked</p>
  <h2 id="ic-ask" class="canvas__title">One label per frame</h2>
  <div class="paper ask">
    <div>
      <p>For each of the 199,319 frames of one match's tactical video, say who has the ball. Two official metrics grade the answer: <strong>spellF1</strong>, the ranking metric, scores whole possessions; <strong>macroF1</strong> scores every frame.</p>
      <p>Possession is control, and control persists: a pass in flight belongs to the passer, and a touch is not a turnover. Every label depends on the frames around it.</p>
      <p>The catch: the ball is untracked on 41% of graded frames, so a missing ball has to count as <em>no evidence</em>, not as a stoppage.</p>
    </div>
    <ul class="hda" role="list">
      <li class="is-h"><b aria-hidden="true">H</b>Home team in possession</li>
      <li class="is-a"><b aria-hidden="true">A</b>Away team in possession</li>
      <li class="is-d"><b aria-hidden="true">D</b>Ball dead</li>
    </ul>
  </div>
</section>

{% include ch-reading-route.html id="ic-route" num="C" kicker="How we read the problem" %}

<section class="canvas__block" aria-labelledby="ic-steps">
  <p class="kicker"><span class="kicker__num">D</span>Method</p>
  <h2 id="ic-steps" class="canvas__title">Three moves, no training</h2>
  <ol class="steps" role="list">
    <li class="glass step">
      <span class="step__num" aria-hidden="true">01</span>
      <h3 class="step__title">Evidence</h3>
      <p>Per frame: a player within 1.5&nbsp;m of the ball and closer than any opponent, ball out of play, collective stillness, restart windows from Smart Tagging, and calibrated team signals from every tag code.</p>
    </li>
    <li class="glass step">
      <span class="step__num" aria-hidden="true">02</span>
      <h3 class="step__title">Decode</h3>
      <p>An exact Viterbi pass per half over three states (H, A, D), with a cost for every change of state. One noisy frame cannot flip possession; a reception and a touch can.</p>
    </li>
    <li class="glass step">
      <span class="step__num" aria-hidden="true">03</span>
      <h3 class="step__title">Choose</h3>
      <p>Parameters come from a Pareto front of spellF1 and macroF1 on simulated matches with known answers. The submitted profile was picked on a real, externally labelled Bundesliga match.</p>
    </li>
  </ol>
</section>

<section class="canvas__block" aria-labelledby="ic-results">
  <p class="kicker"><span class="kicker__num">E</span>External validation</p>
  <h2 id="ic-results" class="canvas__title">Tested on labels we did not make</h2>
  <div class="glass results-panel">
    {% include results-table.html %}
    <p class="band__note">Open DFL/IDSSE data (Bassek et al. 2025, CC-BY 4.0), scored with the official, unchanged metric. There is no Smart Tagging for DFL, so this measures the tracking part of the pipeline.</p>
    <p class="band__note">Read the last column too. The baseline method reports 570 possessions where the match has 402: it invents turnovers. We report 249: turnovers hidden in long tracking gaps arrive late, and that gap is what the <a href="{{ '/challenges/roadmap/' | relative_url }}">roadmap</a> goes after.</p>
  </div>
</section>

<section class="paper get-code" aria-labelledby="ic-code">
  <div>
    <p class="kicker"><span class="kicker__num">F</span>Go deeper</p>
    <h2 id="ic-code">Code and report</h2>
    <p>Reproduce the submission with Docker in under ten seconds, read the full reasoning, trials and limitations in the technical report, or walk the design call by call in the architecture study.</p>
  </div>
  <div class="actions">
    <a class="button" href="{{ page.code_url }}">Code on GitHub <span class="button__arrow" aria-hidden="true">&rarr;</span></a>
    <a class="button button--ghost" href="{{ page.report_url }}">Technical report (PDF)</a>
    <a class="button button--ghost" href="{{ '/architecture/the-shrewdies-decoder/' | relative_url }}">The architecture</a>
    <a class="button button--ghost" href="{{ '/challenges/roadmap/' | relative_url }}">Roadmap</a>
  </div>
</section>
