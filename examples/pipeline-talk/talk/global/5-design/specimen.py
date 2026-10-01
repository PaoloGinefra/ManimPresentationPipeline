"""This talk's half of the specimen: its cast, in the house style. Rendered by `mpp specimen`."""

from components.pipeline import aside, card, card_centre, checks, ladder, note, row
from manim import DOWN, RIGHT, Scene, VGroup

from mpp import chrome
from mpp import tokens as tk

tk.apply_style()


class StageExplained(Scene):
    """A stage beat's first click: the cache talk's checkpoint, centred, above the row."""

    def construct(self):
        self.add(chrome.headline("The digest lists what the talk could say, with sources."), chrome.slide_number(8))
        self.add(card_centre("digest"), row(done=1, lit=1))


class StageChecked(Scene):
    """A stage beat's second click: the card aside, the author's checks, the stage ticked."""

    def construct(self):
        self.add(chrome.headline("The author sorts every item and answers every gap."), chrome.slide_number(9))
        lst = checks(["must, could or leave out", "every gap answered"])
        for line in lst[1]:
            line[2].set_stroke(opacity=1)
        self.add(aside(card_centre("digest")), lst, row(done=2))


class Forms(Scene):
    """Every form of the card, side by side, then the note and the ladder."""

    def construct(self):
        names = ["title", "brief", "digest", "options", "outline-focus", "script", "storyboard", "greybox",
                 "render", "specimen", "release"]
        forms = VGroup(*[card(f).scale(0.27) for f in names]).arrange_in_grid(cols=4, buff=0.18)
        forms.move_to(tk.px(960, 400))
        extras = VGroup(note(), ladder().scale(0.45)).arrange(RIGHT, buff=0.8)
        self.add(forms, extras.next_to(forms, DOWN, buff=0.25))
