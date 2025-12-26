import dearpygui.dearpygui as dpg

class Interface:

    def get(self, tag):
        if dpg.does_item_exist(tag):
            return dpg.get_value(tag)

    def set(self, tag, value):
        if dpg.does_item_exist(tag):
            dpg.set_value(tag, value)

    def configure(self, tag, **kwargs):
        if dpg.does_item_exist(tag):
            dpg.configure_item(tag, **kwargs)

    def show(self, tag):
        if dpg.does_item_exist(tag):
            dpg.show_item(tag)

    def hide(self, tag):
        if dpg.does_item_exist(tag):
            dpg.hide_item(tag)

    def bind_item_theme(self, tag, theme):
        if dpg.does_item_exist(tag):
            dpg.bind_item_theme(tag, theme)

    def set_viewport_always_top(self, state: bool):
        dpg.set_viewport_always_top(state)

    # specific tags i forgot why i did ts </3
    def run_button_update(self, state: bool):
        if state:
            self.configure('run_button', label='ä')
            self.configure('run_button_tooltip', default_value='stop')
        else:
            self.configure('run_button', label='â')
            self.configure('run_button_tooltip', default_value='start')

    def update_status(self, text):
        dpg.configure_item('farm_status', label=text)
