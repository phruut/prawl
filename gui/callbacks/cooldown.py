import threading

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
