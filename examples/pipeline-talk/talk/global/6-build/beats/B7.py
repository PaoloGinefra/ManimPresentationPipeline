from components.pipeline import CHECKS_X, CHECKS_TOP, line_y, px_w
from manim import LEFT, RIGHT, UL, FadeIn, RoundedRectangle, SurroundingRectangle, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

TREE = ["AGENTS.md", "pipeline/", "engine/", "talk/", "    source/", "    global/", "    variants/", "vendor/"]
PITCH = 52


class B7(Beat):
    def construct(self):
        stages = self.carried("row")
        lines = VGroup()
        for k, s in enumerate(TREE):
            indent = len(s) - len(s.lstrip())
            line = tk.words(s.strip(), "label", color=tk.INK if 3 <= k <= 6 else tk.MUTED)
            line.move_to(tk.px(tk.MARGIN_X + 16 * indent, 0), aligned_edge=LEFT)  # on the headline's margin
            tk.set_baseline(line, line_y(CHECKS_TOP + PITCH * k, "label"))
            lines.add(line)
        lit = SurroundingRectangle(VGroup(*lines[3:7]), color=tk.OURS, buff=px_w(14), corner_radius=0.06,
                                   stroke_width=3)
        title = tk.words("AGENTS.md", "label", weight="SEMIBOLD")
        steps = [tk.words("read the principles, run mpp status,", "label"), tk.words("follow the stage it names", "label")]
        for k, t in enumerate([title, *steps]):
            t.move_to(tk.px(CHECKS_X + 40, 0), aligned_edge=LEFT)
            tk.set_baseline(t, line_y(CHECKS_TOP + PITCH * k, "label"))
        card = RoundedRectangle(corner_radius=0.06, width=px_w(840), height=px_w(PITCH * 3 + 50),
                                stroke_color=tk.STRUCTURE, stroke_width=2)
        card.move_to(tk.px(CHECKS_X, CHECKS_TOP - 40), aligned_edge=UL)
        agents = VGroup(card, title, *steps)
        self.click(self.crossfade(lines, lit, agents, keep=[stages]))

        commands = VGroup()
        for k, (cmd, what) in enumerate((("uv run mpp doctor", "checks the machine"),
                                         ("uv run mpp build", "builds the deck, offline"))):
            y = line_y(CHECKS_TOP + PITCH * 3 + 90 + 64 * k, "label")
            c = tk.words(cmd, "label", color=tk.OURS).move_to(tk.px(CHECKS_X + 40, 0), aligned_edge=LEFT)
            w = tk.words(what, "label", color=tk.MUTED).move_to(tk.px(CHECKS_X + 400, 0), aligned_edge=LEFT)
            for t in (c, w):
                tk.set_baseline(t, y)
            commands.add(VGroup(c, w))
        self.click(FadeIn(commands, shift=RIGHT * 0.2))
