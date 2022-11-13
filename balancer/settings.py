import os
import configparser
from logging import INFO
from pathlib import Path


PROJECT_ROOT = Path(os.path.dirname(__file__)).parent

CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config', 'config.ini')

CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)


SERVERS_ADDRESSES = CONFIG['SERVERS']['ADDRESSES'].split(', ')

