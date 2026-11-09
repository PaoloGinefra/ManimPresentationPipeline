# Stage 0: Brief

Fix what the talk is for before reading the source in depth.

## Input

The author's request and the files in `talk/source/`.

## Steps

1. Skim the source enough to suggest answers.
2. Ask the author the questions below, a few at a time, each with a suggested answer.
3. Write `0-brief/brief.md` (the prose) and `0-brief/talk.toml` (the numbers the tools read).

## Questions

- Who is in the room, and what do they already know?
- How long is the slot? Are questions inside it?
- Which pace class: slow (120 wpm), normal (135) or fast (150)? Measure it instead of guessing (below).
- By when, in minutes, should the audience hear what the author did? A talk that spends half its slot
  on motivation reads as slow to every committee; write the target down and check it at the outline.
- What is the one sentence the audience should repeat afterwards?
- What must not be said, or is held for questions?
- Are there existing figures, a house style, or standing rules to follow?
- What does the author want delivered: script, deck, static PDF, backup slides?

## Measure the speaker

A word budget is only as good as the pace behind it. Before the outline, the author reads one sample
paragraph aloud **twice**: once reading it word for word, once speaking freely from it. Record both
in `brief.md` (set `pace` in `talk.toml` to the nearest class):

- the reading pace (words per minute), which sets the pace class;
- the **expansion factor**: spoken words over written words when speaking freely. Many speakers say
  1.3 to 1.8 times what is written. Every later budget divides the slot by it: a 15-minute slot for a
  speaker who expands by 1.5 holds about 10 minutes of written script.

## Checkpoint

`brief.md` and `talk.toml`, from `templates/0-brief/`.

## Done when

The author approves the brief. Tag `global/brief-1`.

## Later changes

A change of slot, pace or audience is a brief change. Every later stage is checked against it
(`feedback.md`).
