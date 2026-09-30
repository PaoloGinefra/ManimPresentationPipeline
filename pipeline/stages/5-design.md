# Stage 5: Design system

Fix the look once, for every role and object the storyboard uses, and nothing more.

## Input

The approved skeleton and storyboard (colour roles, cast, transition weights), and a house style
if the brief names one.

## House style

A house style is a folder holding `design.md`, `tokens.toml` and any fonts. To start from one,
copy it into `5-design/`, then adjust only what this talk needs. To save this talk's design as a
house style, copy `5-design/` out. The repository ships a default in the template talk.

If the brief names a house style, skip step 1.

## Steps

1. Propose 2 or 3 options, each a palette, a type pairing and a motion feel, shown as a few
   stills of one real frame from the storyboard. The author picks one.
2. Write:
   - `design.md`: the palette with each colour's role, screen regions, type sizes, the
     transition bound to each weight, and how each recurring object is drawn;
   - `tokens.toml`: the same values as data, read by the engine;
   - the specimen: one rendered page showing every token and every recurring object.
3. Check colour-blind safety and projector contrast.

## Checkpoint

The specimen, with `design.md` beside it.

## Done when

The author approves the specimen. Tag `global/design-1`.
