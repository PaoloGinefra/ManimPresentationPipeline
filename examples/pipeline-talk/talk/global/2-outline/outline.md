# Outline

Version 2, after review note #5: act 2 is one beat per stage.

**The one sentence:** Build a talk the way you build software: in stages, each checked cheaply by
its author, from one source file.

**Thread:** a talk about a cache, made with the pipeline. In the brief and the digest it is a whole
talk: an audience, a slot, its own one sentence, its claims. From the outline on, one of its
sentences is followed alone: "the slowest waits halve once the cache is warm".

**Peaks:** 1. B11, the sentence is picked out of the digest and becomes one beat of the cache talk's
outline: from here on the talk follows it alone. 2. B6, a reviewer's late note on that sentence's
slide travels back to the script stage. 3. B8, this slide's own greybox becomes this slide.

**Every stage beat has the same two moves:** what the stage is, shown as the cache talk's checkpoint
file at that stage; then what the author checks before moving on, as a short list, and the stage
ticks on the row.

**Slot:** 8 min at normal pace (135 wpm), about 1,080 words.

## Acts

| Act | title | time |
|---|---|---|
| 1 | The problem | 1:20 |
| 2 | The stages | 5:40 |
| 3 | Using it | 1:00 |

## Beats

Beat IDs are stable: B4 and B5 of version 1 are retired (their content now lives in the stage
beats), the stage beats take the next free IDs, and the order lives in the storyboard.

| ID | act | type | spine line | the author checks | time |
|---|---|---|---|---|---|
| B0 | 1 | setup | (title card) | | 0:00 |
| B1 | 1 | setup | An animated talk shows what slides can't, and it's expensive to change. | | 0:30 |
| B2 | 1 | obstacle | Most notes arrive when the deck is built, where every change costs a render. | | 0:25 |
| B3 | 1 | turn | So check each decision where it's cheapest to change, in stages. | | 0:25 |
| B9 | 2 | setup | The brief fixes what the talk is for, before anyone writes. | who is in the room; the slot and pace; the one sentence | 0:40 |
| B10 | 2 | payoff | The digest lists everything the talk could say, each with its source. | must, could or leave out; every gap answered | 0:35 |
| B11 | 2 | PEAK | The outline is the story on one page; from here, follow one sentence. | a pick per decision; the story on one page | 0:40 |
| B12 | 2 | payoff | The script is what the speaker says, written for the ear. | every act read aloud; the total fits the slot | 0:40 |
| B13 | 2 | payoff | The storyboard splits it into clicks, and the greybox shows them as rough boxes. | a pick per beat; the greybox: one claim per slide | 0:45 |
| B14 | 2 | payoff | The design system fixes the look once, on one page. | the specimen | 0:25 |
| B15 | 2 | payoff | The build renders the deck, as drafts first. | stills of every slide; a click-through per act | 0:35 |
| B6 | 2 | PEAK | Rehearsal: a late note goes back to the earliest stage it changes. | the plan: each note with its stage | 0:55 |
| B16 | 2 | payoff | The final stage releases the deck once everything is checked. | one click-through, end to end | 0:25 |
| B7 | 3 | payoff | Clone the repository, write only in talk/, point any agent at AGENTS.md. | | 0:30 |
| B8 | 3 | PEAK | This talk was made this way; this slide started as a grey box. | | 0:30 |

Backup: **S1**, what the build checks at every click.

## Plants and payoffs

| planted in | what | paid in |
|---|---|---|
| B2 | notes arrive at the expensive end | B6 (the note lands where it belongs) |
| B3 | the row of stages | every stage beat ticks it; B8 ticks the last |
| B10 | the sentence, one row among the cache talk's claims | B11 (it is picked out) |
| B13 | the greybox form | B8 (this talk's own greybox) |
| B9 | the cache talk's one sentence, different from the slide sentence | B11 (one talk, many sentences: follow one) |

## Cut or held for questions

- Caching and handoff between beats; variants in detail (one clause in B7).
- The layout lint and seam check (backup S1).
- How long the pipeline saves: not measured, not claimed.
