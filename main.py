import dearpygui.dearpygui as dpg
import pywinstyles
from core.config import Config, get_platform
from core.input import KeySequence
from core.farmer import Farmer
from core.update import Update
from core.network import Network
from core.process import Process
from core.logger import setup_logger
from gui.gui import MainGUI
from gui.interface import Interface

# stop farmer, release all keys, show window if hidden
def on_exit():
    config.settings.save_all()
    hwnd = process.get_hwnd()
    if farmer.running:
        farmer.stop()
    if hwnd:
        keyseq.release_all()
        process.show()

if __name__ == '__main__' and get_platform():
    setup_logger()
    config = Config()
    interface = Interface()
    process = Process(config)
    update = Update(config)
    network = Network(config, process)
    keyseq = KeySequence(process, interface)
    farmer = Farmer(process, interface, keyseq, network)
    gui = MainGUI(config, process, interface, keyseq, farmer, update)
    dpg.create_viewport(
        title=f'prawl v{config.version}',
        min_width=292, width=292,
        min_height=170, height=170,
        small_icon=str(config.icon),
        large_icon=str(config.icon)
    )
    dpg.set_viewport_always_top(bool(config.settings.get('other', 'always_on_top')))
    dpg.set_exit_callback(on_exit)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window('main', True)

    pywinstyles.change_header_color(None, config.theme.to_hex(config.theme.get_col('colors', 'bg_primary')))
    pywinstyles.change_border_color(None, config.theme.to_hex(config.theme.get_col('colors', 'bg_primary')))
    pywinstyles.change_title_color(None, config.theme.to_hex(config.theme.get_col('colors', 'text_secondary_disabled')))

    if config.settings.get('other', 'auto_launch'):
        gui.callbacks.launch_button()

    dpg.start_dearpygui()
    dpg.destroy_context()
