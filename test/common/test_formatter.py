from src.common.config_handler import set_config_value
from src.common.formatter import *

# ----------------------------
# Tests
# ----------------------------

def test_format_ticket_key_simple():

    key_to_format = "15"
    key_formatted = "000015"

    assert format_ticket_key(key_to_format) == key_formatted

def test_format_ticket_key_complex():

    key_to_format = "15"
    key_formatted = "DEV-2025-000015"

    set_config_value('rei3-tickets-api', 'key_format', 'DEV-2025-{key:06d}')

    assert format_ticket_key(key_to_format) == key_formatted
