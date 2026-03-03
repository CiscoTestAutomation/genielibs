import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    unconfigure_authentication_event_server
)


class TestUnconfigureAuthenticationEventServer(TestCase):

    def test_unconfigure_authentication_event_server(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_authentication_event_server(
            device,
            'GigabitEthernet1/0/2',
            'dead',
            'authorize',
            '50'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn(
            'interface GigabitEthernet1/0/2',
            sent_commands
        )
        self.assertIn(
            'no authentication event server dead action authorize voice',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()