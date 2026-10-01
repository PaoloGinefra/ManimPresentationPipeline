from components.pipeline import px_w, row
from manim import DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, GrowArrow, Line, Rectangle, RoundedRectangle, Transform, VGroup

from mpp import tokens as tk
from mpp.beat import Beat


def doc(title, w, h, color=None, lines=4):
    box = RoundedRectangle(corner_radius=0.06, width=px_w(w), height=px_w(h), stroke_color=color or tk.STRUCTURE,
                           stroke_width=3 if color else 2, fill_color=tk.GROUND, fill_opacity=1)
    name = tk.words(title, "note", color=tk.INK if color else tk.MUTED).next_to(box, DOWN, buff=px_w(16))
    bars = VGroup(*[Rectangle(width=px_w(w * 0.7 - 24 * (i % 2)), height=px_w(10), stroke_width=0,
                              fill_color=tk.FAINT, fill_opacity=1) for i in range(lines)])
    bars.arrange(DOWN, aligned_edge=LEFT, buff=px_w(22)).move_to(box)
    return VGroup(box, bars, name)


class B5(Beat):
    def construct(self):
        stages = self.carried("row")
        source = doc("storyboard.toml", 300, 360, color=tk.OURS, lines=6).move_to(tk.px(960, 520))
        script = doc("script", 220, 280).move_to(tk.px(480, 540))
        deck = doc("deck", 320, 180).move_to(tk.px(1440, 540))
        to_script = Arrow(source[0].get_left(), script[0].get_right(), buff=px_w(24), color=tk.STRUCTURE, stroke_width=3)
        to_deck = Arrow(source[0].get_right(), deck[0].get_left(), buff=px_w(24), color=tk.STRUCTURE, stroke_width=3)
        self.click(*self.wipe(keep=[stages]), FadeIn(source), Transform(stages, row(done=6)))
        self.play(GrowArrow(to_script), FadeIn(script, shift=LEFT * 0.3))
        self.play(GrowArrow(to_deck), FadeIn(deck, shift=RIGHT * 0.3))

        # one frame, one click: the scene must play exactly what the storyboard lists
        frames = VGroup(*[tk.words(f"frame {i}", "note") for i in (1, 2, 3)]).arrange(DOWN, buff=px_w(40))
        clicks = VGroup(*[tk.words(f"click {i}", "note") for i in (1, 2, 3, 4)]).arrange(DOWN, buff=px_w(40))
        frames.move_to(tk.px(700, 420), aligned_edge=UP)
        clicks.next_to(frames, RIGHT, buff=px_w(420)).align_to(frames, UP)
        heads = VGroup(tk.words("storyboard", "note", color=tk.MUTED).next_to(frames, UP, buff=px_w(36)),
                       tk.words("scene", "note", color=tk.MUTED).next_to(clicks, UP, buff=px_w(36)))
        pairs = VGroup(*[Line(f.get_right() + RIGHT * px_w(20), c.get_left() + LEFT * px_w(20), stroke_color=tk.OURS,
                              stroke_width=3) for f, c in zip(frames, clicks)])
        extra = clicks[3].set_color(tk.FAILURE)
        strike = Line(extra.get_left(), extra.get_right(), stroke_color=tk.FAILURE, stroke_width=4)
        stop = tk.words("the build stops", "note", color=tk.FAILURE).next_to(extra, RIGHT, buff=px_w(30))
        self.click(self.crossfade(frames, clicks[:3], heads, keep=[stages]))
        self.play(*[Create(p) for p in pairs])
        self.play(FadeIn(extra), Create(strike), FadeIn(stop))
