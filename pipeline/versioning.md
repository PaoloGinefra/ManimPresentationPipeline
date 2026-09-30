# Versioning

## Commits

One commit per step, and the message starts with the stage and, for a variant, its name:

```
outline: move the demo before the method
short/script: cut B7 to fit ten minutes
```

## Stage tags

When the author approves a stage, tag it with `uv run mpp approve <stage> [variant]`:

- `global/brief-1`, `global/outline-2`, ...
- `<variant>/script-1`, ...

The number counts approvals of that stage. A stage re-approved after a backtrack gets the next
number, so the history of every decision stays in git.

## Releases

`uv run mpp release [variant]` tags `<variant>/vN` (`global/vN` for the main talk) and writes the
files to `releases/<variant>/vN/`. The `releases/` folder is outside git: rendered videos are
large, and any release can be rebuilt from its tag.

## Drafts

Draft decks show their build commit in a corner, so a note on an old draft can be traced to the
storyboard it was built from (`feedback.md`).
