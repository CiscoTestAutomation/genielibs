import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import get_mgmt_ip_and_mgmt_src_ip_addresses


class TestGetMgmtIpAndMgmtSrcIpAddresses(unittest.TestCase):

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

    def test_get_mgmt_ip_and_mgmt_src_ip_addresses_with_source(self):
        result = get_mgmt_ip_and_mgmt_src_ip_addresses(self.device, '192.168.1.5')
        expected_output = ('192.168.1.6', {'192.168.1.5'})
        self.assertEqual(result, expected_output)

    def test_get_mgmt_ip_and_mgmt_src_ip_addresses(self):
        result = get_mgmt_ip_and_mgmt_src_ip_addresses(self.device)
        expected_output = ('192.168.1.6', {'192.168.1.5'})
        self.assertEqual(result, expected_output)
