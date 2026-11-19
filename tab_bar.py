"""Tab bar drawing that takes its colours from the active kitty theme.

The active tab is painted with a theme colour that stands out from both the terminal background and
the tab bar background, and its text with the theme foreground or background, whichever reads better.
The colours are read from the live kitty options on every draw, so a theme change applies at once.
"""

from kitty.fast_data_types import Color, Screen, get_options
from kitty.tab_bar import DrawData, ExtraData, TabBarData, draw_tab_with_fade

# Minimum WCAG contrast ratio between the active tab and the colours it sits on.
MIN_DISTINCT_CONTRAST = 1.2


def _linear(channel: int) -> float:
    value = channel / 255
    return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4


def _luminance(colour: Color) -> float:
    return 0.2126 * _linear(colour.red) + 0.7152 * _linear(colour.green) + 0.0722 * _linear(colour.blue)


def _contrast(first: Color, second: Color) -> float:
    lighter, darker = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _active_colours(draw_data: DrawData) -> tuple[Color, Color]:
    """Return the (background, foreground) of the active tab, both taken from the theme."""
    opts = get_options()
    surfaces = (opts.background, draw_data.default_bg)
    candidates = [
        colour
        for colour in (opts.selection_background, opts.color8, opts.color0, opts.foreground)
        if colour is not None
    ]

    def separation(colour: Color) -> float:
        return min(_contrast(colour, surface) for surface in surfaces)

    distinct = [colour for colour in candidates if separation(colour) >= MIN_DISTINCT_CONTRAST]
    background = distinct[0] if distinct else max(candidates, key=separation)
    foreground = max((opts.foreground, opts.background), key=lambda colour: _contrast(colour, background))
    return background, foreground


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_tab_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    background, foreground = _active_colours(draw_data)
    themed = draw_data._replace(active_bg=background, active_fg=foreground)
    return draw_tab_with_fade(themed, screen, tab, before, max_tab_length, index, is_last, extra_data)
