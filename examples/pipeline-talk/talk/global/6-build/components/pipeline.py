"""The talk's cast: the row of stages, the card in each of its forms, the check list, the note, the
ladder.

Each is drawn here once and reused by every beat, so the row in B8 is the row of B3. Positions are in
1080p pixels; colours and sizes come from the tokens. Alignment is designed in: every left edge sits
on the margin or on a column, and labels that share a line share a baseline (`tk.set_baseline`).
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    Circle,
    DashedVMobject,
    Line,
    Rectangle,
    RoundedRectangle,
    VGroup,
    VMobject,
)

from mpp import tokens as tk

STAGES = ["brief", "digest", "outline", "script", "visual", "design", "build", "rehearsal", "final"]
OPTIONAL = {"rehearsal"}
ROW_Y = 930  # the row's centre line: above the draft label, below the content
GAP = 18
BOX_W = (1920 - 2 * tk.MARGIN_X - (len(STAGES) - 1) * GAP) / len(STAGES)  # margin to margin
BOX_H = 56
CARD_Y = 530  # the card's centre line
SHRINK = 0.55  # the card, set aside while the check list is read
CHECKS_X = 820  # the check list's left edge, in pixels
SENTENCE = "The slowest waits halve once the cache is warm."


def px_w(n: float) -> float:
    return n * tk.PX


def stage_x(i: int) -> float:
    """The centre of stage i's box, in pixels."""
    return tk.MARGIN_X + BOX_W / 2 + i * (BOX_W + GAP)


def line_y(centre_px: float, role: str = "note") -> float:
    """The baseline, in scene units, that centres a role's capital letters on `centre_px`."""
    return tk.px(0, centre_px + tk.CAP[role] / 2)[1]


def tick_mark(at, size=1.0, color=None) -> VMobject:
    s = px_w(10) * size
    return VMobject(stroke_color=color or tk.GROUND, stroke_width=3.5 * size).set_points_as_corners(
        [at + [-s, 0, 0], at + [-0.3 * s, -0.7 * s, 0], at + [1.1 * s, 0.9 * s, 0]]
    )


# ------------------------------------------------------------------ the row of stages
def row(done: int = 0, lit: int | None = None, lit_color=None) -> VGroup:
    """The stages along the bottom. The first `done` carry a tick badge; `lit` is the stage in focus.

    Every item always holds the same four parts (fill, outline, label, badge), invisible where unused,
    so one state of the row transforms into another part by part."""
    items = VGroup()
    col = lit_color or tk.OURS
    for i, name in enumerate(STAGES):
        on, finished = lit == i, i < done
        shape = RoundedRectangle(corner_radius=0.06, width=px_w(BOX_W), height=px_w(BOX_H)).move_to(
            tk.px(stage_x(i), ROW_Y)
        )
        fill = shape.copy().set_stroke(width=0).set_fill(col, opacity=0.12 if on else 0)
        stroke = col if on else (tk.INK if finished else tk.STRUCTURE)
        outline = shape.copy().set_fill(opacity=0).set_stroke(stroke, width=3.5 if on else 2)
        if name in OPTIONAL:
            outline = DashedVMobject(outline, num_dashes=36, dashed_ratio=0.6)
        label = tk.words(name, "note", color=tk.INK if (finished or on) else tk.MUTED)
        label.set_x(shape.get_x())
        tk.set_baseline(label, line_y(ROW_Y))
        corner = shape.get_corner(UP + RIGHT)
        dot = Circle(radius=px_w(13), stroke_width=0, fill_color=tk.INK, fill_opacity=1).move_to(corner)
        badge = VGroup(dot, tick_mark(corner, 0.8))
        badge.set_opacity(1 if finished else 0)
        items.add(VGroup(fill, outline, label, badge))
    items.role = "row"
    return items


def above(i: int, height: float = 0) -> list:
    """A point above stage i's box, `height` pixels up."""
    return tk.px(stage_x(i), ROW_Y - BOX_H / 2 - 14 - height)


# ------------------------------------------------------------------ the card
CARD_W, CARD_H, PAD = 1100, 619, 56  # 16:9: in its slide forms the card is the slide


def _frame():
    return RoundedRectangle(corner_radius=0.06, width=px_w(CARD_W), height=px_w(CARD_H), stroke_color=tk.STRUCTURE,
                            stroke_width=2, fill_color=tk.GROUND, fill_opacity=1)


def _bar(w):
    return Rectangle(width=px_w(w), height=px_w(12), stroke_width=0, fill_color=tk.FAINT, fill_opacity=1)


def _caption(s):
    return tk.words(s, "note", color=tk.MUTED)


def _rows(rows, colors=None, gap=36, pitch=56, header=None):
    """A table: columns as wide as their widest cell, every cell of a row on one baseline, every
    column on one left edge. `colors` gives a colour per row, or a list of colours per cell."""
    lines = ([header] if header else []) + list(rows)
    cells = []
    for r, line in enumerate(lines):
        is_head = header is not None and r == 0
        row_col = None if is_head else (colors[r - (1 if header else 0)] if colors else None)
        cells.append([
            _caption(s) if is_head
            else tk.words(s, "note", color=(row_col[c] if isinstance(row_col, list) else row_col) or tk.INK)
            for c, s in enumerate(line)
        ])
    widths = [max(cells[r][c].width for r in range(len(cells))) for c in range(len(cells[0]))]
    out = VGroup()
    x = 0.0
    for r, line in enumerate(cells):
        x = 0.0
        y = -r * px_w(pitch)
        for c, cell in enumerate(line):
            cell.move_to([x, 0, 0], aligned_edge=LEFT)
            tk.set_baseline(cell, y)
            x += widths[c] + px_w(gap)
        out.add(VGroup(*line))
    if header:
        rule_y = -px_w(pitch) / 2 + px_w(6)
        out.add(Line([0, rule_y, 0], [x - px_w(gap), rule_y, 0], stroke_color=tk.STRUCTURE, stroke_width=1.5))
    return out


def _fields(pairs, colors=None):
    """Key-value lines: keys in one column, values in the next, each pair on one baseline."""
    colors = colors or [None] * len(pairs)
    return _rows([[k, v] for k, v in pairs], colors=[[tk.MUTED, c or tk.INK] for c in colors])


OUTLINE = [
    ["B1", "setup", "At rush hour, users wait.", "0:45"],
    ["B2", "obstacle", "A cold cache makes it worse.", "0:50"],
    ["B3", "PEAK", SENTENCE, "1:10"],
    ["B4", "payoff", "The cache warms itself.", "0:40"],
]


def card(form: str) -> VGroup:
    """The cache talk at one stage, as one 16:9 card. Every form's content starts at the same left
    edge and is centred vertically, so moving from one form to the next reads as the same card
    changing, never as content jumping sideways."""
    frame = _frame()
    corner = None
    if form == "title":
        body = VGroup(tk.words("Warm caches", "title", weight="SEMIBOLD"),
                      tk.words("a talk to the systems group, made with the pipeline", "label", color=tk.MUTED))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(28))
    elif form == "brief":
        body = VGroup(_caption("brief.md"), _fields([
            ("audience", "the systems group"),
            ("slot", "10 minutes, normal pace"),
            ("one sentence", "A cache that warms itself halves the slowest waits."),
            ("held back", "the eviction policy"),
        ]))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
    elif form == "digest":
        body = VGroup(_caption("digest.md"), _rows(
            [["Most requests repeat within a minute.", "logs/", "must"],
             ["The cache fills itself as it serves.", "cache.py", "could"],
             [SENTENCE, "bench/", "must"]],
            colors=[None, None, [tk.OURS, tk.INK, tk.INK]],
            header=["claim", "source", "sort"]))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
    elif form == "options":
        body = VGroup(_caption("options.md"), _rows(
            [["hook", "a queue at rush hour", "a cold start", "a question"],
             ["thread", "one user's request", "one slow page", "the cache itself"],
             ["peaks", "the cache warming", "the slow tail halving", "a cold restart"]],
            colors=[[tk.MUTED, tk.OURS, tk.INK, tk.INK], [tk.MUTED, tk.OURS, tk.INK, tk.INK],
                    [tk.MUTED, tk.OURS, tk.OURS, tk.INK]]))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
    elif form in ("outline", "outline-focus"):
        dim = tk.FAINT if form == "outline-focus" else tk.INK
        colors = [[dim] * 4, [dim] * 4, [tk.INK, tk.INK, tk.OURS, tk.INK], [dim] * 4]
        body = VGroup(_caption("outline.md"), _rows(OUTLINE, colors=colors, header=["ID", "type", "spine line", "time"]))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
    elif form == "script":
        body = VGroup(_caption("### B3. The cache warms - 1:10"),
                      tk.words(SENTENCE, "label", color=tk.OURS, weight="SEMIBOLD"),
                      _bar(660), _bar(560), _caption("> the bars of the slow requests shrink"))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(26))
    elif form == "storyboard":
        body = VGroup(_caption("[[B3.frame]]"), _fields(
            [("head =", f'"{SENTENCE}"'), ("trigger =", '"once the cache is warm"'), ("narration =", '"..."')],
            colors=[tk.OURS, None, tk.MUTED]))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
        corner = tk.words("B3.2", "note", color=tk.MUTED)
    elif form == "specimen":
        chips = VGroup()
        for role in ("ink", "ours", "baseline", "highlight", "structure"):
            chip = RoundedRectangle(corner_radius=0.04, width=px_w(64), height=px_w(64), stroke_width=0,
                                    fill_color=tk.COLORS[role], fill_opacity=1)
            name = _caption(role)
            name.set_x(chip.get_x())
            tk.set_baseline(name, chip.get_bottom()[1] - px_w(40))
            chips.add(VGroup(chip, name))
        chips.arrange(RIGHT, buff=px_w(40), aligned_edge=UP)
        types = VGroup(*[tk.words(f"{r}, {tk.CAP[r]} px", r, weight="SEMIBOLD" if r == "headline" else "NORMAL")
                         for r in ("headline", "label", "note")]).arrange(DOWN, aligned_edge=LEFT, buff=px_w(22))
        body = VGroup(_caption("specimen"), chips, types).arrange(DOWN, aligned_edge=LEFT, buff=px_w(40))
    elif form == "release":
        body = VGroup(_caption("releases/global/v1/"), _rows(
            [["talk.html", "the animated deck, offline"],
             ["talk.pdf", "one page per click"],
             ["script.pdf", "the script, with every click"],
             ["design.md, tokens.toml", "the design system"]],
            colors=[[tk.OURS, tk.INK]] * 4))
        body.arrange(DOWN, aligned_edge=LEFT, buff=px_w(34))
    elif form in ("greybox", "render"):
        head = tk.words(SENTENCE, "label", color=tk.INK, weight="SEMIBOLD")
        head.move_to(frame.get_corner(UL) + [px_w(PAD), -px_w(PAD), 0], aligned_edge=UL)
        corner = tk.words("7", "note", color=tk.MUTED)
        base = Line(LEFT * px_w(200), RIGHT * px_w(200), stroke_color=tk.STRUCTURE, stroke_width=2)
        grey = form == "greybox"
        fills = (tk.FAINT, tk.FAINT) if grey else (tk.STRUCTURE, tk.OURS)
        heights = (200, 200) if grey else (200, 100)
        bars = VGroup(*[Rectangle(width=px_w(110), height=px_w(h), stroke_width=0, fill_color=f, fill_opacity=1)
                        for f, h in zip(fills, heights)])
        names = VGroup(*[_caption(s) for s in (("bar", "bar") if grey else ("cold", "warm"))])
        for b, n, dx in zip(bars, names, (-90, 90)):
            b.next_to(base, UP, buff=0).shift(RIGHT * px_w(dx))
            n.set_x(b.get_x())
            tk.set_baseline(n, base.get_y() - px_w(40))
        chart = VGroup(base, bars, names).move_to(frame.get_center() + DOWN * px_w(40))
        body = VGroup(head, chart)
    else:
        raise ValueError(form)
    if form not in ("greybox", "render"):
        body.move_to(frame.get_left() + RIGHT * px_w(PAD), aligned_edge=LEFT)
    out = VGroup(frame, body)
    if corner is not None:
        corner.move_to(frame.get_corner(UP + RIGHT) + [-px_w(PAD), -px_w(PAD), 0], aligned_edge=UP + RIGHT)
        out.add(corner)
    out.role = "card"
    out.form = form
    return out


def card_centre(form: str) -> VGroup:
    return card(form).move_to(tk.px(960, CARD_Y))


CHECKS_TOP = 330  # the check list's title line, in pixels; the card set aside hangs from its capitals


def aside(c: VGroup) -> VGroup:
    """Where a card stands, shrunk, while the check list is read: on the left margin, its top level
    with the capitals of the list's title."""
    small = c.copy().scale(SHRINK)
    return small.move_to(tk.px(tk.MARGIN_X, CHECKS_TOP - tk.CAP["label"] / 2), aligned_edge=UL)


# ------------------------------------------------------------------ the check list
def checks(items) -> VGroup:
    """'The author checks', then one line per check, each with a box that is ticked later. Every
    line starts on one left edge; each box sits on its line's capital letters."""
    title = tk.words("The author checks", "label", color=tk.MUTED)
    title.move_to(tk.px(CHECKS_X, 0), aligned_edge=LEFT)
    tk.set_baseline(title, line_y(CHECKS_TOP, "label"))
    lines = VGroup()
    for k, s in enumerate(items):
        y = 410 + 74 * k
        box = RoundedRectangle(corner_radius=0.03, width=px_w(30), height=px_w(30), stroke_color=tk.INK,
                               stroke_width=2.5)
        box.move_to(tk.px(CHECKS_X + 15, y))
        text = tk.words(s, "label")
        text.move_to(tk.px(CHECKS_X + 54, 0), aligned_edge=LEFT)
        tk.set_baseline(text, line_y(y, "label"))
        mark = tick_mark(box.get_center(), 1.0, color=tk.INK).set_stroke(opacity=0)
        lines.add(VGroup(box, text, mark))
    out = VGroup(title, lines)
    out.role = "checks"
    return out


# ------------------------------------------------------------------ the note
def note(text: str = "slide 7: say halves, not 48%", width: float = 600, size: str = "label") -> VGroup:
    box = RoundedRectangle(corner_radius=0.06, width=px_w(width), height=px_w(104 if size == "label" else 70),
                           stroke_color=tk.HIGHLIGHT, stroke_width=3, fill_color=tk.HIGHLIGHT, fill_opacity=0.12)
    t = tk.words(text, size, color=tk.INK)
    t.set_x(box.get_x())
    tk.set_baseline(t, box.get_y() - tk.CAP[size] * tk.PX / 2)
    n = VGroup(box, t)
    n.role = "note"
    return n


# ------------------------------------------------------------------ the ladder
RUNGS = ["outline", "script", "storyboard", "deck"]
RUNG_TO_STAGE = [2, 3, 4, 6]  # outline, script, visual, build
RUNG_X = 760  # every rung starts here; the labels end 28 px to its left


def ladder() -> VGroup:
    """Four rungs, cheapest at the bottom, each longer than the one below: the cost of a change,
    drawn without numbers because it was never measured. Rungs share a left edge, labels a right
    edge, and each label sits on its rung's line."""
    rungs = VGroup()
    for i, name in enumerate(RUNGS):
        y = 800 - i * 120
        rect = RoundedRectangle(corner_radius=0.06, width=px_w(260 + 200 * i), height=px_w(BOX_H),
                                stroke_color=tk.STRUCTURE, stroke_width=2)
        rect.move_to(tk.px(RUNG_X, y), aligned_edge=LEFT)
        label = tk.words(name, "label")
        label.move_to(tk.px(RUNG_X - 28, 0), aligned_edge=RIGHT)
        tk.set_baseline(label, line_y(y, "label"))
        rungs.add(VGroup(rect, label))
    cheap = _caption("cheap to change").move_to(tk.px(RUNG_X, 0), aligned_edge=LEFT)
    tk.set_baseline(cheap, line_y(800 + 70))
    dear = _caption("expensive to change").move_to(tk.px(RUNG_X, 0), aligned_edge=LEFT)
    tk.set_baseline(dear, line_y(800 - 3 * 120 - 70))
    out = VGroup(rungs, cheap, dear)
    out.role = "ladder"
    return out
