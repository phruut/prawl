import dearpygui.dearpygui as dpg
from typing import Any, Optional

class ToggleSwitch:
    def __init__(self, label:str='', tag=None, default_value:bool=False, width:int=200, height:int=20, rounding:float=1.0, callback=None, user_data=None, config: Optional[Any]=None):
        self.label = str(label)
        self.callback = callback
        self.user_data = user_data
        self.width= int(width)
        self.height = int(height)
        self._centered = False

        # colors
        if config is not None:
            self.track_active = config.theme.get('colors', 'active')
            self.track_active_hover = config.theme.get('colors', 'active')
            self.track_inactive = config.theme.get('colors', 'bg_secondary')
            self.track_inactive_hover = config.theme.get('colors', 'hover')
            self.knob_active = config.theme.get('colors', 'bg_primary')
            self.knob_active_hover = config.theme.get('colors', 'bg_secondary')
            self.knob_inactive = config.theme.get('colors', 'bg_primary')
            self.knob_inactive_hover = config.theme.get('colors', 'bg_primary')
        else:
            self.track_active = (255, 114, 121, 255)
            self.track_active_hover = (255, 114, 121, 255)
            self.track_inactive = (48, 48, 52, 255)
            self.track_inactive_hover = (54, 54, 58, 255)
            self.knob_active = (42, 42, 45, 255)
            self.knob_active_hover = (48, 48, 52, 255)
            self.knob_inactive = (42, 42, 45, 255)
            self.knob_inactive_hover = (42, 42, 45, 255)

        # dimensions
        self.switch_width = self.height * 1.8
        self.knob_padding = self.height / 5
        self.knob_size = self.height - self.knob_padding
        self.x_pos_off = self.knob_padding / 2
        self.x_pos_on = self.switch_width - self.knob_size - (self.knob_padding / 2)
        self.y_pos = self.knob_padding / 2
        self.track_radius = (self.height / 2) * max(0.0, min(1.0, rounding))
        self.knob_radius = (self.knob_size / 2) * max(0.0, min(1.0, rounding))

        # status bar
        self.bar_width = 4
        self.bar_height = self.height - self.height/5
        self.bar_spacer = 8

        # value registry
        with dpg.value_registry():
            if tag:
                self.tag = tag
                if not dpg.does_item_exist(self.tag):
                    dpg.add_bool_value(default_value=default_value, tag=self.tag)
            else:
                self.tag = dpg.add_bool_value(default_value=default_value)

        # theme to remove table padding
        with dpg.theme() as self.grid_theme:
            with dpg.theme_component(dpg.mvTable):
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, x=0, y=0)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, x=4, y=0)

        # main wrapper
        with dpg.group() as self.id:

            with dpg.table(header_row=False, width=int(width), policy=dpg.mvTable_SizingStretchProp) as self.table_id:
                dpg.bind_item_theme(self.table_id, self.grid_theme)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=self.bar_width)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=self.bar_spacer)
                dpg.add_table_column(width_stretch=True)
                dpg.add_table_column(width_fixed=True, init_width_or_weight=self.switch_width)

                with dpg.table_row():

                    # bar
                    with dpg.group():
                        with dpg.drawlist(width=0, height=(self.height / 5) / 2):  # pyright: ignore[reportArgumentType]
                            dpg.draw_rectangle(pmin=[0, 0], pmax=[0, (self.height / 5) / 2], color=[0,0,0,0])

                        with dpg.drawlist(width=self.bar_width, height=self.bar_height):  # pyright: ignore[reportArgumentType]
                            self.bar_id = dpg.draw_rectangle(
                                pmin=[0, 0], pmax=[self.bar_width, self.bar_height],
                                color=(0,0,0,0), fill=self.track_inactive,
                                thickness=0, rounding=self.knob_radius
                            )

                    with dpg.drawlist(width=self.bar_spacer, height=0):
                        dpg.draw_rectangle(pmin=[0, 0], pmax=[self.bar_spacer, 0], color=[0,0,0,0])

                    # label
                    with dpg.group():
                        with dpg.drawlist(width=0, height=self.height * 0.33) as self.spacer_id:  # pyright: ignore[reportArgumentType]
                            dpg.draw_rectangle(pmin=[0, 0], pmax=[0, self.height * 0.33], color=[0,0,0,0])
                        dpg.add_text(label)

                    # switch
                    with dpg.drawlist(width=self.switch_width, height=self.height) as self.drawlist_id:  # pyright: ignore[reportArgumentType]
                        self.bg_id = dpg.draw_rectangle(
                            pmin=[0, 0], pmax=[self.switch_width, self.height],
                            color=(0,0,0,0), fill=self.track_inactive,
                            rounding=self.track_radius, thickness=0
                        )
                        self.knob_id = dpg.draw_rectangle(
                            pmin=[self.x_pos_off, self.y_pos], pmax=[self.x_pos_off + self.knob_size, self.y_pos + self.knob_size],
                            color=(0,0,0,0), fill=self.knob_inactive,
                            rounding=self.knob_radius, thickness=0
                        )

        # click and hover handler
        with dpg.item_handler_registry() as handler:
            dpg.add_item_clicked_handler(callback=self._on_click)
            dpg.add_item_visible_handler(callback=self._update_view)

        dpg.bind_item_handler_registry(self.drawlist_id, handler)

        # initial render
        self._update_view()

    def _update_view(self):

        # text vertical alignment
        if not self._centered:
            text_size = dpg.get_text_size(self.label)
            if text_size is not None:
                text_height = text_size[1]
                spacer_height = max(0, (self.height - text_height) / 3.33)
                dpg.configure_item(self.spacer_id, height=int(spacer_height))
                self._centered = True

        # colors and position
        state = dpg.get_value(self.tag)
        is_hovered = dpg.is_item_hovered(self.drawlist_id)

        if state:
            bg_color = self.track_active_hover if is_hovered else self.track_active
            knob_color = self.knob_active_hover if is_hovered else self.knob_active
            knob_pos = [self.x_pos_on, self.y_pos]
        else:
            bg_color = self.track_inactive_hover if is_hovered else self.track_inactive
            knob_color = self.knob_inactive_hover if is_hovered else self.knob_inactive
            knob_pos = [self.x_pos_off, self.y_pos]

        # update track, knob, status bar
        dpg.configure_item(self.bg_id, fill=bg_color)
        dpg.configure_item(self.knob_id, fill=knob_color, pmin=knob_pos, pmax=[knob_pos[0] + self.knob_size, knob_pos[1] + self.knob_size])
        dpg.configure_item(self.bar_id, fill=bg_color)

    def _on_click(self, sender, app_data):
        new_val = not dpg.get_value(self.tag)
        dpg.set_value(self.tag, new_val)
        self._update_view()
        if self.callback:
            self.callback(self.tag, new_val, self.user_data)

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title='toggle switch test', width=400, height=200)

    with dpg.window(width=300, height=150):

        ts = ToggleSwitch(label='toggle 1', tag='toggle_1', width=280, height=50, rounding=0.5)
        with dpg.tooltip(ts.id):
            dpg.add_text('tooltip 1')

        ts = ToggleSwitch(width=280, height=20)
        with dpg.tooltip(ts.id):
            dpg.add_text('tooltip 2')

        ts = ToggleSwitch(label='toggle 3', width=280, height=20, rounding=0.4)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
