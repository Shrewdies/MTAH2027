# README hero animation

`make_hero.py` draws `assets/hero/hero.svg`: a 14-second loop of a choreographed, entirely
synthetic 11 v 11 play, and the possession labels our decoder assigns to it.

Nothing on the timeline is drawn by hand. The script builds the play as a
`possession.inputs.Tracking` (positions in metres, ball missing during the tracking gap), runs
`possession.decoder.decode` with the submitted `macro` profile, and shows exactly what comes back:

* **decoded** lane and the badge: the Viterbi labels (H / A / D);
* **per frame** lane: the strongest evidence of each frame on its own (dots = ball not tracked);
* **evidence this frame** panel: the decoder's own features (`decoder.features`), with the weights
  from the profile.

The decoder sees three back-to-back copies of the loop and the middle copy is shown, so the loop
seam is decoded like any other frame. A tagged `SET PIECES` window brackets the throw-in, as Smart
Tagging would provide on a real match.

## Regenerate

```powershell
python -m venv tools\hero\.venv          # .venv is git-ignored
tools\hero\.venv\Scripts\python -m pip install -r tools\hero\requirements.txt
tools\hero\.venv\Scripts\python tools\hero\make_hero.py --report            # hero.svg only
tools\hero\.venv\Scripts\python tools\hero\make_hero.py --report --raster   # + gif, webp, poster
```

`--raster` screenshots the SVG in headless Edge or Chrome (`HERO_BROWSER` overrides the path) with
its SMIL timeline paused at each frame, so `hero.gif`, `hero.webp` and `hero-poster.png` are the SVG
itself, not a second drawing. It takes a few minutes. `--report` prints the decoded runs and the
evidence features, which is the quickest check after changing the choreography.

Output is deterministic (fixed seed, no clock). The SVG uses SMIL only: no script, no external
fonts or images, so GitHub renders it animated inside `<img>`.

## Changing the play

Story beats are the `T_*` constants; scripted players are `ACTORS` (waypoints in metres, home
attacks left to right, `y = 0` is the top touchline); the ball follows `BALL_SCRIPT` and flies
between holds. The other 18 players hold a team shape that slides with the ball. After an edit,
check `--report`: the touch must stay below the switch cost (a few frames), and the dead-ball
spell should show `still` frames.
