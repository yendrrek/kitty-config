"""Paste text from the clipboard, or forward Ctrl+V when the clipboard holds an image.

Kitty's paste_from_clipboard only handles text, so an image on the clipboard is
dropped. Programs such as Claude Code read the image from the clipboard themselves
when they receive Ctrl+V, so the key press has to reach them.
"""

import shutil
import subprocess
from typing import Any

from kittens.tui.handler import result_handler


def main(args: list[str]) -> str:
    return ''


def _clipboard_targets() -> list[str]:
    if shutil.which('wl-paste'):
        command = ['wl-paste', '--list-types']
    elif shutil.which('xclip'):
        command = ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o']
    else:
        return []
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=2, check=False)
    except (OSError, subprocess.SubprocessError):
        return []
    return result.stdout.split()


def _clipboard_has_image() -> bool:
    return any(target.startswith('image/') for target in _clipboard_targets())


@result_handler(no_ui=True)
def handle_result(args: list[str], answer: str, target_window_id: int, boss: Any) -> None:
    window = boss.window_id_map.get(target_window_id)
    if window is None:
        return
    if _clipboard_has_image():
        window.send_key('ctrl+v')
    else:
        boss.paste_from_clipboard()
