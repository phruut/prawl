from core.input import KeyListener
from .cooldown import CooldownTimer
from .misc import MiscCallbacks
from .main import MainCallbacks
from .settings import SettingsCallbacks
from .help import HelpCallbacks

class Callbacks(MiscCallbacks, MainCallbacks, SettingsCallbacks, HelpCallbacks):
    def __init__(self, gui):
        self.gui = gui
        self.config = self.gui.config
        self.process = self.gui.process
        self.keyseq = self.gui.keyseq
        self.farmer = self.gui.farmer
        self.update = self.gui.update
        self.interface = self.gui.interface
        self.listener = KeyListener()

        # timers
        self.launch_timer = CooldownTimer(2.0, self._launch_state_reset)
        self.launch_count = 0
        self.timing_timer = CooldownTimer(2.0, self._general_state_reset)
        self.timing_count = 0

        # state
        self.hwnd = None
