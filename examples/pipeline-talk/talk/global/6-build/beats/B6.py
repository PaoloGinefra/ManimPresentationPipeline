from components.pipeline import STAGES, above, card, note, px_w, row, stage_x
from manim import DOWN, UP, FadeIn, Succession, Transform, VGroup

from mpp import tokens as tk
from mpp.beat import Beat

REHEARSAL, SCRIPT = STAGES.index("rehearsal"), STAGES.index("script")


def over(i: int, height: float, width: float):
    """Above stage i, kept inside the margins for something `width` pixels wide."""
    x = min(max(stage_x(i), tk.MARGIN_X + width / 2), 1920 - tk.MARGIN_X - width / 2)
    return tk.px(x, 0)[0], above(i, height)[1]


class B6(Beat):
    def construct(self):
        stages = self.carried("row")
        msg = note()
        x, y = over(REHEARSAL, 330, msg.width / tk.PX)
        msg.move_to([x, y, 0])
        self.click(*self.wipe(keep=[stages]), FadeIn(msg, shift=DOWN * 0.4),
                   Transform(stages, row(done=7, lit=REHEARSAL)), run_time=tk.MOVE)

        where = tk.words("slide 7 = B3.2, in that draft", "label", color=tk.MUTED)
        where.set_x(msg.get_x())
        tk.set_baseline(where, msg.get_bottom()[1] - px_w(56))
        self.click(FadeIn(where))

        stage = tk.words("stage: script", "label", color=tk.HIGHLIGHT, weight="SEMIBOLD")
        stage.set_x(msg.get_x())
        tk.set_baseline(stage, msg.get_top()[1] + px_w(24))
        self.click(FadeIn(stage))
        travelling = VGroup(msg, where, stage)
        x, _ = over(SCRIPT, 330, msg.width / tk.PX)
        # the note really goes back: along the row, to the stage it belongs to
        self.play(travelling.animate.set_x(x),
                  Transform(stages, row(done=7, lit=SCRIPT, lit_color=tk.HIGHLIGHT)), run_time=2)

        states = [row(done=7, lit=i) for i in range(SCRIPT + 1, REHEARSAL)] + [row(done=8)]
        still = card("render").scale(0.36)
        sx, sy = over(REHEARSAL - 1, 260, still.width / tk.PX)
        still.move_to([sx, sy, 0])
        self.click(Succession(*[Transform(stages, s, run_time=0.45) for s in states]))
        self.play(FadeIn(still, shift=UP * 0.3))
