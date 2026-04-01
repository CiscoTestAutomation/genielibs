import unittest
from unittest import mock
from genie.libs.sdk.apis.iosxe.startup_config.configure import configure_ignore_startup_config, unconfigure_ignore_startup_config


class TestStartupConfigConfigure(unittest.TestCase):
    def test_configure_ignore_startup_config(self):
        device = mock.Mock()
        device.api.get_config_register = mock.Mock(return_value='0x102')
        device.api.execute_set_config_register = mock.Mock()
    
        configure_ignore_startup_config(device)
        device.api.execute_set_config_register.assert_called_once_with('0x142')

    def test_unconfigure_ignore_startup_config(self):
        device = mock.Mock()
        device.api.get_config_register = mock.Mock(return_value='0x2142')
        device.api.execute_set_config_register = mock.Mock()

        unconfigure_ignore_startup_config(device)
        device.api.execute_set_config_register.assert_called_once_with('0x2102')
