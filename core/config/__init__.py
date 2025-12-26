from pathlib import Path
from .base import script_dir, data_dir, logs_dir, get_platform, logger  # noqa: F401
from .settings import SettingsConfig
from .network import NetworkConfig
from .theme import ThemeConfig

class Config:
    def __init__(self):
        self.version = '0.3.0'
        self.settings = SettingsConfig()
        self.network = NetworkConfig()
        self.theme = ThemeConfig()

        # resources
        _root = Path(script_dir())
        self.main_font = _root / 'res' / str(self.theme.get('fonts', 'main_file'))
        self.icon_font = _root / 'res' / str(self.theme.get('fonts', 'icon_file'))
        self.icon = _root / 'res' / 'prawl-app.ico'
