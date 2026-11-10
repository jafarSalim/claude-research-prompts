import subprocess, sys, pytest
from researchprompts import load, get, STAGES
from researchprompts.research_lint import full_check
from researchprompts.cost import session_cost


def test_library_shape():
    ps = load()
    assert len(ps) == 24 and len({p.id for p in ps}) == 24
    assert all(sum(p.stage == s for p in ps) == 3 for s in STAGES)


def test_fill_needs_every_field():
    p = get("paper-deconstructor")
    with pytest.raises(KeyError):
        p.fill({"PAPER": "text"})
    out = p.fill({"PAPER": "PAPER BODY", "FOCUS": "noise"})
    assert "{{" not in out and "PAPER BODY" in out


def test_cache_layout_puts_the_paper_first():
    shared, rest = get("critical-appraisal").cache_layout({"PAPER": "BODY", "FIELD": "optics"})
    assert shared == "<paper>\nBODY\n</paper>" and "BODY" not in rest and rest.startswith("You are")
    shared2, _ = get("paper-deconstructor").cache_layout({"PAPER": "BODY", "FOCUS": "x"})
    assert shared == shared2  # identical prefix, so the cache can hit across prompts


@pytest.mark.parametrize("p", load(), ids=lambda p: p.id)
def test_strong_beats_weak(p):
    strong = full_check(p.template, p.stage, p.kind)[3]
    weak = full_check(p.weak, p.stage, p.kind)[3]
    assert strong >= 70 and strong - weak >= 50


def test_linter_catches_missing_exit():
    r = full_check("Summarize this paper.\n{{PAPER}}", "read", "general")[0]
    assert r["unsure"] is False and r["grounding"] is False and r["role"] is False


def test_cost_model():
    a = dict(model="Claude Sonnet 5.5", paper=12_000, prompt=270, output=1_000)
    assert session_cost(**a, k=1, layout="paper_first") > session_cost(**a, k=1, layout="paper_last")  # cache write costs extra once
    assert session_cost(**a, k=2, layout="paper_first") < session_cost(**a, k=2, layout="paper_last")  # and pays back on call 2
    assert session_cost(**a, k=6, layout="batch") == pytest.approx(0.5 * session_cost(**a, k=6, layout="paper_last"))
    # hand check, k = 1, paper last: (12,270 x $2 + 1,000 x $10) / 1e6
    assert session_cost(**a, k=1, layout="paper_last") == pytest.approx((12_270 * 2 + 1_000 * 10) / 1e6)


def test_cli_runs(tmp_path):
    f = tmp_path / "p.txt"; f.write_text("Summarize {{PAPER}}")
    out = subprocess.run([sys.executable, "-m", "researchprompts", "lint", str(f)], capture_output=True, text=True, check=True).stdout
    assert "Research score 0/100" in out
