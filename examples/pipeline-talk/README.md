# Example: the pipeline run on itself

An eight-minute talk about this repository, made with this repository: every stage's checkpoint
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
| Review | `talk/global/7-review/log.md`: seven notes; one restructured the talk and went back to the outline, one changed the slot in the brief, one on alignment went back to the design |

## The result

The release, tracked in git so it can be read without building anything:

| File | What |
|---|---|
| [`talk.html`](releases/global/v2/talk.html) | the animated deck: one offline file, speaker notes included (download and open it) |
| [`talk.pdf`](releases/global/v2/talk.pdf) | the static deck, one page per click |
| [`script.pdf`](releases/global/v2/script.pdf) | the script, with a cue at every click |
| [`specimen.html`](releases/global/v2/specimen.html) | the design system's specimen page |
| [`design.md`](releases/global/v2/design.md), [`tokens.toml`](releases/global/v2/tokens.toml) | the design system, with every token resolved |

The high-level storyboard is [`skeleton.md`](talk/global/4-visual/skeleton.md), the frame-by-frame
one [`storyboard.toml`](talk/global/4-visual/storyboard.toml), and both as a page
[`greybox.html`](talk/global/4-visual/greybox.html).

## Build it

From this folder:

```bash
uv run --project ../.. mpp build           # draft: build/global/draft.html
uv run --project ../.. mpp script --pdf    # the script: build/global/script.pdf
uv run --project ../.. mpp greybox         # the greybox page
```

Its tags carry its path: `examples/pipeline-talk/global/brief-1` and so on, and
`examples/pipeline-talk/global/v2` for the current release (v1 is the six-minute first version,
still in the history at its tag).

## What is not real about it

- **The agent stood in for the author at most checkpoints.** It made the picks in the option files
  and created the approval tags; each tag's message says so. A real run stops at every one of those
  points.
- **No one has read the script aloud.** Its time is a word count at normal pace
  (`readaloud.md`).
- **Review notes #1 to #4 were the agent's own**, from looking at the first draft's stills. Notes #5
  to #7 came from a person, on the first release: one beat per stage, a longer slot, and alignment.
  They went back to the outline, the brief and the design, and every stage after them was redone
  and re-approved; the tags (`outline-2`, `script-3`, `design-2`, ...) record it.
- **The talk-within-the-talk is invented.** "The slowest waits halve once the cache is warm" is
  the guides' running example, not a measured result, and its bars carry no numbers.
