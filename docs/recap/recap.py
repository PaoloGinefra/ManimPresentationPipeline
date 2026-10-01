"""The README's recap: the pipeline in thirty seconds, drawn with the example talk's own cast.

A silent loop: the row of stages, the cache talk's card changing form as it travels along it, a late
note going back to its stage, the release. Rendered by docs/recap/render.sh, which points the engine
at examples/pipeline-talk for its tokens and components.
"""

from components.pipeline import STAGES, above, card, note, px_w, row, stage_x
from manim import DOWN, UP, AnimationGroup, FadeIn, FadeOut, FadeTransform, LaggedStart, Scene, Succession, Transform, VGroup

from mpp import chrome
from mpp import tokens as tk

tk.apply_style()

SCALE = 0.72  # the card, small enough to travel above the row
STEPS = [
    ("brief", "brief", "Brief: who is in the room, how long, the one sentence."),
    ("digest", "digest", "Digest: everything the talk could say, with its source."),
    ("outline-focus", "outline", "Outline: the story on one page; then follow one sentence."),
    ("script", "script", "Script: written for the ear, read aloud."),
    ("storyboard", "visual", "Storyboard: one frame per click."),
    ("greybox", "visual", "Greybox: every slide as rough boxes, before any render."),
    ("specimen", "design", "Design: the look, fixed once, on one page."),
    ("render", "build", "Build: drafts first, checked at every click."),
]
HOLD = 2.0  # long enough to read the caption: the change itself takes 1 s


def placed(form: str, stage: int) -> VGroup:
    """The card in `form`, above `stage`, kept inside the margins."""
    c = card(form).scale(SCALE)
    half = c.width / tk.PX / 2
    x = min(max(stage_x(stage), tk.MARGIN_X + half), 1920 - tk.MARGIN_X - half)
    return c.move_to(tk.px(x, 520))


class Recap(Scene):
    def caption(self, text: str, old=None):
        new = chrome.headline(text)
        if old is None:
            return new, [FadeIn(new, shift=UP * 0.18)]
        return new, [AnimationGroup(FadeOut(old, shift=UP * 0.18), FadeIn(new, shift=UP * 0.18), lag_ratio=0.6)]

    def construct(self):
        title = VGroup(tk.words("manim-presentation-pipeline", "title", weight="SEMIBOLD"),
                       tk.words("from a source to a spoken script and an animated deck", "label", color=tk.MUTED))
        title.arrange(DOWN, buff=px_w(28)).move_to(tk.px(960, 500))
        self.play(FadeIn(title, shift=UP * 0.2), run_time=1.2)
        self.wait(1.6)

        stages = row()
        head, anims = self.caption("Nine stages, each ending with something short the author checks.")
        self.play(FadeOut(title), *anims, LaggedStart(*[FadeIn(item) for item in stages], lag_ratio=0.12), run_time=1.6)
        self.wait(1.2)

        current = None
        for form, stage_name, text in STEPS:
            i = STAGES.index(stage_name)
            new_card = placed(form, i)
            head, anims = self.caption(text, head)
            move = FadeIn(new_card, shift=UP * 0.2) if current is None else FadeTransform(current, new_card)
            self.play(move, *anims, Transform(stages, row(done=i, lit=i)), run_time=1.0)
            self.wait(HOLD)
            current = new_card
        self.play(Transform(stages, row(done=7)), run_time=0.5)

        # rehearsal: a late note goes back to the earliest stage it changes
        rehearsal, script = STAGES.index("rehearsal"), STAGES.index("script")
        msg = note(width=520)
        msg.move_to([min(above(rehearsal, 300)[0], tk.px(1920 - tk.MARGIN_X - 260, 0)[0]), above(rehearsal, 300)[1], 0])
        head, anims = self.caption("Rehearsal: a late note goes back to the earliest stage it changes.", head)
        self.play(FadeOut(current), run_time=0.5)  # one picture leaves before the next arrives
        self.play(FadeIn(msg, shift=DOWN * 0.3), *anims, Transform(stages, row(done=7, lit=rehearsal)), run_time=1.0)
        self.wait(0.8)
        self.play(msg.animate.move_to([above(script, 300)[0], msg.get_y(), 0]),
                  Transform(stages, row(done=7, lit=script, lit_color=tk.HIGHLIGHT)), run_time=1.6)
        ripple = [row(done=7, lit=k) for k in range(script + 1, rehearsal)] + [row(done=8)]
        self.play(Succession(*[Transform(stages, r, run_time=0.35) for r in ripple]))
        self.wait(1.4)

        final = STAGES.index("final")
        release = placed("release", final)
        head, anims = self.caption("Final: the deck, the script and the design system, offline.", head)
        self.play(FadeOut(msg), run_time=0.5)
        self.play(FadeIn(release, shift=UP * 0.2), *anims, Transform(stages, row(done=8, lit=final)), run_time=1.0)
        self.play(Transform(stages, row(done=9)), run_time=0.6)
        self.wait(1.8)

        end = VGroup(tk.words("Clone it, then:", "label", color=tk.MUTED),
                     tk.words("uv run mpp status", "headline", color=tk.OURS, weight="SEMIBOLD"))
        end.arrange(DOWN, buff=px_w(24)).move_to(tk.px(960, 500))
        self.play(FadeOut(release), FadeOut(head), run_time=0.6)
        self.play(FadeIn(end, shift=UP * 0.2), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(end), FadeOut(stages), run_time=0.8)
        self.wait(0.2)
