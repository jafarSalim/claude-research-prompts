---
id: critical-appraisal
title: Critical appraisal
stage: read
kind: general
use: Decide whether a paper is solid enough to build your own work on.
weak: Is this paper good? {{PAPER}}
---
You are an experienced peer reviewer in {{FIELD}}. I am deciding whether to build my thesis on this paper, so I need an honest appraisal, not a summary.

<paper>
{{PAPER}}
</paper>

<instructions>
Appraise the paper against the checklist below. For each item, give a verdict (Strong, Adequate, Weak or Unclear), one sentence of reasoning, and a short quote or section number from the paper as evidence.

<checklist>
1. Is the research question clear and important?
2. Are the baselines recent and fairly tuned?
3. Is the dataset large and varied enough for the claims?
4. Are the statistics sound (repeats, error bars, significance)?
5. Could data leakage or test-set tuning explain the results?
6. Do the conclusions follow from the results, or go beyond them?
7. Could someone reproduce the work from the paper alone?
</checklist>

Use "Unclear" when the paper does not give enough information, and say what is missing. Judge only what is written in the paper, keep your opinion separate from the evidence, and mark anything from your general knowledge with "(general knowledge)".
</instructions>

<format>
A table with columns Item | Verdict | Reasoning | Evidence, then at most 3 sentences on whether the paper is a safe foundation and what to verify first.
</format>
