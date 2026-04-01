import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.evpn.configure import (
    configure_evpn_ethernet_segment
)


class TestConfigureEvpnEthernetSegment(TestCase):

    def test_configure_evpn_ethernet_segment(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_evpn_ethernet_segment(
            device,
            6,                      # ethernet_segment
            0,                      # identifier_type
            None,                   # system_mac
            '00.00.00.00.00.00.00.00.01',  # esi
            True                    # single_active
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('l2vpn evpn ethernet-segment 6', sent_commands)
        self.assertIn('redundancy single-active', sent_commands)

    def test_configure_evpn_ethernet_segment_1(self):
        device = Mock()
        device.state_machine.current_state = 'enable'  # Assume device is in enable mode

        result = configure_evpn_ethernet_segment(
            device,
            7,            # ethernet_segment
            3,            # identifier_type
            '00.00.00',   # system_mac
            None,         # esi
            False         # single_active
        )

        expected_output = None
        self.assertEqual(result, expected_output)

        device.configure.assert_called_once()
        sent_commands = device.configure.mock_calls[0].args[0]

        self.assertIn('l2vpn evpn ethernet-segment 7', sent_commands)
        self.assertIn('identifier type 3 system-mac 00.00.00', sent_commands)


if __name__ == '__main__':
    unittest.main()