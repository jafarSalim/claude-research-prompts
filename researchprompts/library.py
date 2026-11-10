"""Loads the prompt files in prompts/ and fills their {{FIELDS}}."""
import pathlib, re
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parents[1] / "prompts"
FIELD = re.compile(r"\{\{([A-Z_]+)\}\}")
STAGES = ["discover", "read", "design", "analyze", "write", "polish", "submit", "revise"]
# Fields that hold your own material (papers, drafts, data), not short settings
DOC_FIELDS = {"PAPER", "PAPERS", "ABSTRACTS", "ABSTRACT", "NOTES", "DRAFT", "TEXT", "MANUSCRIPT", "RESULTS", "CLAIMS",
              "CODE", "REVIEWS", "CHANGES", "CANDIDATES", "DATA", "GUIDELINES", "DRAFT_REPLY", "SOURCES", "DETAILS"}


@dataclass
class Prompt:
    id: str
    title: str
    stage: str
    kind: str
    use: str
    weak: str
    template: str
    path: pathlib.Path = field(repr=False, default=None)

    @property
    def fields(self):
        return list(dict.fromkeys(FIELD.findall(self.template)))

    @property
    def doc_fields(self):
        return [f for f in self.fields if f in DOC_FIELDS]

    def fill(self, values, strict=True):
        """Replaces every {{FIELD}}. With strict=True, a missing value raises KeyError."""
        missing = [f for f in self.fields if f not in values]
        if strict and missing:
            raise KeyError("missing values for: " + ", ".join(missing))
        return FIELD.sub(lambda m: str(values.get(m.group(1), m.group(0))), self.template)

    def cache_layout(self, values):
        """Splits the filled prompt into (shared, rest) for prompt caching.

        Caching matches an identical prefix, so when you ask several prompts about the same
        paper, the paper block must come first and be byte-identical every time. The first
        material block moves to the front; everything else follows unchanged.
        """
        text = self.template
        for f in self.doc_fields:
            m = re.search(r"<(\w+)>\s*\{\{" + f + r"\}\}\s*</\1>\n*", text)
            if m:
                shared = FIELD.sub(lambda x: str(values[x.group(1)]), m.group(0)).strip()
                rest = (text[:m.start()] + text[m.end():]).strip()
                tmp = Prompt(**{**self.__dict__, "template": rest})
                return shared, tmp.fill(values)
        return "", self.fill(values)


def _parse(path):
    raw = path.read_text(encoding="utf8")
    _, head, body = raw.split("---\n", 2)
    meta = dict(l.split(": ", 1) for l in head.strip().splitlines())
    return Prompt(id=meta["id"], title=meta["title"], stage=meta["stage"], kind=meta["kind"], use=meta["use"],
                  weak=meta["weak"].replace("\\n", "\n"), template=body.strip() + "\n", path=path)


def load():
    """All prompts, in stage order then file order."""
    ps = [_parse(p) for p in sorted(ROOT.glob("*/*.md"))]
    return sorted(ps, key=lambda p: (STAGES.index(p.stage), str(p.path)))


def get(pid):
    for p in load():
        if p.id == pid:
            return p
    raise KeyError(f"no prompt called {pid!r}; run 'python -m researchprompts list'")
