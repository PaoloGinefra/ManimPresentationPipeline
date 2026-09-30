"""The review log: one row per note, 7-review/log.md, a Markdown table people can read and edit.

A note given by slide number is translated to its stable ID through the storyboard at the build the
author saw, so a note on an old draft still lands on the right frame.
"""

import datetime
import re
import subprocess
from pathlib import Path

from .project import REPO, Talk

COLUMNS = ["#", "date", "build", "slide", "ID", "note", "stage", "fix", "commit", "status"]
NOTE_STAGES = ["brief", "digest", "outline", "script", "visual", "design", "build"]
TEMPLATE = REPO / "pipeline" / "templates" / "7-review" / "log.md"


def path(talk: Talk) -> Path:
    return talk.root / talk.layers[0] / "7-review" / "log.md"


def cell(s: str) -> str:
    return " ".join(str(s).split()).replace("|", "\\|")


def read(talk: Talk) -> tuple[list[str], list[dict]]:
    """The file's lines before the table, and the rows."""
    p = path(talk)
    text = (p if p.exists() else TEMPLATE).read_text()
    head, rows = [], []
    for line in text.splitlines():
        if not line.startswith("|"):
            if not rows:
                head.append(line)
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])]
        if cells[0].isdigit() and len(cells) == len(COLUMNS):
            rows.append(dict(zip(COLUMNS, cells)))
    return head, rows


def write(talk: Talk, head: list[str], rows: list[dict]) -> Path:
    while head and not head[-1].strip():
        head.pop()
    lines = [*head, "", "| " + " | ".join(COLUMNS) + " |", "|" + "---|" * len(COLUMNS)]
    lines += ["| " + " | ".join(cell(r[c]) for c in COLUMNS) + " |" for r in rows]
    p = path(talk)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n")
    return p


def short(talk: Talk, rev: str = "HEAD") -> str:
    r = subprocess.run(["git", "rev-parse", "--short", rev], cwd=talk.root, capture_output=True, text=True)
    if r.returncode:
        raise ValueError(f"no commit {rev!r}")
    return r.stdout.strip()


def add(talk: Talk, slide: str, note: str, stage: str, build: str | None = None) -> dict:
    if stage not in NOTE_STAGES:
        raise ValueError(f"stage must be one of {', '.join(NOTE_STAGES)}")
    build = short(talk, (build or "HEAD").split()[0])
    frame = Talk(talk.root, talk.variant, commit=build).storyboard().resolve(slide) if slide else None
    head, rows = read(talk)
    row = {
        "#": str(max((int(r["#"]) for r in rows), default=0) + 1),
        "date": datetime.date.today().isoformat(),
        "build": build,
        "slide": str(frame.number) if frame else "",
        "ID": frame.id if frame else "",
        "note": note,
        "stage": stage,
        "fix": "",
        "commit": "",
        "status": "open",
    }
    write(talk, head, [*rows, row])
    return row


def close(talk: Talk, number: str, status: str, fix: str, commit: str | None = None) -> dict:
    head, rows = read(talk)
    hit = [r for r in rows if r["#"] == str(number)]
    if not hit:
        raise KeyError(f"no note #{number} in {path(talk).relative_to(talk.root)}")
    hit[0].update(status=status, fix=fix, commit=short(talk, commit or "HEAD"))
    write(talk, head, rows)
    return hit[0]
