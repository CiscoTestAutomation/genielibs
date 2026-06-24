import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_bandwidth_remaining_policy_map


class TestConfigureBandwidthRemainingPolicyMap(unittest.TestCase):

    def test_configure_bandwidth_remaining_policy_map(self):
        device = Mock()

        result = configure_bandwidth_remaining_policy_map(
            device,
            ['child1', 'child1', 'parent'],
            '4',
            None,
            None,
            True
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map child1',
                'policy-map child1',
                'class class-default',
                'shape average percent 4',
                'service-policy parent'
            ],)
        )