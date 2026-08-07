from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_mode,
)


class TestUnconfigureSpanningTreeMode(TestCase):

    def test_unconfigure_spanning_tree_mode(self):
        device = Mock()

        result = unconfigure_spanning_tree_mode(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no spanning-tree mode'
        )
