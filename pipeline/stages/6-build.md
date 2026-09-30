# Stage 6: Build

Turn the storyboard into the animated deck, one act at a time.

## Input

The approved storyboard and design system.

## Where things go

- `6-build/beats/<ID>.py`: one scene per beat, named by its stable ID.
- `6-build/components/`: recurring objects used by more than one beat.
- Generic pieces (headline, slide number, charts, camera moves) come from the engine. Do not
  copy them into the talk.
- Renders go to the render folder (configurable, persistent), never into git.

## Steps, per act

1. Build the act's beats from the storyboard frames. Text comes from the storyboard, look from
   `tokens.toml`. No literal colours, sizes or headlines in scene code.
2. Render a draft: `uv run mpp build --act N`. Drafts are low quality (720p, 24 fps), labelled as
   drafts, and show the build commit small in a corner.
3. Run `uv run mpp check`: frame counts against the storyboard, seams between beats, layout lint.
   Fix every failure before showing anything.
4. Show the author stills: `uv run mpp preview` (a standalone page, one still per frame).
5. Apply notes (`feedback.md`), preview only the changed frames (`mpp preview --changed`).
6. When the stills are approved, the author clicks through the act's draft deck.

Do not edit scene code while a build is running; beats hand state to each other and a mixed
build is inconsistent.

## Checkpoint

Per act: the stills, then the draft deck.

## Done when

Every act is approved in a click-through. Tag `global/build-1`.
