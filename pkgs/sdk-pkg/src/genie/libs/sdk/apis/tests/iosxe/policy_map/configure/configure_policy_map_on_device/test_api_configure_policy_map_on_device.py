import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_on_device


class TestConfigurePolicyMapOnDevice(unittest.TestCase):

    def test_configure_policy_map_on_device(self):
        device = Mock()

        result = configure_policy_map_on_device(
            device,
            'queue',
            'qos11',
            '2000000',
            'dscp',
            '50'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map queue',
              'class qos11',
              'shape average 2000000',
              'set dscp 50'],)
        )