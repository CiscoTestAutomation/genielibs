import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_set_cos_cos_table
)


class TestConfigurePolicyMapSetCosCosTable(unittest.TestCase):

    def test_configure_policy_map_set_cos_cos_table(self):
        device = Mock()

        result = configure_policy_map_set_cos_cos_table(
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
              'set cos cos table cos2cos'],)
        )