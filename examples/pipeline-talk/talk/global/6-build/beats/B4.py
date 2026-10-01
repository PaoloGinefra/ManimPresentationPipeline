from components.pipeline import card_at, row
from manim import FadeIn, FadeTransform, Transform

from mpp import tokens as tk
from mpp.beat import Beat

# (form, stage it belongs to); the sentence starts in the source, before the first stage
STEPS = [("source", 0), ("digest", 1), ("outline", 2), ("script", 3), ("storyboard", 4), ("greybox", 4), ("render", 6)]


class B4(Beat):
    def construct(self):
        stages = self.carried("row")
        card = card_at("source", 0)
        self.click(*self.wipe(keep=[stages]), FadeIn(card))
        for form, stage in STEPS[1:]:
            new = card_at(form, stage)
            self.click(FadeTransform(card, new), Transform(stages, row(done=stage, lit=stage)), run_time=tk.MOVE)
            card = new

