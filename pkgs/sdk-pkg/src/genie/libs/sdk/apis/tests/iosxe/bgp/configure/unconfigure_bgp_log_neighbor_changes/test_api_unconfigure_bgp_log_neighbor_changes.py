from unittest import TestCase
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_bgp_log_neighbor_changes
from unittest.mock import Mock


class TestUnconfigureBgpLogNeighborChanges(TestCase):

    def test_unconfigure_bgp_log_neighbor_changes(self):
        self.device = Mock()
        result = unconfigure_bgp_log_neighbor_changes(self.device, '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 100', 'no bgp log-neighbor-changes'],)
        )
