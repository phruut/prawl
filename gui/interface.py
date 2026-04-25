import dearpygui.dearpygui as dpg

class Interface:

    def get(self, tag):
        if dpg.does_item_exist(tag):
            return dpg.get_value(tag)

    def set(self, tag, value):
        if dpg.does_item_exist(tag):
            dpg.set_value(tag, value)
            user_data = dpg.get_item_user_data(tag)
            if isinstance(user_data, tuple) and len(user_data) == 3 and isinstance(user_data[0], str):
                prefix, singular, plural = user_data
                if isinstance(value, float):
                    val_text = f'{value:.2f}'
                else:
                    val_text = f'{value}'
                suffix = singular if value == 1 else plural
                dpg.configure_item(tag, format=f'{prefix}{val_text}{suffix}')

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
