from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_ssmmap_static

class TestUnconfigureIpIgmpSsmmapStatic(TestCase):

    def test_unconfigure_ip_igmp_ssmmap_static(self):
        device = Mock()
        result = unconfigure_ip_igmp_ssmmap_static(device, 'ACL1', '10.1.1.1')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip igmp ssm-map static ACL1 10.1.1.1',)
        )