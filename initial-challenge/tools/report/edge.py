"""Thin wrappers around headless Microsoft Edge: screenshot HTML or SVG to PNG.

Edge ships with Windows, so the report needs no LaTeX, no wkhtmltopdf and no Node toolchain.
Set EDGE=/path/to/msedge (or chrome) to use another Chromium build.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

FONTS_LINK = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:'
              'wght@600;800;900&family=JetBrains+Mono:wght@400;600&family=Manrope:wght@400;500;700;800&display=swap">')

_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/microsoft-edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]


def edge_binary() -> str:
    env = os.environ.get("EDGE")
    if env:
        return env
    for c in _CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("msedge") or shutil.which("chrome") or shutil.which("chromium")
    if not found:
        raise SystemExit("Microsoft Edge (or another Chromium) not found; set EDGE=/path/to/browser")
    return found


def _run(args: list[str]) -> None:
    # A private profile keeps the build away from the user's browser profile and running windows.
    with tempfile.TemporaryDirectory(prefix="edge-profile-") as profile:
        cmd = [edge_binary(), "--headless", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               "--disable-extensions", "--hide-scrollbars", f"--user-data-dir={profile}",
               "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw", *args]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def screenshot(html: Path, png: Path, width: int, height: int, scale: float = 2.0, transparent: bool = False) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    if png.exists():
        png.unlink()
    extra = ["--default-background-color=00000000"] if transparent else []
    _run([f"--window-size={width},{height}", f"--force-device-scale-factor={scale}", *extra,
          f"--screenshot={png}", html.resolve().as_uri()])
    if not png.exists():
        raise SystemExit(f"Edge did not write {png}")


def svg_to_png(svg: Path, png: Path, width: int, height: int, *, scale: float = 2.0,
               background: str | None = None, workdir: Path) -> None:
    """Render an SVG at an exact CSS size. The SVG is inlined so the web fonts apply to its text."""
    markup = svg.read_text(encoding="utf-8")
    bg = background or "transparent"
    page = (f"<!doctype html><html><head><meta charset='utf-8'>{FONTS_LINK}<style>"
            f"html,body{{margin:0;padding:0;background:{bg};overflow:hidden}}"
            f"svg{{display:block;width:{width}px;height:{height}px}}</style></head>"
            f"<body>{markup}</body></html>")
    workdir.mkdir(parents=True, exist_ok=True)
    tmp = workdir / f"_{svg.stem}.html"
    tmp.write_text(page, encoding="utf-8")
    try:
        screenshot(tmp, png, width, height, scale, transparent=background is None)
    finally:
        tmp.unlink(missing_ok=True)
