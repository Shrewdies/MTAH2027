---
layout: section
title: On-device
collection_index: ondevice
permalink: /on-device/
summary: "Security, reproducibility and the hardware we compute on. The match data never left our laptop, and every result can be rebuilt byte for byte."
extra_css: [/assets/ondevice/ondevice.css]
---
<div class="od-index">
  <div>
    <p><strong>Everything happened on one laptop.</strong> The competition data was processed in a sealed, offline container, never committed and never uploaded. The pipeline is pinned from base image to last dependency, so anyone can rebuild our exact output. And the chip that ran it has room to spare for what comes next.</p>
    <ul class="od-chips" role="list">
      <li style="--c:#2F86F0">offline container</li>
      <li style="--c:#B9A2D8">byte-identical runs</li>
      <li style="--c:#E5336F">Windows on Arm</li>
      <li>CPU · GPU · NPU</li>
    </ul>
  </div>
  <div class="od-index__art">
    <svg class="od-svg" viewBox="0 0 480 300" role="img" aria-label="Four topics orbit one laptop: security, reproducibility, our machine and hardware" focusable="false">
      <rect x="70" y="30" width="340" height="210" rx="18" fill="rgba(10,31,68,.78)" stroke="#E9EDF5" stroke-width="4"/>
      <path d="M40 248h400l-18 18H58z" fill="#E9EDF5"/>
      <path class="ln" d="M240 135L130 85M240 135L350 85M240 135L130 190M240 135L350 190"/>
      <path class="od-flow" pathLength="100" d="M130 85L240 135"/>
      <path class="od-flow od-flow--d1" pathLength="100" d="M350 85L240 135"/>
      <path class="od-flow od-flow--white od-flow--d2" pathLength="100" d="M130 190L240 135"/>
      <path class="od-flow od-flow--white" pathLength="100" d="M350 190L240 135"/>
      <circle class="od-spin" cx="240" cy="135" r="44" fill="none" stroke="#C4F000" stroke-width="3" stroke-dasharray="5 9"/>
      <circle class="od-ping" cx="240" cy="135" r="30" fill="none" stroke="#C4F000" stroke-width="3"/>
      <rect x="214" y="109" width="52" height="52" rx="10" fill="#C4F000"/>
      <rect x="228" y="123" width="24" height="24" rx="4" fill="#0A1F44"/>
      <g fill="#004D98" stroke="#E9EDF5" stroke-width="2.5">
        <circle cx="130" cy="85" r="26"/><circle cx="350" cy="85" r="26"/>
      </g>
      <g fill="#A50044" stroke="#E9EDF5" stroke-width="2.5">
        <circle cx="130" cy="190" r="26"/><circle cx="350" cy="190" r="26"/>
      </g>
      <g fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M130 71l11 5v8c0 7-5 12-11 15-6-3-11-8-11-15v-8z"/>
        <path d="M362 85a12 12 0 1 1-3.5-8.5M362 72v6h-6"/>
        <rect x="116" y="180" width="28" height="18" rx="2"/><path d="M112 203h36"/>
        <rect x="339" y="179" width="22" height="22" rx="3"/><path d="M345 175v4M355 175v4M345 201v4M355 201v4M335 185h4M335 195h4M361 185h4M361 195h4"/>
      </g>
      <text class="t-mono t-lime" x="96" y="56" font-size="14">01</text>
      <text class="t-mono t-lime" x="368" y="56" font-size="14">02</text>
      <text class="t-mono t-lime" x="96" y="230" font-size="14">03</text>
      <text class="t-mono t-lime" x="368" y="230" font-size="14">04</text>
    </svg>
  </div>
</div>
