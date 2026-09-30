# Stage 4: Visual

Decide what the audience sees at every click, before any styling or animation. Read
`guides/talk-storyboards.md` first.

## Input

The approved script, outline and digest (for reusable figures).

## 4a: Brainstorm

1. Design the peaks first: one key image each, and which earlier beats plant its parts.
2. For each beat, give 2 or 3 visual options, one line each, with a suggested pick. Mark each
   option's animation level:
   - **static**: a still picture, built up by clicks;
   - **motion**: objects move or transform;
   - **scene**: a full animated sequence.

   Prefer the source's own figures where they fit.
3. Write `4-visual/options.md`. The author picks per beat.

## 4b: Consolidate

1. **Skeleton** (`skeleton.md`): the cast of recurring objects, the canvas, colour roles, the
   interaction policy, and one row per beat.
2. **Storyboard** (`storyboard.toml`): every beat split into frames, one frame per click. Each
   frame has its headline, the trigger words, its narration (moved from `script.md`) and a note
   for the builder. Format in `templates/4-visual/storyboard.toml`.
3. **Greybox** (`greybox.html`): one standalone page showing every frame as rough boxes, with its
   plain slide number, its stable ID, its real headline and its narration underneath. No colours
   beyond grey, no styling. The author must be able to open it with no tools.
4. Run `uv run mpp script` to regenerate `3-script/script.md` from the storyboard, and check the
   times still fit.

## Checkpoint

`options.md` (4a), then the greybox (4b), with the skeleton and storyboard beside it.

## Done when

The author approves the greybox. Tag `global/visual-1`.
