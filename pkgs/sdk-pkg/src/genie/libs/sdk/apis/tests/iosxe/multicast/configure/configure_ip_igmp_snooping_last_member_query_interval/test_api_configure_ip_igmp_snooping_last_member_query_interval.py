import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_igmp_snooping_last_member_query_interval,
)


class TestConfigureIpIgmpSnoopingLastMemberQueryInterval(TestCase):

    def test_configure_ip_igmp_snooping_last_member_query_interval(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_igmp_snooping_last_member_query_interval(
            device,
            "1500",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ip igmp snooping last-member-query-interval 1500",
        )


if __name__ == "__main__":
    unittest.main()
