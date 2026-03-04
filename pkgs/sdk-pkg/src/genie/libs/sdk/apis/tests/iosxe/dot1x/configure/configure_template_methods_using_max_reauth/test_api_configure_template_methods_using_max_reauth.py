import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import (
    configure_template_methods_using_max_reauth
)


class TestConfigureTemplateMethodsUsingMaxReauth(TestCase):

    def test_configure_template_methods_using_max_reauth(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_template_methods_using_max_reauth(
            device,
            'DefaultWiredMabClosedAuth',
            7,
            3
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        # Template
        self.assertIn(
            'template DefaultWiredMabClosedAuth',
            sent_commands
        )

        # dot1x timers / limits
        self.assertIn(
            'dot1x timeout tx-period 7',
            sent_commands
        )
        self.assertIn(
            'dot1x max-reauth-req 3',
            sent_commands
        )


if __name__ == '__main__':
    unittest.main()