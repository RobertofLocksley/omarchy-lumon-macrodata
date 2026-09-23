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
DIGIT = CELL * 0.38     # the field's digits, larger than the chrome
BAR_H = 26              # the desktop bar the header must clear
TOP_INSET = BAR_H + 10
HEADER_H = 72
FIELD_TOP = TOP_INSET + HEADER_H + 18
FOOTER_H = 148          # bins plus coordinates, with room to breathe
FIELD_BOTTOM = H - FOOTER_H
COLS = int(W // CELL)
ROWS = int((FIELD_BOTTOM - FIELD_TOP) // CELL)
ORIGIN_X = (W - COLS * CELL) / 2
ORIGIN_Y = FIELD_TOP

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
for y, alpha in ((FIELD_TOP - 10, 0.85), (FIELD_TOP - 7, 0.35),
                 (FIELD_BOTTOM + 10, 0.85), (FIELD_BOTTOM + 13, 0.35)):
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
box_y, box_h = TOP_INSET, HEADER_H
inner = 3

logo_h = box_h * 1.16  # slightly proud of the box, still clear of the bar
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
# A halo around each glyph, not a rectangle: a rectangular knockout leaves its
# own corners visible as dark blocks against the wireframe.
mark_pt = logo_h * 0.34
mark_w = mark_pt * 3.45          # "LUMON" in the bold cut, measured
mark_pos = f"+{cx-mark_w/2:.0f}+{cy+mark_pt*0.36:.0f}"
args += ["-font", SANS_BOLD, "-pointsize", f"{mark_pt:.0f}",
         "-stroke", BG, "-strokewidth", f"{logo_h*0.05:.1f}", "-fill", BG,
         "-annotate", mark_pos, "LUMON"]
args += ["-stroke", "none", "-fill", FG, "-annotate", mark_pos, "LUMON"]

# ---- bins -----------------------------------------------------------------
bin_w = W / 5
plate_w = bin_w * 0.74
plate_h = 32
stack_gap = 7
bins_y = FIELD_BOTTOM + 22
args += ["-font", SANS_BOLD]
for i in range(5):
    px = i * bin_w + (bin_w - plate_w) / 2
    args += ["-fill", BG, "-stroke", FG, "-strokewidth", "1.5",
             "-draw", f"rectangle {px:.0f},{bins_y:.0f} {px+plate_w:.0f},{bins_y+plate_h:.0f}"]
    args += ["-stroke", "none", "-fill", FG, "-pointsize", "24",
             "-annotate", f"+{px+plate_w/2-15:.0f}+{bins_y+plate_h*0.72:.0f}", f"{i+1:02d}"]

    by2 = bins_y + plate_h + stack_gap
    args += ["-fill", BG, "-stroke", FG, "-strokewidth", "1.5",
             "-draw", f"rectangle {px:.0f},{by2:.0f} {px+plate_w:.0f},{by2+plate_h:.0f}"]
    fill_w = (plate_w - 3) * PROGRESS
    if fill_w > 0:
        args += ["-stroke", "none", "-fill", FG,
                 "-draw", f"rectangle {px+1.5:.1f},{by2+1.5:.1f} {px+1.5+fill_w:.1f},{by2+plate_h-1.5:.1f}"]
    # dark glyphs with a bright edge, so the figure survives on either ground
    pos = f"+{px+10:.0f}+{by2+plate_h*0.72:.0f}"
    args += ["-stroke", FG, "-strokewidth", "2.5", "-fill", BG, "-pointsize", "22",
             "-annotate", pos, f"{int(PROGRESS*100)}%"]
    args += ["-stroke", "none", "-fill", BG, "-annotate", pos, f"{int(PROGRESS*100)}%"]

# ---- coordinates: plain text, no filled bar -------------------------------
coords = "0x%06X : 0x%06X" % (random.getrandbits(24), random.getrandbits(24))
args += ["-font", SANS_BOLD, "-stroke", "none", "-fill", FG, "-pointsize", "24",
         "-annotate", f"+{W/2 - len(coords)*7.2:.0f}+{H - 24:.0f}", coords]

out = sys.argv[1] if len(sys.argv) > 1 else "backgrounds/03-macrodata-refinement.png"
args.append(out)
subprocess.run(args, check=True)
print("wrote", out)
