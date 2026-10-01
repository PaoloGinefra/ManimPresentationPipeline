from components.pipeline import px_w, row
from manim import DOWN, FadeIn, FadeTransform, Rectangle, Transform, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

CLOSE = ["Build a talk the way you build software:", "in stages, each checked cheaply by its author,", "from one source file."]


class B8(Beat):
    def construct(self):
        stages = self.carried("row")
        sentence = VGroup(*[tk.words(s, "headline", weight="SEMIBOLD" if i == 0 else "NORMAL",
                                     color=tk.INK if i == 0 else tk.OURS) for i, s in enumerate(CLOSE)])
        sentence.arrange(DOWN, buff=px_w(30)).move_to(tk.px(960, 520))
        # the same layout, as the greybox draws it: one grey box per line
        grey = VGroup(*[Rectangle(width=line.width, height=px_w(52), stroke_width=0, fill_color=tk.FAINT,
                                  fill_opacity=1).move_to(line) for line in sentence])
        label = tk.words("the one sentence", "note", color=tk.MUTED).move_to(grey[1])
        self.click(*self.wipe(keep=[stages]), FadeIn(grey), FadeIn(label), Transform(stages, row(done=6)))

        self.click(FadeTransform(VGroup(grey, label), sentence), Transform(stages, row(done=8)), run_time=2)
