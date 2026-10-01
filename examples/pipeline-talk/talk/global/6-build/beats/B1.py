from components.pipeline import line_y, px_w
from manim import LEFT, RIGHT, FadeIn, LaggedStart, RoundedRectangle, Square, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

CODE = [
    "class B1(Beat):",
    "    def construct(self):",
    "        queue = requests(6)",
    "        self.click(fill(queue))",
    "        self.play(warm(cache))",
]
MID = 520  # the picture's centre line, in pixels


class B1(Beat):
    def construct(self):
        queue = VGroup(*[Square(px_w(70), stroke_color=tk.STRUCTURE, stroke_width=2.5) for _ in range(6)])
        queue.arrange(RIGHT, buff=px_w(14))
        cache = RoundedRectangle(corner_radius=0.08, width=px_w(260), height=px_w(180), stroke_color=tk.STRUCTURE,
                                 stroke_width=2.5, fill_color=tk.OURS, fill_opacity=0)
        VGroup(queue, cache).arrange(RIGHT, buff=px_w(200)).move_to(tk.px(960, MID))
        captions = VGroup()
        for thing, word in ((queue, "requests"), (cache, "cache")):
            c = tk.words(word, "note", color=tk.MUTED)
            c.set_x(thing.get_x())
            tk.set_baseline(c, line_y(MID + 90 + 50))  # one line under both, whatever their heights
            captions.add(c)

        # a queue fills, a cache warms: the motion is the content
        self.click(self.crossfade(captions, cache))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.4) for s in queue], lag_ratio=0.3, run_time=2.4))
        self.play(cache.animate.set_fill(opacity=0.35).set_stroke(tk.OURS, width=4), run_time=2)

        panel = RoundedRectangle(corner_radius=0.08, width=px_w(1180), height=px_w(400), stroke_color=tk.STRUCTURE,
                                 stroke_width=2, fill_color=tk.GROUND, fill_opacity=1).move_to(tk.px(960, MID))
        lines = VGroup()
        for k, s in enumerate(CODE):
            line = tk.words(s.strip(), "label")
            indent = len(s) - len(s.lstrip())  # Text drops leading spaces: indent by hand
            line.move_to(panel.get_left() + RIGHT * px_w(64 + 16 * indent), aligned_edge=LEFT)
            tk.set_baseline(line, line_y(MID - 120 + 60 * k, "label"))
            lines.add(line)
        self.click(self.crossfade(VGroup(panel, lines)))
