import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_shape_map


class TestConfigureShapeMap(unittest.TestCase):

    def test_configure_shape_map(self):
        device = Mock()

        result = configure_shape_map(
            device,
            'test',
            [{'bandwidth': 10, 'child_policy': 'tcy1', 'class_map_name': 'tc7', 'discard_class_value': 0, 'mark_probability': 3, 'maximum_threshold': 50, 'minimum_threshold': 25, 'priority_level': 1, 'queue_limit': 1000000, 'random_detect_type': 'discard-class', 'shape_average': 44444, 'shape_average_percent': 2}],
            'service-policy'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type queueing test',
              'class tc7',
              'priority level 1',
              'shape average 44444',
              'bandwidth remaining ratio 10',
              'queue-limit 1000000 bytes',
              'service-policy tcy1',
              'random-detect discard-class 0 percent 25 50 3'],)
        )

    def test_configure_shape_map_1(self):
        device = Mock()

        result = configure_shape_map(
            device,
            'test',
            [{'bandwidth': 10, 'class_map_name': 'tc7', 'discard_class_value': 0, 'mark_probability': 3, 'maximum_threshold': 50, 'minimum_threshold': 25, 'random_detect_type': 'discard-class', 'shape_average_percent': 2},
             {'class_map_name': 'tc7', 'random_detect_type': 'discard-class-based', 'shape_average_percent': 2}],
            'service-policy'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type queueing test',
              'class tc7',
              'shape average percent 2',
              'bandwidth remaining ratio 10',
              'random-detect discard-class 0 percent 25 50 3',
              'class tc7',
              'shape average percent 2',
              'random-detect discard-class-based'],)
        )

    def test_configure_shape_map_2(self):
        device = Mock()

        result = configure_shape_map(
            device,
            'test',
            [{'bandwidth': 10, 'class_map_name': 'tc7', 'discard_class_value': 0, 'maximum_threshold': 50, 'minimum_threshold': 25, 'priority_level': 1, 'queue_limit': 1000000, 'random_detect_type': 'discard-class', 'shape_average': 44444}],
            'service-policy'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type queueing test',
              'class tc7',
              'priority level 1',
              'shape average 44444',
              'bandwidth remaining ratio 10',
              'queue-limit 1000000 bytes',
              'random-detect discard-class 0 percent 25 50'],)
        )

    def test_configure_shape_map_3(self):
        device = Mock()

        result = configure_shape_map(
            device,
            None,
            [{'bandwidth': 10, 'child_policy': 'tcy1', 'class_map_name': 'tc7', 'discard_class_value': 0, 'maximum_threshold': 50, 'minimum_threshold': 25, 'priority_level': 1, 'random_detect_type': 'dscp', 'shape_average': 44444, 'shape_average_percent': 2}],
            'service-policy',
            'map1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map1',
              'class tc7',
              'priority level 1',
              'shape average 44444',
              'bandwidth remaining ratio 10',
              'service-policy tcy1',
              'random-detect dscp 0 percent 25 50'],)
        )

    def test_configure_shape_map_4(self):
        device = Mock()

        result = configure_shape_map(
            device,
            None,
            [{'bandwidth': 10, 'class_map_name': 'tc7', 'discard_class_value': 0, 'maximum_threshold': 50, 'minimum_threshold': 25, 'random_detect_type': 'dscp', 'shape_average_percent': 2},
             {'class_map_name': 'tc7', 'random_detect_type': 'dscp-based', 'shape_average_percent': 2}],
            'service-policy',
            'map1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map1',
              'class tc7',
              'shape average percent 2',
              'bandwidth remaining ratio 10',
              'random-detect dscp 0 percent 25 50',
              'class tc7',
              'shape average percent 2',
              'random-detect dscp-based'],)
        )

    def test_configure_shape_map_5(self):
        device = Mock()

        result = configure_shape_map(
            device,
            None,
            [{'bandwidth': 10, 'class_map_name': 'tc7', 'discard_class_value': 0, 'maximum_threshold': 50, 'minimum_threshold': 25, 'priority_level': 1, 'random_detect_type': 'precedence', 'shape_average': 44444}],
            'service-policy',
            'map1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map1',
              'class tc7',
              'priority level 1',
              'shape average 44444',
              'bandwidth remaining ratio 10',
              'random-detect precedence 0 percent 25 50'],)
        )