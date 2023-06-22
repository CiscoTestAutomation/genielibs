import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_class_parameters


class TestConfigurePolicyMapClassParameters(unittest.TestCase):

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

    def test_configure_policy_map_class_parameters(self):
        result = configure_policy_map_class_parameters(self.device, 'test', 'test', 200000, None, None, None, None, 'set-discard-class-transmit', 5, 60000000, 'set-discard-class-transmit', 5, 'set-dscp-transmit', 'dscp', 't1', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_policy_map_class_parameters_1(self):
        result = configure_policy_map_class_parameters(self.device, 'test', 'test', None, None, 30, None, None, 'transmit', None, None, None, None, 'set-dscp-transmit', 'dscp', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_policy_map_class_parameters_2(self):
        result = configure_policy_map_class_parameters(self.device, 'test', 'test', None, None, None, None, 20, 'set-discard-class-transmit', 5, None, 'transmit', None, 'set-dscp-transmit', 'dscp', 't1', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
