import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_l2vpn_route_map


class TestConfigureBgpL2vpnRouteMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IR1101:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IR1101']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_l2vpn_route_map(self):
        result = configure_bgp_l2vpn_route_map(self.device, 'l2vpn', 1, 'pg-ibgp-rc', 'rm-bgp-no-export', 'in', 'evpn')
        expected_output = None
        self.assertEqual(result, expected_output)
