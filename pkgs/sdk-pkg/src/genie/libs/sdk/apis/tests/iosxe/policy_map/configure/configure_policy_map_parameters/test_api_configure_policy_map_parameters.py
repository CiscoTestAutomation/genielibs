import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_parameters
)


class TestConfigurePolicyMapParameters(unittest.TestCase):

    def test_configure_policy_map_parameters(self):
        device = Mock()

        result = configure_policy_map_parameters(
            device,
            'abc',
            'tc7',
            1,
            40
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type queueing abc',
              'class tc7',
              'priority level 1',
              'bandwidth remaining ratio 40'],)
        )