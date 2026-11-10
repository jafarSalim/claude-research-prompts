"""Neon-on-dark styling for native Excel charts (openpyxl), plus a LibreOffice PNG renderer."""
import pathlib, subprocess, tempfile
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText
from openpyxl.chart.axis import ChartLines
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import ParagraphProperties, CharacterProperties, Paragraph, Font as DFont

BG, PLOT, GRID, TEXT, MUTED = "120E26", "1A1438", "352D5C", "EDEBFF", "A69FD6"
WEAK, STRONG, GOLD = "FF4D6D", "00F5D4", "FFD60A"
STAGE = {"discover": "F72585", "read": "FB5607", "design": "FFBE0B", "analyze": "8AC926",
         "write": "00F5D4", "polish": "3A86FF", "submit": "8338EC", "revise": "FF99C8"}
NEON = ["F72585", "00F5D4", "FFBE0B", "3A86FF", "8AC926", "FB5607", "8338EC", "FF99C8"]
SHEETF = "Segoe UI"


def _rich(color=TEXT, size=1000, bold=False):
    cp = CharacterProperties(latin=DFont(typeface="Calibri"), sz=size, b=bold, solidFill=color)
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])


def dark(ch, title, w=26, h=14, legend="b"):
    """Dark background, light text, faint grid."""
    ch.title = title
    ch.width, ch.height = w, h
    cp = CharacterProperties(latin=DFont(typeface="Calibri"), sz=1600, b=True, solidFill=TEXT)
    ch.title.tx.rich.p[0].pPr = ParagraphProperties(defRPr=cp)
    ch.graphical_properties = GraphicalProperties(solidFill=BG, ln=LineProperties(noFill=True))
    ch.plot_area.graphicalProperties = GraphicalProperties(solidFill=PLOT, ln=LineProperties(noFill=True))
    for ax in (getattr(ch, "x_axis", None), getattr(ch, "y_axis", None)):
        if ax is None:
            continue
        ax.delete = False
        ax.txPr = _rich(MUTED, 1000)
        ax.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill=GRID))
        if ax.majorGridlines is not None:
            ax.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=GRID, prstDash="dash"))
        if ax.title is not None:
            ax.title.tx.rich.p[0].pPr = ParagraphProperties(defRPr=CharacterProperties(sz=1100, b=True, solidFill=MUTED))
    if ch.legend is not None:
        if legend:
            ch.legend.position = legend
            ch.legend.txPr = _rich(TEXT, 1100)
        else:
            ch.legend = None
    return ch


def axis_title(ax, text):
    ax.title = text
    ax.title.tx.rich.p[0].pPr = ParagraphProperties(defRPr=CharacterProperties(sz=1100, b=True, solidFill=MUTED))


def paint(series, color, line=False, width=31750, marker=None):
    series.graphicalProperties = GraphicalProperties()
    if line:
        series.graphicalProperties.line.solidFill = color
        series.graphicalProperties.line.width = width
        series.smooth = False
        if marker:
            series.marker.symbol = marker
            series.marker.size = 8
            series.marker.graphicalProperties = GraphicalProperties(solidFill=color, ln=LineProperties(solidFill=BG))
    else:
        series.graphicalProperties.solidFill = color
        series.graphicalProperties.line.solidFill = BG


def labels(series, fmt=None, pos=None, color=TEXT, size=900):
    series.dLbls = DataLabelList()
    series.dLbls.showVal = True
    for k in ("showSerName", "showCatName", "showLegendKey", "showPercent"):
        setattr(series.dLbls, k, False)
    series.dLbls.txPr = _rich(color, size, True)
    if fmt:
        series.dLbls.numFmt = fmt
    if pos:
        series.dLbls.position = pos


def page(ws, area="A1:R32"):
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = ws.page_setup.fitToHeight = 1
    ws.print_area = area


def chart_sheet(wb, name, ch, note=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.add_chart(ch, "B2")
    if note:
        ws["B31"] = note
        ws["B31"].font = Font(name="Calibri", italic=True, color="6B6494", size=9)
    from openpyxl.utils import get_column_letter
    page(ws, f"A1:{get_column_letter(int(ch.width / 1.69) + 4)}{int(ch.height / 0.5) + 4}")
    return ws


def render(xlsx, pages, out_dir, margin=0):
    """pages: {sheet name: png file}. Exports those sheets to cropped PNGs."""
    from openpyxl import load_workbook
    from PIL import Image, ImageChops
    tmp = pathlib.Path(tempfile.mkdtemp())
    wb = load_workbook(xlsx)
    for ws in wb.worksheets:
        ws.sheet_state = "visible" if ws.title in pages else "hidden"
    wb.active = wb.sheetnames.index(next(n for n in wb.sheetnames if n in pages))
    wb.save(tmp / "r.xlsx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(tmp / "r.xlsx")], check=True, capture_output=True, timeout=300)
    subprocess.run(["pdftoppm", "-r", "200", "-png", str(tmp / "r.pdf"), str(tmp / "p")], check=True)
    imgs = sorted(tmp.glob("p-*.png"), key=lambda p: int(p.stem.split("-")[1]))
    names = [n for n in wb.sheetnames if n in pages]
    if len(imgs) != len(names):
        raise SystemExit(f"{len(imgs)} pages for {len(names)} sheets")
    out_dir = pathlib.Path(out_dir)
    for n, p in zip(names, imgs):
        im = Image.open(p).convert("RGB")
        box = ImageChops.difference(im, Image.new("RGB", im.size, "white")).point(lambda v: 255 if v > 12 else 0).getbbox()
        im.crop((max(box[0] - margin, 0), max(box[1] - margin, 0), min(box[2] + margin, im.width), min(box[3] + margin, im.height))).save(out_dir / pages[n])
    return names
