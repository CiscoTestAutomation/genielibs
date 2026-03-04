from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_ssm_map

class TestUnconfigureIpIgmpSsmMap(TestCase):

    def test_unconfigure_ip_igmp_ssm_map(self):
        device = Mock()
        result = unconfigure_ip_igmp_ssm_map(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp ssm-map enable',)
        )