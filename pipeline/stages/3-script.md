# Stage 3: Script

Write the spoken text, beat by beat. Read `guides/talk-scripts.md` first.

## Input

The approved outline and digest.

## Steps

1. Write `3-script/script.md`: one section per beat, in the outline's order, in the format of
   `templates/3-script/script.md` (bold spine line, then support).
2. **Expand, then compress.** While the story settles, add freely and report the running time in
   one line. Compress only when the author asks, and then cut whole beats with them, not words.
3. Run `uv run mpp script` for word counts and times per beat and act at the pace class.
   From stage 4 on, `uv run mpp script --pdf` also writes the script PDF.
4. **Read-aloud, one act at a time.** The author reads the act aloud and sends back one of:
   - notes;
   - a recording;
   - a transcript.

   Apply what it shows (rules in `guides/talk-scripts.md`) and record the act's measured time in
   `3-script/readaloud.md`.

## Checkpoint

`script.md` per act, then the whole script with `readaloud.md`.

## Done when

Every act has been read aloud and the total fits the slot. Tag `global/script-1`.

## After this stage

In stage 4 the script's text moves into `storyboard.toml`, and `mpp script --from-storyboard`
replaces the hand-written `script.md` with a generated one. From then on `script.md` is generated
by `mpp script` and must not be edited by hand; script notes are fixed in the storyboard. Until
then `mpp script` only times the hand-written file and never overwrites it.
