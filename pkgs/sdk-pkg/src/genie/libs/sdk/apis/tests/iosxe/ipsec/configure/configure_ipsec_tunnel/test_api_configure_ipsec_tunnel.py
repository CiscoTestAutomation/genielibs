import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_tunnel


class TestConfigureIpsecTunnel(unittest.TestCase):

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
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipsec_tunnel(self):
        result = configure_ipsec_tunnel(self.device, 'Tunnel1', '200.2.0.2', '255.255.255.0', '2001::99:2:4:2', 'ipv6', '2001::99:6:8:8', 'gre_profile', False, None, None, '2001::200:2:8:2/112', 'pe1_pe3_tunnel', 'gre', 'True')
        expected_output = None
        self.assertEqual(result, expected_output)
