import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_authentication_control_direction
)


class TestConfigureAuthenticationControlDirection(TestCase):

    def test_configure_authentication_control_direction(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device assumed in enable mode

        result = configure_authentication_control_direction(
            device=device,
            interface='g1/0/1',
            direction='in'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Assert that configuration was called
        device.configure.assert_called_once()

        # Assert exact commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface g1/0/1', sent_commands)
        self.assertIn('authentication control-direction in', sent_commands)


if __name__ == '__main__':
    unittest.main()