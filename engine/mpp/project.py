"""Where a talk's files are, with the variant cascade applied.

A talk is `talk/global/` plus, optionally, one variant folder `talk/variants/<name>/` holding only
what differs. A variant may build on another one (`base = "<name>"` in its own `0-brief/talk.toml`),
whose layer then sits between it and `global/`. A file is looked up in the variant first, then in its
bases, then in `global/`. TOML files merge key by
key instead (tables recursively, anything else replaced whole), over the engine's defaults where it
has some. Everything the engine and the CLI read about a talk goes through here, so the cascade has
one definition.

A Talk can also be read at a git commit, which is how a slide number on an old draft is traced back
to the storyboard it was built from.

A talk's root is any folder holding `talk/global/`: the repository's own, or an example inside it
(`examples/<name>/`). What every talk shares (`pipeline/`, `vendor/`) is found from the engine.
"""

import os
import subprocess
import tomllib
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
REPO = ENGINE.parent.parent  # pipeline/ and vendor/; the engine runs from its checkout (uv sync)
DEFAULTS = ENGINE / "defaults"


def merge(base: dict, over: dict) -> dict:
    """`over` on top of `base`: tables merge recursively, any other value is replaced whole."""
    out = dict(base)
    for k, v in over.items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def find_root(start: Path) -> Path | None:
    """The nearest folder at or above `start` that holds a talk."""
    for p in (start, *start.parents):
        if (p / "talk" / "global").is_dir():
            return p
    return None


class Talk:
    def __init__(self, root: Path, variant: str | None = None, commit: str | None = None):
        self.root = Path(root)
        self.variant = variant or None
        self.commit = commit
        self.name = self.variant or "global"
        self.layers = []
        name, seen = self.variant, []
        while name:  # a variant may build on another (`base` in its talk.toml): its layer sits beneath
            if name in seen:
                raise ValueError(f"variant {self.variant!r}: its bases loop ({' -> '.join([*seen, name])})")
            layer = f"talk/variants/{name}"
            if not self._exists(layer):
                raise FileNotFoundError(f"no variant {name!r}: {layer}/ does not exist")
            seen.append(name)
            self.layers.append(layer)
            own = self._read_layer(layer, "0-brief/talk.toml")
            name = tomllib.loads(own).get("base") if own else None
        self.layers.append("talk/global")

    @classmethod
    def current(cls) -> "Talk":
        """The talk a render belongs to: set by the build through MPP_ROOT and MPP_VARIANT, else found
        from the working directory or from this package's own checkout."""
        root = os.environ.get("MPP_ROOT")
        root = Path(root) if root else find_root(Path.cwd()) or find_root(ENGINE)
        if root is None:
            raise RuntimeError("no talk here: no talk/global/ in this folder or above")
        return cls(root, os.environ.get("MPP_VARIANT"))

    # ------------------------------------------------------------ files
    def _exists(self, rel: str) -> bool:
        if self.commit is None:
            return (self.root / rel).exists()
        return self._git("cat-file", "-e", f"{self.commit}:./{rel}") is not None

    def _git(self, *args) -> str | None:
        r = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None

    def _read_layer(self, layer: str, rel: str) -> str | None:
        if self.commit is None:
            p = self.root / layer / rel
            return p.read_text() if p.is_file() else None
        return self._git("show", f"{self.commit}:./{layer}/{rel}")

    def read(self, rel: str) -> str | None:
        """A whole file, from the first layer that has it."""
        for layer in self.layers:
            text = self._read_layer(layer, rel)
            if text is not None:
                return text
        return None

    def path(self, rel: str) -> Path | None:
        """The file on disk that `read` would return (working tree only)."""
        for layer in self.layers:
            p = self.root / layer / rel
            if p.exists():
                return p
        return None

    def toml(self, rel: str, base: dict | None = None) -> dict:
        """A TOML file merged key by key: `base`, then global, then the variant."""
        out = dict(base or {})
        for layer in reversed(self.layers):
            text = self._read_layer(layer, rel)
            if text is not None:
                out = merge(out, tomllib.loads(text))
        return out

    def dirs(self, rel: str) -> list[Path]:
        """A folder in every layer that has it, variant first: the import path for beats and components."""
        return [self.root / layer / rel for layer in self.layers if (self.root / layer / rel).is_dir()]

    @property
    def tag_base(self) -> str:
        """Approval and release tags start here: `global`, or `examples/<name>/global` for a talk that
        is not at the repository's root, so two talks in one repository never share a tag."""
        return (self._git("rev-parse", "--show-prefix") or "").strip() + self.name

    # ------------------------------------------------------------ the talk's data
    def config(self) -> dict:
        return self.toml("0-brief/talk.toml")

    def tokens(self) -> dict:
        return self.toml("5-design/tokens.toml", base=tomllib.loads((DEFAULTS / "tokens.toml").read_text()))

    def storyboard(self):
        from .storyboard import Storyboard

        data = self.toml("4-visual/storyboard.toml")
        if not data:
            raise FileNotFoundError("no storyboard: talk/global/4-visual/storyboard.toml does not exist")
        return Storyboard(data)

    # ------------------------------------------------------------ outputs
    def renders(self, quality: str | None = None) -> Path:
        """Renders, handoffs and logs: a cache, large, one per variant and quality (draft or final), so a
        final render never evicts the drafts. MPP_OUT moves it (a local disk, a scratch space)."""
        quality = quality or os.environ.get("MPP_QUALITY", "draft")
        base = os.environ.get("MPP_OUT")
        return (Path(base) / self.tag_base if base else self.root / "build" / "render" / self.name) / quality

    def exports(self) -> Path:
        """Draft decks and stills for the author: build/<variant>/."""
        return self.root / "build" / self.name



def load_layer_module(rel: str):
    """Import a module from the talk's layers by its file (`6-build/beats/defence_act1.py`), the first
    layer that has it winning. Beat files share one `beats` package name across layers, so a variant
    built on another imports that variant's beat classes this way: `load_layer_module(...).D2`."""
    import importlib.util
    import sys

    talk = Talk.current()
    path = talk.path(rel)
    if path is None:
        raise FileNotFoundError(f"{rel}: in none of {talk.layers}")
    name = "mpp_layer_" + "_".join(Path(rel).with_suffix("").parts).replace("-", "_")
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]
