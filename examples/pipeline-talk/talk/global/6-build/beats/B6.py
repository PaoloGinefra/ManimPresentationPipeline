from components.pipeline import above, card, note, px_w, row
from manim import DOWN, UP, FadeIn, Succession, Transform, VGroup

from mpp import tokens as tk
from mpp.beat import Beat


class B6(Beat):
    def construct(self):
        stages = self.carried("row")
        msg = note().move_to(above(6, 120))
        self.click(*self.wipe(keep=[stages]), FadeIn(msg, shift=DOWN * 0.4))

        where = tk.words("slide 7 = B3.2, in that draft", "note", color=tk.MUTED).next_to(msg, DOWN, buff=px_w(16))
        self.click(FadeIn(where))

        stage = tk.words("stage: script", "note", color=tk.HIGHLIGHT, weight="SEMIBOLD").next_to(msg, UP, buff=px_w(16))
        self.click(FadeIn(stage))
        travelling = VGroup(msg, where, stage)
        # the note really goes back: along the row, to the stage it belongs to
        self.play(travelling.animate.move_to(above(3, 150)),
                  Transform(stages, row(done=6, lit=3, lit_color=tk.HIGHLIGHT)), run_time=2)

        states = [row(done=6, lit=i) for i in range(4, 7)] + [row(done=6)]
        still = card("render").scale(0.3).move_to(above(6, 150))
        self.click(Succession(*[Transform(stages, s, run_time=0.45) for s in states]))
        self.play(FadeIn(still, shift=UP * 0.3))
