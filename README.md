# kitty-config

A [kitty](https://sw.kovidgoyal.net/kitty/) configuration with split-based window management, a
top tab bar, and the Heritage colour themes.

## Requirements

- kitty (tested with 0.48.2)
- JetBrainsMono Nerd Font
- `wl-clipboard` on Wayland or `xclip` on X11 (image paste, see [Keymaps](#keymaps))

## Install

```bash
git clone https://github.com/yendrrek/kitty-config.git ~/dev/kitty-config
ln -s ~/dev/kitty-config ~/.config/kitty
```

Move an existing `~/.config/kitty` aside first. kitty reads the configuration on start; press
`Ctrl+Shift+F5` to reload it in a running window.

## Layout

| Path | Content |
| --- | --- |
| `kitty.conf` | Settings and keymaps. Unchanged defaults stay commented out. |
| `current-theme.conf` | The active colour theme, written by `kitten themes`. |
| `themes/` | Heritage themes, listed by `kitten themes`. |
| `tab_bar.py` | Tab bar drawing that colours tabs from the active theme. |
| `paste_or_forward.py` | Kitten bound to `Ctrl+V`. |

Choose a theme with:

```bash
kitten themes
```

## Keymaps

The split prefix is `Alt+C`.

| Keys | Action |
| --- | --- |
| `Alt+C` `Shift+2` / `Shift+5` | Split horizontally / vertically in the current directory |
| `Alt+C` `Up` / `Down` | Focus the window above / below |
| `Ctrl+T` | New tab |
| `Alt+1` to `Alt+8` | Go to tab 1 to 8 |
| `Ctrl+Shift+Alt+T` | Rename the tab |
| `Ctrl+Shift+Alt+N` | Move the tab into a new window |
| `Ctrl+C` | Copy the selection; with none, send `Ctrl+C` to the program |
| `Ctrl+V` | Paste text; with an image on the clipboard, send `Ctrl+V` to the program |

`Ctrl+Shift+V` is unbound. Programs such as Claude Code read a clipboard image themselves when they
receive `Ctrl+V`, which is why `paste_or_forward.py` forwards the key.

## Appearance

| Setting | Value |
| --- | --- |
| Font | JetBrainsMono Nerd Font, 9 pt |
| Layout | `splits` only |
| Cursor | Underline |
| Tab bar | Top edge, titled `<index>: <title>` |
| Active tab | A theme colour that stands out from the background, set by `tab_bar.py` |
| Window decorations | Hidden |
