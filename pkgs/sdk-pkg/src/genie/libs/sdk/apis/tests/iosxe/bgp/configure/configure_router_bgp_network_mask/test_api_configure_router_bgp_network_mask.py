from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_router_bgp_network_mask
from unittest.mock import Mock

class TestConfigureRouterBgpNetworkMask(TestCase):

    def test_configure_router_bgp_network_mask(self):
        self.device = Mock()
        configure_router_bgp_network_mask(self.device, '100', '11.11.11.0', '255.255.255.0')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 100', 'network 11.11.11.0 mask 255.255.255.0'],))
