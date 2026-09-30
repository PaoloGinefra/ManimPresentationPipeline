from manim import FadeIn

from mpp import chrome
from mpp.beat import TALK, Beat


class B0(Beat):
    def construct(self):
        cfg = TALK.config()
        card = chrome.title_card(cfg.get("title") or self.frames[0]["head"], cfg.get("speaker", ""), cfg.get("date", ""))
        self.click(FadeIn(card), headline=False)
