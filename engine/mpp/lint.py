"""Layout lint: what a person would catch by looking at a frame, checked from geometry instead.

With MPP_LINT set (the build's check pass sets it), every beat checks the picture it holds at each
click for text that overlaps other text, text lying outside the frame, and texts that almost align
and do not, and appends what it finds to <renders>/lint/<beat>.txt. It reads geometry, so it cannot
see colour or taste; it catches the collisions and near-misses that a contact sheet shows.
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


NEAR = (1, 10)  # pixels at 1080p: closer than this is meant to align, further is a clear offset


def near_misses(ts):
    """Texts that almost align and do not: baselines on one row, or left edges in one column, a few
    pixels apart. Almost-aligned reads as a mistake; align exactly or offset clearly."""
    from . import tokens as tk

    lo, hi = NEAR[0] * tk.PX, NEAR[1] * tk.PX
    lines = [t for t in ts if isinstance(t, Text) and "\n" not in t.original_text]
    base = {id(t): tk.baseline(t) for t in lines}
    found = []
    for i, a in enumerate(lines):
        for b in lines[i + 1 :]:
            (ax0, ay0, _, ay1), (bx0, by0, _, by1) = box(a), box(b)
            same_row = min(ay1, by1) > max(ay0, by0)
            d = abs(base[id(a)] - base[id(b)])
            if same_row and lo < d < hi:
                found.append(f"baselines {d / tk.PX:.0f} px apart: '{name(a)}' / '{name(b)}'")
            near_column = min(abs(ay0 - by1), abs(by0 - ay1)) < 250 * tk.PX and not same_row
            d = abs(ax0 - bx0)
            if near_column and lo < d < hi:
                found.append(f"left edges {d / tk.PX:.0f} px apart: '{name(a)}' / '{name(b)}'")
    return found


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
    found += near_misses(ts)
    W, H = config.frame_width / 2 + MARGIN, config.frame_height / 2 + MARGIN
    for t in ts:  # only text: a picture past the edge is usually a zoom, cropped on purpose
        x0, y0, x1, y1 = box(t)
        if x0 < -W or x1 > W or y0 < -H or y1 > H:
            found.append(f"outside the frame: '{name(t)}'")
    if found:
        _write(scene, found, label)
