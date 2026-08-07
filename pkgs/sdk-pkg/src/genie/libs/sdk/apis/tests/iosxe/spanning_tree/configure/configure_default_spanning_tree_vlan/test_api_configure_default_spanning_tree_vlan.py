from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_default_spanning_tree_vlan,
)


class TestConfigureDefaultSpanningTreeVlan(TestCase):

    def test_configure_default_spanning_tree_vlan(self):
        device = Mock()

        result = configure_default_spanning_tree_vlan(
            device,
            '1-3',
            'max-age'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'default spanning-tree vlan 1-3 max-age',
            )
        )

    def test_configure_default_spanning_tree_vlan_1(self):
        device = Mock()

        result = configure_default_spanning_tree_vlan(
            device,
            '3-8',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'default spanning-tree vlan 3-8',
            )
        )
