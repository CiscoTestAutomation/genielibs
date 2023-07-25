import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import unconfigure_route_map_route_map_to_bgp_neighbor


class TestUnconfigureRouteMapRouteMapToBgpNeighbor(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_route_map_route_map_to_bgp_neighbor(self):
        result = unconfigure_route_map_route_map_to_bgp_neighbor(self.device, 65000, 'vpnv4', [{'direction': 'in', 'neighbor': '1.1.1.4', 'route_map': 'test'}], '', '')
        expected_output = None
        self.assertEqual(result, expected_output)
