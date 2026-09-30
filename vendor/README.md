# Vendored files

Kept in the repository so a build needs no network.

| Folder | What | Licence |
|---|---|---|
| `fonts/` | Source Sans 3 (Adobe), the default face | SIL Open Font License 1.1, see `fonts/LICENSE.md` |
| `cache/manim-slides/revealjs6.0.1/` | reveal.js 6.0.1 (Hakim El Hattab), as manim-slides fetches it | MIT |

The build points manim-slides' cache (`XDG_CACHE_HOME`) at `cache/`, so the exported HTML deck
inlines this copy instead of downloading one.
