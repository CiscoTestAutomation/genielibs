import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_dot1x_supplicant
)


class TestConfigureDot1xSupplicant(TestCase):

    def test_configure_dot1x_supplicant(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_dot1x_supplicant(
            device,
            'ten1/0/7',
            'credentialsDemo',
            'eapProfile',
            'auto'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface Ten1/0/7', sent_commands)
        self.assertIn('dot1x pae supplicant', sent_commands)
        self.assertIn('dot1x credentials credentialsDemo', sent_commands)
        self.assertIn('dot1x supplicant eap profile eapProfile', sent_commands)
        self.assertIn('authentication port-control auto', sent_commands)


if __name__ == '__main__':
    unittest.main()