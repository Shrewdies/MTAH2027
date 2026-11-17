# Who has the ball?
### Decoding team possession frame by frame — The Shrewdies · More Than a Hack 2027 · Initial Challenge

| | |
|---|---|
| **Team** | 1 Yousef Fayez · 2 Mahmoud Abubakr · 3 Ahmed Awwad · 4 Abdullah Ashmawei |
| **Code** | [github.com/Shrewdies/MTAH2027](https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge), Initial Challenge in `/initial-challenge` |
| **Knowledge hub** | [theshrewdies.com](https://theshrewdies.com), the whole hackathon, hosted separately from this report |

> **In one sentence.** We read the match the way a match official would — who can actually
> play the ball, has it left the pitch, has play stopped — and then let an exact algorithm write
> the single most coherent possession story for each half, with every parameter chosen away from
> the competition match.

---

## 1. Executive summary

**What we deliver**

| | deliverable | where |
|---|---|---|
| 1 | **Per-frame labels**: 199,319 video frames, each **H** (Barcelona in possession), **A** (Athletic Club in possession) or **D** (ball dead) | the submission file, regenerated in under ten seconds on a laptop CPU, byte-identical on every run |
| 2 | **Public repository** with one-command reproduction in a pinned container | [github.com/Shrewdies/MTAH2027](https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge), `/initial-challenge` |
| 3 | **This technical report** | Markdown (this file), and the same deck as PowerPoint and PDF in `report/` |
| 4 | **Knowledge hub** for the whole hackathon | [theshrewdies.com](https://theshrewdies.com), mapped in [section 12](#12-beyond-this-report) |

- **Our key idea.** A ball the tracker cannot see is *not* a stoppage. Possession stays with the
  team that last controlled it until real evidence says otherwise, which removes the main
  failure mode of frame-by-frame approaches.
- **Measured, not assumed.** On an openly labelled Bundesliga match, degraded to look like the
  competition data, we beat the organisers' baseline method on both official metrics:
  spellF1 **0.340 vs 0.235**, macroF1 **0.693 vs 0.383**.
- **Integrity by design.** No hand labels, no training on the match, the public answers never used
  to choose anything, and the match data never leaves the laptop.

## 2. The question, for football fans

Watch any match and ask, every 1/25 of a second: *who has the ball?* A team keeps possession
through a loose ball or a scramble; it loses it only when the opponent takes **control**. When the
referee stops play — throw-in, foul, goal kick — nobody has it: the ball is **dead**.

What we are given is automatic: computer-vision tracking of 22 players and the ball, plus automatic
tactical tags ("build up", "set piece", …). Two facts make it hard:

| challenge | why it matters |
|---|---|
| The ball is **missing on 41%** of the frames that count | exactly in crowds, tackles and aerial duels — the moments that decide possession |
| Players have **no identities**, only a team | we must reason about teams, not individuals |

## 3. How we are judged, in plain words

- **spellF1 (ranking).** Each possession is treated as one object, like a sentence in a story. A
  predicted possession scores only if it overlaps a real one well. Inventing extra possessions or
  splitting real ones is punished hard.
- **macroF1 (tie-break).** Frame-by-frame correctness for H, A and D, each class counting equally.

The lesson: **coherence beats twitchiness**. A method that flickers between teams can look fine
frame by frame and still tell the wrong story.

## 4. Our approach in four ideas

**① Evidence, frame by frame.** For every frame we score three hypotheses — home, away, dead:

| signal | meaning | supports |
|---|---|---|
| a player within **1.5 m** of a ball moving slower than 7 m/s | someone can actually play it | that player's team |
| ball more than 1 m beyond a line | out of play | dead |
| players almost standing still for 3 s | play has stopped | dead |
| ball placed and motionless for 1.5 s | free kick, goal kick, kick-off | dead |
| start of a tagged set piece | restart coming | dead |
| a fast ball inside the pitch | play is live | not dead |

**② Silence is not a stoppage.** When the ball is untracked, every hypothesis scores zero — the
story simply continues. That is the challenge's own rule: during loose or contested phases
"possession stays with the last team that had it".

**③ The best story, not the best frame.** An exact dynamic-programming algorithm (**Viterbi**,
the decoder behind speech recognition and GPS map-matching) chooses the whole sequence that
maximises evidence minus a fixed cost for every change of state. A touch, a deflection or a pass
flashing past an opponent cannot flip possession; sustained control can.

**④ Two separate questions.** "Is the ball alive?" and "which team has it?" are independent, so we
keep their evidence apart. Tag information may decide *which team*, but it can never lengthen or
shorten a stoppage. A unit test guarantees it.

## 5. Making the tags speak for themselves

Fourteen tag codes name a team, but what does the team mean? For "Build up" it is the team with
the ball; for "Defending in middle third" it is the team *without* it. Instead of hand-picking
codes, the pipeline measures — **without any answers** — how often each code's team agrees with
visible ball control, and turns that into a weight (log-odds):

| code | agreement with visible control | learned weight |
|---|---|---|
| Build up | 86.5% | **+1.86** |
| Defending in attacking third | 13.5% | **−1.86** |
| Progression | 83.0% | +1.58 |
| Players in the box | 58.2% | +0.33 |

Defending codes come out as exact mirrors of attacking ones, and vague codes count for little.
Nobody told the program which is which. The tags remain a light hint (scale 0.035); visible ball
control always dominates.

## 6. Choosing the parameters: the Pareto decision log

**Why a Pareto front.** spellF1 (ranking) and macroF1 (tie-break) pull the switch costs in opposite
directions, so there is no single "best" setting. There is a **Pareto front**: the settings where
neither metric can improve without the other getting worse. The search keeps the whole front, and
an explicit rule selects from it.

**What was searched, and what was not.** Seven dials: the two switch costs and five evidence
weights. Every other constant keeps its physical meaning and its source.

| dial | what it controls | reasoned | balanced (= spell) | **macro** |
|---|---|---|---|---|
| team switch cost | clear control needed to change possession | 10.0 | 8.35 | **4.23** |
| alive/dead switch cost | evidence needed to start or end a stoppage | 20.0 | 12.50 | **9.43** |
| out-of-bounds weight | ball beyond a line | 3.0 | 2.49 | **3.30** |
| stillness weight | players standing still | 0.3 | 0.80 | **0.79** |
| stationary-ball weight | ball placed and motionless | 0.5 | 0.51 | **0.36** |
| set-piece weight | start of a tagged set piece | 0.6 | 0.56 | **0.66** |
| tag scale | weight of the calibrated tag hint | 0.1 | 0.049 | **0.035** |
| control radius | **not searched**: a physical constant | 1.5 m | 1.5 m | **1.5 m** |

The control radius is excluded on purpose. Left free, the search pushed it to 0.8 m, an artefact
of a simulator that keeps the ball unrealistically close to the carrier. It stays 1.5 m, the
default possession zone of the open-source FIFA method implementation in databallpy.

**Step 1 — explore on simulated matches.** We built a match simulator with known answers from
football rules of thumb (possessions of about 11 s, a third of them ending in a stoppage of about
20 s, the ball missing on 41% of frames). An evolutionary multi-objective search in the spirit of
NSGA-II evaluated 159 settings with the **official scorer** and froze three profiles:

| profile | chosen as | spellF1 (sim.) | macroF1 (sim.) |
|---|---|---|---|
| reasoned | our starting values | 0.606 | 0.835 |
| balanced (= spell) | best combined score | 0.638 | 0.857 |
| **macro** | best frame accuracy | 0.618 | 0.859 |

The search taught two things: **declare stoppages more readily** (lower alive/dead switch cost,
more weight on stillness), and **keep tags a light hint** (tag scale from 0.1 down to 0.035–0.049).

**Step 2 — let real labels decide.** A simulator is a hypothesis, so the final choice was made on
a real match we did not label: the open DFL Bundesliga data (CC-BY 4.0), whose every frame carries
the league's official alive/dead and possession flags. We hid the ball on 41% of frames to mirror
the competition tracking and scored everything with the official metric:

| method | spellF1 | macroF1 | possessions found (truth 402) |
|---|---|---|---|
| organisers' baseline method | 0.235 | 0.383 | 570 |
| ours, reasoned | 0.249 | 0.661 | 166 |
| ours, balanced | 0.286 | 0.686 | 186 |
| **ours, macro (submitted)** | **0.340** | **0.693** | **249** |

**The selection rule: simulate to explore, validate on real labels to decide.** On the external
match, macro beats balanced on **both** metrics, including spellF1, the ranking metric. It changes
possession more readily (team switch cost ≈ 4 frames of clear control, against ≈ 8 for balanced
and 10 for reasoned), which matches a fact the real data revealed: real matches contain many short
possessions. When the simulator and the real world disagree, we follow the real world. The
`--profile` switch keeps every alternative one argument away.

**Decision log: the design decisions behind the final pipeline.** Our rule: parameters are
fitted only on simulated matches and openly licensed external data, never on the competition match.

| decision | what it means | why |
|---|---|---|
| **Missing ball = no evidence** | an untracked ball scores zero for every state; possession stays with the last team in control | "no ball = stoppage" invents stoppages inside possessions |
| **Alive/dead separate from which-team** | tags may decide which team, never the length of a stoppage; a unit test guarantees it | hand-picked attacking tags quietly shortened stoppages |
| **Tags calibrated automatically** | weights from agreement with visible ball control, measured without any answers | defending codes come out as exact mirrors of attacking ones (+1.86 / −1.86) |
| **Control radius kept physical** | 1.5 m, outside the search | left free, the simulator pushed it to an unrealistic 0.8 m |
| **Profile chosen on real labels** | macro, selected on the labelled external match | beats balanced on both metrics: 0.340 / 0.693 vs 0.286 / 0.686 |
| **Public window: a check, not a judge** | correctness check on candidate files only | 17 possessions are too few to choose between settings (section 7) |

The search is seeded and reruns in about 15 s (command in [README.md](README.md)). Its 159 points
are frozen in `possession/pareto_front.json` and the profiles, with their provenance, in
`possession/profiles.json`.

## 7. On the competition match

Without ground truth we can still check that the output is sensible:

| | reasoned | **submitted (macro)** |
|---|---|---|
| possessions / mean length | 215 / 18.8 s | **337 / 11.5 s** |
| dead-ball share of match time | 36% | 39% |
| Barcelona's share of live play | 62% | 64% |

337 possessions is in the range of a real match (402 on the DFL match), and 39% dead time is close
to typical effective-playing-time figures in elite football.

**The public 5-minute window** served only as a correctness check on candidate files: format,
frames aligned, teams the right way round (share error 0.016 on the submitted file). It never chose
between them. For transparency: another profile scored higher there (spellF1 0.43 vs 0.36), and
we submitted macro anyway. With 17 possessions, one possession moves spellF1 by about six points,
and the organisers show that this window prefers the variant that loses on the full match. The
decision rests on the fully labelled external match.

## 8. Reproducibility: how it is ensured

| layer | how |
|---|---|
| **Container** | `python:3.11.11-slim-bookworm` pinned by sha256 digest; multi-arch (linux/arm64 and linux/amd64) |
| **Dependencies** | numpy 2.2.6 and pandas 2.2.3 plus their four dependencies, pinned in `requirements-solution.txt`. An optional offline wheels folder (`scripts/fetch_wheels.*`) builds the image with no network; the offline and the PyPI build paths were both tested |
| **Run sandbox** | `--network none`, read-only root filesystem, tmpfs `/tmp`, source and data mounted read-only; only the output folder is writable |
| **Determinism** | no randomness in decoding; byte-identical output on every run; CSV written with LF line endings; a full run takes under 10 s on a laptop CPU |
| **Frozen decisions** | parameter profiles in `possession/profiles.json`, the Pareto front in `possession/pareto_front.json`; the seeded search reruns in about 15 s |
| **Checks** | 15 behaviour tests on fabricated scenes, no data needed; the organisers' official validator runs on every produced file |
| **External validation** | reproduces from public data: DFL/IDSSE open data, CC-BY 4.0, figshare DOI 10.6084/m9.figshare.28196177 |

One command per OS:

```bash
scripts/run.sh build && scripts/run.sh test && scripts/run.sh submit "$DATA" outputs
```

Windows: `.\scripts\build.ps1`, `.\scripts\test.ps1`, `.\scripts\run_protected.ps1 -DataDir "$DATA"`.
Details in [README.md](README.md).

## 9. Data privacy and security: considered at every step

| step | what we did |
|---|---|
| **Storage** | The competition data is never committed. The repository holds no match data, `.gitignore` blocks the data paths, and [DATA.md](DATA.md) says where to place it locally |
| **Processing** | All processing of the match data happened on the team's own laptop, inside the offline container with read-only mounts. The data was never uploaded to any external service, cloud platform or hosted model, as the competition terms require |
| **Outputs** | Generated outputs live outside the repository, in a separate folder, and git ignores the output folders. Diagnostics and everything published (this report, the website) are aggregate metrics only |
| **Integrity** | No hand labels. No use of the video to label or check outputs. No tuning on any ground truth of the competition match. The public 5-minute window was a correctness check on candidate files (format, frame alignment, team orientation), never a way to choose between them |
| **Search and validation** | Parameter search and validation used only synthetic matches and openly licensed external data |
| **Supply chain** | A minimal dependency set (numpy, pandas), pinned versions, a digest-pinned base image and an offline build option |

## 10. What we tried and learned

1. **Nearest player + "no ball = stoppage"** (the baseline idea) invents stoppages inside
   possessions. → *Silence is not a stoppage.*
2. **Hand-picked attacking tags** helped the team question but quietly shortened stoppages.
   → *Separate alive/dead from which-team; calibrate all tags automatically.*
3. **Simulator-only tuning** pushed one constant to an impossible value and ranked two profiles
   the wrong way round. → *Simulate to explore, validate on real labels to decide.*

## 11. What comes next

The ball the tracker cannot see, on 41% of the frames that count, is where the next gains are.
We are going after it.

| frontier | the direction |
|---|---|
| **A single source of truth** | three witnesses of one match, video frames, tactical-camera tracking and broadcast-camera tracking, each filling the gaps of the others |
| **Ball-free reasoning** | possession read from player interactions alone, fused with the evidence decoder |
| **On-device vision** | the frames the tracker loses, seen again on the laptop's NPU |
| **Evidence learned on open labels** | weights learned from openly labelled matches, never from the competition match |
| **Duration-aware decoding** | 249 possessions found where the external match has 402: the measurable gap to close |
| **Possession as language** | the possession story turned into language, on the device |

## 12. Beyond this report

This report is one page of a much bigger playbook. It covers the Initial Challenge only; the rest
is open in the team's knowledge hub, hosted separately at
**[theshrewdies.com](https://theshrewdies.com)**.

**The squad in numbers**

<!-- squad-numbers: the counts below repeat the constants at the top of tools/report/deck.py; change both, then rebuild -->

| | |
|---|---|
| **50+** years | of professional experience, combined |
| **19** countries, **5** cultures | of professional journeys |
| **20+** patents | in the squad |
| **7** specialisms | each mapped to football intelligence |
| **23** datasets scouted | 22 atlas pages |
| **74** models, methods and tools reviewed | 47 judged pages |
| **16** architecture studies in 5 families | our DNA in architecting solutions |
| **12** insight pages | on how we read the challenge |
| **140+** knowledge pages | on theshrewdies.com |

<!-- /squad-numbers -->

**Six doors into the playbook**

<!-- squad-numbers: the doors repeat the counts of countries, specialisms, insight pages, datasets and models -->

| door | why open it |
|---|---|
| [Team](https://theshrewdies.com/team/) | four Shrewdies, 19 countries, 7 specialisms: why this mix matters for football |
| [Challenges](https://theshrewdies.com/challenges/) | 12 insight pages on how we read the problem, and the roadmap to what comes next |
| [Datasets](https://theshrewdies.com/datasets/) | 23 datasets scouted, and what each one can teach a possession model |
| [Solutions](https://theshrewdies.com/solutions/) | 74 models, methods and tools for football intelligence, mapped and judged |
| [Architecture](https://theshrewdies.com/architecture/) | our DNA in architecting football intelligence: the design space and the calls we made in it. Start with the [single source of truth](https://theshrewdies.com/architecture/single-source-of-truth/) |
| [On-device](https://theshrewdies.com/on-device/) | security, data protection and reproducibility, on our own machine and hardware |

<!-- /squad-numbers -->

Who has the ball was the first question. The roadmap at
[theshrewdies.com/challenges/roadmap/](https://theshrewdies.com/challenges/roadmap/) shows where
we take the answer in the Innovative Challenge.

## Glossary

**Possession spell** — an unbroken run of one team with the ball alive. **Viterbi** — an exact
algorithm that finds the best whole sequence instead of the best single frame. **Log-odds** — how
much more often something is right than wrong, on a scale where 0 means "no information".
**Pareto front** — the set of choices where one goal cannot improve without hurting another.
**NSGA-II** — a standard evolutionary algorithm for problems with several goals. **Digest pin** —
a container base image named by the hash of its content, so it cannot change underneath a build.

## References

Vidal-Codina et al. (2022) arXiv:2202.00804 · databallpy, possession (MIT) · Link & Hoernig (2017)
PLOS ONE 12:e0179953 · Lang et al. (2022) Scientific Reports, doi:10.1038/s41598-022-19948-1 ·
Deb et al. (2002) IEEE TEC 6(2) (NSGA-II) · Kim et al. (2026) arXiv:2602.12080 (PathCRF) ·
Bassek et al. (2025) Scientific Data 12:195 (DFL open data, CC-BY 4.0,
doi:10.6084/m9.figshare.28196177) · Komorowski et al. (2020), FootAndBall (MIT).

---

The Shrewdies · [theshrewdies.com](https://theshrewdies.com) ·
[github.com/Shrewdies/MTAH2027](https://github.com/Shrewdies/MTAH2027/tree/main/initial-challenge)
