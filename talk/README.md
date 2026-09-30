# Your talk

Everything about your presentation lives in this folder, and nothing else in the repository needs
to change. Start with `uv run mpp status`, and with `AGENTS.md` if an agent is helping.

| Folder | What |
|---|---|
| `source/` | the paper, report, thesis, data or code the talk is about |
| `global/` | the talk, one folder per stage, each holding that stage's checkpoint files |
| `variants/` | other versions of the talk (a shorter cut, another audience): only what differs |

The files in `global/` start as blank templates, except a placeholder storyboard and its two
scenes, so `uv run mpp build` works right away. Stage 4 replaces them.
