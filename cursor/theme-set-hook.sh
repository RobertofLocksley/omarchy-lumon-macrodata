#!/bin/bash
# Swap the pointer with the theme. Omarchy themes cannot carry a cursor, so the
# switch is done here instead: the Lumon pointer under the macrodata theme, the
# system default everywhere else.

if [[ $1 == "lumon-macrodata" ]] && [[ -d "$HOME/.local/share/icons/LumonMacrodata" ]]; then
  cursor="LumonMacrodata"
else
  cursor="default"
fi

size="${XCURSOR_SIZE:-24}"

# setcursor applies to the running compositor immediately; the gsettings key is
# what GTK apps read.
hyprctl setcursor "$cursor" "$size" >/dev/null 2>&1 || true
gsettings set org.gnome.desktop.interface cursor-theme "$cursor" >/dev/null 2>&1 || true
