from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_ipv6_dampening
from unittest.mock import Mock


class TestConfigureBgpIpv6Dampening(TestCase):

    def test_configure_bgp_ipv6_dampening(self):
        self.device = Mock()
        result = configure_bgp_ipv6_dampening(self.device, '50', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 50', 'address-family ipv6', 'bgp dampening', 'exit-address-family'],)
        )
