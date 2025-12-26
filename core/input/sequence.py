import time
from .definitions import get_definitions
from .backend import InputBackend
from .._utils import sleep

class SequenceStopped(Exception):
    pass

class KeySequence:
    def __init__(self, process, interface):
        self.interface = interface
        self.backend = InputBackend(process, interface)
        self.network = None
        self.is_running = lambda: False

    def release_all(self):
        self.backend.release_all()

    def action(self, sequence_names, is_running_callback, network=None):
        """main thing that executes a list of sequences"""
        self.network = network
        self.is_running = is_running_callback
        definitions = get_definitions(self.interface)

        try:
            for seq_name in sequence_names:
                self._check_active()
                steps = definitions.get(seq_name, [])
                for step in steps:
                    self._execute_step(step)
        except SequenceStopped:
            pass

    # helpers
    # -----------------------------------------------

    def _execute_step(self, step):
        """runs a single step tuple to the handlers"""
        self._check_active()
        cmd, args = step[0], step[1:]

        # find handler methods
        handler = getattr(self, f'_cmd_{cmd}', None)
        if handler:
            handler(*args)

    def _sleep(self, ms):
        if ms <= 0:
            return

        start_time = time.perf_counter()
        while True:
            self._check_active()

            current_time = time.perf_counter()
            remaining = (ms / 1000) - (current_time - start_time)

            if remaining <= 0:
                break

            step = min(0.1, remaining)
            sleep(step)

    def _check_active(self):
        if not self.is_running():
            self.interface.run_button_update(self.is_running)
            raise SequenceStopped()

    # command handlers
    # -----------------------------------------------

    def _cmd_status(self, text):
        self._check_active()
        self.interface.update_status(text)

    def _cmd_wait(self, ms):
        self._check_active()
        self._sleep(ms)

    def _cmd_press(self, key, options=None):
        self._check_active()

        options = options or {}
        count = options.get('count', 1)
        hold = options.get('hold', self.interface.get('keypress_hold'))
        delay = options.get('delay', self.interface.get('keypress_delay'))

        for _ in range(count):
            self._check_active()
            self.backend.press(key, hold_ms=hold, delay_ms=delay)

        if delay > 0:
            self._sleep(delay)

    def _cmd_countdown(self, duration, message):
        self._check_active()
        for i in range(duration):
            self._check_active()
            self.interface.update_status(message.format(duration - i))
            self._sleep(1000)

    def _cmd_retry_net(self, options, sub_steps):
        self._check_active()
        if not self.network:
            return

        mode = options.get('mode', '')
        attempts = options.get('attempts', 1)

        for i in range(attempts):
            self._check_active()
            active = self.network.is_match_active()
            if (mode == 'disconnect' and not active) or (mode == 'connect' and active):
                return
            self.interface.update_status(f'try {mode} ({i+1}/{attempts})')

            # do sub steps
            for step in sub_steps:
                self._execute_step(step)

            #self._sleep(200)

        raise SequenceStopped()
