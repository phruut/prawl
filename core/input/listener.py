import time
import win32api
from ._codes import VK_CODE, VK_NAME

class KeyListener:
    def hotkey(self):
        while any(win32api.GetAsyncKeyState(key) for key in VK_CODE.values()):
            time.sleep(0.01)
        while True:
            for key_code in VK_NAME:
                if win32api.GetAsyncKeyState(key_code) & 0x8000:
                    return VK_NAME[key_code]
            time.sleep(0.01)
