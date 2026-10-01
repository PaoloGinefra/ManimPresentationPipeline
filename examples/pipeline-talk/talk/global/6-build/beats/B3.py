from components.pipeline import RUNG_TO_STAGE, above, px_w, row
from manim import UP, FadeIn, FadeOut, LaggedStart, RoundedRectangle, Transform, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

CHECKPOINTS = [(2, "one page"), (3, "read aloud"), (4, "grey boxes")]


class B3(Beat):
    def construct(self):
        lad = self.carried("ladder")
        rungs, cheap, dear = lad
        notes = [m for m in self.inherited if getattr(m, "role", None) == "note"]
        target = row()
        # the ladder turns on its side: each rung is the stage it names
        morph = [Transform(r[0], target[j][0]) for r, j in zip(rungs, RUNG_TO_STAGE)]
        gone = [FadeOut(r[1]) for r in rungs] + [FadeOut(cheap), FadeOut(dear)] + [FadeOut(n) for n in notes]
        self.click(*morph, *gone, run_time=tk.MOVE)
        shown = [target[i] for i in range(len(target)) if i not in RUNG_TO_STAGE]
        shown += [target[j][1] for j in RUNG_TO_STAGE]
        self.play(LaggedStart(*[FadeIn(m) for m in shown], lag_ratio=0.15))
        # the morphed rungs now look exactly like their boxes: swap in the row as one object
        self.remove(lad, *notes, *shown)
        self.add(target)

        cards = VGroup()
        for i, text in CHECKPOINTS:
            box = RoundedRectangle(corner_radius=0.06, width=px_w(200), height=px_w(84), stroke_color=tk.OURS,
                                   stroke_width=2.5, fill_color=tk.OURS, fill_opacity=0.08)
            cards.add(VGroup(box, tk.words(text, "note").move_to(box)).move_to(above(i, 60)))
        self.click(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cards], lag_ratio=0.6, run_time=2.4))
