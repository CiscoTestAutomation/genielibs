import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_on_device


class TestConfigPolicyMapOnDevice(unittest.TestCase):

    def test_config_policy_map_on_device(self):
        device = Mock()

        result = configure_policy_map_on_device(
            device,
            'test-shape',
            'class-default',
            '500000'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map test-shape',
                'class class-default',
                'shape average 500000'
            ],)
        )