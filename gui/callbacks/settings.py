import winsound
import threading
from typing import Any

class SettingsCallbacks:
    interface: Any
    config: Any
    listener: Any
    farmer: Any
    process: Any
    hwnd: Any

    # ui settings tab buttons
    # ----------------------------------------------

    def settings_tab_button(self, sender, app_data, user_data):
        tabs = {
            'settings_tab_loop_button':  'settings_loop_group',
            'settings_tab_input_button': 'settings_input_group',
            'settings_tab_sound_button': 'settings_sound_group',
            'settings_tab_other_button': 'settings_other_group',
        }
        for button_id, group_id in tabs.items():
            if button_id == sender:
                self.interface.bind_item_theme(button_id, '__activeButtonTheme')
                self.interface.show(group_id)
            else:
                self.interface.bind_item_theme(button_id, 0)
                self.interface.hide(group_id)

    # loop tab
    # ----------------------------------------------

    # network mode toggle
    def toggle_network_mode(self, sender, app_data, user_data):
        self.interface.configure('network_settings_group', show=app_data)
        self.update_threshold_tooltip()

    # threshold calculate
    def update_threshold_tooltip(self, sender=None, app_data=None):
        match_time = self.interface.get('match_time')
        threshold = self.interface.get('early_dc_thresh')
        threshold_minutes = (match_time * threshold) / 100
        minutes = int(threshold_minutes)
        seconds = int((threshold_minutes % 1) * 60)
        self.interface.set('early_dc_thresh_tooltip_text', f'if the match disconnects before {minutes}:{seconds:02}, assume it to be a network error and farming will stop')

    # open menu hold toggle
    def select_open_menu_hold(self, sender, app_data, user_data):
        if self.interface.get('open_menu_hold'):
            self.interface.set('open_menu_default', False)
        else:
            self.interface.set('open_menu_default', True)

    # input tab
    # ----------------------------------------------

    # change hotkey
    def hotkey_button(self, sender, app_data, user_data):
        key_tag = user_data

        # disable all hotkey buttons so they dont overlap
        key_names = ['key_menu', 'key_up', 'key_down', 'key_left', 'key_right', 'key_light', 'key_heavy', 'key_throw']
        for tag in key_names:
            self.interface.configure(f'{tag}_button', enabled=False)

        # change button label and tooltip
        self.interface.configure(f'{key_tag}_button', label='...')
        self.interface.set(f'{key_tag}_tooltip_text', 'waiting for key, esc to cancel')

        def listen_and_update():
            hotkey = self.listener.hotkey()
            def update_ui():

                # esc to cancel
                save_hotkey = None
                if hotkey in ['esc']:
                    pass
                else:
                    # check if hotkey is already set to another one, then set config value
                    save_hotkey = hotkey
                    for tag in key_names:
                        existing_val = self.interface.get(tag)
                        if existing_val == hotkey:
                            self.interface.configure(f'{tag}_button', label='...')
                            self.interface.set(tag, '')
                    self.interface.set(key_tag, save_hotkey)

                # change the hotkey button label and tooltip back
                text = ' '.join(reversed(key_tag.split('_')))
                self.interface.set(f'{key_tag}_tooltip_text', f'change {text}')
                self.interface.configure(f'{key_tag}_button', label=self.interface.get(key_tag))

                # enable the buttons again
                for tag in key_names:
                    self.interface.configure(f'{tag}_button', enabled=True)

            self.interface.queue_callback(update_ui)
        threading.Thread(target=listen_and_update, daemon=True).start()

    # esc or enter key select
    def menu_key_button(self, sender, app_data, user_data):
        btn_esc = 'key_menu_esc_button'
        btn_enter = 'key_menu_enter_button'
        if sender == btn_esc:
            self.interface.bind_item_theme(btn_esc, '__activeButtonTheme')
            self.interface.bind_item_theme(btn_enter, 0)
            self.interface.set('key_menu', 'esc')
        elif sender == btn_enter:
            self.interface.bind_item_theme(btn_esc, 0)
            self.interface.bind_item_theme(btn_enter, '__activeButtonTheme')
            self.interface.set('key_menu', 'enter')

    # sound tab
    # ----------------------------------------------

    # frequency
    def beep_sound(self):
        winsound.Beep(self.interface.get('beep_frequency'), self.interface.get('beep_duration'))

    # duration
    def beep_reset(self):
        self.interface.set('beep_frequency', 500)
        self.interface.set('beep_duration', 72)

    # other tab
    # ----------------------------------------------

    # always on top toggle
    def update_aot(self, sender, app_data, user_data):
        self.interface.set_viewport_always_top(app_data)

    # rate limit
    def rate_limit_detect(self, sender, app_data, user_data):
        if app_data:
            self.interface.show('rate_limit_wait_group')
        else:
            self.interface.hide('rate_limit_wait_group')

    def rate_limit_wait(self, sender, app_data, user_data):
        if app_data:
            self.interface.show('rate_limit_wait_time_spacer')
            self.interface.show('rate_limit_wait_time_tooltip')
            self.interface.show('rate_limit_wait_time')
        else:
            self.interface.hide('rate_limit_wait_time_spacer')
            self.interface.hide('rate_limit_wait_time_tooltip')
            self.interface.hide('rate_limit_wait_time')

    # max game limit
    def max_games(self, sender, app_data, user_data):
        if app_data:
            self.interface.show('max_games_spacer')
            self.interface.show('max_games_tooltip')
            self.interface.show('max_games_amount')
        else:
            self.interface.hide('max_games_spacer')
            self.interface.hide('max_games_tooltip')
            self.interface.hide('max_games_amount')

    # lobby setup buttons
    def mini_lobby_setup_start(self):
        self.hwnd = self.process.get_hwnd()
        if self.hwnd:
            self.interface.configure('run_button', label='ä')
            self.interface.configure('run_button_tooltip', default_value='stop')
            self.farmer.start(0, ['lobby_setup_gamerule', 'lobby_setup_exit', 'stop_farmer'])

    def full_lobby_setup_start(self):
        self.hwnd = self.process.get_hwnd()
        if self.hwnd:
            self.interface.configure('run_button', label='ä')
            self.interface.configure('run_button_tooltip', default_value='stop')
            self.farmer.start(0, ['lobby_setup_gamerule', 'lobby_setup_lobby', 'lobby_setup_exit', 'lobby_setup_party', 'stop_farmer'])
