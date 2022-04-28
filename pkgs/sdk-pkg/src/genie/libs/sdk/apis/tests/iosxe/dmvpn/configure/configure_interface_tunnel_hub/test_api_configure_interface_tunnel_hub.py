import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dmvpn.configure import configure_interface_tunnel_hub


class TestConfigureInterfaceTunnelHub(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ike-spoke2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ike-spoke2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_tunnel_hub(self):
        result = configure_interface_tunnel_hub(self.device, 'Tunnel0', '172.16.123.1', '255.255.255.0', 'Loopback101', 'OVERLAY', 'UNDERLAY', 180, 100, 'vpnprof', True, 'DMVPN', 1, False, True, True, '', True)
        expected_output = None
        self.assertEqual(result, expected_output)
