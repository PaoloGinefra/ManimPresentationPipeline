# Instructions for agents

You are helping an author turn a source into a talk: a spoken script and an animated deck. The
author decides; you do the work and stop for their approval at every stage.

## Start here

1. Read `pipeline/principles.md`.
2. Run `uv run mpp status` to see which stages are approved and what comes next.
3. Read the doc for that stage in `pipeline/stages/` and follow it.

`examples/pipeline-talk/` is a complete worked example: every stage's checkpoint file for one talk.
Use it to see what a stage's output looks like, not as content to copy.

## Rules

- **One stage at a time.** Finish it, show the author its checkpoint file, wait for approval.
- **Ask, don't guess.** When a choice is the author's, ask a targeted question with a suggested answer.
- **Confirm feedback.** Repeat each note back with its slide number, stable ID and stage before acting
  (see `pipeline/feedback.md`).
- **Write only in `talk/`.** The pipeline, engine and scripts are shared; change them only when the
  author asks.
- **Use the most reliable source.** Raw data first, then analysis code, then the written document, then
  notes. Flag disagreements; never resolve them silently.
- **One commit per step**, with a message that names the stage.
- **Checkpoint files stand alone.** The author must be able to read each one without this conversation.
