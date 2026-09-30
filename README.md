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
scripts/setup.sh           # cairo and pango, the Python environment, then `mpp doctor`
uv run mpp build           # the placeholder talk: build/global/draft.html
```

1. Put your source files in `talk/source/`.
2. Point your agent at `AGENTS.md`. It runs the stages and stops for you at each one.

## Setup

Everything runs through [uv](https://docs.astral.sh/uv/), which installs Python 3.12 and every
Python package from the lockfile. Three things come from the system:

| What | Why | macOS | Debian, Ubuntu | Cluster without root |
|---|---|---|---|---|
| cairo, pango, pkg-config | manim compiles against them | `brew install cairo pango pkg-config` | `sudo apt install libcairo2-dev libpango1.0-dev pkg-config python3-dev` | `scripts/bootstrap-native.sh` (dnf systems) |
| LaTeX with dvisvgm | mathematics on slides only | BasicTeX: `brew install --cask basictex`, then `sudo tlmgr install standalone preview dvisvgm cm-super babel-english` | `sudo apt install texlive-latex-extra texlive-fonts-recommended dvisvgm cm-super` | the TeX Live user installer into `~/texlive`, its `bin/` on `PATH` |
| git | approvals and releases are git tags | preinstalled | `sudo apt install git` | preinstalled |

`scripts/setup.sh` does what it can for your machine, prints the command where root is needed,
runs `uv sync`, and ends with `uv run mpp doctor`, which checks every piece and renders one still.
Run `uv run mpp doctor` again whenever something looks wrong.

Nothing is downloaded at build time: the font and reveal.js are in `vendor/`, and the exported deck
is one offline HTML file. Once `uv sync` has run, `uv sync --offline` rebuilds the environment from
uv's cache without a network.

On a cluster, renders can be large: set `MPP_OUT` to a local or scratch disk to keep them there.
Builds use every core the job was given.

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
