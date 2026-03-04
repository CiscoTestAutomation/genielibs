from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_pim_rp_address

class TestUnconfigureIpv6PimRpAddress(TestCase):

    def test_unconfigure_ipv6_pim_rp_address(self):
        device = Mock()
        result = unconfigure_ipv6_pim_rp_address(device, '2012:AA:23::3')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ipv6 pim rp-address 2012:AA:23::3'],)
        )