# Lumon Macrodata

An Omarchy 4 theme for a compliant Macrodata Refinement workstation.

```bash
omarchy theme install https://github.com/RobertofLocksley/omarchy-lumon-macrodata
```

## The live field

Paired with
[omarchy-mdr-background](https://github.com/RobertofLocksley/omarchy-mdr-background),
the desktop background becomes a working Macrodata Refinement terminal: digits
fill the screen, "scary" ones swell and twitch in drifting clusters, and you can
lasso a cluster into one of the five bins along the bottom.

```bash
omarchy plugin add https://github.com/RobertofLocksley/omarchy-mdr-background
```

The plugin only draws the field under this theme; every other theme keeps
Omarchy's stock wallpaper behaviour. Without the plugin, this theme still works
— you get the wallpapers instead.

## Contents

| File | Purpose |
|---|---|
| `colors.toml` | The palette; Omarchy derives terminal colors from it |
| `shell.lock.toml` | Lock screen text and border colors |
| `keyboard.rgb` | Keyboard backlight color |
| `hyprland.lua` | Border and presentation tuning |
| `btop.theme`, `chromium.theme`, `neovim.lua`, `vscode.json` | App palettes |
| `icons.theme` | Icon theme selection |
| `backgrounds/` | Wallpapers |
| `cursor/` | Pointer generator and installer |
| `tools/` | Wallpaper generator |

## Pointer

Omarchy themes cannot carry a cursor, so the Lumon pointer is installed
separately:

```bash
./cursor/install.sh
```

It follows the theme from then on — applied under this theme, reverting to the
system default under any other. Requires `xorg-xcursorgen` and ImageMagick.

## The bins

| Code | Temper | Feeling |
|------|--------|-----------------------------|
| `WO` | Woe    | melancholy, despair         |
| `FC` | Frolic | joy, gaiety, ecstasy        |
| `DR` | Dread  | fear, anxiety, apprehension |
| `MA` | Malice | anger, a desire to do harm  |

Please enjoy each color equally.

## License

MIT. Built on Omarchy's `lumon` theme, also MIT —
[basecamp/omarchy](https://github.com/basecamp/omarchy).

Visual language derives from *Severance* (Apple TV+). Not affiliated with or
endorsed by Apple or the show's producers.
