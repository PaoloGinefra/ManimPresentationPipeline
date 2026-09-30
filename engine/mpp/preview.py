"""Stills for the author: the hold frame of chosen slides, and the specimen, each on one standalone page.

A still is the last frame of a slide's draft video: the picture the presenter holds, and the page the
static PDF shows. The whole talk is built first (cached beats cost nothing), because a beat opens on
its predecessor's picture and a partial build could show a stale one.
"""

import base64
import io
import json
import subprocess
from pathlib import Path

from . import page
from .build import build, environment
from .checks import _frames
from .project import ENGINE, Talk
from .storyboard import Frame, Storyboard


def select(sb: Storyboard, refs: list[str]) -> list[Frame]:
    """Slide numbers ("7"), ranges ("7-12"), frame IDs ("B3.2") or whole beats ("B3"), in talk order."""
    frames = sb.frames()
    chosen = set()
    for ref in refs:
        if "-" in ref and all(p.isdigit() for p in ref.split("-", 1)):
            lo, hi = map(int, ref.split("-", 1))
            hit = [f for f in frames if lo <= f.number <= hi]
        elif ref in sb.data and ref in sb.sequence():
            hit = [f for f in frames if f.beat == ref]
        else:
            hit = [sb.resolve(ref)]
        if not hit:
            raise KeyError(f"no slide matches {ref!r}")
        chosen.update(f.number for f in hit)
    return [f for f in frames if f.number in chosen]


def png(array) -> str:
    from PIL import Image

    buf = io.BytesIO()
    Image.fromarray(array).save(buf, format="PNG", optimize=True)
    return f'<img alt="" src="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}">'


def hold(talk: Talk, frame: Frame):
    renders = talk.renders("draft")
    slides = json.loads((renders / "slides" / f"{frame.beat}.json").read_text())["slides"]
    p = Path(slides[frame.index - 1]["file"])
    return _frames(p if p.is_absolute() else renders / p, "last")


def preview(talk: Talk, refs: list[str], changed: bool = False) -> tuple[Path, list[Frame]]:
    build(talk, export=False)
    sb = talk.storyboard()
    renders, out = talk.renders("draft"), talk.exports()
    stamps = json.loads((renders / "stamps.json").read_text())
    seen_file = out / "preview-stamps.json"
    seen = json.loads(seen_file.read_text()) if seen_file.exists() else {}
    if changed:
        frames = [f for f in sb.frames() if f.beat in stamps and stamps[f.beat] != seen.get(f.beat)]
    else:
        frames = select(sb, refs)
    frames = [f for f in frames if (renders / "slides" / f"{f.beat}.json").exists()]
    body = "".join(
        f"<div class='frame'><div class='screen'>{png(hold(talk, f))}</div>"
        f"<div class='text'><p class='id'>slide {f.number} · {f.id}</p>"
        f"<p><strong>{page.esc(f.head)}</strong></p><p>{page.esc(f.narration.replace('**', ''))}</p></div></div>"
        for f in frames
    )
    seen.update({f.beat: stamps[f.beat] for f in frames})
    out.mkdir(parents=True, exist_ok=True)
    seen_file.write_text(json.dumps(seen, indent=1))
    what = "changed since the last preview" if changed else " ".join(refs)
    title = talk.config().get("title") or "Talk"
    path = page.write(
        out / "preview.html",
        f"{title}: preview",
        f"{len(frames)} stills ({page.esc(what)}), built at {page.esc(environment(talk, 'draft')['MPP_DRAFT'])}. "
        "Each still shows the commit its beat was rendered at; slide numbers are the same at both.",
        body or "<p>Nothing to show.</p>",
    )
    return path, frames


def specimen(talk: Talk) -> Path:
    """Render the engine's specimen and every scene in the talk's 5-design/specimen.py as stills."""
    import ast

    renders = talk.renders("final") / "specimen"
    env = environment(talk, "final")
    scenes = [(ENGINE / "specimen.py", "Specimen")]
    own = talk.path("5-design/specimen.py")
    if own:
        scenes += [(own, n.name) for n in ast.parse(own.read_text()).body if isinstance(n, ast.ClassDef)]
    body = []
    for file, scene in scenes:
        r = subprocess.run(
            ["manim", "render", "-s", "-qh", "--media_dir", str(renders), str(file), scene],
            cwd=talk.root,
            env=env,
            capture_output=True,
            text=True,
        )
        stills = sorted((renders / "images" / file.stem).glob(f"{scene}*.png"), key=lambda p: p.stat().st_mtime)
        if r.returncode or not stills:
            raise RuntimeError(f"specimen scene {scene} failed:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
        body.append(f"<h2>{page.esc(scene)}</h2><div class='screen'>{page.image(stills[-1])}</div>")
    title = talk.config().get("title") or "Talk"
    return page.write(
        talk.exports() / "specimen.html",
        f"{title}: design specimen",
        "Every token drawn by the engine, then the talk's own specimen scenes.",
        "".join(body),
    )
