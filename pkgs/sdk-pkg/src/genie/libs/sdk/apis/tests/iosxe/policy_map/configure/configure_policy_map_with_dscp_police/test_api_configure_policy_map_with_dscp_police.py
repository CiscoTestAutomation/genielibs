import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_with_dscp_police
)


class TestConfigurePolicyMapWithDscpPolice(unittest.TestCase):

    def test_configure_policy_map_with_dscp_police(self):
        device = Mock()

        result = configure_policy_map_with_dscp_police(
            device,
            'map2',
            'class-default',
            '1gig',
            'dscp',
            't1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map2',
              'class class-default',
              'police 1gig',
              'exit',
              'set dscp dscp table t1'],)
        )