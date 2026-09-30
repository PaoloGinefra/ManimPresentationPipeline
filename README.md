# manim-presentation-pipeline

From a source (paper, report, thesis, project) to a spoken script and an animated deck, through
fixed stages. Agents do the work; you steer with short, targeted feedback at every stage.

What you get:

- **Script:** a PDF with click cues.
- **Deck:** an animated offline HTML presentation with speaker notes, plus a static PDF.
- **Design system:** a document, tokens and a specimen page.
- **Backup slides** for questions.

Everything rebuilds with one command. The deck is rendered with
[manim](https://www.manim.community/) and [manim-slides](https://github.com/jeertmans/manim-slides).

## Quick start

```bash
git clone <this repo> my-talk && cd my-talk
uv sync
uv run mpp doctor          # checks Python, cairo, pango, LaTeX, fonts, reveal.js
```

1. Put your source files in `talk/source/`.
2. Point your agent at `AGENTS.md`. It runs the stages and stops for you at each one.

## Where things are

| Path | What |
|---|---|
| `AGENTS.md` | entry point for any agent |
| `CLAUDE.md` | Claude Code notes: which docs to install as skills |
| `DESIGN.md` | the design of the pipeline |
| `pipeline/` | the process: principles, stages, feedback, variants, versioning, guides, templates |
| `engine/` | the Python package: deck engine and the `mpp` CLI |
| `talk/` | your presentation; the only folder you edit |
| `scripts/` | setup and environment checks |
| `vendor/` | fonts and reveal.js, for offline builds |
| `examples/` | the pipeline run on itself: a complete talk about this repository |

Your content lives only under `talk/`, so pipeline updates merge cleanly.

## Licence

MIT, see `LICENSE`. The vendored font keeps its own OFL licence. Your talk is yours.
