import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_filter_description


class TestConfigureBgpNeighborFilterDescription(unittest.TestCase):

    def test_configure_bgp_neighbor_filter_description(self):
        device = Mock()
        device.configure.return_value = ""

        neighbors = [{
            "as_id": 300,
            "damping_id": 1,
            "description": "ibgp vers SWTDATA01",
            "filter_list": 1,
            "filter_routes": "out",
            "mtu_discovery": 1,
            "neighbor_ip": "20.20.20.3",
            "neighbor_tag": "externalpg",
            "soft_reconfiguration": 1,
        }]

        result = configure_bgp_neighbor_filter_description(device, 100, neighbors)
        self.assertIsNone(result)

        device.configure.assert_called_once()
        cmds = device.configure.mock_calls[0].args[0]

        expected_cmds = [
            "router bgp 100",
            "bgp dampening 1",
            "neighbor externalpg peer-group",
            "neighbor 20.20.20.3 remote-as 300",
            "neighbor 20.20.20.3 peer-group externalpg",
            "neighbor externalpg filter-list 1 out",
            "neighbor 20.20.20.3 soft-reconfiguration inbound",
            "neighbor 20.20.20.3 description ibgp vers SWTDATA01",
            "neighbor 20.20.20.3 transport path-mtu-discovery",
        ]

        for exp in expected_cmds:
            self.assertIn(exp, cmds)