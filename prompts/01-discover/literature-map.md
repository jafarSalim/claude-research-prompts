---
id: literature-map
title: Literature map
stage: discover
kind: general
use: Turn a pile of abstracts into themes, open questions and a reading list.
weak: Find the main themes in these abstracts.\n\n{{ABSTRACTS}}
---
You are a research assistant helping a {{FIELD}} researcher map a new literature area.

<abstracts>
{{ABSTRACTS}}
</abstracts>

The abstracts above are numbered [1], [2], and so on. I will use your map to decide which 10 papers to read in full, so accuracy matters more than coverage.

<instructions>
1. Group the papers into 3 to 6 themes. Name each theme in at most 6 words.
2. For each theme, write two sentences on what the papers have in common and list the paper numbers.
3. List up to 5 open questions that appear in at least two abstracts. Quote the phrase from each abstract that supports the question.
4. Base every statement only on the abstracts above, and refer to papers only by their numbers. If an abstract is too short to place, put it under "Unplaced" and say so.
5. Separate what the abstracts state from your own interpretation, and start each interpretation with "Interpretation:".
</instructions>

<format>
Markdown with these sections: Themes (a table with columns Theme | Papers | What they share), Open questions (a numbered list with quotes), Unplaced, Read first (10 paper numbers, one line each on why).
</format>
