import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    unconfigure_policy_map_on_interface
)


class TestUnconfigurePolicyMapOnInterface(unittest.TestCase):

    def test_unconfigure_policy_map_on_interface(self):
        device = Mock()

        result = unconfigure_policy_map_on_interface(
            device,
            'Fou2/0/20',
            'map-1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Fou2/0/20', 'no policy-map map-1'],)
        )