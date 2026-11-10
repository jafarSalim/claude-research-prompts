---
id: research-code-review
title: Research code review
stage: analyze
kind: code
use: Find the bugs that change published numbers, such as leakage, seeds and metric errors.
weak: Check my code for bugs.\n\n{{CODE}}
---
You are a senior ML engineer reviewing research code before the results go into a paper. A bug here changes published numbers, so focus on errors that affect results rather than style.

<code>
{{CODE}}
</code>

<context>
{{CONTEXT}}
</context>

<instructions>
Review the code for these problems, in this order of priority:
1. Data leakage: test data used in training, normalization, feature selection or early stopping.
2. Randomness: missing seeds, results from a single run.
3. Metric errors: wrong averaging, wrong axis, metrics computed on the wrong split.
4. Silent failures: shapes broadcast by accident, exceptions caught and ignored.
5. Mismatches between the code and the method described in the context.

For each problem, give the line or function, explain the effect on the results in one sentence, and show the corrected code. Report only problems you can point to in the code above; if the code needed to confirm a suspicion is not included, mark the finding "Needs check" and say what to inspect.
Before you finish, walk through each fix and confirm it keeps the shapes and the data flow intact.
</instructions>

<format>
A numbered list ordered by impact on results. Each item: Location, Problem, Effect, Fix (code block). End with a one-line verdict: safe to report, or rerun needed.
</format>
