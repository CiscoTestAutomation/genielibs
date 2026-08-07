from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_mst_priority,
)


class TestConfigureSpanningTreeMstPriority(TestCase):

    def test_configure_spanning_tree_mst_priority(self):
        device = Mock()

        result = configure_spanning_tree_mst_priority(
            device,
            0,
            4096
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['spanning-tree mst 0 priority 4096'],)
        )
