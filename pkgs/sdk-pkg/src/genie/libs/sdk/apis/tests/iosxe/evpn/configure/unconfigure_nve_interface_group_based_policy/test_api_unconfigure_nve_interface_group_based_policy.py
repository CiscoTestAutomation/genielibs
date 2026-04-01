import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_nve_interface_group_based_policy
)


class TestUnconfigureNveInterfaceGroupBasedPolicy(TestCase):

    def test_unconfigure_nve_interface_group_based_policy(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_nve_interface_group_based_policy(device, '1')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface nve 1', sent_commands)
        self.assertIn('no group-based-policy', sent_commands)


if __name__ == '__main__':
    unittest.main()