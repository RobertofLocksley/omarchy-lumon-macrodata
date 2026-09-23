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

MONO = "/usr/share/fonts/gsfonts/NimbusMonoPS-Bold.otf"
SANS = "/usr/share/fonts/gsfonts/NimbusSans-Regular.otf"
SANS_BOLD = "/usr/share/fonts/gsfonts/NimbusSans-Bold.otf"

BUFFER = min(W, H) * 0.0926           # 100 at 1080p
CELL = (min(W, H) - BUFFER * 2) / 10  # 88
BASE = CELL * 0.30      # chrome text
DIGIT = CELL * 0.46     # the field's digits are much larger
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
args += ["-font", SANS]
for r in range(ROWS):
    for c in range(COLS):
        v = noise(c, r)
        scary = v > THRESHOLD
        heat = (v - THRESHOLD) / (1 - THRESHOLD) if scary else 0.0
        size = DIGIT * (1 + heat * 1.1)
        cx = ORIGIN_X + c * CELL + CELL / 2
        cy = ORIGIN_Y + r * CELL + CELL / 2
        if scary:
            cx += random.uniform(-2.5, 2.5)
            cy += random.uniform(-2.5, 2.5)
        colour = SELECT if heat > 0.45 else FG
        ink = rgba(colour, 0.82 + heat * 0.18)
        args += ["-fill", ink, "-stroke", ink, "-strokewidth", "1",
                 "-pointsize", f"{size:.1f}",
                 "-annotate", f"+{cx - size * 0.30:.0f}+{cy + size * 0.36:.0f}",
                 str(random.randint(0, 9))]

# ---- field rules, drawn as close-set pairs --------------------------------
for y, alpha in ((BUFFER, 0.85), (BUFFER + 3, 0.35),
                 (H - BUFFER, 0.85), (H - BUFFER + 3, 0.35)):
    args += ["-stroke", rgba(FG, alpha), "-strokewidth", "1", "-fill", "none",
             "-draw", f"line 0,{y:.0f} {W},{y:.0f}"]

# ---- header ---------------------------------------------------------------
# One outlined box holding a tick track that lights from the left, the file
# name in its own knocked-out panel over it, the completion figure at the
# right, and the Lumon mark overlapping the box's right end.
PROGRESS = 0.0
FILE_NAME = "Dranesville"

box_w = W * 0.9
box_x = (W - box_w) / 2
box_y, box_h = 12, 76
inner = 3

logo_h = box_h * 1.3   # fits inside the top buffer
logo_w = logo_h * 2.05
logo_x = W - logo_w - 12          # sits at the screen edge, clear of the text
logo_y = box_y + box_h / 2 - logo_h / 2

args += ["-stroke", FG, "-strokewidth", "2", "-fill", "none",
         "-draw", f"rectangle {box_x:.0f},{box_y:.0f} {box_x+box_w:.0f},{box_y+box_h:.0f}"]

# tick track, lit from the left
track_x0 = box_x + inner
track_x1 = logo_x - 24            # ticks and figure stop short of the mark
tick_w = box_h * 0.085
pitch = tick_w * 2.25
count = int((track_x1 - track_x0) // pitch)
lit = round(count * PROGRESS)
args += ["-stroke", "none", "-fill", FG]
for i in range(lit):
    x = track_x0 + i * pitch
    args += ["-draw", f"rectangle {x:.1f},{box_y+inner:.1f} {x+tick_w:.1f},{box_y+box_h-inner:.1f}"]

# file name in a knocked-out panel over the track
args += ["-font", SANS_BOLD, "-pointsize", "48"]
name_w = len(FILE_NAME) * 27 + 48
args += ["-fill", BG, "-stroke", FG, "-strokewidth", "1.5",
         "-draw", f"rectangle {box_x+inner+2:.0f},{box_y+inner+2:.0f} "
                  f"{box_x+inner+2+name_w:.0f},{box_y+box_h-inner-2:.0f}"]
args += ["-stroke", "none", "-fill", FG,
         "-annotate", f"+{box_x+inner+26:.0f}+{box_y+54:.0f}", FILE_NAME]

# completion figure: bright glyphs with a dark edge so it survives either ground
pct_text = f"{int(PROGRESS*100)}% Complete"
pct_x = track_x1 - len(pct_text) * 26 - 10
args += ["-stroke", BG, "-strokewidth", "3", "-fill", BG,
         "-annotate", f"+{pct_x:.0f}+{box_y+54:.0f}", pct_text]
args += ["-stroke", "none", "-fill", FG,
         "-annotate", f"+{pct_x:.0f}+{box_y+54:.0f}", pct_text]

# ---- the Lumon mark -------------------------------------------------------
stroke = max(1, logo_h * 0.045)
cx, cy = logo_x + logo_w / 2, logo_y + logo_h / 2
a, b = logo_w / 2 - stroke, logo_h / 2 - stroke
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
tw, th = logo_h * 1.30, logo_h * 0.34
args += ["-stroke", "none", "-fill", BG,
         "-draw", f"rectangle {cx-tw/2:.1f},{cy-th/2:.1f} {cx+tw/2:.1f},{cy+th/2:.1f}"]
args += ["-fill", FG, "-font", SANS_BOLD, "-pointsize", f"{logo_h*0.40:.0f}",
         "-annotate", f"+{cx-tw/2+logo_h*0.02:.0f}+{cy+logo_h*0.14:.0f}", "LUMON"]

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
