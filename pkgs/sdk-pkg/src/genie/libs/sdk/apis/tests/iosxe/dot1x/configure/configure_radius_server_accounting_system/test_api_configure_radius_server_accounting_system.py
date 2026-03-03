import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_radius_server_accounting_system


class TestConfigureRadiusServerAccountingSystem(TestCase):

    def test_configure_radius_server_accounting_system(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Device in enable mode

        result = configure_radius_server_accounting_system(
            device,
            0,
            0,
            15,
            'NO'
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

        self.assertIn('radius-server accounting system host-config', normalized)
        self.assertIn('line console 0', normalized)
        self.assertIn('exec-timeout 0 0', normalized)
        self.assertIn('privilege level 15', normalized)
        self.assertIn('login authentication NO', normalized)


if __name__ == '__main__':
    unittest.main()