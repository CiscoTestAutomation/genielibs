import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_router_id_neighbor_ip_peergroup_neighbor


class TestConfigureBgpRouterIdNeighborIpPeergroupNeighbor(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_router_id_neighbor_ip_peergroup_neighbor(self):
        result = configure_bgp_router_id_neighbor_ip_peergroup_neighbor(self.device, '1', '6.25.25.2', 'neigh-gig1')
        expected_output = None
        self.assertEqual(result, expected_output)
