from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_router_bgp_neighbor_remote_as
from unittest.mock import Mock

class TestConfigureRouterBgpNeighborRemoteAs(TestCase):

    def test_configure_router_bgp_neighbor_remote_as(self):
        self.device = Mock()
        configure_router_bgp_neighbor_remote_as(self.device, '100', '20.20.20.2', '200')
        self.assertEqual(self.device.configure.mock_calls[0].args, (['router bgp 100', 'neighbor 20.20.20.2 remote-as 200'],))