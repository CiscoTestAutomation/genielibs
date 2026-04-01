import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_l2vpn_evpn_router_id
)


class TestUnconfigureL2vpnEvpnRouterId(TestCase):

    def test_unconfigure_l2vpn_evpn_router_id(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_l2vpn_evpn_router_id(device, 'loopback0')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('l2vpn evpn', sent_commands)
        self.assertIn('no router-id loopback0', sent_commands)


if __name__ == '__main__':
    unittest.main()