import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_with_no_set_dscp
)


class TestConfigurePolicyMapWithNoSetDscp(unittest.TestCase):

    def test_configure_policy_map_with_no_set_dscp(self):
        device = Mock()

        result = configure_policy_map_with_no_set_dscp(
            device,
            'map1',
            'cs5',
            1000000000,
            'dscp',
            'cs4'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map1',
              'class cs5',
              'police 1000000000',
              'no set dscp cs4'],)
        )