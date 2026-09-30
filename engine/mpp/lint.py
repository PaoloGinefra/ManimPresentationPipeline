"""Layout lint: what a person would catch by looking at a frame, checked from geometry instead.

With MPP_LINT set (the build's check pass sets it), every beat checks the picture it holds at each click for
text that overlaps other text, and for text lying outside the frame, and appends what it finds to
<renders>/lint/<beat>.txt. It reads bounding boxes, so it cannot see colour or taste; it catches the
collisions that a contact sheet shows.
"""

import os

from manim import ImageMobject, MarkupText, MathTex, SingleStringMathTex, Tex, Text, VMobject, config

from .project import Talk

TEXTS = (Text, MarkupText, MathTex, Tex, SingleStringMathTex)
MARGIN = 0.05  # scene units a mobject may poke past the frame before it counts


def visible(m):
    if isinstance(m, ImageMobject):
        return getattr(m, "stroke_opacity", 1) > 0.05
    op = max(m.get_fill_opacity(), m.get_stroke_opacity()) if isinstance(m, VMobject) and m.has_points() else 0
    return op > 0.05 or any(visible(s) for s in m.submobjects)  # a ValueTracker and the like: no points, never seen


def texts(mobjects):
    """The outermost text mobjects on screen: a MathTex counts once, not once per glyph."""
    out = []

    def walk(m):
        if isinstance(m, TEXTS):
            if visible(m) and m.width > 1e-3:
                out.append(m)
            return
        for s in m.submobjects:
            walk(s)

    for m in mobjects:
        walk(m)
    return out


def box(m):
    lo, hi = m.get_corner([-1, -1, 0]), m.get_corner([1, 1, 0])
    return lo[0], lo[1], hi[0], hi[1]


def overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return w * h / small if small > 0 else 0.0


def name(m):
    t = getattr(m, "text", None) or getattr(m, "tex_string", None) or type(m).__name__
    return " ".join(str(t).split())[:40]


def check(scene, label):
    if not os.environ.get("MPP_LINT"):
        return
    try:
        _check(scene, label)
    except Exception as e:  # a lint must never break a render
        _write(scene, [f"lint failed: {type(e).__name__}: {e}"], label)


def _write(scene, found, label):
    d = Talk.current().renders() / "lint"
    d.mkdir(parents=True, exist_ok=True)
    with open(d / f"{scene.id}.txt", "a") as f:
        for line in dict.fromkeys(found):
            f.write(f"{label}: {line}\n")


def _check(scene, label):
    ms = [m for m in scene.mobjects if visible(m)]
    found = []
    ts = texts(ms)
    for i, a in enumerate(ts):
        for b in ts[i + 1 :]:
            if a in b.get_family() or b in a.get_family():
                continue
            o = overlap(box(a), box(b))
            if o > 0.15:
                found.append(f"overlap {o:.0%}: '{name(a)}' / '{name(b)}'")
    W, H = config.frame_width / 2 + MARGIN, config.frame_height / 2 + MARGIN
    for t in ts:  # only text: a picture past the edge is usually a zoom, cropped on purpose
        x0, y0, x1, y1 = box(t)
        if x0 < -W or x1 > W or y0 < -H or y1 > H:
            found.append(f"outside the frame: '{name(t)}'")
    if found:
        _write(scene, found, label)
