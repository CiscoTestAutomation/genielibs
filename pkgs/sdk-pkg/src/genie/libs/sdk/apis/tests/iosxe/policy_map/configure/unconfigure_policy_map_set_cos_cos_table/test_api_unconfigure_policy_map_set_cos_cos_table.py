import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_set_cos_cos_table
)


class TestUnconfigurePolicyMapSetCosCosTable(unittest.TestCase):

    def test_unconfigure_policy_map_set_cos_cos_table(self):
        device = Mock()

        result = unconfigure_policy_map_set_cos_cos_table(
            device,
            'map1',
            'class-default',
            'cos2cos'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map map1',
              'class class-default',
              'no set cos cos table cos2cos'],)
        )