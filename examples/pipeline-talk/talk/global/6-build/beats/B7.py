from components.pipeline import px_w
from manim import DOWN, LEFT, RIGHT, UL, FadeIn, RoundedRectangle, SurroundingRectangle, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

TREE = ["AGENTS.md", "pipeline/", "engine/", "talk/", "    source/", "    global/", "    variants/", "vendor/"]


class B7(Beat):
    def construct(self):
        stages = self.carried("row")
        lines = VGroup(*[tk.words(s, "label", color=tk.INK if s.strip().startswith("talk") else tk.MUTED) for s in TREE])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=px_w(16)).move_to(tk.px(260, 250), aligned_edge=UL)
        talk = VGroup(*lines[3:7])
        lit = SurroundingRectangle(talk, color=tk.OURS, buff=px_w(14), corner_radius=0.06, stroke_width=3)
        agents = RoundedRectangle(corner_radius=0.06, width=px_w(720), height=px_w(250), stroke_color=tk.STRUCTURE,
                                  stroke_width=2).move_to(tk.px(1260, 380))
        steps = VGroup(tk.words("AGENTS.md", "label", weight="SEMIBOLD"),
                       tk.words("read the principles, run mpp status,", "note"),
                       tk.words("follow the stage it names", "note")).arrange(DOWN, aligned_edge=LEFT, buff=px_w(18))
        steps.move_to(agents)
        self.click(self.crossfade(lines, lit, VGroup(agents, steps), keep=[stages]))

        commands = VGroup(
            VGroup(tk.words("uv run mpp doctor", "label", color=tk.OURS), tk.words("checks the machine", "note", color=tk.MUTED)),
            VGroup(tk.words("uv run mpp build", "label", color=tk.OURS), tk.words("builds the deck, offline", "note", color=tk.MUTED)),
        )
        for c in commands:
            c.arrange(RIGHT, buff=px_w(28))
        commands.arrange(DOWN, aligned_edge=LEFT, buff=px_w(30)).next_to(agents, DOWN, buff=px_w(60)).align_to(agents, LEFT)
        self.click(FadeIn(commands, shift=RIGHT * 0.2))
