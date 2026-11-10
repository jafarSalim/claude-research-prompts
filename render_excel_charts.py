"""Exports the workbook's sheets and native Excel charts as PNG images for the README (needs LibreOffice)."""
from xlkit.neon import render

PAGES = {"Dashboard": "overview.png", "Library": "library.png", "Checks Strong": "checks_strong.png", "Checks Weak": "checks_weak.png",
         "Chart Scores": "scores.png", "Chart Stages": "stages_chart.png", "Chart Radar": "radar.png", "Chart Anatomy": "anatomy.png",
         "Chart Anatomy Stage": "anatomy_by_stage.png", "Chart Bubble": "bubble.png", "Chart Cost": "cost_curve.png",
         "Chart Project": "project_cost.png", "Chart Overhead": "overhead.png"}
for n in render("excel/claude_research_prompts.xlsx", PAGES, "results"):
    print(n, "->", PAGES[n])
