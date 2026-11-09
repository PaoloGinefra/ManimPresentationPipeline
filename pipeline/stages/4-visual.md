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
   frame has its headline, the trigger words, its narration (moved from `script.md`), its rough
   layout (`boxes`) and a note for the builder. Format in `templates/4-visual/storyboard.toml`.
3. **Greybox**: run `uv run mpp greybox`. It writes `greybox.html`, one standalone page showing
   every frame as labelled grey boxes, with its plain slide number, its stable ID, its real
   headline and its narration underneath. It is generated from the storyboard, so it never
   drifts from it; fix the storyboard, not the page.
4. Run `uv run mpp script --from-storyboard`: `3-script/script.md` is now generated from the
   storyboard. Check the times still fit, and diff it against the approved script: the words
   should not have changed on the way.

## Results frames

- **One claim per frame.** A frame that shows every setting of every experiment shows none.
  The full table is a backup.
- **Show the measurement before the number.** A small diagram of what is measured (what goes in,
  what is compared) precedes the value; an unexplained score is not evidence for a lay audience.
- **Choose the form from the claim**, not by habit: a count out of a whole as a pictogram, a trend as
  a curve, a ratio as one large number, a comparison of two as two numbers side by side. Bar charts
  at full-slide size give every value equal weight and are rarely the best choice.
- **Name the environments before their results**, with a short look at each (a looping recording
  is ideal). A number about a world nobody has seen does not land.

## Preview before building

Whenever a frame has two or more credible designs, render each as a single still with the real
assets and real numbers, side by side, and let the author choose. Do not build a beat whose look
is still in question: a still costs seconds, a rebuild of the following beats costs far more.

## Checkpoint

`options.md` (4a), then the greybox (4b), with the skeleton and storyboard beside it.

## Done when

The author approves the greybox. Tag `global/visual-1`.
