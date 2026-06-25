import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map


class TestConfigurePolicyMap(unittest.TestCase):

    def test_configure_policy_map(self):
        device = Mock()

        result = configure_policy_map(
            device,
            'egress_policy',
            [
                {
                    'class_map_name': 'class6',
                    'priority_percent': '20'
                },
                {
                    'bandwidth_remaining_percent': '10',
                    'class_map_name': 'class-default'
                }
            ]
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map egress_policy',
                'class class6',
                'priority percent 20',
                'class class-default',
                'bandwidth remaining percent 10'
            ],)
        )