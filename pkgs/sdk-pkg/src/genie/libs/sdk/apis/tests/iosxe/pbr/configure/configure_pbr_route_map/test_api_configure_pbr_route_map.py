import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_pbr_route_map


class TestConfigurePbrRouteMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Int_HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500H
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Int_HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_pbr_route_map(self):
        result = configure_pbr_route_map(self.device, 'pbrv6_1', 'aclv6_1', '12::1:1', None, 'RED', None, None, '10', 'permit', True)
        expected_output = None
        self.assertEqual(result, expected_output)
