"""Scores every prompt (weak and strong), measures its parts in tokens, and models the API cost
of a literature review. Writes results/analysis.json, which build_excel.py turns into charts."""
import json, statistics as st
from researchprompts import load, STAGES
from researchprompts.research_lint import full_check, ALL_RULES, RESEARCH_RULES
from researchprompts.lint import RULES as BASE_RULES
from researchprompts.anatomy import anatomy, PARTS
from researchprompts.tokens import count
from researchprompts.cost import session_cost, PRICES

PAPER, OUTPUT = 12_000, 1_000          # assumed tokens in one paper and in one answer
PAPERS, PER_PAPER = 40, 6              # assumed literature review: 40 papers, 6 prompts each

rows = []
for p in load():
    rs, g, r, c = full_check(p.template, p.stage, p.kind)
    rw, gw, ww, cw = full_check(p.weak, p.stage, p.kind)
    rows.append(dict(id=p.id, title=p.title, stage=p.stage, kind=p.kind, fields=len(p.fields), doc_fields=len(p.doc_fields),
                     rules_strong=rs, rules_weak=rw, general_strong=g, general_weak=gw, research_strong=r, research_weak=ww,
                     combined_strong=c, combined_weak=cw, tokens_strong=count(p.template), tokens_weak=count(p.weak),
                     anatomy=anatomy(p.template)))

stages = []
for s in STAGES:
    rr = [x for x in rows if x["stage"] == s]
    stages.append(dict(stage=s, n=len(rr), **{k: st.mean(x[k] for x in rr) for k in
                  ("combined_weak", "combined_strong", "general_weak", "general_strong", "research_weak", "research_strong", "tokens_strong")},
                  anatomy={part: st.mean(x["anatomy"][part] for x in rr) for part in PARTS}))

pass_rate = {}
for rule in ALL_RULES:
    for side in ("weak", "strong"):
        vals = [x[f"rules_{side}"][rule.key] for x in rows if x[f"rules_{side}"][rule.key] is not None]
        pass_rate[f"{rule.key}_{side}"] = 100 * sum(vals) / len(vals) if vals else None

read_like = [x["tokens_strong"] for x in rows if x["stage"] in ("read", "analyze")]
prompt_tok = round(st.mean(read_like))
curves = {m: {lay: [session_cost(m, PAPER, prompt_tok, OUTPUT, k, lay) for k in range(1, 13)]
              for lay in ("paper_last", "paper_first", "batch", "batch_cache")} for m in ("Claude Sonnet 5.5", "Claude Opus 5.5")}
project = {m: {lay: PAPERS * session_cost(m, PAPER, prompt_tok, OUTPUT, PER_PAPER, lay)
               for lay in ("paper_last", "paper_first", "batch", "batch_cache")} for m in PRICES}

summary = dict(
    prompts=len(rows), stages=len(STAGES), rules=len(ALL_RULES),
    combined_weak=st.mean(x["combined_weak"] for x in rows), combined_strong=st.mean(x["combined_strong"] for x in rows),
    general_weak=st.mean(x["general_weak"] for x in rows), general_strong=st.mean(x["general_strong"] for x in rows),
    research_weak=st.mean(x["research_weak"] for x in rows), research_strong=st.mean(x["research_strong"] for x in rows),
    tokens_weak=st.mean(x["tokens_weak"] for x in rows), tokens_strong=st.mean(x["tokens_strong"] for x in rows),
    perfect=sum(x["combined_strong"] == 100 for x in rows),
    prompt_tokens_read=prompt_tok,
    overhead_pct=100 * (st.mean(x["tokens_strong"] for x in rows) - st.mean(x["tokens_weak"] for x in rows)) / PAPER,
    project_saving_pct=100 * (1 - project["Claude Sonnet 5.5"]["paper_first"] / project["Claude Sonnet 5.5"]["paper_last"]),
)
json.dump(dict(assumptions=dict(paper_tokens=PAPER, output_tokens=OUTPUT, papers=PAPERS, prompts_per_paper=PER_PAPER,
                                tokenizer="Llama 4 tokenizer as a stand-in; Claude counts differ"),
               rules=[dict(key=r.key, name=r.name, weight=r.weight, source=r.source, research=r in RESEARCH_RULES) for r in ALL_RULES],
               parts=PARTS, rows=rows, stages=stages, pass_rate=pass_rate, curves=curves, project=project, summary=summary),
          open("results/analysis.json", "w"), indent=1)
for k, v in summary.items():
    print(f"{k:22} {v:.2f}" if isinstance(v, float) else f"{k:22} {v}")
print({m: {k: round(v, 2) for k, v in d.items()} for m, d in project.items()})
