import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_with_type_queue
)


class TestUnconfigurePolicyMapWithTypeQueue(unittest.TestCase):

    def test_unconfigure_policy_map_with_type_queue(self):
        device = Mock()

        result = unconfigure_policy_map_with_type_queue(
            device,
            'queue',
            'llq'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no policy-map type queue llq'],)
        )