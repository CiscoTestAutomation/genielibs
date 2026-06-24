import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_shape_on_device
)


class TestUnconfigurePolicyMapShapeOnDevice(unittest.TestCase):

    def test_unconfigure_policy_map_shape_on_device(self):
        device = Mock()

        result = unconfigure_policy_map_shape_on_device(
            device,
            'llq',
            'class-default'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['policy-map type queueing llq', 'class class-default', 'no shape average'],)
        )