import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_bandwidth_remaining_policy_map
)


class TestUnconfigureBandwidthRemainingPolicyMap(unittest.TestCase):

    def test_unconfigure_bandwidth_remaining_policy_map(self):
        device = Mock()

        result = unconfigure_bandwidth_remaining_policy_map(
            device,
            ['parent', 'grandparent']
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no policy-map parent', 'no policy-map grandparent'],)
        )