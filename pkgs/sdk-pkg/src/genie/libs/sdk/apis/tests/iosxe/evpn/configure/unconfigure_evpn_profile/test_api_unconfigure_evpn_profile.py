import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_evpn_profile
)


class TestUnconfigureEvpnProfile(TestCase):

    def test_unconfigure_evpn_profile(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_evpn_profile(device, 'evpn_va1', 'vlan-aware')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('l2vpn evpn profile evpn_va1 vlan-aware', sent_commands)
        self.assertIn('no evi-id', sent_commands)
        self.assertIn('exit', sent_commands)
        self.assertIn('no l2vpn evpn profile evpn_va1 vlan-aware', sent_commands)


if __name__ == '__main__':
    unittest.main()