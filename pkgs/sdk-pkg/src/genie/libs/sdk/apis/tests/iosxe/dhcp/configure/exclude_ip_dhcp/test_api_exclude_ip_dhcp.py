import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import exclude_ip_dhcp


class TestExcludeIpDhcp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_exclude_ip_dhcp(self):
        result = exclude_ip_dhcp(self.device, '6.6.6.0', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_exclude_ip_dhcp_1(self):
        result = exclude_ip_dhcp(self.device, '4.4.4.4', '5.5.5.5')
        expected_output = None
        self.assertEqual(result, expected_output)
