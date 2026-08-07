from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    unconfigure_spanning_tree_portfast_bridge_assurance_on_interface,
)


class TestUnconfigureSpanningTreePortfastBridgeAssuranceOnInterface(TestCase):

    def test_unconfigure_spanning_tree_portfast_bridge_assurance_on_interface(self):
        device = Mock()

        result = unconfigure_spanning_tree_portfast_bridge_assurance_on_interface(
            device,
            'TwentyFiveGigE3/0/2',
            'edge trunk'
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'interface TwentyFiveGigE3/0/2',
                'no spanning-tree portfast edge trunk',
            ]
        )
