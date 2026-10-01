"""The talk's cast: the row of stages, the sentence card in each of its forms, the note, the ladder.

Each is drawn here once and reused by every beat, so the row in B8 is the row of B3. Positions are in
1080p pixels; colours and sizes come from the tokens.
"""

from manim import DOWN, LEFT, RIGHT, UP, UL, Line, Rectangle, RoundedRectangle, VGroup, VMobject

from mpp import tokens as tk

STAGES = ["brief", "digest", "outline", "script", "visual", "design", "build", "final"]
ROW_Y = 930  # the row's centre line: above the draft label, below the content
BOX_W, BOX_H, GAP = 180, 56, 26
CARD_Y = 530  # the sentence card's centre line
SENTENCE = "The slowest waits halve once the cache is warm."


def stage_x(i: int) -> float:
    """The centre of stage i's box, in pixels."""
    width = len(STAGES) * BOX_W + (len(STAGES) - 1) * GAP
    return (1920 - width) / 2 + BOX_W / 2 + i * (BOX_W + GAP)


def px_w(n: float) -> float:
    return n * tk.PX


# ------------------------------------------------------------------ the row of stages
def tick(at) -> VMobject:
    return VMobject(stroke_color=tk.INK, stroke_width=4).set_points_as_corners(
        [at + [-0.08, 0, 0], at + [-0.02, -0.07, 0], at + [0.1, 0.09, 0]]
    )


def row(done: int = 0, lit: int | None = None, lit_color=None) -> VGroup:
    """The stages along the bottom. The first `done` carry a tick; `lit` is the stage in focus.

    Every item always holds a box, a label and a tick (invisible until done), so one state of the row
    transforms into another part by part.
    """
    items = VGroup()
    for i, name in enumerate(STAGES):
        on = lit == i
        col = lit_color or tk.OURS
        box = RoundedRectangle(
            corner_radius=0.06,
            width=px_w(BOX_W),
            height=px_w(BOX_H),
            stroke_color=col if on else (tk.INK if i < done else tk.STRUCTURE),
            stroke_width=4 if on else 2,
            fill_color=col,
            fill_opacity=0.12 if on else 0,
        ).move_to(tk.px(stage_x(i), ROW_Y))
        label = tk.words(name, "note", color=tk.INK if (i < done or on) else tk.MUTED)
        label.move_to(box).shift(LEFT * px_w(14))
        mark = tick(box.get_right() + LEFT * px_w(24)).set_stroke(opacity=1 if i < done else 0)
        items.add(VGroup(box, label, mark))
    items.role = "row"
    return items


def above(i: int, height: float = 0) -> list:
    """A point just above stage i's box, `height` pixels up."""
    return tk.px(stage_x(i), ROW_Y - BOX_H / 2 - 14 - height)


# ------------------------------------------------------------------ the sentence card
CARD_W, CARD_H, PAD = 1100, 619, 48  # 16:9: in its last two forms the card is a slide


def _frame():
    return RoundedRectangle(corner_radius=0.06, width=px_w(CARD_W), height=px_w(CARD_H), stroke_color=tk.STRUCTURE,
                            stroke_width=2, fill_color=tk.GROUND, fill_opacity=1)


def _bar(w):
    return Rectangle(width=px_w(w), height=px_w(12), stroke_width=0, fill_color=tk.FAINT, fill_opacity=1)


def _caption(s):
    return tk.words(s, "note", color=tk.MUTED)


def _table(headers, cells, colors, gap=30):
    """A header row, a rule and one row of cells, each column as wide as its widest entry."""
    head = [_caption(h) for h in headers]
    body = [tk.words(s, "note", color=c) for s, c in zip(cells, colors)]
    x = 0.0
    for h, b in zip(head, body):
        w = max(h.width, b.width)
        h.move_to([x, 0, 0], aligned_edge=LEFT)
        b.move_to([x, -px_w(56), 0], aligned_edge=LEFT)
        x += w + px_w(gap)
    rule = Line([0, -px_w(26), 0], [x - px_w(gap), -px_w(26), 0], stroke_color=tk.STRUCTURE, stroke_width=1.5)
    return VGroup(*head, rule, *body)


def card(form: str) -> VGroup:
    """The thread sentence in one stage's form. Every form is the same 16:9 card, so moving from one
    to the next reads as the same object changing; in the last two forms the card is the slide."""
    frame = _frame()
    corner = None
    if form == "source":
        body = VGroup(_caption("results.md"), _bar(640), _bar(600),
                      tk.words(SENTENCE, "label", color=tk.OURS), _bar(660), _bar(420))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(26))
    elif form == "digest":
        body = _table(["#", "claim", "source"], ["C3", SENTENCE, "results.md"], [tk.INK, tk.OURS, tk.INK])
    elif form == "outline":
        body = _table(["ID", "type", "spine line", "time"], ["B3", "PEAK", SENTENCE, "1:10"],
                      [tk.INK, tk.INK, tk.OURS, tk.INK])
    elif form == "script":
        body = VGroup(_caption("### B3. The cache warms - 1:10"),
                      tk.words(SENTENCE, "label", color=tk.OURS, weight="SEMIBOLD"),
                      _bar(660), _bar(560), _caption("> the bars of the slow requests shrink"))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(24))
    elif form == "storyboard":
        def field(k, v):
            return VGroup(tk.words(f"{k} =", "note", color=tk.MUTED), v).arrange(RIGHT, buff=px_w(10))
        body = VGroup(_caption("[[B3.frame]]"),
                      field("head", tk.words(f'"{SENTENCE}"', "note", color=tk.OURS)),
                      field("trigger", tk.words('"once the cache is warm"', "note")),
                      field("narration", _bar(420)))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(26))
        corner = tk.words("B3.2", "note", color=tk.MUTED)
    elif form in ("greybox", "render"):
        head = tk.words(SENTENCE, "label", color=tk.INK, weight="SEMIBOLD")
        head.move_to(frame.get_corner(UL) + [px_w(PAD), -px_w(PAD), 0], aligned_edge=UL)
        corner = tk.words("7", "note", color=tk.MUTED)
        base = Line(LEFT * px_w(200), RIGHT * px_w(200), stroke_color=tk.STRUCTURE, stroke_width=2)
        if form == "greybox":
            fills = (tk.FAINT, tk.FAINT)
            heights = (200, 200)
            names = VGroup(_caption("bar"), _caption("bar"))
        else:
            fills = (tk.STRUCTURE, tk.OURS)
            heights = (200, 100)
            names = VGroup(_caption("cold"), _caption("warm"))
        bars = VGroup(*[Rectangle(width=px_w(110), height=px_w(h), stroke_width=0, fill_color=f, fill_opacity=1)
                        for f, h in zip(fills, heights)])
        for b, dx in zip(bars, (-90, 90)):
            b.next_to(base, UP, buff=0).shift(RIGHT * px_w(dx))
        for n, b in zip(names, bars):
            n.next_to(b, DOWN, buff=px_w(16)).set_y(base.get_y() - px_w(30))
        chart = VGroup(base, bars, names).move_to(frame.get_center() + DOWN * px_w(40))
        body = VGroup(head, chart)
    else:
        raise ValueError(form)
    if form not in ("greybox", "render"):
        body.move_to(frame)
    out = VGroup(frame, body)
    if corner is not None:
        out.add(corner.move_to(frame.get_corner(UP + RIGHT) + [-px_w(PAD), -px_w(PAD) + px_w(8), 0], aligned_edge=UP + RIGHT))
    out.role = "card"
    out.form = form
    return out


def card_at(form: str, stage: int) -> VGroup:
    """The card in `form`, above `stage`, kept on screen."""
    c = card(form)
    half = c.width / tk.PX / 2
    x = min(max(stage_x(stage), tk.MARGIN_X + half), 1920 - tk.MARGIN_X - half)
    return c.move_to(tk.px(x, CARD_Y))


# ------------------------------------------------------------------ the note
def note(text: str = "slide 7: say halves, not 48%", width: float = 420) -> VGroup:
    box = RoundedRectangle(corner_radius=0.06, width=px_w(width), height=px_w(70), stroke_color=tk.HIGHLIGHT,
                           stroke_width=3, fill_color=tk.HIGHLIGHT, fill_opacity=0.12)
    t = tk.words(text, "note", color=tk.INK).move_to(box)
    n = VGroup(box, t)
    n.role = "note"
    return n


# ------------------------------------------------------------------ the ladder
RUNGS = ["outline", "script", "storyboard", "deck"]
RUNG_TO_STAGE = [2, 3, 4, 6]  # outline, script, visual, build


def ladder() -> VGroup:
    """Four rungs, cheapest at the bottom, each wider than the one below: the cost of a change, drawn
    without numbers because it was never measured."""
    rungs = VGroup()
    for i, name in enumerate(RUNGS):
        w = 260 + 200 * i
        rect = RoundedRectangle(corner_radius=0.06, width=px_w(w), height=px_w(BOX_H), stroke_color=tk.STRUCTURE,
                                stroke_width=2)
        rect.move_to(tk.px(1060, 820 - i * 120))
        label = tk.words(name, "note", color=tk.INK).next_to(rect, LEFT, buff=px_w(24))
        rungs.add(VGroup(rect, label))
    cheap = _caption("cheap to change").next_to(rungs[0], DOWN, buff=px_w(20))
    dear = _caption("expensive to change").next_to(rungs[-1], UP, buff=px_w(20))
    out = VGroup(rungs, cheap, dear)
    out.role = "ladder"
    return out
