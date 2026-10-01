# Digest

The source is this repository; paths are relative to its root. Each item has a sort: **must**,
**could** or **leave out**. Where a document describes what the code does, the code was checked.

## Claims

| # | claim | source | sort |
|---|---|---|---|
| C1 | A source becomes a script and an animated deck through fixed stages; agents do the work and the author steers. | `DESIGN.md` Goal | must |
| C2 | Every stage ends with something short for the author to approve. | `pipeline/principles.md` principle 1 | must |
| C3 | Each decision is checked where it is cheapest: story on a one-page outline, words by reading aloud, visuals on rough boxes, fixes on stills. Render only when needed. | `pipeline/principles.md` principle 3 | must |
| C4 | The storyboard holds every slide's text and narration; the script and the deck are generated from it. | `pipeline/principles.md` principle 5; `engine/mpp/script.py`, `engine/mpp/beat.py` | must |
| C5 | A note belongs to the earliest stage it changes; it is fixed there and everything after it is regenerated, never patched downstream. | `pipeline/feedback.md` | must |
| C6 | Each note is repeated back with its slide number, stable ID and stage before anything changes. | `pipeline/feedback.md` The loop | must |
| C7 | Slides show plain numbers; stable IDs (B3.2) are internal; the numbering is recomputed from the storyboard at any commit. | `pipeline/feedback.md`; `engine/mpp/storyboard.py`, `engine/mpp/project.py` | must |
| C8 | Drafts are rendered small and carry their build commit; finals are full quality. | `engine/mpp/build.py` | could |
| C9 | A beat's scene must play exactly the clicks its storyboard lists, or the build fails. | `engine/mpp/beat.py` `tear_down` | could |
| C10 | The greybox is every frame as rough grey boxes on one standalone page, generated from the storyboard. | `engine/mpp/greybox.py` | must |
| C11 | The author's content lives only in `talk/`; the pipeline is cloned and the engine is shared. | `DESIGN.md` Repository | must |
| C12 | Builds work offline: the font and reveal.js are in the repository. | `vendor/README.md`; `engine/mpp/build.py` | could |
| C13 | Instructions are plain Markdown, so any agent can follow them; `AGENTS.md` is the entry point. | `AGENTS.md` | could |
| C14 | Variants hold only what differs from the main talk. | `pipeline/variants.md` | could |
| C15 | The build checks every click for text over text and text off the frame, and every seam between slides for a jump. | `engine/mpp/lint.py`, `engine/mpp/checks.py` | leave out (backup) |
| C16 | Only changed beats are rendered again. | `engine/mpp/build.py` | leave out |
| C17 | Brief: the author answers who is in the room, the slot and pace, the one sentence, and what is held back. | `pipeline/stages/0-brief.md` Questions | must |
| C18 | Digest: the author sorts every item must / could / leave out, and answers every gap and disagreement. | `pipeline/stages/1-digest.md` Checkpoint, Done when | must |
| C19 | Outline: the author picks per decision among small options, then approves the story on one page. | `pipeline/stages/2-outline.md` | must |
| C20 | Script: the author reads every act aloud, and the total must fit the slot. | `pipeline/stages/3-script.md` Done when | must |
| C21 | Visual: the author picks per beat, then approves the greybox. | `pipeline/stages/4-visual.md` | must |
| C22 | Design: the author approves the specimen, one page. | `pipeline/stages/5-design.md` | must |
| C23 | Build: the author approves stills of every slide, then each act in a click-through. | `pipeline/stages/6-build.md` | must |
| C24 | Rehearsal (optional): reviewers' notes are traced to their stages; the author approves the plan. | `pipeline/stages/7-rehearsal.md` | must |
| C25 | Final: the release is refused while a stage is unapproved or a note is open; the author approves the release. | `pipeline/stages/8-final.md`; `engine/mpp/cli.py` `cmd_release` | must |

## Numbers

| # | number | backs claim | source | sort |
|---|---|---|---|---|
| N1 | 9 stages, 0 (brief) to 8 (final); 7 is optional | C1 | `pipeline/principles.md` Stages | must |
| N2 | pace classes: 120, 135, 150 words per minute | C3 | `pipeline/principles.md` | could |
| N3 | drafts 720p at 24 frames per second; finals 1080p at 30 | C8 | `engine/mpp/build.py` `QUALITY` | could |
| N4 | the template talk builds from a fresh clone in about 12 seconds | C11 | working notes, measured once on one machine | leave out: in no document |

The talk's running example, a talk about a cache, is invented to illustrate the stages: its brief,
claims and sentence are not results of anything.

## Figures

None exist. Every visual is new, drawn in the default house style.

## Terms

| term | definition in the source | source |
|---|---|---|
| beat | one idea of the talk; a scene in the build | `pipeline/guides/talk-scripts.md` |
| frame | one click: a headline, the words that trigger it, its narration | `pipeline/guides/talk-storyboards.md` |
| checkpoint | the standalone file a stage ends with, for the author to approve | `pipeline/principles.md` |
| storyboard | `4-visual/storyboard.toml`, the talk's single source of text | `pipeline/guides/talk-storyboards.md` |
| greybox | every frame as rough grey boxes, on one page | `pipeline/stages/4-visual.md` |
| stable ID | `B3.2`: beat 3, frame 2 | `pipeline/feedback.md` |

## Limits

| # | limit | source |
|---|---|---|
| L1 | Scenes are Python: the build stage needs someone, or an agent, who can write manim. | `pipeline/stages/6-build.md` |
| L2 | This example is the pipeline's first complete run: there is no record yet of other authors using it. | working notes |

## Gaps

| # | gap | author's answer |
|---|---|---|
| G1 | No measurement of time saved against a conventional workflow. | Claim none. Say where each kind of change is cheapest, not how much time is saved. |

## Disagreements

None found: the documents describe what the code does.
