import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    unconfigure_interface_evpn_ethernet_segment
)


class TestUnconfigureInterfaceEvpnEthernetSegment(TestCase):

    def test_unconfigure_interface_evpn_ethernet_segment(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = unconfigure_interface_evpn_ethernet_segment(
            device,
            'FastEthernet0/0/1'
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        # Ensure configure was called
        device.configure.assert_called_once()

        # Validate commands sent to the device
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('interface FastEthernet0/0/1', sent_commands)
        self.assertIn('no evpn ethernet-segment', sent_commands)


if __name__ == '__main__':
    unittest.main()