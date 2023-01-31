import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.verify import verify_ipsec_tunnel_status


class TestVerifyIpsecTunnelStatus(unittest.TestCase):

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

    def test_verify_ipsec_tunnel_status(self):
        result = verify_ipsec_tunnel_status(self.device, 'Tunnel10', 5, 1, 'UP-ACTIVE')
        expected_output = True
        self.assertEqual(result, expected_output)
