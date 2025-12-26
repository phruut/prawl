from pathlib import Path
from .base import Base, data_dir

class NetworkConfig(Base):
    DEFAULTS = {
        'network': {
            'match_ports': '23000-23008',
            'host_patterns': r'ec2-.+\.compute\.amazonaws\.com',
        },
        'process': {
            'executable': 'Brawlhalla.exe',
            'window_title': 'Brawlhalla',
        },
    }

    def __init__(self, filepath=None):
        self.repo_owner = 'phruut'
        self.repo_name = 'prawl'
        path = Path(filepath) if filepath else data_dir() / 'match.cfg'
        super().__init__(path, self.DEFAULTS)
