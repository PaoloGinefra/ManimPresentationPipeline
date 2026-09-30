"""The `mpp` command line. Commands are filled in as the pipeline is built."""

import argparse

COMMANDS = {
    "setup": "install what can be installed",
    "doctor": "check Python, cairo, pango, LaTeX, fonts, reveal.js",
    "new-variant": "create a variant folder",
    "status": "approved stages and what's next",
    "approve": "tag a stage as approved",
    "script": "generate the script, with timing at the pace class",
    "build": "draft or full-quality render",
    "check": "frame counts, seams, layout lint",
    "preview": "stills as a standalone file",
    "review": "the review log",
    "release": "final checks, full render, copy to releases, tag",
}


def main() -> None:
    parser = argparse.ArgumentParser(prog="mpp", description="manim-presentation-pipeline")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text in COMMANDS.items():
        sub.add_parser(name, help=help_text)
    args, _ = parser.parse_known_args()
    raise SystemExit(f"mpp {args.command}: not implemented yet")
