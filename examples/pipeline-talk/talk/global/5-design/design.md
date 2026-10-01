# Design system

This starts as the engine's default house style. Every value here is also in the tokens: the
defaults in `engine/mpp/defaults/tokens.toml`, and this talk's changes in `tokens.toml` beside this
file. The engine reads the tokens; people read this file. Change both together.

## Palette

Every colour means one thing for the whole talk. Everything that is not a role is neutral;
emphasis is made by dimming the rest, never by a new hue.

| role | colour | used for |
|---|---|---|
| ink | `#1B1F2A` | text, and anything that simply is |
| muted | `#5B6170` | secondary text, captions, the slide number |
| structure | `#9AA0AA` | axes, frames, rules |
| faint | `#D5D8DD` | grid lines, inactive items |
| ground | `#FFFFFF` | the background |
| ours | `#0072B2` | the thing the talk is about |
| baseline | `#E69F00` | what it is compared with (`baseline_text` `#8F5F00` for its text) |
| highlight | `#CC79A7` | a term being pointed at |
| failure | `#D55E00` | what breaks |

Checked for: colour-blind safety (the roles are the Okabe-Ito set), projector contrast (text
colours are at least 4.5:1 on the ground).

## Screen regions

In pixels at 1080p. Headline top left, from (96, 64), at most 1500 wide and two lines. Slide
number top right. Content between 220 and 950. A progress spine, when used, bottom left; the
draft label bottom right. Ours sits left of the baseline in every comparison.

## Type

Source Sans 3, sized by cap height so every role reads the same on every slide.

| use | font | size |
|---|---|---|
| title | Source Sans 3 Semibold | 64 px |
| headline | Source Sans 3 Semibold | 40 px |
| label | Source Sans 3 | 28 px |
| note (the smallest anything read aloud may be) | Source Sans 3 | 23 px |
| slide number | Source Sans 3 | 24 px |

Mathematics is set in LaTeX at the same cap height as the words around it.

## Transitions

| weight | transition | duration |
|---|---|---|
| step | fade, or a small move | 0.8 s |
| move | pan: the old picture leaves left, the new one arrives from the right | 1.1 s |
| act break | zoom | 2.4 s |
| same object changing | transform | 0.8 s |
| attention cue | dim the rest to 25% | 0.4 s |

## Cast

Drawn once in `6-build/components/pipeline.py`; the specimen shows each.

| object | how it is drawn |
|---|---|
| row of stages | nine rounded boxes spanning margin to margin along the bottom (centre line at 930 px); labels centred, on one baseline; done: ink outline and an ink tick badge on the corner; in focus: ours outline, a 12% ours fill; not yet: structure outline, muted label; rehearsal dashed, because it is optional |
| card | one 16:9 card, 1100 by 619 px, structure outline; its content starts at a 56 px left padding in every form, so changing form never moves content sideways; the followed sentence is always in ours; in its slide forms the card is the slide |
| card, set aside | the card at 55%, on the left margin, its top level with the capitals of the check list's title |
| check list | "The author checks" in muted label size, then one line per check with a box that ticks; every line on one left edge (820 px) |
| note | a rounded card with a highlight outline and a 12% highlight fill |
| ladder | four rungs on one left edge, each longer than the one below, no numbers; labels right-aligned to one edge, each on its rung's line |

## Alignment

Every left edge sits on the 96 px margin or on a column of the layout (the card's padding, the check
list at 820 px). Texts that share a line share a baseline (`tk.set_baseline`), never a centre: a word
with a descender would otherwise sit higher. `mpp check` reports near-misses of a few pixels.

The talk uses the default house style unchanged: ours for the thread and the stage in focus,
highlight for the note, structure for the scaffolding. No new colour.
