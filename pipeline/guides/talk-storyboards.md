---
name: talk-storyboards
description: Method and principles for the visual design and storyboarding of a spoken talk that will be built as an animation (manim, manim-slides) rather than as static slides. Covers the evidence base (Mayer, Alley, Tversky, Heer and Robertson, Zongker and Salesin, Doumont, Duarte, film and comics grammar, 3Blue1Brown), the stages (skeleton, storyboard, greybox, design system, build), continuity and transition rules, how to stage equations and results, and the skeleton and storyboard formats. Use whenever turning a talk script or outline into visuals, reviewing a storyboard, choosing how a figure or equation should appear, or handing a scene to a manim implementer.
---

# Talk storyboards

A storyboard decides **what the audience looks at, second by second, while the speaker
talks**. It sits between the script (what is said, from `talk-scripts.md`) and the manim build
(how pixels move). Its output is not pictures for their own sake; it is a sequence of frames
and transitions that the implementer can build without asking what anything is for.

Two facts drive every rule below. The audience has **one visual channel and one verbal
channel, both small**, and whatever the screen does competes with the speaker unless it says
the same thing at the same moment. And an animation is **a claim about structure**: whatever
moves, persists, or morphs is read as meaningful, whether or not you meant it.

## The evidence base, distilled

**Cognitive load (Mayer, multimedia learning).** Five rules, each replicated:
- *Coherence*: cut every element that is not needed for the claim. Decoration costs recall.
- *Signalling*: cue the organisation (highlight, arrow, colour change) so the eye knows where to go.
- *Redundancy*: narration plus picture beats narration plus picture plus the same words on
  screen. **Never put on screen what the speaker is saying.** Text on screen is for what must
  persist after the words are gone: a headline claim, a label, a symbol.
- *Spatial contiguity*: a label sits on the thing it names, not in a legend.
- *Temporal contiguity*: the thing appears **when** it is named, not a click before or after.
- Plus *segmenting* (a complex build in presenter-paced steps) and *pre-training* (name and
  show a concept's parts before the mechanism that uses them).

**Assertion-evidence (Alley).** Each frame is one claim stated as a sentence (at most two
lines) plus visual evidence for it, never a topic title plus bullets. Controlled studies show
better comprehension and recall at the same spoken words. Doumont adds: **one message per
slide, one slide per message**; the headline goes where the eye starts (top left).

**Glance test (Duarte).** A held frame must be graspable in about three seconds. If it takes
reading, the audience reads instead of listening.

**When animation helps (Tversky, Morrison and Betrancourt).** Two conditions, both needed:
- *Congruence*: change over time on screen must correspond to something that actually
  changes, flows or causes in the idea. A process, a transformation, an optimisation, a
  sequence of steps. A static fact does not earn motion.
- *Apprehension*: the motion must be slow and simple enough to be perceived correctly. Most
  failed animations fail here: too fast, too many simultaneous changes.

**Animated transitions (Heer and Robertson).** Keep every intermediate frame a *valid*
picture; never morph an object into an unrelated one (false object constancy, it asserts a
relation that does not exist); give different semantic operations visibly different
transitions; group things that change together (common fate); avoid occlusion; use
slow-in slow-out easing; **stage** complex changes into simple sequential ones; about **one
second** per transition, faster for small moves.

**Animated presentations (Zongker and Salesin, SIGGRAPH talks built in a scripted system,
the direct ancestor of a manim talk).**
- *Make all movement meaningful.* Classical character-animation tricks (squash, stretch,
  exaggeration) turn diagrams into characters and pull attention off the speaker. Economy of
  motion wins.
- *Separate the attention cue from the action.* Flag where something is about to happen
  with a colour change or arrow, something that cannot be mistaken for the event itself.
- *Avoid hard cuts inside a section*; even a short fade keeps continuity and lets attention
  move between screen and speaker.
- *Transition size tracks semantic distance.* Quiet transitions inside a section, one big
  move between sections, so the visuals punctuate the talk the way the voice does.
- *Large virtual canvas.* Something that slides off screen stays in the mind's eye; memory
  for location supports memory for content. Pan and zoom rather than blink.
- *Expand and compress detail smoothly*; zoom into the active part, zoom back for context.
- *Manage complexity by layers*: overlay detail when needed, remove it after.
- *Do one thing at a time*, and *reinforce animation with narration*: the speaker describes
  what is moving while it moves. To make a point that is not illustrated, **stop the motion**;
  stillness returns attention to the speaker.
- *Parameterise*: build a figure as a model with a few meaningful controls (a load, a
  threshold, a time step) and animate the controls, not the pieces.

**Graphics perception (Kosslyn's eight principles; Tufte).** Relevance, appropriate
knowledge, salience, discriminability, perceptual organisation, compatibility, informative
changes, capacity limits. The most common violations in real talks are relevance and
discriminability. From Tufte: erase non-data ink; for comparisons, **small multiples** on
shared axes beat a crowded single plot. From Knaflic: grey everything, then colour the one
thing the claim is about (preattentive attributes: colour, size, position).

**Film and comics grammar.**
- *Establishing shot*: show the whole space before any close-up, and return to it when the
  audience may be lost.
- *Screen direction (the 180-degree rule)*: keep consistent sides. If "ours" enters on the
  left, it lives on the left for the whole talk; time and progress flow left to right.
- *Continuity*: track every recurring object's position, colour and state across frames.
- *Panel transitions (McCloud)*: moment-to-moment (continuous morph of one object),
  action-to-action (key steps of a process), subject-to-subject (move within one idea),
  scene-to-scene (new place or act), aspect-to-aspect (a tour of one figure). Name the one
  each cut uses; the audience performs *closure* across it, so the gap must be closable.
- *Thumbnails first, animatic before production* (Pixar story reels): cheap rough frames,
  timed against the voice, redrawn many times before anything is built. In the pipeline this
  is the greybox.

**Math exposition (3Blue1Brown, and manim's own purpose).** Concrete before abstract; put
the visual first and let the explanation form around it; an equation arrives **after** its
symbols have been seen as objects, and each symbol carries the colour of the object it
names; aim for the audience to feel they could have invented it.

**Story shape (Duarte, Peyton Jones).** Alternate *what is* and *what could be*; give each
peak one *STAR moment* (something they'll always remember), a single image that could be
described to a colleague afterwards; examples before the general case.

## The rules

1. **The script owns meaning; the storyboard owns attention.** Every frame answers: which
   spoken clause is this for, and where is the eye at that instant? A visual with no clause
   is cut; a clause that needs a picture and has none is flagged back to the script stage.
2. **One claim per frame, and the frame states it.** The headline is the spine line of the
   beat (or its compressed form), a full sentence, at most two lines. Topic titles are not
   allowed.
3. **Motion only where the idea moves** (congruence). Each animation carries a one-line
   justification of what real change it depicts. "Fade in" needs none; a morph does.
4. **One change at a time, synchronised to one clause.** If two things must change, stage
   them. A beat's build is a list of frames, each tied to the words that trigger it.
5. **Every held frame is a finished slide.** Presenter pauses, questions and a restart after
   a stumble all land on hold frames, so each must pass the glance test on its own.
6. **Persist, do not replace.** A recurring object (the running example, the key figure, the
   progress tracker) is the *same mobject* across beats, moved and transformed, never
   redrawn from scratch. Morph only between things that really are the same thing.
7. **Transition magnitude equals semantic distance.** Within a beat: fades and small moves.
   Between beats in an act: pan on the canvas. Between acts: one deliberate, larger move
   (zoom out to the map, a wipe) and nothing else that dramatic anywhere.
8. **Words on screen are labels and claims, never transcript.** No bullets. Text that is also
   being spoken is deleted (redundancy).
9. **Colour is semantic and global.** Each colour means one thing for the whole talk (ours,
   baseline, the running example, a highlighted term). Everything else is neutral grey. Fix
   the roles in the skeleton and the colours once, in the design system.
10. **Peaks get a signature image, designed first.** Each PEAK beat has one visual that
    carries it; earlier beats *plant* its parts and later beats *call back* to it.
11. **Results: evidence builds before the claim lands.** Axes, then what is measured, then
    the baseline, then ours; highlight the gap; only then the headline sentence appears.
    Every metric carries its direction (up or down arrow).
12. **Equations are earned.** Picture first, then symbols attached to picture parts in their
    colours, then the equation assembles from those symbols (`TransformMatchingTex`-style),
    one term at a time. An unexplained symbol never sits on screen.

## Stages, in order

Each is reviewable in one sitting and cheaper to change than the next, so arguments happen as
early as they can.

1. **Skeleton** (stage 4b, text only). What each beat shows and how the beats connect.
2. **Storyboard** (stage 4b, frames). Each beat expanded into frames keyed to trigger words.
3. **Greybox** (stage 4b). Every frame as rough grey boxes with its real headline and
   narration: the animatic, reviewable without rendering anything.
4. **Design system** (stage 5, look). Palette, typography, screen regions, motion timing.
5. **Build** (stage 6, manim). Built from the storyboard, styled by the design system.

What separates the skeleton from the design system: anything that is **story logic** is fixed
in the skeleton even when it sounds visual. That covers the recurring objects and their roles,
continuity between beats, colour *roles* (ours, baseline, the running example; not the colours),
and transition *weight* (act break or step inside an act). Anything that is **appearance** waits
for the design system: hex values, fonts, backgrounds, easing.

### Skeleton format

Above the table: the one sentence, the thread, the peaks and their key images, the
**cast** (each recurring object, its role, its verbs, the beats it appears in), the
**canvas** (where each act lives, so movement between acts is spatial), the colour roles,
and the **interaction policy** (the rules below, plus any exception this talk makes).

One row per beat:

| field | content |
|---|---|
| headline | the claim on screen, one sentence |
| visual idea | what the audience sees, one sentence of words, no styling |
| in / out | what it inherits from the previous beat, what it hands on |
| transition | weight of the cut into it: step, move, act break |
| role | setup / obstacle / payoff / turn / PEAK, with the key image named on peaks |
| asset | exists (which figure or scene), adapt, or new |
| time | from the outline |

### Design system

- **Palette**: colour for each role fixed in the skeleton, plus the neutral set. Checked
  for colour-blind safety and projector contrast.
- **Screen grammar**: fixed regions (headline top left; the persistent progress element;
  where "ours" and "baseline" sit); type sizes readable from the back row; safe margins.
- **Transition vocabulary**: the concrete transition bound to each weight (e.g. fade =
  step, pan = move, zoom out to the map = act break, transform = the same object changing).
- **Look of the cast**: how each recurring object is drawn, once, for every beat.

## Interaction: when the presenter clicks

Policy is fixed in the skeleton, click placement in the storyboard, the code at build.

1. **One click, one change.** Each click starts exactly one segment, which ends on a finished
   hold frame (Mayer's segmenting: presenter-paced beats system-paced).
2. **The speaker leads, the screen follows.** Every click sits on a spoken trigger phrase, so
   the thing appears as it is named (temporal contiguity). Spine lines are natural clicks.
3. **No timed auto-advance.** Pre-timed animation outruns or lags the live speaker. A segment
   may chain internally (AUTO) only when it depicts one continuous process.
4. **No idle loops.** Motion on a held frame pulls attention off the speaker; stillness hands
   it back. Question stops rest on a still frame.
5. **Act transitions are one click each**; the zoom or move runs to the next hold frame.
6. **Every click is reversible.** Stepping back one segment lands on a valid frame.
7. **Backup material is hidden segments** reachable from the question stops, placed where
   it belongs in the talk's structure.
8. **Clicks are marked in the script** at their exact word, so they are rehearsed with it.
   The generated script shows every click cue.
9. **Every slide shows a plain number** in a fixed corner, so an audience member can name a
   slide in a question and a reviewer can cite one in notes. Stable IDs (`B3.2`) stay
   internal; `../feedback.md` converts between them.

## Building for reuse

A deck built for one script should serve the next one (a defence, a conference cut, a lab
talk) by changing the sequence, not the animation code. Four layers, each reusable to a
different degree:

| layer | content | reusable | fixed in |
|---|---|---|---|
| **Design tokens** | colour roles and values, type sizes, motion timing, transition per weight | fully | stage 5 |
| **Components** | the cast as parameterised objects, each with a small set of **verbs** (appear, highlight, tick, open, zoom-into) | yes | stages 5, 6 |
| **Beat scenes** | thin compositions of components, one per beat, named by beat ID | when two talks share a beat | stage 6 |
| **The talk** | which beats, in what order, with which clicks | no: this is what a variant changes | the storyboard's `order` |

Consequences for the earlier stages: the skeleton's cast table lists each component's verbs,
and storyboard notes are written as component verbs, so the storyboard doubles as the
assembly spec. **A component earns parameters only when two beats or two talks use it**;
everything else stays a one-off scene. Data plots take their numbers from files, never from
literals in scene code, so a rerun updates the talk.

## Storyboard format

The storyboard is `4-visual/storyboard.toml`, the talk's single source of text. One table per
beat, one `frame` entry per click, in the order given by `order`:

```toml
[B7]
title = "PEAK 2: the cache warms itself"
act = 2
kind = "peak"            # beat, peak or stop
budget_s = 70
note = """
Transition in: move, same act. Carried in: the timeline and the request stream (from B5).
Carried out: the timeline, now showing short waits. STAR: the slow tail of the histogram
collapsing."""

[[B7.frame]]
head = "Most requests repeat one answered a minute ago."
trigger = "the same request comes back"
narration = """
**Most of what arrives, we have already answered.** The same request comes back again and
again."""
boxes = ["request stream @ left", "repeats highlighted @ left"]
note = "`stream.highlight(repeats)`. HOLD."

[[B7.frame]]
head = "The cache fills itself while the system runs."
trigger = "nobody fills it by hand"
narration = "..."
boxes = ["request stream @ left", "cache @ right"]
note = "`cache.fill(stream)`. Why motion: the cache really fills over time. HOLD."

[[B7.frame]]
head = "The slowest waits halve once the cache is warm."
trigger = "look at the slowest requests"
narration = "..."
boxes = ["wait histogram @ center"]
note = "`histogram.morph(before, after)`: the same histogram changing. Lower is better. HOLD."
```

Beat fields: `title`, `act`, `kind`, `budget_s`, and a `note` with the transition in, what is
carried in and out, and the STAR image on peaks. Frame fields:

- `head`: the headline on screen;
- `trigger`: the spoken words that fire the click;
- `narration`: what is said on this frame, spine lines in `**bold**`; it becomes the script
  and the speaker notes;
- `boxes` (optional): the rough layout, a list of `"label @ region"`; the region is one of
  `top-left`, `top`, `top-right`, `left`, `center`, `right`, `bottom-left`, `bottom`,
  `bottom-right`, the area under the headline split three by three. `mpp greybox` draws each as
  a labelled grey box;
- `note`: for the builder: component verbs where a component exists, prose where it does not,
  a *why motion* line for any non-trivial animation, and HOLD or AUTO at the end.

A frame that continues without a click is marked AUTO and must depict one continuous process.

## Workflow

**Skeleton**
1. **Read the brief, outline and script**, in that order. Note the one sentence, the
   thread, the peaks and the time budget. Do not start drawing from the script prose.
2. **Inventory the assets**: every existing figure in the source, and which beat could use it.
3. **Design the peaks first.** Name the key image for each peak, then trace backwards which
   earlier beats must plant its parts and which later beats call back to it.
4. **Cast and canvas.** The recurring objects, their roles and beats; where each act lives.
5. **One row per beat** in the skeleton format. Check it reads as a story with the sound off
   (headlines plus visual ideas alone should carry the argument; the assertion-evidence test).
6. **Continuity check.** For each recurring object, beat by beat: present or not, and what
   state it is in. Every change needs a transition that explains it. Remove orphans.

**Storyboard and greybox**
7. **Build pass.** Expand each beat into frames: one click per frame keyed to its trigger
   words, a HOLD at its end, component verbs, why-motion notes. One change per frame.
8. **Timing pass.** Run `uv run mpp script` for times at the pace class. A frame with less than
   about two seconds of narration is merged; one held for more than about thirty seconds
   without change needs a new frame or cutting.
9. **Critique pass.** Run the checklist below; flag to the author any beat whose words and
   picture cannot be made to say the same thing. That is a script problem, not a visual one.
10. **Greybox.** Give every frame its `boxes` and run `uv run mpp greybox`: one standalone HTML
    page with every frame as labelled grey boxes, its number, ID, headline and narration, for
    the author to review.

**Design system** (stage 5). Fix the look for every role and object the skeleton and storyboard
use, and nothing more.

**Build** (stage 6). The storyboard plus the design system are the spec for the manim build.

## Review checklist

- Does every frame have a sentence headline that is a claim, and does the frame show evidence for it?
- Does every hold frame pass the three-second glance test?
- Is any on-screen text a copy of what is being said? Delete it.
- Does each motion depict a real change (congruence) and is it slow and single enough to follow (apprehension)?
- Does anything change without being named at that moment (temporal contiguity)?
- Does any morph connect two things that are not the same thing?
- Are colours and screen sides consistent with the design system from first beat to last?
- Is there exactly one big transition per act break, and only there?
- Does each peak have its STAR image, planted earlier and called back later?
- Does every result frame build the evidence before the claim, with metric direction shown?
- Does every equation arrive after its symbols were seen as picture parts?

## Failure modes

Decoration that asserts meaning (things bouncing, morphing, spinning for energy); animation
that runs while the speaker talks about something else; slides as the speaker's notes;
hard cuts between states of one figure; a new visual style per section; results tables read
aloud; equations dropped in whole; everything highlighted, so nothing is; building a scene
in manim before its greybox frame was approved.

## Sources

- R. E. Mayer, *Multimedia Learning*; Cambridge Handbook of Multimedia Learning, ch. 12.
- M. Alley, *The Craft of Scientific Presentations*; Garner and Alley, assertion-evidence studies.
- J.-l. Doumont, *Trees, Maps, and Theorems*; "Creating effective slides".
- N. Duarte, *slide:ology*, *Resonate*, *DataStory*; "Do your slides pass the glance test?" (HBR 2012).
- B. Tversky, J. B. Morrison, M. Betrancourt, "Animation: can it facilitate?" IJHCS 2002.
- J. Heer, G. Robertson, "Animated Transitions in Statistical Data Graphics", InfoVis 2007.
- D. Zongker, D. Salesin, "On Creating Animated Presentations", SCA 2003.
- S. M. Kosslyn, *Clear and to the Point*; *Graph Design for the Eye and Mind*.
- E. Tufte, *The Visual Display of Quantitative Information*; C. N. Knaflic, *Storytelling with Data*.
- G. Reynolds, *Presentation Zen*; S. Peyton Jones, "How to give a great research talk".
- S. McCloud, *Understanding Comics*; film continuity editing (establishing shot, 180-degree rule); Pixar story reels.
- G. Sanderson (3Blue1Brown), Summer of Math Exposition guidance.
