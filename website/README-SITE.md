# The team website: how it works

The `website/` folder of [Shrewdies/MTAH2027](https://github.com/Shrewdies/MTAH2027) is a small Jekyll
site that GitHub Pages builds and publishes at [theshrewdies.com](https://theshrewdies.com). You edit
plain text files; `.github/workflows/pages.yml` publishes them a minute or two after each change to
`website/` on `main`.

## What is where

```
website/
├─ index.html              home: logo hero, team intro, challenge journey, animation, squad teaser, sections
├─ team.md, challenges.md, on-device.md
│                          one landing page per section (lists its pages automatically,
│                          or shows an animated "coming soon" block while it is empty)
├─ datasets.md, solutions.md, architecture.md
│                          hubs of the three knowledge sections (see "Wiki pages")
├─ datasets/, solutions/, architecture/
│                          one family page per family of each hub, e.g. datasets/possession.md
├─ brand.md                colours, logo and motion reference page
├─ _team/                  pages of the "Team" section
├─ _challenges/            Initial Challenge, Innovative Challenge and their background pages
├─ _datasets/              one page per dataset
├─ _solutions/             one page per model, method or tool, in one sub-folder per category
├─ _architecture/          one page per architecture study
├─ _ondevice/              Security & Data Protection, Reproducibility, Machine & Hardware
├─ redirects/              old addresses that forward to their new page
├─ _data/team.yml          team members for the squad cards
├─ _data/results.yml       the external-validation table on the Initial Challenge page
├─ _config.yml             site title, links, list of sections
├─ _layouts/, _includes/   page templates (no need to touch for content changes);
│                          wiki-entry.html, wiki-hub.html and _includes/wiki/ are the wiki kit
└─ assets/
   ├─ wiki/                wiki.css, wiki.js (wiki pages and their animated diagrams)
   ├─ brand/               tokens.css, wordmark, favicon, stage motifs, BRAND.md guide
   ├─ hero/                the "Who has the ball?" animation
   ├─ css/                 site.css, stage.css (background), logo.css, team.css
   └─ js/                  site.js, stage.js (background), logo.js, team.js
```

## Add or edit a page

1. Open the folder of the section, for example `website/_ondevice/` (create it if it does not exist yet).
2. Add a `.md` file named with lowercase words and dashes: `my-new-page.md`. The name becomes the
   web address (`/on-device/my-new-page/`).
3. Start it with a block between two `---` lines (`title`, `order`, `summary`), then write the page in
   Markdown: `## Heading`, `**bold**`, `- list item`, tables with `|`.
4. Save and commit. The page appears in the top menu and on its section page automatically, and the
   section's "coming soon" block disappears.

Pages in Datasets, Solutions and Architecture use a richer template with its own fields: see
[Wiki pages](#wiki-pages-datasets-solutions-architecture).

If a value contains a colon (`:`), wrap it in double quotes.

Optional front matter on any page:

| key | effect |
|---|---|
| `status: Draft` | label next to the title and on cards (`Done`, `Coming soon`, `Draft` …) |
| `coming_soon: true` | shows the animated "coming soon" block under the title |
| `coming_soon_text: "…"` | the sentence inside that block |
| `canvas: true` | content is laid out by the page itself (wide visual blocks) instead of a text card |
| `nav_exclude: true` | keeps the page out of menus and section lists |

### Simple page (`_ondevice/<name>.md`, `_team/<name>.md`)

```yaml
---
title: Reproducibility
order: 2                  # position in the menu and on the section page
summary: One sentence shown on cards and under the title.
status: Draft             # optional
---
```

**New section:** create a folder such as `_talks/`, add it in `_config.yml` under both `collections:`
and `sections:` (copy an existing entry; `soon:` is the coming-soon sentence), and add a landing page
like `on-device.md`.

## Wiki pages (Datasets, Solutions, Architecture)

The three knowledge sections share one kit: an **entry** template for single pages, a **hub** template
for the landing pages and the family pages, and a library of small animated diagrams called **motifs**.
Each section is read in three steps: the hub shows its families, a family page explains one family and
lists its entries, an entry covers one dataset, solution or architecture study.

Pages in `_datasets/`, `_solutions/` and `_architecture/` use the entry template automatically and stay
out of the top menu (the menu lists the families instead, from `sections[].families` in `_config.yml`);
a page in `_challenges/` opts in with `layout: wiki-entry`.

| File | Role |
|---|---|
| `_layouts/wiki-entry.html` | one dataset, solution, architecture study or challenge note |
| `_layouts/wiki-hub.html` | section hub (families), family page, or a plain grouped list |
| `_includes/wiki/motif.html` | puts one motif in a framed stage, in a layout or inside Markdown |
| `_includes/wiki/motifs/<id>.html` | the motifs, one inline SVG each |
| `_includes/wiki/glyph.html` | the small animated glyph on cards and group headings |
| `_includes/wiki/` (others) | cards, group blocks, search lines, sorting: used by the two layouts |
| `assets/wiki/wiki.css`, `wiki.js` | styles, motion, search, count-up; loaded by the two layouts |

### Entry page

Copy this into `_datasets/<name>.md`, `_architecture/<name>.md` or `_solutions/<category>/<name>.md`.
Only `title` is required; a block whose field is missing is simply not shown.

```yaml
---
title: PathCRF
kicker: Direct possession            # small label above the title
summary: One-sentence lede, also shown on cards.
group: direct-possession             # category key; hubs group by it
order: 10                            # position inside the group (then by title)
chips: [Tracking, Ball-free, MPL-2.0]   # short tags; cards show the first four
motif: graph                         # animated diagram, see the library below
motif_caption: Caption under the diagram.
motif_labels: [Carrier, Pass, Receiver]  # up to 6 short labels drawn inside the motif
facts:
  - { k: Modality, v: 25 Hz tracking }
  - { k: Licence, v: MPL-2.0 }
verdict: { label: Our read, text: "One or two sentences of judgement." }
call:                                # only on pages where we made a decision
  title: Why it stayed off the pitch
  constraint: Competition rules      # the real constraint, shown as a chip
  text: "Two or three sentences."
sources:
  - { title: "Paper (KDD 2026)", url: "https://example.org/paper" }
related:
  - /solutions/direct-possession/borghesi-possession-tcn/
  - /datasets/dfl-idsse/
---

## What it is

Body text in Markdown: `##` headings, lists, tables, code, quotes.
```

The page is laid out in this order: breadcrumb, kicker, title, summary, chips; the motif; the fact
grid; the Markdown body; the verdict; the "Our call" box; sources; related cards; previous and next
within the same family; a link back to the hub. The breadcrumb reads Home / section / family / page,
and the family links to its family page (the `url` of that group in the hub's `groups`).

| Field | Notes |
|---|---|
| `title` | required |
| `kicker` | defaults to the group title, then the section title |
| `summary`, `facts`, `verdict.text`, `call.text` | plain text; inline HTML such as `<code>` is allowed |
| `group`, `order` | previous and next links stay inside the group; pages without `order` come last |
| `verdict` | `{ label, text }`, or just a sentence (the label is then "Our read") |
| `call` | `title`, `constraint`, `text`; optional `label` replaces "Our call" |
| `sources` | `{ title, url }`; `url` may be left out, or be a path on this site |
| `related` | addresses on this site, any section; one that does not exist yet is skipped |
| `icon` | optional: built-in motif id for the animated glyph on the page's cards. Without it a custom `motif` gets a generic glyph |
| `status` | optional label next to the kicker, as on other pages |
| `section` | optional, for a wiki-entry page outside a collection: the section it belongs to |

Start body headings at `##` (the title is the only `#`). Wide tables scroll inside their own frame.
A body with two or more `##` headings gets an "On this page" list on wide screens.

### Section hub (families)

A hub is an ordinary page in the `website/` folder, for example `datasets.md`. With `families: true`
it shows the families, not every entry:

```yaml
---
layout: wiki-hub
title: Datasets
permalink: /datasets/
collection_index: datasets           # the folder to list, without the underscore
families: true
summary: Lede.
motif: stack
motif_labels: [Video, Tracking, Events, Labels]
stats:                               # optional row; numbers count up once
  - { value: "{count}", label: datasets mapped }   # {count} = number of entries listed
  - { value: "6", label: families }
groups:                              # one item per family, in display order
  - key: possession                  # the `group:` value of its entries
    title: Possession labels
    url: /datasets/possession/       # the family page
    motif: ribbon                    # live diagram on the family card
    motif_labels: [Noisy frames, Decoded spells, Home, Away, Dead ball]
    blurb: "One or two sentences on what the family is."
    points:                          # up to three short insights
      - Only one release labels all three states
      - Use it as a judge first and a teacher second
featured: [/datasets/dfl-idsse/]     # optional "Start here" row of entry cards
---

Optional Markdown here becomes an intro panel under the hero. Keep it short.
```

The hub shows the hero, the stats, the intro, then one large card per family: its motif running live,
title, blurb, points, the number of entries in the family and a button to the family page (the whole
card is the link). The `featured` entries follow, then "Find a page": a search box over every entry of
the section, with results appearing as you type. Without JavaScript the box is replaced by a closed
"All N pages" list of plain links.

| Field | Notes |
|---|---|
| `groups[].url` | the family page; if left out, the kit looks for a page with `only_group: <key>` |
| `groups[].cta` | optional button text (default "Open the family") |
| `families_title` | optional heading above the family cards (default "The families") |
| `featured_title` | optional heading of the featured row (default "Start here") |
| `kicker`, `chips`, `motif_caption` | as on entry pages |

The same list must be mirrored under `sections[].families` in `_config.yml` (title and url): the top
menu reads it from there.

### Family page

One page per family, for example `datasets/possession.md`. Its Markdown body is the real explanation
of the family and comes before the entries:

```yaml
---
layout: wiki-hub
title: Possession labels
permalink: /datasets/possession/
nav_exclude: true
collection_index: datasets
only_group: possession               # the family's key
family: true
parent: /datasets/                   # the section hub
kicker: Datasets family
summary: Lede.
motif: ribbon
motif_labels: [Noisy frames, Decoded spells, Home, Away, Dead ball]
motif_caption: Caption under the hero diagram.
stats:                               # optional
  - { value: "{count}", label: datasets }
---

## What this family is for

Tight prose, short comparison tables, and diagrams placed where they explain something:

{% include wiki/motif.html id="decoder" labels="Home|Away|Dead ball|Decoded path" caption="What to notice." %}

<div class="wiki-figures" markdown="0">
{% include wiki/motif.html id="sync" labels="Video clock|Tracking clock|Aligned" caption="First this." %}
{% include wiki/motif.html id="gauge" caption="Then this." %}
</div>
```

The page shows the breadcrumb Home / section / family, the hero with the motif, the stats, the body as
an explanation panel, the family's entries as cards ("In this family"), the previous and next family
in the order of the parent hub's `groups`, and a link back to the hub. `title`, `summary`, `motif` and
`motif_labels` fall back to the family's item in the parent's `groups` when left out.

Inside the body, a motif on its own line is set at reading width; wrap two in
`<div class="wiki-figures" markdown="0">` to place them side by side on wide screens (they stack on
phones). Labels given to the include inside Markdown are one string separated by `|`.

| Field | Notes |
|---|---|
| `parent` | the hub this family belongs to; without it the kit uses the section's main hub |
| `entries_title` | optional heading above the entry cards (default "In this family") |

### Plain list hub

Without `families: true` a hub lists every entry, grouped by `group` in the order of `groups`, under a
filter bar (group chips and a text box that searches titles, summaries and chips). A group key that is
not declared still gets its own block after the declared ones, and entries without a group land in
"Other". Without JavaScript the chips are plain jump links and the list is complete. `groups[].short`
gives a chip a shorter name. A page with `only_group` but without `family: true` lists that one group
under a search box. An empty collection shows the "coming soon" block.

### Cards

Entry cards (featured rows, family pages, related entries, list hubs) carry a small animated glyph of
the entry's motif type instead of a full motif. It moves while the card is on screen, hovered or
focused, and rests as a complete drawing when motion is paused or reduced. An entry whose `motif` is a
custom one gets a generic glyph unless it names a built-in type in `icon:`.

### Motif library

One line puts a motif anywhere (entry and hub pages do it for you from `motif:`):

```liquid
{% include wiki/motif.html id="ribbon" labels=page.motif_labels caption="What to notice." %}
```

`labels` is a list (`labels=page.motif_labels`) or one string separated by `|` (`labels="A|B|C"`), which
is the form to use inside a Markdown body. Several motifs can share a page.

Labels are optional: each motif has sensible defaults. They are positional, in this order:

| id | Shows | Labels, in order |
|---|---|---|
| `graph` | player-interaction graph with a pass in motion | carrier, pass, receiver |
| `ribbon` | noisy per-frame strip above the clean decoded strip | top strip, bottom strip, home, away, dead ball |
| `decoder` | three-state trellis, best path lighting up | state 1, state 2, state 3, best path |
| `boxes` | detection boxes on players and ball | player, ball |
| `tracks` | moving dots with identity trails | track id, trail |
| `homography` | camera trapezoid mapped to a pitch rectangle | image side, transform, pitch side |
| `sync` | two timelines sliding into alignment | first clock, second clock, aligned |
| `field` | pitch-control regions pulsing | first team, second team |
| `trajectory` | ball arc with an uncertainty ellipse | observed, predicted, uncertainty |
| `spikes` | event spikes on a timeline | three event types |
| `stack` | four data layers | the layers, top to bottom |
| `pipeline` | four to six stages with pulses flowing | one per stage (fewer than four: defaults) |
| `ensemble` | several strips voting into one | four models, the vote, the result |
| `pareto` | scatter with the frontier drawing in | x axis, y axis, frontier, chosen point |
| `tree` | feature table feeding a decision tree | table, tree, classes |
| `changepoint` | signal with detected change-points | signal, change-point, regimes |
| `matrix` | comparison grid, cells lighting | up to five column headings |
| `camera` | several cameras around a pitch | four camera names |
| `gauge` | confidence dial with provenance ticks | the reading, then three sources |
| `timeline` | two halves with gaps and an offset | first half, second half, gap, offset |

Keep labels short (about 12 characters; long ones are cut). An unknown id draws a neutral pitch motif.
Entry cards never embed a motif: they show a small animated glyph of the same type (see "Cards").

Motifs animate only transform, opacity and stroke-dashoffset. They pause while off screen, show a
complete still frame when the visitor pauses motion with the site's button or prefers reduced motion,
and are hidden from screen readers (the caption carries the meaning).

**Adding a motif.** Create `_includes/wiki/motifs/<prefix>-<name>.html` with the prefix of its section
(`ds-`, `sol-`, `bp-` or `ch-`) and use that file name as the `motif:` id. Ids with one of these
prefixes are trusted to exist: a missing file stops the build. The file is a single inline SVG:

```liquid
{%- assign L = include.labels -%}
<svg class="wm" viewBox="0 0 640 400" aria-hidden="true" focusable="false">
  <path class="wm-ln wm-ln--dash" d="M80 300H560"/>
  <path class="wm-flow" d="M80 300H560" pathLength="100"/>
  <circle class="wm-lime wm-ping" cx="560" cy="300" r="10"/>
  <text x="80" y="340">{{ L[0] | default: "Signal" | escape }}</text>
</svg>
```

Draw the finished picture first: what the SVG shows with no animation is the still frame. Then add
motion classes from `assets/wiki/wiki.css` rather than new keyframes.
Colour comes from classes, which win over `fill=""` and `stroke=""` attributes on the same element.
An element that carries a `transform=""` attribute must not also carry a motion class: wrap it in a
`<g>` and animate the group. Prefix any `id` inside the SVG with `{{ include.uid }}`.

| Classes | Purpose |
|---|---|
| `wm-h`, `wm-a`, `wm-d`, `wm-lime`, `wm-white`, `wm-ink` | fills: home blue, away garnet, dead-ball mauve, lime, white, navy |
| `wm-ln` + `--bold`, `--dash`, `--lime`, `--white`, `--mauve`, `--h`, `--a` | lines; the colour modifiers recolour any stroke |
| `wm-panel`, `wm-node`, `wm-ring`, `wm-box`, `wm-edge`, `wm-ticks` | frames, graph nodes, lime rings, detection boxes, white outline, ruler ticks |
| `wm-t--s`, `--xs`, `--tight`, `--lime`, `--dim`, `--ink`, `--disp`, `--num`, `--big` | text sizes and colours (text is mono capitals by default) |
| `wm-flow` (+ `--white`) | a pulse running along a path (`pathLength="100"`) |
| `wm-draw` | a path drawing itself in, then holding (`pathLength="100"`) |
| `wm-travel` + `wm-trail` | a mark moving in from `--fx`, `--fy` to its place, and the straight line it leaves behind |
| `wm-pop`, `wm-grow`, `wm-light`, `wm-late` | staged reveals: scale in, rise from the baseline, light up in turn (`--i`, `--step`), appear in the second half of the cycle |
| `wm-pulse`, `wm-ping`, `wm-breathe`, `wm-float`, `wm-swing`, `wm-blink` | endless loops: glow, radar ring, gentle scale, drift, rotation between `--from` and `--to`, blink |
| `wm-shift`, `wm-slide`, `wm-step`, `wm-lob`, `wm-wipe`, `wm-hold`, `wm-ends`, `wm-lit` | slides, wipes and sequences used by `sync`, `ensemble`, `trajectory`, `ribbon` and `pipeline`; read those files for the pattern |

Timing is set per element with inline custom properties: `--dur`, `--delay`, `--i`, `--step`.
`{% include wiki/pitch-lines.html x=40 y=50 scale=1 %}` draws a top-down pitch backdrop (560 by 290
before scaling) inside any motif.

## Embed an animation

Put the file in `website/assets/` (for example `assets/hero/`), then add one line to any page:

```liquid
{% include motion.html src="/assets/hero/hero.svg" caption="What the viewer should notice." %}
```

Works with `.svg`, `.gif`, `.webp`, `.png` (images), `.mp4` / `.webm` (silent looping video, with a
pause button) and `.json` (Lottie). Optional extras: `ratio="16 / 10"`, `alt="description"`,
`poster="/assets/hero/hero-poster.png"` for videos. If the file is missing, the page still builds and
shows a tidy "on its way" panel instead.

The animated "coming soon" block can also be placed anywhere:

```liquid
{% include coming-soon.html title="Heatmaps" text="One sentence on what is coming." %}
```

## Preview on your own computer (optional)

With Docker running, from the `website` folder:

```bash
docker run --rm -it -p 4000:4000 -v "$PWD:/site" -w /site ruby:3.3 \
  sh -c "gem install github-pages webrick --no-document && jekyll serve --host 0.0.0.0 --baseurl ''"
```

Then open http://localhost:4000. The first run takes a few minutes to install. Changes to
`_config.yml` need a restart of the preview.
