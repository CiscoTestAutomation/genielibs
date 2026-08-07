from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_portfast,
)


class TestUnconfigureSpanningTreePortfast(TestCase):

    def test_unconfigure_spanning_tree_portfast(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast(
            device,
            True,
            True,
            False
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no spanning-tree portfast bpduguard default'
        )

    def test_unconfigure_spanning_tree_portfast_1(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast(
            device,
            False,
            True,
            False
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no spanning-tree portfast bpduguard'
        )

    def test_unconfigure_spanning_tree_portfast_2(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast(
            device,
            True,
            False,
            True
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no spanning-tree portfast bpdufilter default'
        )
