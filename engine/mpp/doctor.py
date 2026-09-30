"""`mpp doctor`: is this machine ready to build a talk? Each check says what it found or how to fix it.

The last check renders one still of the specimen, which exercises the whole chain (cairo, pango, the
fonts, the tokens, manim) the way a build does. LaTeX is only needed for mathematics on slides, so
its absence is reported but does not fail the doctor.
"""

import importlib.metadata as md
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .project import ENGINE, REPO, Talk

MAC = sys.platform == "darwin"
FIX = {
    "native": "run scripts/setup.sh (it installs cairo and pango, or explains how)",
    "latex": (
        "install BasicTeX (brew install --cask basictex), then: sudo tlmgr install standalone preview "
        "dvisvgm cm-super babel-english"
        if MAC
        else "install TeX Live: sudo apt install texlive-latex-extra texlive-fonts-recommended dvisvgm cm-super, "
        "or without root the user installer from tug.org/texlive into ~/texlive, then put its bin/ on PATH"
    ),
}


def check_python():
    ok = sys.version_info[:2] == (3, 12)
    return ok, f"Python {platform.python_version()}", "uv sync installs 3.12 (see .python-version)"


def check_packages():
    try:
        import cairo
        import manimpango

        found = f"cairo {cairo.cairo_version_string()}, pango {manimpango.pango_version()}"
    except ImportError as e:
        return False, f"cannot import {e.name}", FIX["native"]
    versions = ", ".join(f"{p} {md.version(p)}" for p in ("manim", "manim-slides", "screenplain"))
    return True, f"{found}; {versions}", ""


def check_fonts():
    import manimpango

    files = sorted((REPO / "vendor" / "fonts").glob("*.[ot]tf"))
    for f in files:
        manimpango.register_font(str(f))
    face = Talk.current().tokens()["type"]["face"]
    ok = face in manimpango.list_fonts()
    return (
        ok,
        f"{len(files)} vendored font files; face '{face}' {'registered' if ok else 'not found'}",
        ("put the face's .otf or .ttf files in vendor/fonts/ or talk/global/5-design/fonts/"),
    )


def check_revealjs():
    from manim_slides.convert import RevealJS

    version = RevealJS.model_fields["reveal_version"].default
    ok = (REPO / "vendor" / f"revealjs{version}" / "reveal.js").exists()
    return (
        ok,
        f"manim-slides wants reveal.js {version}; vendored: {'yes' if ok else 'no'}",
        (f"download reveal.js {version}'s dist files into vendor/revealjs{version}/"),
    )


def check_git():
    ok = shutil.which("git") is not None
    return ok, "git on PATH" if ok else "no git", "install git: stages are approved with git tags"


def check_latex():
    missing = [t for t in ("latex", "dvisvgm") if shutil.which(t) is None]
    if missing:
        return None, f"not on PATH: {', '.join(missing)} (needed only for mathematics)", FIX["latex"]
    code = (
        "from manim import config; from mpp import tokens as tk; "
        f"config.media_dir = {tempfile.mkdtemp()!r}; tk.math(r'\\int_0^1 x^2\\,\\mathrm{{d}}x = \\tfrac{{1}}{{3}}')"
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=Talk.current().root)
    tail = (r.stderr.strip().splitlines() or ["?"])[-1]
    return (
        (r.returncode == 0),
        "latex and dvisvgm compile a formula" if not r.returncode else f"a formula fails: {tail}",
        (FIX["latex"]),
    )


def check_render():
    talk = Talk.current()
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(
            ["manim", "render", "-s", "-ql", "--media_dir", tmp, str(ENGINE / "specimen.py"), "Specimen"],
            capture_output=True,
            text=True,
            cwd=talk.root,
        )
        ok = r.returncode == 0 and any(Path(tmp).rglob("Specimen*.png"))
    tail = (r.stderr.strip().splitlines() or r.stdout.strip().splitlines() or ["?"])[-1]
    return ok, "rendered a still of the specimen" if ok else f"render failed: {tail}", FIX["native"]


CHECKS = [
    ("python", check_python, True),
    ("packages", check_packages, True),
    ("fonts", check_fonts, True),
    ("reveal.js", check_revealjs, True),
    ("git", check_git, True),
    ("latex", check_latex, False),
    ("render", check_render, True),
]


def run() -> bool:
    healthy = True
    for name, fn, required in CHECKS:
        try:
            ok, found, fix = fn()
        except Exception as e:  # a check must report, never crash the doctor
            ok, found, fix = False, f"{type(e).__name__}: {e}", FIX["native"]
        mark = "ok  " if ok else "FAIL" if required else "warn"
        print(f"{mark}  {name:<10} {found}")
        if not ok and fix:
            print(f"{'':16}fix: {fix}")
        healthy &= bool(ok) or not required
        if name == "packages" and not ok:
            print(f"{'':16}(the remaining checks need these packages)")
            return False
    return healthy
