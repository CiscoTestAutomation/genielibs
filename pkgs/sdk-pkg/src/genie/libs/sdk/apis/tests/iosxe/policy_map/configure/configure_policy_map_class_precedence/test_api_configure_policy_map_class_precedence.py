import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_class_precedence
)


class TestConfigurePolicyMapClassPrecedence(unittest.TestCase):

    def test_configure_policy_map_class_precedence(self):
        device = Mock()

        result = configure_policy_map_class_precedence(
            device,
            'pm-marking_verify',
            'prec3',
            3
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map pm-marking_verify',
              'class prec3',
              'set precedence 3'],)
        )