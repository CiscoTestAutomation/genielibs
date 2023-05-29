import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_overload_rule


class TestConfigureNatOverloadRule(unittest.TestCase):

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

    def test_configure_nat_overload_rule(self):
        result = configure_nat_overload_rule(self.device, 'Loopback100', 'test4', True)
        expected_output = 'ip nat inside source list test4 interface Loopback100 overload\r\nip nat inside source list test4 interface Loopback100 overload\r\n'
        self.assertEqual(result, expected_output)

    def test_configure_nat_overload_rule_1(self):
        result = configure_nat_overload_rule(self.device, 'Loopback100', 'test4', False)
        expected_output = 'ip nat inside source list test4 interface Loopback100\r\nip nat inside source list test4 interface Loopback100\r\n'
        self.assertEqual(result, expected_output)
