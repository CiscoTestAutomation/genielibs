from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_weight
from unittest.mock import Mock


class TestConfigureBgpNeighborWeight(TestCase):

    def test_configure_bgp_neighbor_weight(self):
        self.device = Mock()
        result = configure_bgp_neighbor_weight(self.device, 200, '102.0.1.2', 100)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'neighbor 102.0.1.2 weight 100'],)
        )
