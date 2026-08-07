from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_backbonefast,
)


class TestConfigureSpanningTreeBackbonefast(TestCase):

    def test_configure_spanning_tree_backbonefast(self):
        device = Mock()

        result = configure_spanning_tree_backbonefast(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree backbonefast',
            )
        )
