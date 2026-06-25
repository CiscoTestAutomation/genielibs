import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_type_service
)


class TestUnconfigurePolicyMapTypeService(unittest.TestCase):

    def test_unconfigure_policy_map_type_service(self):
        device = Mock()

        result = unconfigure_policy_map_type_service(
            device,
            'pppoe_rar'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no policy-map type service pppoe_rar',)
        )