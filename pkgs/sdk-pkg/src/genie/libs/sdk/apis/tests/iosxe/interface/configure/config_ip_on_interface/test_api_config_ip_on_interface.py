import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import config_ip_on_interface


class TestConfigIpOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Stargazer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_ip_on_interface(self):
        result = config_ip_on_interface(self.device, 'TenGigabitEthernet1/2/0/19', None, None, None, None, None, None, False, False, '', None, 'fe80:1::1', False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_config_ip_on_interface_secondary(self):
        result = config_ip_on_interface(self.device, 'TenGigabitEthernet1/2/0/19', '14.1.1.3', '255.255.255.0', None, None, None, None, False, False, '', None, None, True)
        expected_output = None
        self.assertEqual(result, expected_output)

