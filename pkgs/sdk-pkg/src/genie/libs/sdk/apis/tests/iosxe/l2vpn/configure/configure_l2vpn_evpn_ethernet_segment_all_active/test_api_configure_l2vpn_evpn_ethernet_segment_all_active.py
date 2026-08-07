import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    configure_l2vpn_evpn_ethernet_segment_all_active,
)


class TestConfigureL2vpnEvpnEthernetSegmentAllActive(TestCase):

    def test_configure_l2vpn_evpn_ethernet_segment_all_active(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_l2vpn_evpn_ethernet_segment_all_active(
            device,
            1,
            3,
            "0012.0012.0012",
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "l2vpn evpn ethernet-segment 1",
                "identifier type 3 system-mac 0012.0012.0012",
                "redundancy all-active",
                "df-election wait-time 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
