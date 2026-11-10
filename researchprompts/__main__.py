"""Command line:

  python -m researchprompts list                       all prompts by stage
  python -m researchprompts show paper-deconstructor   the full template and its fields
  python -m researchprompts fill paper-deconstructor --file PAPER=paper.txt --set FOCUS="the noise model"
  python -m researchprompts lint my_prompt.txt --stage read --kind extract
"""
import argparse, pathlib, sys
from .library import load, get, STAGES
from .research_lint import full_check, ALL_RULES, RESEARCH_ADVICE
from .lint import ADVICE


def main(argv=None):
    ap = argparse.ArgumentParser(prog="researchprompts", description="Research prompts for Claude")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    s = sub.add_parser("show"); s.add_argument("id")
    f = sub.add_parser("fill"); f.add_argument("id")
    f.add_argument("--set", action="append", default=[], metavar="FIELD=text")
    f.add_argument("--file", action="append", default=[], metavar="FIELD=path")
    f.add_argument("--cache-layout", action="store_true", help="print the shared paper block first, for prompt caching")
    f.add_argument("-o", "--out")
    l = sub.add_parser("lint"); l.add_argument("file")
    l.add_argument("--stage", default="read", choices=STAGES)
    l.add_argument("--kind", default="general", choices=["general", "classify", "extract", "format", "style", "math", "code", "data"])
    a = ap.parse_args(argv)

    if a.cmd == "list":
        for st in STAGES:
            print(f"\n{st.upper()}")
            for p in load():
                if p.stage == st:
                    print(f"  {p.id:<26} {p.use}")
    elif a.cmd == "show":
        p = get(a.id)
        print(f"# {p.title} ({p.stage})\nFields: {', '.join(p.fields)}\n\n{p.template}")
    elif a.cmd == "fill":
        p = get(a.id)
        vals = dict(x.split("=", 1) for x in a.set)
        vals.update({k: pathlib.Path(v).read_text(encoding="utf8").strip() for k, v in (x.split("=", 1) for x in a.file)})
        if a.cache_layout:
            shared, rest = p.cache_layout(vals)
            text = f"{shared}\n\n=== put cache_control on the block above; the part below changes per prompt ===\n\n{rest}"
        else:
            text = p.fill(vals)
        if a.out:
            pathlib.Path(a.out).write_text(text, encoding="utf8"); print("wrote", a.out)
        else:
            print(text)
    elif a.cmd == "lint":
        text = pathlib.Path(a.file).read_text(encoding="utf8")
        r, g, rs, c = full_check(text, a.stage, a.kind)
        print(f"General score {g:.0f}/100 | Research score {rs:.0f}/100 | Combined {c:.0f}/100\n")
        for rule in ALL_RULES:
            v = r[rule.key]
            mark = "n/a " if v is None else ("PASS" if v else "FIX ")
            print(f"  [{mark}] {rule.name}")
            if v is False:
                print(f"         -> {ADVICE.get(rule.key) or RESEARCH_ADVICE[rule.key]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
