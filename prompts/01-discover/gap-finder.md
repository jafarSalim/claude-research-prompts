---
id: gap-finder
title: Research gap finder
stage: discover
kind: general
use: Find thesis-sized gaps in your reading notes, each backed by a quote.
weak: What are some research gaps in {{FIELD}}? Give me good ideas for my thesis.
---
You are a research strategist in {{FIELD}}. I am choosing a thesis topic, and a gap that has already been filled would cost me months, so evidence matters more than creativity here.

<notes>
{{NOTES}}
</notes>

<instructions>
1. From the reading notes above, list 5 to 8 candidate research gaps. Use these gap types: untested condition, missing comparison, conflicting results, unrealistic assumption, missing dataset.
2. For each gap, quote the note that reveals it and cite the paper key in square brackets. Cite only papers that appear in the notes.
3. Rate each gap from 1 to 5 on novelty, feasibility for one student in 12 months, and impact, with one sentence of reasoning per rating.
4. Separate what the notes state from your inference: write "The notes show..." for evidence and "I infer..." for interpretation.
5. My notes cover only part of the literature, so for each gap write one search query I should run to check that nobody has filled it yet.
6. If the notes are too thin to support a gap, say so.
</instructions>

<format>
A table: Gap | Type | Evidence (quote + key) | Novelty | Feasibility | Impact | Check query. Then the top 2 gaps with 3 sentences each.
</format>
