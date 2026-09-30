"""One standalone HTML page, for every checkpoint that is a page: greybox, preview, specimen.

Everything is inline (styles, images as data URIs), so the author opens the file with nothing else.
"""

import base64
import html
from pathlib import Path

STYLE = """
:root { --ink: #1b1f2a; --muted: #5b6170; --line: #c9ccd2; --box: #e4e6ea; --ground: #ffffff; }
@media (prefers-color-scheme: dark) {
  :root { --ink: #e8eaee; --muted: #a3a8b3; --line: #4a4f5a; --box: #2e323b; --ground: #16181d; }
}
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 16px 64px; background: var(--ground); color: var(--ink);
       font: 15px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width: 1100px; margin: 0 auto; }
h1 { font-size: 22px; margin: 0 0 4px; }
h2 { font-size: 17px; margin: 40px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--line); }
.meta { color: var(--muted); margin: 0 0 24px; }
.frame { display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); gap: 20px; margin: 0 0 28px; }
@media (max-width: 760px) { .frame { grid-template-columns: 1fr; } }
.screen { position: relative; aspect-ratio: 16 / 9; border: 1px solid var(--line); border-radius: 4px;
          overflow: hidden; background: var(--ground); }
.screen img { width: 100%; height: 100%; display: block; }
.head { position: absolute; left: 5%; top: 5%; width: 78%; font-weight: 600; font-size: clamp(11px, 1.8vw, 17px); }
.num { position: absolute; right: 4%; top: 5%; color: var(--muted); font-size: 13px; }
.grid { position: absolute; left: 5%; right: 5%; top: 22%; bottom: 8%; display: grid;
        grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr); gap: 6px; }
.box { background: var(--box); border-radius: 3px; display: flex; align-items: center; justify-content: center;
       text-align: center; padding: 4px; color: var(--muted); font-size: 12px; }
.text p { margin: 0 0 8px; }
.id { color: var(--muted); font-size: 13px; }
.trigger { color: var(--muted); font-style: italic; }
.note { color: var(--muted); font-size: 13px; }
"""


def esc(s: str) -> str:
    return html.escape(" ".join((s or "").split()))


def image(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    return f'<img alt="" src="data:image/png;base64,{data}">'


def write(path: Path, title: str, meta: str, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        f"<meta name='viewport' content='width=device-width, initial-scale=1'><title>{esc(title)}</title>"
        f"<style>{STYLE}</style></head><body><main><h1>{esc(title)}</h1><p class='meta'>{meta}</p>"
        f"{body}</main></body></html>\n"
    )
    return path
