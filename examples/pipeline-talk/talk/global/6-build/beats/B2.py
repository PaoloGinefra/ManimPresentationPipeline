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

        # the notes land on the top rung's line, after its caption
        notes = VGroup(*[note("note", width=130, size="note") for _ in range(3)]).arrange(RIGHT, buff=px_w(16))
        notes.next_to(dear, RIGHT, buff=px_w(40))
        notes.shift(UP * (tk.baseline(dear) - tk.baseline(notes[0][1])))  # on the caption's line
        self.click(LaggedStart(*[FadeIn(n, shift=DOWN * 0.5) for n in notes], lag_ratio=0.35, run_time=1.6))
