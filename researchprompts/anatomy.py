"""Splits a prompt template into parts and counts the tokens in each."""
import re
from .tokens import count

PARTS = ["Role and purpose", "Your material", "Instructions", "Context notes", "Output format", "Examples"]
TOP = re.compile(r"^<(\w+)[^>]*>\n([\s\S]*?)^</\1>\s*$", re.M)


def anatomy(template):
    out = dict.fromkeys(PARTS, 0)
    pos, first = 0, True
    for m in TOP.finditer(template):
        gap = template[pos:m.start()].strip()
        if gap:
            out["Role and purpose" if first else "Context notes"] += count(gap)
        first = False
        tag, body = m.group(1), m.group(2)
        n = count(m.group(0))
        if tag in ("instructions",):
            out["Instructions"] += n
        elif tag == "format":
            out["Output format"] += n
        elif tag in ("example", "examples"):
            out["Examples"] += n
        elif re.fullmatch(r"\s*(\{\{[A-Z_]+\}\}\s*)+|[\s\S]*\{\{[A-Z_]+\}\}[\s\S]*", body) and len(re.sub(r"\{\{[A-Z_]+\}\}|\w+:", "", body).strip()) < 60:
            out["Your material"] += n
        else:
            out["Context notes"] += n
        pos = m.end()
    tail = template[pos:].strip()
    if tail:
        out["Context notes"] += count(tail)
    return out
