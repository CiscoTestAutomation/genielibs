import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_template_methods_for_dot1x
)


class TestConfigureTemplateMethodsForDot1x(TestCase):

    def test_configure_template_methods_for_dot1x(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_template_methods_for_dot1x(
            device,
            'DefaultWiredDot1xClosedAuth',
            7,
            4,
            'PMAP_DefaultWiredDot1xClosedAuth_1X_MAB'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # Template
        self.assertIn(
            'template DefaultWiredDot1xClosedAuth',
            sent_commands
        )

        # Dot1x / MAB / access-session
        self.assertIn('access-session closed', sent_commands)
        self.assertIn('access-session port-control auto', sent_commands)
        self.assertIn('dot1x pae authenticator', sent_commands)
        self.assertIn('mab', sent_commands)

        # Authentication timers
        self.assertIn('authentication periodic', sent_commands)
        self.assertIn(
            'authentication timer reauthenticate server',
            sent_commands
        )

        # Switchport configuration
        self.assertIn('switchport mode access', sent_commands)
        self.assertIn('switchport access vlan 7', sent_commands)
        self.assertIn('switchport voice vlan 4', sent_commands)

        # Service policy
        self.assertIn(
            'service-policy type control subscriber '
            'PMAP_DefaultWiredDot1xClosedAuth_1X_MAB',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()