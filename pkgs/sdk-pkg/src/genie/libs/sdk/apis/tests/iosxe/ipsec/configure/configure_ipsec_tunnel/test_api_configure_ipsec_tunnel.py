import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ipsec_tunnel


class TestConfigureIpsecTunnel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipsec_tunnel(self):
        result = configure_ipsec_tunnel(self.device, 'Tunnel1', '192.168.1.1', '255.255.255.0', 'G1', 'dual-overlay', '30.30.30.2', 'global_ipsec_profile', 'OVERLAY', 'UNDERLAY')
        expected_output = None
        self.assertEqual(result, expected_output)
