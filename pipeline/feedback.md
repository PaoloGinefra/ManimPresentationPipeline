# Feedback

How author and reviewer notes turn into changes, at any stage.

## Slide numbers and stable IDs

- Slides show plain numbers (1, 2, 3), one per click. Backup slides continue after the last one.
- Internally every frame has a stable ID: `B3.2` is beat 3, frame 2.
- Beat IDs never change. Frame IDs are positions inside a beat, so splitting or merging a frame
  moves the later frames of that beat.
- Draft slides show their build commit in a corner. The numbering is a function of the
  storyboard, so the conversion table (number, ID, headline) for any draft is recomputed from the
  storyboard at that commit. Always translate a note through the build the author actually saw,
  not the current one.

## The loop

1. The author gives notes, by slide number where there is a deck.
2. Translate each number to its stable ID: `uv run mpp numbers --at <commit on the draft>`.
3. Repeat each note back in one line, with its stage:

   > slide 7 (B3.2), script: say "halves", not "reduces by 48%".

   The stages are: brief, digest, outline, script, visual, design, build.
4. The author confirms or corrects, including the stage.
5. Fix each note at its stage (below). Then regenerate everything after that stage.
6. Show only the changed pieces for re-approval: `mpp preview --changed` for frames, a diff for
   text.
7. Log it (below).

## Choosing the stage

A note belongs to the **earliest** stage it changes. You propose the stage; the author confirms.

| The note changes | Stage |
|---|---|
| audience, slot, pace, what to hold back | brief |
| a fact, a number, its source | digest |
| order, what is in or out, a peak, the thread | outline |
| spoken words | script |
| what is on screen, when it appears, a click | visual |
| a colour, a font, how an object looks everywhere | design |
| one frame's layout, timing or animation | build |

Never patch a note downstream. A wrong number fixed in a scene stays wrong in the script.

## After a fix

- A fix at stage N marks every later stage's files as possibly stale. Regenerate what is
  generated (script, deck); check by hand what is written (skeleton, greybox).
- A fix in `talk/global/` lists every variant that uses the changed file. Each one is rebuilt and
  its changed pieces re-approved (`variants.md`).
- If a fix changes the time, report the new total at the pace class.

## The review log

`7-review/log.md`, one row per note:

| # | date | build | slide | ID | note | stage | fix | commit | status |
|---|---|---|---|---|---|---|---|---|---|

`status` is `open`, `done` or `declined` (with a reason). The talk is not released while a note is
open.

```bash
uv run mpp review add 7 "say halves, not reduces by 48%" --stage script --build <commit on the draft>
uv run mpp review list --open
uv run mpp review done 1 "reworded in the storyboard"      # records HEAD as the fix's commit
uv run mpp review decline 2 "kept: the number is the point"
```

`review add` turns the slide number into its stable ID through the storyboard at `--build`.
