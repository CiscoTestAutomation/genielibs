from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup
from unittest.mock import Mock


class TestConfigureBgpNeighborRemoteAsFallOverAsWithPeergroup(TestCase):

    def test_configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(self):
        self.device = Mock()
        result = configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(self.device, '65012', '10.10.10.1', None, '22479', None, '64678', '6 20')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 65012', 'neighbor 10.10.10.1 remote-as 22479', 'neighbor 10.10.10.1 local-as 64678', 'neighbor 10.10.10.1 timers 6 20'],)
        )
