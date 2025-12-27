import os
import sys
import configparser
import copy
import ast
import dearpygui.dearpygui as dpg
from pathlib import Path

import logging
logger = logging.getLogger('prawl')

# platform thing
def get_platform():
    platform = sys.platform
    if platform.lower().startswith('win'):
        return platform
    else:
        logger.error('unsupported operating system, please use windows!')

# handles paths properly when compiled or running from source
def script_dir():
    if getattr(sys, 'frozen', False):
        # for running as executable
        return os.path.dirname(sys.executable)
    else:
        # for running as script
        return os.path.dirname(os.path.abspath(sys.argv[0]))

# settings, match, legends stats csv soon maybe idk
def data_dir():
    path = Path(script_dir()) / 'data'
    path.mkdir(parents=True, exist_ok=True)
    return path

# logs
def logs_dir():
    path = Path(script_dir()) / 'logs'
    path.mkdir(parents=True, exist_ok=True)
    return path

# resources
def res_dir() -> Path:
    path = Path(script_dir()) / 'res'
    if not path.exists():
        raise FileNotFoundError(f'missing resource directory: {path}')
    return path

class Base:
    def __init__(self, filepath, defaults):
        self.filepath = Path(filepath)
        self.defaults = defaults
        self.data = copy.deepcopy(self.defaults)
        if self.filepath.exists():
            self.load()
        else:
            self.save()

    def default(self, section, key):
        """get default value"""
        try:
            return self.defaults[section][key]
        except KeyError:
            logger.warning(f'default for [{section}].{key} not found')
            return None

    def load(self):
        """load config from file, default if missing"""
        logger.debug('loading all configs')
        parser = configparser.ConfigParser()
        parser.read(self.filepath, encoding='utf-8')
        for section, defaults in self.defaults.items():
            if not parser.has_section(section):
                continue
            # use type of default to get correct type
            for key, default in defaults.items():
                if isinstance(default, bool):
                    self.data[section][key] = parser.getboolean(section, key, fallback=default)
                elif isinstance(default, int):
                    self.data[section][key] = parser.getint(section, key, fallback=default)
                elif isinstance(default, (list, tuple)):
                    val = parser.get(section, key, fallback=str(default))
                    try:
                        self.data[section][key] = ast.literal_eval(val)
                    except (ValueError, SyntaxError):
                        self.data[section][key] = default
                else:
                    self.data[section][key] = parser.get(section, key, fallback=str(default))

    def get(self, section, key=None):
        """get config value, default if none"""
        logger.debug(f'getting value for: {section}, {key}')
        value = self.data.get(section, {}).get(key)
        if value is None:
            return self.default(section, key)
        return value

    def save_all(self):
        """save all configs to file by pulling values from DPG tags"""
        try:
            for section, options in self.defaults.items():
                for key in options.keys():
                    if dpg.does_item_exist(key):
                        value = dpg.get_value(key)
                        if value is not None:
                            self.set(section, key, value)
            self.save()
            logger.info(f'saved configuration to {self.filepath.name}')
        except Exception as e:
            logger.error(f'failed to save_all: {e}')



    # unused for now, i might switch to this later idk tho

    def set(self, section, key, value):
        """set config value"""
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value

    def save(self):
        """save config to file"""
        parser = configparser.ConfigParser()
        for section, options in self.data.items():
            parser.add_section(section)
            for key, value in options.items():
                parser.set(section, key, str(value))
        with open(self.filepath, 'w', encoding='utf-8') as f:
            parser.write(f)

    def update(self, section, key, value):
        """update value and save"""
        self.set(section, key, value)
        self.save()
