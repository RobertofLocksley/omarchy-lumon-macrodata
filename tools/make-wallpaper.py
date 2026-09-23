#!/usr/bin/env python3
"""Render a Macrodata Refinement still for use as a wallpaper.

Generated rather than screen-captured, so the result carries no compositor
chrome and is reproducible. Geometry and palette mirror the live field in the
omarchy-mdr-background plugin, so the static wallpaper and the animated version
agree.

    ./tools/make-wallpaper.py backgrounds/03-macrodata-refinement.png

Requires ImageMagick.
"""
import math
import random
import subprocess
import sys

W, H = 1920, 1080
BG = "#010A13"
FG = "#ABFFE9"
SELECT = "#EEFFFF"

MONO = "/usr/share/fonts/gsfonts/NimbusMonoPS-Regular.otf"
SANS = "/usr/share/fonts/gsfonts/NimbusSans-Bold.otf"

BUFFER = min(W, H) * 0.0926           # 100 at 1080p
CELL = (min(W, H) - BUFFER * 2) / 10  # 88
BASE = CELL * 0.30
COLS = int(W // CELL)
ROWS = int((H - BUFFER * 2) // CELL)
ORIGIN_X = (W - COLS * CELL) / 2
ORIGIN_Y = BUFFER

PROGRESS = 0.0
FILE_NAME = "Dranesville"
THRESHOLD = 0.62

random.seed(20260922)


def noise(cx, cy):
    """Coherent field in 0..1, so thresholding yields blobs not speckle."""
    v = (math.sin(cx * 0.55 + 1.3) * math.cos(cy * 0.61 - 0.7)
         + math.sin((cx + cy) * 0.31 + 2.1) * 0.8
         + math.cos((cx - cy) * 0.43 - 1.1) * 0.6)
    return (v / 2.4 + 1) / 2


def rgba(hex_color, alpha):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha:.3f})"


args = ["magick", "-size", f"{W}x{H}", f"xc:{BG}"]

# ---- digits: idle ones dim and small, clusters bright and swollen ----------
args += ["-font", MONO]
for r in range(ROWS):
    for c in range(COLS):
        v = noise(c, r)
        scary = v > THRESHOLD
        heat = (v - THRESHOLD) / (1 - THRESHOLD) if scary else 0.0
        size = BASE * (1 + heat * 1.1)
        cx = ORIGIN_X + c * CELL + CELL / 2
        cy = ORIGIN_Y + r * CELL + CELL / 2
        if scary:
            cx += random.uniform(-2.5, 2.5)
            cy += random.uniform(-2.5, 2.5)
        colour = SELECT if heat > 0.45 else FG
        args += ["-fill", rgba(colour, 0.48 + heat * 0.52), "-stroke", "none",
                 "-pointsize", f"{size:.1f}",
                 "-annotate", f"+{cx - size * 0.30:.0f}+{cy + size * 0.36:.0f}",
                 str(random.randint(0, 9))]

# ---- field rules, drawn as close-set pairs --------------------------------
for y, alpha in ((BUFFER, 0.85), (BUFFER + 3, 0.35),
                 (H - BUFFER, 0.85), (H - BUFFER + 3, 0.35)):
    args += ["-stroke", rgba(FG, alpha), "-strokewidth", "1", "-fill", "none",
             "-draw", f"line 0,{y:.0f} {W},{y:.0f}"]

# ---- header ---------------------------------------------------------------
hx, hy = W * 0.05, BUFFER * 0.25
hw, hh = W * 0.9, BUFFER * 0.5
args += ["-stroke", FG, "-strokewidth", "2", "-fill", "none",
         "-draw", f"roundrectangle {hx:.0f},{hy:.0f} {hx+hw:.0f},{hy+hh:.0f} "
                  f"{hh*0.16:.0f},{hh*0.16:.0f}"]

args += ["-stroke", "none", "-fill", FG, "-font", MONO,
         "-pointsize", f"{BASE*0.78:.1f}",
         "-annotate", f"+{hx+BUFFER*0.16:.0f}+{hy+hh*0.66:.0f}", FILE_NAME]

pct_text = f"{int(PROGRESS * 100)}% Complete"
logo_w = hh * 0.88 * 2.05
pct_x = hx + hw - BUFFER * 0.06 - logo_w - BUFFER * 0.16 - len(pct_text) * BASE * 0.43
args += ["-pointsize", f"{BASE*0.72:.1f}",
         "-annotate", f"+{pct_x:.0f}+{hy+hh*0.66:.0f}", pct_text]

# segmented tick meter between the file name and the percentage
meter_x0 = hx + BUFFER * 0.16 + len(FILE_NAME) * BASE * 0.47 + BUFFER * 0.18
meter_x1 = pct_x - BUFFER * 0.18
tick_w = max(2, BASE * 0.13)
gap = tick_w * 1.4
count = max(1, int((meter_x1 - meter_x0) // (tick_w + gap)))
lit = round(count * PROGRESS)
mh = hh * 0.52
my = hy + (hh - mh) / 2
for i in range(count):
    x = meter_x0 + i * (tick_w + gap)
    args += ["-fill", rgba(FG, 1.0 if i < lit else 0.18),
             "-draw", f"rectangle {x:.1f},{my:.1f} {x+tick_w:.1f},{my+mh:.1f}"]

# ---- the Lumon mark: the oval is the globe --------------------------------
lh = hh * 0.88
lw = lh * 2.05
lx = hx + hw - BUFFER * 0.06 - lw
ly = hy + (hh - lh) / 2
stroke = max(1, lh * 0.042)
cx, cy = lx + lw / 2, ly + lh / 2
a, b = lw / 2 - stroke, lh / 2 - stroke

args += ["-fill", BG, "-stroke", FG, "-strokewidth", f"{stroke:.1f}",
         "-draw", f"ellipse {cx:.1f},{cy:.1f} {a:.1f},{b:.1f} 0,360"]
args += ["-fill", "none"]
for m in (0.62, 0.24):
    args += ["-draw", f"ellipse {cx:.1f},{cy:.1f} {a*m:.1f},{b:.1f} 0,360"]
args += ["-draw", f"line {cx:.1f},{cy-b:.1f} {cx:.1f},{cy+b:.1f}"]
for f in (-0.46, 0.46):
    y = cy + b * f
    half = a * math.sqrt(max(0, 1 - f * f))
    args += ["-draw", f"line {cx-half:.1f},{y:.1f} {cx+half:.1f},{y:.1f}"]

tw, th = lh * 1.30, lh * 0.34
args += ["-stroke", "none", "-fill", BG,
         "-draw", f"rectangle {cx-tw/2:.1f},{cy-th/2:.1f} {cx+tw/2:.1f},{cy+th/2:.1f}"]
args += ["-fill", FG, "-font", SANS, "-pointsize", f"{lh*0.40:.0f}",
         "-annotate", f"+{cx-tw/2+lh*0.02:.0f}+{cy+lh*0.14:.0f}", "LUMON"]

# ---- bins -----------------------------------------------------------------
bin_w = W / 5
plate_w = bin_w * 0.75
mouth_y = H - BUFFER * 0.75 - BUFFER * 0.14
ph = BUFFER * 0.26
args += ["-font", MONO]
for i in range(5):
    px = i * bin_w + (bin_w - plate_w) / 2
    args += ["-fill", BG, "-stroke", FG, "-strokewidth", "1",
             "-draw", f"rectangle {px:.0f},{mouth_y:.0f} {px+plate_w:.0f},{mouth_y+ph:.0f}"]
    args += ["-stroke", "none", "-fill", FG, "-pointsize", f"{BASE*0.62:.1f}",
             "-annotate", f"+{px+plate_w/2-BASE*0.4:.0f}+{mouth_y+ph*0.72:.0f}", f"{i+1:02d}"]
    by2 = mouth_y + ph + BUFFER * 0.06
    args += ["-fill", BG, "-stroke", FG, "-strokewidth", "1",
             "-draw", f"rectangle {px:.0f},{by2:.0f} {px+plate_w:.0f},{by2+ph:.0f}"]
    args += ["-stroke", "none", "-fill", FG, "-pointsize", f"{BASE*0.5:.1f}",
             "-annotate", f"+{px+5:.0f}+{by2+ph*0.72:.0f}", f"{int(PROGRESS*100)}%"]

# ---- coordinates: plain text, no filled bar -------------------------------
coords = "0x%06X : 0x%06X" % (random.getrandbits(24), random.getrandbits(24))
args += ["-fill", FG, "-pointsize", f"{BASE*0.62:.1f}",
         "-annotate", f"+{W/2 - len(coords)*BASE*0.19:.0f}+{H - BASE*0.35:.0f}", coords]

out = sys.argv[1] if len(sys.argv) > 1 else "backgrounds/03-macrodata-refinement.png"
args.append(out)
subprocess.run(args, check=True)
print("wrote", out)
