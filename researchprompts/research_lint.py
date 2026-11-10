"""Six research checks on top of the 11 general rules in lint.py.

They follow Anthropic's guide to reducing hallucinations (allow "I don't know", ground the
answer in direct quotes, verify with citations, restrict the answer to the documents given)
and the habits reviewers expect: keep the author's meaning, keep evidence apart from opinion.
https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations

Like lint.py, this is a checklist: it shows what a prompt asks for, not how well the model
follows it. Test prompts on your own papers.
"""
import re
from .lint import Rule, check as base_check, score as base_score, RULES as BASE_RULES
from .library import FIELD, DOC_FIELDS

GROUND = r"\b(use only|using only|only (the|from|on|that|facts|numbers|methods|problems|mismatches|what)|based? (every|each|the|your)[^.\n]{0,40}\bonly\b|judge only|report only|recommend only|only from)\b"
QUOTE = r"\bquot(e|es|ing)\b|word for word|exact numbers|copy numbers exactly|point to in the code"
UNSURE = r"not reported|not stated|i don't know|say so|unclear|cannot tell|instead of (guessing|assuming|estimating|inventing)|\[missing|\[verify\]|\[to find\]|\[action needed|needs check|ask me|unverified|cannot see"
CITE = r"cite the quote|cite only|only cite|citing only|refer to papers only|\[citation needed\]|\[verify\]|unverified|by their (numbers|keys)"
VOICE = r"(keep|keeping|preserve)[^.\n]{0,60}(voice|meaning|terminology|claims|wording|technical point)|without changing"
SEPARATE = r"(separate|apart|distinguish)[^.\n]{0,80}(interpret|opinion|assessment|inference|speculat)|(opinion|interpretation|assessment)[^.\n]{0,30}(separate|apart) from"

RESEARCH_RULES = [
    Rule("grounding", "Limits the answer to your material", 2, "Restrict to the provided documents"),
    Rule("quotes", "Asks for quotes or exact numbers as evidence", 2, "Use direct quotes for factual grounding"),
    Rule("unsure", "Allows 'not reported' or 'I don't know'", 2, "Allow Claude to say I don't know"),
    Rule("citations", "Keeps citations to sources you gave", 2, "Verify with citations"),
    Rule("voice", "Protects your meaning, terms and voice", 1, "Academic editing practice"),
    Rule("separate", "Keeps evidence apart from interpretation", 1, "Peer review practice"),
]
ALL_RULES = BASE_RULES + RESEARCH_RULES


def research_check(text, stage, kind):
    low = text.lower()
    has_doc = any(f in DOC_FIELDS for f in FIELD.findall(text))
    r = {}
    r["grounding"] = bool(re.search(GROUND, low)) if has_doc else None
    r["quotes"] = bool(re.search(QUOTE, low)) if has_doc and kind != "style" else None  # rewriting tasks need no quotes
    r["unsure"] = bool(re.search(UNSURE, low))
    r["citations"] = bool(re.search(CITE, low)) if stage in ("discover", "read", "write", "submit") else None
    r["voice"] = bool(re.search(VOICE, low)) if kind == "style" else None
    r["separate"] = bool(re.search(SEPARATE, low)) if stage in ("discover", "read", "analyze") else None
    return r


def weighted(result, rules):
    num = sum(x.weight for x in rules if result.get(x.key) is True)
    den = sum(x.weight for x in rules if result.get(x.key) is not None)
    return 100 * num / den if den else 0.0


def full_check(text, stage, kind):
    """Returns (rule results, general score, research score, combined score)."""
    r = {**base_check(text, kind), **research_check(text, stage, kind)}
    return r, base_score(r), weighted(r, RESEARCH_RULES), weighted(r, ALL_RULES)


RESEARCH_ADVICE = {
    "grounding": "Say 'use only the paper above' so the answer cannot drift into memory.",
    "quotes": "Ask for word-for-word quotes or exact numbers behind each claim.",
    "unsure": "Give an exit: 'If the paper does not report it, write Not reported'.",
    "citations": "Allow citations only from your list, and mark the rest [CITATION NEEDED].",
    "voice": "Tell the editor to keep your claims, numbers and terminology.",
    "separate": "Ask for evidence and interpretation in separate, labeled parts.",
}
