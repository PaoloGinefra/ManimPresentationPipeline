from components.pipeline import px_w
from manim import DOWN, RIGHT, FadeIn, Rectangle, RoundedRectangle, SurroundingRectangle, VGroup

from mpp import tokens as tk
from mpp.beat import Beat


def text_bar(w):
    """A line of text as the greybox draws it: the lint itself would flag two real overlapping texts."""
    return Rectangle(width=px_w(w), height=px_w(30), stroke_width=0, fill_color=tk.STRUCTURE, fill_opacity=1)


class S1(Beat):
    def construct(self):
        a, b = text_bar(520), text_bar(420)
        b.move_to(a.get_center() + [px_w(140), -px_w(16), 0])
        flag = SurroundingRectangle(VGroup(a, b), color=tk.FAILURE, buff=px_w(16), stroke_width=3)
        why = tk.words("two labels on top of each other, found before any render", "note", color=tk.MUTED)
        pic = VGroup(a, b, flag)
        pic.move_to(tk.px(960, 500))
        why.next_to(pic, DOWN, buff=px_w(40))
        self.click(*self.wipe(), FadeIn(pic), FadeIn(why))

        def screen(caption, shift):
            box = RoundedRectangle(corner_radius=0.05, width=px_w(560), height=px_w(315), stroke_color=tk.STRUCTURE,
                                   stroke_width=2)
            bar = text_bar(300).move_to(box.get_center() + [shift, 0, 0])
            return VGroup(box, bar, tk.words(caption, "note", color=tk.MUTED).next_to(box, DOWN, buff=px_w(16)))

        end, start = screen("end of slide 7", 0), screen("start of slide 8", px_w(90))
        pair = VGroup(end, start).arrange(RIGHT, buff=px_w(80)).move_to(tk.px(960, 520))
        jump = tk.words("they differ: the audience sees a jump", "note", color=tk.FAILURE).next_to(pair, DOWN, buff=px_w(40))
        self.click(self.crossfade(pair, jump))
