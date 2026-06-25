import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_with_police_cir_percentage
)


class TestConfigurePolicyMapWithPoliceCirPercentage(unittest.TestCase):

    def test_configure_policy_map_with_police_cir_percentage(self):
        device = Mock()

        result = configure_policy_map_with_police_cir_percentage(
            device,
            'pm-acl-policer',
            'cm-acl100',
            10,
            'drop'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map pm-acl-policer',
              'class cm-acl100',
              'police cir percent 10 conform-action transmit exceed-action drop'],)
        )