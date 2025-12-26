from typing import Any

class MiscCallbacks:
    interface: Any
    timing_count: int
    timing_timer: Any

    # ui main, settings, help nav buttons
    # ----------------------------------------------

    def show_main_group(self, sender, app_data, user_data):
        self.interface.show('main_group')
        self.interface.hide('settings_group')
        self.interface.hide('help_group')

    def show_settings_group(self, sender, app_data, user_data):
        self.interface.hide('main_group')
        self.interface.show('settings_group')
        self.interface.hide('help_group')

    def show_help_group(self, sender, app_data, user_data):
        self.interface.hide('main_group')
        self.interface.hide('settings_group')
        self.interface.show('help_group')

    # ehh
    # ----------------------------------------------

    def _general_state_reset(self):
        self.timing_count = 0
        self.interface.configure('reset_general_button_text', show=False)
        self.interface.configure('reset_general_button_tooltip', default_value='reset all general settings')

    def reset_general(self):
        self.timing_count += 1
        if self.timing_count == 1:
            self.interface.configure('reset_general_button_text', show=True)
            self.interface.configure('reset_general_button_tooltip', default_value='click again to reset')
            self.timing_timer.start()
        elif self.timing_count == 2:
            self.interface.configure('reset_general_button_text', show=False)
            self.interface.configure('reset_general_button_tooltip', default_value='reset all general settings')
            self.interface.set('start_spam', 10)
            self.interface.set('wait_restart', 4)
            self.interface.set('wait_gameload', 15)
            self.interface.set('menu_key_presses', 2)
            self.interface.set('wait_disconnect', 100)
            self.interface.set('wait_reconnect', 4)
            self.interface.set('keypress_hold', 70)
            self.interface.set('keypress_delay', 150)
            self.timing_count = 0
            self.timing_timer.cancel()
