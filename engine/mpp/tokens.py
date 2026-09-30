"""The design tokens as Python: colour, type, layout, motion, read from the talk's tokens.toml.

Values are data (defaults/tokens.toml, then 5-design/tokens.toml, then the variant's), so a talk
changes its look without touching code. Every key becomes a module constant in upper case:
`[colors] ours` is `tk.OURS`, `[layout] margin_x` is `tk.MARGIN_X`, `[motion] step` is `tk.STEP`;
`tk.CAP` holds the type sizes. Sizes are cap heights in pixels at 1080p, the unit a reader in the
back row actually sees.
"""

import manimpango
from manim import MathTex, Mobject, Tex, Text, TexTemplate, config

from .project import ENGINE, Talk

TALK = Talk.current()
RAW = TALK.tokens()

COLORS: dict = RAW["colors"]
CAP: dict = RAW["type"]["cap"]
FACE: str = RAW["type"]["face"]
globals().update({k.upper(): v for k, v in COLORS.items()})
globals().update({k.upper(): v for k, v in RAW["layout"].items()})
globals().update({k.upper(): v for k, v in RAW["motion"].items()})

for folder in [ENGINE.parent.parent / "vendor" / "fonts", *TALK.dirs("5-design/fonts")]:
    for f in sorted(folder.glob("*.[ot]tf")):
        manimpango.register_font(str(f))

PX = config.frame_height / 1080  # scene units per pixel at 1080p

TEX = TexTemplate(
    documentclass=r"\documentclass[preview]{standalone}",
    preamble="\n".join(
        [
            r"\usepackage[english]{babel}",
            r"\usepackage[T1]{fontenc}",
            *[rf"\usepackage{{{p}}}" for p in RAW["type"]["tex_packages"]],
        ]
    ),
)

_TEXT_CAP_PER_SIZE = Text("H", font=FACE, font_size=100).height / 100
_math_cap = None


def words(s: str, role: str = "label", color=None, weight: str = "NORMAL", slant: str = "NORMAL") -> Text:
    """Text at a type role, sized by cap height so every role reads the same on every slide."""
    size = CAP[role] * PX / _TEXT_CAP_PER_SIZE
    return Text(s, font=FACE, font_size=size, color=color or COLORS["ink"], weight=weight, slant=slant)


def math(*tex: str, role: str = "label", color=None, **kw) -> MathTex:
    """Math at the same cap height as the words around it. Several pieces give several submobjects,
    so one term can carry its role colour."""
    global _math_cap
    if _math_cap is None:  # measured on first use: a talk without math never needs LaTeX
        _math_cap = MathTex(r"\mathrm{H}", tex_template=TEX, font_size=100).height / 100
    return MathTex(*tex, tex_template=TEX, font_size=CAP[role] * PX / _math_cap, color=color or COLORS["ink"], **kw)


def apply_style() -> None:
    config.background_color = COLORS["ground"]
    Mobject.set_default(color=COLORS["ink"])
    for cls in (Tex, MathTex):
        cls.set_default(color=COLORS["ink"], tex_template=TEX)


def px(x: float, y: float):
    """A point given in 1080p pixels from the top-left corner, in scene coordinates."""
    return [(x - 960) * PX, (540 - y) * PX, 0]
