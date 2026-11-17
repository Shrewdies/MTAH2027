---
title: "Reproducibility"
order: 2
summary: "Same inputs, same bytes. A digest-pinned image, pinned dependencies, frozen parameters and a deterministic decoder: anyone can rebuild our exact output file in three commands."
canvas: true
extra_css: [/assets/ondevice/ondevice.css]
---
<ul class="facts" role="list">
  <li class="glass"><span class="facts__value">&lt; 10 s</span><span class="facts__label">full decode on a laptop CPU</span></li>
  <li class="glass"><span class="facts__value">15</span><span class="facts__label">behaviour tests, no data needed</span></li>
  <li class="glass"><span class="facts__value">~15 s</span><span class="facts__label">to rerun the seeded Pareto search</span></li>
  <li class="glass"><span class="facts__value">2</span><span class="facts__label">architectures: arm64 and amd64</span></li>
</ul>

<section class="canvas__block" aria-labelledby="rep-pipe">
  <p class="kicker"><span class="kicker__num">A</span>In motion</p>
  <h2 id="rep-pipe" class="canvas__title">Clone to identical file</h2>
  <div class="od-stage">
    <ol class="od-pipe" role="list">
      <li style="--i:0">
        <span class="od-node" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="6" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.2"/><circle cx="18" cy="7" r="2.2"/><path d="M6 7.2v9.6M18 9.2c0 4-6 3.5-11 7.8"/></svg></span>
        <span><span class="od-pipe__name">Clone</span><span class="od-pipe__note">public repo, no data</span></span>
      </li>
      <li style="--i:1">
        <span class="od-node" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2.5l8.5 4.7v9.6L12 21.5l-8.5-4.7V7.2z"/><path d="M3.5 7.2L12 12l8.5-4.8M12 12v9.5"/></svg></span>
        <span><span class="od-pipe__name">Build</span><span class="od-pipe__note">digest-pinned image</span></span>
      </li>
      <li style="--i:2">
        <span class="od-node" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 6.5l2 2 3.5-3.5M4 13.5l2 2 3.5-3.5M12.5 7h7.5M12.5 14h7.5M4 20h16"/></svg></span>
        <span><span class="od-pipe__name">Test</span><span class="od-pipe__note">15 behaviour tests</span></span>
      </li>
      <li style="--i:3">
        <span class="od-node" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 4.5v15l12.5-7.5z"/></svg></span>
        <span><span class="od-pipe__name">Run</span><span class="od-pipe__note">offline, under 10 s</span></span>
      </li>
      <li style="--i:4">
        <span class="od-node" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6 2.5h8l5 5v14H6z"/><path d="M14 2.5v5h5"/><path d="M9 14.5l2.2 2.2 4.3-4.6"/></svg></span>
        <span><span class="od-pipe__name">Same file</span><span class="od-pipe__note">validated, byte for byte</span></span>
      </li>
    </ol>
    <div class="od-match">
      <div class="od-file">
        <div class="od-file__head"><b>Run 1</b><span>submission.csv</span></div>
        <div class="od-hash" aria-hidden="true"><i style="--c:#C4F000;--i:0"></i><i style="--c:#2F86F0;--i:1"></i><i style="--c:#B9A2D8;--i:2"></i><i style="--c:#E5336F;--i:3"></i><i style="--c:#E9EDF5;--i:4"></i><i style="--c:#6E4C9F;--i:5"></i><i style="--c:#C4F000;--i:6"></i><i style="--c:#004D98;--i:7"></i><i style="--c:#E5336F;--i:8"></i><i style="--c:#B9A2D8;--i:9"></i><i style="--c:#2F86F0;--i:10"></i><i style="--c:#C4F000;--i:11"></i><i style="--c:#E9EDF5;--i:12"></i><i style="--c:#A50044;--i:13"></i><i style="--c:#6E4C9F;--i:14"></i><i style="--c:#C4F000;--i:15"></i></div>
        <div class="od-file__foot">sha256 fingerprint · LF line endings</div>
      </div>
      <div class="od-eq">
        <span class="od-eq__badge" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></span>
        <span>Match</span>
      </div>
      <div class="od-file">
        <div class="od-file__head"><b>Run 2</b><span>submission.csv</span></div>
        <div class="od-hash" aria-hidden="true"><i style="--c:#C4F000;--i:0"></i><i style="--c:#2F86F0;--i:1"></i><i style="--c:#B9A2D8;--i:2"></i><i style="--c:#E5336F;--i:3"></i><i style="--c:#E9EDF5;--i:4"></i><i style="--c:#6E4C9F;--i:5"></i><i style="--c:#C4F000;--i:6"></i><i style="--c:#004D98;--i:7"></i><i style="--c:#E5336F;--i:8"></i><i style="--c:#B9A2D8;--i:9"></i><i style="--c:#2F86F0;--i:10"></i><i style="--c:#C4F000;--i:11"></i><i style="--c:#E9EDF5;--i:12"></i><i style="--c:#A50044;--i:13"></i><i style="--c:#6E4C9F;--i:14"></i><i style="--c:#C4F000;--i:15"></i></div>
        <div class="od-file__foot">same fingerprint, every run</div>
      </div>
    </div>
  </div>
  <p class="od-caption">Deterministic decoding: the same data gives byte-identical output on every run, and the official validator checks every file.</p>
</section>

<section class="canvas__block" aria-labelledby="rep-three">
  <p class="kicker"><span class="kicker__num">B</span>Try it</p>
  <h2 id="rep-three" class="canvas__title">Reproduce in three commands</h2>
  <p class="od-lead">Only Docker is needed. <code>DATA</code> is your local folder with the match bundle, placed as <code>DATA.md</code> describes. It is never part of the repository.</p>
  <div class="od-repro">
    <div class="od-term">
      <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>Linux · macOS</span></div>
<pre><span class="line c" style="--i:0"># git clone https://github.com/Shrewdies/MTAH2027
# cd MTAH2027/initial-challenge</span>
<span class="line" style="--i:1"><span class="p">$ </span><span class="k">scripts/run.sh build</span></span>
<span class="line" style="--i:2"><span class="p">$ </span><span class="k">scripts/run.sh test</span></span>
<span class="line" style="--i:3"><span class="p">$ </span><span class="k">scripts/run.sh submit "$DATA" outputs</span> <span class="od-term__caret" aria-hidden="true"></span></span></pre>
    </div>
    <div class="od-term">
      <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>Windows · PowerShell</span></div>
<pre><span class="line c" style="--i:0"># same clone, then from
# initial-challenge</span>
<span class="line" style="--i:1"><span class="p">&gt; </span><span class="k">.\scripts\build.ps1</span></span>
<span class="line" style="--i:2"><span class="p">&gt; </span><span class="k">.\scripts\test.ps1</span></span>
<span class="line" style="--i:3"><span class="p">&gt; </span><span class="k">.\scripts\run_protected.ps1 -DataDir "$DATA"</span> <span class="od-term__caret" aria-hidden="true"></span></span></pre>
    </div>
  </div>
</section>

<section class="canvas__block" aria-labelledby="rep-files">
  <p class="kicker"><span class="kicker__num">C</span>Open the files</p>
  <h2 id="rep-files" class="canvas__title">The container and the scripts</h2>
  <div class="od-get">
    <div class="od-get__group">
      <p class="od-get__os"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l8.5 4.7v9.6L12 21.5l-8.5-4.7V7.2z"/><path d="M3.5 7.2L12 12l8.5-4.8M12 12v9.5"/></svg>Docker</p>
      <p class="od-get__note">The digest-pinned image and the complete dependency list.</p>
      <div class="actions"><a class="button" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/Dockerfile" rel="noopener">Dockerfile<span class="button__arrow" aria-hidden="true">&rarr;</span></a><a class="button button--ghost" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/requirements-solution.txt" rel="noopener">requirements-solution.txt<span class="button__arrow" aria-hidden="true">&rarr;</span></a></div>
    </div>
    <div class="od-get__group">
      <p class="od-get__os"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5l6 6.5-6 6.5M12 18.5h8"/></svg>Linux · macOS</p>
      <p class="od-get__note">One script: <code>build</code>, <code>test</code>, <code>submit</code>.</p>
      <div class="actions"><a class="button" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/scripts/run.sh" rel="noopener">scripts/run.sh<span class="button__arrow" aria-hidden="true">&rarr;</span></a></div>
    </div>
    <div class="od-get__group">
      <p class="od-get__os"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5.5l7.5-1v7H3zM12.5 4.2L21 3v8.5h-8.5zM3 12.5h7.5v7L3 18.5zM12.5 12.5H21V21l-8.5-1.2z"/></svg>Windows</p>
      <p class="od-get__note">PowerShell: build the image, run the tests, generate the file.</p>
      <div class="actions"><a class="button" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/scripts/build.ps1" rel="noopener">build.ps1<span class="button__arrow" aria-hidden="true">&rarr;</span></a><a class="button button--ghost" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/scripts/test.ps1" rel="noopener">test.ps1<span class="button__arrow" aria-hidden="true">&rarr;</span></a><a class="button button--ghost" href="https://github.com/Shrewdies/MTAH2027/blob/main/initial-challenge/scripts/run_protected.ps1" rel="noopener">run_protected.ps1<span class="button__arrow" aria-hidden="true">&rarr;</span></a></div>
    </div>
  </div>
  <div class="od-get__cta">
    <a class="button" href="https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge#reproduce" rel="noopener">Full reproduce guide<span class="button__arrow" aria-hidden="true">&rarr;</span></a>
    <p>The README's Reproduce section: every OS, plain Docker, and offline builds.</p>
  </div>
</section>

<section class="canvas__block" aria-labelledby="rep-pins">
  <p class="kicker"><span class="kicker__num">D</span>Pinned</p>
  <h2 id="rep-pins" class="canvas__title">Every layer is pinned</h2>
  <div class="od-pins">
    <ol class="od-stack" role="list">
      <li style="--i:0"><b>Base image</b><span>python:3.11.11-slim-bookworm @sha256:081075da…fd38e5</span></li>
      <li style="--i:1"><b>numpy</b><span>2.2.6</span></li>
      <li style="--i:2"><b>pandas</b><span>2.2.3</span></li>
      <li style="--i:3"><b>python-dateutil</b><span>2.9.0.post0</span></li>
      <li style="--i:4"><b>pytz</b><span>2024.2</span></li>
      <li style="--i:5"><b>tzdata</b><span>2024.2</span></li>
      <li style="--i:6"><b>six</b><span>1.16.0</span></li>
    </ol>
    <div class="od-pins__side">
      <div class="od-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M4 20h16"/></svg><div><b>Offline wheels</b>With the pinned wheels in <code>wheels/</code>, the build installs with no network at all.</div></div>
      <div class="od-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2.5v3M15 2.5v3M9 18.5v3M15 18.5v3M2.5 9h3M2.5 15h3M18.5 9h3M18.5 15h3"/></svg><div><b>Multi-arch</b>One image for linux/arm64 and linux/amd64: Windows, macOS and Linux alike.</div></div>
      <div class="od-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg><div><b>Both paths tested</b>The offline wheel build and the pinned PyPI build were both tested.</div></div>
    </div>
  </div>
</section>

<section class="canvas__block" aria-labelledby="rep-frozen">
  <p class="kicker"><span class="kicker__num">E</span>Frozen</p>
  <h2 id="rep-frozen" class="canvas__title">Nothing left to chance</h2>
  <ul class="od-cards" role="list">
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2.5v19M3.8 7.2l16.4 9.6M3.8 16.8l16.4-9.6"/><path d="M9.5 4l2.5 2.5L14.5 4M9.5 20l2.5-2.5 2.5 2.5"/></svg></span>
      <h3 class="od-card__title">Frozen profiles</h3>
      <p>Decoder parameters live in <code>possession/profiles.json</code>: <code>macro</code>, <code>balanced</code>, <code>spell</code> and <code>reasoned</code>, each one argument away.</p>
    </li>
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M3 20h18M5 17c3-9 7-12 14-13"/><circle cx="8" cy="12" r="1.4"/><circle cx="12" cy="8" r="1.4"/><circle cx="17" cy="6" r="1.4"/></svg></span>
      <h3 class="od-card__title">Seeded search</h3>
      <p>The Pareto search behind the profiles is seeded and runs on simulated matches; it reruns in about 15 seconds.</p>
    </li>
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 6.5l2 2 3.5-3.5M4 13.5l2 2 3.5-3.5M12.5 7h7.5M12.5 14h7.5M4 20h16"/></svg></span>
      <h3 class="od-card__title">Tested and validated</h3>
      <p>15 behaviour tests on fabricated scenes run with no match data. The official validator runs on every output file.</p>
    </li>
  </ul>
  <p class="od-plans"><b>Next</b>Our future plans join this page as the Innovative Challenge takes shape.</p>
</section>
