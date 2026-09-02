from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import (
    unconfigure_class_map_type_inspect,
)


class TestUnconfigureClassMapTypeInspect(TestCase):

    def test_unconfigure_class_map_type_inspect_child(self):
        self.device = Mock()
        unconfigure_class_map_type_inspect(
            self.device,
            'child1',
            match_type='match-any',
            match_protocol=['icmp', 'tcp', 'udp'],
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-any child1',
                'no match protocol icmp',
                'no match protocol tcp',
                'no match protocol udp',
                'exit',
                'no class-map type inspect match-any child1',
            ]
        )

    def test_unconfigure_class_map_type_inspect_parent(self):
        self.device = Mock()
        unconfigure_class_map_type_inspect(
            self.device,
            'parent',
            match_type='match-all',
            match_access_group=101,
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-all parent',
                'no match access-group 101',
                'exit',
                'no class-map type inspect match-all parent',
            ]
        )

    def test_unconfigure_class_map_type_inspect_unbind_only(self):
        self.device = Mock()
        unconfigure_class_map_type_inspect(
            self.device,
            'parent',
            match_type='match-all',
            match_class_map='child1',
            remove_class_map=False,
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-all parent',
                'no match class-map child1',
                'exit',
            ]
        )

    def test_unconfigure_class_map_type_inspect_delete_only(self):
        self.device = Mock()
        unconfigure_class_map_type_inspect(
            self.device,
            'child1',
            match_type='match-any',
        )
        self.device.configure.assert_called_once_with(
            [
                'no class-map type inspect match-any child1',
            ]
        )

    def test_unconfigure_class_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            unconfigure_class_map_type_inspect(
                self.device, 'child1', match_protocol='icmp'
            )
