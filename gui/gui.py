import dearpygui.dearpygui as dpg
from gui.themes import create_themes, create_fonts
from gui.callbacks import Callbacks
from gui.views import MainView, SettingsView, HelpView

class MainGUI:
    def __init__(self, config, process, interface, keyseq, farmer, update):
        self.config = config
        self.process = process
        self.interface = interface
        self.keyseq = keyseq
        self.farmer = farmer
        self.update = update
        self.callbacks = Callbacks(self)
        self.farmer.set_on_stop_callback(self.callbacks.on_timer_stopped)

        dpg.create_context()
        create_themes(config)
        self.main_font, self.icon_font = create_fonts(config)

        # setup pages
        fonts = (self.main_font, self.icon_font)
        self.main_view = MainView(config, interface, self.callbacks, fonts)
        self.settings_view = SettingsView(config, interface, self.callbacks, fonts)
        self.help_view = HelpView(config, interface, self.callbacks, fonts)

        self._create_widgets()

    def _create_widgets(self):
        with dpg.window(tag='main'):
            dpg.bind_item_theme(dpg.last_item(), '__windowTheme')
            dpg.bind_font(self.main_font)
            self.main_view.build()
            self.settings_view.build()
            self.help_view.build()
