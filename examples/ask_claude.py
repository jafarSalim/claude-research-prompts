"""Ask several research prompts about one paper with prompt caching (Anthropic Python SDK).

    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python examples/ask_claude.py examples/sample_paper.txt

The paper block goes first and carries cache_control, so call 1 writes it to the cache and
calls 2..k read it at a fraction of the input price. Papers shorter than the minimum
cacheable size (512 tokens for the Claude 5.5 models) are simply not cached.
"""
import pathlib, sys
import anthropic
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from researchprompts import get

paper = pathlib.Path(sys.argv[1]).read_text(encoding="utf8")
client = anthropic.Anthropic()
jobs = [("paper-deconstructor", {"FOCUS": "the main method and its results"}),
        ("critical-appraisal", {"FIELD": "wireless communications"})]
for pid, values in jobs:
    shared, rest = get(pid).cache_layout({"PAPER": paper, **values})
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": shared, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": rest},
        ]}],
    )
    u = msg.usage
    print(f"\n===== {pid} =====\n{msg.content[0].text}")
    print(f"[tokens] input {u.input_tokens}, cache write {u.cache_creation_input_tokens}, cache read {u.cache_read_input_tokens}, output {u.output_tokens}")
