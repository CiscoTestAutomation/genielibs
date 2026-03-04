from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_snooping_last_member_query_interval

class TestUnconfigureIpIgmpSnoopingLastMemberQueryInterval(TestCase):

    def test_unconfigure_ip_igmp_snooping_last_member_query_interval(self):
        device = Mock()
        result = unconfigure_ip_igmp_snooping_last_member_query_interval(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp snooping last-member-query-interval',)
        )