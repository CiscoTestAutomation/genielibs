import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_dynamic_path_in_tunnel


class TestUnconfigureDynamicPathInTunnel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_dynamic_path_in_tunnel(self):
        result = unconfigure_dynamic_path_in_tunnel(self.device, 'Tunnel100', '100', False, 'vis', 'vis', True, 'igp')
        expected_output = None
        self.assertEqual(result, expected_output)
