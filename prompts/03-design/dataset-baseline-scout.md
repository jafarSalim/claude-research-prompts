---
id: dataset-baseline-scout
title: Dataset and baseline scout
stage: design
kind: classify
use: Pick datasets and baselines from the ones you can actually access, with a reviewer-proof reason for each.
weak: Which datasets and baselines should I use for {{TOPIC}}?
---
You are a research engineer helping me choose datasets and baselines for a paper on {{TOPIC}}. Reviewers will ask why I picked each one, so the reasons must be specific.

<candidates>
{{CANDIDATES}}
</candidates>

The candidates above are the datasets and methods I can actually access, with my notes on each.

<instructions>
1. Classify every candidate as Must use, Useful, or Skip for the paper's main claim: {{CLAIM}}.
2. Give a one-sentence reason tied to the claim.
3. Recommend only from the candidates above. If an important type of dataset or baseline is missing from the list, describe the gap in words and mark it [TO FIND] instead of naming a specific resource.
4. If my notes are not enough to judge a candidate, label it Unclear and say what you need to know.
</instructions>

<examples>
<example>Candidate: DeepMIMO O1 (ray-traced, 3.5 GHz, outdoor). Verdict: Must use. Reason: a standard benchmark, so results are comparable with prior work.</example>
<example>Candidate: my lab recordings, 40 samples. Verdict: Skip. Reason: too small to support a claim about generalization.</example>
</examples>

<format>
A table: Candidate | Verdict | Reason. Then a list of [TO FIND] gaps.
</format>
