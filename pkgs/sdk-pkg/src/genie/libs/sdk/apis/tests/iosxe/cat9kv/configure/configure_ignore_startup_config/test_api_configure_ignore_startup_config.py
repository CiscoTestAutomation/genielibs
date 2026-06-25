import unittest
from unittest.mock import Mock

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.cat9kv.configure import configure_ignore_startup_config


class TestConfigureIgnoreStartupConfig(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_cat9kv'

    def test_configure_ignore_startup_config_rommon(self):
        self.device.state_machine.current_state = 'rommon'
        configure_ignore_startup_config(self.device)
        self.device.execute.assert_called_once_with('confreg 0x2142')
        self.device.configure.assert_not_called()

    def test_configure_ignore_startup_config_enable(self):
        self.device.state_machine.current_state = 'enable'
        configure_ignore_startup_config(self.device)
        self.device.configure.assert_called_once_with('config-register 0x2142')
        self.device.execute.assert_not_called()

if __name__ == '__main__':
    unittest.main()