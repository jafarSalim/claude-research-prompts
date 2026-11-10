---
id: rebuttal-tone
title: Rebuttal tone fixer
stage: revise
kind: style
use: Turn a defensive reply into a polite, confident one without losing a single point.
weak: Make this reply sound more polite: {{DRAFT_REPLY}}
---
You are an editor who specializes in reviewer correspondence. My draft reply below is accurate but sounds defensive, and the editor will read the tone as closely as the content.

<draft_reply>
{{DRAFT_REPLY}}
</draft_reply>

<reviewer_comment>
{{COMMENT}}
</reviewer_comment>

<instructions>
Rewrite the reply so it is polite, confident and short.
- Keep every technical point, number and citation from my draft; preserve the meaning exactly.
- Acknowledge what is valid in the comment in one sentence before answering.
- Replace emotional words ("clearly", "obviously", "misunderstood") with evidence from the draft.
- Keep the length between 80% and 120% of the draft.
- If my draft concedes something it should defend, or argues something the evidence in the draft cannot support, point it out after the rewrite.
</instructions>

<example>
Draft: "The reviewer clearly misunderstood our method. We already explained this in Section 3."
Rewrite: "Thank you for raising this point; our description in Section 3 was too brief. We have expanded it to explain ..."
</example>

<format>
The rewritten reply, then at most 3 bullets of notes on content issues.
</format>
