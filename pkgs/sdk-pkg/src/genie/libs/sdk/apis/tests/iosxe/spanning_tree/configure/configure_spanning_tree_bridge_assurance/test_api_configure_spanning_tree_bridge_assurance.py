from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_bridge_assurance,
)


class TestConfigureSpanningTreeBridgeAssurance(TestCase):

    def test_configure_spanning_tree_bridge_assurance(self):
        device = Mock()

        result = configure_spanning_tree_bridge_assurance(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                'spanning-tree bridge assurance',
            )
        )
