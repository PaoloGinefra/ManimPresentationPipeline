"""The fixed furniture of every frame: headline, slide number, draft label, act card, a spine.

Each lives in one place on the screen for the whole talk (the layout tokens), so a listener who
looks away finds them again where they left them.
"""

from manim import DOWN, LEFT, RIGHT, UL, UP, Create, FadeOut, Line, RoundedRectangle, Transform, VGroup, VMobject

from . import tokens as tk


def headline(s: str) -> VGroup:
    """The frame's claim, a sentence, top-left: one line if it fits, else two lines of balanced length
    (a greedy wrap strands the last word on a line of its own). Never three."""
    size = lambda t: tk.words(t, "headline", weight="SEMIBOLD").width
    limit = tk.HEADLINE_MAX_W * tk.PX
    words = s.split()
    if size(s) <= limit:
        lines = [s]
    else:
        splits = [(" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))]
        lines = list(min(splits, key=lambda ab: max(size(ab[0]), size(ab[1]))))
        assert max(map(size, lines)) <= limit, f"headline needs three lines: shorten it: {s!r}"
    block = VGroup(*[tk.words(line, "headline", weight="SEMIBOLD") for line in lines])
    block.arrange(DOWN, aligned_edge=LEFT, buff=tk.CAP["headline"] * tk.PX * 0.7)
    return block.move_to(tk.px(tk.MARGIN_X, tk.MARGIN_TOP), aligned_edge=UL)


def slide_number(n: int):
    """The slide's plain number, top-right: for citing a slide in a question or a note."""
    t = tk.words(str(n), "number", color=tk.MUTED)
    return t.move_to(tk.px(1920 - tk.MARGIN_X, tk.MARGIN_TOP), aligned_edge=UP + RIGHT)


def draft_label(commit: str):
    """Bottom-right, small: which build this is, so a note on it can be traced to its storyboard."""
    t = tk.words(f"draft {commit}", "note", color=tk.STRUCTURE)
    return t.move_to(tk.px(1920 - tk.MARGIN_X, 1080 - tk.MARGIN_BOTTOM), aligned_edge=DOWN + RIGHT)


def title_card(title: str, speaker: str = "", date: str = "") -> VGroup:
    """The talk's title, with who and when under it, centred."""
    card = VGroup(tk.words(title, "title", weight="SEMIBOLD"))
    if speaker or date:
        card.add(tk.words(" · ".join(s for s in (speaker, date) if s), "label", color=tk.MUTED))
    return card.arrange(DOWN, buff=0.35).move_to(tk.px(960, 540))


def act_card(number: int, title: str) -> VGroup:
    """An act's title card, centred."""
    return (
        VGroup(tk.words(f"act {number}", "label", color=tk.MUTED), tk.words(title, "title", weight="SEMIBOLD"))
        .arrange(DOWN, buff=0.2)
        .move_to(tk.px(960, 540))
    )


def spine(items, done: int = 0, current: int | None = None, answers=None) -> VGroup:
    """A progress list, bottom-left: questions, steps, choices.

    Done items carry a tick; the current one is set in ink and the rest are faint. No new hue:
    state is shown by weight and contrast only. With `answers`, a done item reads as its answer
    instead of its question.
    """
    row = VGroup()
    for i, s in enumerate(items):
        active = current == i
        col = tk.INK if (i < done or active) else tk.STRUCTURE
        box = RoundedRectangle(
            corner_radius=0.04, width=0.26, height=0.26, stroke_color=col, stroke_width=3 if active else 2
        )
        text = answers[i] if answers and i < done else s
        item = VGroup(box, tk.words(text, "note", color=col, weight="SEMIBOLD" if active else "NORMAL"))
        item.text_value = text
        item.arrange(RIGHT, buff=0.14)
        if i < done:
            tick = VMobject(stroke_color=tk.INK, stroke_width=4).set_points_as_corners(
                [
                    box.get_center() + [-0.08, 0, 0],
                    box.get_center() + [-0.02, -0.07, 0],
                    box.get_center() + [0.1, 0.09, 0],
                ]
            )
            item.add(tick)
        row.add(item)
    row.arrange(RIGHT, buff=0.5)
    return row.move_to(tk.px(tk.MARGIN_X, 1080 - tk.MARGIN_BOTTOM), aligned_edge=DOWN + LEFT)


def respine(sp, new):
    """Move a spine to a new state item by item: a tick is drawn into its box, a name changes weight in
    place. Morphing the whole spine at once pairs up the wrong parts (a new tick with an old letter),
    and the words shuffle."""
    anims = []
    for old_item, new_item in zip(sp, new):
        anims.append(Transform(old_item[0], new_item[0]))
        if getattr(old_item, "text_value", None) == getattr(new_item, "text_value", None):
            anims.append(Transform(old_item[1], new_item[1]))
        else:
            # new words cross-fade, and the new text takes the old one's place inside the item: a
            # FadeTransform would leave it an orphan that the next slide change fades away
            ghost = old_item[1]
            label = new_item[1].copy().set_opacity(0)
            old_item.submobjects[1] = label
            anims += [FadeOut(ghost), label.animate.set_opacity(1)]
        old_item.text_value = getattr(new_item, "text_value", None)
        if len(new_item) > 2 and len(old_item) == 2:
            old_item.add(new_item[2])
            anims.append(Create(new_item[2]))
    return anims


def rule_under(mob, color=None):
    """A hairline for grouping, when proximity alone is not enough."""
    return Line(
        mob.get_corner(DOWN + LEFT), mob.get_corner(DOWN + RIGHT), stroke_color=color or tk.FAINT, stroke_width=1.5
    ).shift(DOWN * 0.08)
