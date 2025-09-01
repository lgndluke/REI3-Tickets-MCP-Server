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

def get_config_value(section: str, key: str, fallback='') -> str:
    """
    Returns a configuration value from the given section and key.
    """
    return config.get(section, key, fallback=fallback)

def set_config_value(section: str, key: str, value: str) -> None:
    """
    Set a configuration value in the given section.
    (The changes are only applied in memory, not persisted on disk! To persist call save_config())
    """
    config.set(section, key, value)

def save_config() -> None:
    """
    Write the current config state to the config.ini file.
    """
    with open(path, 'w') as config_file:
        config.write(config_file)
