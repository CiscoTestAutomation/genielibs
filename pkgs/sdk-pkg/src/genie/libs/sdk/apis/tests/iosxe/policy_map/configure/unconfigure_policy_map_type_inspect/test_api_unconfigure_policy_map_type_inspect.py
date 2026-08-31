from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.policy_map.configure import (
    unconfigure_policy_map_type_inspect,
)


class TestUnconfigurePolicyMapTypeInspect(TestCase):

    def test_unconfigure_policy_map_type_inspect(self):
        self.device = Mock()
        unconfigure_policy_map_type_inspect(
            self.device, 'pm', class_map_name='parent',
        )
        self.device.configure.assert_called_once_with(
            [
                'policy-map type inspect pm',
                'no class type inspect parent',
                'exit',
                'no policy-map type inspect pm',
            ]
        )

    def test_unconfigure_policy_map_type_inspect_delete_only(self):
        self.device = Mock()
        unconfigure_policy_map_type_inspect(self.device, 'pm')
        self.device.configure.assert_called_once_with(
            [
                'no policy-map type inspect pm',
            ]
        )

    def test_unconfigure_policy_map_type_inspect_remove_class_only(self):
        self.device = Mock()
        unconfigure_policy_map_type_inspect(
            self.device, 'pm', class_map_name='parent',
            remove_policy_map=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'policy-map type inspect pm',
                'no class type inspect parent',
                'exit',
            ]
        )

    def test_unconfigure_policy_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_policy_map_type_inspect(self.device, 'pm')
