import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_tunnel


class TestConfigureIpsecTunnel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          rad-vtep1:
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
        self.device = self.testbed.devices['rad-vtep1']
        self.device.connect()

    def test_configure_ipsec_tunnel(self):
        result = configure_ipsec_tunnel(self.device, 'tunnel20', '200.1.1.1', '255.255.255.255', '200.2.1.1', 'ipv4', '200.2.1.4', 'ipsec_profile_new')
        expected_output = None
        self.assertEqual(result, expected_output)
