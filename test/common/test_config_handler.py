from src.common.config_handler import *

# ----------------------------
# Tests
# ----------------------------

def test_get_config_value():

    old_truth = '127.0.0.1'
    old_fetched = get_config_value('general', 'host')

    assert old_fetched == old_truth

def test_set_config_value():

    old_truth = '127.0.0.1'
    new_truth = '127.0.0.2'

    set_config_value('general', 'host', new_truth)
    new_fetched = get_config_value('general', 'host')

    assert new_fetched != old_truth
    assert new_fetched == new_truth

def test_save_config():

    old_truth = '127.0.0.1'
    new_truth = '127.0.0.2'

    save_config()

    new_fetched = get_config_value('general', 'host')

    assert new_fetched != old_truth
    assert new_fetched == new_truth

def test_reload_config():

    old_truth = '127.0.0.1'
    new_truth = '127.0.0.2'

    set_config_value('general', 'host', old_truth)
    old_fetched = get_config_value('general', 'host')
    assert old_fetched == old_truth
    reload_config()
    new_fetched = get_config_value('general', 'host')
    assert new_fetched != old_truth
    assert new_fetched == new_truth
