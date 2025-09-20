import dearpygui.dearpygui as dpg
import webbrowser
from gui._themes import create_themes, create_fonts
from gui._callbacks import Callbacks

class PrawlGUI:
    def __init__(self, config, main_font, icon_font, timer, keyseq, state, update):

        self.config = config
        self.timer = timer
        self.keyseq = keyseq
        self.state = state
        self.update = update
        self.callbacks = Callbacks(self)
        self.timer.set_on_stop_callback(self.callbacks.on_timer_stopped)

        dpg.create_context()
        create_themes()
        self.main_font, self.icon_font = create_fonts(main_font, icon_font)
        self._create_widgets()

    def _hyperlink(self, text, address):
        with dpg.group(horizontal=True):
            dpg.add_text(f'(', color=(100, 149, 238))
            dpg.bind_item_font(dpg.last_item(), self.icon_font)
            dpg.add_button(label=text, callback=lambda: webbrowser.open(address))
            dpg.bind_item_theme(dpg.last_item(), "__hyperlinkTheme")

    def _create_widgets(self):
        config = self.config
        with dpg.window(tag='main'):
            dpg.bind_item_theme(dpg.last_item(), '__windowTheme')
            dpg.bind_font(self.main_font)

            # main page
            with dpg.group(tag='main_group', show=True):
                with dpg.group(horizontal=True):
                    with dpg.group():
                        with dpg.group():
                            dpg.add_slider_int(min_value=1, max_value=25, default_value=int(config.get('match_time', 25)), width=168, height=20, tag='match_time', callback=self.callbacks.match_time_slider)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('', tag='estimated_values');self.callbacks.update_values(None, config.get('match_time', 25))
                            dpg.add_spacer(height=0.5)
                            self.callbacks.update_slider_format(int(self.config.get('match_time', 25)))

                        # buttons
                        with dpg.group(horizontal=True):
                            dpg.add_button(label='P', width=36, height=28, callback=self.callbacks.show_settings_group)
                            dpg.bind_item_font(dpg.last_item(), self.icon_font)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('settings')
                            dpg.add_button(label='Ó', width=36, height=28, callback=self.callbacks.oops_button)
                            dpg.bind_item_font(dpg.last_item(), self.icon_font)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('retry dc / rc (oops)')
                            dpg.add_button(label='O', width=36, height=28, tag='toggle_button', callback=self.callbacks.toggle_button)
                            dpg.bind_item_font(dpg.last_item(), self.icon_font)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('hide brawlhalla window', tag='toggle_button_tooltip')
                            dpg.add_button(label='\\', width=36, height=28, callback=self.callbacks.launch_button)
                            dpg.bind_item_font(dpg.last_item(), self.icon_font)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('start brawlhalla', tag='launch_button_tooltip')

                        # stats
                        dpg.add_spacer(height=0.5)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label=self.state['total_games'], width=20, height=20, tag='total_games')
                            dpg.bind_item_theme(dpg.last_item(), '__gameTextTheme')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('total games')
                            dpg.add_button(label=self.state['total_gold'], width=66, height=20, tag='total_gold')
                            dpg.bind_item_theme(dpg.last_item(), '__goldTextTheme')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('total gold')
                            dpg.add_button(label=self.state['total_exp'], width=66, height=20, tag='total_exp')
                            dpg.bind_item_theme(dpg.last_item(), '__expTextTheme')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('total exp')

                    # biiig button
                    dpg.add_button(label='â', tag='run_button', width=83, height=83, callback=self.callbacks.run_button)
                    dpg.bind_item_font(dpg.last_item(), self.icon_font)
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('start', tag='run_button_tooltip')

                # status text
                dpg.add_spacer(height=0.5)
                dpg.add_button(label='inactive', width=259, height=23, tag='farm_status')
                dpg.bind_item_theme(dpg.last_item(), '__statusTextTheme')

            # settings page
            with dpg.group(tag='settings_group', show=False):
                with dpg.group(horizontal=True):
                    dpg.add_button(label='ö', width=20, height=20, callback=self.callbacks.show_main_group)
                    dpg.bind_item_font(dpg.last_item(), self.icon_font)
                    dpg.add_button(label='settings', width=203, height=20)
                    dpg.bind_item_theme(dpg.last_item(), '__centerTitleTheme')
                    dpg.add_button(label='/', width=20, height=20, callback=self.callbacks.show_help_group)
                    dpg.bind_item_font(dpg.last_item(), self.icon_font)

                # general settings
                with dpg.collapsing_header(label='general', bullet=True):
                    dpg.add_spacer(height=0.5)

                    # loop options
                    with dpg.tree_node(label='starting / restarting'):
                        dpg.add_spacer(height=0.5)
                        dpg.add_text('spam amount'); dpg.add_slider_int(label='presses', min_value=0, max_value=20, default_value=int(config.get('game_start_spam', 12)), tag='start_spam')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('how many times to press going through match result screen etc', wrap=190)
                        dpg.add_text('match restart delay'); dpg.add_slider_int(label='seconds', min_value=0, max_value=30, default_value=int(config.get('game_restart_delay', 4)), tag='wait_restart')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('the time to wait after a match finishes before restarting', wrap=190)
                        dpg.add_text('match load time'); dpg.add_slider_int(label='seconds', min_value=10, max_value=30, default_value=int(config.get('game_load_time', 15)), tag='wait_gameload')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('the time to wait for a match to start up to the countdown', wrap=190)

                    # dc rc options
                    dpg.add_spacer(height=0.5)
                    with dpg.tree_node(label='disconnect / reconnect'):
                        dpg.add_spacer(height=0.5); dpg.add_text('mode')
                        dpg.add_checkbox(label='default', tag='open_menu_default', default_value=bool(config.get('open_menu_default', True)), callback=self.callbacks.select_open_menu_default)
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('default mode c:', wrap=190)
                        dpg.add_spacer(height=0.5)
                        with dpg.group(horizontal=True):
                            dpg.add_checkbox(label='+fix', tag='open_menu_fix', default_value=bool(config.get('open_menu_fix', False)), callback=self.callbacks.select_open_menu_fix)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('tries to fix esc menu not opening, works pretty good for both default and direct input mode', wrap=190)
                            dpg.add_checkbox(label='+fix2', tag='open_menu_fix2', default_value=bool(config.get('open_menu_fix2', False)), callback=self.callbacks.select_open_menu_fix2)
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('tries the fix but 2 times', wrap=190)
                        dpg.add_spacer(height=0.5)
                        dpg.add_checkbox(label='hold to pause', tag='open_menu_hold', default_value=bool(config.get('open_menu_hold', False)), callback=self.callbacks.select_open_menu_hold)
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('must enable in brawlhalla: OPTIONS > SYSTEM SETTINGS > HOLD TO PAUSE', wrap=190)
                        dpg.add_spacer(height=0.5)
                        dpg.add_checkbox(label='use ENTER key', tag='open_menu_enter', default_value=bool(config.get('open_menu_enter', True)))
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('use ENTER key instead of ESC', wrap=190)
                        dpg.add_spacer(height=0.5)
                        dpg.add_text('menu key presses', tag='menu_key_presses_text'); dpg.add_slider_int(label='times', min_value=1, max_value=4, default_value=int(config.get('menu_key_presses', 2)), tag='menu_key_presses')
                        with dpg.tooltip(dpg.last_item(), tag='menu_key_presses_tooltip'): dpg.add_text('times to press the menu key (background key actions dont register so its default to 2)', wrap=190)
                        dpg.add_text('disconnect delay'); dpg.add_slider_int(label='ms', min_value=100, max_value=1000, default_value=int(config.get('disconnect_delay', 120)), tag='wait_disconnect')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('time to wait for the menu to pop up after pressing menu key', wrap=190)
                        dpg.add_text('reconnect delay'); dpg.add_slider_int(label='seconds', min_value=3, max_value=10, default_value=int(config.get('reconnect_delay', 4)), tag='wait_reconnect')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('time to wait before reconnectng to the match', wrap=190)

                    # input related
                    dpg.add_spacer(height=0.5)
                    with dpg.tree_node(label='input config'):
                        dpg.add_spacer(height=0.5)
                        dpg.add_checkbox(label='direct input mode', tag='direct_input', default_value=bool(config.get('direct_input', False)))
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('wont work in background! try this if you are having issues with inputs', wrap=190)
                        dpg.add_spacer(height=0.5)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label='', width=26, height=26)
                            dpg.bind_item_theme(dpg.last_item(), '__blankButtonTheme')
                            dpg.add_button(label=config.get('key_up', 'up'), tag='key_up_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_up')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change up key', tag='key_up_tooltip_text')
                        dpg.add_spacer(height=0.5)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label=config.get('key_left', 'left'), tag='key_left_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_left')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change left key', tag='key_left_tooltip_text')
                            dpg.add_button(label=config.get('key_down', 'down'), tag='key_down_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_down')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change down key', tag='key_down_tooltip_text')
                            dpg.add_button(label=config.get('key_right', 'right'), tag='key_right_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_right')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change right key', tag='key_right_tooltip_text')
                            dpg.add_spacer(width=13)
                            dpg.add_button(label=config.get('key_throw', 'v'), tag='key_throw_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_throw')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change throw weapon key', tag='key_throw_tooltip_text')
                            dpg.add_button(label=config.get('key_light', 'c'), tag='key_light_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_light')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change light attack key', tag='key_light_tooltip_text')
                            dpg.add_button(label=config.get('key_heavy', 'x'), tag='key_heavy_button', width=26, height=26, callback=self.callbacks.hotkey_button, user_data='key_heavy')
                            with dpg.tooltip(dpg.last_item()): dpg.add_text('change heavy attack key', tag='key_heavy_tooltip_text')

                            # storing values like this im too sleepy
                            dpg.add_text(default_value=config.get('key_up', 'up'), tag='key_up', show=False)
                            dpg.add_text(default_value=config.get('key_left', 'left'), tag='key_left', show=False)
                            dpg.add_text(default_value=config.get('key_down', 'down'), tag='key_down', show=False)
                            dpg.add_text(default_value=config.get('key_right', 'right'), tag='key_right', show=False)
                            dpg.add_text(default_value=config.get('key_throw', 'v'), tag='key_throw', show=False)
                            dpg.add_text(default_value=config.get('key_light', 'c'), tag='key_light', show=False)
                            dpg.add_text(default_value=config.get('key_heavy', 'x'), tag='key_heavy', show=False)

                        dpg.add_spacer(height=0.5)
                        dpg.add_text('hold'); dpg.add_slider_int(label='ms', min_value=0, max_value=300, default_value=int(config.get('keypress_hold', 70)), tag='keypress_hold')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('average hold duration of the key', wrap=190)
                        dpg.add_text('delay'); dpg.add_slider_int(label='ms', min_value=50, max_value=500, default_value=int(config.get('keypress_delay', 150)), tag='keypress_delay')
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('time to wait before any new key is pressed in sequence', wrap=190)
                    dpg.add_spacer(height=0.5)
                    with dpg.group(horizontal=True, show=False):
                        dpg.add_button(label='W', callback=self.callbacks.reset_general)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('reset all general settings', tag='reset_general_button_tooltip')
                        dpg.add_text('are you sure?', wrap=260, show=False, tag='reset_general_button_text')
                    dpg.add_spacer(height=0.5)

                # sound
                with dpg.collapsing_header(label='boop beep?', bullet=True):
                    dpg.add_spacer(height=0.5)
                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(label='timer sound', tag='timer_sound', default_value=bool(config.get('timer_sound', False)))
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('plays a sound after the timer ends', wrap=190)
                        dpg.add_button(label='Ù', callback=self.callbacks.beep_sound)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('boop')
                        dpg.add_button(label='W', callback=self.callbacks.beep_reset)
                        dpg.bind_item_font(dpg.last_item(), self.icon_font)
                        with dpg.tooltip(dpg.last_item()): dpg.add_text('reset')
                    dpg.add_text('beep frequency'); dpg.add_slider_int(label='hz', min_value=100, max_value=2000, default_value=int(config.get('beep_frequency', 500)), tag='beep_frequency')
                    dpg.add_text('beep duration'); dpg.add_slider_int(label='ms', min_value=10, max_value=1000, default_value=int(config.get('beep_duration', 72)), tag='beep_duration')
                    dpg.add_spacer(height=0.5)

                # other things
                with dpg.collapsing_header(label='other', bullet=True):
                    dpg.add_spacer(height=0.5)
                    dpg.add_checkbox(label='always on top', tag='always_on_top', default_value=bool(config.get('always_on_top', True)), callback=self.callbacks.update_aot)
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('makes this window stay on top')
                    dpg.add_spacer(height=0.5)
                    dpg.add_checkbox(label='launch brawlhalla with prawl', tag='auto_launch', default_value=bool(config.get('auto_launch', False)))
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('launches brawlhalla when you launch prawl')
                    dpg.add_spacer(height=0.5)
                    dpg.add_checkbox(label='rate limit detection', tag='rate_limit_detect', default_value=bool(config.get('rate_limit_detect', True)))
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('detects if you are rate limited in exp/gold')
                    dpg.add_spacer(height=0.5)
                    dpg.add_checkbox(label='rate limit auto wait', tag='rate_limit_wait', default_value=bool(config.get('rate_limit_wait', True)))
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('waits for rate limit reset and starts farming')
                    dpg.add_spacer(height=0.5)
                    dpg.add_slider_int(label='mins', min_value=30, max_value=60, default_value=int(config.get('rate_limit_wait_time', 45)), tag='rate_limit_wait_time')
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('time to wait for rate limit to reset')
                    dpg.add_spacer(height=0.5)
                    dpg.add_checkbox(label='max games', tag='max_games', default_value=bool(config.get('max_games', False)))
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('stops after set amount of games')
                    dpg.add_spacer(height=0.5)
                    dpg.add_slider_int(label='games', min_value=1, max_value=99, default_value=int(config.get('max_games_amount', 16)), tag='max_games_amount')
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('the amount of games to stop at')

                dpg.add_spacer(height=0.5)
                with dpg.group(horizontal=True):
                    dpg.add_button(label='STOP', callback=self.callbacks.stop_button)
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('stop setup')
                    dpg.add_button(label='MINI LOBBY SETUP', callback=self.callbacks.mini_lobby_setup_start)
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('only game rules')
                    dpg.add_button(label='FULL LOBBY SETUP', callback=self.callbacks.full_lobby_setup_start)
                    with dpg.tooltip(dpg.last_item()): dpg.add_text('game rules, lobby rules, bots, handicaps')
                dpg.add_spacer(height=0.5)
                dpg.add_text('always create a new custom game room before you use these setup buttons (still buggy)', wrap=0)

            # help page
            with dpg.group(tag='help_group', show=False):
                with dpg.group(horizontal=True):
                    dpg.add_button(label='ö', callback=self.callbacks.show_settings_group)
                    dpg.bind_item_font(dpg.last_item(), self.icon_font)
                    dpg.add_button(label='help', width=203, height=20)
                    dpg.bind_item_theme(dpg.last_item(), '__centerTitleTheme')

                with dpg.collapsing_header(label='instructions', bullet=True):
                    dpg.add_text('1. make a custom game room', indent=8)
                    dpg.add_text('2. apply the settings below', indent=8)
                    dpg.add_text('3. select a legend to farm', indent=8)
                    dpg.add_text('4. press the start button!', indent=8)
                    dpg.add_spacer(height=0.5)
                    with dpg.tree_node(label='GAME RULE'):
                        for text in ['create a private custom lobby', 'game mode: crew battle', 'stocks: 99', 'match time: 25 minutes', 'mapset: (tournament) 1v1', 'max players: 2']:
                            dpg.add_text(text, bullet=True)
                    dpg.add_spacer(height=0.5)
                    with dpg.tree_node(label='LOBBY'):
                        for text in ['map selection: random', 'disable friend/clan join', 'choose legend, dont start game', 'press start button']:
                            dpg.add_text(text, bullet=True)

                with dpg.collapsing_header(label='faq', bullet=True):
                    dpg.add_spacer(height=0.5)
                    with dpg.tree_node(label='why crew battle?'):
                        dpg.add_text('because it has 25 minute game option and the less time you spend in game menus, the more exp youre gonna get (i think lol)', wrap=0)
                        self._hyperlink('cat 05/17/2024', 'https://discord.com/channels/829496409681297409/1240709211642527824/1240710940140503170')
                        dpg.add_text('xp and gold requires active participation and different modes calculate participation differently so bot is too dumb for ffa basically, because ffa requires actually doing damage and kills', wrap=0)
                        self._hyperlink('sovamorco 10/08/2023', 'https://discord.com/channels/829496409681297409/829503904190431273/1160557662145097898')

                    with dpg.tree_node(label='exp rate limit'):
                        dpg.add_text('Around 5 hours or once you earn around 13000 XP, you have to stop farming for about 45-50 minutes to reset the XP limit.', wrap=0)
                        self._hyperlink('jeffriesuave 10/16/2023', 'https://discord.com/channels/829496409681297409/829503904190431273/1163246039197831198')
                        dpg.add_text('*most people are reporting a wait time of 30 to 60 minutes', wrap=0)

                dpg.add_spacer(height=0.5)
                with dpg.group(horizontal=True):
                    dpg.add_button(label='check for updates', tag='update_button', callback=self.callbacks.update_button)
                    dpg.add_text('', tag='update_status_text')
                dpg.add_button(label='download', tag='update_link', show=False)
                dpg.bind_item_theme(dpg.last_item(), '__hyperlinkTheme')
