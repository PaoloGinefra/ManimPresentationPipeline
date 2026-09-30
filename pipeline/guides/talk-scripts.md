---
name: talk-scripts
description: Method and house style for writing any spoken talk script (defence, lab talk, conference talk, job talk). Covers the principles that decide what goes in, the outline-first workflow, the spine-line script format, the rules for writing for the ear instead of the eye, the read-aloud revision loop, and the expand-then-compress rule. Use whenever drafting, restructuring, rewriting or reviewing a presentation script, planning a talk's structure, or turning a read-aloud transcript into edits.
---

# Talk scripts

A talk is **acted, not read**. Every rule here follows from two facts: the listener gets one
pass and cannot go back, and the speaker has to be able to say the words out loud.

Before writing a line, fix three things with the speaker: **who is in the room**, **how long
the slot is** (and whether questions are inside it), and **the one sentence they should be
able to repeat afterwards**. Everything else is subordinate to that sentence. In the pipeline
these live in the brief (stage 0).

## Principles that decide what goes in

- **One big idea, promised early, paid at the end.** A talk is borrowed attention; spend it on
  the single claim the work stands or falls on, and subordinate every other result to it.
  (Peyton Jones, *How to give a great research talk*.)
- **Problem and stakes before any mechanism.** Roughly the first fifth of the time carries
  motivation with no method detail in it.
- **And, But, Therefore, not And, And, And.** A list of true statements is not a story. Each
  section needs a tension: what we wanted, what blocked it, what follows. (Olson, *Houston, We
  Have a Narrative*.)
- **Dig for the conflict.** Name what failed, what surprised you, what is still unexplained.
  Audiences remember conflict and resolution; they do not remember a list of findings.
- **Adapt to this audience, and maximise signal-to-noise.** Cut every sentence that does not
  advance the argument. (Doumont, *Trees, Maps, and Theorems*.)
- **Effective redundancy.** Say each key idea three times in different shapes: name it, unpack
  it, then show a consequence or an example. Preview the findings, show them, restate them.
  Budget roughly **one new idea per 20 to 30 seconds**; denser than that and listeners fall
  off and never rejoin.
- **Every slide answers "so what?"** Slide titles are claims, not topics: "the cache halves the
  slowest waits", not "latency results". (Doumont; Alley's assertion-evidence format: a
  sentence headline plus one figure, minimal text.)
- **Cycling.** About a fifth of any room is elsewhere at any moment, so the central claim is
  said at least three times, in different words, at different points.
- **Verbal punctuation.** Fixed spoken landmarks ("that is the problem; here is the idea") give
  a listener who drifted a place to get back on.
- **Near-miss comparisons.** Define a hard concept against the thing it is almost: a median
  against a mean, a virus against a bacterium. (Winston, *How to Speak*.)
- **State limitations before you are asked.** In a defence especially, naming the strongest
  weakness yourself reads as command of the work; evasion reads as the opposite. Say your own
  role plainly too.
- **Close by answering the opening promise.** The last line maps onto the first, and it is the
  sentence you want quoted.

Common failure modes, in the order they occur: reciting facts with no tension; slides as a
crutch; assuming subfield vocabulary; cramming every result and rushing the ending; and going
defensive about limitations.

## Workflow

1. **Brief** (stage 0). Audience, slot length, whether questions are inside it, pace class, the
   one sentence, and what must *not* be said (held for questions).
2. **Outline, one page, before any prose** (stage 2). First brainstorm small options for the
   hook, thread, peaks, structure and close; then consolidate into 15 to 25 beats. One row each:

   | ID | type | spine line (one sentence that must be said) | support (a few clauses) | time |

   `type` is `setup`, `obstacle`, `payoff`, `turn` or `PEAK`. Above the table, name the
   **thread** (the example that will return), the **three peaks**, and the list of what is cut
   and held for questions. The story either works here or it does not, and fixing it here costs
   five minutes instead of an hour.
3. **Prose, one section per beat** (stage 3), in the format below.
4. **Read-aloud loop.** The speaker reads an act aloud and sends notes, a recording or a
   transcript. A transcript is the highest-signal input available:
   - where they unpacked a sentence, the script was too dense: split it;
   - where they re-said a line their own way, adopt their words verbatim;
   - where they said "I don't like this", cut it without negotiating;
   - where they added an example or a caveat, it belongs in the script;
   - where they stumbled on a word, replace the word.
5. **Expand, then compress.** Keep adding while the story is still settling; report the running
   total in one clause at most and do not propose cuts. When the speaker calls the compression
   pass, cut at **beat level** from the outline, with them, rather than quietly tightening
   prose. A talk that has to lose a third of its length loses beats, not adjectives.

## Script format

One `###` section per beat, headed by its stable ID and a time budget so `mpp script` can read it:

```markdown
### B6. Why the queue forms - 1:15
**The bold line is the spine: the one sentence that must be said, more or less as written.**

Support, in speakable prose. The speaker improvises around this on the day.

> A visual note. Not spoken.
```

A beat carries a second spine line when it makes two moves; peaks usually do. Keep alternate
takes in the file under headings with no time budget, so nothing good is lost.

From stage 4 on, the same text lives in the storyboard's `narration` fields (spine lines stay in
`**bold**`), and this file is generated from it.

## Story rules

- **One thread, and make it return.** Pick one concrete example and bring it back so that it
  does different work each time: motivating the idea, making an argument concrete, being
  measured in the results, closing the talk. An example that appears once is decoration.
- **Every section ends on the question the next one answers**, and the next one opens by naming
  it. Sections that start fresh read as separate documents stapled together.
- **Three peaks; everything else quieter.** A peak gets its own slide and 1:00 to 1:15. Valleys
  get 30 to 45 seconds. If everything is emphasised, nothing is.
- **One framing at a time.** Two indexes over the same material (say "two payoffs" and "three
  questions") force the listener to hold both, and they never line up. Keep the one that
  carries the message; delete the other.
- **Never re-use labels across sections.** If the theory has a "second question", the empirical
  part must not.
- **One list per section, three items maximum.** Nested triples are unfollowable by ear; put the
  rest on the slide.
- **Announce what you promise, and pay it.** Plant callbacks explicitly ("we will meet this
  again") and collect them.
- **Concrete before abstract.** The plain sentence first, then "formally, that takes three
  clauses".
- **Motivate, don't assert.** "The natural fix is a cache" is an assertion. "Most requests repeat
  one we answered a minute ago, so keep the answer" is an argument. Whenever a line states a
  choice, ask what makes it the natural one and say that first.

## Writing for the ear, not the eye

- One idea per sentence. Eight to fifteen words. Verb early. Fragments are fine.
- No colons, semicolons or appositives doing logical work: a listener cannot hear them. Say
  "here is the first thing" instead.
- Contractions throughout. Written-out formality is audible and stiff.
- Expand every acronym aloud on first use, even a familiar one.
- Numbers: spoken as words, rounded, at most about three per section.
- No symbols in the mouth. Say "the error", "the average wait", never their notation. Notation
  belongs on the slide.
- Replace any word the speaker would not say naturally, and any word that is awkward to
  pronounce.
- Signpost transitions out loud; the audience cannot see your section headings.
- Read every new paragraph as if speaking it. If you run out of breath, it is two sentences.

## Accuracy

- **Keep neighbouring claims separate.** If the method is faster on large inputs but uses more
  memory on all of them, say exactly that. Merging them into "it scales better" is the one thing
  a careful listener can check and find wrong.
- **One-sentence qualification where it arises**, full version held for questions.
- **Verify every number against the most reliable source** (the digest records which) before it
  enters the script, and round only in the safe direction ("within two points", not "within one
  and a half").
- **Flag anything that comes from working notes rather than the written document**, so the
  speaker knows which numbers are not in it.
- **Check historical or anecdotal openings against a primary source.** Someone in the room may
  know the story better than the speaker does.

## Timing

- Plan at the brief's **pace class**: slow 120, normal 135, fast 150 words per minute. Fifteen
  minutes at normal pace is roughly 2,000 words.
- Budget per beat, and make the budgets sum to the slot. Run `uv run mpp script` after every
  editing pass.
- Leave **30 to 60 seconds of slack per results section** so peaks' figures can be read in
  silence.
- Budget question stops as their own zero-word beats, so the total stays honest.
- Expect the first full draft to run 1.5 to 2x the slot. That is the expansion phase working,
  not a failure.
