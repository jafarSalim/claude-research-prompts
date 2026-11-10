"""Builds excel/claude_research_prompts.xlsx: the check matrices with live score formulas,
a live cost model, and native Excel charts in a dark neon style."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.chart import BarChart, LineChart, RadarChart, DoughnutChart, PieChart, BubbleChart, Reference, Series
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.utils import get_column_letter as L
from xlkit.neon import BG, PLOT, GRID, TEXT, MUTED, WEAK, STRONG, GOLD, STAGE, NEON, dark, paint, labels, chart_sheet, page, axis_title

A = json.load(open("results/analysis.json", encoding="utf8"))
ROWS, RULES, PARTS, STAGES = A["rows"], A["rules"], A["parts"], A["stages"]
NP, NR = len(ROWS), len(RULES)
wb = Workbook(); wb.remove(wb.active)
DARK, CARD = PatternFill("solid", fgColor=BG), PatternFill("solid", fgColor=PLOT)
F = lambda color=TEXT, size=11, bold=False, italic=False: Font(name="Calibri", color=color, size=size, bold=bold, italic=italic)
INPUT = F("7DF9FF")  # inputs you can change, in cyan
edge = Side(style="thin", color=GRID)
BOX = Border(edge, edge, edge, edge)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def darken(ws, rows, cols):
    ws.sheet_view.showGridLines = False
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            ws.cell(r, c).fill = DARK
            if ws.cell(r, c).font.color is None or ws.cell(r, c).value is None:
                ws.cell(r, c).font = F()


def head(ws, row, names, widths, col=1, fill="2B2256"):
    for i, n in enumerate(names):
        c = ws.cell(row, col + i, n)
        c.fill, c.font, c.alignment, c.border = PatternFill("solid", fgColor=fill), F(GOLD, 11, True), CENTER, BOX
    for i, w in enumerate(widths):
        ws.column_dimensions[L(col + i)].width = w


# ---------- Check matrices: 1 = pass, 0 = fix, blank = not applicable ----------
for side in ("Strong", "Weak"):
    ws = wb.create_sheet(f"Checks {side}")
    darken(ws, NR + 6, NP + 2)
    ws["A1"] = f"17 checks on every {side.lower()} prompt   ✓ pass   ✗ fix   blank = not applicable"
    ws["A1"].font = F(STRONG if side == "Strong" else WEAK, 16, True)
    head(ws, 2, ["Check", "Weight"] + [r["id"] for r in ROWS], [40, 8] + [6.2] * NP)
    ws.row_dimensions[2].height = 150
    for j in range(3, 3 + NP):
        ws.cell(2, j).alignment = Alignment(text_rotation=90, horizontal="center", vertical="bottom")
        ws.cell(2, j).fill = PatternFill("solid", fgColor=STAGE[ROWS[j - 3]["stage"]])
        ws.cell(2, j).font = F(BG, 10, True)
    for i, rule in enumerate(RULES, 3):
        ws.cell(i, 1, ("🔬 " if rule["research"] else "") + rule["name"]).font = F(GOLD if rule["research"] else TEXT, 11, rule["research"])
        ws.cell(i, 2, rule["weight"]).font = INPUT
        ws.cell(i, 2).alignment = CENTER
        for j, row in enumerate(ROWS, 3):
            v = row[f"rules_{side.lower()}"][rule["key"]]
            c = ws.cell(i, j, None if v is None else int(v))
            c.number_format, c.alignment, c.border, c.font = '"✓";;"✗"', CENTER, BOX, F(BG, 12, True)
    last = 2 + NR
    rng = f"C3:{L(2 + NP)}{last}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor=STRONG, bgColor=STRONG)))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=["0"], fill=PatternFill("solid", fgColor=WEAK, bgColor=WEAK)))
    for k, (lab, r0, r1) in enumerate([("General score", 3, 13), ("Research score", 14, last), ("Combined score", 3, last)]):
        sr = last + 1 + k
        ws.cell(sr, 1, lab).font = F(GOLD, 11, True)
        for j in range(3, 3 + NP):
            col = L(j)
            c = ws.cell(sr, j, f'=IFERROR(100*SUMPRODUCT($B${r0}:$B${r1},{col}{r0}:{col}{r1})/SUMPRODUCT($B${r0}:$B${r1},--({col}{r0}:{col}{r1}<>"")),0)')
            c.number_format, c.font, c.alignment = "0", F(TEXT, 10, True), CENTER
    ws.conditional_formatting.add(f"C{last + 1}:{L(2 + NP)}{last + 3}", ColorScaleRule(start_type="num", start_value=0, start_color="5C1A33", mid_type="num", mid_value=50, mid_color="6A4C93", end_type="num", end_value=100, end_color="00A896"))
    ws.cell(last + 5, 1, "Score = sum of weights of passed checks ÷ sum of weights of applicable checks. Change a weight (cyan) and every score updates.").font = F(MUTED, 9, italic=True)
    page(ws, f"A1:{L(2 + NP)}{last + 3}")
SC = 3 + NR  # first score row

# ---------- Library ----------
lib = wb.create_sheet("Library", 0)
darken(lib, NP + 4, 9)
lib["A1"] = "Claude Research Prompts: 24 prompts, 8 stages"
lib["A1"].font = F(GOLD, 18, True)
head(lib, 3, ["#", "Stage", "Prompt", "What it gives you", "Fields", "Tokens", "Weak score", "Strong score", "Gain"], [5, 11, 26, 62, 8, 9, 11, 12, 9])
for i, row in enumerate(ROWS, 4):
    col = L(i - 1)
    vals = [i - 3, row["stage"].title(), row["title"], None,
            row["fields"], row["tokens_strong"], f"='Checks Weak'!{col}{SC + 2}", f"='Checks Strong'!{col}{SC + 2}", f"=H{i}-G{i}"]
    for j, v in enumerate(vals, 1):
        c = lib.cell(i, j, v)
        c.font, c.border, c.alignment = F(TEXT, 11), BOX, Alignment(vertical="center", horizontal="center" if j != 4 and j != 3 else "left", wrap_text=True)
        c.fill = CARD
    lib.cell(i, 2).fill = PatternFill("solid", fgColor=STAGE[row["stage"]])
    lib.cell(i, 2).font = F(BG, 11, True)
    lib.cell(i, 3).font = F(TEXT, 11, True)
    for j in (7, 8, 9):
        lib.cell(i, j).number_format = "0"
    lib.cell(i, 9).number_format = '"+"0'
    lib.cell(i, 9).font = F(GOLD, 11, True)
from researchprompts import load
USE = {p.id: p.use for p in load()}
for i, row in enumerate(ROWS, 4):
    lib.cell(i, 4, USE[row["id"]])
lib.conditional_formatting.add(f"G4:G{NP + 3}", ColorScaleRule(start_type="num", start_value=0, start_color="5C1A33", end_type="num", end_value=100, end_color="00A896"))
lib.conditional_formatting.add(f"H4:H{NP + 3}", ColorScaleRule(start_type="num", start_value=0, start_color="5C1A33", end_type="num", end_value=100, end_color="00A896"))
page(lib, f"A1:I{NP + 3}")

# ---------- Score data ----------
sd = wb.create_sheet("Score Data")
darken(sd, NP + 4, 8)
head(sd, 1, ["Prompt", "Weak", "Strong", "General weak", "General strong", "Research weak", "Research strong", "Stage"], [26, 9, 9, 12, 13, 13, 14, 11])
for i, row in enumerate(ROWS, 2):
    col = L(i + 1)
    sd.cell(i, 1, row["title"])
    sd.cell(i, 2, f"='Checks Weak'!{col}{SC + 2}"); sd.cell(i, 3, f"='Checks Strong'!{col}{SC + 2}")
    sd.cell(i, 4, f"='Checks Weak'!{col}{SC}"); sd.cell(i, 5, f"='Checks Strong'!{col}{SC}")
    sd.cell(i, 6, f"='Checks Weak'!{col}{SC + 1}"); sd.cell(i, 7, f"='Checks Strong'!{col}{SC + 1}")
    sd.cell(i, 8, row["stage"])
    for j in range(2, 8):
        sd.cell(i, j).number_format = "0"
E_ = NP + 1
sd.cell(E_ + 1, 1, "Average").font = F(GOLD, 11, True)
for c in "BCDEFG":
    sd[f"{c}{E_ + 1}"] = f"=AVERAGE({c}2:{c}{E_})"; sd[f"{c}{E_ + 1}"].number_format = "0.0"

# Chart: weak vs strong per prompt
ch = BarChart(); ch.type, ch.grouping, ch.gapWidth, ch.overlap = "bar", "clustered", 40, -10
ch.add_data(Reference(sd, min_col=2, max_col=3, min_row=1, max_row=E_), titles_from_data=True)
ch.set_categories(Reference(sd, min_col=1, min_row=2, max_row=E_))
dark(ch, "24 research prompts: the one-line version vs the full prompt (combined score, 0–100)", 30, 24)
paint(ch.series[0], WEAK); paint(ch.series[1], STRONG); labels(ch.series[1], "0", "outEnd", STRONG, 800); labels(ch.series[0], "0", "outEnd", WEAK, 800)
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 110
ch.x_axis.scaling.orientation = "maxMin"
chart_sheet(wb, "Chart Scores", ch)

# ---------- Stage data ----------
st = wb.create_sheet("Stage Data")
darken(st, 12, 10)
head(st, 1, ["Stage", "General weak", "General strong", "Research weak", "Research strong", "Combined strong", "Tokens"], [12, 13, 14, 14, 15, 16, 9])
for i, s in enumerate(STAGES, 2):
    st.cell(i, 1, s["stage"].title())
    n = s["stage"]
    for j, key in enumerate(["General weak", "General strong", "Research weak", "Research strong", "Combined strong"], 2):
        src = {"General weak": "D", "General strong": "E", "Research weak": "F", "Research strong": "G", "Combined strong": "C"}[key]
        st.cell(i, j, f'=AVERAGEIF(\'Score Data\'!$H$2:$H${E_},"{n}",\'Score Data\'!{src}$2:{src}${E_})').number_format = "0"
    st.cell(i, 7, round(s["tokens_strong"]))
ch = BarChart(); ch.type, ch.gapWidth, ch.overlap = "col", 60, -5
ch.add_data(Reference(st, min_col=2, max_col=5, min_row=1, max_row=9), titles_from_data=True)
ch.set_categories(Reference(st, min_col=1, min_row=2, max_row=9))
dark(ch, "Every stage, before and after: general checks vs research checks", 30, 15)
for s_, c_ in zip(ch.series, ["7A2E4A", STRONG, "6B2F8F", GOLD]):
    paint(s_, c_)
labels(ch.series[3], "0", "outEnd", GOLD, 800); labels(ch.series[1], "0", "outEnd", STRONG, 800)
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 110
chart_sheet(wb, "Chart Stages", ch)

# ---------- Pass rate per check (radar) ----------
pr = wb.create_sheet("Pass Rates")
darken(pr, NR + 3, 4)
head(pr, 1, ["Check", "Weak prompts (%)", "Strong prompts (%)"], [42, 16, 16])
for i, rule in enumerate(RULES, 2):
    pr.cell(i, 1, rule["name"])
    rr = i + 1  # row in the check sheets
    for j, side in ((2, "Weak"), (3, "Strong")):
        rng = f"'Checks {side}'!$C${rr}:${L(2 + NP)}${rr}"
        pr.cell(i, j, f'=IFERROR(100*SUM({rng})/COUNT({rng}),0)').number_format = "0"
ch = RadarChart(); ch.type = "marker"
ch.add_data(Reference(pr, min_col=2, max_col=3, min_row=1, max_row=NR + 1), titles_from_data=True)
ch.set_categories(Reference(pr, min_col=1, min_row=2, max_row=NR + 1))
dark(ch, "Share of prompts that pass each check (%)", 28, 20)
paint(ch.series[0], WEAK, line=True, marker="circle"); paint(ch.series[1], STRONG, line=True, marker="diamond")
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 100
ch.y_axis.delete = True
chart_sheet(wb, "Chart Radar", ch)

# ---------- Anatomy ----------
an = wb.create_sheet("Anatomy Data")
darken(an, 14, 10)
head(an, 1, ["Stage"] + PARTS, [12] + [15] * len(PARTS))
for i, s in enumerate(STAGES, 2):
    an.cell(i, 1, s["stage"].title())
    for j, part in enumerate(PARTS, 2):
        an.cell(i, j, round(s["anatomy"][part], 1)).number_format = "0"
an.cell(11, 1, "Average").font = F(GOLD, 11, True)
for j in range(2, 2 + len(PARTS)):
    an.cell(11, j, f"=AVERAGE({L(j)}2:{L(j)}9)").number_format = "0"
an.cell(13, 1, "Tokens counted with the open Llama 4 tokenizer as a stand-in; Claude's own counts differ a little.").font = F(MUTED, 9, italic=True)
# doughnut of the average
ch = DoughnutChart(); ch.holeSize = 52
ch.add_data(Reference(an, min_col=2, max_col=1 + len(PARTS), min_row=11), from_rows=True, titles_from_data=False)
ch.set_categories(Reference(an, min_col=2, max_col=1 + len(PARTS), min_row=1))
dark(ch, "Where the tokens of a strong prompt go (average of 24)", 22, 15, legend="r")
s_ = ch.series[0]
s_.dPt = [DataPoint(idx=k, spPr=GraphicalProperties(solidFill=NEON[k], ln=LineProperties(solidFill=BG, w=25400))) for k in range(len(PARTS))]
labels(s_, None, None, BG, 1000); s_.dLbls.showVal, s_.dLbls.showPercent = False, True
chart_sheet(wb, "Chart Anatomy", ch)
# stacked columns by stage
ch = BarChart(); ch.type, ch.grouping, ch.overlap, ch.gapWidth = "col", "stacked", 100, 45
ch.add_data(Reference(an, min_col=2, max_col=1 + len(PARTS), min_row=1, max_row=9), titles_from_data=True)
ch.set_categories(Reference(an, min_col=1, min_row=2, max_row=9))
dark(ch, "Prompt anatomy by stage (tokens per part)", 30, 15, legend="b")
for k, s_ in enumerate(ch.series):
    paint(s_, NEON[k])
chart_sheet(wb, "Chart Anatomy Stage", ch)

# ---------- Tokens vs score bubble, one series per stage ----------
bd = wb.create_sheet("Bubble Data")
darken(bd, NP + 3, 5)
head(bd, 1, ["Prompt", "Tokens", "Combined score", "Fields", "Stage"], [26, 9, 15, 8, 11])
for i, row in enumerate(ROWS, 2):
    bd.cell(i, 1, row["title"]); bd.cell(i, 2, row["tokens_strong"]); bd.cell(i, 3, f"='Score Data'!C{i}"); bd.cell(i, 4, row["fields"]); bd.cell(i, 5, row["stage"])
ch = BubbleChart(); ch.style = 18
for k, s in enumerate(STAGES):
    r0 = 2 + 3 * k
    ser = Series(Reference(bd, min_col=3, min_row=r0, max_row=r0 + 2), Reference(bd, min_col=2, min_row=r0, max_row=r0 + 2),
                 zvalues=Reference(bd, min_col=4, min_row=r0, max_row=r0 + 2), title=s["stage"].title())
    ser.graphicalProperties = GraphicalProperties(solidFill=STAGE[s["stage"]], ln=LineProperties(solidFill=BG))
    ch.series.append(ser)
ch.bubbleScale = 16
dark(ch, "Longer is not the goal: tokens vs score (bubble size = number of fields)", 30, 16, legend="b")
axis_title(ch.x_axis, "Tokens in the prompt template"); axis_title(ch.y_axis, "Combined score")
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 60, 105
ch.x_axis.scaling.min, ch.x_axis.scaling.max = 150, 400
chart_sheet(wb, "Chart Bubble", ch)

# ---------- Live cost model ----------
cm = wb.create_sheet("Cost Model")
darken(cm, 40, 10)
AS = A["assumptions"]
cm["A1"] = "What a literature review costs on the Claude API, and what putting the paper first saves"
cm["A1"].font = F(GOLD, 15, True)
head(cm, 3, ["Model", "Input $/MTok", "5-min cache write", "1-hour cache write", "Cache read", "Output $/MTok"], [30, 13, 15, 15, 12, 14])
from researchprompts.cost import PRICES
for i, (m, p) in enumerate(PRICES.items(), 4):
    cm.cell(i, 1, m)
    for j, v in enumerate(p, 2):
        cm.cell(i, j, v).font = INPUT; cm.cell(i, j).number_format = "$0.000"
cm["A7"] = "Source: platform.claude.com/docs/en/about-claude/pricing (retrieved 2026-11-09). Batch API = 50% off."
cm["A7"].font = F(MUTED, 9, italic=True)
inputs = [("Model used below", "Claude Sonnet 5.5", "Must match a row above"),
          ("Tokens in one paper", AS["paper_tokens"], "Assumption: a 10-page paper"),
          ("Tokens in the prompt around it", A["summary"]["prompt_tokens_read"], "Measured: average read/analyze template"),
          ("Tokens in one answer", AS["output_tokens"], "Assumption"),
          ("Papers in the review", AS["papers"], "Assumption"),
          ("Prompts per paper", AS["prompts_per_paper"], "Assumption"),
          ("Batch discount", 0.5, "From the pricing page")]
for i, (k, v, n) in enumerate(inputs, 9):
    cm.cell(i, 1, k); cm.cell(i, 2, v).font = INPUT; cm.cell(i, 3, n).font = F(MUTED, 9, italic=True)
P = {"in": "INDEX($B$4:$B$6,MATCH($B$9,$A$4:$A$6,0))", "w5": "INDEX($C$4:$C$6,MATCH($B$9,$A$4:$A$6,0))",
     "rd": "INDEX($E$4:$E$6,MATCH($B$9,$A$4:$A$6,0))", "out": "INDEX($F$4:$F$6,MATCH($B$9,$A$4:$A$6,0))"}
head(cm, 18, ["Prompts about one paper (k)", "Paper last", "Paper first + cache", "Batch", "Batch + cache"], [30, 13, 18, 12, 14])
for k in range(1, 13):
    r = 18 + k
    cm.cell(r, 1, k)
    cm.cell(r, 2, f"=A{r}*(($B$10+$B$11)*{P['in']}+$B$12*{P['out']})/1000000")
    cm.cell(r, 3, f"=($B$10*{P['w5']}+(A{r}-1)*$B$10*{P['rd']}+A{r}*($B$11*{P['in']}+$B$12*{P['out']}))/1000000")
    cm.cell(r, 4, f"=$B$15*B{r}"); cm.cell(r, 5, f"=$B$15*C{r}")
    for j in range(2, 6):
        cm.cell(r, j).number_format = "$0.000"
cm["G18"], cm["G19"] = "Whole review (papers × cost at k = prompts per paper)", "Paper last"
cm["G18"].font = F(GOLD, 11, True)
for j, lab in enumerate(["Paper last", "Paper first + cache", "Batch", "Batch + cache"]):
    cm.cell(19 + j, 7, lab)
    cm.cell(19 + j, 8, f"=$B$13*INDEX({L(2 + j)}19:{L(2 + j)}30,$B$14)").number_format = "$0.00"
cm["G24"], cm["H24"] = "Saving from paper-first caching", "=1-H20/H19"
cm["H24"].number_format, cm["H24"].font = "0%", F(GOLD, 14, True)
cm.column_dimensions["G"].width, cm.column_dimensions["H"].width = 34, 12
ch = LineChart()
ch.add_data(Reference(cm, min_col=2, max_col=5, min_row=18, max_row=30), titles_from_data=True)
ch.set_categories(Reference(cm, min_col=1, min_row=19, max_row=30))
dark(ch, "Cost of asking k prompts about one 12,000-token paper (Claude Sonnet 5.5, USD)", 30, 15)
for s_, c_, mk in zip(ch.series, [WEAK, STRONG, GOLD, "B388FF"], ["circle", "diamond", "triangle", "square"]):
    paint(s_, c_, line=True, marker=mk)
labels(ch.series[0], "$0.00", "t", WEAK, 800)
axis_title(ch.x_axis, "Prompts about the same paper"); axis_title(ch.y_axis, "USD")
ch.y_axis.number_format = "$0.00"
chart_sheet(wb, "Chart Cost", ch)

# Whole review by model
pm = wb.create_sheet("Project Data")
darken(pm, 8, 6)
head(pm, 1, ["Model", "Paper last", "Paper first + cache", "Batch", "Batch + cache"], [20, 12, 18, 12, 14])
for i, (m, d) in enumerate(A["project"].items(), 2):
    pm.cell(i, 1, m.replace("Claude ", ""))
    for j, lay in enumerate(["paper_last", "paper_first", "batch", "batch_cache"], 2):
        pm.cell(i, j, round(d[lay], 4)).number_format = "$0.00"
pm["A6"] = "Values from run_analysis.py (researchprompts/cost.py). The Cost Model sheet recomputes Sonnet 5.5 with live formulas."
pm["A6"].font = F(MUTED, 9, italic=True)
ch = BarChart(); ch.type, ch.gapWidth, ch.overlap = "col", 55, -5
ch.add_data(Reference(pm, min_col=2, max_col=5, min_row=1, max_row=3), titles_from_data=True)
ch.set_categories(Reference(pm, min_col=1, min_row=2, max_row=3))
dark(ch, f"A {AS['papers']}-paper review, {AS['prompts_per_paper']} prompts per paper: total API cost (USD)", 28, 15)
for s_, c_ in zip(ch.series, [WEAK, STRONG, GOLD, "B388FF"]):
    paint(s_, c_); labels(s_, "$0.00", "outEnd", c_, 900)
ch.y_axis.number_format = "$0"
chart_sheet(wb, "Chart Project", ch)

# Where the input tokens of one call go
ov = wb.create_sheet("Overhead Data")
darken(ov, 6, 3)
head(ov, 1, ["Part of one call", "Tokens"], [36, 10])
ov["A2"], ov["B2"] = "Your paper", "='Cost Model'!B10"
ov["A3"], ov["B3"] = "Strong prompt template", f"={round(A['summary']['tokens_strong'])}"
ov["A4"], ov["B4"] = "One-line prompt it replaces", f"={round(A['summary']['tokens_weak'])}"
ch = DoughnutChart(); ch.holeSize = 60
ch.add_data(Reference(ov, min_col=2, min_row=2, max_row=3))
ch.set_categories(Reference(ov, min_col=1, min_row=2, max_row=3))
dark(ch, "A strong prompt is about 2% of the input when you send a paper", 22, 14, legend="r")
s_ = ch.series[0]
s_.dPt = [DataPoint(idx=0, spPr=GraphicalProperties(solidFill="3A86FF", ln=LineProperties(solidFill=BG, w=19050))),
          DataPoint(idx=1, spPr=GraphicalProperties(solidFill=GOLD, ln=LineProperties(solidFill=BG, w=19050)))]
labels(s_, "0.0%", "bestFit", TEXT, 1100); s_.dLbls.showVal, s_.dLbls.showPercent = False, True
chart_sheet(wb, "Chart Overhead", ch)

# ---------- Dashboard tiles ----------
db = wb.create_sheet("Dashboard", 0)
db.sheet_view.showGridLines = False
items = [("=COUNTA('Score Data'!A2:A25)", "0", "research prompts", "F72585"),
         (f"=ROUND('Score Data'!B{E_ + 1},0)&\" → \"&ROUND('Score Data'!C{E_ + 1},0)", "@", "combined score, weak → strong", STRONG),
         (f"=ROUND('Score Data'!F{E_ + 1},0)&\" → \"&ROUND('Score Data'!G{E_ + 1},0)", "@", "research-safety score", GOLD),
         ("='Cost Model'!H24", "0%", "cheaper with the paper first", "3A86FF"),
         ("=Overhead Data!B3/'Overhead Data'!B2".replace("=Overhead Data", "='Overhead Data'"), "0.0%", "extra input for a strong prompt", "FB5607")]
db.column_dimensions["A"].width = 2
for r in range(1, 7):
    for c in range(1, 2 + 2 * len(items)):
        db.cell(r, c).fill = DARK
db.row_dimensions[2].height, db.row_dimensions[3].height, db.row_dimensions[4].height = 10, 70, 34
for k, (f, fmt, lab, color) in enumerate(items):
    col = L(2 + 2 * k)
    db.column_dimensions[col].width, db.column_dimensions[L(3 + 2 * k)].width = 27, 2
    a, b = db[f"{col}3"], db[f"{col}4"]
    a.value, a.number_format = f, fmt
    a.font, a.fill, a.alignment = F(color, 36, True), CARD, CENTER
    b.value, b.font, b.fill, b.alignment = lab, F(TEXT, 12), CARD, CENTER
page(db, f"A1:{L(1 + 2 * len(items))}5")

wb._sheets.insert(1, wb._sheets.pop(wb.sheetnames.index("Library")))
wb.save("excel/claude_research_prompts.xlsx")
print("saved", wb.sheetnames)
