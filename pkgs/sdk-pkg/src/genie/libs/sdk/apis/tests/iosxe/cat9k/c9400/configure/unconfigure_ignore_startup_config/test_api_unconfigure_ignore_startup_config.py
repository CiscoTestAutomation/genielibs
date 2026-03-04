import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9400.configure import unconfigure_ignore_startup_config


class TestUnconfigureIgnoreStartupConfig(TestCase):

    def test_unconfigure_ignore_startup_config(self):
        device = Mock()
        device.subconnections = None  # This will cause it to use [device]
        device.state_machine.current_state = 'enable'  # Not rommon
        device.role = 'active'  # Not standby
        
        result = unconfigure_ignore_startup_config(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no system ignore startupconfig',)
        )


if __name__ == '__main__':
    unittest.main()