import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_tunnel_with_ipsec


class TestConfigureTunnelWithIpsec(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE-A:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_tunnel_with_ipsec(self):
        result = configure_tunnel_with_ipsec(self.device, 'Tunnel50', 'ipv4', '11.11.11.1', '255.255.255.0', '2.2.2.1', '2.2.2.2', '5 2', None, None, None, 'gre', 'ipsec', 'ipsec_profile_v4_lo', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
