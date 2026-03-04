from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_static_ipv6_pim_rp_address

class TestUnconfigureStaticIpv6PimRpAddress(TestCase):

    def test_unconfigure_static_ipv6_pim_rp_address(self):
        device = Mock()
        result = unconfigure_static_ipv6_pim_rp_address(device, '2001::100', 'None')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ipv6 pim vrf None rp-address 2001::100',)
        )