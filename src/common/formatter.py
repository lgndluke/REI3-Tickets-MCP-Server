from .config_handler import get_config_value

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
        key_to_format = get_config_value("rei3-tickets-api", "key_format", fallback="{key:06d}")
        return key_to_format.format(key=int(key))
    except (ValueError, KeyError):
        return key
