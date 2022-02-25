import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_tunnel_interface


class TestConfigureIpOnTunnelInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300x-A:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300x-A']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_on_tunnel_interface(self):
        result = configure_ip_on_tunnel_interface(self.device, 'Tunnel60', None, None, '66:12::1', '77:12::2', 10, None, '1:2:3::4', '64', 'ipsec', 'ipsec', 'ipsecprofilev6overv6')
        expected_output = None
        self.assertEqual(result, expected_output)
