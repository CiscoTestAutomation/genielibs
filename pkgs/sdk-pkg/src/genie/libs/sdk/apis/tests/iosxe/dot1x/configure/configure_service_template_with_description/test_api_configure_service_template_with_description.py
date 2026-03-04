import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_service_template_with_description


class TestConfigureServiceTemplateWithDescription(TestCase):

    def test_configure_service_template_with_description(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_service_template_with_description(
            device,
            'cisco_des',
            'Hello world'
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

        self.assertIn('service-template cisco_des', normalized)
        self.assertIn('description Hello world', normalized)


if __name__ == '__main__':
    unittest.main()