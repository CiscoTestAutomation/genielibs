from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_mst_configuration,
)


class TestUnconfigureSpanningTreeMstConfiguration(TestCase):

    def test_unconfigure_spanning_tree_mst_configuration(self):
        device = Mock()

        result = unconfigure_spanning_tree_mst_configuration(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ['no spanning-tree mst configuration']
        )
