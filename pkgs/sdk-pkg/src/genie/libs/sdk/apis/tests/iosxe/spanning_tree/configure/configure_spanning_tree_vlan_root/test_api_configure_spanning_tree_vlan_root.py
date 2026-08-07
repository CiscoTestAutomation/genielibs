from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_vlan_root,
)


class TestConfigureSpanningTreeVlanRoot(TestCase):

    def test_configure_spanning_tree_vlan_root(self):
        device = Mock()

        result = configure_spanning_tree_vlan_root(
            device,
            '1,100',
            'primary',
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree vlan 1,100 root primary',
            )
        )

    def test_configure_spanning_tree_vlan_root_1(self):
        device = Mock()

        result = configure_spanning_tree_vlan_root(
            device,
            '1,100',
            'secondary',
            3
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree vlan 1,100 root secondary diameter 3',
            )
        )