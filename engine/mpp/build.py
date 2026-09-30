"""Build a talk, or part of it, in the storyboard's order: check, render what changed, export.

Three passes, so a change costs what it touches:
  1. check: each beat whose inputs changed runs once without animation (manim's last-frame mode), in
     the talk's order. It fails in seconds where a render would fail after minutes, runs the layout
     lint at every click, fills the text cache before any parallel work, and writes the beat's
     handoff, the picture the next beat opens on.
  2. render: the changed beats render in parallel. A beat's inputs are its own code, the shared code
     it uses, the engine, the components, the tokens, its storyboard entry, its first slide number and
     the picture it opens on. A beat whose predecessor now ends differently is changed too; one
     untouched by an edit is not rendered again.
  3. export: one offline HTML file (every video inlined) and a PDF with one page per click.

Drafts render at 720p24 and show the build commit; finals render at 1080p30 without it. The commit is
deliberately not part of a beat's inputs, or every commit would re-render the whole talk. A cached beat
still shows a commit whose storyboard numbers it the same way, because the slide number is an input.
"""

import ast
import hashlib
import json
import os
import pickle
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .project import ENGINE, REPO, Talk

QUALITY = {"draft": ["-qm", "--fps", "24"], "final": ["-qh", "--fps", "30"]}
SCENE_MODULES = ["project", "storyboard", "tokens", "chrome", "camera", "motion", "charts", "lint", "beat"]


class BuildError(RuntimeError):
    pass


def cores() -> int:
    """The cores this process may use: on a cluster node, cpu_count is the whole node."""
    affinity = getattr(os, "sched_getaffinity", None)
    return len(affinity(0)) if affinity else os.cpu_count() or 1


def by_name(folders: list[Path], pattern: str) -> dict[str, Path]:
    """Files under the folders by relative path, the first folder winning: the variant cascade."""
    found = {}
    for folder in reversed(folders):
        for f in sorted(folder.rglob(pattern)):
            found[str(f.relative_to(folder))] = f
    return found


def beat_sources(talk: Talk) -> dict[str, tuple[Path, str, str]]:
    """Beat name -> (file, the class's own source, the file's shared source), read without importing manim."""
    found = {}
    for f in by_name(talk.dirs("6-build/beats"), "*.py").values():
        src = f.read_text()
        tree = ast.parse(src)
        shared = "\n".join(ast.get_source_segment(src, n) or "" for n in tree.body if not isinstance(n, ast.ClassDef))
        for n in tree.body:
            if isinstance(n, ast.ClassDef):
                found[n.name] = (f, ast.get_source_segment(src, n), shared)
    return found


def fingerprint(path: Path) -> str | None:
    """What a handoff looks like, not how pickle happened to lay it out: pickled bytes differ from run to
    run, the picture does not."""
    if not path.exists():
        return None
    import numpy as np

    h = hashlib.sha1()
    data = pickle.loads(path.read_bytes())
    h.update(repr(data.get("head_text")).encode())
    for top in data["content"]:
        for m in top.get_family():
            h.update(type(m).__name__.encode())
            h.update(np.round(np.asarray(m.points, dtype=float), 4).tobytes())
            for attr in ("stroke_color", "fill_color", "stroke_width", "stroke_opacity", "fill_opacity"):
                h.update(repr(getattr(m, attr, None)).encode())
            if hasattr(m, "pixel_array"):
                h.update(hashlib.sha1(np.ascontiguousarray(m.pixel_array)).digest())
    return h.hexdigest()


def commit_label(root: Path) -> str:
    """The short commit, marked when the working tree differs from it."""
    git = lambda *a: subprocess.run(["git", *a], cwd=root, capture_output=True, text=True).stdout.strip()
    sha = git("rev-parse", "--short", "HEAD") or "uncommitted"
    return sha + (" (modified)" if git("status", "--porcelain", "--untracked-files=no") else "")


def environment(talk: Talk, quality: str, lint: bool = False) -> dict:
    layers = [str(d) for d in talk.dirs("6-build")]
    env = {
        **os.environ,
        "MPP_ROOT": str(talk.root),
        "MPP_VARIANT": talk.variant or "",
        "MPP_QUALITY": quality,
        "MPP_DRAFT": commit_label(talk.root) if quality == "draft" else "",
        "PYTHONPATH": os.pathsep.join([*layers, os.environ.get("PYTHONPATH", "")]).rstrip(os.pathsep),
    }
    if lint:
        env["MPP_LINT"] = "1"
    return env


def run(cmd, cwd, env, log=None, ok=lambda code, text: code == 0) -> bool:
    """Run a command; with `log`, its output goes there and only a failure is shown."""
    cmd = list(map(str, cmd))
    if log is None:
        print("$", " ".join(cmd), flush=True)
        return subprocess.run(cmd, cwd=cwd, env=env).returncode == 0
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    text = r.stdout + r.stderr
    log.write_text(text)
    return ok(r.returncode, text)


def build(
    talk: Talk,
    beats: list[str] | None = None,
    act: int | None = None,
    final: bool = False,
    force: bool = False,
    jobs: int | None = None,
    export_only: bool = False,
    export: bool = True,
    name: str | None = None,
) -> list[Path]:
    """Build the selection and return the exported files. Raises BuildError with the log to read.

    Every beat before the selection is checked too (not rendered): a beat opens on its predecessor's
    handoff, and a predecessor outside the selection may have changed since it last wrote one.
    """
    quality = "final" if final else "draft"
    sb = talk.storyboard()
    problems = sb.problems()
    if problems:
        raise BuildError("the storyboard has problems:\n  " + "\n  ".join(problems))
    order = sb.sequence()
    selected = beats or [b for b in order if act is None or sb.beat(b)["act"] == act]
    sources = beat_sources(talk)
    missing = [b for b in selected if b not in sources]
    if missing and beats:
        raise BuildError(f"no scene for {missing} in 6-build/beats/")
    if missing:  # a whole act or talk: build what exists, say what does not
        print("not built yet:", ", ".join(missing), flush=True)
    selected = sorted([b for b in selected if b in sources], key=order.index)
    if not selected:
        raise BuildError("nothing to build: no beat in the selection has a scene")

    renders, exports = talk.renders(quality), talk.exports()
    logs, handoff, stamps_file = renders / "logs", renders / "handoff", renders / "stamps.json"
    for d in (renders, logs, exports):
        d.mkdir(parents=True, exist_ok=True)
    stamps = json.loads(stamps_file.read_text()) if stamps_file.exists() else {}
    shared = "".join((ENGINE / f"{m}.py").read_text() for m in SCENE_MODULES)
    components = "".join(
        f"{k}\0{p.read_text()}" for k, p in sorted(by_name(talk.dirs("6-build/components"), "*.py").items())
    )
    tokens = json.dumps(talk.tokens(), sort_keys=True)

    def key(b):
        own, common = sources[b][1], sources[b][2]
        prev = sb.previous(b)
        parts = [
            own,
            common,
            shared,
            components,
            tokens,
            json.dumps(sb.beat(b), sort_keys=True),
            str(sb.first_number(b)),
            repr(QUALITY[quality]),
            fingerprint(handoff / f"{prev}.pkl") if prev else "",
        ]
        return hashlib.sha1("\x00".join(map(str, parts)).encode()).hexdigest()

    if not export_only:
        # 1. check, in order: a beat's key depends on the handoff its predecessor's check just wrote
        check_env = environment(talk, quality, lint=True)
        upto = [b for b in order[: order.index(selected[-1]) + 1] if b in sources]
        dirty = {}
        for b in upto:
            k = key(b)
            if force or stamps.get(b) != k:
                print(f"check  {b}", flush=True)
                (renders / "lint" / f"{b}.txt").unlink(missing_ok=True)
                passed = run(
                    ["manim", "render", "-s", "--media_dir", renders / "checkmedia", "-ql", sources[b][0], b],
                    renders,
                    check_env,
                    logs / f"{b}.check.log",
                    ok=lambda code, text: code == 0 or "Failed to merge basenames" in text,
                )  # -s cannot save slides
                if not passed:
                    raise BuildError(f"{b} fails before rendering; see {logs / (b + '.check.log')}")
                dirty[b] = k
        dirty = {b: k for b, k in dirty.items() if b in selected}
        # 2. render the changed beats, in parallel: every handoff they open on is already final
        print(f"render {', '.join(dirty) or 'nothing (all up to date)'}", flush=True)
        render_env = environment(talk, quality)

        def render(b):
            # its own media folder: manim's text and TeX caches rewrite and delete shared files in place, so
            # two processes on one cache corrupt each other's texts
            return b, run(
                ["manim", "render", "--media_dir", renders / "media" / b, *QUALITY[quality], sources[b][0], b],
                renders,
                render_env,
                logs / f"{b}.render.log",
            )

        with ThreadPoolExecutor(max_workers=jobs or cores()) as pool:
            for b, ok in pool.map(render, dirty):
                if not ok:
                    raise BuildError(f"{b} failed to render; see {logs / (b + '.render.log')}")
                stamps[b] = dirty[b]
                stamps_file.write_text(json.dumps(stamps, indent=1))
                print(f"  done {b}", flush=True)

    if not export:
        return []
    # 3. export; manim-slides looks for reveal.js in its cache, so point the cache at the vendored copy
    if name is None:
        name = f"{quality}-{'-'.join(selected)}" if beats else f"{quality}-act{act}" if act is not None else quality
    export_env = {**os.environ, "XDG_CACHE_HOME": str(REPO / "vendor" / "cache")}
    folder = ["--folder", renders / "slides"]
    out = [exports / f"{name}.html", exports / f"{name}.pdf"]
    if not (
        run(
            [
                "manim-slides",
                "convert",
                *folder,
                *selected,
                out[0],
                "--to",
                "html",
                "--one-file",
                "--offline",
                "-cprogress=true",
                "-chash=true",
            ],
            renders,
            export_env,
        )
        and run(["manim-slides", "convert", *folder, *selected, out[1], "--to", "pdf"], renders, export_env)
    ):
        raise BuildError("export failed")
    return out
