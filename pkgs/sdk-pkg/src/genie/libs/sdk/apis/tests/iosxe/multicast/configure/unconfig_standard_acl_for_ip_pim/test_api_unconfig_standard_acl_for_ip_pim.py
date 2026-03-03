from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfig_standard_acl_for_ip_pim

class TestUnconfigStandardAclForIpPim(TestCase):

    def test_unconfig_standard_acl_for_ip_pim(self):
        device = Mock()
        result = unconfig_standard_acl_for_ip_pim(device, 'vrf3001-BidigroupRP')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip access-list standard vrf3001-BidigroupRP',)
        )