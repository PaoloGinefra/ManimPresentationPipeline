# Variants

One talk, several versions: a shorter cut, another audience, another language.

## Layout

```
talk/
  global/            the full talk, every stage folder
  variants/
    short/           only the files that differ from global/
      0-brief/talk.toml
      4-visual/storyboard.toml
```

Create one with `uv run mpp new-variant <name>`.

## Lookup

- A file is looked up in the variant first, then in `global/`.
- **Markdown and other files** override whole: the variant's copy replaces the global one.
- **TOML files** merge key by key: the variant file holds only the keys it changes. Tables merge
  recursively; any other value, including a list, is replaced whole.
- One level only. A variant cannot build on another variant.

## Beat order

The storyboard's `order` and `backup` lists decide which beats a variant contains. A variant that
lists its own `order` drops every beat it leaves out, or moves it to `backup`. It can also
override single keys of a beat, such as a headline or a narration.

## Stages

A variant goes through the stages its files touch. A shorter cut usually changes the brief
(`talk.toml`), the outline and the storyboard, and reuses the design and the beat scenes. Its
approvals are tagged under its name (`versioning.md`).

## Changes to global/

A change in `global/` affects every variant that does not override that file or key. List them
(`mpp status` does), rebuild each, and re-approve only the changed pieces.
