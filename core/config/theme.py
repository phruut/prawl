from pathlib import Path
from .base import Base, data_dir

class ThemeConfig(Base):
    DEFAULTS = {
        'colors': {

            # background
            'bg_primary': [42, 42, 45, 255],
            'bg_secondary': [50, 50, 54, 255],
            'bg_tertiary': [38, 38, 41, 255],
            'bg_quaternary': [36, 36, 39, 255],

            # text
            'text_primary': [182, 185, 186, 255],
            'text_primary_disabled': [155, 161, 168, 255],
            'text_secondary': [250, 206, 211, 255],
            'text_secondary_disabled': [215, 180, 184, 255],

            # widget hover
            'hover': [56, 56, 60, 255],
            'hover_extra': [62, 62, 68, 255],

            # widget active like button click
            'active': [255, 114, 121, 255],
            'active_hover': [255, 120, 127, 255],

            # hyperlinks
            'hyper_text': [100, 149, 238, 255],
            'hyper_hover': [29, 151, 236, 25],

            # stats
            'stats_game': [7, 190, 171, 255],
            'stats_gold': [213, 189, 4, 255],
            'stats_exp': [17, 175, 208, 255],

            # misc
            'transparent': [0, 0, 0, 0],
        },
        'fonts': {
            'main_file': 'cq-pixel-min.ttf', # font size is in increments of 7.5 pixels to be pixel perfect lol
            'main_size': 15,
            'icon_file': 'Piconic.ttf',
            'icon_size': 16,
        },
    }

    def __init__(self, filepath=None):
        path = Path(filepath) if filepath else data_dir() / 'theme.cfg'
        super().__init__(path, self.DEFAULTS)

    def get_col(self, section, key) -> list[int]:
        val = self.get(section, key)
        return self.to_rgba(val)

    @staticmethod
    def _normalize(color) -> list[int]:
        """parses color formats and returns a [r, g, b, a]"""

        # hex
        if isinstance(color, str):
            color = color.lstrip('#')
            lv = len(color)
            if lv == 6:
                return [int(color[i:i+2], 16) for i in (0, 2, 4)] + [255]
            elif lv == 8:
                return [int(color[i:i+2], 16) for i in (0, 2, 4, 6)]
            return [0, 0, 0, 255]

        # rgb / rgba
        if isinstance(color, (list, tuple)):
            if len(color) == 3:
                return [int(c) for c in color] + [255]
            elif len(color) == 4:
                return [int(c) for c in color]

        # fallback
        return [0, 0, 0, 255]

    @staticmethod
    def to_rgba(color) -> list[int]:
        return ThemeConfig._normalize(color)

    @staticmethod
    def to_hex(color) -> str:
        r, g, b, a = ThemeConfig._normalize(color)

        if a == 255:
            return f'#{r:02x}{g:02x}{b:02x}'
        return f'#{r:02x}{g:02x}{b:02x}{a:02x}'
