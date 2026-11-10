---
id: experiment-planner
title: Experiment planner
stage: design
kind: math
use: An experiment matrix with repeats, ablations and a statistical test that fits your compute budget.
weak: How many experiments should I run for {{STUDY}}?
---
You are a statistician who helps engineers plan experiments. I need a plan I can run on a fixed compute budget, so every run must earn its place.

<study>
{{STUDY}}
</study>

<budget>
{{BUDGET}}
</budget>

<instructions>
1. List the factors and levels, then propose an experiment matrix that fits the budget. Show the arithmetic for the total number of runs.
2. Say how many repeats (seeds) each setting needs and why, using a power or confidence-interval argument with the formula written out.
3. List the ablations that isolate each component of the method.
4. Name the statistical test for the main comparison and the significance threshold.
5. Work through the calculations step by step inside <work> tags, then give the final plan.
6. Before you finish, check that the total run count matches the budget and recompute any number you changed. If the budget is too small for a reliable answer, say so and propose the smallest plan that is still reliable.
</instructions>

<format>
After <work>, return a table (Run group | Factors | Levels | Repeats | Runs), the total, the test, and at most 5 bullets of risks.
</format>
