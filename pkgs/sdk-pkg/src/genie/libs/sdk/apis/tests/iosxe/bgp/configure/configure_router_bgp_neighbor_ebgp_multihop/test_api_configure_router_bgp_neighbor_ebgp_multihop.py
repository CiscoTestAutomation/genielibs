from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_router_bgp_neighbor_ebgp_multihop
from unittest.mock import Mock

class TestConfigureRouterBgpNeighborEbgpMultihop(TestCase):

    def test_configure_router_bgp_neighbor_ebgp_multihop(self):
        self.device = Mock()
        configure_router_bgp_neighbor_ebgp_multihop(self.device, '100', '22.22.22.22', '2')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 100', 'neighbor 22.22.22.22 ebgp-multihop 2'],))