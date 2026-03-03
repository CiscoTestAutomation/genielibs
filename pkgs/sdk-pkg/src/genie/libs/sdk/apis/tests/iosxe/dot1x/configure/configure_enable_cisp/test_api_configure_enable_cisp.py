import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_enable_cisp
)


class TestConfigureEnableCisp(TestCase):

    def test_configure_enable_cisp(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_enable_cisp(device)

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('cisp enable', sent_commands)


if __name__ == '__main__':
    unittest.main()