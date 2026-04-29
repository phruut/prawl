import dearpygui.dearpygui as dpg

class TextSlider:
    def __init__(self, tag, default_value, prefix, singular, plural=None, callback=None, **kwargs):
        self.tag = tag
        self.callback = callback

        if isinstance(default_value, float):
            self.widget_creator = dpg.add_slider_float
        else:
            self.widget_creator = dpg.add_slider_int
        self.widget_creator(tag=self.tag, default_value=default_value, user_data=(prefix, singular, plural if plural else singular + 's'), callback=self._on_change, **kwargs)  # pyright: ignore[reportArgumentType]

        user_data = (prefix, singular, plural if plural else singular + 's')
        self._on_change(self.tag, default_value, user_data)

    def _on_change(self, sender, app_data, user_data=None):
        prefix, singular, plural = dpg.get_item_user_data(sender) or ('', '', '')

        if isinstance(app_data, float):
            val_text = f'{app_data:.2f}'
        else:
            val_text = f'{app_data}'

        suffix = singular if app_data == 1 else plural
        label = f'{prefix}{val_text}{suffix}'
        dpg.configure_item(self.tag, format=label)

        if self.callback:
            self.callback(sender, app_data)


class TextSliderWidth:
    def __init__(self, tag, default_value, prefix, singular, plural=None, callback=None, **kwargs):
        self.tag = tag
        self.callback = callback
        self.is_int = isinstance(default_value, int)

        config = kwargs.copy()

        def to_float(val):
            return float(val) if val is not None else 0.0
        f_default_value = to_float(default_value)
        if 'min_value' in config:
            config['min_value'] = to_float(config['min_value'])
        if 'max_value' in config:
            config['max_value'] = to_float(config['max_value'])

        config['user_data'] = (prefix, singular, plural if plural else singular + 's')
        dpg.add_slider_float(tag=self.tag, default_value=f_default_value, callback=self._on_change, **config)

        user_data = (prefix, singular, plural if plural else singular + 's')
        self._on_change(self.tag, f_default_value, user_data)

    def _on_change(self, sender, app_data, user_data=None):
        prefix, singular, plural = dpg.get_item_user_data(sender) or ('', '', '')

        if self.is_int:
            value = int(round(app_data))
            if app_data != value:
                dpg.set_value(sender, value)
            val_text = f'{value}'
        else:
            value = app_data
            val_text = f'{value:.2f}'

        suffix = singular if value == 1 else plural
        label = f'{prefix}{val_text}{suffix}'
        dpg.configure_item(self.tag, format=label)

        if self.callback:
            self.callback(sender, value)
