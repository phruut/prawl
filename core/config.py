import os
import sys
import configparser
import dearpygui.dearpygui as dpg

# platform thing
def get_platform():
    platform = sys.platform
    if platform.lower().startswith('win'):
        return platform
    else:
        print('unsupported operating system, please use windows!')

# handles paths properly when compiled or running from source
def script_dir():
    if getattr(sys, 'frozen', False):
        # for running as executable
        return os.path.dirname(sys.executable)
    else:
        # for running as script
        return os.path.dirname(os.path.abspath(sys.argv[0]))

class Config:
    def __init__(self, filepath='config.ini'):
        self.version = '0.1.2'
        self.filepath = os.path.join(script_dir(), filepath)
        self.icon = os.path.join(script_dir(), 'res/prawl-app.ico')
        self.main_font = os.path.join(script_dir(), 'res/cq-pixel-min.ttf')
        self.icon_font = os.path.join(script_dir(), 'res/Piconic.ttf')
        self.defaults = {
            'match_time': 25,
            'timer_sound': False,
            'always_on_top': True,
            'game_start_spam': 12,
            'game_restart_delay': 4,
            'game_load_time': 15,
            'menu_key_presses': 2,
            'disconnect_delay': 100,
            'reconnect_delay': 4,
            'open_menu_default': True,
            'open_menu_fix': False,
            'open_menu_fix2': False,
            'open_menu_hold': False,
            'open_menu_enter': True,
            'direct_input': False,
            'keypress_hold': 70,
            'keypress_delay': 150,
            'beep_frequency': 500,
            'beep_duration': 72,
            'rate_limit_detect': True,
            'rate_limit_wait': True,
            'rate_limit_wait_time': 45,
            'max_games': False,
            'max_games_amount': 16,
            'auto_launch': False,
            'key_light': 'c',
            'key_heavy': 'x',
            'key_throw': 'v',
            'key_left': 'left',
            'key_up': 'up',
            'key_right': 'right',
            'key_down': 'down',
        }
        self.config = configparser.ConfigParser()
        self.data = {}
        self.load()

    def load(self):
        self.config.read(self.filepath)

        if not self.config.has_section('settings'):
            self.config.add_section('settings')

        updated = False
        for key, value in self.defaults.items():
            if not self.config.has_option('settings', key):
                self.config.set('settings', key, str(value))
                updated = True

        if updated:
            with open(self.filepath, 'w') as f:
                self.config.write(f)

        for key, default_value in self.defaults.items():
            val_str = self.config.get('settings', key)
            try:
                if isinstance(default_value, bool):
                    self.data[key] = self.config.getboolean('settings', key)
                elif isinstance(default_value, int):
                    self.data[key] = self.config.getint('settings', key)
                elif isinstance(default_value, float):
                    self.data[key] = self.config.getfloat('settings', key)
                else:
                    self.data[key] = val_str
            except ValueError:
                self.data[key] = default_value

    def save(self):
        if not self.config.has_section('settings'):
            self.config.add_section('settings')

        for key in self.defaults.keys():
            dpg_tag = key
            if dpg.does_item_exist(dpg_tag):
                value = dpg.get_value(dpg_tag)
                self.data[key] = value
                self.config.set('settings', key, str(value))

        with open(self.filepath, 'w') as f:
            self.config.write(f)
