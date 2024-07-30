import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_class


class TestConfigurePolicyMapClass(unittest.TestCase):

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

    def test_configure_policy_map_class(self):
        result = configure_policy_map_class(self.device, 'policy1', [{'bandwidth_percent': 40,
  'bandwidth_remaining_percent': 50,
  'class_map_name': 'test',
  'match_mode': ['dscp', 'cos'],
  'matched_value': ['cs1', 5],
  'police_cir_percent': 30,
  'policer_val': 2000000000,
  'priority_level': 3,
  'table_map_mode': 'cos',
  'table_map_name': 'test'}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_policy_map_class_1(self):
        result = configure_policy_map_class(self.device, 'policy1', [{'bandwidth_percent': 40,
  'bandwidth_remaining_percent': 50,
  'class_map_name': 'test',
  'police_cir_percent': 30,
  'policer_val': 2000000000,
  'priority_level': 2}])
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_policy_map_class_2(self):
        result = configure_policy_map_class(self.device, 'policy1', [{'bandwidth_remaining_percent': 50,
  'class_map_name': 'test',
  'match_mode': ['dscp', 'cos'],
  'matched_value': ['cs1', 5],
  'table_map_mode': 'cos',
  'table_map_name': 'test'}])
        expected_output = None
        self.assertEqual(result, expected_output)
