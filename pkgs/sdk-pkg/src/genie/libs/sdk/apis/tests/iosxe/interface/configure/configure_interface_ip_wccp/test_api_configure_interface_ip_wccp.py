import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ip_wccp


class TestConfigureInterfaceIpWccp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyq-PE1:
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
        self.device = self.testbed.devices['stack3-nyq-PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_ip_wccp(self):
        result = configure_interface_ip_wccp(self.device, 'Tw1/0/10', 100, 'in', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_interface_ip_wccp_1(self):
        result = configure_interface_ip_wccp(self.device, 'Tw1/0/10', 90, 'out', False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_interface_ip_wccp_2(self):
        result = configure_interface_ip_wccp(self.device, 'Tw1/0/10', 90, None, True)
        expected_output = None
        self.assertEqual(result, expected_output)
