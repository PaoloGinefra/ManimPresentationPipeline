# Stage 1: Digest

Collect everything the talk could say, each item with where it comes from.

## Input

The approved brief and everything in `talk/source/`.

## Source order

Use the most reliable source available, in this order:

1. raw data and results;
2. the analysis code;
3. the written document (paper, report, thesis);
4. notes and summaries.

When two sources disagree, flag it to the author. Never resolve it silently. The written document
stays the reference for how a claim is worded.

## Steps

1. Read the source. Where data or code is available, check the document's numbers against it.
2. List, each with its source (file and place):
   - **claims**, stated as sentences;
   - **numbers** that back them, with uncertainty where it exists;
   - **figures** that could be reused;
   - **terms** and how the source defines them;
   - **limits** the source states or that you find;
   - **gaps**: what the talk would need that the source does not give;
   - **disagreements** between sources.
3. Suggest a first sort: must, could, leave out. Base it on the brief's one sentence.
4. Write `1-digest/digest.md`.

## Checkpoint

`digest.md`. The author marks each item must / could / leave out, and answers the gaps and the
disagreements.

## Done when

Every item is sorted and every gap and disagreement has an answer. Tag `global/digest-1`.
