# Skeleton

**The one sentence:** Build a talk the way you build software: in stages, each checked cheaply by
its author, from one source file.

**Thread:** the sentence "the slowest waits halve once the cache is warm", as a card.

**Peaks and key images:** B4, the card changing form along the row. B6, the note travelling back.
B8, this slide's greybox becoming this slide.

## Cast

| object | role | verbs | beats |
|---|---|---|---|
| queue and cache | what motion is good at | fill, warm | B1 |
| ladder | cost of a change, by stage, qualitative | appear, pile notes, turn into the row | B2, B3 |
| row of stages | the pipeline: brief, digest, outline, script, visual, design, build, final | appear, tick, light one, ripple | B3 to B8 |
| sentence card | the thread | move to a stage, change form | B4, B6 |
| note card | a reviewer's late note | appear, label, travel | B2, B6 |
| storyboard file | the one source | appear, emit script, emit deck | B5 |

## Canvas

One screen. Act 1 uses the centre. From B3 on, the row of stages lives along the bottom and stays;
act 2 and act 3 build above it. No zooms: the talk is short, and the row is its map.

## Colour roles

| role | used for |
|---|---|
| ours | the thread sentence, and the pipeline's own objects when they are the subject |
| highlight | the note |
| structure | rows, rungs, boxes, everything that is scaffolding |
| muted | labels that name things |

## Interaction policy

The rules in `pipeline/guides/talk-storyboards.md`. No exceptions.

## Beats

| ID | headline | visual idea | in / out | transition | role | asset | time |
|---|---|---|---|---|---|---|---|
| B0 | Build a talk like software | title card | - / - | - | setup | new | 0:00 |
| B1 | An animated talk shows what slides can't. | a queue fills, a cache warms | - / - | step | setup | new | 0:35 |
| B2 | The same note costs more the later it lands. | ladder, notes pile at the top | - / ladder | step | obstacle | new | 0:40 |
| B3 | Check each decision where it's cheapest to change. | ladder turns into the row | ladder / row | step | turn | new | 0:35 |
| B4 | One sentence changes form at every stage. | the card moves along the row | row / row, card at render | step | PEAK: the changing card | new | 1:10 |
| B5 | The storyboard is the one source file. | file emits script and deck | row / row | step | payoff | new | 0:40 |
| B6 | A late note goes back to the earliest stage it changes. | note travels back, ripple forward | row / row | step | PEAK: the note going home | new | 1:05 |
| B7 | Clone it, write only in talk/, point any agent at AGENTS.md. | folders, talk/ lit | row / row | act break (quiet: a crossfade) | payoff | new | 0:35 |
| B8 | This slide started as a grey box. | greybox becomes the slide | row / - | step | PEAK: the greybox turning real | new | 0:40 |
| S1 | The build checks every click for text over text. | overlap flagged; seam pair | - / - | - | backup | new | - |
