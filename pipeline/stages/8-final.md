# Stage 8: Final

Produce the release.

## Steps

1. Check that every stage is approved and every review note is fixed or declined.
2. Check that the timed read-aloud fits the slot.
3. Run `uv run mpp release [variant]`. It:
   - runs all checks;
   - renders at full quality (1080p) without the draft label;
   - writes the script PDF, the HTML deck, the static PDF (one page per click) and the design
     system;
   - copies them to `releases/<variant>/vN/`, outside git;
   - tags `<variant>/vN`.
4. Open the HTML deck and click through it once end to end.

## Checkpoint

The release folder.

## Done when

The author approves the release.
