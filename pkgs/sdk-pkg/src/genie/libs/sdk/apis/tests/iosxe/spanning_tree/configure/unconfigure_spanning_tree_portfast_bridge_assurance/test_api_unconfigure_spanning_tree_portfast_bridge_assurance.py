from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_portfast_bridge_assurance,
)


class TestUnconfigureSpanningTreePortfastBridgeAssurance(TestCase):

    def test_unconfigure_spanning_tree_portfast_bridge_assurance(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast_bridge_assurance(
            device,
            'edge bpduguard'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no spanning-tree portfast  edge bpduguard default'
        )
