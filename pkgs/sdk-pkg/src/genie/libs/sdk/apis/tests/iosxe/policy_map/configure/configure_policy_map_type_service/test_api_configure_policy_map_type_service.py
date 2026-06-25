import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_type_service
)


class TestConfigurePolicyMapTypeService(unittest.TestCase):

    def test_configure_policy_map_type_service(self):
        device = Mock()

        result = configure_policy_map_type_service(
            device,
            'map1',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type service map1'],)
        )