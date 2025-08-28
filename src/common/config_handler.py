import configparser

from pathlib import Path

# ----------------------------
# Load configuration file
# ----------------------------

config = configparser.ConfigParser()
path   = Path(__file__).resolve().parents[2] / "config.ini"
config.read(path)

# ----------------------------
# Functions
# ----------------------------

def get_config_value(section: str, key: str, fallback: str) -> str:
    return config.get(section, key, fallback=fallback)

def set_config_value(section: str, key: str, value: str) -> None:
    config.set(section, key, value)
