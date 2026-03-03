import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9500.C9500_24Y4C.configure import configure_ignore_startup_config


class TestConfigureIgnoreStartupConfig(TestCase):

    def test_configure_ignore_startup_config(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Not rommon
        
        result = configure_ignore_startup_config(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('system ignore startupconfig',)
        )


if __name__ == '__main__':
    unittest.main()