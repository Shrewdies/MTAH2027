---
title: "One Laptop, Three Engines"
nav_title: "Machine & Hardware"
order: 3
summary: "The match data could not leave our hands, so the compute came to the data. One Snapdragon X Elite laptop: its CPU decodes a full match in under 10 seconds, and its GPU and NPU are the headroom for local models."
canvas: true
extra_css: [/assets/ondevice/ondevice.css]
---
<ol class="od-story" role="list" aria-label="The story in five steps">
  <li><a href="#mh-laptop"><b>01</b>This laptop</a></li>
  <li><a href="#mh-engines"><b>02</b>Three engines</a></li>
  <li><a href="#mh-today"><b>03</b>Today: the CPU</a></li>
  <li><a href="#mh-next"><b>04</b>Next: local models</a></li>
  <li><a href="#mh-why"><b>05</b>Why hardware</a></li>
</ol>

<section class="canvas__block" aria-labelledby="mh-laptop">
  <p class="kicker"><span class="kicker__num">01</span>This laptop</p>
  <h2 id="mh-laptop" class="canvas__title">Where every byte stayed</h2>
  <div class="od-spec">
    <div class="od-stage od-spec__die">
      <svg class="od-svg" viewBox="0 0 520 540" role="img" aria-labelledby="mach-svg-t" focusable="false">
        <title id="mach-svg-t">Our system on chip: twelve Oryon CPU cores, an Adreno X1-85 GPU and a Hexagon NPU sharing 32 GB of memory</title>
        <defs>
          <linearGradient id="mach-silver" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#FFFFFF"/><stop offset=".4" stop-color="#B8C2D3"/><stop offset=".7" stop-color="#E9EDF5"/><stop offset="1" stop-color="#8E98B4"/>
          </linearGradient>
          <linearGradient id="mach-die" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#13296B"/><stop offset="1" stop-color="#0B1433"/>
          </linearGradient>
          <linearGradient id="mach-core" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#2F86F0"/><stop offset="1" stop-color="#004D98"/>
          </linearGradient>
          <clipPath id="mach-clip"><rect x="40" y="40" width="440" height="460" rx="26"/></clipPath>
        </defs>
        <g fill="#B8C2D3">
          <rect x="70" y="22" width="10" height="18" rx="2"/><rect x="110" y="22" width="10" height="18" rx="2"/><rect x="150" y="22" width="10" height="18" rx="2"/><rect x="190" y="22" width="10" height="18" rx="2"/><rect x="230" y="22" width="10" height="18" rx="2"/><rect x="270" y="22" width="10" height="18" rx="2"/><rect x="310" y="22" width="10" height="18" rx="2"/><rect x="350" y="22" width="10" height="18" rx="2"/><rect x="390" y="22" width="10" height="18" rx="2"/><rect x="430" y="22" width="10" height="18" rx="2"/>
          <rect x="70" y="500" width="10" height="18" rx="2"/><rect x="110" y="500" width="10" height="18" rx="2"/><rect x="150" y="500" width="10" height="18" rx="2"/><rect x="190" y="500" width="10" height="18" rx="2"/><rect x="230" y="500" width="10" height="18" rx="2"/><rect x="270" y="500" width="10" height="18" rx="2"/><rect x="310" y="500" width="10" height="18" rx="2"/><rect x="350" y="500" width="10" height="18" rx="2"/><rect x="390" y="500" width="10" height="18" rx="2"/><rect x="430" y="500" width="10" height="18" rx="2"/>
          <rect x="22" y="80" width="18" height="10" rx="2"/><rect x="22" y="130" width="18" height="10" rx="2"/><rect x="22" y="180" width="18" height="10" rx="2"/><rect x="22" y="230" width="18" height="10" rx="2"/><rect x="22" y="280" width="18" height="10" rx="2"/><rect x="22" y="330" width="18" height="10" rx="2"/><rect x="22" y="380" width="18" height="10" rx="2"/><rect x="22" y="430" width="18" height="10" rx="2"/>
          <rect x="480" y="80" width="18" height="10" rx="2"/><rect x="480" y="130" width="18" height="10" rx="2"/><rect x="480" y="180" width="18" height="10" rx="2"/><rect x="480" y="230" width="18" height="10" rx="2"/><rect x="480" y="280" width="18" height="10" rx="2"/><rect x="480" y="330" width="18" height="10" rx="2"/><rect x="480" y="380" width="18" height="10" rx="2"/><rect x="480" y="430" width="18" height="10" rx="2"/>
        </g>
        <rect x="40" y="40" width="440" height="460" rx="26" fill="url(#mach-silver)"/>
        <rect x="58" y="58" width="404" height="424" rx="16" fill="url(#mach-die)"/>
        <g clip-path="url(#mach-clip)"><rect class="od-sweep" x="-140" y="20" width="110" height="520" fill="rgba(255,255,255,.18)"/></g>
        <text class="t-mono t-lime" x="80" y="92" font-size="15">ORYON CPU · 12 CORES</text>
        <g>
          <rect class="od-wave" style="--i:0" x="80" y="108" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:1" x="176" y="108" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:2" x="272" y="108" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:3" x="368" y="108" width="72" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:4" x="80" y="172" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:5" x="176" y="172" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:6" x="272" y="172" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:7" x="368" y="172" width="72" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:8" x="80" y="236" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:9" x="176" y="236" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:10" x="272" y="236" width="80" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
          <rect class="od-wave" style="--i:11" x="368" y="236" width="72" height="54" rx="8" fill="url(#mach-core)" stroke="#2F86F0"/>
        </g>
        <g class="t-disp" font-size="22" text-anchor="middle">
          <text x="120" y="143">01</text><text x="216" y="143">02</text><text x="312" y="143">03</text><text x="404" y="143">04</text>
          <text x="120" y="207">05</text><text x="216" y="207">06</text><text x="312" y="207">07</text><text x="404" y="207">08</text>
          <text x="120" y="271">09</text><text x="216" y="271">10</text><text x="312" y="271">11</text><text x="404" y="271">12</text>
        </g>
        <rect x="80" y="308" width="176" height="96" rx="10" fill="#6E4C9F" stroke="#B9A2D8"/>
        <path d="M96 330h144M96 346h144M96 362h144M96 378h144" stroke="rgba(255,255,255,.18)" stroke-width="6"/>
        <text class="t-disp" x="96" y="352" font-size="26">ADRENO</text>
        <text class="t-mono" x="96" y="390" font-size="13">GPU · X1-85</text>
        <rect x="272" y="308" width="168" height="96" rx="10" fill="#A50044" stroke="#E5336F"/>
        <polygon class="od-spin" points="410,330 424,338 424,354 410,362 396,354 396,338" fill="none" stroke="#C4F000" stroke-width="3"/>
        <text class="t-disp" x="288" y="352" font-size="26">HEXAGON</text>
        <text class="t-mono" x="288" y="390" font-size="13">NPU</text>
        <rect x="80" y="414" width="360" height="56" rx="10" fill="rgba(196,240,0,.1)" stroke="#C4F000" stroke-width="2"/>
        <path class="ln" d="M92 423H428M92 461H428" style="stroke:rgba(196,240,0,.3)"/>
        <path class="od-flow" pathLength="100" d="M92 423H428"/>
        <path class="od-flow od-flow--back od-flow--white od-flow--d1" pathLength="100" d="M92 461H428"/>
        <text class="t-mono t-lime" x="260" y="447" font-size="14" text-anchor="middle">SHARED MEMORY · 32 GB</text>
      </svg>
    </div>
    <div>
      <div class="od-spec__head"><span>Spec sheet</span><b>Read locally with Get-CimInstance</b></div>
      <ul class="od-rows" role="list">
        <li class="od-row od-row--hero" style="--i:0"><span class="od-row__k">Device</span><span class="od-row__v">Snapdragon X Elite laptop<small>the only machine the match data ever touched</small></span></li>
        <li class="od-row" style="--i:1"><span class="od-row__k">Processor</span><span class="od-row__v">Snapdragon X Elite<small>X1E78100 · Qualcomm Oryon CPU</small></span></li>
        <li class="od-row" style="--i:2"><span class="od-row__k">Cores</span><span class="od-row__v">12<small>Oryon CPU cores</small></span></li>
        <li class="od-row" style="--i:3"><span class="od-row__k">Memory</span><span class="od-row__v">32 GB<small>system memory</small></span></li>
        <li class="od-row" style="--i:4"><span class="od-row__k">Graphics</span><span class="od-row__v">Adreno X1-85<small>Qualcomm Adreno GPU</small></span></li>
        <li class="od-row" style="--i:5"><span class="od-row__k">Storage</span><span class="od-row__v">1 TB<small>internal drive</small></span></li>
        <li class="od-row" style="--i:6"><span class="od-row__k">System</span><span class="od-row__v">Windows 11 Pro<small>ARM64 · 64-bit</small></span></li>
      </ul>
    </div>
  </div>
  <details class="od-details">
    <summary>How we read the specs</summary>
    <div class="od-term">
    <div class="od-term__bar" aria-hidden="true"><i></i><i></i><i></i><span>PowerShell</span></div>
<pre><span class="line" style="--i:0"><span class="p">&gt; </span><span class="k">'Win32_ComputerSystem','Win32_Processor','Win32_PhysicalMemory',</span></span>
<span class="line" style="--i:1"><span class="k">  'Win32_OperatingSystem','Win32_VideoController','Win32_DiskDrive' |</span></span>
<span class="line" style="--i:2"><span class="k">  ForEach-Object { Get-CimInstance $_ }</span> <span class="od-term__caret" aria-hidden="true"></span></span></pre>
  </div>
    <p class="od-note">Published: device class, processor and core count, memory, graphics, storage, OS edition and architecture. Left out on purpose: serial numbers, user and host names, and anything else that identifies the device.</p>
  </details>
</section>

<section class="canvas__block" aria-labelledby="mh-engines">
  <p class="kicker"><span class="kicker__num">02</span>Three engines</p>
  <h2 id="mh-engines" class="canvas__title">CPU, GPU and NPU on one chip</h2>
  <div class="od-stage">
    <svg class="od-svg" viewBox="0 0 900 880" role="img" aria-labelledby="hw-svg-t hw-svg-d" focusable="false">
      <title id="hw-svg-t">Snapdragon X Elite system on chip</title>
      <desc id="hw-svg-d">Abstract diagram of the Snapdragon X Elite. A Qualcomm AI stack layer (AI Engine, AI Hub, local LLMs and local models) feeds down into three engines on one chip: the Oryon CPU with twelve cores on our machine, the Adreno X1-85 GPU and the Hexagon NPU rated at up to 45 TOPS. Data pulses flow between all three over shared memory. Today our decoder runs on the CPU; vision models and local LLMs are next for the GPU and NPU. Everything stays on the device.</desc>
      <defs>
        <linearGradient id="hw-silver" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="#B8C2D3"/><stop offset=".62" stop-color="#F2F4F9"/><stop offset="1" stop-color="#8E98B4"/>
        </linearGradient>
        <linearGradient id="hw-die" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#132A70"/><stop offset=".6" stop-color="#0D1B4C"/><stop offset="1" stop-color="#1F1550"/>
        </linearGradient>
        <linearGradient id="hw-core" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#4C9BFF"/><stop offset="1" stop-color="#0A57B0"/>
        </linearGradient>
        <linearGradient id="hw-cpu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#0F63C4"/><stop offset="1" stop-color="#003A78"/>
        </linearGradient>
        <linearGradient id="hw-gpu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#7A57B3"/><stop offset="1" stop-color="#40307A"/>
        </linearGradient>
        <linearGradient id="hw-npu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#C0175A"/><stop offset="1" stop-color="#6D0F2C"/>
        </linearGradient>
        <linearGradient id="hw-tile" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="rgba(255,255,255,.2)"/><stop offset="1" stop-color="rgba(255,255,255,.05)"/>
        </linearGradient>
        <pattern id="hw-grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <path d="M24 0H0V24" fill="none" stroke="rgba(233,237,245,.06)" stroke-width="1"/>
        </pattern>
        <clipPath id="hw-pkg"><rect x="40" y="262" width="820" height="576" rx="28"/></clipPath>
      </defs>
      <!-- device boundary -->
      <rect class="od-march" x="10" y="14" width="880" height="856" rx="34" fill="none" stroke="#C4F000" stroke-width="2" stroke-dasharray="16 8" opacity=".55"/>
      <rect x="34" y="0" width="356" height="28" fill="#13296B"/>
      <circle class="od-blink" cx="50" cy="14" r="6" fill="#C4F000"/>
      <text class="t-mono t-lime" x="66" y="20" font-size="16">ON-DEVICE · DATA STAYS HERE</text>
      <!-- AI stack -->
      <text class="t-mono t-silver" x="60" y="84" font-size="16">QUALCOMM AI STACK</text>
      <g>
        <rect x="60" y="100" width="250" height="92" rx="16" fill="url(#hw-tile)" stroke="rgba(233,237,245,.55)" stroke-width="2"/>
        <text class="t-disp" x="82" y="144" font-size="34">AI ENGINE</text>
        <text class="t-mono t-silver" x="82" y="174" font-size="14">CPU + GPU + NPU</text>
        <rect x="325" y="100" width="250" height="92" rx="16" fill="url(#hw-tile)" stroke="rgba(233,237,245,.55)" stroke-width="2"/>
        <text class="t-disp" x="347" y="144" font-size="34">AI HUB</text>
        <text class="t-mono t-silver" x="347" y="174" font-size="14">DEVICE-READY MODELS</text>
        <rect x="590" y="100" width="250" height="92" rx="16" fill="rgba(196,240,0,.14)" stroke="#C4F000" stroke-width="2"/>
        <text class="t-disp t-lime" x="612" y="144" font-size="34">LOCAL LLMS</text>
        <text class="t-mono t-silver" x="612" y="174" font-size="14">+ LOCAL MODELS</text>
      </g>
      <!-- package and pins -->
      <g fill="#B8C2D3"><rect x="24" y="300" width="16" height="12" rx="2"/><rect x="860" y="300" width="16" height="12" rx="2"/><rect x="24" y="340" width="16" height="12" rx="2"/><rect x="860" y="340" width="16" height="12" rx="2"/><rect x="24" y="380" width="16" height="12" rx="2"/><rect x="860" y="380" width="16" height="12" rx="2"/><rect x="24" y="420" width="16" height="12" rx="2"/><rect x="860" y="420" width="16" height="12" rx="2"/><rect x="24" y="460" width="16" height="12" rx="2"/><rect x="860" y="460" width="16" height="12" rx="2"/><rect x="24" y="500" width="16" height="12" rx="2"/><rect x="860" y="500" width="16" height="12" rx="2"/><rect x="24" y="540" width="16" height="12" rx="2"/><rect x="860" y="540" width="16" height="12" rx="2"/><rect x="24" y="580" width="16" height="12" rx="2"/><rect x="860" y="580" width="16" height="12" rx="2"/><rect x="24" y="620" width="16" height="12" rx="2"/><rect x="860" y="620" width="16" height="12" rx="2"/><rect x="24" y="660" width="16" height="12" rx="2"/><rect x="860" y="660" width="16" height="12" rx="2"/><rect x="24" y="700" width="16" height="12" rx="2"/><rect x="860" y="700" width="16" height="12" rx="2"/><rect x="24" y="740" width="16" height="12" rx="2"/><rect x="860" y="740" width="16" height="12" rx="2"/><rect x="24" y="780" width="16" height="12" rx="2"/><rect x="860" y="780" width="16" height="12" rx="2"/><rect x="84" y="246" width="12" height="16" rx="2"/><rect x="84" y="838" width="12" height="16" rx="2"/><rect x="132" y="246" width="12" height="16" rx="2"/><rect x="132" y="838" width="12" height="16" rx="2"/><rect x="180" y="246" width="12" height="16" rx="2"/><rect x="180" y="838" width="12" height="16" rx="2"/><rect x="228" y="246" width="12" height="16" rx="2"/><rect x="228" y="838" width="12" height="16" rx="2"/><rect x="276" y="246" width="12" height="16" rx="2"/><rect x="276" y="838" width="12" height="16" rx="2"/><rect x="324" y="246" width="12" height="16" rx="2"/><rect x="324" y="838" width="12" height="16" rx="2"/><rect x="372" y="246" width="12" height="16" rx="2"/><rect x="372" y="838" width="12" height="16" rx="2"/><rect x="420" y="246" width="12" height="16" rx="2"/><rect x="420" y="838" width="12" height="16" rx="2"/><rect x="468" y="246" width="12" height="16" rx="2"/><rect x="468" y="838" width="12" height="16" rx="2"/><rect x="516" y="246" width="12" height="16" rx="2"/><rect x="516" y="838" width="12" height="16" rx="2"/><rect x="564" y="246" width="12" height="16" rx="2"/><rect x="564" y="838" width="12" height="16" rx="2"/><rect x="612" y="246" width="12" height="16" rx="2"/><rect x="612" y="838" width="12" height="16" rx="2"/><rect x="660" y="246" width="12" height="16" rx="2"/><rect x="660" y="838" width="12" height="16" rx="2"/><rect x="708" y="246" width="12" height="16" rx="2"/><rect x="708" y="838" width="12" height="16" rx="2"/><rect x="756" y="246" width="12" height="16" rx="2"/><rect x="756" y="838" width="12" height="16" rx="2"/><rect x="804" y="246" width="12" height="16" rx="2"/><rect x="804" y="838" width="12" height="16" rx="2"/></g>
      <rect x="40" y="262" width="820" height="576" rx="28" fill="url(#hw-silver)"/>
      <rect x="66" y="288" width="768" height="524" rx="18" fill="url(#hw-die)"/>
      <rect x="66" y="288" width="768" height="524" rx="18" fill="url(#hw-grid)"/>
      <g clip-path="url(#hw-pkg)"><rect class="od-sweep" x="-150" y="250" width="120" height="600" fill="rgba(255,255,255,.12)"/></g>
      <text class="t-disp" x="96" y="336" font-size="34">SNAPDRAGON X ELITE</text>
      <text class="t-mono t-silver" x="804" y="334" font-size="14" text-anchor="end">SYSTEM ON CHIP</text>
      <!-- blocks -->
      <rect x="96" y="362" width="226" height="240" rx="14" fill="url(#hw-cpu)" stroke="#7FB6FF" stroke-width="2"/>
      <text class="t-disp" x="116" y="404" font-size="36">ORYON</text>
      <text class="t-mono" x="116" y="430" font-size="14">CPU · 12 CORES</text>
      <rect class="od-wave" style="--i:0" x="116" y="448" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:1" x="166" y="448" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:2" x="216" y="448" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:3" x="266" y="448" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:4" x="116" y="494" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:5" x="166" y="494" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:6" x="216" y="494" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:7" x="266" y="494" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:8" x="116" y="540" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:9" x="166" y="540" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:10" x="216" y="540" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/><rect class="od-wave" style="--i:11" x="266" y="540" width="40" height="36" rx="6" fill="url(#hw-core)" stroke="#7FB6FF" stroke-width="1.5"/>
      <rect x="337" y="362" width="226" height="240" rx="14" fill="url(#hw-gpu)" stroke="#B9A2D8" stroke-width="2"/>
      <text class="t-disp" x="357" y="404" font-size="36">ADRENO</text>
      <text class="t-mono" x="357" y="430" font-size="14">GPU · X1-85</text>
      <rect class="od-wave" style="--i:0" x="357" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 366 459)"/><rect class="od-wave" style="--i:1" x="385" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 394 459)"/><rect class="od-wave" style="--i:2" x="413" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 422 459)"/><rect class="od-wave" style="--i:3" x="441" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 450 459)"/><rect class="od-wave" style="--i:4" x="469" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 478 459)"/><rect class="od-wave" style="--i:5" x="497" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 506 459)"/><rect class="od-wave" style="--i:6" x="525" y="450" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 534 459)"/><rect class="od-wave" style="--i:1" x="357" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 366 487)"/><rect class="od-wave" style="--i:2" x="385" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 394 487)"/><rect class="od-wave" style="--i:3" x="413" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 422 487)"/><rect class="od-wave" style="--i:4" x="441" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 450 487)"/><rect class="od-wave" style="--i:5" x="469" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 478 487)"/><rect class="od-wave" style="--i:6" x="497" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 506 487)"/><rect class="od-wave" style="--i:7" x="525" y="478" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 534 487)"/><rect class="od-wave" style="--i:2" x="357" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 366 515)"/><rect class="od-wave" style="--i:3" x="385" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 394 515)"/><rect class="od-wave" style="--i:4" x="413" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 422 515)"/><rect class="od-wave" style="--i:5" x="441" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 450 515)"/><rect class="od-wave" style="--i:6" x="469" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 478 515)"/><rect class="od-wave" style="--i:7" x="497" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 506 515)"/><rect class="od-wave" style="--i:8" x="525" y="506" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 534 515)"/><rect class="od-wave" style="--i:3" x="357" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 366 543)"/><rect class="od-wave" style="--i:4" x="385" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 394 543)"/><rect class="od-wave" style="--i:5" x="413" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 422 543)"/><rect class="od-wave" style="--i:6" x="441" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 450 543)"/><rect class="od-wave" style="--i:7" x="469" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 478 543)"/><rect class="od-wave" style="--i:8" x="497" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 506 543)"/><rect class="od-wave" style="--i:9" x="525" y="534" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 534 543)"/><rect class="od-wave" style="--i:4" x="357" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 366 571)"/><rect class="od-wave" style="--i:5" x="385" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 394 571)"/><rect class="od-wave" style="--i:6" x="413" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 422 571)"/><rect class="od-wave" style="--i:7" x="441" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 450 571)"/><rect class="od-wave" style="--i:8" x="469" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 478 571)"/><rect class="od-wave" style="--i:9" x="497" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 506 571)"/><rect class="od-wave" style="--i:10" x="525" y="562" width="18" height="18" rx="4" fill="#B9A2D8" transform="rotate(45 534 571)"/>
      <rect x="574" y="362" width="226" height="240" rx="14" fill="url(#hw-npu)" stroke="#FF8AB0" stroke-width="2"/>
      <text class="t-disp" x="594" y="404" font-size="36">HEXAGON</text>
      <text class="t-mono" x="594" y="430" font-size="14">NPU</text>
      <polygon class="od-spin" points="770,378 786,387 786,405 770,414 754,405 754,387" fill="none" stroke="#C4F000" stroke-width="3"/>
      <text class="t-disp t-lime" x="592" y="548" font-size="112">45</text>
      <text class="t-mono t-silver" x="712" y="498" font-size="14">UP TO</text>
      <text class="t-disp" x="712" y="534" font-size="34">TOPS</text>
      <circle class="od-wave" style="--i:0" cx="600" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:1" cx="623" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:2" cx="646" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:3" cx="669" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:4" cx="692" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:5" cx="715" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:6" cx="738" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:7" cx="761" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:8" cx="784" cy="570" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:2" cx="600" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:3" cx="623" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:4" cx="646" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:5" cx="669" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:6" cx="692" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:7" cx="715" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:8" cx="738" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:0" cx="761" cy="588" r="4.5" fill="#FF8AB0"/><circle class="od-wave" style="--i:1" cx="784" cy="588" r="4.5" fill="#FF8AB0"/>
      <!-- links from the stack into the engines -->
      <path class="ln" d="M185 192C185 280 209 280 209 362"/>
      <path class="ln" d="M450 192V362"/>
      <path class="ln" d="M715 192C715 280 687 280 687 362"/>
      <path class="od-flow od-flow--violet od-flow--slow" pathLength="100" d="M185 192C185 280 209 280 209 362"/>
      <path class="od-flow od-flow--violet od-flow--slow od-flow--d1" pathLength="100" d="M450 192V362"/>
      <path class="od-flow od-flow--slow od-flow--d2" pathLength="100" d="M715 192C715 280 687 280 687 362"/>
      <!-- shared memory bus -->
      <rect x="96" y="646" width="704" height="64" rx="16" fill="rgba(196,240,0,.1)" stroke="#C4F000" stroke-width="2"/>
      <path class="ln" d="M112 658H784M112 698H784" style="stroke:rgba(196,240,0,.35)"/>
      <path class="od-flow" pathLength="100" d="M112 658H784"/>
      <path class="od-flow od-flow--d2" pathLength="100" d="M112 658H784"/>
      <path class="od-flow od-flow--back od-flow--white" pathLength="100" d="M112 698H784"/>
      <path class="od-flow od-flow--back od-flow--white od-flow--d1" pathLength="100" d="M112 698H784"/>
      <text class="t-disp t-lime" x="448" y="689" font-size="26" text-anchor="middle">SHARED MEMORY</text>
      <!-- engine to memory, both ways -->
      <path class="ln" d="M201 602V646M217 602V646M442 602V646M458 602V646M679 602V646M695 602V646"/>
      <path class="od-flow" pathLength="100" d="M201 602V646"/>
      <path class="od-flow od-flow--back od-flow--white od-flow--d1" pathLength="100" d="M217 602V646"/>
      <path class="od-flow od-flow--d2" pathLength="100" d="M442 602V646"/>
      <path class="od-flow od-flow--back od-flow--white" pathLength="100" d="M458 602V646"/>
      <path class="od-flow od-flow--d1" pathLength="100" d="M679 602V646"/>
      <path class="od-flow od-flow--back od-flow--white od-flow--d2" pathLength="100" d="M695 602V646"/>
      <!-- today and next -->
      <rect x="96" y="734" width="226" height="48" rx="24" fill="#C4F000"/>
      <circle class="od-ping" cx="122" cy="758" r="9" fill="none" stroke="#0A1F44" stroke-width="3"/>
      <circle cx="122" cy="758" r="6" fill="#0A1F44"/>
      <text class="t-mono t-navy" x="140" y="764" font-size="15">TODAY: DECODER</text>
      <rect x="337" y="734" width="226" height="48" rx="24" fill="none" stroke="#C4F000" stroke-width="2" stroke-dasharray="7 6"/>
      <text class="t-mono t-lime" x="450" y="764" font-size="15" text-anchor="middle">NEXT: VISION</text>
      <rect x="574" y="734" width="226" height="48" rx="24" fill="none" stroke="#C4F000" stroke-width="2" stroke-dasharray="7 6"/>
      <text class="t-mono t-lime" x="687" y="764" font-size="15" text-anchor="middle">NEXT: LOCAL LLMS</text></svg>
  </div>
  <ul class="od-legend" role="list">
    <li style="--c:#2F86F0"><span><b>Oryon CPU</b> · 12 cores on our machine. Runs our decoder today.</span></li>
    <li style="--c:#B9A2D8"><span><b>Adreno GPU</b> · X1-85 on our machine. Next: vision models.</span></li>
    <li style="--c:#E5336F"><span><b>Hexagon NPU</b> · up to 45 TOPS. Next: local LLMs.</span></li>
    <li style="--c:#C4F000"><span><b>Shared memory</b> · one pool for all three engines.</span></li>
  </ul>
</section>

<section class="canvas__block" aria-labelledby="mh-today">
  <p class="kicker"><span class="kicker__num">03</span>Today</p>
  <h2 id="mh-today" class="canvas__title">The CPU decodes a match</h2>
  <ul class="facts" role="list">
    <li class="glass"><span class="facts__value">&lt; 10 s</span><span class="facts__label">full-match decode, numpy only</span></li>
    <li class="glass"><span class="facts__value">1 of 3</span><span class="facts__label">engines used: the Oryon CPU</span></li>
    <li class="glass"><span class="facts__value">arm64</span><span class="facts__label">native Linux container, offline</span></li>
    <li class="glass"><span class="facts__value">0</span><span class="facts__label">bytes sent off the machine</span></li>
  </ul>
  <p class="od-caption">Our Initial Challenge solution ran on the Oryon CPU alone. The Adreno GPU and the Hexagon NPU sat idle.</p>
</section>

<section class="canvas__block" aria-labelledby="mh-next">
  <p class="kicker"><span class="kicker__num">04</span>Next</p>
  <h2 id="mh-next" class="canvas__title">Headroom for local models</h2>
  <div class="od-article">
    <ul class="od-cards od-cards--2" role="list">
      <li class="od-card glass">
        <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3"/><path d="M12 1.5v4M12 18.5v4M1.5 12h4M18.5 12h4"/></svg></span>
        <h3 class="od-card__title">Vision on device</h3>
        <p>A light ball detector for the frames the tracker misses, running on the GPU or NPU, beside the data. It is the on-device vision engine on our <a href="{{ '/challenges/roadmap/' | relative_url }}">roadmap</a>.</p>
      </li>
      <li class="od-card glass">
        <span class="od-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 5.5h16v10H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/></svg></span>
        <h3 class="od-card__title">Local LLMs</h3>
        <p>Language models that turn possession numbers into tactical text, run locally with nothing sent anywhere.</p>
      </li>
    </ul>
    <div class="od-article__side">
      <figure class="od-quote">
        <span class="od-quote__num">45</span><span class="od-quote__unit">TOPS · HEXAGON NPU</span>
        <blockquote><p>The Hexagon NPU in our laptop is rated at up to 45&nbsp;TOPS: trillions of operations every second, set aside for neural networks alone. It sat idle through the Initial Challenge. That idle silicon is our headroom.</p></blockquote>
      </figure>
      <div class="od-split__item"><b>Our measure</b><p>What we vouch for is what we ran ourselves: a full match decoded in under 10 seconds, on the CPU alone, with the network switched off.</p></div>
    </div>
  </div>
</section>

<section class="canvas__block" aria-labelledby="mh-why">
  <h2 id="mh-why" class="visually-hidden">Why hardware</h2>
  <div class="od-strip">
    <p class="od-strip__big">Privacy is a place</p>
    <p>The match data may not go to any cloud platform, external service or hosted model, so renting a GPU or calling a hosted API was never an option. A laptop strong enough to do the work means nothing has to leave it. Privacy and speed come from the same choice: computing locally.</p>
  </div>
</section>
