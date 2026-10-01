# Skeleton

**The one sentence:** Build a talk the way you build software: in stages, each checked cheaply by
its author, from one source file.

**Thread:** a talk about a cache. In the brief and the digest it is shown whole; from the outline on,
one of its sentences, "the slowest waits halve once the cache is warm", is followed alone.

**Peaks and key images:** B11, the sentence lifting out of the outline to be followed alone. B6, the
note travelling back along the row. B8, this slide's greybox becoming this slide.

## Cast

| object | role | verbs | beats |
|---|---|---|---|
| queue and cache | what motion is good at | fill, warm | B1 |
| ladder | cost of a change, by stage, qualitative | appear, pile notes, turn into the row | B2, B3 |
| row of stages | the pipeline: nine stages, rehearsal dashed because it is optional | appear, light one, tick, ripple | B3 to B8 |
| card | the cache talk's checkpoint at each stage, one 16:9 card that changes form | change form, shrink aside | B3 to B16 |
| check list | what the author checks before moving on | appear item by item | every stage beat |
| note card | a reviewer's late note | appear, label, travel | B2, B6 |

## Canvas

One screen. From B3 on, the row of stages lives along the bottom and stays; the card lives above it,
centred while its stage is explained, shrunk to the left while the check list stands on the right.

## Alignment

Every left edge sits on the headline's margin or on a column of the layout; labels that share a
line share a baseline (`tk.set_baseline`), not a centre. The check list's items share one left edge.

## Colour roles

| role | used for |
|---|---|
| ours | the followed sentence, the stage in focus |
| highlight | the note |
| structure | rows, rungs, cards, everything that is scaffolding |
| muted | labels that name things |

## Interaction policy

The rules in `pipeline/guides/talk-storyboards.md`. Every stage beat makes the same two clicks: the
checkpoint, then the checks; the second click ends with the stage's tick.

## Beats

| ID | headline | visual idea | in / out | transition | role | time |
|---|---|---|---|---|---|---|
| B0 | Build a talk like software | title card | - / - | - | setup | 0:00 |
| B1 | An animated talk shows what slides can't. | a queue fills, a cache warms; then code covers it | - / - | step | setup | 0:30 |
| B2 | The same note costs more the later it lands. | ladder, notes pile at the top | - / ladder | step | obstacle | 0:25 |
| B3 | Check each decision where it's cheapest to change. | ladder turns into the nine-stage row; the cache talk's card | ladder / row, card | step | turn | 0:25 |
| B9 | The brief fixes what the talk is for. | the cache talk's brief; checks | row, card / row, card | step | stage | 0:40 |
| B10 | The digest lists what the talk could say, with sources. | three claims, the result in ours; checks | same | step | stage | 0:35 |
| B11 | The outline is the story on one page. | options, then the page; B3 lifts out; checks | same | step | PEAK: the sentence picked | 0:40 |
| B12 | The script is what the speaker says, written for the ear. | spine line; checks | same | step | stage | 0:40 |
| B13 | The storyboard splits the script into clicks. | frame, then greybox; checks | same | step | stage | 0:45 |
| B14 | The design system fixes the look once. | specimen; checks | same | step | stage | 0:25 |
| B15 | The build renders the deck, drafts first. | the rendered slide; checks | same | step | stage | 0:35 |
| B6 | Rehearsal: a late note goes back to the earliest stage it changes. | note travels back, ripple forward | row / row | step | PEAK: the note going home | 0:55 |
| B16 | The final stage releases the talk. | the release folder; checks; every stage ticked | row / row | step | stage | 0:25 |
| B7 | Clone it, write only in talk/, point any agent at AGENTS.md. | folders, talk/ lit; two commands | row / row | act break (quiet) | payoff | 0:30 |
| B8 | This slide started as a grey box. | greybox becomes the slide | row / - | step | PEAK: the greybox turning real | 0:30 |
| S1 | The build checks every click for text over text. | overlap flagged; seam pair | - / - | - | backup | - |
