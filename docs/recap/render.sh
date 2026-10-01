#!/usr/bin/env bash
# Render the README's recap: docs/recap.mp4 (1080p) and docs/recap.gif (960 px, loops inline on GitHub).
# The scene uses the example talk's tokens and cast, so the engine is pointed at it.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export MPP_ROOT="$PWD/examples/pipeline-talk"
export PYTHONPATH="$MPP_ROOT/talk/global/6-build"
uv run manim render -qh --fps 30 --media_dir build/recap docs/recap/recap.py Recap
cp build/recap/videos/recap/1080p30/Recap.mp4 docs/recap.mp4
uv run python docs/recap/gif.py docs/recap.mp4 docs/recap.gif
ls -la docs/recap.mp4 docs/recap.gif
