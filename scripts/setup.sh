#!/usr/bin/env bash
# One-time setup on a new machine: cairo and pango, then the Python environment, then `mpp doctor`.
#
# This is a shell script, not an `mpp` command, because `uv run mpp` first installs manim, and
# installing manim is the step that needs cairo and pango. Safe to run again: each step is skipped
# when already done. It never runs sudo; where root is needed it prints the command instead.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
say() { printf '\n== %s\n' "$*"; }

say "uv"
if ! command -v uv >/dev/null; then
  echo "uv is missing. Install it, then run this again:"
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi
uv --version

say "cairo and pango"
if [ -d .native ]; then
  export PKG_CONFIG_PATH="$PWD/.native/usr/lib64/pkgconfig" PKG_CONFIG_DONT_DEFINE_PREFIX=1
fi
if pkg-config --exists cairo pangocairo 2>/dev/null; then
  echo "found: cairo $(pkg-config --modversion cairo), pango $(pkg-config --modversion pangocairo)"
elif [ "$(uname)" = "Darwin" ]; then
  if command -v brew >/dev/null; then
    brew install cairo pango pkg-config
  else
    echo "Install Homebrew (https://brew.sh), then run this again."
    exit 1
  fi
elif command -v apt-get >/dev/null; then
  echo "Needs root. Run this, then run setup again:"
  echo "  sudo apt install libcairo2-dev libpango1.0-dev pkg-config python3-dev"
  exit 1
elif command -v dnf >/dev/null && ls /usr/lib64/libcairo.so.2 >/dev/null 2>&1; then
  echo "cairo is installed but its headers are not: unpacking them into .native/ (no root needed)"
  scripts/bootstrap-native.sh
  export PKG_CONFIG_PATH="$PWD/.native/usr/lib64/pkgconfig" PKG_CONFIG_DONT_DEFINE_PREFIX=1
else
  echo "Install cairo and pango with their development headers and pkg-config, then run this again."
  exit 1
fi

say "Python environment"
uv sync

say "LaTeX (only for mathematics on slides)"
if command -v latex >/dev/null && command -v dvisvgm >/dev/null; then
  latex --version | head -1
else
  echo "not found: mpp doctor prints how to install it"
fi

say "mpp doctor"
uv run mpp doctor
