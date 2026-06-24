import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map
)


class TestUnconfigurePolicyMap(unittest.TestCase):

    def test_unconfigure_policy_map(self):
        device = Mock()

        result = unconfigure_policy_map(
            device=device,
            policy_name='policy1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no policy-map policy1',)
        )