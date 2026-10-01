"""A beat of the talk as a scene: its text comes from the storyboard, its drawing from the components.

A beat's code says only what happens on each click. The furniture every frame shares (the headline,
the slide number, the draft label) and the speaker notes are handled here, from the storyboard, so
editing a sentence never means touching scene code.

    class B1(Beat):
        def construct(self):
            box = Square()
            self.click(FadeIn(box))           # frame B1.1: its headline, number and notes are set here
            self.play(box.animate.shift(UP))  # still frame B1.1
            self.click(...)                   # frame B1.2

Beats hand over: a beat opens on exactly the picture the beat before it (in the storyboard's order)
ended on, so there is no cut between scenes. Each beat saves its last picture to <renders>/handoff/
when it finishes; the next one loads it as `self.inherited`. Render in the talk's order (the build
does), or a beat opens on a stale picture of its predecessor.
"""

import copy
import os
import pickle

from manim import LEFT, RIGHT, UP, AnimationGroup, FadeIn, FadeOut, Group, Mobject, Wait, config
from manim_slides import Slide

from . import chrome, lint
from . import tokens as tk
from .camera import ClippingCamera
from .storyboard import spoken

tk.apply_style()  # before any scene exists: the camera takes its background from config when it is built

TALK = tk.TALK
STORYBOARD = TALK.storyboard()
RENDERS = TALK.renders()
HANDOFF = RENDERS / "handoff"
DRAFT = os.environ.get("MPP_DRAFT", "")  # the build commit on a draft; empty on a final render
ROLL = UP * 0.18  # headlines change by rolling up: the old leaves upward, the new arrives from below


def swap(old, new, shift=ROLL, run_time=None):
    """Replace one text (or any small group) with another: the old rolls out, then the new rolls in.
    Staggered, never crossed: two texts in one place at once read as a smudge."""
    return [
        AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=1, run_time=run_time or tk.STEP)
    ]


class Beat(Slide):
    """One beat: a scene whose clicks are the frames listed under its name in the storyboard."""

    beat_id: str | None = None  # defaults to the class name, which is how the storyboard refers to it

    def __init__(self, *args, **kwargs):
        super().__init__(*args, camera_class=ClippingCamera, output_folder=RENDERS / "slides", **kwargs)

    def setup(self):
        super().setup()
        self.id = self.beat_id or type(self).__name__
        self.text = STORYBOARD.beat(self.id)
        self.frames = self.text["frame"]
        self.first = STORYBOARD.first_number(self.id)
        self.n = 0
        self.head, self.head_text, self.tag = None, None, None
        self.label = chrome.draft_label(DRAFT) if DRAFT else None
        self.inherited = []
        prev = STORYBOARD.previous(self.id)
        if prev and (HANDOFF / f"{prev}.pkl").exists():
            h = pickle.loads((HANDOFF / f"{prev}.pkl").read_bytes())
            self.inherited = h["content"]
            self.add(*self.inherited)
            self.head, self.head_text, self.tag = h["head"], h["head_text"], h["tag"]
            self.add(*[m for m in (self.head, self.tag) if m is not None])
        if self.label is not None:
            self.add(self.label)

    def click(self, *animations, headline: bool = True, pan=None, zoomed_head=None, **play_kwargs):
        """Start the next frame: the presenter's click lands here.

        Closes the previous slide, sets this frame's speaker notes from its narration, shows its number,
        and plays its opening animations together with the headline's change, if the headline changed.
        Each animation keeps its own run time. Further `self.play` calls until the next `click` belong
        to the same frame.

        `pan` (a mobject or a list) is the transition between beats in one act: the old picture leaves
        to the left and `pan` arrives from the right, already composed.

        `zoomed_head` is for a zoom: the old headline belongs to the picture being zoomed, so the caller
        zooms it away with the rest (see `take_head`) and this frame's headline arrives once it has gone.
        """
        if self.n >= len(self.frames):
            raise IndexError(
                f"{self.id} has {len(self.frames)} frames in the storyboard, "
                f"and the scene asks for a frame {self.n + 1}"
            )
        frame = self.frames[self.n]
        if self.n:
            self.settle()
            lint.check(self, f"{self.id}.{self.n}")
        self.n += 1
        self.next_slide(notes=spoken(frame["narration"]))
        if self.tag is not None:
            self.remove(self.tag)
        self.tag = chrome.slide_number(self.first + self.n - 1)
        self.add(self.tag)
        opening, gone = list(animations), []
        if pan is not None:
            gone = self.content()
            for m in gone:
                m.clear_updaters()
            arriving = list(pan) if isinstance(pan, (list, tuple)) else [pan]
            for m in arriving:
                m.shift(RIGHT * config.frame_width)
            opening += [m.animate(run_time=tk.MOVE).shift(LEFT * config.frame_width) for m in gone + arriving]
        if headline and frame["head"] != self.head_text:
            new = chrome.headline(frame["head"])
            if zoomed_head is not None:  # arrives after the old one has zoomed out of the frame
                opening.append(
                    AnimationGroup(Wait(zoomed_head), FadeIn(new, shift=ROLL, run_time=tk.STEP), lag_ratio=1)
                )
            else:
                opening += (
                    swap(self.head, new) if self.head is not None else [FadeIn(new, shift=ROLL, run_time=tk.STEP)]
                )
            self.head, self.head_text = new, frame["head"]
        elif not headline and self.head is not None:
            opening.append(FadeOut(self.head, run_time=tk.STEP))
            self.head, self.head_text = None, None
        # the furniture is drawn over everything, whatever moves: `play` re-adds a moving group that is
        # not itself in the scene on top of everything, which would bury it
        self.add_foreground_mobjects(*self.chrome())
        self.play(*(opening or [Wait(tk.STEP)]), **play_kwargs)
        self.remove(*gone)

    def dim(self, *keep, opacity=None):
        """The attention cue: everything on screen except `keep` fades to `opacity`."""
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        chrome_ids = {id(m) for c in self.chrome() for m in c.get_family()}
        return [
            m.animate.set_opacity(tk.DIM if opacity is None else opacity)
            for m in self.mobjects
            if id(m) not in keep_ids and id(m) not in chrome_ids
        ]

    def settle(self):
        """Write one frame of the finished state. manim writes an animation's frames up to, not including,
        its end, so without this a slide's last frame (its hold, and its PDF page) shows the final
        animation a frame short: a staggered fade leaves its last letters missing."""
        self.wait(1 / config.frame_rate)

    def take_head(self):
        """Hand the headline over to a zoom: it stops being furniture and becomes part of the picture, which
        a zoom carries off the screen. Returns it (or None)."""
        head = self.head
        self.head, self.head_text = None, None
        return head

    def chrome(self):
        """The furniture on screen now: headline, number, draft label."""
        return [c for c in (self.head, self.tag, self.label) if c is not None]

    def content(self):
        """What is on screen besides the furniture, as the objects a beat made.

        Some animations (Succession, an AnimationGroup) leave the scene holding a role-less `Group`
        around the objects they moved, and empty `Mobject` placeholders. Those are looked through, so a
        role given to an object survives into the handoff."""
        keep = {id(c) for c in self.chrome()}
        out = []
        for m in self.mobjects:
            if id(m) in keep:
                continue
            if type(m) in (Group, Mobject) and getattr(m, "role", None) is None:
                out += [s for s in m.submobjects if id(s) not in keep]
            else:
                out.append(m)
        return out

    def crossfade(self, *new, keep=(), run_time=None):
        """Change the picture in one move: what is on screen fades out while `new` fades in just behind it,
        so the screen is never empty between two pictures. Anything in `keep` stays, to be moved by the
        caller: continuity is the better transition whenever an object survives into the next picture."""
        kept = {id(m) for k in keep for m in k.get_family()}
        old = [m for m in self.content() if not any(id(f) in kept for f in m.get_family())]
        for m in old:
            m.clear_updaters()
        parts = [AnimationGroup(*[FadeOut(m) for m in old])] if old else []
        parts += [AnimationGroup(*[FadeIn(m) for m in new])] if new else []
        return AnimationGroup(*parts, lag_ratio=0.4, run_time=run_time or tk.MOVE)

    def carried(self, role):
        """The object with this `role` in the picture the previous beat handed over, for moving it on.
        Give an object a role (`obj.role = "timeline"`) in the beat that makes it."""
        return next((m for m in self.inherited if getattr(m, "role", None) == role), None)

    def wipe(self, *also, keep=(), run_time=None):
        """Fade out everything but the furniture and `keep`: the usual start of a frame that changes the
        picture. Quick, so the new picture can follow it in a second `play` instead of crossing it."""
        run_time = run_time or tk.FOCUS
        kept = {id(m) for k in keep for m in k.get_family()}
        for m in self.mobjects:
            m.clear_updaters()
        gone = [m for m in self.content() if not any(id(f) in kept for f in m.get_family())]
        return [FadeOut(m, run_time=run_time) for m in [*gone, *also]]

    def tear_down(self):
        """The scene must use exactly the frames the storyboard lists, so text and scene cannot drift.
        Then the last picture is handed to the next beat."""
        if self.n != len(self.frames):
            raise AssertionError(
                f"{self.id}: the storyboard lists {len(self.frames)} frames, the scene played {self.n}"
            )
        self.settle()
        lint.check(self, f"{self.id}.{self.n}")
        HANDOFF.mkdir(parents=True, exist_ok=True)
        content = [copy.deepcopy(m) for m in self.content()]
        for m in content:
            m.clear_updaters()
        tmp = (
            HANDOFF / f".{self.id}.pkl.{os.getpid()}"
        )  # written whole, then renamed: a parallel reader never sees half
        tmp.write_bytes(
            pickle.dumps({"content": content, "head": self.head, "head_text": self.head_text, "tag": self.tag})
        )
        tmp.replace(HANDOFF / f"{self.id}.pkl")
        super().tear_down()
