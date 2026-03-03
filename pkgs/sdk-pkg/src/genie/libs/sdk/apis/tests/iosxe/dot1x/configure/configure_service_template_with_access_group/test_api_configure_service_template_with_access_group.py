import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_service_template_with_access_group


class TestConfigureServiceTemplateWithAccessGroup(TestCase):

    def test_configure_service_template_with_access_group(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_service_template_with_access_group(
            device,
            'DefaultCriticalAccess_SRV_TEMPLATE',
            'IPV4_CRITICAL_AUTH_ACL'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate the commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # Normalize commands (strip whitespace/newlines)
        if isinstance(sent_commands, list):
            normalized = [cmd.strip() for cmd in sent_commands]
        else:
            normalized = sent_commands

        self.assertIn('service-template DefaultCriticalAccess_SRV_TEMPLATE', normalized)
        self.assertIn('access-group IPV4_CRITICAL_AUTH_ACL', normalized)


if __name__ == '__main__':
    unittest.main()