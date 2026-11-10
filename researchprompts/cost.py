"""API cost of asking several prompts about the same paper, with and without prompt caching.

Prices in USD per million tokens. Source: https://platform.claude.com/docs/en/about-claude/pricing
(retrieved 2026-11-09). Columns: input, 5-minute cache write, 1-hour cache write, cache read, output.
Batch API: 50% off everything. Check the source before relying on these numbers.
"""
PRICES = {
    "Claude Sonnet 5.5": (2, 2.50, 4, 0.10, 10),
    "Claude Opus 5.5": (4, 5, 8, 0.20, 20),
    "Claude Haiku 5.5": (0.10, 0.125, 0.20, 0.01, 0.50),
}
BATCH = 0.5
MIN_CACHE = 512  # smallest cacheable prefix for these models, in tokens


def session_cost(model, paper, prompt, output, k, layout):
    """Cost of k prompts about one paper.

    paper, prompt, output: tokens per call (prompt = the template around the paper).
    layout: 'paper_last'  -> the paper sits after instructions that change, so nothing can be cached
            'paper_first' -> the paper is the identical first block, cached on call 1, read on calls 2..k
            'batch'       -> paper_last through the Batch API
            'batch_cache' -> paper_first through the Batch API (batch cache hits are best effort)
    """
    inp, w5, _, rd, out = PRICES[model]
    if layout in ("paper_last", "batch"):
        c = k * ((paper + prompt) * inp + output * out)
    else:
        if paper < MIN_CACHE:
            return session_cost(model, paper, prompt, output, k, "batch" if layout == "batch_cache" else "paper_last")
        c = paper * w5 + (k - 1) * paper * rd + k * (prompt * inp + output * out)
    return c / 1e6 * (BATCH if layout.startswith("batch") else 1)
