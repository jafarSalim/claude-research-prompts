---
id: related-work-synthesizer
title: Related work synthesizer
stage: write
kind: style
use: Turn reading notes into a related-work section that synthesizes instead of listing.
weak: Write a related work section using these papers.\n\n{{NOTES}}
---
You are a senior researcher helping me turn reading notes into a related-work section. Reviewers penalize sections that list papers one by one, so the goal is synthesis: grouping, contrasting, and leading to our gap.

<notes>
{{NOTES}}
</notes>

<our_work>
{{OUR_WORK}}
</our_work>

<instructions>
1. Group the papers in the notes into 2 to 4 themes.
2. For each theme, write one paragraph (at most 150 words) that states the shared idea, contrasts the approaches, and names the limitation that matters for our work.
3. End with one paragraph that positions our work against the themes, keeping our description as written, without changing its claims.
4. Cite only the papers in the notes, by their keys in square brackets. Base every statement on the notes only; if a note is too thin to support a statement, mark it [VERIFY].
5. Keep what the papers report separate from your interpretation of trends, and phrase interpretations as such, for example "taken together, these results suggest ...".
</instructions>

<format>
Markdown with a short heading per theme, then the positioning paragraph. After the text, a table: Key | Theme | Used for.
</format>
