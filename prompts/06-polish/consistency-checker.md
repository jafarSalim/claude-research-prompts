---
id: consistency-checker
title: Consistency checker
stage: polish
kind: extract
use: Catch numbers, terms and units that disagree across your manuscript.
weak: Check my paper for mistakes.\n\n{{MANUSCRIPT}}
---
You are a meticulous technical proofreader. Numbers that disagree between the abstract, the text and the tables are a common reason for desk rejection, so I need every mismatch found.

<manuscript>
{{MANUSCRIPT}}
</manuscript>

<instructions>
Check the manuscript above for:
1. Numbers that appear more than once with different values (abstract, results, tables, conclusion).
2. Terms, symbols and abbreviations used in two different ways, or used before they are defined.
3. Figures and tables that are referenced but missing, or present but never referenced.
4. Units that change for the same quantity.

For each finding, quote both locations word for word with their section names. Report only mismatches you can quote from the manuscript; when two values may differ on purpose (for example, different test sets), list them as "Check" rather than "Error".
Before you finish, go through the abstract and conclusion once more and confirm each of their numbers appears in the results.
</instructions>

<format>
A table: Type | Location A (quote) | Location B (quote) | Severity (Error or Check). Then the count of each type.
</format>
