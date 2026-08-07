from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_priority,
)


class TestUnconfigureSpanningTreePriority(TestCase):

    def test_unconfigure_spanning_tree_priority(self):
        device = Mock()

        result = unconfigure_spanning_tree_priority(
            device,
            10,
            5
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            'no spanning-tree vlan 10 priority 5'
        )

    def test_unconfigure_spanning_tree_priority_1(self):
        device = Mock()

        result = unconfigure_spanning_tree_priority(
            device,
            10,
            None
        )

        self.assertEqual(result, None)
        device.configure.assert_called_once_with(
            'no spanning-tree vlan 10 priority'
        )
