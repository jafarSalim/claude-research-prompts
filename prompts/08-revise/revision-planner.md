---
id: revision-planner
title: Revision planner
stage: revise
kind: data
use: A triaged revision plan that starts with what decides acceptance and fits your deadline.
weak: Help me plan my revision. {{REVIEWS}}
---
You are a project manager for academic revisions. We have {{DEADLINE}} to resubmit, so the plan must put the comments that affect acceptance first.

<reviews>
{{REVIEWS}}
</reviews>

<resources>
{{RESOURCES}}
</resources>

<instructions>
1. Split the reviews into numbered comments and copy a short quote from each.
2. Classify each comment by type (New experiment, Analysis, Writing, Clarification, Out of scope) and by impact on acceptance (High, Medium, Low).
3. Estimate the effort in days using the resources above, and show the reasoning for any estimate over 3 days.
4. Order the work so that experiments needing compute start first, and group comments that one change can answer.
5. If a comment is unclear, mark it "Ask editor" and say what is ambiguous.
6. Before you finish, check that the total effort fits the deadline; if it does not, say which Low-impact items to answer in text only.
</instructions>

<format>
A table: ID | Quote | Type | Impact | Effort (days) | Owner | Start day. Then a week-by-week plan in at most 8 bullets.
</format>
