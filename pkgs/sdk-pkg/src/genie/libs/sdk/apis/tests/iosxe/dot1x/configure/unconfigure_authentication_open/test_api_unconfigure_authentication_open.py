import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_authentication_open
)


class TestUnconfigureAuthenticationOpen(TestCase):

    def test_unconfigure_authentication_open(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_authentication_open(
            device,
            'g1/0/1'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'interface g1/0/1',
            sent_commands
        )
        self.assertIn(
            'no authentication open',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()