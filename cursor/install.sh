#!/usr/bin/env bash
# Build the Lumon pointer and wire it to theme switching.
#
#   ./cursor/install.sh
#
# Requires xorg-xcursorgen and ImageMagick.
set -euo pipefail

THEME_DIR="$HOME/.local/share/icons/LumonMacrodata"
HOOK_DIR="$HOME/.config/omarchy/hooks/theme-set.d"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for dep in xcursorgen magick python3; do
  command -v "$dep" >/dev/null || { echo "missing dependency: $dep" >&2; exit 1; }
done

rm -rf "$THEME_DIR"
python3 "$SRC/make-cursor.py" "$THEME_DIR"

mkdir -p "$HOOK_DIR"
install -m 755 "$SRC/theme-set-hook.sh" "$HOOK_DIR/lumon-cursor"

echo
echo "Installed to $THEME_DIR"
echo "The pointer now follows the theme: it applies under lumon-macrodata and"
echo "reverts to the system default under any other theme."
echo "Run 'omarchy theme set \"Lumon Macrodata\"' to apply it now."
