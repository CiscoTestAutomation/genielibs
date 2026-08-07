from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_vlan_root,
)


class TestUnconfigureSpanningTreeVlanRoot(TestCase):

    def test_unconfigure_spanning_tree_vlan_root(self):
        device = Mock()

        result = unconfigure_spanning_tree_vlan_root(
            device,
            '1,100'
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            'no spanning-tree vlan 1,100 root'
        )
