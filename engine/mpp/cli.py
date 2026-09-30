"""The `mpp` command line: `uv run mpp <command> [-v VARIANT] ...`.

Each command is a thin wrapper over one engine module; this file only parses arguments and prints.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from .project import Talk, find_root


def talk_of(args) -> Talk:
    root = find_root(Path.cwd())
    if root is None:
        sys.exit("not inside a manim-presentation-pipeline repository (no talk/ and pipeline/ here or above)")
    return Talk(root, getattr(args, "variant", None))


def rel(talk: Talk, p: Path) -> str:
    return str(p.relative_to(talk.root)) if p.is_relative_to(talk.root) else str(p)


# ---------------------------------------------------------------- commands
def cmd_status(args):
    from . import stages

    talk = talk_of(args)
    rows = stages.status(talk)
    others = stages.variants(talk)
    print(f"talk: {talk.name}" + (f"   (variants: {', '.join(others)})" if others and not talk.variant else ""))
    for r in rows:
        s = r["stage"]
        state = (
            f"approved {r['tag']}" + (", changed since" if r["changed"] else "")
            if r["tag"]
            else "has files, not approved"
            if r["has_files"]
            else "not started"
        )
        print(f"  {s.name:<10} {state}{'   (optional)' if s.optional else ''}")
    nxt = stages.next_stage(rows)
    print(
        f"\nnext: {nxt.name} (pipeline/stages/{nxt.folder.split('-')[0]}-{nxt.name}.md)" if nxt else "\nnext: release"
    )
    if not talk.variant:
        for v in others:
            tags = stages.git(talk, "tag", "--list", f"{v}/*", "--sort=creatordate").split()
            global_changed = tags and subprocess.run(
                ["git", "diff", "--quiet", tags[-1], "--", "talk/global"], cwd=talk.root
            )
            if global_changed and global_changed.returncode:
                print(f"variant {v}: talk/global changed since {tags[-1]}; rebuild it and re-approve what changed")


def cmd_approve(args):
    from . import stages

    talk = talk_of(args)
    print("tagged", stages.approve(talk, args.stage, args.message or ""))


def cmd_new_variant(args):
    talk = talk_of(args)
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.name) or args.name == "global":
        sys.exit("a variant name is lower case letters, digits and dashes, and not 'global'")
    folder = talk.root / "talk" / "variants" / args.name
    if folder.exists():
        sys.exit(f"{rel(talk, folder)} exists")
    (folder / "0-brief").mkdir(parents=True)
    (folder / "0-brief" / "talk.toml").write_text(
        f"# Variant {args.name}: only the keys that differ from talk/global/0-brief/talk.toml.\n"
        "# Other files: put a copy in the same stage folder here, and it replaces global's (Markdown)\n"
        "# or merges over it key by key (TOML). See pipeline/variants.md.\n"
    )
    print(f"created {rel(talk, folder)}/")


def cmd_numbers(args):
    talk = talk_of(args)
    sb = Talk(talk.root, talk.variant, commit=args.at).storyboard()
    for f in sb.frames():
        print(f"{f.number:>4}  {f.id:<10} {f.head}")


def cmd_script(args):
    from . import script

    print(script.run(talk_of(args), pdf=args.pdf))


def cmd_greybox(args):
    from . import greybox

    talk = talk_of(args)
    print("wrote", rel(talk, greybox.write(talk)))


def cmd_specimen(args):
    from .preview import specimen

    talk = talk_of(args)
    print("wrote", rel(talk, specimen(talk)))


def cmd_build(args):
    from .build import BuildError, build

    talk = talk_of(args)
    try:
        out = build(talk, beats=args.beats or None, act=args.act, final=args.final, force=args.force, jobs=args.jobs)
    except BuildError as e:
        sys.exit(str(e))
    print("\n".join(f"wrote {rel(talk, p)}" for p in out))


def cmd_check(args):
    from . import checks

    talk = talk_of(args)
    quality = "final" if args.final else "draft"
    problems = checks.static(talk)
    lint = checks.lint(talk, quality)
    rows, bad = checks.seams(talk, quality, sheet=Path(args.sheet) if args.sheet else None)
    for p in problems:
        print("storyboard:", p)
    for line in lint:
        print("layout:", line)
    for a, b, d in bad:
        print(f"seam: {a} -> {b} differs by {d:.1f}")
    print(
        f"\n{len(problems)} storyboard problems, {len(lint)} layout findings, {len(bad)} of {len(rows)} seams flagged"
    )
    if problems or lint or bad:
        sys.exit(1)


def cmd_preview(args):
    from .build import BuildError
    from .preview import preview

    talk = talk_of(args)
    if not args.refs and not args.changed:
        sys.exit("name slides (7, 7-12, B3.2, B3) or pass --changed")
    try:
        path, frames = preview(talk, args.refs, changed=args.changed)
    except BuildError as e:
        sys.exit(str(e))
    print(f"wrote {rel(talk, path)} ({len(frames)} stills)")


def cmd_review(args):
    from . import review

    talk = talk_of(args)
    if args.action == "add":
        r = review.add(talk, args.slide, args.note, args.stage, args.build)
        print(f"#{r['#']}  slide {r['slide']} ({r['ID']}), {r['stage']}: {r['note']}")
    elif args.action in ("done", "decline"):
        r = review.close(talk, args.number, "done" if args.action == "done" else "declined", args.text, args.commit)
        print(f"#{r['#']} {r['status']}: {r['fix']}")
    else:
        _, rows = review.read(talk)
        for r in rows:
            if not args.open or r["status"] == "open":
                where = f"slide {r['slide'] or '-':<4} {r['ID'] or '-':<8}"
                print(f"#{r['#']:<3} {r['status']:<8} {where} {r['stage']:<8} {r['note']}")


def toml_dump(data: dict, prefix: str = "") -> str:
    """Enough TOML for resolved tokens: tables of strings, numbers and lists of strings."""

    def val(v):
        if isinstance(v, str):
            return f'"{v}"'
        return "[" + ", ".join(map(val, v)) + "]" if isinstance(v, list) else str(v)

    plain = [f"{k} = {val(v)}" for k, v in data.items() if not isinstance(v, dict)]
    out = ([f"[{prefix}]"] if prefix and plain else []) + plain
    for k, v in data.items():
        if isinstance(v, dict):
            out += ["", toml_dump(v, f"{prefix}.{k}" if prefix else k)]
    return "\n".join(out)


def cmd_release(args):
    from . import checks, review, stages
    from . import script as scripts
    from .build import BuildError, build
    from .preview import specimen

    talk = talk_of(args)
    if stages.git(talk, "status", "--porcelain", "--untracked-files=no"):
        sys.exit("commit everything first: a release is rebuilt from its tag")
    rows = stages.status(talk)
    pending = [r["stage"].name for r in rows if not r["stage"].optional and (r["tag"] is None or r["changed"])]
    if pending:
        sys.exit(f"not approved (or changed since): {', '.join(pending)}")
    open_notes = [r for r in review.read(talk)[1] if r["status"] == "open"]
    if open_notes:
        sys.exit(f"{len(open_notes)} review notes are open: see `mpp review list --open`")
    problems = checks.static(talk)
    if problems:
        sys.exit("storyboard problems:\n  " + "\n  ".join(problems))
    print(scripts.run(talk, pdf=True))
    if stages.git(talk, "status", "--porcelain", "--untracked-files=no"):
        sys.exit("script.md was out of date with the storyboard: it is regenerated now; commit it and release again")
    try:
        html, pdf = build(talk, final=True, name="talk")
    except BuildError as e:
        sys.exit(str(e))
    lint = checks.lint(talk, "final")
    if lint:
        sys.exit("layout findings:\n  " + "\n  ".join(lint))
    for a, b, d in checks.seams(talk, "final")[1]:
        print(f"warning: seam {a} -> {b} differs by {d:.1f}; look at it before presenting")
    spec = specimen(talk)
    versions = [
        int(m[1])
        for t in stages.git(talk, "tag", "--list", f"{talk.name}/v*").split()
        if (m := re.fullmatch(r".*/v(\d+)", t))
    ]
    n = max(versions, default=0) + 1
    dest = talk.root / "releases" / talk.name / f"v{n}"
    dest.mkdir(parents=True, exist_ok=True)
    for src in (html, pdf, talk.exports() / "script.pdf", spec):
        shutil.copy2(src, dest / src.name)
    design = talk.path("5-design/design.md")
    if design:
        shutil.copy2(design, dest / "design.md")
    (dest / "tokens.toml").write_text(
        "# Resolved: engine defaults, then the talk's own tokens.\n" + toml_dump(talk.tokens()) + "\n"
    )
    tag = f"{talk.name}/v{n}"
    stages.git(talk, "tag", "-a", tag, "-m", f"release {tag}")
    print(f"released {rel(talk, dest)}/ and tagged {tag}")


def cmd_later(args):
    sys.exit(f"mpp {args.command}: not implemented yet")


# ---------------------------------------------------------------- parser
def main() -> None:
    ap = argparse.ArgumentParser(prog="mpp", description="manim-presentation-pipeline: uv run mpp <command>")
    sub = ap.add_subparsers(dest="command", required=True, metavar="command")
    variant = argparse.ArgumentParser(add_help=False)
    variant.add_argument("-v", "--variant", help="a variant of the talk (default: the main talk, global)")

    def command(name, fn, help_text, parents=(variant,)):
        p = sub.add_parser(name, help=help_text, description=help_text, parents=list(parents))
        p.set_defaults(fn=fn)
        return p

    command("setup", cmd_later, "install what can be installed", ())
    command("doctor", cmd_later, "check Python, cairo, pango, LaTeX, fonts, reveal.js", ())
    command("status", cmd_status, "approved stages and what's next")
    p = command("approve", cmd_approve, "tag a stage as approved")
    p.add_argument("stage", help="brief, digest, outline, script, visual, design, build or rehearsal")
    p.add_argument("-m", "--message", help="the tag message")
    p = command("new-variant", cmd_new_variant, "create a variant folder", ())
    p.add_argument("name")
    p = command("numbers", cmd_numbers, "the conversion table: slide number, stable ID, headline")
    p.add_argument("--at", metavar="COMMIT", help="as built at this commit (the one on the draft)")
    p = command("script", cmd_script, "time the script at the pace class; regenerate it from the storyboard")
    p.add_argument("--pdf", action="store_true", help="also write the script PDF to build/<variant>/")
    command("greybox", cmd_greybox, "the greybox page, generated from the storyboard")
    command("specimen", cmd_specimen, "the design-system specimen page")
    p = command("build", cmd_build, "render the deck: a draft (720p24) by default")
    p.add_argument("beats", nargs="*", help="beat IDs; default: the whole talk, or --act")
    p.add_argument("--act", type=int)
    p.add_argument("--final", action="store_true", help="full quality (1080p30), no draft label")
    p.add_argument("--force", action="store_true", help="render every selected beat, changed or not")
    p.add_argument("--jobs", type=int, help="beats rendered at once; default: the cores this process may use")
    p = command("check", cmd_check, "storyboard problems, layout lint, seams")
    p.add_argument("--final", action="store_true", help="check the final renders instead of the drafts")
    p.add_argument("--sheet", help="write the worst seams side by side to this image")
    p = command("preview", cmd_preview, "stills of chosen slides as one page")
    p.add_argument("refs", nargs="*", help="7, 7-12, B3.2 or B3")
    p.add_argument("--changed", action="store_true", help="every slide whose beat changed since the last preview")
    p = command("review", cmd_review, "the review log")
    actions = p.add_subparsers(dest="action", required=True, metavar="action")
    a = actions.add_parser("add", help="log a note", parents=[variant])
    a.add_argument("slide", help="slide number or stable ID; '' for a note on no slide")
    a.add_argument("note")
    a.add_argument("--stage", required=True, help="brief, digest, outline, script, visual, design or build")
    a.add_argument("--build", help="the commit on the draft the note was made on (default: HEAD)")
    a = actions.add_parser("list", help="the notes", parents=[variant])
    a.add_argument("--open", action="store_true", help="only open notes")
    for name, what in (("done", "the fix"), ("decline", "the reason")):
        a = actions.add_parser(name, help=f"close a note with {what}", parents=[variant])
        a.add_argument("number")
        a.add_argument("text", help=what)
        a.add_argument("--commit", help="the commit with the fix (default: HEAD)")
    command("release", cmd_release, "final checks, full render, copy to releases/, tag")

    args = ap.parse_args()
    try:
        args.fn(args)
    except (FileNotFoundError, KeyError, ValueError, RuntimeError) as e:
        sys.exit(f"mpp {args.command}: {e}")
