import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9300.configure import configure_ignore_startup_config


class TestConfigureIgnoreStartupConfig(TestCase):

    def test_configure_ignore_startup_config(self):
        device = Mock()
        device.subconnections = None
        device.state_machine.current_state = 'enable'
        device.role = 'active'
        
        result = configure_ignore_startup_config(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct command
        device.configure.assert_called_once_with('system ignore startupconfig switch all')


if __name__ == '__main__':
    unittest.main()