from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_snooping_tcn_flood

class TestUnconfigureIpIgmpSnoopingTcnFlood(TestCase):

    def test_unconfigure_ip_igmp_snooping_tcn_flood(self):
        device = Mock()
        result = unconfigure_ip_igmp_snooping_tcn_flood(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp snooping tcn flood query count',)
        )