from manim import RIGHT, RoundedRectangle, VGroup

from mpp import tokens as tk
from mpp.beat import Beat


class B1(Beat):
    def construct(self):
        box = RoundedRectangle(corner_radius=0.2, width=4, height=2.4, color=tk.OURS)
        idea = VGroup(box, tk.words("one idea", "label").move_to(box))
        idea.role = "idea"  # a later beat could pick it up with self.carried("idea")
        self.click(self.crossfade(idea))
        self.click(idea.animate.shift(RIGHT * 3))
