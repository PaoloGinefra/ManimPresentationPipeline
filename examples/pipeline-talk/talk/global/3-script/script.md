# Script

One section per beat, in outline order. The bold line is the spine; the rest is support.
`> ` lines are visual notes, not spoken.

## Act 1: The problem

### B1. Motion is expensive - 0:35
**An animated talk shows what slides can't, and it's expensive to change.**

When an idea is a process, motion carries it. A queue fills up. A cache warms. The room watches it
happen instead of reading about it. But every frame of that is code. And every change means
rendering it again. A word you'd fix in a second on a slide becomes a scene to rewrite.

> A queue of requests fills; the cache beside it warms.

### B2. Notes arrive late - 0:40
**Most notes arrive when the deck is built, and that's where every change costs a render.**

Think about where a note can land. On a one-page outline, moving a section costs a line. In a
script, changing a word costs a word. In a finished deck, the same note costs a scene and a render.
And that's where most notes arrive. It's the first time anyone sees the talk. So the feedback
comes in at the expensive end.

> A ladder of four rungs, outline to deck, each a little more expensive; the notes pile up at the top.

## Act 2: The pipeline

### B3. Check where it's cheap - 0:35
**So check each decision where it's cheapest to change.**

That's the whole idea. Split the work into stages. End each one with something short the author
can check in a few minutes. The story, on one page. The words, read aloud. The pictures, as rough
grey boxes. Agents do the work. The author decides, and nothing moves on until they do.

> The ladder turns on its side and becomes a row of stages, each with a tick.

### B4. One sentence, every stage - 1:10
**Follow one sentence through the pipeline, and it changes form at every stage.**

Here's a sentence from a talk about a cache. The slowest waits halve once the cache is warm. It
starts in the source, as a result. The digest copies it out, with where it came from. In the
outline, it's one beat with a time budget. In the script, it's the line the speaker has to say. In
the storyboard, it becomes a frame. A headline, the words that fire the click, and what's said
while it's up. In the greybox, it's a page of rough boxes. Only then does anyone render it.

**Each form takes a minute to read, and each is where one kind of mistake is cheapest to catch.**

> The sentence travels along the row of stages and changes form at each one.

### B5. One source file - 0:40
**The storyboard is the one source file. The script and the deck are both made from it.**

Every click of the talk is one entry. Its headline, its trigger words, its narration. The script
you rehearse is printed from it. The speaker notes come from it too. And a scene has to play
exactly the clicks it lists, or the build stops. So the words you rehearse are the words on screen.

> One file in the middle; the script and the deck come out of it.

### B6. A late note goes home - 1:05
**A late note goes back to the earliest stage it changes, and everything after it is rebuilt.**

Say a reviewer writes, slide seven, say halves, not forty-eight percent. Slide seven is just the
number on the screen. The agent looks up which frame that was, in the draft the reviewer saw. Beat
three, frame two. Then it says the note back, with its stage. This one's a script note. The author
confirms. The fix goes into the storyboard, not into the scene. The script and the deck are made
again, and only what changed comes back for a look.

**The note lands where it belongs, so it costs a sentence again.**

> The note travels from slide 7 back along the row to the script stage, then forward again.

## Act 3: Using it

### B7. Using it - 0:35
**Clone the repository, write only in the talk folder, and point any agent at the agents file.**

The instructions are plain text, so any coding agent can follow them. One command checks your
machine. One builds the deck, and it works offline. Your talk lives in one folder, so updates to
the pipeline never touch it. And a shorter cut of the same talk keeps only what's different.

> The repository as folders; the talk folder lights up.

### B8. This slide was a grey box - 0:40
**This talk was made this way. This slide started as a grey box.**

Brief, digest, outline, script, storyboard, greybox. Then the render. Each stage checked before
the next. That's how a late note goes back to costing a sentence.

**Build a talk the way you build software. In stages, each checked cheaply by its author, from one
source file.**

> This slide's own greybox frame turns into this slide.
