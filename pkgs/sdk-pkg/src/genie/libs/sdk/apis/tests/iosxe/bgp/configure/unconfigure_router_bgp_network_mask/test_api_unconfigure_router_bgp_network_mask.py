from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_router_bgp_network_mask
from unittest.mock import Mock


class TestUnconfigureRouterBgpNetworkMask(TestCase):

    def test_unconfigure_router_bgp_network_mask(self):
        self.device = Mock()
        result = unconfigure_router_bgp_network_mask(self.device, 100, '40.40.40.0', '255.255.255.0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'no network 40.40.40.0 mask 255.255.255.0'],)
        )
