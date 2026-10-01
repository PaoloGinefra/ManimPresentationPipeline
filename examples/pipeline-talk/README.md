# Example: the pipeline run on itself

A six-minute talk about this repository, made with this repository: every stage's checkpoint
file is here, in the same layout as `talk/`, with its git history and approval tags. Read it as a
worked example of what each stage produces.

| Stage | Read |
|---|---|
| 0 Brief | `talk/global/0-brief/brief.md`, `talk.toml` |
| 1 Digest | `talk/global/1-digest/digest.md`: every claim with its source in this repository |
| 2 Outline | `talk/global/2-outline/options.md`, then `outline.md` |
| 3 Script | `talk/global/3-script/script.md` (generated since stage 4), `readaloud.md` |
| 4 Visual | `talk/global/4-visual/options.md`, `skeleton.md`, `storyboard.toml`, `greybox.html` |
| 5 Design | `talk/global/5-design/design.md`, `tokens.toml`, `specimen.py` |
| 6 Build | `talk/global/6-build/beats/`, `components/pipeline.py` |
| Review | `talk/global/7-review/log.md`: four notes on the first draft, one of them sent back to the visual stage |

## Build it

From this folder:

```bash
uv run --project ../.. mpp build           # draft: build/global/draft.html
uv run --project ../.. mpp script --pdf    # the script: build/global/script.pdf
uv run --project ../.. mpp greybox         # the greybox page
```

Its tags carry its path: `examples/pipeline-talk/global/brief-1` and so on, and
`examples/pipeline-talk/global/v1` for the release.

## What is not real about it

- **There was no author.** The agent that built the pipeline stood in for the author at every
  checkpoint: it made the picks in the option files and created the approval tags. Each tag's
  message says so. A real run stops at every one of those points.
- **No one has read the script aloud.** Its time is a word count at normal pace
  (`readaloud.md`).
- **The review notes were the agent's own**, from looking at the first draft's stills. They are
  real defects, fixed the way the pipeline prescribes, but no second person made them.
- **The talk-within-the-talk is invented.** "The slowest waits halve once the cache is warm" is
  the guides' running example, not a measured result, and its bars carry no numbers.
