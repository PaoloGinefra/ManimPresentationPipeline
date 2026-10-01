"""The stage beat: every beat of act 2 makes the same two moves, so they share one scene.

First, what the stage is: the cache talk's checkpoint at that stage, on the card, centred; a frame may
show several forms in turn. Then what the author checks: the card steps aside, the check list
appears, its boxes tick, and the stage ticks on the row.
"""

from components.pipeline import aside, card_centre, checks, row
from manim import FadeIn, FadeTransform, LaggedStart, Transform

from mpp import tokens as tk
from mpp.beat import Beat


class StageBeat(Beat):
    stage: int = 0  # its index in the row
    forms: list[list[str]] = []  # per explaining click, the card's forms in turn
    items: list[str] = []  # what the author checks
    done_after: int | None = None  # stages ticked at the end; default: this one and those before

    def construct(self):
        stages = self.carried("row")
        card = self.carried("card")
        for k, forms in enumerate(self.forms):
            first = card_centre(forms[0])
            if k == 0:
                opening = [FadeIn(first)] if card is None else [FadeTransform(card, first)]
                keep = [stages] if card is None else [stages, card]
                self.click(*self.wipe(keep=keep), *opening, Transform(stages, row(done=self.stage, lit=self.stage)),
                           run_time=tk.MOVE)
            else:
                self.click(FadeTransform(card, first), run_time=tk.MOVE)
            card = first
            for form in forms[1:]:
                nxt = card_centre(form)
                self.play(FadeTransform(card, nxt), run_time=tk.MOVE)
                card = nxt

        title, lines = checks(self.items)
        self.click(Transform(card, aside(card)), FadeIn(title), run_time=tk.MOVE)
        self.play(LaggedStart(*[FadeIn(line[0], line[1]) for line in lines], lag_ratio=0.5, run_time=1.2 * len(lines)))
        self.play(LaggedStart(*[line[2].animate.set_stroke(opacity=1) for line in lines], lag_ratio=0.4),
                  Transform(stages, row(done=self.done_after or self.stage + 1)), run_time=1.4)
