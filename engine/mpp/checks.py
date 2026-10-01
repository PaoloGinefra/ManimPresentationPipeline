"""What a person would catch by clicking through a deck, checked without a person.

- `static`: the storyboard's own problems, and beats in the order with no scene. Needs no render.
- `lint`: text over text, text off the frame, as found by the build's check pass at every click.
- `seams`: the last frame of each slide against the first frame of the next. A click should start
  from exactly the picture the previous click held, so the two match up to encoding noise; a large
  difference is a cut (a stale handoff, a headline that pops, a picture that jumps).

Frame counts need no check here: a beat that plays a different number of clicks than its storyboard
lists fails to build.
"""

import json
from pathlib import Path

from .build import beat_sources
from .project import Talk


def static(talk: Talk) -> list[str]:
    """Problems that make the talk wrong: the storyboard's own, and a beat of the talk with no scene."""
    sb = talk.storyboard()
    found = sb.problems()
    sources = beat_sources(talk)
    found += [f"{b} has no scene in 6-build/beats/" for b in sb.order if b in sb.data and b not in sources]
    return found


def warnings(talk: Talk) -> list[str]:
    """What is missing but does not make the talk wrong: a backup beat with no scene is left out of the
    deck, and its slide numbers stay reserved."""
    sb = talk.storyboard()
    sources = beat_sources(talk)
    return [f"backup {b} has no scene: left out of the deck" for b in sb.backup if b in sb.data and b not in sources]


def lint(talk: Talk, quality: str = "draft") -> list[str]:
    """Layout findings, less those the author has looked at and accepted: talk.toml [check] accept, a
    list of findings exactly as reported (say "B21.4: overlap 23%: 'a' / 'b'"), each with its reason in
    a comment beside it."""
    folder = talk.renders(quality) / "lint"
    accepted = set(talk.config().get("check", {}).get("accept", []))
    order = talk.storyboard().sequence()
    out = []
    for b in order:
        f = folder / f"{b}.txt"
        if f.exists():
            out += [line for line in dict.fromkeys(f.read_text().splitlines()) if line and line not in accepted]
    return out


def _frames(path: Path, which: str):
    """The first or last decoded frame of a slide video, as an array."""
    import av

    first = last = None
    for i, f in enumerate(av.open(str(path)).decode(video=0)):
        if i == 0:
            first = f
        last = f
    return (first if which == "first" else last).to_ndarray(format="rgb24")


def seams(talk: Talk, quality: str = "draft", threshold: float = 2.0, sheet: Path | None = None):
    """Every seam as (from ID, to ID, mean absolute difference 0-255), and those above `threshold`.
    With `sheet`, the worst flagged seams are written side by side to that image."""
    import numpy as np

    renders = talk.renders(quality)
    slides = []
    for b in talk.storyboard().order:
        f = renders / "slides" / f"{b}.json"
        if not f.exists():
            continue
        for i, s in enumerate(json.loads(f.read_text())["slides"], 1):
            p = Path(s["file"])
            slides.append((f"{b}.{i}", p if p.is_absolute() else renders / p))
    rows, bad = [], []
    for (na, fa), (nb, fb) in zip(slides, slides[1:]):
        x, y = _frames(fa, "last").astype(float), _frames(fb, "first").astype(float)
        d = float(np.abs(x - y).mean()) if x.shape == y.shape else 999.0
        rows.append((na, nb, d))
        if d > threshold:
            bad.append((d, na, nb, x, y))
    if sheet and bad:
        from PIL import Image, ImageDraw

        bad.sort(key=lambda t: -t[0])
        worst = bad[:12]
        img = Image.new("RGB", (960, 270 * len(worst)), "white")
        for k, (d, na, nb, x, y) in enumerate(worst):
            for j, im in enumerate((x, y)):
                t = Image.fromarray(im.astype("uint8")).resize((480, 270))
                ImageDraw.Draw(t).text(
                    (4, 256), f"{na} end" if j == 0 else f"{nb} start   diff {d:.1f}", fill=(200, 0, 0)
                )
                img.paste(t, (j * 480, k * 270))
        img.save(sheet)
    return rows, [(na, nb, d) for d, na, nb, _, _ in bad]
