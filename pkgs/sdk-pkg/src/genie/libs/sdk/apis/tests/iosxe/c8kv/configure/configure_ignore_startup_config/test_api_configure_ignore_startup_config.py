import unittest
from unittest.mock import Mock, PropertyMock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.c8kv.configure import configure_ignore_startup_config


class TestConfigureIgnoreStartupConfig(unittest.TestCase):

    def setUp(self):
        self.device = Mock()
        self.device.name = 'test_c8kv'

    def test_configure_ignore_startup_config_rommon(self):
        """Test confreg 0x2142 is sent when device is in rommon/GRUB state"""
        self.device.state_machine.current_state = 'rommon'
        configure_ignore_startup_config(self.device)
        self.device.execute.assert_called_once_with('confreg 0x2142')
        self.device.configure.assert_not_called()

    def test_configure_ignore_startup_config_enable(self):
        """Test config-register 0x2142 is sent when device is not in rommon"""
        self.device.state_machine.current_state = 'enable'
        configure_ignore_startup_config(self.device)
        self.device.configure.assert_called_once_with('config-register 0x2142')
        self.device.execute.assert_not_called()

    def test_configure_ignore_startup_config_rommon_failure(self):
        """Test SubCommandFailure is raised when execute fails in rommon"""
        self.device.state_machine.current_state = 'rommon'
        self.device.execute.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ignore_startup_config(self.device)

    def test_configure_ignore_startup_config_enable_failure(self):
        """Test SubCommandFailure is raised when configure fails"""
        self.device.state_machine.current_state = 'enable'
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_ignore_startup_config(self.device)


if __name__ == '__main__':
    unittest.main()
