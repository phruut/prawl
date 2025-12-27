from .base import script_dir, data_dir, logs_dir, res_dir, get_platform  # noqa: F401
from .settings import SettingsConfig
from .network import NetworkConfig
from .theme import ThemeConfig

class Config:
    def __init__(self):
        self.version = '0.3.1'
        self.settings = SettingsConfig()
        self.network = NetworkConfig()
        self.theme = ThemeConfig()

        # resources
        self.main_font = res_dir() / str(self.theme.get('fonts', 'main_file'))
        self.icon_font = res_dir() / str(self.theme.get('fonts', 'icon_file'))
        self.icon = res_dir() / 'prawl-app.ico'
