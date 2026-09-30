"""The generic half of the design-system specimen: every token on one still, drawn by the engine.

The talk adds its own half in 5-design/specimen.py (a few real frames, its cast, any comparison of
options). Both are rendered as stills and gathered on one page for the author to approve. manim loads
this file by path, so its imports are absolute.
"""

from manim import DOWN, LEFT, RIGHT, UL, Rectangle, Scene, VGroup

from mpp import charts, chrome
from mpp import tokens as tk

tk.apply_style()


def swatches():
    items = VGroup()
    for role, hexa in tk.COLORS.items():
        chip = Rectangle(
            width=0.55, height=0.55, fill_color=hexa, fill_opacity=1, stroke_color=tk.FAINT, stroke_width=1
        )
        items.add(
            VGroup(
                chip,
                VGroup(tk.words(role, "note"), tk.words(hexa, "note", color=tk.MUTED)).arrange(
                    DOWN, aligned_edge=LEFT, buff=0.06
                ),
            ).arrange(RIGHT, buff=0.15)
        )
    return items.arrange_in_grid(cols=2, buff=(0.5, 0.22), cell_alignment=LEFT)


def type_scale():
    return VGroup(
        *[
            tk.words(f"{role} {size}px", role, weight="SEMIBOLD" if role in ("title", "headline") else "NORMAL")
            for role, size in tk.CAP.items()
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)


class Specimen(Scene):
    def construct(self):
        self.add(
            chrome.headline("The claim of the frame, one sentence at most two lines."),
            chrome.slide_number(7),
            chrome.draft_label("abc1234"),
            chrome.spine(["first question", "second", "third"], done=1, current=1),
        )
        colours = swatches().move_to(tk.px(tk.MARGIN_X, tk.CONTENT_TOP), aligned_edge=UL)
        types = type_scale().move_to(tk.px(700, tk.CONTENT_TOP), aligned_edge=UL)
        c = charts.paired_bars(
            ["A", "B", "C"],
            [72, 55, 41],
            [60, 50, 22],
            err=([3, 4, 5], [4, 3, 4]),
            box=(1250, 330, 1820, 780),
            metric="success (%)",
        )
        self.add(colours, types, c.axis, c.title, c.key, *[m for g in c.groups for m in (g.ours, g.base, g.name)])
