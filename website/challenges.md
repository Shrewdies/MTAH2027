---
layout: page
title: Challenges
permalink: /challenges/
collection_index: challenges
kicker: '<span class="kicker__num">02</span>Section'
summary: Our More Than a Hack 2027 journey, stage by stage. The Initial Challenge is done, the roadmap shows what is in development, and the Innovative Challenge is next.
canvas: true
extra_css: [/assets/wiki/wiki.css, /assets/wiki/ch-route.css]
extra_js: [/assets/wiki/ch-route.js]
---
{%- assign stages = site.challenges | sort: "order" | where_exp: "d", "d.nav_exclude != true" -%}
<section aria-labelledby="ch-stages">
  <h2 id="ch-stages" class="visually-hidden">The stages</h2>
  <ol class="card-grid ch-stage-cards" role="list">
    {%- for doc in stages %}
    <li class="card">
      <span class="card__num" aria-hidden="true">{{ forloop.index | prepend: "0" | slice: -2, 2 }}</span>
      <h3 class="card__title"><a href="{{ doc.url | relative_url }}">{{ doc.nav_title | default: doc.title }}</a></h3>
      {%- if doc.summary %}<p class="card__text">{{ doc.summary }}</p>{% endif %}
      {%- if doc.status %}<span class="status status--{{ doc.status | slugify }}">{{ doc.status }}</span>{% endif %}
      <span class="card__arrow" aria-hidden="true">&rarr;</span>
    </li>
    {%- endfor %}
  </ol>
</section>

{% include ch-reading-route.html id="hub-route" num="R" kicker="The reading route" %}
