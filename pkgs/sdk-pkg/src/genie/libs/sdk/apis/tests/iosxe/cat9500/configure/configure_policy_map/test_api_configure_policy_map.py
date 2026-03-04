import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cat9k.c9500.configure import configure_policy_map


class TestConfigurePolicyMap(TestCase):

    def test_configure_policy_map(self):
        device = Mock()
        result = configure_policy_map(
            device,
            'policy1',
            [
                {'class_map_name': 'cs7', 'policer_val': '2000000000', 'priority_level': 1},
                {'class_map_name': 'cs2', 'policer_val': '1000000000', 'priority_level': 2},
                {'bandwidth_percent': 10, 'class_map_name': 'cs1'},
                {'bandwidth_percent': 10, 'class_map_name': 'cs4'},
                {'class_map_name': 'cs5', 'shape_average': '10000000000'}
            ]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify configure was called with the correct commands
        device.configure.assert_called_once_with([
            "policy-map policy1",
            "class cs7",
            "police  2000000000",
            "priority level  1",
            "class cs2",
            "police  1000000000",
            "priority level  2",
            "class cs1",
            "bandwidth percent 10",
            "class cs4",
            "bandwidth percent 10",
            "class cs5",
            "shape average 10000000000",
        ])


if __name__ == '__main__':
    unittest.main()