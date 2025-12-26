import dearpygui.dearpygui as dpg
from typing import Any, Optional

class Separator:
    def __init__(self, width:int=100, height:int=5, rounding:float=0.0, config:Optional[Any]=None):
        self.width = int(width)
        self.height = int(height)

        if config is not None:
            self.color = config.theme.get('colors', 'bg_secondary')
        else:
            self.color = [50, 50, 54, 255]

        self.radius = (min(self.width, self.height) / 2) * max(0.0, min(1.0, rounding))

        self.id = dpg.add_drawlist(
            width=self.width,
            height=self.height,
        )

        self.rect_id = dpg.draw_rectangle(
            pmin=(0, 0), pmax=(self.width, self.height),
            color=(0, 0, 0, 0), fill=self.color,
            rounding=self.radius,
            thickness=0,
            parent=self.id
        )
