from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_ssm_map_query_dns

class TestUnconfigureIpIgmpSsmMapQueryDns(TestCase):

    def test_unconfigure_ip_igmp_ssm_map_query_dns(self):
        device = Mock()
        result = unconfigure_ip_igmp_ssm_map_query_dns(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp ssm-map query dns',)
        )