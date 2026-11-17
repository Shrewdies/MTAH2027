---
layout: wiki-entry
nav_exclude: true
title: Two cameras, two clocks
kicker: The data
summary: "The broadcast feed sees the foot on the ball. It also cuts, zooms and replays. Before it can add evidence, every one of its frames needs an honest answer to one question: when was this?"
route_label: Broadcast
hook: "Two cameras, two clocks"
group: data
order: 100
chips: [Tactical clock, Broadcast cuts, Replays]
motif: sync
motif_caption: "Two clocks, one match. A live shot can be slid into alignment; a replay cannot, because it points backwards."
motif_labels: [Tactical clock, Broadcast clock, Live shot aligned]
facts:
  - { k: Master clock, v: "Tactical video frame, from 0" }
  - { k: Broadcast records, v: "164,488 on their own index" }
  - { k: Broadcast ball, v: "Tracked on 50.5% of frames" }
  - { k: Mapping, v: "None supplied" }
verdict:
  label: Our read
  text: "Cross-view fusion is a synchronisation problem before it is a vision problem. Alignment has to be segment by segment, with confidence, and with replays treated as what they are: old news."
sources:
  - { title: "DATA (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md" }
  - { title: "FAQ (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
related:
  - /challenges/data-asset-map/
  - /challenges/homography/
  - /challenges/tactical-tracking/
  - /architecture/match-timeline/
---
## One clock rules

The answer is graded on the tactical video's frame index, starting at 0. Everything on the tactical side hangs off it with simple conventions.

| Source | Index | To tactical frame |
|---|---|---|
| Tactical tracking | Frame id from 1 | Subtract 1 |
| Tactical homography | Frame from 0 | As is |
| Smart Tagging | Seconds from clip start | Multiply by 25 and round |
| Broadcast, all files | Its own frame index | No mapping supplied |

## What the broadcast adds

A director follows the ball. The broadcast view is closer, so feet, contacts and the ball itself are larger in the image, and its tracking is a second, independent look at the same play. The ball is tracked on 50.5% of broadcast frames and its homography is usable on 65.8%.

The price is the edit: pans and zooms, cuts between cameras, close-ups with no pitch lines, graphics, and replays.

## Frame numbers do not travel

A broadcast frame cannot be equated with the tactical frame of the same number. Each kind of footage relates to match time differently.

| Footage | Relation to match time | Usable for geometry |
|---|---|---|
| Live wide shot | Runs forward at clock rate | Yes, where the homography is valid |
| Live close-up | Live, but few landmarks | Rarely |
| Replay | Jumps back to an earlier event | Only once grounded to that event |
| Slow-motion replay | Earlier event, stretched | Only once grounded and rescaled |
| Crowd, bench, graphics | No pitch correspondence | No |

A replay is the dangerous one. It shows a clean view of a turnover that has already happened, on frames that sit next to live play.

## How it plugs into possession

Our decoder runs on the tactical clock alone, which keeps every frame of evidence unambiguous in time. Verified broadcast observations fit the same design without changing it: each becomes one more piece of evidence on a tactical frame, weighted by the confidence of its alignment.

Getting there is a design problem of its own: a mapping for each live segment, a confidence on every link, and replays grounded to the passage they repeat or left out. The design is in [One clock for the match]({{ '/architecture/match-timeline/' | relative_url }}). The tools are in the [Synchronisation]({{ '/solutions/synchronization/' | relative_url }}) family.
