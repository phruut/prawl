from pathlib import Path
from .base import Base, data_dir

class SettingsConfig(Base):
    DEFAULTS = {
        'timings': {
            'match_time': 25,
            'game_start_spam': 12,
            'game_load_delay': 15,
            'disconnect_delay': 100,
            'reconnect_delay': 4,
            'game_restart_delay': 4,
            'open_menu_hold': False,
        },
        'network': {
            'network_mode': False,
            'retry_amount': 5,
            'early_dc_thresh': 90,
            'online_mode': False,
            'queue_delay': 300
            #'timeout_wait': 60,
            #'connection_stabilize': 10,
            #'disconnect_stabilize': 5,
            #'early_dc_thresh': False,
            #'early_dc_thresh_mode': 'percentage',
            #'early_dc_thresh_perc': 90,
            #'early_dc_thresh_time': 5,
            #'auto_network': False, # auto updating network config
        },
        'input': {
            'keypress_hold': 70,
            'keypress_delay': 150,
            'direct_input': False,
            'key_menu': 'esc',
            'key_up': 'up',
            'key_down': 'down',
            'key_left': 'left',
            'key_right': 'right',
            'key_throw': 'v',
            'key_light': 'c',
            'key_heavy': 'x',
        },
        'sound': {
            'timer_sound': False,
            'beep_frequency': 500,
            'beep_duration': 72,
        },
        'other': {
            'always_on_top': True,
            'auto_launch': False,
            'exp_multiplier': 1,
            'rate_limit_detect': True,
            'rate_limit_wait': True,
            'rate_limit_wait_time': 45,
            'max_games': False,
            'max_games_amount': 16,
            'auto_update': False,
        },
    }

    def __init__(self, filepath=None):
        path = Path(filepath) if filepath else data_dir() / 'settings.cfg'
        super().__init__(path, self.DEFAULTS)
