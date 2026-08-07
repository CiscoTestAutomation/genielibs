import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.l2vpn.configure import (
    configure_evpn_instance_vlan_based_flood_suppression,
)


class TestConfigureEvpnInstanceVlanBasedFloodSuppression(TestCase):

    def test_configure_evpn_instance_vlan_based_flood_suppression(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_evpn_instance_vlan_based_flood_suppression(
            device,
            "2000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "l2vpn evpn instance 2000 vlan-based",
                "encapsulation vxlan",
                "flooding-suppression address-resolution disable",
            ],
        )


if __name__ == "__main__":
    unittest.main()
