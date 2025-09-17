import time
import random
import win32api
import win32con
import dearpygui.dearpygui as dpg
from scripts.window import activate
from scripts._direct import Keyboard

class KeyListener:
    def __init__(self):
        self.VK_CODE = {
            'enter':13, 'esc':27, 'spacebar':32,
            'left':37, 'up':38, 'right':39, 'down':40,
            '0':48, '1':49, '2':50, '3':51, '4':52, '5':53, '6':54, '7':55, '8':56, '9':57,
            'a':65, 'b':66, 'c':67, 'd':68, 'e':69, 'f':70, 'g':71, 'h':72, 'i':73, 'j':74, 'k':75, 'l':76, 'm':77,
            'n':78, 'o':79, 'p':80, 'q':81, 'r':82, 's':83, 't':84, 'u':85, 'v':86, 'w':87, 'x':88, 'y':89, 'z':90,
            'numpad_0':96, 'numpad_1':97, 'numpad_2':98, 'numpad_3':99, 'numpad_4':100, 'numpad_5':101, 'numpad_6':102, 'numpad_7':103, 'numpad_8':104, 'numpad_9':105,
            'left_shift':160, 'right_shift':161, 'left_control':162, 'right_control':163,
            '+':187, ',':188, '-':189, '.':190, '/':191, '`':192, ';':186, '[':219, '\\':220, ']':221, "'":222
        }
        self.VK_NAME = {v: k for k, v in self.VK_CODE.items()}

    def hotkey(self):
        while any(win32api.GetAsyncKeyState(key) for key in self.VK_CODE.values()):
            time.sleep(0.01)
        while True:
            for key_code in self.VK_NAME:
                if win32api.GetAsyncKeyState(key_code) & 0x8000:
                    key_name = self.VK_NAME[key_code]
                    if key_name == 'esc':
                        return None
                    return key_name
            time.sleep(0.01)

class KeySequence:
    def __init__(self, config, keyboard: Keyboard):
        self.keyboard = keyboard
        self.config = config
        self._cache = None
        self._last_d = None
        self._last_a = None
        self._last_menu_k = None

    def _keypress(self, hwnd, key, hold=70, delay=150, direct=False):
        vk = win32api.VkKeyScan(key) if isinstance(key, str) else key
        hold = random.uniform((hold-10),(hold+20))/1000
        delay = random.uniform(delay, (delay+40))/1000
        if direct:
            self.keyboard.press(key)
            time.sleep(hold)
            self.keyboard.release(key)
            time.sleep(delay)
        else:
            win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(hold)
            win32api.SendMessage(hwnd, win32con.WM_KEYUP, vk, 0)
            time.sleep(delay)

    def _build(self, time_d, time_c, menu_k, hwnd):
        left_k, up_k, down_k, esc = self.config['key_left'], self.config['key_up'], self.config['key_down'], win32con.VK_ESCAPE
        throw_k, light_k, heavy_k = self.config['key_throw'], self.config['key_light'], self.config['key_heavy']

        sequences_data = {
            'wait_restart': [
                ('countdown', 'wait_restart', 'starting game in {}...'),
            ],
            'spam_menu': [
                ('status', 'spamming through menu!'),
                ('press', light_k, {'count': 'start_spam'}),
                ('countdown', 'wait_gameload', 'waiting for game {}...'),
            ],
            'open_menu': [
                ('status', 'open esc menu'),
                ('press', menu_k, {'count': 'menu_key_presses'}),
            ],
            'disconnect': [
                ('status', 'wait disconnect delay'),
                ('wait', 'wait_disconnect'),
                ('press', up_k),
                ('press', light_k),
            ],
            'reconnect': [
                ('countdown', 'wait_reconnect', 'reconnecting in {}...'),
                ('status', 'pressing...'),
                ('press', light_k, {'count': 2}),
            ],
            'open_menu_fix': [
                ('status', 'esc menu fix...'),
                ('press', menu_k),
                ('press', up_k),
                ('press', light_k),
            ],
            'open_menu_hold': [
                ('status', 'open esc menu (hold)'),
                ('press', menu_k, {'count': 2}),
                ('press', menu_k, {'hold': 2}),
            ],
            'lobby_setup_game_rules': [
                ('status', 'GAME RULES'), ('press', heavy_k),
                ('status', 'selecting CREW BATTLE'), ('press', left_k, {'count': 6}),
                ('status', 'setting LIVES to 99'), ('press', down_k, {'count': 3}), ('press', left_k, {'count': 3}),
                ('status', f'setting MATCH TIME {dpg.get_value("match_time")}'), ('press', down_k), ('press', time_d, {'count': time_c}),
                ('status', 'setting DAMAGE'), ('press', down_k, {'count': 2}), ('press', left_k, {'count': 5}),
                ('status', 'turning gadgets off'), ('press', down_k, {'count': 2}), ('press', left_k),
                ('status', 'maps to Tournament 1v1'), ('press', down_k, {'count': 3}), ('press', left_k, {'count': 2}),
                ('status', 'setting MAX PLAYERS to 2'), ('press', down_k), ('press', left_k, {'count': 2}),
            ],
            'lobby_setup_lobby': [
                ('status', 'LOBBY'), ('press', ']'),
                ('status', 'turning off FRIENDS'), ('press', down_k, {'count': 3}), ('press', left_k),
                ('status', 'turning off CLANMATES'), ('press', down_k), ('press', left_k),
                ('status', 'setting MAP CHOOSING to Random'), ('press', down_k, {'count': 2}), ('press', left_k, {'count': 2}),
                ('status', 'turning on ALLOW HANDICAPS'), ('press', down_k, {'count': 2}), ('press', left_k),
            ],
            'lobby_setup_party': [
                ('status', 'opening MANAGE PARTY menu'), ('press', throw_k),
                ('status', 'adding and opening BOT menu'), ('press', light_k, {'count': 2, 'delay': 0.5}),
                ('status', 'set LIVES to 89'), ('press', down_k), ('press', left_k, {'count': 10}),
                ('status', 'set Dmg Done 50%'), ('press', down_k), ('press', left_k, {'count': 5}),
                ('status', 'set Dmg Taken 50%'), ('press', down_k), ('press', left_k, {'count': 5}),
                ('status', 'switching to P1 menu'), ('press', light_k), ('press', up_k), ('press', light_k),
                ('status', 'set Dmg Done 50%'), ('press', down_k, {'count': 2}), ('press', left_k, {'count': 5}),
                ('status', 'set Dmg Taken 50%'), ('press', down_k), ('press', left_k, {'count': 5}),
                ('status', 'close MANAGE PARTY menu'), ('press', throw_k)
            ],
            'lobby_setup_finish': [
                ('press', light_k, {'delay': 0.5}),
            ]
        }

        action_map = {}
        for name, steps in sequences_data.items():
            action_list = []
            for step in steps:
                command, args = step[0], step[1:]

                if command == 'status':
                    action_list.append((lambda l=args[0]: dpg.configure_item('farm_status', label=l), 0))

                elif command == 'wait':
                    delay_sec = dpg.get_value(args[0]) / 1000
                    action_list.append((lambda: None, delay_sec))

                elif command == 'countdown':
                    duration_tag, label_template = args[0], args[1]
                    duration = dpg.get_value(duration_tag)
                    for i in range(duration):
                        label = label_template.format(duration - i)
                        action_list.append((lambda l=label: dpg.configure_item('farm_status', label=l), 1))

                elif command == 'press':
                    key = args[0]
                    overrides = args[1] if len(args) > 1 else {}

                    count_val = overrides.get('count', 1)
                    num_repeats = dpg.get_value(count_val) if isinstance(count_val, str) else count_val

                    hold_default = overrides.get('hold', dpg.get_value('keypress_hold'))
                    delay_after = overrides.get('delay', 0)

                    for _ in range(num_repeats):
                        action = (lambda k=key, h=hold_default: self._keypress(hwnd, k, h, dpg.get_value('keypress_delay'), dpg.get_value('direct_input')), delay_after)
                        action_list.append(action)

            action_map[name] = action_list
        return action_map

    def action(self, sequences, is_running, hwnd):
        def scrolls(start, target, pos=25):
            r_scroll = (target - start) % pos
            l_scroll = (start - target) % pos
            return (self.config['key_right'], r_scroll) if r_scroll <= l_scroll else (self.config['key_left'], l_scroll)

        TIME_D, TIME_C = scrolls(20, dpg.get_value('match_time'))
        MENU_K = win32con.VK_RETURN if dpg.get_value('open_menu_enter') else win32con.VK_ESCAPE

        action_map = self._build(TIME_D, TIME_C, MENU_K, hwnd)
        actions = [action for seq in sequences if seq in action_map for action in action_map[seq]]
        for action, delay in actions:
            if not is_running(): break
            if dpg.get_value('direct_input'): activate(hwnd)
            action()
            if delay >= 1:
                for _ in range(int(delay)):
                    if not is_running(): break
                    time.sleep(1)
            else:
                time.sleep(delay)
