from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_backbonefast,
)


class TestUnconfigureSpanningTreeBackbonefast(TestCase):

    def test_unconfigure_spanning_tree_backbonefast(self):
        device = Mock()

        result = unconfigure_spanning_tree_backbonefast(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'no spanning-tree backbonefast',
            )
        )