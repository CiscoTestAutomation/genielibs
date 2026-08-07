import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.configure import (
    configure_ipv6_mld_snooping_suppression,
)


class TestConfigureIpv6MldSnoopingSuppression(TestCase):

    def test_configure_ipv6_mld_snooping_suppression(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_mld_snooping_suppression(device)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ipv6 mld snooping listener-message-suppression")

    def test_configure_ipv6_mld_snooping_suppression_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_mld_snooping_suppression(device, vlan=100)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(
            sent,
            "ipv6 mld snooping vlan 100 listener-message-suppression")


if __name__ == "__main__":
    unittest.main()
