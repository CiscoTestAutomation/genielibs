from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ipv6_pim_rp_vrf
from unittest.mock import Mock


class TestConfigureIpv6PimRpVrf(TestCase):

    def test_configure_ipv6_pim_rp_vrf(self):
        self.device = Mock()
        result = configure_ipv6_pim_rp_vrf(self.device, 'VRF1', '2001:db8::1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ipv6 pim vrf VRF1 rp-address 2001:db8::1',)
        )
