"""Draws the banner, the stage cards and the before/after card for the README (Pillow).
Numbers come from results/analysis.json, so the pictures always match the analysis."""
import json, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from researchprompts import load, STAGES

A = json.load(open("results/analysis.json", encoding="utf8"))
OUT = pathlib.Path("results")
BG = (18, 14, 38)
STAGE = {"discover": "#F72585", "read": "#FB5607", "design": "#FFBE0B", "analyze": "#8AC926",
         "write": "#00F5D4", "polish": "#3A86FF", "submit": "#8338EC", "revise": "#FF99C8"}
ICON = {"discover": "🔭", "read": "📖", "design": "🧪", "analyze": "📊", "write": "✍", "polish": "✨", "submit": "🚀", "revise": "🔁"}


def font(weight, size):
    for f in (f"/usr/share/fonts/opentype/inter/Inter-{weight}.otf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


MONO = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", s)
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))


def glow(size, blobs):
    """Dark background with soft neon light blobs."""
    im = Image.new("RGB", size, BG)
    layer = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    for (x, y, r, c) in blobs:
        d.ellipse([x - r, y - r, x + r, y + r], fill=hexrgb(c))
    layer = layer.filter(ImageFilter.GaussianBlur(size[0] // 9))
    return Image.blend(im, layer, 0.55)


def wrap(d, text, f, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            out.append(cur); cur = w
    return out + [cur]


def banner():
    W, H = 2560, 900
    im = glow((W, H), [(300, 150, 420, "#F72585"), (1300, 950, 520, "#3A86FF"), (2400, 150, 450, "#00F5D4"), (1900, 800, 300, "#FFBE0B")])
    d = ImageDraw.Draw(im)
    d.text((140, 150), "CLAUDE", font=font("Black", 70), fill="#FFD60A")
    d.text((140, 225), "Research Prompts", font=font("Black", 170), fill="white")
    S = A["summary"]
    d.text((146, 440), f"{S['prompts']} prompts for every stage of a research paper, a research-aware linter,", font=font("Medium", 50), fill="#E6E3FF")
    d.text((146, 505), "and the math of running them cheaply on the Claude API.", font=font("Medium", 50), fill="#E6E3FF")
    x, y = 146, 640
    for s in STAGES:
        f = font("Bold", 40)
        w = d.textlength(s.upper(), font=f) + 70
        if x + w > W - 120:
            x, y = 146, y + 100
        d.rounded_rectangle([x, y, x + w, y + 76], 38, fill=STAGE[s])
        d.text((x + 35, y + 15), s.upper(), font=f, fill=BG)
        x += w + 22
    im.save(OUT / "banner.png")


def stage_cards():
    W, H, cols = 2560, 1240, 4
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    cw, chh, gap = (W - 5 * 40) // cols, (H - 3 * 40) // 2, 40
    ps = load()
    stats = {s["stage"]: s for s in A["stages"]}
    for k, s in enumerate(STAGES):
        x, y = gap + (k % cols) * (cw + gap), gap + (k // cols) * (chh + gap)
        c = hexrgb(STAGE[s])
        card = Image.new("RGB", (cw, chh), (0, 0, 0))
        cd = ImageDraw.Draw(card)
        for i in range(chh):  # vertical gradient from the stage color to dark
            t = i / chh
            cd.line([(0, i), (cw, i)], fill=tuple(int(c[j] * (1 - t) * 0.9 + (34, 27, 70)[j] * t) for j in range(3)))
        mask = Image.new("L", (cw, chh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw, chh], 36, fill=255)
        im.paste(card, (x, y), mask)
        d.text((x + 40, y + 30), f"{k + 1:02d}", font=font("Black", 96), fill=(255, 255, 255))
        d.text((x + 40, y + 150), s.upper(), font=font("Black", 54), fill=BG)
        yy = y + 250
        for p in [p for p in ps if p.stage == s]:
            d.rounded_rectangle([x + 34, yy, x + cw - 34, yy + 66], 18, fill=(18, 14, 38))
            d.text((x + 56, yy + 14), p.title, font=font("SemiBold", 32), fill="white")
            yy += 84
        st = stats[s]
        d.text((x + 40, y + chh - 66), f"score {st['combined_weak']:.0f} → {st['combined_strong']:.0f}", font=font("Bold", 36), fill="#FFD60A")
    im.save(OUT / "stage_cards.png")


def before_after():
    W, H = 2560, 1300
    im = glow((W, H), [(200, 1200, 400, "#FF4D6D"), (2400, 100, 450, "#00F5D4")])
    d = ImageDraw.Draw(im)
    p = next(x for x in load() if x.id == "paper-deconstructor")
    row = next(r for r in A["rows"] if r["id"] == p.id)
    # left: the weak prompt
    d.rounded_rectangle([80, 120, 980, 1220], 40, fill=(43, 15, 35), outline="#FF4D6D", width=6)
    d.text((130, 160), "WHAT MOST PEOPLE TYPE", font=font("Black", 44), fill="#FF4D6D")
    yy = 280
    for line in wrap(d, p.weak.replace("\n", " ").replace("{{PAPER}}", "").strip(), font("SemiBold", 52), 780):
        d.text((130, yy), line, font=font("SemiBold", 52), fill="white"); yy += 70
    d.text((130, yy + 20), "{{PAPER}}", font=MONO(40), fill="#A69FD6")
    d.text((130, 880), f"{row['combined_weak']:.0f}", font=font("Black", 210), fill="#FF4D6D")
    d.text((136, 1110), "out of 100 on the 17 checks", font=font("Medium", 38), fill="#E6E3FF")
    # arrow
    d.polygon([(1030, 610), (1150, 670), (1030, 730)], fill="#FFD60A")
    d.rectangle([995, 650, 1040, 690], fill="#FFD60A")
    # right: the strong prompt
    d.rounded_rectangle([1200, 120, 2480, 1220], 40, fill=(12, 40, 48), outline="#00F5D4", width=6)
    d.text((1250, 160), "THE PAPER DECONSTRUCTOR", font=font("Black", 44), fill="#00F5D4")
    yy = 250
    for line in p.template.splitlines()[:20]:
        if not line.strip():
            yy += 14; continue
        col = "#FFD60A" if line.startswith("<") else ("#7DF9FF" if "{{" in line else "#E6E3FF")
        for seg in wrap(d, line, MONO(27), 1180):
            if yy > 860:
                break
            d.text((1250, yy), seg, font=MONO(27), fill=col); yy += 36
    d.text((1250, 880), f"{row['combined_strong']:.0f}", font=font("Black", 210), fill="#00F5D4")
    d.text((1256, 1110), "out of 100 on the 17 checks", font=font("Medium", 38), fill="#E6E3FF")
    passed = [k for k, v in row["rules_strong"].items() if v]
    d.text((1700, 1000), f"✓ {len(passed)} checks passed", font=font("Bold", 46), fill="#FFD60A")
    d.text((1700, 1066), f"{row['tokens_strong']} tokens vs {row['tokens_weak']}", font=font("Medium", 38), fill="#E6E3FF")
    im.save(OUT / "before_after.png")


def social():
    W, H = 1280, 640
    im = glow((W, H), [(150, 80, 260, "#F72585"), (1180, 600, 300, "#00F5D4"), (700, 700, 200, "#FFBE0B")])
    d = ImageDraw.Draw(im)
    S = A["summary"]
    d.text((70, 70), "CLAUDE", font=font("Black", 34), fill="#FFD60A")
    d.text((70, 108), "Research Prompts", font=font("Black", 86), fill="white")
    d.text((72, 225), f"{S['prompts']} prompts · 8 research stages · a research-aware linter", font=font("Medium", 28), fill="#E6E3FF")
    d.text((70, 300), f"{S['combined_weak']:.0f} → {S['combined_strong']:.0f}", font=font("Black", 130), fill="#00F5D4")
    d.text((74, 450), "average score, one-line prompt vs full prompt", font=font("Medium", 28), fill="#E6E3FF")
    x, y = 72, 530
    for s in STAGES:
        w = d.textlength(s, font=font("Bold", 22)) + 34
        d.rounded_rectangle([x, y, x + w, y + 40], 20, fill=STAGE[s]); d.text((x + 17, y + 7), s, font=font("Bold", 22), fill=BG); x += w + 10
    d.text((72, 590), "github.com/jafarSalim", font=font("Medium", 22), fill="#A69FD6")
    im.save(OUT / "social_preview.png")


for fn in (banner, stage_cards, before_after, social):
    fn(); print("drew", fn.__name__)
