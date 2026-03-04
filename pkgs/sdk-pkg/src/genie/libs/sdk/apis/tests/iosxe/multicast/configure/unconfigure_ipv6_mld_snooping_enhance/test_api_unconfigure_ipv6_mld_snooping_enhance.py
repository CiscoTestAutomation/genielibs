from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_snooping_enhance

class TestUnconfigureIpv6MldSnoopingEnhance(TestCase):

    def test_unconfigure_ipv6_mld_snooping_enhance(self):
        device = Mock()
        result = unconfigure_ipv6_mld_snooping_enhance(device, None, 101, None, None, None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 mld snooping last-listener-query-interval 101',)
        )