import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.qos.configure import (
    config_policy_map_on_interface
)


class TestConfigPolicyMapOnInterface(unittest.TestCase):

    def test_config_policy_map_on_interface(self):
        device = Mock()

        result = config_policy_map_on_interface(
            device,
            'Fou2/0/20',
            'map-1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface Fou2/0/20', 'policy-map map-1'],)
        )