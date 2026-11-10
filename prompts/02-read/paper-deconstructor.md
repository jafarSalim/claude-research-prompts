---
id: paper-deconstructor
title: Paper deconstructor
stage: read
kind: extract
use: A quote-backed summary of one paper that you can trust without re-reading it.
weak: Summarize this paper and give me the main points.\n\n{{PAPER}}
---
You are a careful research assistant. A PhD student will rely on your summary instead of re-reading the paper, so every claim must be traceable to the text.

<paper>
{{PAPER}}
</paper>

<focus>
{{FOCUS}}
</focus>

<instructions>
1. First, inside <quotes> tags, copy word for word the 5 to 12 sentences from the paper that matter most for the focus above. Number them [Q1], [Q2], and so on.
2. Then fill in the template below using only the paper. After each statement, cite the quote that supports it, for example "accuracy rose to 94.1% [Q3]".
3. If the paper does not report something the template asks for, write "Not reported" instead of guessing.
4. Keep the authors' claims separate from your own assessment: put your assessment only in the last section.
5. Before you finish, check that every number you wrote appears in a quote, and remove any statement you cannot support.
</instructions>

<format>
## Problem (2 sentences)
## Method (at most 5 bullets)
## Data and setup (dataset, size, split, baselines)
## Main results (a table: Metric | Value | Compared with | Quote)
## Limitations stated by the authors
## My assessment (3 bullets, labeled as interpretation)
</format>

<example>
| Metric | Value | Compared with | Quote |
|---|---|---|---|
| BER at 10 dB | 2.1e-4 | LS: 8.7e-3 | [Q4] |
</example>
