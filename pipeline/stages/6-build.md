# Stage 6: Build

Turn the storyboard into the animated deck, one act at a time.

## Input

The approved storyboard and design system.

## Where things go

- `6-build/beats/<ID>.py`: one scene per beat, a subclass of `mpp.beat.Beat` whose class name is
  the beat's stable ID. A file may hold several beats; one per file keeps variants simple, since a
  variant overrides a file whole.
- `6-build/components/`: recurring objects used by more than one beat, imported as
  `from components.<name> import ...`. No `__init__.py`: the folder is a namespace package, so a
  variant's `components/` file of the same name wins.
- Generic pieces (headline, slide number, charts, zooms, tokens) come from the engine
  (`from mpp import charts, motion`, `from mpp import tokens as tk`). Do not copy them into the talk.
- A talk's own furniture (a progress gauge, say) goes in a subclass of `mpp.beat.Beat` in
  `components/`: return it from `furniture()`, and put any state the next beat needs in `self.carry`
  (the next beat reads it as `self.handed`).
- Code from outside the repository (a paper's figure library) is imported through
  `[build] python_path` in `talk.toml`, never by copying it in.
- Give a recurring object a role (`obj.role = "timeline"`) so the next beat can pick it up with
  `self.carried("timeline")`.
- Renders go to `build/render/<variant>/<draft or final>/`, or under `MPP_OUT` when it is set
  (a local disk, a scratch space). Never into git.

## Steps, per act

1. Build the act's beats from the storyboard frames. Text comes from the storyboard, look from
   `tokens.toml`. No literal colours, sizes or headlines in scene code.
2. Render a draft: `uv run mpp build --act N`. Drafts are low quality (720p, 24 fps), labelled as
   drafts, and show the build commit small in a corner.
3. Run `uv run mpp check`: storyboard problems, layout lint (text over text, text off the frame,
   texts whose baselines or left edges miss each other by a few pixels), and seams between slides.
   Set labels that share a line with `tk.set_baseline`, not by centring them: centring aligns ink,
   and a word with a descender then sits higher than one without. A beat whose clicks differ from its storyboard frames fails to build.
   Fix every failure before showing anything. A finding the author has looked at and accepted goes
   in `talk.toml` under `[check] accept`, exactly as reported, with the reason in a comment.
4. Show the author stills: `uv run mpp preview 7-12` (slide numbers, ranges, IDs like `B3.2`, or
   whole beats like `B3`). It writes `build/<variant>/preview.html`, one still per slide.
5. Apply notes (`feedback.md`), then show only what changed: `uv run mpp preview --changed`.
6. When the stills are approved, the author clicks through the act's draft deck.

Do not edit scene code while a build is running; beats hand state to each other and a mixed
build is inconsistent.

## Checkpoint

Per act: the stills, then the draft deck.

## Done when

Every act is approved in a click-through. Tag `global/build-1`.
