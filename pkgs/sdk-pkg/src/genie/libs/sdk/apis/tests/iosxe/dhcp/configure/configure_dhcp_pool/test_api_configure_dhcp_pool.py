import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_dhcp_pool


class TestConfigureDhcpPool(unittest.TestCase):

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

    def test_configure_dhcp_pool(self):
        result = configure_dhcp_pool(self.device, 'test', '192.168.1.10', '192.168.21.1', '255.255.255.0')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_dhcp_pool_1(self):
        result = configure_dhcp_pool(self.device, 'test1', '2.2.2.2', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_dhcp_pool_2(self):
        result = configure_dhcp_pool(self.device, 'test3', None, '172.16.1.0', '255.255.0.0')
        expected_output = None
        self.assertEqual(result, expected_output)
