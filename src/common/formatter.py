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

def format_ticket_key(key: str) -> str:
    """
    Format a ticket key using the customizable format specified inside the configuration files value 'key_format'.

    Args:
        key: The ticket key to is to be formatted. (e.g.: '15').

    :returns:
        The formatted ticket key or the unformatted key on error. (e.g.: '000015' or '15')
    """
    try:
        key_to_format = config.get("rei3-tickets-api", "key_format", fallback="{key:06d}")
        return key_to_format.format(key=int(key))
    except (ValueError, KeyError):
        return key
