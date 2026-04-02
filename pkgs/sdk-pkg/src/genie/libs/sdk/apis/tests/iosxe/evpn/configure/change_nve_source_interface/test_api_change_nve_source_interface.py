import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    change_nve_source_interface
)


class TestChangeNveSourceInterface(TestCase):

    def test_change_nve_source_interface(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = change_nve_source_interface(device, '1', 'Loopback1')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('int nve1', sent_commands)
        self.assertIn('source-interface Loopback1', sent_commands)


if __name__ == '__main__':
    unittest.main()