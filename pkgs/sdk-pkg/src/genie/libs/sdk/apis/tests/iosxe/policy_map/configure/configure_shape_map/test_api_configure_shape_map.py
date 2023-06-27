import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_shape_map


class TestConfigureShapeMap(unittest.TestCase):

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
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_shape_map(self):
        result = configure_shape_map(self.device, 'test', [{'bandwidth': 10,
  'child_policy': 'tcy1',
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'mark_probability': 3,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'priority_level': 1,
  'queue_limit': 1000000,
  'random_detect_type': 'discard-class',
  'shape_average': 44444,
  'shape_average_percent': 2}], 'service-policy')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_shape_map_1(self):
        result = configure_shape_map(self.device, 'test', [{'bandwidth': 10,
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'mark_probability': 3,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'random_detect_type': 'discard-class',
  'shape_average_percent': 2},
 {'class_map_name': 'tc7',
  'random_detect_type': 'discard-class-based',
  'shape_average_percent': 2}], 'service-policy')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_shape_map_2(self):
        result = configure_shape_map(self.device, 'test', [{'bandwidth': 10,
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'priority_level': 1,
  'queue_limit': 1000000,
  'random_detect_type': 'discard-class',
  'shape_average': 44444}], 'service-policy')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_shape_map_3(self):
        result = configure_shape_map(self.device, None, [{'bandwidth': 10,
  'child_policy': 'tcy1',
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'priority_level': 1,
  'random_detect_type': 'dscp',
  'shape_average': 44444,
  'shape_average_percent': 2}], 'service-policy', 'map1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_shape_map_4(self):
        result = configure_shape_map(self.device, None, [{'bandwidth': 10,
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'random_detect_type': 'dscp',
  'shape_average_percent': 2},
 {'class_map_name': 'tc7',
  'random_detect_type': 'dscp-based',
  'shape_average_percent': 2}], 'service-policy', 'map1')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_shape_map_5(self):
        result = configure_shape_map(self.device, None, [{'bandwidth': 10,
  'class_map_name': 'tc7',
  'discard_class_value': 0,
  'maximum_threshold': 50,
  'minimum_threshold': 25,
  'priority_level': 1,
  'random_detect_type': 'precedence',
  'shape_average': 44444}], 'service-policy', 'map1')
        expected_output = None
        self.assertEqual(result, expected_output)
