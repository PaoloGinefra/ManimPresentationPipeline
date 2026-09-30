# CLAUDE.md

Read `AGENTS.md` and follow it. Everything there applies to Claude Code.

## Skills

Three docs work best installed as skills, so they load whenever the task needs them. Symlink them
into your skills folder:

| Skill | Source |
|---|---|
| `mpp-pipeline` | `pipeline/principles.md` |
| `talk-scripts` | `pipeline/guides/talk-scripts.md` |
| `talk-storyboards` | `pipeline/guides/talk-storyboards.md` |

```bash
for s in mpp-pipeline:pipeline/principles.md \
         talk-scripts:pipeline/guides/talk-scripts.md \
         talk-storyboards:pipeline/guides/talk-storyboards.md; do
  name=${s%%:*}; src=${s#*:}
  mkdir -p .claude/skills/$name
  ln -sf "$PWD/$src" .claude/skills/$name/SKILL.md
done
```
