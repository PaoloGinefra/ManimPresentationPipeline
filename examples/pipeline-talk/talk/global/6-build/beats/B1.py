from components.pipeline import px_w
from manim import DOWN, LEFT, RIGHT, FadeIn, LaggedStart, RoundedRectangle, Square, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

CODE = [
    "class B1(Beat):",
    "    def construct(self):",
    "        queue = requests(6)",
    "        self.click(fill(queue))",
    "        self.play(warm(cache))",
]


class B1(Beat):
    def construct(self):
        queue = VGroup(*[Square(px_w(70), stroke_color=tk.STRUCTURE, stroke_width=2.5) for _ in range(6)])
        queue.arrange(RIGHT, buff=px_w(14)).move_to(tk.px(700, 560))
        caption_q = tk.words("requests", "note", color=tk.MUTED).next_to(queue, DOWN, buff=px_w(24))
        cache = RoundedRectangle(corner_radius=0.08, width=px_w(260), height=px_w(180), stroke_color=tk.STRUCTURE,
                                 stroke_width=2.5, fill_color=tk.OURS, fill_opacity=0).move_to(tk.px(1330, 560))
        caption_c = tk.words("cache", "note", color=tk.MUTED).next_to(cache, DOWN, buff=px_w(24))

        # a queue fills, a cache warms: the motion is the content
        self.click(self.crossfade(caption_q, cache, caption_c))
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.4) for s in queue], lag_ratio=0.3, run_time=2.4))
        self.play(cache.animate.set_fill(opacity=0.35).set_stroke(tk.OURS, width=4), run_time=2)

        panel = RoundedRectangle(corner_radius=0.08, width=px_w(760), height=px_w(330), stroke_color=tk.STRUCTURE,
                                 stroke_width=2, fill_color=tk.GROUND, fill_opacity=1)
        lines = VGroup(*[tk.words(s, "note", color=tk.INK) for s in CODE]).arrange(DOWN, aligned_edge=LEFT, buff=px_w(18))
        code = VGroup(panel, lines.move_to(panel)).move_to(tk.px(1080, 600))
        self.click(*self.dim(), FadeIn(code, shift=LEFT * 0.6))
