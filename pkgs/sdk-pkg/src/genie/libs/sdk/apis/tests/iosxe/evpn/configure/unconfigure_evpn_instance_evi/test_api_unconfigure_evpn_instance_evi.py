import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_evpn_instance_evi
)


class TestUnconfigureEvpnInstanceEvi(TestCase):

    def test_unconfigure_evpn_instance_evi(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        # If the API handles the CLI error "% EVPN instance ... does not exist",
        # simulate the device returning that output.
        device.configure.return_value = (
            "no l2vpn evpn instance 201 vlan-based\n"
            "% EVPN instance 201 does not exist"
        )

        result = unconfigure_evpn_instance_evi(device, '201', 'vlan-based')

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]
        self.assertIn('no l2vpn evpn instance 201 vlan-based', sent_commands)


if __name__ == '__main__':
    unittest.main()