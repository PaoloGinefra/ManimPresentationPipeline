from components.pipeline import ladder, note, px_w
from manim import DOWN, RIGHT, UP, FadeIn, LaggedStart, VGroup

from mpp import tokens as tk
from mpp.beat import Beat


class B2(Beat):
    def construct(self):
        lad = ladder()
        rungs, cheap, dear = lad
        self.click(*self.wipe())
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rungs], FadeIn(cheap), FadeIn(dear),
                              lag_ratio=0.5, run_time=3))
        self.remove(*rungs, cheap, dear)  # faded in part by part: hand over the ladder as one object
        self.add(lad)

        top = rungs[-1][0]
        notes = VGroup(*[note("note", width=130) for _ in range(3)]).arrange(RIGHT, buff=px_w(16))
        notes.next_to(top, UP, buff=px_w(70))
        self.click(LaggedStart(*[FadeIn(n, shift=DOWN * 0.5) for n in notes], lag_ratio=0.35, run_time=1.6))
