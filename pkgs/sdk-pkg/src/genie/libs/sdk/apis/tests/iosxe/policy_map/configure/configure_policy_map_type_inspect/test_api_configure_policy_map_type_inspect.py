from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    configure_policy_map_type_inspect,
)


class TestConfigurePolicyMapTypeInspect(TestCase):

    def test_configure_policy_map_type_inspect(self):
        self.device = Mock()
        configure_policy_map_type_inspect(
            self.device, 'pm', 'parent', 'inspect', log_param='log_param',
        )
        self.device.configure.assert_called_once_with(
            [
                'policy-map type inspect pm',
                'class type inspect parent',
                'no inspect',
                'no pass',
                'no drop',
                'inspect log_param',
            ]
        )

    def test_configure_policy_map_type_inspect_no_reset(self):
        self.device = Mock()
        configure_policy_map_type_inspect(
            self.device, 'pm', 'parent', 'drop', reset_actions=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'policy-map type inspect pm',
                'class type inspect parent',
                'drop',
            ]
        )

    def test_configure_policy_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_inspect(
                self.device, 'pm', 'parent', 'inspect',
            )
