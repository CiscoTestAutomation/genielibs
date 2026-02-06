import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup



class TestConfigureBgpNeighborRemoteAsFallOverAsWithPeergroup(unittest.TestCase):

    def test_configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(
            device,
            "10",
            "1002:101::2",
            "bfd",
            None,
            "neigh-gig1",
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 10",
                "neighbor 1002:101::2 peer-group neigh-gig1",
                "neighbor 1002:101::2 fall-over bfd",
            ],)
        )