from src.format import *

# ----------------------------
# Tests
# ----------------------------

def test_format_ticket_key():

    key_to_format = "15"
    key_formatted = "000015"

    assert format_ticket_key(key_to_format) == key_formatted
