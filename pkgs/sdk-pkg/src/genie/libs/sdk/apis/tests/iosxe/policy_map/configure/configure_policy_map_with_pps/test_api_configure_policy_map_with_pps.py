import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_with_pps
)


class TestConfigurePolicyMapWithPps(unittest.TestCase):

    def test_configure_policy_map_with_pps(self):
        device = Mock()

        result = configure_policy_map_with_pps(
            device,
            'system-cpp-policy',
            'system-cpp-police-routing-control',
            2000
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map system-cpp-policy',
              'class system-cpp-police-routing-control',
              'police rate 2000 pps'],)
        )