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

## Notes from an external reviewer

A reviewer (an advisor, a colleague) usually gives a handful of general remarks rather than
slide-by-slide notes. Before acting:

1. **List them**, each in one line.
2. **Triage each one**: accept, accept in part, needs clarification, or disagree, with the reason.
   Do not accept everything: a reviewer's fix ("add the full citation") can work against another of
   their remarks ("too much text").
3. **Find shared causes.** Several remarks often come from one root ("too much content" explains
   speaking fast, moving fast and seeming confusing). Fix the root, then check which remarks remain.
4. **Order them**: the root causes first, then by earliest stage; quick independent fixes (a bug)
   can go at once.
5. **Collect the questions to send back** for remarks that cannot be acted on without more detail
   ("slide 6 is confusing": which part?).
6. Work through them one at a time with the author, each through the loop below.

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
