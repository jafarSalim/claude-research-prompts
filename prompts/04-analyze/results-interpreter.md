---
id: results-interpreter
title: Results interpreter
stage: analyze
kind: data
use: Check every claim against your numbers before reviewers do.
weak: Do my results support my claims? {{RESULTS}} {{CLAIMS}}
---
You are a co-author checking our results section before we write the discussion. Overclaiming is the most common reason papers in our field get rejected, so be strict.

<results>
{{RESULTS}}
</results>

<claims>
{{CLAIMS}}
</claims>

<instructions>
1. For each claim, decide whether the results above Support it, Partly support it, or Fail to support it. Quote the exact numbers you used.
2. Check the arithmetic: recompute every difference, ratio and percentage the claims mention.
3. Flag gaps that weaken a claim: a single seed, overlapping error bars, a missing baseline, a test set that is too small.
4. Rewrite each claim so it says exactly what the numbers show, and keep the observed result separate from your interpretation of why it happened.
5. If a value needed to judge a claim is missing, say so instead of estimating it.
6. Before you finish, check every number in your answer against the results.
</instructions>

<format>
A table: Claim | Verdict | Numbers used | Problem. Then the rewritten claims as a numbered list, each at most 2 sentences.
</format>
