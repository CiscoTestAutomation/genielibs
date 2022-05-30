import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ip_on_tunnel_interface


class TestConfigureIpOnTunnelInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Galaga-4:
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
        self.device = self.testbed.devices['Galaga-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_on_tunnel_interface(self):
        result = configure_ip_on_tunnel_interface(self.device, 'tunnel20', '140.1.1.2', '255.255.255.0', '5.1.1.2', '5.1.1.1', 10, None, None, None, None, 'ipsec', 'dut1_dut2_v4IPsecProfile120', 'CLIENT-VRFv4', 'WAN-VRFv4')
        expected_output = None
        self.assertEqual(result, expected_output)
