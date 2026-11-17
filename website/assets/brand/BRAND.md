# The Shrewdies — brand system: "Floodlit Blaugrana"

One set of files for the website, the written reports and the slides. Everything in this folder is
self-contained: no build step, no external references inside the SVGs, and fonts fall back to
system faces when the web fonts are not available (offline, print, PDF export).

| file | what it is |
|---|---|
| `tokens.css` | colours, gradients, type scale, spacing, radii, glass and paper surfaces, motion, as CSS custom properties |
| `wordmark.svg` | the logo: the "The Shrewdies" wordmark. Animated on the site by `_includes/logo.html` |
| `favicon.svg` | browser tab icon |
| `motif-ball.svg` | abstract ball used by the background stage (silver sphere, lime/blue/garnet swirls) |
| `motif-boot.svg` | abstract boot silhouette used by the background stage (silver upper, lime sole and seam) |

The wordmark is the logo; there is no separate symbol or mark.

## Colour

| token | hex | role |
|---|---|---|
| `--sh-blue` | `#004D98` | Blaugrana blue; start of the floodlit gradient; home state `H` |
| `--sh-blue-bright` | `#2F86F0` | floodlit blue, for light and glows |
| `--sh-violet` | `#6E4C9F` | where blue meets garnet |
| `--sh-garnet` | `#A50044` | Blaugrana garnet; end of the gradient; away state `A` |
| `--sh-garnet-bright` | `#E5336F` | floodlit garnet, for light and glows |
| `--sh-mauve` | `#B9A2D8` | soft light |
| `--sh-lime` | `#C4F000` | the hype accent: glows, strokes, highlights, CTAs, motion trails |
| `--sh-silver` / `--sh-silver-2` | `#E9EDF5` / `#B8C2D3` | shine |
| `--sh-navy` | `#0A1F44` | the deepest tone; small doses only; text on lime and on paper |
| `--sh-offwhite` / `--sh-white` | `#F7F6FB` / `#FFFFFF` | text on the gradient and on glass |

`--sh-black` is kept for compatibility and now holds night navy `#0B1433`; it is never a background.
Dead ball `D` uses ink `#3A4372`.

Gradients: `--sh-grad-floodlit` (the page), `--sh-grad-violet`, `--sh-grad-dusk`, `--sh-grad-lime`,
`--sh-grad-shine` (silver), `--sh-grad-tricolour` (blue, lime, garnet rules), `--sh-grad-stripes`.

### Rules

1. **Bright, never black.** Pages sit on the floodlit gradient with mauve light, white floodlights and
   lime glows. Navy is the deepest tone and is used sparingly.
2. **Lime is generous.** Glows, outlines, highlights, primary buttons, trails, key numbers. On white,
   lime is a fill or highlighter behind navy text, never text itself.
3. **Text sits on glass or paper.** Long text goes on `--sh-glass` (translucent navy, backdrop blur,
   white text) or `--sh-paper` (bright off-white, navy text). Large headings may sit on the gradient
   with a soft navy scrim.
4. **Colour only.** Club colours are referenced as colour. No club, league or company crests, logos,
   trademarks or real kit replicas, anywhere.

### Contrast (WCAG 2.x)

| pair | ratio |
|---|---|
| white on `--sh-glass` over the brightest stage light | ≥ 6:1 |
| `#E1E6F2` muted text on `--sh-glass` | ≥ 5:1 |
| navy on paper | 15.5:1 |
| `#3D4670` muted on paper | 8.9:1 |
| blue `#004D98` link on paper | 8.4:1 |
| garnet `#A50044` on paper | 7.1:1 |
| navy on lime | 12:1 |
| white on blue / on garnet | 8.6:1 / 7.0:1 |

## Type

| role | face | weights | fallback stack |
|---|---|---|---|
| Display: headlines, numbers | Big Shoulders Display | 800, 900 | Bahnschrift Condensed, Arial Narrow, Impact |
| Text: body and interface | Manrope | 400, 500, 700, 800 | Segoe UI, system-ui, Roboto, Arial |
| Mono: labels, kickers, figures, code | JetBrains Mono | 400, 600 | Cascadia Mono, Consolas, Menlo |

All three are open-licence Google Fonts:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=JetBrains+Mono:wght@400;600&family=Manrope:wght@400;500;700;800&display=swap">
```

## Motion

The site's background stage (`_includes/stage.html`, `assets/css/stage.css`, `assets/js/stage.js`)
layers a drifting gradient mesh, diagonal sheen bands, two floodlight beams, a perspective pitch that
draws itself in and drifts, a curling-ball trajectory, stud marks, two boots (one kicking with lime
trails, one spinning), a bouncing ball with squash and stretch, and lime sparks.

- Only `transform` and `opacity` animate (the pitch lines draw once on load).
- It pauses when the tab is hidden and from the round button in the bottom corner; the choice is
  remembered and adds `sh-motion-paused` to `<html>`.
- With `prefers-reduced-motion: reduce` it shows a still composition.
- Phones get fewer motifs.

`--sh-ease-out`, `--sh-ease-snap` and `--sh-dur-*` keep interface motion consistent.
