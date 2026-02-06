import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_router_id_peergroup_neighbor


class TestConfigureBgpRouterIdPeergroupNeighbor(unittest.TestCase):

    def test_configure_bgp_router_id_peergroup_neighbor(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_router_id_peergroup_neighbor(
            device,
            1,
            "pg-ibgp-rc",
            1,
            "102.102.102.0/24",
            "pg-ibgp-rc",
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "bgp log-neighbor-changes",
                "neighbor pg-ibgp-rc peer-group",
                "neighbor pg-ibgp-rc remote-as 1",
                "bgp listen range 102.102.102.0/24 peer-group pg-ibgp-rc",
            ],)
        )