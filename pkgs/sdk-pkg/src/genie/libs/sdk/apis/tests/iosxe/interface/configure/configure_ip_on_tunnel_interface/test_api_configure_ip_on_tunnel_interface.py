import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_tunnel_interface


class TestConfigureIpOnTunnelInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Hub:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C8000V
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Hub']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_on_tunnel_interface(self):
        result = configure_ip_on_tunnel_interface(self.device, 'tunnel1', '6.6.6.1', '255.255.255.0', '2.2.2.2', '1.1.1.2', 10, None, None, None, None, 'ipsec', 'P1', None, None, '100', 'ipv4')
        expected_output = None
        self.assertEqual(result, expected_output)
