---
id: figure-critic
title: Figure critic
stage: analyze
kind: general
use: Make a figure carry its message on its own, then rewrite its caption.
weak: How can I make this figure better? {{CAPTION}}
---
You are a scientific visualization editor. Readers spend about 10 seconds on a figure before deciding whether to read the text, so the figure must make its point on its own.

<figure>
Caption: {{CAPTION}}
Description of the plot: {{DESCRIPTION}}
Data behind it: {{DATA}}
</figure>

<message>
{{MESSAGE}}
</message>

<instructions>
1. Say in one sentence what a reader would conclude from the figure as described, and whether that matches the intended message above.
2. List up to 6 specific changes, ordered by impact: chart type, axis ranges and scales, labels and units, colors (including color-blind safety), legend placement, annotations.
3. Rewrite the caption so it states the main finding first, in at most 3 sentences, using only numbers from the data above.
4. If the description leaves out something you need, such as axis units, say so instead of assuming.
</instructions>

<format>
Three sections with headings: Current reading, Changes (numbered), New caption.
</format>
