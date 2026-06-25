import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_class


class TestConfigurePolicyMapClass(unittest.TestCase):

    def test_configure_policy_map_class(self):
        device = Mock()

        result = configure_policy_map_class(
            device,
            'policy1',
            [{
                'bandwidth_percent': 40,
                'bandwidth_remaining_percent': 50,
                'class_map_name': 'test',
                'match_mode': ['dscp', 'cos'],
                'matched_value': ['cs1', 5],
                'police_cir_percent': 30,
                'policer_val': 2000000000,
                'priority_level': 3,
                'table_map_mode': 'cos',
                'table_map_name': 'test'
            }]
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map policy1',
                'class test',
                'priority level 3',
                'bandwidth percent 40',
                'bandwidth remaining percent 50',
                'set dscp cs1',
                'set cos 5',
                'set cos cos table test',
                'police rate 2000000000',
                'police cir percent 30'
            ],)
        )

    def test_configure_policy_map_class_1(self):
        device = Mock()

        result = configure_policy_map_class(
            device,
            'policy1',
            [{
                'bandwidth_percent': 40,
                'bandwidth_remaining_percent': 50,
                'class_map_name': 'test',
                'police_cir_percent': 30,
                'policer_val': 2000000000,
                'priority_level': 2
            }]
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map policy1',
                'class test',
                'priority level 2',
                'bandwidth percent 40',
                'bandwidth remaining percent 50',
                'police rate 2000000000',
                'police cir percent 30'
            ],)
        )

    def test_configure_policy_map_class_2(self):
        device = Mock()

        result = configure_policy_map_class(
            device,
            'policy1',
            [{
                'bandwidth_remaining_percent': 50,
                'class_map_name': 'test',
                'match_mode': ['dscp', 'cos'],
                'matched_value': ['cs1', 5],
                'table_map_mode': 'cos',
                'table_map_name': 'test'
            }]
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map policy1',
                'class test',
                'bandwidth remaining percent 50',
                'set dscp cs1',
                'set cos 5',
                'set cos cos table test'
            ],)
        )