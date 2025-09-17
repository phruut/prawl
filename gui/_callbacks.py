import subprocess
import time
import winsound
import webbrowser
import threading
import dearpygui.dearpygui as dpg
import scripts.window as window
from scripts.timer import calculate_exp, calculate_gold
from scripts.input import KeyListener

class CooldownTimer:
    def __init__(self, duration, callback):
        self._duration = duration
        self._callback = callback
        self._timer = None

    def start(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(self._duration, self._callback)
        self._timer.start()

    def cancel(self):
        if self._timer:
            self._timer.cancel()

class Callbacks:
    def __init__(self, gui_instance):
        self.gui = gui_instance
        self.config = self.gui.config
        self.timer = self.gui.timer
        self.keyseq = self.gui.keyseq
        self.state = self.gui.state
        self.update = self.gui.update
        self.listener = KeyListener()
        self.launch_timer = CooldownTimer(2.0, self._launch_state_reset)
        self.launch_count = 0
        self.timing_timer = CooldownTimer(2.0, self._general_state_reset)
        self.timing_count = 0

    # ui nav buttons
    # ---------------------------------------------------
    def show_main_group(self, sender, app_data, user_data):
        dpg.hide_item('settings_group')
        dpg.hide_item('help_group')
        dpg.show_item('main_group')

    def show_settings_group(self, sender, app_data, user_data):
        dpg.hide_item('main_group')
        dpg.hide_item('help_group')
        dpg.show_item('settings_group')

    def show_help_group(self, sender, app_data, user_data):
        dpg.hide_item('main_group')
        dpg.hide_item('settings_group')
        dpg.show_item('help_group')

    # main page
    # ---------------------------------------------------
    def run_button(self):
        if self.timer.running:
            self.timer.stop()
        else:
            self.state['hwnd'] = window.find()
            if self.state['hwnd']:
                sequence = ['wait_restart', 'spam_menu', 'open_menu', 'disconnect', 'reconnect']
                if dpg.get_value('open_menu_hold'):
                    sequence = ['open_menu_hold' if item == 'open_menu' else item for item in sequence]
                if dpg.get_value('open_menu_fix'):
                    sequence = ['open_menu_fix' if item == 'open_menu' else item for item in sequence]
                if dpg.get_value('open_menu_fix2'):
                    sequence = [sub for item in sequence for sub in (['open_menu_fix', 'open_menu_fix'] if item == 'open_menu' else [item])]
                self.timer.start(dpg.get_value('match_time'), sequence)
                if self.timer.running:
                    dpg.configure_item('run_button', label='ä')
                    dpg.configure_item('run_button_tooltip', default_value='stop')

            else:
                dpg.configure_item('farm_status', label='brawlhalla window not found')

    def stop_button(self):
        self.timer.stop()

    def on_timer_stopped(self):
        with dpg.mutex():
            dpg.set_frame_callback(
                dpg.get_frame_count() + 1,
                callback=lambda: [dpg.configure_item('run_button', label='â'), dpg.configure_item('run_button_tooltip', default_value='start')]
            )

    # ---------------------------------------------------

    def oops_button(self):
        self.state['hwnd'] = window.find()
        if self.state['hwnd'] and self.timer.running and not self.timer.pressing:
            self.timer.pause()
            sequence = ['open_menu', 'disconnect', 'reconnect']
            if dpg.get_value('open_menu_hold'):
                sequence = ['open_menu_hold' if item == 'open_menu' else item for item in sequence]
            self.keyseq.action(sequence, lambda: self.timer.running, self.state['hwnd'])
            self.timer.pause()
        else:
            dpg.configure_item('farm_status', label='not running')

    def toggle_button(self):
        self.state['hwnd'] = window.find()
        if not self.state['hwnd']:
            dpg.configure_item('farm_status', label='brawlhalla window not found')
            return
        if window.visible(self.state['hwnd']):
            window.hide(self.state['hwnd'])
            dpg.configure_item('farm_status', label='brawlhalla window hidden')
            dpg.configure_item('toggle_button', label='N')
            dpg.configure_item('toggle_button_tooltip', default_value='show brawlhalla window')
        else:
            window.show(self.state['hwnd'])
            dpg.configure_item('farm_status', label='brawlhalla window shown')
            dpg.configure_item('toggle_button', label='O')
            dpg.configure_item('toggle_button_tooltip', default_value='hide brawlhalla window')

    def _launch_state_reset(self):
        self.launch_count = 0
        text = 'stop brawlhalla' if window.running() else 'start brawlhalla'
        dpg.configure_item('farm_status', label='inactive')
        dpg.configure_item('launch_button_tooltip', default_value=text)
    def launch_button(self):
        if window.running():
            self.launch_count += 1
            if self.launch_count == 1:
                dpg.configure_item('farm_status', label='already running! (close?)')
                dpg.configure_item('launch_button_tooltip', default_value='click again to stop')
                self.launch_timer.start()
            elif self.launch_count == 2:
                dpg.configure_item('farm_status', label='terminated brawlhalla')
                dpg.configure_item('launch_button_tooltip', default_value='start brawlhalla')
                window.close()
                self.launch_count = 0
                self.launch_timer.cancel()
                self.timer.stop()
        else:
            subprocess.run('cmd /c start steam://rungameid/291550', check=False)
            dpg.configure_item('farm_status', label='starting brawlhalla...')
            dpg.configure_item('launch_button_tooltip', default_value='stop brawlhalla')
            while not window.running():
                time.sleep(0.5)
            self.state['hwnd'] = window.find()
            dpg.configure_item('farm_status', label='brawlhalla started')

    # ---------------------------------------------------

    def update_values(self, sender, app_data):
        estimated_exp = calculate_exp(app_data)
        estimated_gold = calculate_gold(app_data)
        dpg.set_value('estimated_values', f'gold: {int(estimated_gold)} | exp: {int(estimated_exp)}')

    def update_slider_format(self, value):
        if value == 1:
            dpg.configure_item('match_time', format=f"{value} minute")
        else:
            dpg.configure_item('match_time', format=f"{value} minutes")

    def match_time_slider(self, sender, app_data):
        self.update_slider_format(app_data)
        self.update_values(sender, app_data)

    # settings page
    # ---------------------------------------------------

    def hotkey_button(self, sender, app_data, user_data):
        key_tag = user_data
        dpg.configure_item(f'{key_tag}_button', label='...', enabled=True)
        dpg.set_value(f'{key_tag}_tooltip_text', 'waiting for key, esc to cancel')

        def listen_and_update():
            hotkey = self.listener.hotkey()
            def update_ui():
                if hotkey:
                    self.config[key_tag] = hotkey
                dpg.set_value(key_tag, hotkey)
                dpg.configure_item(f'{key_tag}_button', label=self.config.get(key_tag, None))
                text = ' '.join(reversed(key_tag.split('_')))
                dpg.set_value(f'{key_tag}_tooltip_text', f'change {text}')

            with dpg.mutex():
                dpg.set_frame_callback(dpg.get_frame_count() + 1, callback=update_ui)

        threading.Thread(target=listen_and_update, daemon=True).start()

    # ---------------------------------------------------

    def update_aot(self, sender, app_data):
        dpg.set_viewport_always_top(app_data)

    def _general_state_reset(self):
        self.timing_count = 0
        dpg.configure_item('reset_general_button_text', show=False)
        dpg.configure_item('reset_general_button_tooltip', default_value='reset all general settings')
    def reset_general(self):
        self.timing_count += 1
        if self.timing_count == 1:
            dpg.configure_item('reset_general_button_text', show=True)
            dpg.configure_item('reset_general_button_tooltip', default_value='click again to reset')
            self.timing_timer.start()
        elif self.timing_count == 2:
            dpg.configure_item('reset_general_button_text', show=False)
            dpg.configure_item('reset_general_button_tooltip', default_value='reset all general settings')
            dpg.set_value('start_spam', 10); dpg.set_value('wait_restart', 4); dpg.set_value('wait_gameload', 15)
            dpg.set_value('menu_key_presses', 2); dpg.set_value('menu_key_presses_delay', 0)
            dpg.set_value('wait_disconnect', 100); dpg.set_value('wait_reconnect', 4)
            dpg.set_value('keypress_hold', 70); dpg.set_value('keypress_delay', 150)
            self.timing_count = 0
            self.timing_timer.cancel()

    # ---------------------------------------------------

    def select_open_menu_default(self):
        if not dpg.get_value('open_menu_default'): dpg.set_value('open_menu_default', True)
        else: dpg.configure_item('open_menu_fix', enabled=True); dpg.configure_item('open_menu_fix2', enabled=True)
        for tag in ['menu_key_presses', 'menu_key_presses_delay', 'menu_key_presses_text', 'menu_key_presses_delay_text']:
            dpg.configure_item(tag, show=True)
        dpg.set_value('open_menu_hold', False)

    def select_open_menu_fix(self):
        if dpg.get_value('open_menu_fix2'): dpg.set_value('open_menu_fix2', False)

    def select_open_menu_fix2(self):
        if dpg.get_value('open_menu_fix'): dpg.set_value('open_menu_fix', False)

    def select_open_menu_hold(self):
        if not dpg.get_value('open_menu_hold'): dpg.set_value('open_menu_hold', True)
        dpg.configure_item('open_menu_fix', enabled=False); dpg.configure_item('open_menu_fix2', enabled=False)
        for tag in ['menu_key_presses', 'menu_key_presses_delay', 'menu_key_presses_text', 'menu_key_presses_delay_text']:
            dpg.configure_item(tag, show=False)
        dpg.set_value('open_menu_default', False); dpg.set_value('open_menu_fix', False)

    # ---------------------------------------------------

    def beep_sound(self):
        winsound.Beep(dpg.get_value('beep_frequency'), dpg.get_value('beep_duration'))

    def beep_reset(self):
        dpg.set_value('beep_frequency', 500); dpg.set_value('beep_duration', 72)

    # ---------------------------------------------------

    def mini_lobby_setup_start(self):
        self.state['hwnd'] = window.find()
        if self.state['hwnd']:
            dpg.configure_item('run_button', label='ä')
            dpg.configure_item('run_button_tooltip', default_value='stop')
            self.timer.start(0, ['lobby_setup_gamerule', 'lobby_setup_exit_menu', 'stop_timer'])

    def full_lobby_setup_start(self):
        self.state['hwnd'] = window.find()
        if self.state['hwnd']:
            dpg.configure_item('run_button', label='ä')
            dpg.configure_item('run_button_tooltip', default_value='stop')
            self.timer.start(0, ['lobby_setup_gamerule', 'lobby_setup_lobby', 'lobby_setup_exit_menu', 'lobby_setup_party', 'stop_timer'])

    # ---------------------------------------------------

    def update_button(self):
        dpg.configure_item('update_button', enabled=False)
        dpg.configure_item('update_link', show=False)
        dpg.set_value('update_status_text', 'checking for updates...')
        thread = threading.Thread(target=self.update_worker, daemon=True)
        thread.start()

    def update_worker(self):
        results = self.update.check()
        with dpg.mutex():
            dpg.set_frame_callback(
                dpg.get_frame_count() + 1,
                callback=self.update_post,
                user_data=results
            )

    def update_post(self, sender, app_data, user_data):
        message, is_update_available = user_data
        dpg.set_value('update_status_text', message)
        if is_update_available and self.update.release_url:
            dpg.configure_item(
                'update_link',
                show=True,
                label=f'download {self.update.latest_version}',
                callback=lambda: webbrowser.open(self.update.release_url)
            )
        dpg.configure_item('update_button', enabled=True)
