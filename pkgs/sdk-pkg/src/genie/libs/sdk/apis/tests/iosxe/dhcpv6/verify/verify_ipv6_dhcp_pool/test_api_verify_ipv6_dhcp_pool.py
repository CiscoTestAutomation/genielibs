import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcpv6.verify import verify_ipv6_dhcp_pool


class TestVerifyIpv6DhcpPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ipv6_dhcp_pool(self):
        result = verify_ipv6_dhcp_pool(self.device, 'pool1', ' 2510:1::/64', 1, 15, 5)
        expected_output = False
        self.assertEqual(result, expected_output)
