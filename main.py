import dearpygui.dearpygui as dpg
import pywinstyles
import scripts.window as window
from scripts.config import Config, get_platform
from scripts.input import KeySequence
from scripts.timer import Timer
from scripts.update import Update
from gui.gui import PrawlGUI

# stop timer, release all keys, save config, show window if hidden
def on_exit():
    if timer.running:
        timer.stop()
    keyseq._release_all(state['hwnd'])
    config.save()
    hwnd = window.find()
    if hwnd:
        window.show(hwnd)

if __name__ == '__main__' and get_platform():
    state = {
        'total_games': 0,
        'total_gold': 0,
        'total_exp': 0,
        'current_exp': 0,
        'hwnd': None
    }
    config = Config()
    keyseq = KeySequence(config.data)
    timer = Timer(config.data, keyseq, state)
    update = Update(config.version)

    # setup gui things
    gui = PrawlGUI(config, timer, keyseq, state, update)
    dpg.create_viewport(
        title=f'prawl',
        min_width=291,
        min_height=169,
        width=291,
        height=169,
        small_icon=config.icon,
        large_icon=config.icon
    )
    dpg.set_viewport_always_top(dpg.get_value('always_on_top'))
    dpg.set_exit_callback(on_exit)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window('main', True)

    pywinstyles.change_header_color(None, '#2a2a2d')
    pywinstyles.change_border_color(None, "#2a2a2d")
    pywinstyles.change_title_color(None, '#c0c3c7')

    if config.data['auto_launch']:
        gui._launch_callback()

    dpg.start_dearpygui()
    dpg.destroy_context()
