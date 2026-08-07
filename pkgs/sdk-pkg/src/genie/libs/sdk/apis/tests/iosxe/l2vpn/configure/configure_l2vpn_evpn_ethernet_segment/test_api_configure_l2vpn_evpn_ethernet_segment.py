import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    configure_l2vpn_evpn_ethernet_segment,
)


class TestConfigureL2vpnEvpnEthernetSegment(TestCase):

    def test_configure_l2vpn_evpn_ethernet_segment(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_l2vpn_evpn_ethernet_segment(
            device,
            201,
            3,
            "aaaa.201b.201c",
            1,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "l2vpn evpn ethernet-segment 201",
                "identifier type 3 system-mac aaaa.201b.201c",
                "redundancy single-active",
                "df-election wait-time 1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
