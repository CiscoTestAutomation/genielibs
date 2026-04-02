from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ie3k.configure import unconfigure_ignore_startup_config


class TestUnconfigureIgnoreStartupConfig(TestCase):
    def test_unconfigure_ignore_startup_config(self):
        device = Mock()
        device.api.get_config_register = Mock(return_value='0x142')
        device.api.execute_set_config_register = Mock()

        unconfigure_ignore_startup_config(device)
        device.api.execute_set_config_register.assert_called_once_with('0x102')
