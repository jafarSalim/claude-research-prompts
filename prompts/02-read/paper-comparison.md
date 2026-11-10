---
id: paper-comparison
title: Paper comparison matrix
stage: read
kind: extract
use: One table that compares many papers field by field, with nothing filled from memory.
weak: Compare these papers in a table.\n\n{{PAPERS}}
---
You are a research assistant building a comparison table for a literature review chapter.

<papers>
{{PAPERS}}
</papers>

Each paper above is wrapped in <paper id="..."> tags.

<fields>
{{FIELDS}}
</fields>

<instructions>
1. Extract the fields listed above from every paper, using only that paper's text.
2. Write "Not reported" when a paper does not state a field. Never fill a cell from memory or from another paper.
3. Copy numbers exactly as written, with units.
4. After the table, write 3 to 5 sentences that compare the papers, citing only the paper ids in square brackets. Keep observations (what the table shows) apart from interpretation (what it might mean), and label the interpretation.
5. Before you finish, re-read each row and check every cell against its paper.
</instructions>

<format>
A markdown table with one row per paper and one column per field, then the comparison paragraph.
</format>

<example>
Fields: Task, Dataset, Best metric
| Paper | Task | Dataset | Best metric |
|---|---|---|---|
| [P2] | Channel estimation | DeepMIMO O1 | NMSE −24.3 dB |
</example>
