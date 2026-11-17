---
layout: wiki-entry
nav_exclude: true
title: The rules are the architecture
kicker: Rules and proof
summary: "No hand labels. No tuning on the match. No match data in the cloud. An exact file anyone can regenerate. Read as engineering requirements, the rules design most of the system, and they decide what counts as proof."
route_label: Rules
hook: "Rules are the architecture"
group: rules
order: 110
chips: [Local only, No hand labels, Proof on external labels]
motif: ch-boundary
motif_caption: "Match data crosses one boundary only: into an offline container on one laptop. What comes out is a label file and aggregate metrics."
motif_labels: [Match data, Offline laptop, Label file, Aggregates, Hosted AI, Decoder]
facts:
  - { k: Labels on the match, v: "None, by anyone, for any purpose" }
  - { k: Public answers, v: "Correctness check only" }
  - { k: Match data, v: "Never leaves the machine" }
  - { k: Result, v: "Algorithmic and exactly reproducible" }
verdict:
  label: Our read
  text: "These rules reward the same things a club's data department needs: methods that generalise because they were never fitted to the fixture, and pipelines that can be audited and rerun. The system is built around them."
sources:
  - { title: "RULES (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md" }
  - { title: "FAQ (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/FAQ.md" }
  - { title: "SUBMISSION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/SUBMISSION.md" }
  - { title: "EVALUATION (organisers' repository)", url: "https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/EVALUATION.md" }
related:
  - /challenges/pareto-lens/
  - /architecture/evaluation-framework/
  - /on-device/security-data-protection/
  - /on-device/reproducibility/
---
## Four rules, four design consequences

| The rule | What it removes | What it produces |
|---|---|---|
| No human labels or corrections on the match, even a small validation set | Supervised learning on the fixture | Fixed football evidence and an exact decoder |
| The public five-minute answers verify a pipeline; they never train or tune it | Model selection on the match | Selection on external labels |
| No match data, and no extracts of it, to hosted or cloud AI services | Cloud GPUs, hosted models on the data | Everything computed locally |
| The scored file must be algorithmic and exactly reproducible | Manual fixes, hidden state, randomness | A deterministic, pinned pipeline |

Three more close the remaining doors. Watching the video to understand the data is fine; turning what is seen into labels or frame-specific rules is not. Outside information about this match, including third-party event or possession data, is prohibited. And the restricted data, or anything that could reconstruct it, never enters a public repository.

## What stays open

The rules are precise about what they allow, and it is a lot.

| Material | Allowed use |
|---|---|
| Other matches, openly labelled or annotated by hand | Train, tune, select, report |
| The same matches, degraded | Stress a method under the target's conditions |
| Simulated matches with known answers | Explore, search, unit-test behaviour |
| Downloaded model weights | Run on the participant's own machine, where nothing is transmitted |
| Published baseline scores | Reference points |
| The public five-minute answers | Check frame alignment and label semantics, nothing else |

Model eligibility and data transmission are separate questions. A provider's zero-retention promise is not a permission: what matters is whether the data leaves the machine, not what happens to it afterwards.

## What counts as proof

With no label on the match, a result has to be proved somewhere else. Claims in football AI come in four strengths, and mixing them is how weak systems get strong reputations.

| Level | What it is | What it proves |
|---|---|---|
| Official fact | The organisers' documents and scorer | What the task and the metric are |
| Published result | A paper's numbers on its own dataset | The method works there |
| Running code | A public repository that reproduces | The method exists and executes |
| Hypothesis | An idea with no independent test | Nothing yet |

Every number on this site sits at a stated level. Organisers' figures are cited to their documents. Our own were produced by the official, unchanged scorer on open data anyone can download.

Our proof is a ladder with one job per rung: simulated matches to explore, a real match with external labels to decide, the public window to check the file. How it ran is on [the Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}). Why it is built that way is in [Two metrics, one verdict]({{ '/architecture/evaluation-framework/' | relative_url }}). The numbers are on the [Initial Challenge]({{ '/challenges/initial-challenge/' | relative_url }}) page, and the data behind them is [DFL IDSSE open data]({{ '/datasets/dfl-idsse/' | relative_url }}).

## Where each rule lands in our build

| Rule | In the build | Read more |
|---|---|---|
| No labels | Fixed football evidence, an exact decode, seven parameters set away from the match | [The Shrewdies decoder]({{ '/architecture/the-shrewdies-decoder/' | relative_url }}) |
| Public window | Checked format, frame alignment and team orientation. Chose nothing | [The Pareto lens]({{ '/challenges/pareto-lens/' | relative_url }}) |
| Local only | An offline container on one laptop, read-only inputs, one writable output folder | [Security and data protection]({{ '/on-device/security-data-protection/' | relative_url }}) |
| Reproducible | Pinned image and dependencies, no randomness, the organisers' validator on every file | [Reproducibility]({{ '/on-device/reproducibility/' | relative_url }}) |

Nothing from the match is published. The repository holds no match data, and this site shows aggregate metrics, synthetic animations and results on open data only.

## Why we like these rules

A method fitted to one match's answers tells you about that match. A method that never saw them, and still holds up on a different league's labels, tells you about football. The constraint that looks strictest is the one that makes the result worth trusting.
