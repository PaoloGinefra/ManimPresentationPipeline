# Vendored files

Kept in the repository so a build needs no network.

| Folder | What | Licence |
|---|---|---|
| `fonts/` | Source Sans 3 (Adobe), the default face | SIL Open Font License 1.1, see `fonts/LICENSE.md` |
| `revealjs6.0.1/` | reveal.js 6.0.1 (Hakim El Hattab), the files manim-slides inlines | MIT |

Before every export the build copies `revealjs<version>/` into manim-slides' own cache, where its
offline export looks first, so the HTML deck inlines this copy instead of downloading one. The
version must match the one manim-slides asks for; `mpp doctor` checks it.
