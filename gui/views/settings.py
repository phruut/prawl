
import dearpygui.dearpygui as dpg
from .base import BaseView

class SettingsView(BaseView):
    def build(self):
        with dpg.group(tag='settings_group', show=False):

            # button tabs
            with dpg.group(horizontal=True, show=True):
                # back button
                dpg.add_button(label='ö', width=20, height=20, callback=self.callbacks.show_main_group)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)
                # tab buttons
                with dpg.child_window(width=204, height=20, always_use_window_padding=True):
                    dpg.bind_item_theme(dpg.last_item(), '__groupBackgroundTheme1')
                    with dpg.group(horizontal=True):
                        dpg.add_button(label='loop', tag='settings_tab_loop_button', width=44, height=16, callback=self.callbacks.settings_tab_button)
                        dpg.bind_item_theme(dpg.last_item(), '__activeButtonTheme')
                        dpg.add_button(label='input', tag='settings_tab_input_button', width=44, height=16, callback=self.callbacks.settings_tab_button)
                        dpg.add_button(label='sound', tag='settings_tab_sound_button', width=44, height=16, callback=self.callbacks.settings_tab_button)
                        dpg.add_button(label='other', tag='settings_tab_other_button', width=44, height=16, callback=self.callbacks.settings_tab_button)
                # help button
                dpg.add_button(label='/', width=20, height=20, callback=self.callbacks.show_help_group)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)
            dpg.add_spacer()

            # setup settings pages
            self._settings_loop_group()
            self._settings_input_group()
            self._settings_sound_group()
            self._settings_other_group()

    def _settings_loop_group(self):
        with dpg.group(tag='settings_loop_group', show=True):

            # network mode toggle
            dpg.add_spacer()
            ts = self.add_toggle(
                tag='network_mode',
                label='network monitoring',
                default_value=bool(self.config.settings.get('network', 'network_mode')),
                callback=self.callbacks.toggle_network_mode
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('use network detection instead of timers for match state', wrap=190)

            with dpg.group(tag='network_mode_group', show=bool(self.config.settings.get('network', 'network_mode'))):

                # early disconnect threshold
                dpg.add_spacer()
                self.add_slider_text(
                    tag='early_dc_thresh',
                    width=260, height=20,
                    min_value=0, max_value=99,
                    default_value=int(self.config.settings.get('network', 'early_dc_thresh')),
                    callback=self.callbacks.update_threshold_tooltip,
                    user_data=('early disconnect threshold: ',' %%',' %%')
                )
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('', tag='early_dc_thresh_tooltip_text', wrap=190)
                    self.callbacks.update_threshold_tooltip()

                # network retry amount
                dpg.add_spacer()
                self.add_slider_text(
                    tag='retry_amount',
                    width=260, height=20,
                    min_value=2, max_value=10,
                    default_value=int(self.config.settings.get('network', 'retry_amount')),
                    user_data=('retry: ',' time')
                )
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('amount to retry the disconnect / reconnect sequence before stopping', wrap=190)

                # online mode toggle
                dpg.add_spacer()
                ts = self.add_toggle(
                    tag='online_mode',
                    label='online mode',
                    default_value=bool(self.config.settings.get('network', 'online_mode')),
                    callback=self.callbacks.toggle_online_mode
                )
                with dpg.tooltip(ts.id):
                    dpg.add_text('turn this on if youre using it in ffa or something!', wrap=190)

                with dpg.group(tag='online_mode_group', show=bool(self.config.settings.get('network', 'online_mode'))):

                    # queue wait time
                    dpg.add_spacer()
                    self.add_slider_text(
                        tag='queue_delay',
                        width=260, height=20,
                        min_value=0, max_value=300,
                        default_value=int(self.config.settings.get('network', 'queue_delay')),
                        user_data=('max queue time: ',' second')
                    )
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('max time the script waits in queue for until it stops', wrap=190)

            dpg.add_spacer()
            self.add_separator()

            dpg.add_spacer()
            dpg.add_button(label='starting / restarting', width=260)
            dpg.bind_item_theme(dpg.last_item(), '__centerTitleTheme')

            # spam through lobby
            dpg.add_spacer()
            self.add_slider_text(
                tag='game_start_spam',
                width=260, height=20,
                min_value=5, max_value=30,
                default_value=int(self.config.settings.get('timings', 'game_start_spam')),
                user_data=('before match spam: ',' time')
            )
            with dpg.tooltip(dpg.last_item(), tag='start_spam_tooltip'):
                dpg.add_text('how many times to press going through match result screen etc', wrap=190)

            # wait match load
            dpg.add_spacer()
            self.add_slider_text(
                tag='game_load_delay',
                width=260, height=20,
                min_value=5, max_value=30,
                default_value=int(self.config.settings.get('timings', 'game_load_delay')),
                user_data=('match loading wait: ',' second')
            )
            with dpg.tooltip(dpg.last_item(), tag='wait_gameload_tooltip'):
                dpg.add_text('the time to wait for a match to load until the countdown', wrap=190)

            # restart loop delay
            dpg.add_spacer()
            self.add_slider_text(
                tag='game_restart_delay',
                width=260, height=20,
                min_value=0, max_value=25,
                default_value=int(self.config.settings.get('timings', 'game_restart_delay')),
                user_data=('after match wait: ',' second')
            )
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text('the time to wait after a match finishes before restarting', wrap=190)

            # dc rc options
            dpg.add_spacer()
            self.add_separator()

            dpg.add_spacer()
            dpg.add_button(label='disconnect / reconnect', width=260)
            dpg.bind_item_theme(dpg.last_item(), '__centerTitleTheme')

            # hold to pause
            dpg.add_spacer()
            ts = self.add_toggle(
                tag='open_menu_hold',
                label='hold to pause',
                default_value=bool(self.config.settings.get('timings', 'open_menu_hold')),
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('only works with direct input mode! must enable in brawlhalla: OPTIONS > SYSTEM SETTINGS > HOLD TO PAUSE', wrap=190)

            # disconnect delay
            dpg.add_spacer()
            self.add_slider_text(
                tag='disconnect_delay',
                width=260, height=20,
                min_value=100, max_value=1000,
                default_value=int(self.config.settings.get('timings', 'disconnect_delay')),
                user_data=('menu delay: ',' ms', ' ms')
            )
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text('time to wait for the menu to pop up after pressing menu key', wrap=190)

            # reconnect delay
            dpg.add_spacer()
            self.add_slider_text(
                tag='reconnect_delay',
                width=260, height=20,
                min_value=3, max_value=25,
                default_value=int(self.config.settings.get('timings', 'reconnect_delay')),
                user_data=('reconnect delay: ',' second'))
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text('time to wait before reconnectng to the match', wrap=190)

        with dpg.group(horizontal=True, show=False):
            dpg.add_button(label='W', callback=self.callbacks.reset_general)
            dpg.bind_item_font(dpg.last_item(), self.icon_font)
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text('reset all general settings', tag='reset_general_button_tooltip')
            dpg.add_text('are you sure?', wrap=260, show=False, tag='reset_general_button_text')
            dpg.add_spacer()

    def _settings_input_group(self):
        with dpg.group(tag='settings_input_group', show=False):

            # hotkey buttons row 1
            with dpg.group(horizontal=True):

                # spacer
                dpg.add_button(label='', width=13, height=26)
                dpg.bind_item_theme(dpg.last_item(), '__blankButtonTheme')
                dpg.add_button(label='', width=26, height=26)
                dpg.bind_item_theme(dpg.last_item(), '__blankButtonTheme')

                # up hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_up'), tag='key_up_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_up')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change up key', tag='key_up_tooltip_text')

                # menu key select
                dpg.add_button(label='', width=47, height=26)
                dpg.bind_item_theme(dpg.last_item(), '__blankButtonTheme')
                with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, borders_innerH=False, borders_outerH=False, borders_innerV=False, borders_outerV=False, row_background=False, height=26):
                    dpg.bind_item_theme(dpg.last_item(), '__layoutTableTheme')
                    for _ in range(3):
                        dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.group():
                            self.add_separator(width=0, height=2)
                            dpg.add_button(label='esc', tag='key_menu_esc_button', width=37, height=22, callback=self.callbacks.menu_key_button)
                            with dpg.tooltip(dpg.last_item()):
                                dpg.add_text('use esc key to open menu')
                        self.add_separator(width=4, height=26, rounding=10)
                        with dpg.group():
                            self.add_separator(width=0, height=2)
                            dpg.add_button(label='enter', tag='key_menu_enter_button', width=37, height=22, callback=self.callbacks.menu_key_button)
                            with dpg.tooltip(dpg.last_item()):
                                dpg.add_text('use enter key to open menu')
                    if self.config.settings.get('input', 'key_menu') == 'esc':
                        self.interface.bind_item_theme('key_menu_esc_button', '__activeButtonTheme')
                    else:
                        self.interface.bind_item_theme('key_menu_esnter_button', '__activeButtonTheme')

            # hotkey buttons row 2
            dpg.add_spacer()
            with dpg.group(horizontal=True):

                # spacer
                dpg.add_button(label='', width=13, height=26)
                dpg.bind_item_theme(dpg.last_item(), '__blankButtonTheme')

                # left hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_left'), tag='key_left_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_left')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change left key', tag='key_left_tooltip_text')

                # down hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_down'), tag='key_down_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_down')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change down key', tag='key_down_tooltip_text')

                # down hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_right'), tag='key_right_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_right')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change right key', tag='key_right_tooltip_text')

                # down hotkey button
                dpg.add_spacer(width=13)
                dpg.add_button(label=self.config.settings.get('input', 'key_throw'), tag='key_throw_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_throw')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change throw weapon key', tag='key_throw_tooltip_text')

                # down hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_light'), tag='key_light_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_light')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change light attack key', tag='key_light_tooltip_text')

                # down hotkey button
                dpg.add_button(label=self.config.settings.get('input', 'key_heavy'), tag='key_heavy_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_heavy')
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('change heavy attack key', tag='key_heavy_tooltip_text')

            # save hotkey values lol
            dpg.add_text(default_value=self.config.settings.get('input', 'key_menu'), tag='key_menu', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_up'), tag='key_up', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_left'), tag='key_left', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_down'), tag='key_down', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_right'), tag='key_right', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_throw'), tag='key_throw', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_light'), tag='key_light', show=False)
            dpg.add_text(default_value=self.config.settings.get('input', 'key_heavy'), tag='key_heavy', show=False)

            # direct input mode
            dpg.add_spacer()
            ts = self.add_toggle(
                tag='direct_input',
                label='direct input mode',
                default_value=bool(self.config.settings.get('input', 'direct_input'))
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('wont work in background! try this if you are having issues with inputs', wrap=190)

            # input duration / delay
            dpg.add_spacer()
            with dpg.group(horizontal=True):
                self.add_slider_text(
                    tag='keypress_hold',
                    width=126, height=20,
                    min_value=0, max_value=200,
                    default_value=int(self.config.settings.get('input', 'keypress_hold')),
                    user_data=('hold ', ' ms', ' ms')
                )
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('average hold duration of the key', wrap=190)
                self.add_slider_text(
                    tag='keypress_delay',
                    width=126, height=20,
                    min_value=50, max_value=300,
                    default_value=int(self.config.settings.get('input', 'keypress_delay')),
                    user_data=('delay ',' ms',' ms')
                )
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('time to wait after a key is pressed', wrap=190)

    def _settings_sound_group(self):
        with dpg.group(tag='settings_sound_group', show=False):

            with dpg.group(horizontal=True):
                ts = self.add_toggle(
                    tag='timer_sound',
                    label='timer sound',
                    width=204,
                    default_value=bool(self.config.settings.get('sound', 'timer_sound'))
                )
                with dpg.tooltip(ts.id):
                    dpg.add_text('plays a sound after the timer ends', wrap=190)
                dpg.add_button(label='Ù', callback=self.callbacks.beep_sound)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('boop')
                dpg.add_button(label='W', callback=self.callbacks.beep_reset)
                dpg.bind_item_font(dpg.last_item(), self.icon_font)
                with dpg.tooltip(dpg.last_item()):
                    dpg.add_text('reset')

            dpg.add_spacer()
            self.add_separator()

            dpg.add_spacer()
            self.add_slider_text(
                tag='beep_frequency',
                width=260, height=20,
                min_value=100, max_value=2000,
                default_value=int(self.config.settings.get('sound', 'beep_frequency')),
                user_data=('frequency: ', ' hz', ' hz')
            )
            dpg.add_spacer()
            self.add_slider_text(
                tag='beep_duration',
                width=260, height=20,
                min_value=10, max_value=1000,
                default_value=int(self.config.settings.get('sound', 'beep_duration')),
                user_data=('duration: ', ' ms', ' ms')
            )

    def _settings_other_group(self):
        with dpg.group(tag='settings_other_group', show=False):

            # always on top
            ts = self.add_toggle(
                tag='always_on_top',
                label='always on top',
                default_value=bool(self.config.settings.get('other', 'always_on_top')),
                callback=self.callbacks.update_aot
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('makes this window stay on top')

            # launch with prawl
            dpg.add_spacer()
            ts = self.add_toggle(
                tag='auto_launch',
                label='launch brawlhalla with prawl',
                default_value=bool(self.config.settings.get('other', 'auto_launch'))
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('launches brawlhalla when you launch prawl')

            # exp multiplier
            dpg.add_spacer()
            self.add_slider_text(
                tag='exp_multiplier',
                width=260, height=20,
                min_value=1, max_value=3,
                default_value=int(self.config.settings.get('other', 'exp_multiplier')),
                user_data=('exp multiplier: ', 'x', 'x'),
            )
            with dpg.tooltip(dpg.last_item()):
                dpg.add_text('for double exp events etc', wrap=190)

            # rate limits
            dpg.add_spacer()
            self.add_separator()

            dpg.add_spacer()
            ts = self.add_toggle(
                tag='rate_limit_detect',
                label='rate limit detection',
                default_value=bool(self.config.settings.get('other', 'rate_limit_detect')),
                callback=self.callbacks.rate_limit_detect
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('detects if you are rate limited in exp/gold')
            with dpg.group(tag='rate_limit_wait_group'):
                dpg.add_spacer()
                ts = self.add_toggle(
                    tag='rate_limit_wait',
                    label='rate limit auto wait',
                    default_value=bool(self.config.settings.get('other', 'rate_limit_wait')),
                    callback=self.callbacks.rate_limit_wait
                )
                with dpg.tooltip(ts.id):
                    dpg.add_text('waits for rate limit reset and starts farming')
                dpg.add_spacer(height=0, tag='rate_limit_wait_time_spacer')
                self.add_slider_text(
                    tag='rate_limit_wait_time',
                    width=260, height=20,
                    min_value=30, max_value=60,
                    default_value=int(self.config.settings.get('other', 'rate_limit_wait_time')),
                    user_data=('wait ', ' minute'),
                    show=False
                )
                if self.config.settings.get('other', 'rate_limit_wait'):
                    dpg.configure_item('rate_limit_wait_time', show=True)
            with dpg.tooltip(dpg.last_item(), tag='rate_limit_wait_time_tooltip'):
                dpg.add_text('time to wait for rate limit to reset')

            # max games
            dpg.add_spacer()
            ts = self.add_toggle(
                tag='max_games',
                label='max games',
                default_value=bool(self.config.settings.get('other', 'max_games')),
                callback=self.callbacks.max_games
            )
            with dpg.tooltip(ts.id):
                dpg.add_text('stops after set amount of games')
            dpg.add_spacer(height=0, tag='max_games_spacer')
            self.add_slider_text(
                tag='max_games_amount',
                width=260, height=20,
                min_value=1, max_value=99,
                default_value=int(self.config.settings.get('other', 'max_games_amount')),
                user_data=('stop after: ', ' game'),
                show=False
            )
            with dpg.tooltip(dpg.last_item(), tag='max_games_amount_tooltip'):
                dpg.add_text('the amount of games to stop at')
            if self.config.settings.get('other', 'max_games'):
                dpg.configure_item('max_games', show=False)

            # idk
            dpg.add_spacer()
            self.add_separator()

            dpg.add_spacer()
            with dpg.collapsing_header(label='lobby setup (experimental)', bullet=True):
                dpg.add_spacer()
                dpg.add_text('always create a new custom game room before you use these setup buttons (still buggy)', wrap=0)
                dpg.add_spacer()
                with dpg.group(horizontal=True):
                    dpg.add_button(label='STOP', callback=self.callbacks.stop_button)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('stop setup')
                    dpg.add_button(label='MINI LOBBY SETUP', callback=self.callbacks.mini_lobby_setup_start)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('only game rules')
                    dpg.add_button(label='FULL LOBBY SETUP', callback=self.callbacks.full_lobby_setup_start)
                    with dpg.tooltip(dpg.last_item()):
                        dpg.add_text('game rules, lobby rules, bots, handicaps')
