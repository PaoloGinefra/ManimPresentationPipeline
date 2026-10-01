"""The storyboard: the talk's text, and the numbering that turns a slide number into a stable ID.

Frames are numbered 1, 2, 3 ... through `order`, then on through `backup`. The numbering is a
function of the storyboard alone, so the conversion table of any draft is recomputed from the
storyboard at that draft's commit; nothing is stored.
"""

import re
from dataclasses import dataclass

KINDS = {"beat", "peak", "stop"}
REGIONS = {"top-left", "top", "top-right", "left", "center", "right", "bottom-left", "bottom", "bottom-right"}
REGIONS |= {"top-row", "middle-row", "bottom-row"}  # the full width: a timeline, a caption bar
FRAME_FIELDS = ("head", "trigger", "narration")


@dataclass
class Frame:
    beat: str
    index: int  # 1-based, inside the beat
    number: int  # on the slide
    head: str
    trigger: str
    narration: str
    note: str
    boxes: list

    @property
    def id(self) -> str:
        return f"{self.beat}.{self.index}"


def boxes(frame: dict) -> list[tuple[str, str]]:
    """`"label @ region"` entries as (label, region)."""
    out = []
    for b in frame.get("boxes", []):
        label, _, region = b.rpartition("@")
        out.append((label.strip(), region.strip()))
    return out


def spoken(narration: str) -> str:
    """Narration as said: stage directions (a parenthesised whole) say nothing, markup is dropped."""
    n = " ".join((narration or "").split())
    if n.startswith("(") and n.endswith(")"):
        return ""
    return n.replace("**", "")


class Storyboard:
    def __init__(self, data: dict):
        self.data = data
        self.order: list[str] = list(data.get("order", []))
        self.backup: list[str] = list(data.get("backup", []))
        self.acts: dict[int, str] = {int(k): v for k, v in data.get("acts", {}).items()}

    def beat(self, beat_id: str) -> dict:
        return self.data[beat_id]

    def sequence(self) -> list[str]:
        return self.order + self.backup

    def previous(self, beat_id: str) -> str | None:
        """The beat whose last picture this one opens on; backups open on nothing."""
        if beat_id not in self.order:
            return None
        i = self.order.index(beat_id)
        return self.order[i - 1] if i else None

    def first_number(self, beat_id: str) -> int:
        seq = self.sequence()
        return 1 + sum(len(self.data[b]["frame"]) for b in seq[: seq.index(beat_id)])

    def frames(self, beats: list[str] | None = None) -> list[Frame]:
        out, n = [], 1
        for b in self.sequence():
            for i, f in enumerate(self.data[b]["frame"], 1):
                if beats is None or b in beats:
                    out.append(
                        Frame(
                            b,
                            i,
                            n,
                            f.get("head", ""),
                            f.get("trigger", ""),
                            f.get("narration", ""),
                            f.get("note", ""),
                            boxes(f),
                        )
                    )
                n += 1
        return out

    def resolve(self, ref: str) -> Frame:
        """A slide number ("7") or a stable ID ("B3.2") to its frame."""
        frames = self.frames()
        if ref.isdigit():
            hit = [f for f in frames if f.number == int(ref)]
        else:
            hit = [f for f in frames if f.id == ref]
        if not hit:
            raise KeyError(f"no slide {ref!r} in this storyboard")
        return hit[0]

    def words(self, beat_id: str) -> int:
        return sum(len(spoken(f.get("narration", "")).split()) for f in self.data[beat_id]["frame"])

    def problems(self) -> list[str]:
        """Everything that would make a build or a script wrong, as sentences."""
        found = []
        seq = self.sequence()
        for b in {b for b in seq if seq.count(b) > 1}:
            found.append(f"{b} is listed twice in order/backup")
        for b in seq:
            if b not in self.data or not isinstance(self.data[b], dict):
                found.append(f"{b} is in order/backup but has no [{b}] table")
                continue
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", b):
                found.append(f"{b}: a beat ID must be a valid Python class name")
            beat = self.data[b]
            if beat.get("act") not in self.acts:
                found.append(f"{b}: act {beat.get('act')!r} is not in [acts]")
            if beat.get("kind", "beat") not in KINDS:
                found.append(f"{b}: kind must be one of {sorted(KINDS)}")
            if not beat.get("frame"):
                found.append(f"{b}: no frames")
            for i, f in enumerate(beat.get("frame", []), 1):
                for k in FRAME_FIELDS:
                    if not f.get(k):
                        found.append(f"{b}.{i}: missing {k}")
                for label, region in boxes(f):
                    if region not in REGIONS:
                        found.append(f"{b}.{i}: box {label!r} has region {region!r}; use one of {sorted(REGIONS)}")
        return found
