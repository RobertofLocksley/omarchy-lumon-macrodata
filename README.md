# Lumon Macrodata

An Omarchy 4 theme for a compliant Macrodata Refinement workstation, with an
optional live Macrodata Refinement field in place of the wallpaper.

```bash
omarchy theme install https://github.com/RobertofLocksley/omarchy-lumon-macrodata
```

> The repository name matters. `omarchy theme install` strips a leading
> `omarchy-` and a trailing `-theme` to derive the installed directory name, so
> this repo installs as `lumon-macrodata` — which is the slug the companion
> plugin looks for. Renaming the repo breaks activation of the live field.

## The live field (optional)

Paired with
[omarchy-mdr-background](https://github.com/RobertofLocksley/omarchy-mdr-background),
this theme's desktop background becomes a working Macrodata Refinement terminal:
digits fill the screen, "scary" ones swell and twitch in drifting clusters, and
you can lasso a cluster into one of the five bins along the bottom.

```bash
omarchy plugin add https://github.com/RobertofLocksley/omarchy-mdr-background
```

The plugin reads the active theme and only draws the field under this one, so
every other theme keeps Omarchy's stock wallpaper behaviour. Themes cannot ship
Quickshell plugins themselves, which is why this is two pieces.

**Without the plugin the theme still works** — you get the wallpapers instead.

## Contents

| File | Purpose |
|---|---|
| `colors.toml` | The palette. Omarchy derives terminal colors from this. |
| `shell.lock.toml` | Lock screen text and border colors |
| `keyboard.rgb` | Keyboard backlight color |
| `hyprland.lua` | Border and presentation tuning |
| `btop.theme`, `chromium.theme`, `neovim.lua`, `vscode.json` | App palettes |
| `icons.theme` | Icon theme selection |
| `backgrounds/` | Wallpapers, including a rendered refinement still |

Note that Omarchy 4 derives Alacritty, Ghostty, Kitty and Foot colors from
`colors.toml` and actively rejects per-terminal files from installed themes, so
none are shipped here.

## Provenance

Built on Omarchy's own `lumon` theme (MIT, Basecamp) — see
[basecamp/omarchy](https://github.com/basecamp/omarchy). Added on top:
`shell.lock.toml`, `keyboard.rgb`, and `backgrounds/03-macrodata-refinement.png`,
which is generated rather than captured.

Visual language derives from *Severance* (Apple TV+). Not affiliated with or
endorsed by Apple or the show's producers.

## The bins

| Code | Temper | Feeling |
|------|--------|-----------------------------|
| `WO` | Woe    | melancholy, despair         |
| `FC` | Frolic | joy, gaiety, ecstasy        |
| `DR` | Dread  | fear, anxiety, apprehension |
| `MA` | Malice | anger, a desire to do harm  |

Please enjoy each color equally.
