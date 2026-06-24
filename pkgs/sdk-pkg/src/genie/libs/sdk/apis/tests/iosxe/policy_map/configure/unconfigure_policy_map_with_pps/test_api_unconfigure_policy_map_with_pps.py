import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_with_pps
)


class TestUnconfigurePolicyMapWithPps(unittest.TestCase):

    def test_unconfigure_policy_map_with_pps(self):
        device = Mock()

        result = unconfigure_policy_map_with_pps(
            device,
            'system-cpp-policy',
            'system-cpp-police-sw-forward',
            2000
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map system-cpp-policy',
              'class system-cpp-police-sw-forward',
              'no police rate 2000 pps'],)
        )