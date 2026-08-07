import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import (
    configure_ip_igmp_snooping_last_member_query_count,
)


class TestConfigureIpIgmpSnoopingLastMemberQueryCount(TestCase):

    def test_configure_ip_igmp_snooping_last_member_query_count(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_last_member_query_count(
            device,
            3,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping last-member-query-count 3")

    def test_configure_ip_igmp_snooping_last_member_query_count_vlan(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_last_member_query_count(
            device,
            3,
            vlan="20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        sent = device.configure.call_args.args[0]
        self.assertIsInstance(sent, str)
        self.assertEqual(sent, "ip igmp snooping vlan 20 last-member-query-count 3")


if __name__ == "__main__":
    unittest.main()
