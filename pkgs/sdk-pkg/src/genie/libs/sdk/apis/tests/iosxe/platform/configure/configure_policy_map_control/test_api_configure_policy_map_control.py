import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_policy_map_control


class TestConfigurePolicyMapControl(unittest.TestCase):

    def test_configure_policy_map_control(self):
        device = Mock()

        result = configure_policy_map_control(
            device,
            'BUILTIN_AUTOCONF_POLICY',
            '1',
            '1',
            'DMP_INTERFACE_TEMPLATE',
            'match-first',
            'do-all'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map type control subscriber BUILTIN_AUTOCONF_POLICY',
                'event identity-update match-first',
                '1 class always do-all',
                '1 activate interface-template DMP_INTERFACE_TEMPLATE'
            ],)
        )