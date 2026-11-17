---
title: "Security & Data Protection"
order: 1
summary: "The match data never left our laptop. It was processed in a sealed, offline container, never committed and never uploaded, and only aggregate numbers were ever published."
canvas: true
extra_css: [/assets/ondevice/ondevice.css]
---
<ul class="facts" role="list">
  <li class="glass"><span class="facts__value">0</span><span class="facts__label">match files in the repository</span></li>
  <li class="glass"><span class="facts__value">0</span><span class="facts__label">uploads to any service or model</span></li>
  <li class="glass"><span class="facts__value">None</span><span class="facts__label">network inside the container</span></li>
  <li class="glass"><span class="facts__value">1</span><span class="facts__label">writable folder: the output</span></li>
</ul>

<section class="canvas__block" aria-labelledby="sec-box">
  <p class="kicker"><span class="kicker__num">A</span>In motion</p>
  <h2 id="sec-box" class="canvas__title">Data never leaves the laptop</h2>
  <div class="od-stage">
    <svg class="od-svg" viewBox="0 0 1000 660" role="img" aria-labelledby="sec-svg-t sec-svg-d" focusable="false">
      <title id="sec-svg-t">Data never leaves the laptop</title>
      <desc id="sec-svg-d">Inside the team laptop, match data flows read-only into a sealed Docker container. The container's network cable is cut, so nothing reaches the cloud. A single output door leads to an output folder outside the repository. A .gitignore shield keeps data out of the public repository, which holds code only; the site and report receive aggregate metrics only.</desc>
      <defs>
        <linearGradient id="sec-silver" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#B8C2D3"/><stop offset=".7" stop-color="#E9EDF5"/><stop offset="1" stop-color="#8E98B4"/>
        </linearGradient>
        <linearGradient id="sec-screen" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#0E2361"/><stop offset="1" stop-color="#0A1638"/>
        </linearGradient>
        <linearGradient id="sec-data" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#2F86F0"/><stop offset="1" stop-color="#004D98"/>
        </linearGradient>
        <linearGradient id="sec-out" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#E2FF5C"/><stop offset="1" stop-color="#8FB300"/>
        </linearGradient>
        <pattern id="sec-grid" width="28" height="28" patternUnits="userSpaceOnUse">
          <path d="M28 0H0V28" fill="none" stroke="rgba(233,237,245,.07)" stroke-width="1"/>
        </pattern>
        <clipPath id="sec-screen-clip"><rect x="64" y="124" width="872" height="432" rx="22"/></clipPath>
      </defs>
      <!-- cloud, outside and unreachable -->
      <g class="od-float" opacity=".55">
        <path d="M742 92c-22 0-38-14-38-32 0-17 15-30 33-31 6-17 23-27 42-27 23 0 42 15 45 35 18 1 31 13 31 28 0 15-14 27-32 27z" fill="rgba(255,255,255,.1)" stroke="rgba(233,237,245,.55)" stroke-width="2"/>
        <text class="t-mono" x="790" y="64" font-size="15" text-anchor="middle" fill-opacity=".9">CLOUD</text>
      </g>
      <text class="t-mono t-red" x="870" y="40" font-size="16">0 BYTES SENT</text>
      <path d="M500 112C520 70 620 60 704 62" fill="none" stroke="rgba(233,237,245,.4)" stroke-width="3" stroke-dasharray="4 10"/>
      <!-- laptop -->
      <rect x="56" y="116" width="888" height="448" rx="28" fill="url(#sec-silver)"/>
      <rect x="64" y="124" width="872" height="432" rx="22" fill="url(#sec-screen)"/>
      <rect x="64" y="124" width="872" height="432" rx="22" fill="url(#sec-grid)"/>
      <path d="M20 572h960l-26 26H46z" fill="url(#sec-silver)"/>
      <rect x="440" y="572" width="120" height="8" rx="4" fill="rgba(10,31,68,.35)"/>
      <g clip-path="url(#sec-screen-clip)">
        <rect class="od-sweep" x="-160" y="124" width="160" height="432" fill="rgba(255,255,255,.05)" transform="skewX(-12)"/>
      </g>
      <text class="t-mono t-silver" x="94" y="162" font-size="17">OUR LAPTOP</text>
      <circle cx="78" cy="156" r="5" fill="#C4F000"/>
      <!-- network cable, cut at the edge -->
      <path d="M500 220V172" stroke="#E9EDF5" stroke-width="7" stroke-linecap="round"/>
      <rect x="486" y="156" width="28" height="22" rx="4" fill="#B8C2D3"/>
      <path d="M492 156v-9M508 156v-9" stroke="#B8C2D3" stroke-width="4"/>
      <g class="od-blink">
        <path d="M486 132l28-20M486 112l28 20" stroke="#FF6A97" stroke-width="5" stroke-linecap="round"/>
      </g>
      <text class="t-mono t-lime" x="530" y="168" font-size="17">--network none</text>
      <!-- source mount -->
      <g>
        <rect x="104" y="196" width="150" height="58" rx="12" fill="rgba(255,255,255,.08)" stroke="rgba(233,237,245,.5)" stroke-width="2"/>
        <path d="M124 214h22M124 225h34M124 236h16" stroke="#E9EDF5" stroke-width="3" stroke-linecap="round"/>
        <text class="t-disp" x="176" y="234" font-size="24">CODE</text>
      </g>
      <path class="ln" d="M254 225H330"/>
      <path class="od-conveyor" d="M258 225H326" style="stroke-width:6"/>
      <!-- data folder -->
      <g>
        <path d="M104 302h46l12 14h92a10 10 0 0 1 10 10v66a10 10 0 0 1-10 10H114a10 10 0 0 1-10-10z" fill="url(#sec-data)" stroke="rgba(255,255,255,.55)" stroke-width="2"/>
        <rect x="122" y="336" width="114" height="8" rx="4" fill="rgba(255,255,255,.35)"/>
        <rect x="122" y="352" width="84" height="8" rx="4" fill="rgba(255,255,255,.35)"/>
        <rect x="122" y="368" width="100" height="8" rx="4" fill="rgba(255,255,255,.35)"/>
        <text class="t-disp" x="104" y="436" font-size="27">MATCH DATA</text>
        <text class="t-mono t-silver" x="104" y="460" font-size="14">LOCAL ONLY</text>
      </g>
      <path class="ln" d="M264 350H330"/>
      <path class="od-conveyor" d="M268 350H326"/>
      <!-- container -->
      <rect x="330" y="220" width="340" height="270" rx="22" fill="rgba(10,31,68,.72)"/>
      <rect class="od-march" x="330" y="220" width="340" height="270" rx="22" fill="none" stroke="#C4F000" stroke-width="3" stroke-dasharray="16 8"/>
      <text class="t-mono t-lime" x="352" y="252" font-size="15">DOCKER · OFFLINE</text>
      <!-- read-only locks on the inbound wall -->
      <g transform="translate(316 206)">
        <rect x="0" y="8" width="28" height="22" rx="4" fill="#C4F000"/><path d="M6 8V3a8 8 0 0 1 16 0v5" fill="none" stroke="#C4F000" stroke-width="4"/>
      </g>
      <g transform="translate(316 331)">
        <rect x="0" y="8" width="28" height="22" rx="4" fill="#C4F000"/><path d="M6 8V3a8 8 0 0 1 16 0v5" fill="none" stroke="#C4F000" stroke-width="4"/>
      </g>
      <text class="t-mono t-lime" x="318" y="294" font-size="14" text-anchor="end">READ-ONLY</text>
      <!-- core -->
      <circle cx="500" cy="352" r="86" fill="none" stroke="rgba(196,240,0,.18)" stroke-width="10"/>
      <circle class="od-spin" cx="500" cy="352" r="76" fill="none" stroke="#C4F000" stroke-width="3" stroke-dasharray="6 14" opacity=".8"/>
      <circle class="od-spin od-spin--rev" cx="500" cy="352" r="62" fill="none" stroke="#B9A2D8" stroke-width="2" stroke-dasharray="40 18"/>
      <circle cx="500" cy="352" r="48" fill="#004D98" stroke="#E9EDF5" stroke-width="2"/>
      <circle class="od-ping" cx="500" cy="352" r="48" fill="none" stroke="#C4F000" stroke-width="3"/>
      <text class="t-disp" x="500" y="364" font-size="32" text-anchor="middle">H·A·D</text>
      <text class="t-mono t-silver" x="500" y="466" font-size="13" text-anchor="middle">READ-ONLY ROOT · TMPFS /tmp</text>
      <!-- single output door -->
      <rect x="662" y="322" width="16" height="60" rx="5" fill="#C4F000"/>
      <rect class="od-breathe" x="656" y="316" width="28" height="72" rx="8" fill="none" stroke="#C4F000" stroke-width="2" opacity=".6"/>
      <text class="t-mono t-lime" x="682" y="292" font-size="14">ONE DOOR</text>
      <path class="ln" d="M684 352H748"/>
      <path class="od-conveyor od-conveyor--lime" d="M688 352H744"/>
      <!-- outputs folder -->
      <g>
        <path d="M748 302h46l12 14h92a10 10 0 0 1 10 10v66a10 10 0 0 1-10 10H758a10 10 0 0 1-10-10z" fill="url(#sec-out)" stroke="rgba(255,255,255,.7)" stroke-width="2"/>
        <text class="t-disp t-navy" x="828" y="370" font-size="22" text-anchor="middle">CSV</text>
        <text class="t-disp" x="748" y="436" font-size="27">OUTPUTS</text>
        <text class="t-mono t-silver" x="748" y="460" font-size="14">OUTSIDE THE REPO</text>
      </g>
      <!-- .gitignore shield between the data and the public repo -->
      <path d="M180 470V610" stroke="rgba(233,237,245,.35)" stroke-width="3" stroke-dasharray="4 8"/>
      <g transform="translate(152 486)">
        <path d="M28 0l26 10v20c0 18-11 31-26 38C13 61 2 48 2 30V10z" fill="#A50044" stroke="#FFFFFF" stroke-width="2.5"/>
        <path d="M18 24l20 20M38 24L18 44" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      </g>
      <circle class="od-ping" cx="180" cy="520" r="30" fill="none" stroke="#FF6A97" stroke-width="3"/>
      <text class="t-mono" x="226" y="526" font-size="15">.gitignore</text>
      <!-- what does get out -->
      <path d="M828 470V610" stroke="#C4F000" stroke-width="3" stroke-dasharray="4 8" opacity=".7"/>
      <rect x="40" y="612" width="300" height="40" rx="20" fill="rgba(10,31,68,.85)" stroke="rgba(233,237,245,.6)" stroke-width="2"/>
      <text class="t-mono" x="190" y="638" font-size="15" text-anchor="middle">PUBLIC REPO: CODE ONLY</text>
      <rect x="626" y="612" width="350" height="40" rx="20" fill="#C4F000"/>
      <text class="t-mono t-navy" x="801" y="638" font-size="15" text-anchor="middle">SITE + REPORT: AGGREGATES</text>
    </svg>
  </div>
  <ul class="od-legend" role="list">
    <li style="--c:#2F86F0"><span><b>Match data</b> · local only, mounted read-only.</span></li>
    <li style="--c:#C4F000"><span><b>Container</b> · no network, read-only root, tmpfs /tmp.</span></li>
    <li style="--c:#E2FF5C"><span><b>One door</b> · outputs land outside the repository.</span></li>
    <li style="--c:#E5336F"><span><b>.gitignore</b> · match data is never committed.</span></li>
  </ul>
  <p class="od-caption">Read-only in, one door out, cable cut. The repository never sees a byte of match data.</p>
</section>

<section class="canvas__block" aria-labelledby="sec-flags">
  <p class="kicker"><span class="kicker__num">B</span>The run, flag by flag</p>
  <h2 id="sec-flags" class="canvas__title">One sealed command</h2>
  <div class="od-anatomy">
    <div class="od-term">
      <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>scripts/run.sh submit</span></div>
      <p class="od-cmd"><span class="p" aria-hidden="true">$ </span>docker run &#45;&#45;rm <span class="od-tok" style="&#45;&#45;i:0">&#45;&#45;network none<sup>1</sup></span> <span class="od-tok" style="&#45;&#45;i:1">&#45;&#45;read-only<sup>2</sup></span> <span class="od-tok" style="&#45;&#45;i:2">&#45;&#45;tmpfs /tmp<sup>3</sup></span> -v "$REPO:/work<span class="od-tok" style="&#45;&#45;i:3">:ro<sup>4</sup></span>" -v "$DATA:/data<span class="od-tok" style="&#45;&#45;i:4">:ro<sup>4</sup></span>" -v "$OUT:<span class="od-tok" style="&#45;&#45;i:5">/out<sup>5</sup></span>" mtah2027:dev</p>
    </div>
    <ol class="od-flags">
      <li><b>&#45;&#45;network none</b>No network at all. Nothing inside can reach anything outside.</li>
      <li><b>&#45;&#45;read-only</b>The container cannot change its own filesystem.</li>
      <li><b>&#45;&#45;tmpfs /tmp</b>Scratch space lives in memory and is gone after the run.</li>
      <li><b>:ro</b>Source code and match data are mounted read-only.</li>
      <li><b>/out</b>The single writable path: an output folder outside the repository.</li>
    </ol>
  </div>
</section>

<section class="canvas__block" aria-labelledby="sec-did">
  <p class="kicker"><span class="kicker__num">C</span>What we did</p>
  <h2 id="sec-did" class="canvas__title">Three more safeguards around the run</h2>
  <ul class="od-cards" role="list">
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="6" cy="6" r="2.2"/><circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="9" r="2.2"/><path d="M6 8.2v7.6M18 11.2c0 3-3 3.8-9.8 5.6"/><path d="M3 21L21 3"/></svg></span>
      <h3 class="od-card__title">Never committed</h3>
      <p>The repository holds no match data, and two ignore files keep it that way (below). <code>DATA.md</code> tells each user where to put their own copy locally.</p>
    </li>
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 18a4.5 4.5 0 0 1-.6-9 6 6 0 0 1 11.4 1.6A3.8 3.8 0 0 1 17.5 18z"/><path d="M3 3l18 18"/></svg></span>
      <h3 class="od-card__title">Never uploaded</h3>
      <p>No external service, cloud platform or hosted model ever saw the data, as the competition terms require. Outputs stay outside the repository; the site and report publish aggregate metrics only.</p>
    </li>
    <li class="od-card glass">
      <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="2.5" y="8.5" width="9" height="7" rx="3.5"/><rect x="12.5" y="8.5" width="9" height="7" rx="3.5"/><path d="M8 12h8"/></svg></span>
      <h3 class="od-card__title">Lean supply chain</h3>
      <p>Two libraries, numpy and pandas, and a build that can install from local wheels with no network. Every pin, from the base image down, is listed on <a href="{{ '/on-device/reproducibility/' | relative_url }}">Reproducibility</a>.</p>
    </li>
  </ul>
</section>

<section class="canvas__block" aria-labelledby="sec-ignore">
  <p class="kicker"><span class="kicker__num">D</span>Two ignore files</p>
  <h2 id="sec-ignore" class="canvas__title">Two locks, two doors</h2>
  <div class="od-anatomy">
    <div style="display: grid; gap: 1rem;">
      <div class="od-term">
        <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>.gitignore</span></div>
        <p class="od-cmd">data/*<br>*_atd.txt &nbsp;*_atd.xml<br>*_smart_tagging.xml &nbsp;*_homography.csv<br>*.mp4<br>private_data/<br>outputs/<br>.env &nbsp;.env.*</p>
      </div>
      <div class="od-term">
        <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>.dockerignore</span></div>
        <p class="od-cmd">*<br>!requirements-solution.txt<br>!wheels/</p>
      </div>
    </div>
    <ol class="od-flags">
      <li><b>.gitignore</b>The door to the public repository. Match data is blocked twice: by folder, and again by file name in case a file ever lands somewhere else.</li>
      <li><b>outputs/</b>Generated label files are answers for the whole match, so every output path is ignored too.</li>
      <li><b>.env</b>Secrets and local environments never enter the history. The project needs none, and the rule is there anyway.</li>
      <li><b>.dockerignore</b>The door to the image. It refuses everything, then allows two things: the pinned dependency list and the optional wheels.</li>
      <li><b>*</b>So the image holds Python and two libraries. Code and data are mounted at run time, read-only, and never baked in.</li>
    </ol>
  </div>
</section>

<section class="canvas__block" aria-labelledby="sec-window">
  <h2 id="sec-window" class="visually-hidden">The competition rules</h2>
  <div class="od-strip">
    <p class="od-strip__big">Answers stayed sealed</p>
    <p>No hand labels, nothing tuned on the match's answers, and the public 5-minute window used only as a correctness check. What the rules are, and what each one forced, is in <a href="{{ '/challenges/rules-as-design-constraints/' | relative_url }}">The rules are the architecture</a>. And the team photos on this site? Processed locally too.</p>
  </div>
</section>
