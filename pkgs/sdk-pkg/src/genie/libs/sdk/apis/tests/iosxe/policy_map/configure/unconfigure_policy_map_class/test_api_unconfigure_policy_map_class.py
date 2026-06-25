import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_class
)


class TestUnconfigurePolicyMapClass(unittest.TestCase):

    def test_unconfigure_policy_map_class(self):
        device = Mock()

        result = unconfigure_policy_map_class(
            device,
            'map5',
            'cs5',
            'umbrella'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type umbrella map5', 'no class cs5'],)
        )

    def test_unconfigure_policy_map_class_1(self):
        device = Mock()

        result = unconfigure_policy_map_class(
            device,
            'map5',
            'cs5',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map5',
              'no class cs5'],)
        )