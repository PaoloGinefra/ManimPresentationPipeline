from components.pipeline import RUNG_TO_STAGE, card_centre, row
from manim import FadeIn, FadeOut, LaggedStart, Transform

from mpp import tokens as tk
from mpp.beat import Beat


class B3(Beat):
    def construct(self):
        lad = self.carried("ladder")
        rungs, cheap, dear = lad
        notes = [m for m in self.inherited if getattr(m, "role", None) == "note"]
        target = row()
        # the ladder turns on its side: each rung is the stage it names
        morph = [Transform(r[0], target[j][1]) for r, j in zip(rungs, RUNG_TO_STAGE)]
        gone = [FadeOut(r[1]) for r in rungs] + [FadeOut(cheap), FadeOut(dear)] + [FadeOut(n) for n in notes]
        self.click(*morph, *gone, run_time=tk.MOVE)
        shown = [target[i] for i in range(len(target)) if i not in RUNG_TO_STAGE]
        shown += [target[j][2] for j in RUNG_TO_STAGE]
        self.play(LaggedStart(*[FadeIn(m) for m in shown], lag_ratio=0.12))
        # the morphed rungs now look exactly like their outlines: swap in the row as one object
        self.remove(lad, *notes, *shown)
        self.add(target)

        self.click(FadeIn(card_centre("title")))
