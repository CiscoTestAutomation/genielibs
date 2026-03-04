import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_authentication_event_server
)


class TestConfigureAuthenticationEventServer(TestCase):

    def test_configure_authentication_event_server(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_authentication_event_server(
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

        # Validate the commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface GigabitEthernet1/0/2', sent_commands)
        self.assertIn(
            'authentication event server dead action authorize voice',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()