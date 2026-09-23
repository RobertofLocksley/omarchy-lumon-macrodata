#!/usr/bin/env python3
"""Build an X cursor theme from the Lumon terminal pointer shape.

The pointer is a four-point chevron, dark-filled with a bright cyan outline,
rotated so the tip leads. Rendered at several sizes and assembled with
xcursorgen.
"""
import math
import os
import pathlib
import subprocess
import sys

BG = "#010A13"
FG = "#ABFFE9"

# Chevron in local units, tip first.
POINTS = [(0, -10), (7.5, 10), (0, 5), (-7.5, 10)]
ANGLE = -math.pi / 5          # tip leads up-left, as on the terminals
STROKE = 2.6                  # in local units
SIZES = [24, 32, 48, 64, 96]

out_dir = pathlib.Path(sys.argv[1])
png_dir = out_dir / "png"
png_dir.mkdir(parents=True, exist_ok=True)


def rotate(p, a):
    x, y = p
    return (x * math.cos(a) - y * math.sin(a),
            x * math.sin(a) + y * math.cos(a))


rotated = [rotate(p, ANGLE) for p in POINTS]
pad = STROKE / 2 + 0.5
min_x = min(p[0] for p in rotated) - pad
min_y = min(p[1] for p in rotated) - pad
max_x = max(p[0] for p in rotated) + pad
max_y = max(p[1] for p in rotated) + pad
span = max(max_x - min_x, max_y - min_y)

config_lines = []
for size in SIZES:
    # Inset by a pixel so the antialiased outer edge is not shaved by the
    # canvas boundary.
    scale = (size - 2) / span
    pts = [((x - min_x) * scale + 1, (y - min_y) * scale + 1) for x, y in rotated]
    # Hotspot is the tip, which is the first point.
    xhot, yhot = int(round(pts[0][0])), int(round(pts[0][1]))
    poly = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    name = png_dir / f"pointer_{size}.png"
    subprocess.run([
        "magick", "-size", f"{size}x{size}", "xc:none",
        "-fill", BG, "-stroke", FG,
        "-strokewidth", f"{STROKE * scale:.2f}",
        # Round joins keep the outline exactly STROKE/2 outside the path. Miter
        # joins spike far past that at this shape's acute angles and clip.
        "-draw", f"stroke-linejoin round polygon {poly}",
        str(name),
    ], check=True)
    config_lines.append(f"{size} {xhot} {yhot} {name.name}")

cfg = png_dir / "pointer.cursor"
cfg.write_text("\n".join(config_lines) + "\n")

cursors_dir = out_dir / "cursors"
cursors_dir.mkdir(parents=True, exist_ok=True)
subprocess.run(["xcursorgen", cfg.name, str((cursors_dir / "default").resolve())],
               cwd=png_dir, check=True)

# Every pointer-ish name maps to the same shape; anything else falls through to
# the inherited theme so no cursor ends up missing.
aliases = [
    "left_ptr", "arrow", "top_left_arrow", "default", "pointer",
    "hand1", "hand2", "pointing_hand", "grab", "grabbing",
    "openhand", "closedhand", "context-menu", "copy", "alias",
    "dnd-none", "dnd-copy", "dnd-move", "dnd-link", "move",
]
for a in aliases:
    link = cursors_dir / a
    if link.name == "default":
        continue
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to("default")

(out_dir / "index.theme").write_text(
    "[Icon Theme]\n"
    "Name=Lumon Macrodata\n"
    "Comment=Lumon terminal pointer\n"
    "Inherits=Adwaita\n"
)
(out_dir / "cursor.theme").write_text(
    "[Icon Theme]\n"
    "Inherits=Lumon Macrodata\n"
)

print(f"built {out_dir}")
print("sizes:", ", ".join(str(s) for s in SIZES))
print("aliases:", len(aliases) - 1)
