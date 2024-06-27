import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_tunnel_source


class TestConfigureTunnelSource(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          router1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['router1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_tunnel_source(self):
        result = configure_tunnel_source(self.device, 'gig1', 'tu0')
        expected_output = None
        self.assertEqual(result, expected_output)
