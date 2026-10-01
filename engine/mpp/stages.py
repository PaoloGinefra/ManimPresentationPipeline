"""The stages, their approval tags, and what is next.

An approval is a git tag `<variant>/<stage>-<n>` (`global/outline-2`); `n` counts the approvals of
that stage, so a stage re-approved after a backtrack keeps its history. A stage whose folder changed
since its last approval is shown as changed: it needs approving again.
"""

import subprocess
from dataclasses import dataclass

from .project import Talk


@dataclass
class Stage:
    name: str
    folder: str
    optional: bool = False


STAGES = [
    Stage("brief", "0-brief"),
    Stage("digest", "1-digest"),
    Stage("outline", "2-outline"),
    Stage("script", "3-script"),
    Stage("visual", "4-visual"),
    Stage("design", "5-design"),
    Stage("build", "6-build"),
    Stage("rehearsal", "7-review", optional=True),
]
BY_NAME = {s.name: s for s in STAGES}


def git(talk: Talk, *args) -> str:
    r = subprocess.run(["git", *args], cwd=talk.root, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def approvals(talk: Talk, stage: str) -> list[str]:
    """This talk's approval tags for a stage, oldest first."""
    tags = git(talk, "tag", "--list", f"{talk.tag_base}/{stage}-*").split()
    return sorted(tags, key=lambda t: int(t.rsplit("-", 1)[1]))


def changed_since(talk: Talk, tag: str, folder: str) -> bool:
    """Whether the stage's files, in any layer this talk reads, differ from the tag (committed or not)."""
    paths = [f"{layer}/{folder}" for layer in talk.layers]
    r = subprocess.run(["git", "diff", "--quiet", tag, "--", *paths], cwd=talk.root)
    return r.returncode != 0


def owner(talk: Talk, stage: Stage) -> Talk:
    """Whose approval a stage needs: a variant's own if it overrides files of that stage, else
    global's, which the variant then reads unchanged."""
    if talk.variant and not (talk.root / talk.layers[0] / stage.folder).is_dir():
        return Talk(talk.root)
    return talk


def status(talk: Talk) -> list[dict]:
    rows = []
    for s in STAGES:
        who = owner(talk, s)
        tags = approvals(who, s.name)
        present = [p for p in talk.dirs(s.folder) if any(f.name != ".gitkeep" for f in p.rglob("*") if f.is_file())]
        rows.append(
            {
                "stage": s,
                "tag": tags[-1] if tags else None,
                "changed": bool(tags) and changed_since(who, tags[-1], s.folder),
                "has_files": bool(present),
            }
        )
    return rows


def next_stage(rows: list[dict]) -> Stage | None:
    """The first required stage that is unapproved or changed since its approval."""
    for r in rows:
        if not r["stage"].optional and (r["tag"] is None or r["changed"]):
            return r["stage"]
    return None


def approve(talk: Talk, stage: str, message: str = "") -> str:
    if stage not in BY_NAME:
        raise ValueError(f"no stage {stage!r}; stages are {', '.join(BY_NAME)}")
    folder = BY_NAME[stage].folder
    if owner(talk, BY_NAME[stage]) is not talk:
        raise RuntimeError(f"{talk.name} has no {folder} of its own: it reads global's, so approve it in global")
    paths = [f"{layer}/{folder}" for layer in talk.layers]
    if git(talk, "status", "--porcelain", "--", *paths):
        raise RuntimeError(f"{folder} has uncommitted changes: commit them, then approve")
    tags = approvals(talk, stage)
    if tags and not changed_since(talk, tags[-1], folder):
        raise RuntimeError(f"{stage} is unchanged since {tags[-1]}: nothing new to approve")
    tag = f"{talk.tag_base}/{stage}-{len(tags) + 1}"
    git(talk, "tag", "-a", tag, "-m", message or f"{talk.name}: {stage} approved")
    return tag


def variants(talk: Talk) -> list[str]:
    folder = talk.root / "talk" / "variants"
    return sorted(p.name for p in folder.iterdir() if p.is_dir()) if folder.is_dir() else []
