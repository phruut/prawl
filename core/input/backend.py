import random
import win32api
import win32gui
import win32con
from ._direct import Keyboard
from ._codes import VK_CODE, EXTENDED_KEYS
from .._utils import sleep

import logging
logger = logging.getLogger('prawl')

def resolve_key(key):
    """defined key string or char to vk code"""
    if isinstance(key, int):
        return key

    key_lower = str(key).lower()
    if key_lower in VK_CODE:
        return VK_CODE[key_lower]

    # fallback if its not in map
    return win32api.VkKeyScan(key) & 0xFF

class InputBackend:
    def __init__(self, process, interface):
        self.process = process
        self.interface = interface
        self.direct_kb = Keyboard()

    def press(self, key_name, hold_ms=70, delay_ms=150):
        """press key"""
        hwnd = self.process.get_hwnd()
        if not hwnd:
            return

        hold_sec = random.uniform(hold_ms - 10, hold_ms + 20) / 1000.0
        delay_sec = random.uniform(delay_ms - 5, delay_ms + 20) / 1000.0

        logger.info(f'pressing key: {key_name} | hold: {hold_sec} | delay: {delay_sec}')

        if self.interface.get('direct_input'):
            self.process.activate()
            self.direct_kb.press(key_name)
            sleep(hold_sec)
            self.direct_kb.release(key_name)
        else:
            vk = resolve_key(key_name)
            scan_code = win32api.MapVirtualKey(vk, 0)
            lparam = 1 | (scan_code << 16)
            if vk in EXTENDED_KEYS:
                lparam |= (1 << 24)

            win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, lparam)
            sleep(hold_sec)
            win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk, lparam | 0xC0000000)

        sleep(delay_sec)

    def release_all(self):
        """releases all keys"""
        hwnd = self.process.get_hwnd()
        keys = ['key_left', 'key_up', 'key_down', 'key_right', 'key_light', 'key_heavy', 'key_throw']

        for name in keys:
            key_val = self.interface.get(name)

            if self.interface.get('direct_input'):
                try:
                    self.direct_kb.release(key_val)
                except Exception:
                    pass
            elif hwnd:
                try:
                    vk = resolve_key(key_val)
                    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk, 0)
                except Exception:
                    pass

        logger.info('released all keys')
