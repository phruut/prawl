import time
import threading
import winsound
import dearpygui.dearpygui as dpg

def calculate_exp(minutes):
    return (minutes / 25) * 1000

def calculate_gold(minutes):
    return (minutes / 25) * 250

class Timer:
    def __init__(self, config, keyseq, state):
        self.keyseq = keyseq
        self.state = state
        self.initial_time = 0
        self.remaining_time = 0
        self.waiting_time = config.get('rate_limit_wait_time', 45) * 60
        self.running = False
        self.paused = False
        self.pressing = False
        self._timer_thread = None

    def _update_gui(self, item_tag, **kwargs):
        def update_callback():
            if dpg.does_item_exist(item_tag):
                dpg.configure_item(item_tag, **kwargs)
        with dpg.mutex():
            dpg.set_frame_callback(dpg.get_frame_count() + 1, callback=update_callback)

    def set_on_stop_callback(self, callback):
        self.on_stop_callback = callback

    def start(self, minutes, sequence):
        if self.running:
            dpg.configure_item('farm_status', label='already active')
            return
        self.initial_time = minutes * 60
        self.remaining_time = self.initial_time
        self.sequence = sequence
        self.running = True
        self.paused = False
        self._timer_thread = threading.Thread(target=self._run)
        self._timer_thread.start()

    def stop(self):
        if self.on_stop_callback:
            self.on_stop_callback()
        dpg.configure_item('farm_status', label='stopping...')
        self.running = False
        self._timer_thread = None
        dpg.configure_item('farm_status', label='inactive')

    def pause(self):
        if self.running:
            self.paused = not self.paused
            status = 'paused' if self.paused else 'resumed'
            dpg.configure_item('farm_status', label=f'{status}')

    def _run(self):
        while self.running:
            self.pressing = True
            self.keyseq.action(self.sequence, lambda: self.running, self.state['hwnd'])
            self.pressing = False

            if 'stop_timer' in self.sequence:
                self.stop()
                return

            while self.remaining_time > 0 and self.running:
                if self.paused:
                    while self.paused and self.running:
                        time.sleep(1)
                    continue
                mins, secs = divmod(self.remaining_time, 60)
                self._update_gui('farm_status', label=f'active ({mins}:{secs:02})')
                time.sleep(1)
                self.remaining_time -= 1

            if self.remaining_time == 0 and self.running:
                if dpg.get_value('timer_sound'):
                    winsound.Beep(dpg.get_value('beep_frequency'), dpg.get_value('beep_duration'))

                exp_gain = calculate_exp(self.initial_time / 60)
                gold_gain = calculate_gold(self.initial_time / 60)
                self.state['total_games'] += 1
                self.state['total_gold'] += gold_gain
                self.state['total_exp'] += exp_gain
                self.state['current_exp'] += exp_gain
                self._update_gui('total_games', label=int(self.state['total_games']))
                self._update_gui('total_gold', label=int(self.state['total_gold']))
                self._update_gui('total_exp', label=int(self.state['total_exp']))

                # rate limit
                if dpg.get_value('rate_limit_detect') and self.state['current_exp'] >= 13000:
                    self._update_gui('farm_status', label='exp rate limit...')
                    if dpg.get_value('rate_limit_wait'):
                        self.remaining_time = self.waiting_time
                        while self.remaining_time > 0 and self.running:
                            mins, secs = divmod(self.remaining_time, 60)
                            self._update_gui('farm_status', label=f'exp rate limit reset in {mins}:{secs:02}')
                            time.sleep(1)
                            self.remaining_time -= 1
                        self.state['current_exp'] = 0
                    else:
                        self.stop()
                        return
                self.remaining_time = self.initial_time

                # max games
                if dpg.get_value('max_games') and self.state['total_games'] >= dpg.get_value('max_games_amount'):
                    self._update_gui('farm_status', label='max games reached...')
                    self.stop()
                    return
