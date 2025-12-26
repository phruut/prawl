import dearpygui.dearpygui as dpg
import webbrowser
from gui.widgets import ToggleSwitch, TextSlider, Separator

class BaseView:
    def __init__(self, config, interface, callbacks, fonts):
        self.config = config
        self.interface = interface
        self.callbacks = callbacks
        self.icon_font = fonts[1]

    def add_separator(self, width=260, height=4, rounding=1.0):
        return Separator(
            width=width,
            height=height,
            rounding=rounding,
            config=self.config
        )

    def add_toggle(self, label:str='', tag=None, default_value:bool=False, width:int=260, height:int=20, rounding:float=0.4, callback=None, user_data=None):
        switch = ToggleSwitch(
            label=label,
            tag=tag,
            default_value=default_value,
            width=width,
            height=height,
            rounding=rounding,
            callback=callback,
            user_data=user_data,
            config=self.config
        )
        return switch

    def add_slider_text(self, tag, default_value, user_data, callback=None, **kwargs):
        if isinstance(user_data[-1], list):
             args = user_data[:-1]
        else:
             args = user_data

        prefix = args[0]
        singular = args[1]
        plural = args[2] if len(args) > 2 else None

        TextSlider(
            tag=tag,
            default_value=default_value,
            prefix=prefix,
            singular=singular,
            plural=plural,
            callback=callback,
            **kwargs
        )

    def hyperlink(self, text, address):
        with dpg.group(horizontal=True):
            # clip icon
            dpg.add_text('(', color=(100, 149, 238))
            dpg.bind_item_font(dpg.last_item(), self.icon_font)

            # hyperlink base
            dpg.add_button(label=text, callback=lambda: webbrowser.open(address))
            dpg.bind_item_theme(dpg.last_item(), "__hyperlinkTheme")
