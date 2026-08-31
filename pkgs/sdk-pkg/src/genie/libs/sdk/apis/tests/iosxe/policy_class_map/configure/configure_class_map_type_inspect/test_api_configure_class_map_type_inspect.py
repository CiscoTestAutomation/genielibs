from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import (
    configure_class_map_type_inspect,
)


class TestConfigureClassMapTypeInspect(TestCase):

    def test_configure_class_map_type_inspect_parent(self):
        self.device = Mock()
        configure_class_map_type_inspect(
            self.device,
            'parent',
            match_type='match-all',
            match_access_group=101,
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-all parent',
                'match access-group 101',
            ]
        )

    def test_configure_class_map_type_inspect_child(self):
        self.device = Mock()
        configure_class_map_type_inspect(
            self.device,
            'child1',
            match_type='match-any',
            match_protocol=['icmp', 'tcp', 'udp'],
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-any child1',
                'match protocol icmp',
                'match protocol tcp',
                'match protocol udp',
            ]
        )

    def test_configure_class_map_type_inspect_nested(self):
        self.device = Mock()
        configure_class_map_type_inspect(
            self.device,
            'parent',
            match_type='match-all',
            match_class_map='child1',
        )
        self.device.configure.assert_called_once_with(
            [
                'class-map type inspect match-all parent',
                'match class-map child1',
            ]
        )

    def test_configure_class_map_type_inspect_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_class_map_type_inspect(
                self.device, 'child1', match_protocol='icmp'
            )
