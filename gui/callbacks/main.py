import subprocess
import time
from typing import Any
from core._utils import calculate_exp, calculate_gold

class MainCallbacks:
    config: Any
    interface: Any
    farmer: Any
    process: Any
    keyseq: Any
    hwnd: Any
    launch_count: int
    launch_timer: Any

    # sequence building thging
    # ----------------------------------------------

    def _get_sequence(self, mode):
        seq = []

        # base sequence
        if mode == 'start':
            seq = ['wait_restart', 'spam_menu',]
            if self.interface.get('open_menu_hold'):
                m_seq = ['disconnect_hold']
            else:
                m_seq = ['disconnect']

            seq.extend(m_seq)
            seq.append('reconnect')

        elif mode == 'oops':
            dc_cmd = 'disconnect_hold' if self.interface.get('open_menu_hold') else 'disconnect'
            seq = [dc_cmd, 'reconnect']

        # network mode
        if self.interface.get('network_mode'):
            net_map = {
                'spam_menu': 'spam_menu_net',
                'disconnect': 'disconnect_net',
                'disconnect_hold': 'disconnect_net_hold',
                'reconnect':  'reconnect_net'
            }
            seq = [net_map.get(item, item) for item in seq]

        return seq

    # match time slider update
    # ----------------------------------------------

    def update_estimate(self, sender, app_data):
        multiplier = self.interface.get('exp_multiplier')
        if multiplier is None:
            multiplier = self.config.settings.get('other', 'exp_multiplier')
        estimated_exp = calculate_exp(app_data, multiplier)
        estimated_gold = calculate_gold(app_data, multiplier)
        self.interface.set('estimated_values', f'gold: {int(estimated_gold)} | exp: {int(estimated_exp)} | x{multiplier}')

    # big run  button
    # ----------------------------------------------

    def run_button(self):
        if self.farmer.running:
            self.farmer.stop()
            self.interface.run_button_update(self.farmer.running)

        else:
            self.hwnd = self.process.get_hwnd()
            if self.hwnd:
                sequence = self._get_sequence('start')
                self.farmer.start(self.interface.get('match_time'), sequence)
                self.interface.run_button_update(self.farmer.running)
            else:
                self.interface.update_status('brawlhalla window not found')

    def stop_button(self):
        self.keyseq.release_all(self.hwnd)
        self.farmer.stop()
        self.interface.run_button_update(self.farmer.running)

    # i forgot where this was used lol
    def on_timer_stopped(self):
        self.interface.run_button_update(self.farmer.running)

    # oops button
    # ----------------------------------------------

    def oops_button(self):
        self.hwnd = self.process.get_hwnd()
        if self.hwnd and self.farmer.running:
            self.farmer.pause()
            sequence = self._get_sequence('oops')
            self.keyseq.action(
                sequence,
                lambda: self.farmer.running,
                self.farmer.network,
            )
            self.farmer.pause()
        else:
            self.interface.update_status('not running')

    # show / hide window
    # ----------------------------------------------

    def toggle_button(self):
        self.hwnd = self.process.get_hwnd()
        if not self.hwnd:
            self.interface.update_status('brawlhalla window not found')
            return
        if self.process.visible():
            self.process.hide()
            self.interface.update_status('brawlhalla window hidden')
            self.interface.configure('toggle_button', label='N')
            self.interface.configure('toggle_button_tooltip', default_value='show brawlhalla window')
        else:
            self.process.show()
            self.interface.update_status('brawlhalla window shown')
            self.interface.configure('toggle_button', label='O')
            self.interface.configure('toggle_button_tooltip', default_value='hide brawlhalla window')

    # launch brawlhalla button
    # ----------------------------------------------

    def _launch_state_reset(self):
        self.launch_count = 0
        text = 'stop brawlhalla' if self.process.running() else 'start brawlhalla'
        self.interface.update_status('inactive')
        self.interface.configure('launch_button', label='\\')
        self.interface.configure('launch_button_tooltip', default_value=text)

    def launch_button(self):
        if self.process.running():
            self.launch_count += 1
            if self.launch_count == 1:
                self.interface.update_status('already running! (close?)')
                self.interface.configure('launch_button', label='T')
                self.interface.configure('launch_button_tooltip', default_value='click again to stop')
                self.launch_timer.start()
            elif self.launch_count == 2:
                self.interface.update_status('terminated brawlhalla')
                self.interface.configure('launch_button', label='\\')
                self.interface.configure('launch_button_tooltip', default_value='start brawlhalla')
                self.process.close()
                self.launch_count = 0
                self.launch_timer.cancel()
                self.farmer.stop()
        else:
            subprocess.run('cmd /c start steam://rungameid/291550', check=False)
            self.interface.update_status('starting brawlhalla...')
            self.interface.configure('launch_button_tooltip', default_value='stop brawlhalla')
            while not self.process.running():
                time.sleep(0.5)
            self.hwnd = self.process.get_hwnd()
            self.interface.update_status('brawlhalla started')
