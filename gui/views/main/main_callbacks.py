import subprocess
import time
import logging
from typing import Any
from core._utils import calculate_exp, calculate_gold
from ...utils import CooldownTimer

logger = logging.getLogger('prawl')

class MainCallbacks:
    config: Any
    interface: Any
    farmer: Any
    process: Any
    keyseq: Any
    hwnd: Any
    launch_count: int
    launch_timer: Any

    def __init__(self, gui):
        self.gui = gui
        self.config = gui.config
        self.interface = gui.interface
        self.farmer = gui.farmer
        self.process = gui.process
        self.keyseq = gui.keyseq
        self.launch_timer = CooldownTimer(2.0, self._launch_state_reset)
        self.launch_count = 0
        self.hwnd = None

    # sequence building thging
    # ----------------------------------------------

    def _get_sequence(self, mode):
        is_net = self.interface.get('network_mode')
        is_online = self.interface.get('online_mode')
        is_hold = self.interface.get('open_menu_hold')

        suffix_net = '_net' if is_net else ''
        suffix_hold = '_hold' if is_hold else ''

        dc_cmd = f'disconnect{suffix_net}{suffix_hold}'
        rc_cmd = f'reconnect{suffix_net}'

        if mode == 'oops':
            return [dc_cmd, rc_cmd]

        if mode == 'start':
            if is_net:
                if is_online:
                    middle_seq = ['spam_menu', 'wait_match_net']
                else:
                    middle_seq = ['spam_menu_net']
            else:
                middle_seq = ['spam_menu', 'wait_match']

            return ['wait_restart'] + middle_seq + [dc_cmd, rc_cmd]

        return []

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
        logger.info('run_button pressed')
        if self.farmer.running:
            self.farmer.stop()
            self.interface.run_button_update(self.farmer.running)

        else:
            self.hwnd = self.process.get_hwnd()
            if self.hwnd:
                sequence = self._get_sequence('start')
                logger.info(f'starting farmer | hwnd: {self.hwnd}')
                self.farmer.start(self.interface.get('match_time'), sequence)
                self.interface.run_button_update(self.farmer.running)
            else:
                logger.warning('brawlhalla window not found')
                self.interface.update_status('brawlhalla window not found')

    def stop_button(self):
        logger.info('stop_button pressed')
        self.keyseq.release_all(self.hwnd)
        self.farmer.stop()
        self.interface.run_button_update(self.farmer.running)

    def on_timer_stopped(self):
        self.interface.run_button_update(self.farmer.running)

    # oops button
    # ----------------------------------------------

    def oops_button(self):
        logger.info('oops_button pressed')
        self.hwnd = self.process.get_hwnd()
        if self.hwnd and self.farmer.running:
            self.farmer.pause()
            sequence = self._get_sequence('oops')
            logger.info('retry sequence triggered')
            self.keyseq.action(
                sequence,
                lambda: self.farmer.running,
                self.farmer.network,
            )
            self.farmer.pause()
        else:
            logger.warning('oops_button failed | hwnd or farmer not running')
            self.interface.update_status('not running')

    # show / hide window
    # ----------------------------------------------

    def toggle_button(self):
        self.hwnd = self.process.get_hwnd()
        if not self.hwnd:
            logger.warning('brawlhalla window not found')
            self.interface.update_status('brawlhalla window not found')
            return
        if self.process.visible():
            self.process.hide()
            logger.info('brawlhalla window hidden')
            self.interface.update_status('brawlhalla window hidden')
            self.interface.configure('toggle_button', label='N')
            self.interface.configure('toggle_button_tooltip', default_value='show brawlhalla window')
        else:
            self.process.show()
            logger.info('brawlhalla window shown')
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
        logger.info('launch_button pressed')
        if self.process.running():
            self.launch_count += 1
            if self.launch_count == 1:
                logger.info('brawlhalla already running, prompt to close')
                self.interface.update_status('already running! (close?)')
                self.interface.configure('launch_button', label='T')
                self.interface.configure('launch_button_tooltip', default_value='click again to stop')
                self.launch_timer.start()
            elif self.launch_count == 2:
                logger.info('terminating brawlhalla')
                self.interface.update_status('terminated brawlhalla')
                self.interface.configure('launch_button', label='\\')
                self.interface.configure('launch_button_tooltip', default_value='start brawlhalla')
                self.process.close()
                self.launch_count = 0
                self.launch_timer.cancel()
                self.farmer.stop()
        else:
            logger.info('starting brawlhalla via steam')
            subprocess.run('cmd /c start steam://rungameid/291550', check=False, creationflags=0x08000000)
            self.interface.update_status('starting brawlhalla...')
            self.interface.configure('launch_button_tooltip', default_value='stop brawlhalla')
            while not self.process.running():
                time.sleep(0.5)
            self.hwnd = self.process.get_hwnd()
            logger.info(f'brawlhalla started | hwnd: {self.hwnd}')
            self.interface.update_status('brawlhalla started')
