import dearpygui.dearpygui as dpg
from .themes import create_themes, create_fonts
from .views import MainView, SettingsView, HelpView
from .views.main import MainCallbacks
from .views.settings import SettingsCallbacks
from .views.help import HelpCallbacks
from core.input import KeyListener

class MainGUI:
    def __init__(self, config, process, interface, keyseq, farmer, update):
        self.config = config
        self.process = process
        self.interface = interface
        self.keyseq = keyseq
        self.farmer = farmer
        self.update = update
        self.listener = KeyListener()

        dpg.create_context()
        create_themes(config)
        self.main_font, self.icon_font = create_fonts(config)

        # create view callbacks
        self.main_callbacks = MainCallbacks(self)
        self.settings_callbacks = SettingsCallbacks(self)
        self.help_callbacks = HelpCallbacks(self)

        # attach nav callbacks so views can call self.callbacks.show_something_group
        for cb in (self.main_callbacks, self.settings_callbacks, self.help_callbacks):
            setattr(cb, 'show_main_group', self._show_main_group)
            setattr(cb, 'show_settings_group', self._show_settings_group)
            setattr(cb, 'show_help_group', self._show_help_group)

        self.farmer.set_on_stop_callback(self.main_callbacks.on_timer_stopped)

        # setup pages
        fonts = (self.main_font, self.icon_font)
        self.main_view = MainView(config, interface, self.main_callbacks, fonts)
        self.settings_view = SettingsView(config, interface, self.settings_callbacks, fonts)
        self.help_view = HelpView(config, interface, self.help_callbacks, fonts)

        self.last_settings_tab_height = 484

        self._create_widgets()

    def _create_widgets(self):
        with dpg.window(tag='main'):
            dpg.bind_item_theme(dpg.last_item(), '__windowTheme')
            dpg.bind_font(self.main_font)
            self.main_view.build()
            self.settings_view.build()
            self.help_view.build()

    # nav callbacks
    # ----------------------------------------------

    def _show_main_group(self, sender=None, app_data=None, user_data=None):
        self.interface.show('main_group')
        self.interface.hide('settings_group')
        self.interface.hide('help_group')
        self.interface.set_viewport_height(170)

    def _show_settings_group(self, sender=None, app_data=None, user_data=None):
        self.interface.hide('main_group')
        self.interface.show('settings_group')
        self.interface.hide('help_group')
        self.interface.set_viewport_height(self.last_settings_tab_height)

    def _show_help_group(self, sender=None, app_data=None, user_data=None):
        self.interface.hide('main_group')
        self.interface.hide('settings_group')
        self.interface.show('help_group')
        self.interface.set_viewport_height(170)
