import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.clear import clear_ip_bgp_af_as


class TestClearIpBgpAfAs(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          leaf1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9300
            type: cat9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['leaf1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ip_bgp_af_as(self):
        result = clear_ip_bgp_af_as(self.device, 'l2vpn evpn', '1000')
        expected_output = None
        self.assertEqual(result, expected_output)
