import win32con
import ctypes

# this uses SendInput from Windows API that simulates synthetic mouse / keyboard inputs
# i couldnt get this to work with other libraries i know of so this is a temporary solutionb

# aliases
DWORD, LONG, WORD, UINT, INT = ctypes.c_ulong, ctypes.c_long, ctypes.c_ushort, ctypes.c_uint, ctypes.c_int

# input structures
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', LONG),
        ('dy', LONG),
        ('mouseData', DWORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ctypes.POINTER(DWORD))
    ]
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', WORD),
        ('wScan', WORD),
        ('dwFlags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ctypes.POINTER(DWORD))
    ]
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", DWORD),
        ("wParamL", WORD),
        ("wParamH", WORD),
    ]
class _INPUTunion(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]
class INPUT(ctypes.Structure):
    _fields_ = [
        ('type', DWORD),
        ('union', _INPUTunion)
    ]

class Keyboard:
    """simulate keyboard inputs"""
    def __init__(self):
        self.user32 = ctypes.windll.user32

        # argtypes and restype in SendInput for better type safety
        self.user32.SendInput.argtypes = (UINT, ctypes.POINTER(INPUT), INT)
        self.user32.SendInput.restype = UINT

        # add key mappings
        self.key_mapping = {
            # special keys
            'shift': win32con.VK_SHIFT, 'enter': win32con.VK_RETURN, 'space': win32con.VK_SPACE,
            'tab': win32con.VK_TAB, 'backspace': win32con.VK_BACK, 'escape': win32con.VK_ESCAPE, 'esc': win32con.VK_ESCAPE,
            # arrow keys
            'up': win32con.VK_UP, 'down': win32con.VK_DOWN,
            'left': win32con.VK_LEFT, 'right': win32con.VK_RIGHT,
            # bro...
            '[': 0xDB, ']': 0xDD, '/': 0xBF,
        }
        # add number keys 0-9
        for i in range(10):
            self.key_mapping[str(i)] = ord(str(i))
        # add letter keys a-z
        for i in range(26):
            char = chr(ord('a') + i)
            self.key_mapping[char] = ord(char.upper())

    # create INPUT structure for keyboard events
    def _create_input(self, vk_code: int, key_up: bool = False) -> INPUT:
        inp = INPUT()
        inp.type = win32con.INPUT_KEYBOARD
        inp.union.ki.wVk = vk_code
        inp.union.ki.wScan = self.user32.MapVirtualKeyW(vk_code, 0) # gets hardware scan code for key
        inp.union.ki.dwFlags = win32con.KEYEVENTF_KEYUP if key_up else 0
        inp.union.ki.time = 0
        inp.union.ki.dwExtraInfo = ctypes.pointer(DWORD(0))
        return inp

    # key string or integer to vk code
    def _get_vk_code(self, key):
        if isinstance(key, str):
            return self.key_mapping.get(key.lower())
        elif isinstance(key, int):
            return key
        return None

    # calls SendInput, exception if it fails
    def _send_input(self, inp: INPUT):
        if self.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT)) == 0:
            raise ctypes.WinError()

    def press(self, key):
        """simulate key down event"""
        vk_code = self._get_vk_code(key)
        if vk_code is None:
            raise ValueError(f'unknown key: {key}')
        inp = self._create_input(vk_code, key_up=False)
        self._send_input(inp)

    def release(self, key):
        """simulate key up event"""
        vk_code = self._get_vk_code(key)
        if vk_code is None:
            raise ValueError(f'unknown key: {key}')
        inp = self._create_input(vk_code, key_up=True)
        self._send_input(inp)
