import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_with_percent
)


class TestConfigurePolicyMapWithPercent(unittest.TestCase):

    def test_configure_policy_map_with_percent(self):
        device = Mock()

        result = configure_policy_map_with_percent(
            device,
            'map2',
            'cs6',
            2
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map2', 'class cs6', 'police rate percent 2'],)
        )