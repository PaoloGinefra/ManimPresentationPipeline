"""Motion shared by every scene: an object travelling a path, drawing a line, and the zoom."""

import numpy as np
from manim import ORIGIN, Create, ImageMobject, UpdateFromAlphaFunc, VMobject, config, rate_functions

from . import tokens as tk

SPEED = 5.0  # scene units per second for walk_along: a route takes a beat, not a wait


def face(mob, angle):
    """Turn an object (drawn facing +x) to face `angle`, whatever way it faced before."""
    mob.rotate(angle - getattr(mob, "heading", 0.0))
    mob.heading = angle
    return mob


def path_length(path):
    pts = np.array([path.point_from_proportion(a) for a in np.linspace(0, 1, 200)])
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


def walk_along(mob, path, run_time=None, rate_func=rate_functions.smooth, speed=SPEED):
    """Move an object along `path`, turned to face its direction of travel.

    `mob` is re-placed from an upright copy each frame, so rotations never accumulate; its heading
    is kept on the mobject, so the next walk starts from where this one left it.
    """
    base = mob.copy().rotate(-getattr(mob, "heading", 0.0)).move_to(ORIGIN)
    run_time = run_time or max(0.6, path_length(path) / speed)

    def update(m, a):
        p = path.point_from_proportion(min(a, 0.999))
        q = path.point_from_proportion(min(a + 0.002, 1.0))
        m.heading = np.arctan2(q[1] - p[1], q[0] - p[0])
        m.become(base.copy().rotate(m.heading).move_to(p))

    return UpdateFromAlphaFunc(mob, update, run_time=run_time, rate_func=rate_func)


def draw(mob, **kw):
    """Draw a line, or a cased line, in one stroke: casing and line together, never one after the other
    (Create's default on a group draws its parts in turn, so the coloured line would start halfway)."""
    return Create(mob, lag_ratio=0, **kw)


def scale_world(mob, s, about=ORIGIN):
    """Scale everything, line widths included: a miniature is the full picture, only smaller."""
    mob.scale(s, about_point=np.asarray(about, dtype=float))
    for m in mob.get_family():
        if isinstance(m, VMobject):
            m.set_stroke(width=m.get_stroke_width() * s, background=False, family=False)
    return mob


def opacities(m):
    """What a fade scales from: (stroke, fill) for a shape, the alpha for an image, nothing for a bare group."""
    if isinstance(m, VMobject):
        return (m.get_stroke_opacity(), m.get_fill_opacity())
    if isinstance(m, ImageMobject):
        return getattr(m, "stroke_opacity", 1.0)  # manim keeps an image's opacity here, not in fill_opacity
    return None


def zoom(world, point, factor, to=ORIGIN, run_time=None, rate_func=rate_functions.smooth, fades=()):
    """The camera move: `point` of `world` travels to `to` while everything grows `factor` times.

    The scale is geometric in time (factor**alpha), so the zoom neither speeds up nor slows down, the
    Powers-of-Ten feel; a factor below one zooms out. Line widths scale with it, so zooming into a
    window lands exactly on the full-size picture the window held. `fades` takes (mobject, start, end):
    that mobject fades out over that part of the move, as fractions of it (a frame that becomes the
    screen's edge, say, over (.6, 1)).
    """
    c, d = np.asarray(point, dtype=float), np.asarray(to, dtype=float)
    fixed = (d - factor * c) / (1.0 - factor)
    state = {"s": 1.0}
    fades = [(m, [opacities(sm) for sm in m.get_family()], (a0, a1)) for m, a0, a1 in fades]

    def update(m, a):
        s = factor**a
        scale_world(m, s / state["s"], fixed)
        state["s"] = s
        for mob, start, (a0, a1) in fades:
            k = 1 - rate_functions.smooth(min(1, max(0, (a - a0) / (a1 - a0))))
            for sm, o in zip(mob.get_family(), start):
                if isinstance(sm, VMobject):
                    sm.set_stroke(opacity=o[0] * k, family=False)
                    sm.set_fill(opacity=o[1] * k, family=False)
                elif isinstance(sm, ImageMobject):
                    sm.set_opacity(o * k)

    return UpdateFromAlphaFunc(world, update, run_time=run_time or tk.ZOOM, rate_func=rate_func)


def zoom_into(world, target, **kw):
    """Zoom until `target` (any mobject inside `world`) fills the screen's width."""
    return zoom(world, target.get_center(), config.frame_width / target.width, **kw)


def zoom_out_from(world, target, **kw):
    """The reverse of zoom_into: `world` is drawn at home; it is first blown up so that `target` fills the
    screen, and the returned animation shrinks it back home. The screen starts exactly as the target's
    content at full size, so a zoom-out can pick up from a beat that ended inside it."""
    c = np.asarray(target.get_center(), dtype=float)
    f = config.frame_width / target.width
    scale_world(world, f, about=c)
    world.shift(-c)
    return zoom(world, ORIGIN, 1 / f, to=c, **kw)
