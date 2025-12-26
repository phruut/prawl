import time
import threading
import winsound
from ._utils import calculate_exp, calculate_gold, sleep

import logging
logger = logging.getLogger('prawl')

class Farmer:
    def __init__(self, process, interface, keyseq, network):
        self.process = process
        self.interface = interface
        self.keyseq = keyseq
        self.network = network

        # states
        self.initial_time = 0
        self.remaining_time = 0
        self.running = False
        self.paused = False
        self._timer_thread = None

        # stats
        self.total_games = 0
        self.total_gold = 0
        self.total_exp = 0
        self.current_exp = 0
        self.hwnd = None

    def set_on_stop_callback(self, callback):
        self.on_stop_callback = callback

    def start(self, minutes, sequence):
        if self.running:
            return

        logger.info(f'starting sequence: {sequence}')
        # check if keybinds set
        required_keys = ['key_up', 'key_left', 'key_down', 'key_right', 'key_light', 'key_heavy', 'key_throw']
        for key in required_keys:
            if not self.interface.get(key):
                self.interface.update_status('failed! set keybinds!')
                return

        self.hwnd = self.process.get_hwnd()
        if not self.hwnd:
            self.interface.update_status('brawlhalla window not found')
            return

        self.initial_time = minutes * 60
        self.remaining_time = self.initial_time
        self.sequence = sequence
        self.running = True
        self.paused = False

        self._timer_thread = threading.Thread(target=self._run)
        self._timer_thread.start()

    def stop(self):
        # disable gui updates
        self.interface.update_status('stopping...')

        if self.on_stop_callback:
            self.on_stop_callback()

        self.running = False
        if self.network:
            self.network.stop()
        self._timer_thread = None

        self.interface.update_status('inactive')
        if not self.running:
            self.interface.configure('run_button', label='â')
            self.interface.configure('run_button_tooltip', default_value='start')

    def pause(self):
        if self.running:
            self.paused = not self.paused
            status = 'paused' if self.paused else 'resumed'
            self.interface.update_status(status)

    def _run(self):
        is_net = self.network and self.interface.get('network_mode')

        if is_net:
            self.interface.update_status('starting network monitor')
            self.network.start()
            self.network.update_base()

        try:
            while self.running:
                self.keyseq.action(self.sequence, lambda: self.running, self.network)

                # this is for the lobby setup part
                if 'stop_farmer' in self.sequence:
                    self.stop()
                    return
                if not self.running:
                    break

                match_completed = self._match_monitor(is_net)
                if match_completed and self.running:
                    self._match_end()
                    if self._limits():
                        break
                    self.remaining_time = self.initial_time
        finally:
            if self.network:
                self.network.stop()
            self.running = False
            self.interface.update_status('inactive')

    def _match_monitor(self, is_net):
        start_t = time.time()
        paused_duration = 0
        threshold_pct = self.interface.get('early_dc_thresh')
        threshold_time_seconds = (threshold_pct / 100) * self.initial_time

        while self.running:
            if self.paused:
                pause_start = time.time()
                while self.paused and self.running:
                    sleep(1)
                paused_duration += (time.time() - pause_start)

            current_duration = time.time() - start_t - paused_duration
            self.remaining_time = max(0, self.initial_time - int(current_duration))
            mins, secs = divmod(self.remaining_time, 60)

            if is_net:
                connected = self.network.is_match_active()
                if not connected:
                    if current_duration < threshold_time_seconds:
                        self.interface.update_status('early disconnect detected')
                        self.stop()
                        return False
                    else:
                        return True
            else:
                if self.remaining_time == 0:
                    return True

            status_text = f'active ({mins}:{secs:02})'
            if is_net and self.remaining_time == 0:
                status_text = 'waiting for finish...'

            self.interface.update_status(status_text)

            for _ in range(10):
                if not self.running:
                    return False
                sleep(0.1)

        return False

    def _match_end(self):
        if self.interface.get('timer_sound'):
            winsound.Beep(self.interface.get('beep_frequency'), self.interface.get('beep_duration'))

        target_minutes = self.interface.get('match_time')
        multiplier = self.interface.get('exp_multiplier')
        exp_gain = calculate_exp(target_minutes, multiplier)
        gold_gain = calculate_gold(target_minutes, multiplier)

        self.total_games += 1
        self.total_gold += gold_gain
        self.total_exp += exp_gain
        self.current_exp += exp_gain

        self.interface.configure('total_games', label=self.total_games)
        self.interface.configure('total_gold', label=self.total_gold)
        self.interface.configure('total_exp', label=self.total_exp)

    def _limits(self):
        if self.interface.get('rate_limit_detect') and self.current_exp >= 13000:
            self.interface.update_status('exp rate limit...')
            if self.interface.get('rate_limit_wait'):
                wait_remaining = self.interface.get('rate_limit_wait_time') * 60
                while wait_remaining > 0 and self.running:
                    mins, secs = divmod(wait_remaining, 60)
                    self.interface.update_status(f'exp rate limit reset in {mins}:{secs:02}')
                    sleep(1)
                    wait_remaining -= 1
                self.current_exp = 0
            else:
                self.stop()
                return True

        if self.interface.get('max_games') and self.total_games >= self.interface.get('max_games_amount'):
            self.interface.update_status('max games reached...')
            self.stop()
            return True

        return False
