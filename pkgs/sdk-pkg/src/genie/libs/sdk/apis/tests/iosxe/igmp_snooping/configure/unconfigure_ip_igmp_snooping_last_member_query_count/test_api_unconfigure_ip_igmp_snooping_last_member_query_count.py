import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    unconfigure_ip_igmp_snooping_last_member_query_count,
)


class TestUnconfigureIpIgmpSnoopingLastMemberQueryCount(TestCase):

    def test_unconfigure_ip_igmp_snooping_last_member_query_count(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_last_member_query_count(
            device,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "no ip igmp snooping last-member-query-count")

    def test_unconfigure_ip_igmp_snooping_last_member_query_count_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_igmp_snooping_last_member_query_count(
            device,
            vlan="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "no ip igmp snooping vlan 20 last-member-query-count")


if __name__ == "__main__":
    unittest.main()
