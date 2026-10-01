"""This talk's half of the specimen: its cast, in the house style. Rendered by `mpp specimen`."""

from components.pipeline import card, card_at, ladder, note, row
from manim import DOWN, RIGHT, Scene, VGroup

from mpp import chrome
from mpp import tokens as tk

tk.apply_style()


class Cast(Scene):
    """A frame of B4 as it will look: headline, the card above its stage, the row."""

    def construct(self):
        self.add(chrome.headline("In the storyboard, it becomes a frame."), chrome.slide_number(12))
        self.add(card_at("storyboard", 4), row(done=4, lit=4))


class Forms(Scene):
    """Every form of the sentence card, side by side, and the note and the ladder."""

    def construct(self):
        forms = VGroup(*[card(f).scale(0.36) for f in ("source", "digest", "outline", "script", "storyboard", "greybox", "render")])
        forms.arrange_in_grid(rows=2, buff=0.25).move_to(tk.px(960, 380))
        extras = VGroup(note(), ladder().scale(0.5)).arrange(RIGHT, buff=1).move_to(tk.px(960, 880))
        self.add(forms, extras.next_to(forms, DOWN, buff=0.4))
