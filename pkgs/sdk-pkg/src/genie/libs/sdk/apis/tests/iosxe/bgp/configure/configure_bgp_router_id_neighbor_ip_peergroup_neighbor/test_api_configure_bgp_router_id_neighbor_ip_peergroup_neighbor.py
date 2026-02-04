import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_router_id_neighbor_ip_peergroup_neighbor



class TestConfigureBgpRouterIdNeighborIpPeergroupNeighbor(unittest.TestCase):

    def test_configure_bgp_router_id_neighbor_ip_peergroup_neighbor(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_router_id_neighbor_ip_peergroup_neighbor(
            device,
            "1",          
            "6.25.25.2", 
            "neigh-gig1", 
        )
        self.assertIsNone(result)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "neighbor 6.25.25.2 peer-group neigh-gig1",
            ],)
        )