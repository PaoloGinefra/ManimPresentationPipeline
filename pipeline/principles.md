---
name: mpp-pipeline
description: How to run manim-presentation-pipeline, the staged process that turns a source (paper, report, thesis, project) into a spoken script and an animated manim deck with author approval at every stage. Covers the principles, the stages and their checkpoint files, pace classes, and where each rule lives. Use whenever working inside a manim-presentation-pipeline repository, starting or resuming a talk, or acting on author feedback on one.
---

# The pipeline

Turn a source into a spoken talk and an animated deck, through fixed stages. Agents do the work;
the author steers with targeted feedback.

## Principles

1. **The author decides.** Every stage ends with something short for the author to approve.
2. **Stop and ask.** When a choice is the author's, ask a targeted question with a suggested
   answer instead of guessing.
3. **Check cheaply.** Story on a one-page outline, words by reading aloud, visuals on rough boxes,
   fixes on stills. Render only when needed.
4. **Confirm feedback.** Repeat each note back ("slide 7 (B3.2), script: change X") before acting.
5. **One source file.** From stage 4 on, the storyboard holds every slide's text and narration;
   the script and the deck are generated from it.
6. **Stay true to the source.** Every claim and number comes from the most reliable source
   available. The source's own figures and terms come first.
7. **Written to be heard.** Short sentences, one idea per slide. Pace fixed up front. Cut time by
   removing whole beats.
8. **Self-contained results.** Script, deck and design system each stand on their own.
9. **Reproducible.** Everything in git, built with one command, offline, checked automatically.
10. **Reusable engine.** Only content and look change between talks.

## Stages

Each stage writes standalone checkpoint files into its folder under `talk/global/` (or a
variant, see `variants.md`), stops for the author, and is tagged when approved.

| # | Stage | Folder | Checkpoint files | Doc |
|---|---|---|---|---|
| 0 | Brief | `0-brief/` | `brief.md`, `talk.toml` | `stages/0-brief.md` |
| 1 | Digest | `1-digest/` | `digest.md` | `stages/1-digest.md` |
| 2 | Outline | `2-outline/` | `options.md`, then `outline.md` | `stages/2-outline.md` |
| 3 | Script | `3-script/` | `script.md`, `readaloud.md` | `stages/3-script.md` |
| 4 | Visual | `4-visual/` | `options.md`, then `skeleton.md`, `storyboard.toml`, `greybox.html` | `stages/4-visual.md` |
| 5 | Design system | `5-design/` | `design.md`, `tokens.toml`, specimen | `stages/5-design.md` |
| 6 | Build | `6-build/` | beat scenes; draft deck and stills | `stages/6-build.md` |
| 7 | Rehearsal (optional) | `7-review/` | `log.md`, the plan | `stages/7-rehearsal.md` |
| 8 | Final | `releases/` (outside git) | the release | `stages/8-final.md` |

Blank versions of every checkpoint file are in `templates/`, in the same folder layout.

## Pace classes

The brief fixes one. All timing uses it.

| Class | Words per minute |
|---|---|
| slow | 120 |
| normal | 135 |
| fast | 150 |

## Commands: `uv run mpp <command>`

Every command takes `-v NAME` for a variant; without it, the main talk (`global`).

| Command | Does |
|---|---|
| `setup` | install what can be installed; nothing is fetched at build time |
| `doctor` | check Python, cairo, pango, LaTeX, fonts, reveal.js |
| `status` | each stage: approved, changed since, or not started; what is next |
| `approve <stage>` | tag a stage as approved (refused if uncommitted or unchanged) |
| `new-variant <name>` | create a variant folder |
| `numbers [--at COMMIT]` | the conversion table: slide number, stable ID, headline |
| `script [--pdf]` | time the script at the pace class; regenerate it from the storyboard; the PDF |
| `greybox` | the greybox page, generated from the storyboard |
| `specimen` | the design-system specimen page |
| `build [BEATS] [--act N] [--final]` | render a draft (720p24) or the final (1080p30) deck |
| `check [--final]` | storyboard problems, layout lint, seams |
| `preview <7, 7-12, B3.2, B3> / --changed` | stills of those slides as one standalone page |
| `review add / list / done / decline` | the review log |
| `release` | final checks, full render, copy to `releases/`, tag |

`uv run mpp <command> -h` gives each command's options.

## Where the other rules live

| Topic | File |
|---|---|
| Notes from the author, backtracking, the review log | `feedback.md` |
| Variants of one talk (shorter cut, other audience) | `variants.md` |
| Commits, tags, releases | `versioning.md` |
| Writing spoken text | `guides/talk-scripts.md` |
| Visuals, storyboards, animation | `guides/talk-storyboards.md` |

## Working rules

- One stage at a time. Do not start the next stage before the author approves the current one.
- When the author gives a note that belongs to an earlier stage, go back to that stage
  (`feedback.md`). Never patch it downstream.
- Stable IDs: beats are `B1`, `B2`, ...; frames are `B3.2` (beat 3, frame 2). A beat ID is never
  reused or renumbered; a new beat takes the next free number, and the order lives in the
  storyboard's `order` list. Slides show plain numbers; see `feedback.md` for the conversion.
- One commit per step, named after the stage (`versioning.md`).
