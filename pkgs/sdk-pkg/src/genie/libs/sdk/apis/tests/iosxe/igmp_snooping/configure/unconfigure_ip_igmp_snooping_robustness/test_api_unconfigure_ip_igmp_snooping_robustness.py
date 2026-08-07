import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_ip_igmp_snooping_robustness,
)


class TestUnconfigureIpIgmpSnoopingRobustness(TestCase):

    def test_unconfigure_ip_igmp_snooping_robustness(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_robustness(
            device,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "no ip igmp snooping robustness-variable")

    def test_unconfigure_ip_igmp_snooping_robustness_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_robustness(
            device,
            vlan="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "no ip igmp snooping vlan 20 robustness-variable")


if __name__ == "__main__":
    unittest.main()
