from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_next_hop_self
from unittest.mock import Mock


class TestConfigureBgpNeighborNextHopSelf(TestCase):

    def test_configure_bgp_neighbor_next_hop_self(self):
        self.device = Mock()
        result = configure_bgp_neighbor_next_hop_self(self.device, 200, '102.0.1.2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'neighbor 102.0.1.2 next-hop-self'],)
        )
