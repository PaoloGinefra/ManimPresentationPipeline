"""Charts for results: paired bars, ours on its side of the baseline (the 180-degree rule), an optional floor.

A chart is drawn from numbers, never pasted, so it takes the talk's type and colours; every metric name
carries its direction (higher or lower is better). Bars are returned per group so a beat can build them
group by group.
"""

from types import SimpleNamespace

from manim import DOWN, LEFT, RIGHT, UP, DashedLine, Line, Rectangle, VGroup

from . import tokens as tk

px = tk.px


def arrow(better: str) -> str:
    return "↑" if better == "up" else "↓"


def paired_bars(
    groups,
    ours,
    base,
    floor=None,
    top=100.0,
    box=(300, 300, 1640, 850),
    metric="success (%)",
    better="up",
    fmt="{:.0f}",
    colors=None,
    text_colors=None,
    names=("ours", "baseline"),
    err=None,
    err_note="± 1 s.e. over seeds",
):
    """One group per condition: ours and the baseline, each value above its bar; an optional floor per
    group, dashed across it. `err` is (ours, baseline) lists of half-widths, drawn as error bars and named
    in the title by `err_note`. `box` is (left, top, right, bottom) in 1080p pixels."""
    colors = colors or (tk.OURS, tk.BASELINE)
    text_colors = text_colors or (tk.OURS, tk.COLORS.get("baseline_text", tk.BASELINE))
    sides = (-1, 1) if tk.OURS_SIDE == "left" else (1, -1)
    x0, y0, x1, y1 = box
    base_y = px(0, y1)[1]
    H = px(0, y0)[1] - base_y
    slot = (x1 - x0) / len(groups)
    bw = min(70, slot * 0.28) * tk.PX
    height = lambda v: max(v / top * H, 0.004)
    out = []
    for i, g in enumerate(groups):
        cx = px(x0 + slot * (i + 0.5), 0)[0]
        bars = VGroup()
        for k, (v, col) in enumerate(((ours[i], colors[0]), (base[i], colors[1]))):
            x = cx + sides[k] * 0.5 * (bw * 1.15)
            r = Rectangle(width=bw, height=height(v), fill_color=col, fill_opacity=1, stroke_width=0).move_to(
                [x, base_y, 0], aligned_edge=DOWN
            )
            text = tk.words(fmt.format(v), "note", color=text_colors[k])
            val = VGroup(text)
            e = err[k][i] if err is not None else None
            if e:  # the error bar travels with the value: fading one in fades both
                lo, hi = base_y + height(max(v - e, 0)), base_y + height(v + e)
                cap = bw * 0.3
                val.add(
                    VGroup(
                        Line([x, lo, 0], [x, hi, 0]),
                        Line([x - cap, hi, 0], [x + cap, hi, 0]),
                        Line([x - cap, lo, 0], [x + cap, lo, 0]),
                    ).set_stroke(tk.INK, 2.5)
                )
                text.move_to([x, hi + 0.08 + text.height / 2, 0])
            else:
                text.next_to(r, UP, buff=0.08)
            bars.add(VGroup(r, val))
        fl = VGroup()
        if floor is not None and floor[i] is not None:
            fy = base_y + height(floor[i])
            fl.add(
                DashedLine(
                    [cx - bw * 1.4, fy, 0], [cx + bw * 1.4, fy, 0], color=tk.MUTED, stroke_width=3, dash_length=0.08
                )
            )
        name = tk.words(g, "note").next_to([cx, base_y, 0], DOWN, buff=0.18)
        out.append(
            SimpleNamespace(
                ours=bars[0],
                base=bars[1],
                floor=fl,
                name=name,
                x=cx,
                top=max(bars[0][0].get_top()[1], bars[1][0].get_top()[1]),
            )
        )
    axis = Line(px(x0 - 20, y1), px(x1, y1), color=tk.STRUCTURE, stroke_width=3)
    note = f", {err_note}" if err is not None and err_note else ""
    title = tk.words(f"{metric} {arrow(better)}{note}", "note", color=tk.MUTED).move_to(
        px(x0 - 20, y0 - 30), aligned_edge=LEFT
    )
    entries = [
        VGroup(
            Rectangle(width=0.28, height=0.28, fill_color=c, fill_opacity=1, stroke_width=0), tk.words(n, "note")
        ).arrange(RIGHT, buff=0.12)
        for c, n in zip(colors, names)
    ]
    key = VGroup(*(entries if sides[0] < 0 else entries[::-1]))  # the key reads in the bars' order
    if floor is not None:
        key.add(
            VGroup(
                DashedLine(LEFT * 0.2, RIGHT * 0.2, color=tk.MUTED, stroke_width=3, dash_length=0.08),
                tk.words("floor", "note"),
            ).arrange(RIGHT, buff=0.12)
        )
    key.arrange(RIGHT, buff=0.4).move_to(px(x1, y0 - 75), aligned_edge=RIGHT)
    return SimpleNamespace(groups=out, axis=axis, title=title, key=key, base_y=base_y, H=H, top=top)


def single_bars(groups, values, top, box=(300, 300, 1640, 850), metric="", better="up", fmt="{:+.0f}", color=None):
    """One bar per group: a single quantity, such as a lead."""
    color = color or tk.OURS
    x0, y0, x1, y1 = box
    base_y = px(0, y1)[1]
    H = px(0, y0)[1] - base_y
    slot = (x1 - x0) / len(groups)
    bw = min(90, slot * 0.4) * tk.PX
    out = []
    for i, (g, v) in enumerate(zip(groups, values)):
        cx = px(x0 + slot * (i + 0.5), 0)[0]
        r = Rectangle(
            width=bw, height=max(v / top * H, 0.004), fill_color=color, fill_opacity=1, stroke_width=0
        ).move_to([cx, base_y, 0], aligned_edge=DOWN)
        out.append(
            SimpleNamespace(
                bar=r,
                value=tk.words(fmt.format(v), "label", color=color).next_to(r, UP, buff=0.1),
                name=tk.words(g, "note").next_to([cx, base_y, 0], DOWN, buff=0.18),
                x=cx,
            )
        )
    axis = Line(px(x0 - 20, y1), px(x1, y1), color=tk.STRUCTURE, stroke_width=3)
    title = tk.words(f"{metric} {arrow(better)}", "note", color=tk.MUTED).move_to(
        px(x0 - 20, y0 - 30), aligned_edge=LEFT
    )
    return SimpleNamespace(groups=out, axis=axis, title=title)
