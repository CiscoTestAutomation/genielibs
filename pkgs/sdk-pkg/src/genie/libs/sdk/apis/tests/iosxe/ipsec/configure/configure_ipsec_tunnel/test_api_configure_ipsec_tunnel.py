import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_tunnel


class TestConfigureIpsecTunnel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Arcade1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Arcade1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipsec_tunnel(self):
        result = configure_ipsec_tunnel(self.device, 'Tunnel2', '55.55.55.2', '255.255.255.0', '70.70.70.70', 'ipv4', '71.71.71.71', 'nil_ips', True, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
