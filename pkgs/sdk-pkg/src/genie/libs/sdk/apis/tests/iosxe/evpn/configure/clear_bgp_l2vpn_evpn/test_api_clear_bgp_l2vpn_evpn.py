import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    clear_bgp_l2vpn_evpn
)


class TestClearBgpL2vpnEvpn(TestCase):

    def test_clear_bgp_l2vpn_evpn(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = clear_bgp_l2vpn_evpn(device)

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure execute was called
        device.execute.assert_called_once()

        # Validate command sent to the device
        sent_command = device.execute.mock_calls[0].args[0]
        self.assertEqual(sent_command, 'clear bgp l2vpn evpn *')


if __name__ == '__main__':
    unittest.main()