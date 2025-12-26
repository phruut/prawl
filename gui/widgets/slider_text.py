import dearpygui.dearpygui as dpg

class TextSlider:
    def __init__(self, tag, default_value, prefix, singular, plural=None, callback=None, **kwargs):
        self.tag = tag
        self.prefix = prefix
        self.singular = singular
        self.plural = plural if plural else singular + 's'
        self.callback = callback

        # pick slider type based on default vaLUE
        if isinstance(default_value, float):
            self.widget_creator = dpg.add_slider_float
        else:
            self.widget_creator = dpg.add_slider_int
        self.widget_creator(tag=self.tag, default_value=default_value, callback=self._on_change, **kwargs)  # pyright: ignore[reportArgumentType]

        # update to set the correct format text on launch
        self._on_change(self.tag, default_value, None)

    def _on_change(self, sender, app_data, user_data=None):

        # format value text
        if isinstance(app_data, float):
             val_text = f'{app_data:.2f}'
        else:
             val_text = f'{app_data}'

        # update slider text and value
        suffix = self.singular if app_data == 1 else self.plural
        label = f'{self.prefix}{val_text}{suffix}'
        dpg.configure_item(self.tag, format=label)

        # do callback
        if self.callback:
            self.callback(sender, app_data)




class TextSliderWidth:
    def __init__(self, tag, default_value, prefix, singular, plural=None, callback=None, **kwargs):
        self.tag = tag
        self.prefix = prefix
        self.singular = singular
        self.plural = plural if plural else singular + 's'
        self.callback = callback

        # this slider is made to have the same width grabber for both int and float so we use this
        self.is_int = isinstance(default_value, int)
        config = kwargs.copy()

        # cast to float
        def to_float(val):
            return float(val) if val is not None else 0.0
        f_default_value = to_float(default_value)
        if 'min_value' in config:
            config['min_value'] = to_float(config['min_value'])
        if 'max_value' in config:
            config['max_value'] = to_float(config['max_value'])

        # make the widget
        dpg.add_slider_float(tag=self.tag, default_value=f_default_value, callback=self._on_change, **config)

        # update to set the correct format text on launch
        self._on_change(self.tag, f_default_value, None)

    def _on_change(self, sender, app_data, user_data=None):

        # format value text, snap if int
        if self.is_int:
            value = int(round(app_data))
            if app_data != value:
                dpg.set_value(sender, value)
            val_text = f'{value}'
        else:
            value = app_data
            val_text = f'{value:.2f}'

        # update slider text and value
        suffix = self.singular if value == 1 else self.plural
        label = f'{self.prefix}{val_text}{suffix}'
        dpg.configure_item(self.tag, format=label)

        # do callback
        if self.callback:
            self.callback(sender, value)
