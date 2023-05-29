import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import configure_extended_acl


class TestConfigureExtendedAcl(unittest.TestCase):

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

    def test_configure_extended_acl(self):
        result = configure_extended_acl(self.device, 'test', 'permit', 'tcp', '2.2.2.2', '4.4.4.4', 3, '0.0.0.255', '0.0.255.255', [])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_extended_acl_1(self):
        result = configure_extended_acl(self.device, 'test1', 'deny', 'udp', '2.2.2.2', '4.4.4.4', None, '0.0.0.255', '0.0.255.255', [])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_extended_acl_2(self):
        result = configure_extended_acl(self.device, 'test2', 'permit', 'icmp', 'any', 'any', None, None, None, [])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_extended_acl_3(self):
        result = configure_extended_acl(self.device, 'test3', 'permit', 'tcp', 'any', 'any', 3, None, None, [])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_extended_acl_4(self):
        result = configure_extended_acl(self.device, 'test4', 'permit', 'icmp', 'any', 'any', None, None, None, [{'match_criteria': 'dscp', 'value': 10}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_extended_acl_5(self):
        result = configure_extended_acl(self.device, 'test5', 'deny', 'udp', '2.2.2.2', '4.4.4.4', None, '0.0.0.255', '0.0.255.255', [{'match_criteria': 'range', 'value': '100 500'},
 {'match_criteria': 'dscp', 'value': 40}])
        expected_output = None
        self.assertEqual(result, expected_output)
