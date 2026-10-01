"""The greybox: every frame of the storyboard as rough grey boxes, on one standalone page.

Generated from the storyboard, so it never drifts from it: fix the storyboard, not the page. Each
frame shows its slide number and stable ID, its real headline, its `boxes` laid out on the three by
three grid under the headline, and beside it the trigger words and the narration.
"""

from . import page
from .project import Talk
from .script import mmss, pace, target
from .storyboard import REGIONS

CELLS = {
    "top-left": (1, 1),
    "top": (1, 2),
    "top-right": (1, 3),
    "left": (2, 1),
    "center": (2, 2),
    "right": (2, 3),
    "bottom-left": (3, 1),
    "bottom": (3, 2),
    "bottom-right": (3, 3),
    "top-row": (1, "1 / 4"),
    "middle-row": (2, "1 / 4"),
    "bottom-row": (3, "1 / 4"),
}
assert set(CELLS) == REGIONS


def frame_html(frame) -> str:
    cells: dict[str, list[str]] = {}
    for label, region in frame.boxes:
        cells.setdefault(region, []).append(label)
    boxes = "".join(
        f"<div class='box' style='grid-row:{CELLS[r][0]};grid-column:{CELLS[r][1]}'>"
        f"{'<br>'.join(map(page.esc, labels))}</div>"
        for r, labels in cells.items()
    )
    return (
        f"<div class='frame'><div class='screen'><div class='head'>{page.esc(frame.head)}</div>"
        f"<div class='num'>{frame.number}</div><div class='grid'>{boxes}</div></div>"
        f"<div class='text'><p class='id'>slide {frame.number} · {frame.id}</p>"
        f"<p class='trigger'>click on: {page.esc(frame.trigger)}</p>"
        f"<p>{page.esc(frame.narration.replace('**', ''))}</p>"
        + (f"<p class='note'>{page.esc(frame.note)}</p>" if frame.note else "")
        + "</div></div>"
    )


def write(talk: Talk):
    sb = talk.storyboard()
    problems = sb.problems()
    if problems:
        raise ValueError("the storyboard has problems:\n  " + "\n  ".join(problems))
    name, wpm = pace(talk)
    words = sum(sb.words(b) for b in sb.order)
    body, act = [], None
    for frame in sb.frames():
        beat = sb.beat(frame.beat)
        if frame.beat in sb.order and beat.get("act") != act:
            act = beat.get("act")
            body.append(f"<h2>Act {act}: {page.esc(sb.acts.get(act, ''))}</h2>")
        if frame.beat in sb.backup and frame.beat == sb.backup[0] and frame.index == 1:
            body.append("<h2>Backup</h2>")
        if frame.index == 1:
            body.append(
                f"<p class='id'><strong>{frame.beat}</strong> · {page.esc(beat.get('title', ''))}"
                f" · {beat.get('kind', 'beat')} · budget {mmss(beat.get('budget_s', 0))}</p>"
            )
        body.append(frame_html(frame))
    title = talk.config().get("title") or "Talk"
    meta = (
        f"Greybox, {len(sb.frames())} slides, {mmss(words / wpm * 60)} spoken at {name} pace. "
        "Generated from the storyboard by <code>mpp greybox</code>."
    )
    return page.write(target(talk, "4-visual/greybox.html"), f"{title}: greybox", meta, "".join(body))
