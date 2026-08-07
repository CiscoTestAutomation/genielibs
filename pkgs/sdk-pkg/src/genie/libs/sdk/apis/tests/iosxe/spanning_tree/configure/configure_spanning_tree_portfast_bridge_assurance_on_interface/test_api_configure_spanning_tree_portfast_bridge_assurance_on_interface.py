from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.spanning_tree.configure import (
    configure_spanning_tree_portfast_bridge_assurance_on_interface,
)


class TestConfigureSpanningTreePortfastBridgeAssuranceOnInterface(TestCase):

    def test_configure_spanning_tree_portfast_bridge_assurance_on_interface(self):
        device = Mock()

        result = configure_spanning_tree_portfast_bridge_assurance_on_interface(
            device,
            'TwentyFiveGigE3/0/2',
            'edge trunk'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    'interface TwentyFiveGigE3/0/2',
                    'spanning-tree portfast edge trunk',
                ],
            )
        )