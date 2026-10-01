# Outline

**The one sentence:** Build a talk the way you build software: in stages, each checked cheaply by
its author, from one source file.

**Thread:** one sentence of a talk, "the slowest waits halve once the cache is warm", followed from
the source to its rendered frame (B4), then as the target of a late note (B6), then replaced by this
talk's own frame (B8).

**Peaks:** 1. B4, the sentence changes form at every stage. 2. B6, a late note travels back to its
stage. 3. B8, this slide's own greybox becomes this slide.

**Slot:** 6 min at normal pace (135 wpm), about 810 words.

## Acts

| Act | title | time |
|---|---|---|
| 1 | The problem | 1:15 |
| 2 | The pipeline | 2:50 |
| 3 | Using it | 1:15 |

## Beats

| ID | act | type | spine line | support | time |
|---|---|---|---|---|---|
| B0 | 1 | setup | (title card) | | 0:00 |
| B1 | 1 | setup | An animated talk shows what slides cannot, and it is expensive to change. | motion carries a process; every change is code and a render | 0:35 |
| B2 | 1 | obstacle | Most notes arrive when the deck is built, where every change costs a render. | the same note is a sentence on an outline and a scene rewrite in a deck | 0:40 |
| B3 | 2 | turn | So check each decision where it is cheapest to change. | the author approves something short at every stage; agents do the work | 0:35 |
| B4 | 2 | PEAK | One sentence, followed through every stage, changes form at each checkpoint. | digest row, outline beat, spine line, storyboard frame, grey box, rendered slide | 1:10 |
| B5 | 2 | payoff | The storyboard is the one source file: script and deck are generated from it. | headline, trigger, narration per click; the deck fails to build if a scene drifts | 0:40 |
| B6 | 2 | PEAK | A late note goes back to the earliest stage it changes, and everything after it is rebuilt. | slide 7 is translated to B3.2, echoed with its stage, fixed in the storyboard, regenerated | 1:05 |
| B7 | 3 | payoff | Clone the repository, write only in talk/, and point any agent at AGENTS.md. | plain Markdown instructions, one command per step, offline builds | 0:35 |
| B8 | 3 | PEAK | This talk was made this way: its greybox became this slide. | the close returns to the hook; the one sentence | 0:40 |

Backup: **S1**, what the build checks at every click (text over text, text off the frame, jumps at
seams).

## Plants and payoffs

| planted in | what | paid in |
|---|---|---|
| B1 | the late note and its cost | B6 (the note lands where it belongs), B8 (the close) |
| B2 | the cost ladder, cheap to expensive | B3 (each decision at its cheapest rung) |
| B4 | the sentence's frame and its stable ID B3.2 | B6 (the note is on that frame) |
| B4 | the greybox form | B8 (this talk's own greybox) |

## Cut or held for questions

- Caching and handoff between beats.
- Variants in detail (one clause in B7).
- The layout lint and seam check (backup S1).
- How long the pipeline saves: not measured, not claimed.
